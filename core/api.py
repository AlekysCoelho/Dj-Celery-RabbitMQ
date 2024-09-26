from ninja import NinjaAPI

from stocks.stocks_api import router as stocks_router

api = NinjaAPI()
api.add_router("/stocks/", stocks_router)
