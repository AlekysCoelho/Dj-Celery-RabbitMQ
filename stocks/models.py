from django.db import models
from django.utils.translation import gettext_lazy as _


class Stock(models.Model):
    """"""

    ticker = models.CharField(
        _("Ticker"),
        max_length=30,
        help_text="The ticker for Apple is AAPL, Vale is VALE3.SA... ",
    )
    current_price = models.FloatField(null=True)
    current_open = models.FloatField(null=True)
    pe_ratio = models.FloatField(null=True)
    moment = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.ticker} - R$ {self.current_price}"
