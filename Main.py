from ibapi.client import EClient
from ibapi.common import BarData
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from common import change_to_taiwan_time_zone, generate_range_day
import time
from Database import SQL_operate
import pandas as pd
import json
import datetime


class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.hisotry_datas = []
        self.SQL = SQL_operate.DB_operate()        
        self.symbols = ['USD.HKD']  # 示例多商品列表
        self.symbol = None

    def nextValidId(self, orderId: int):
        # ，我終於理解到為甚麼需要reqID了,
        # 因為系統只是將查詢的結果打包回來給妳，至於這個reqID 只是讓發起的使用者可以用來辨別是哪一次所發起的。


        # 可以用來查詢某個Contract的歷史資料起點
        # self.reqHeadTimeStamp(4101, self.createContract('USD.CAD'), "MIDPOINT", 1, 1)
        
        # 根據輸入訊息來篩選相關的商品
        # self.reqMatchingSymbols(218, "USD")        

        # 資料回補
        self.load_each_symbol(self.symbol)


    def load_each_symbol(self, symbol):
        #  運用遞規函數的概念來解決這個問題
        if symbol is None:
            symbol = self.symbols[0]
            self.symbol = symbol

        else:
            index = self.symbols.index(symbol)
            # to determin index and check len
            if index + 1 == len(self.symbols):
                return
            else:
                symbol = self.symbols[index + 1]
                self.symbol = symbol

        all_df = self.SQL.read_Dateframe(
            f"select Datetime from `{symbol}-1m`  order by Datetime DESC limit 30000;")
        
        
        all_df['Datetime'] = all_df['Datetime'].astype(str)
        self.datetimes = all_df['Datetime'].to_list()

        if self.datetimes:
            last_date = self.datetimes[0]
            def change_datetime_format(input_datetime): return datetime.datetime.strptime(
                input_datetime, "%Y-%m-%d %H:%M:%S").strftime("%Y%m%d %H:%M:%S")
            self.reload_History_data(
                symbol_name=symbol, endDateTime=change_datetime_format(last_date))
            # 2024-04-04 20:32:00
        else:
            self.reload_History_data(
                symbol_name=symbol, endDateTime="20100101 00:00:00")

    def createContract(self, symbol_name: str):
        # 基礎貨幣 # 計價貨幣
        BaseCurrency, QuoteCurrency = symbol_name.split('.')

        # 寫入資料庫的表名稱
        self.table_name = symbol_name + '-1m'

        # 設定外匯合約的屬性
        contract = Contract()
        contract.symbol = BaseCurrency  # 修改為正確的貨幣對符號
        contract.secType = "CASH"  # 外匯使用 "CASH"
        contract.currency = QuoteCurrency
        contract.exchange = "IDEALPRO"

        return contract

    def reload_History_data(self, symbol_name: str, endDateTime: str):
        # 建立合約
        contract = self.createContract(symbol_name=symbol_name)

        # 時間頻率
        durationStr = "5 D"

        endDateTimes = generate_range_day(
            durationStr, endDateTime)  # 從2010年1月1日開始 # 尚未有時區

        self.reload_times = len(endDateTimes)

        count = 1
        for day in endDateTimes:
            print(f"目前回補日期:{day}")
            # 正確的時間格式
            self.reqHistoricalData(reqId=count,
                                   contract=contract,
                                   endDateTime=day,
                                   durationStr=durationStr,
                                   barSizeSetting="1 min",
                                   whatToShow="MIDPOINT",
                                   useRTH=1,
                                   formatDate=1,
                                   keepUpToDate=False,
                                   chartOptions=[])

            count += 1
            time.sleep(0.5)

    def historicalData(self, reqId: int, bar: BarData):
        """        
        # Historical Data: Date: 20240328 17:15:00 US/Eastern, Open: 151.386, High: 151.3925, Low: 151.3655, Close: 151.3865, Volume: -1, WAP: -1, BarCount: -1
        # Historical Data: Date: 20240328 18:00:00 US/Eastern, Open: 151.3865, High: 151.4545, Low: 151.3725, Close: 151.4175, Volume: -1, WAP: -1, BarCount: -1

        # ====================================================================================
        # 2024-04-02 04:57:00 151.653 151.6545 151.6465 151.649 -1 -1 -1
        # 2024-04-02 04:58:00 151.649 151.6595 151.6485 151.6565 -1 -1 -1
        # 2024-04-02 04:59:00 151.6565 151.6565 151.645 151.647 -1 -1 -1
        # 2024-04-02 05:15:00 151.6725 151.6725 151.656 151.6605 -1 -1 -1
        # 2024-04-02 05:16:00 151.6605 151.665 151.6415 151.642 -1 -1 -1
        # 2024-04-02 05:17:00 151.642 151.6435 151.628 151.6335 -1 -1 -1
        # 2024-04-02 05:18:00 151.6335 151.643 151.626 151.643 -1 -1 -1
        # 2024-04-02 05:19:00 151.643 151.643 151.642 151.6425 -1 -1 -1
        # ====================================================================================
        # 2024-04-03 08:44:00 151.52 151.5215 151.518 151.518 -1 -1 -1
        # 2024-04-03 08:45:00 151.518 151.527 151.5155 151.5205 -1 -1 -1
        # 2024-04-03 08:46:00 151.5205 151.527 151.5205 151.523 -1 -1 -1
        # 2024-04-03 08:47:00 151.523 151.5255 151.515 151.519 -1 -1 -1
        # 2024-04-03 08:48:00 151.519 151.5225 151.5045 151.515 -1 -1 -1
        # 2024-04-03 08:49:00 151.515 151.5175 151.506 151.5155 -1 -1 -1
        # 2024-04-03 08:50:00 151.5155 151.52 151.514 151.519 -1 -1 -1


        Args:
            reqId (int): _description_
            bar (BarData): _description_
        """
        date = change_to_taiwan_time_zone(bar.date)

        # 創建一個包含所有資料的字典
        bar_data = {
            'Datetime': date,
            'Open': bar.open,
            'High': bar.high,
            'Low': bar.low,
            'Close': bar.close,
        }

        # 將字典轉換為 Series 並添加到列表中
        self.hisotry_datas.append(bar_data)

    def historicalDataEnd(self, reqId: int, start: str, end: str):
        print(f'End of Historical Data,reqId = {reqId}')
        print('*'*120)

        if reqId == self.reload_times:
            clean_data = self.filter_same_date(self.hisotry_datas)
            # prepar insert datas
            data_to_insert = []
            for each_data in clean_data:
                if each_data['Datetime'] not in self.datetimes:
                    data_to_insert.append(each_data)

            if data_to_insert:
                # 使用批量插入操作将数据插入数据库
                self.SQL.write_Dateframe(df=pd.DataFrame(data_to_insert),
                                         table_name=self.table_name,
                                         exists='append',
                                         if_index=False)

            print(f"table name:{self.table_name}, reload complete!")
            self.hisotry_datas.clear()  # 清除資料以準備下一商品的數據
            self.load_each_symbol(self.symbol)

    def filter_same_date(self, data: list):
        # Use a list comprehension to filter out duplicate datetime entries
        unique_data = []
        seen_datetimes = set()
        for entry in data:
            if entry["Datetime"] not in seen_datetimes:
                seen_datetimes.add(entry["Datetime"])
                unique_data.append(entry)

        return unique_data
    
    def headTimestamp(self, reqId:int, headTimestamp:str):
        print("HeadTimestamp. ReqId:", reqId, "HeadTimeStamp:", headTimestamp)


    def symbolSamples(self, reqId: int, contractDescriptions):
        print("Symbol Samples. Request Id: ", reqId)
        for contractDescription in contractDescriptions:
            derivSecTypes = ""
            for derivSecType in contractDescription.derivativeSecTypes:
                derivSecTypes += " "
                derivSecTypes += derivSecType

                if contractDescription.contract.secType == 'CASH':
                    print("Contract: conId:%s, symbol:%s, secType:%s primExchange:%s, "
                        "currency:%s, derivativeSecTypes:%s, description:%s, issuerId:%s" % (
                        contractDescription.contract.conId,
                        contractDescription.contract.symbol,
                        contractDescription.contract.secType,
                        contractDescription.contract.primaryExchange,
                        contractDescription.contract.currency, derivSecTypes,
                        contractDescription.contract.description,
                        contractDescription.contract.issuerId))

app = TestApp()
app.connect("127.0.0.1", 7497, clientId=1)
app.run()
