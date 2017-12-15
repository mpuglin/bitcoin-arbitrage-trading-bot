import settings
from exchange import Exchange


class Spread:
    def __init__(self, exchange_one: Exchange, exchange_two: Exchange) -> None:
        if exchange_one.currency_pair != exchange_two.currency_pair:
            raise AttributeError('Spread between different currency pairs is not supported')
        self.exchange_one = exchange_one
        self.exchange_two = exchange_two
        self.spread = self._calculate_spread()

    def __str__(self) -> str:
        return self.summary

    @property
    def summary(self):
        return f'{self.exchange_buy} [{self.exchange_buy.last_ask_price}] -> ' \
               f'{self.exchange_sell} [{self.exchange_sell.last_bid_price}] -> ' \
               f'Spread: {self.spread}'

    def _calculate_spread(self) -> float:
        d1 = self.exchange_one.last_bid_price - self.exchange_two.last_ask_price
        d2 = self.exchange_two.last_bid_price - self.exchange_one.last_ask_price

        if d1 > d2:
            self.exchange_buy = self.exchange_two
            self.exchange_sell = self.exchange_one
        else:
            self.exchange_buy = self.exchange_one
            self.exchange_sell = self.exchange_two

        return max(d1, d2)

    def is_above_notification_thresehold(self) -> bool:
        return self.spread > settings.MINIMUM_SPREAD_NOTIFICATION

    def is_above_trading_thresehold(self) -> bool:
        return self.spread > settings.MINIMUM_SPREAD_TRADING