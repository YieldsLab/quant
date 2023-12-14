import time

import numpy as np

from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_exchange import AbstractExchange
from core.models.symbol import Symbol


class TWAP:
    def __init__(self, config_service: AbstractConfig):
        self.config = config_service.get("position")

    def calculate(self, symbol: Symbol, exchange: AbstractExchange):
        current_time = 0
        timepoints = []
        twap_duration = self.config["twap_duration"]

        while current_time < twap_duration:
            bids, ask = self._fetch_book(symbol, exchange)

            timepoints.append((bids[:, 0], ask[:, 0]))

            time_interval = twap_duration / len(bids)
            current_time += time_interval

            time.sleep(time_interval)

            twap_value = self._twap(timepoints)

            yield round(twap_value, symbol.price_precision)

    def _fetch_book(self, symbol: Symbol, exchange: AbstractExchange):
        bids, asks = exchange.fetch_order_book(symbol)
        return np.array(bids), np.array(asks)

    @staticmethod
    def _twap(order_book):
        timepoints = np.vstack(order_book)
        prices = timepoints[:, 0]
        total_timepoints = len(prices)
        return np.sum(prices) / total_timepoints
