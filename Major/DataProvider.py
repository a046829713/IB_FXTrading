from Database import SQL_operate
from Major.DataTransformer import Datatransformer
import time
class DataProvider():
    def __init__(self) -> None:
        self.SQL = SQL_operate.DB_operate()
        self.datatransformer = Datatransformer()

    def getsymboldata(self,symbol_name:str,freq:int,save=False):
        df = self.SQL.read_Dateframe(f"select * from  `{symbol_name.lower()}-1m`")
        df = self.datatransformer.get_tradedata(df,freq=freq)

        if save:
            df.to_csv(f"{symbol_name}-{freq}-Min.csv")