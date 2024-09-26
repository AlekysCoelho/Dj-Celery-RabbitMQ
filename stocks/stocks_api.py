from typing import List

from ninja import Router, Schema

from .models import Stock
from .tasks import api_stock

router = Router()


class Message(Schema):
    message: str


class StockShema(Schema):
    ticker: str


@router.get("/tickers/", response=List[StockShema])
def list_stocks(request):
    queryset = Stock.objects.all()
    return queryset


@router.post("/ticker/", response={200: Message, 400: Message})
def post_stock(request, data: StockShema):

    if data.ticker:
        api_stock.delay(data.ticker)
        return 200, {"message": "added new ticker"}
