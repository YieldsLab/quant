import asyncio
from enum import Enum, auto
from itertools import product
from random import shuffle

from core.commands.account import UpdateAccountSize
from core.commands.backtest import BacktestRun
from core.commands.broker import Subscribe, UpdateSettings
from core.models.broker import MarginMode, PositionMode
from core.interfaces.abstract_system import AbstractSystem
from core.queries.broker import GetAccountBalance, GetSymbols
from core.queries.portfolio import GetTopStrategy

from .trading_context import TradingContext


class SystemState(Enum):
    BACKTESTING = auto()
    OPTIMIZATION = auto()
    TRADING = auto()
    STOPPED = auto()


class TrendSystem(AbstractSystem):
    def __init__(self, context: TradingContext, state: SystemState = SystemState.BACKTESTING):
        super().__init__()
        self.context = context
        self.state = state
        self.signals = []

    async def start(self):
        while True:
            match self.state:
                case SystemState.BACKTESTING:
                    await self._run_backtest()
                case SystemState.OPTIMIZATION:
                    await self._run_optimization()
                case SystemState.TRADING:
                    await self._run_trading()
                case SystemState.STOPPED:
                    return

    async def _run_backtest(self):
        async for actors in self._generate_actors():
            await asyncio.gather(*[actor.start() for actor in actors])

            signal = actors[0]

            await self.dispatcher.execute(
                BacktestRun(self.context.datasource, signal.symbol, signal.timeframe, self.context.lookback, self.context.batch_size))

            await asyncio.gather(*[actor.stop() for actor in actors])

            self.signals.append(signal)

        self.state = SystemState.OPTIMIZATION
            
    async def _run_optimization(self):
       strategies = await self.dispatcher.query(GetTopStrategy(num=20))
       print(strategies)
       
       self.state = SystemState.TRADING

    async def _run_trading(self):
        strategies = await self.dispatcher.query(GetTopStrategy(num=1))
        symbols = [strategy[1] for strategy in strategies]

        for symbol in symbols:
            await self.dispatcher.execute(
                UpdateSettings(symbol, self.context.leverage, PositionMode.ONE_WAY, MarginMode.ISOLATED))
   
        symbols_and_timeframes = sorted(list(product(symbols, self.context.timeframes)), key=lambda x: x[1])
       
        await self.dispatcher.execute(Subscribe(symbols_and_timeframes))

    async def _generate_actors(self):
        account_size = await self.dispatcher.query(GetAccountBalance())
        await self.dispatcher.execute(UpdateAccountSize(account_size))
        
        symbols = await self.dispatcher.query(GetSymbols())
        symbols = [symbol for symbol in symbols if symbol.name in self.context.symbols if len(self.context.symbols) > 0]
        shuffle(symbols)
        symbols_and_timeframes = sorted(list(product(symbols, self.context.timeframes)), key=lambda x: x[1])

        for symbol, timeframe in symbols_and_timeframes:
            executor_actor = self.context.executor_factory.create_actor(symbol, timeframe, live=False)
            position_actor = self.context.position_factory.create_actor(symbol, timeframe)
            risk_actor = self.context.risk_factory.create_actor(symbol, timeframe)

            for path, strategy_name, strategy_parameters in self.context.strategies:
                signal_actor = self.context.signal_factory.create_actor(
                    symbol, timeframe, f'./wasm/{path}.wasm', strategy_name, strategy_parameters)

                yield signal_actor, position_actor, risk_actor, executor_actor

