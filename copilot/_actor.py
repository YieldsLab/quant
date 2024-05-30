import logging

from core.actors import BaseActor
from core.interfaces.abstract_llm_service import AbstractLLMService
from core.models.risk_type import SignalRiskType
from core.models.side import SignalSide
from core.queries.copilot import EvaluateSignal

from ._prompt import signal_risk_prompt, system_prompt

CopilotEvent = EvaluateSignal

logger = logging.getLogger(__name__)


class CopilotActor(BaseActor):
    _EVENTS = [EvaluateSignal]

    def __init__(self, llm: AbstractLLMService):
        super().__init__()
        self.llm = llm

    async def on_receive(self, event: CopilotEvent):
        handlers = {
            EvaluateSignal: self._evaluate_signal,
        }

        handler = handlers.get(type(event))

        if handler:
            return await handler(event)

    async def _evaluate_signal(self, msg: EvaluateSignal) -> SignalRiskType:
        signal = msg.signal
        side = "LONG" if signal.side == SignalSide.BUY else "SHORT"
        prompt = signal_risk_prompt.format(current_bar=str(signal.ohlcv), side=side)

        logger.info(f"Signal Prompt: {prompt}")

        answer = await self.llm.call(system_prompt, prompt)

        logger.info(f"LLM Answer: {answer}")

        risk_level_enum = SignalRiskType.from_string(answer)
        return risk_level_enum