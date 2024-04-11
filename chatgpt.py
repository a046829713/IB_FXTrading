from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import datetime

class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def historicalData(self, reqId, bar):
        print(f"Time: {bar.date}, Open: {bar.open}, High: {bar.high}, Low: {bar.low}, Close: {bar.close}, Volume: {bar.volume}")

app = TestApp()
app.connect("127.0.0.1", 4001, clientId=100)

contract = Contract()
contract.symbol = "AAPL"
contract.secType = "STK"
contract.currency = "USD"
contract.exchange = "SMART"

queryTime = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime("%Y%m%d %H:%M:%S")

app.reqHistoricalData(1, contract, queryTime, "1 D", "1 hour", "MIDPOINT", 1, 1, False, [])

app.run()
