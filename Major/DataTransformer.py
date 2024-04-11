import pandas as pd
import time

class Datatransformer:
    def get_tradedata(self, original_df: pd.DataFrame, freq: int = 30):
        """
            將已經是台灣時區的資料轉換成需要是candle 區間
            採用IB 官方向前機制
        Args:
            original_df (pd.DataFrame):
                data from sql
            freq (int): 
                "this is resample time like"

        """
        df = original_df.copy()
        df.set_index("Datetime", inplace=True, drop=False)
        df = self.drop_colunms(df)
        # 採用biance 向前機制
        new_df = pd.DataFrame()
        new_df['Open'] = df['Open'].resample(
            rule=f'{freq}min', label="left").first()
        new_df['High'] = df['High'].resample(
            rule=f'{freq}min', label="left").max()
        new_df['Low'] = df['Low'].resample(
            rule=f'{freq}min', label="left").min()
        new_df['Close'] = df['Close'].resample(
            rule=f'{freq}min', label="left").last()


        # 去除全為NaN的行（即在該時間範圍內沒有交易的情況）
        new_df.dropna(how='all', inplace=True)

        return new_df        


    def drop_colunms(self, df: pd.DataFrame):
        """
            拋棄不要的Data

        """
        for key in df.columns:
            if key not in ['Datetime', 'Open', 'High', 'Low', 'Close']:
                df = df.drop(columns=[key])

        return df

    