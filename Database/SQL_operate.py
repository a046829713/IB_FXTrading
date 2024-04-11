from Database import router
from sqlalchemy import text
import pandas as pd
from utils import Debug_tool


class DB_operate():
    
    def write_Dateframe(self, df: pd.DataFrame, table_name: str, exists='replace', if_index=True):
        """
            # 資料庫配置：某些資料庫預設配置可能會要求明確提交commit。
            to write pandas Dateframe
            symbol_name or tablename: 
        """
        try:
            self.userconn = router.Router().mysql_conn
            with self.userconn as conn:
                table_name = table_name.lower()  # 在windows 裡面,MySQL 表名為小寫
                df.to_sql(table_name, con=conn,
                          if_exists=exists, index=if_index)                

                conn.commit()
        except:
            Debug_tool.debug.print_info()
    
    def get_db_data(self, text_msg: str) -> list:
        """
            專門用於select from
        """
        try:
            self.userconn = router.Router().mysql_conn
            with self.userconn as conn:

                result = conn.execute(
                    text(text_msg)
                )
                # 資料範例{'Date': '2022/07/01', 'Time': '09:25:00', 'Open': '470', 'High': '470', 'Low': '470', 'Close': '470', 'Volume': '10'}

                return list(result)
        except:
            Debug_tool.debug.print_info()

    def change_db_data(self, text_msg: str) -> None:
        """ 用於下其他指令
        Args:
            text_msg (str): SQL_Query
        Returns:
            None
        """
        try:
            self.userconn = router.Router().mysql_conn
            with self.userconn as conn:
                conn.execute(text(text_msg))
                conn.commit()  # 在这里调用commit来确保更改被保存
        except:
            Debug_tool.debug.print_info()

    def read_Dateframe(self, text_msg: str) -> pd.DataFrame:
        """
            to get pandas Dateframe
            symbol_name: 'btcusdt-f'
        """
        try:
            self.userconn = router.Router().mysql_conn
            with self.userconn as conn:
                return pd.read_sql(text_msg, con=conn)
        except:
            Debug_tool.debug.print_info()




class SqlSentense():
    @staticmethod
    def create_table_name(tb_symbol_name: str) -> str:
        """ to create 1 min """
        sql_query = f"""CREATE TABLE `IBData`.`{tb_symbol_name}`(
                `Datetime` DATETIME NOT NULL,
                `Open` FLOAT NOT NULL,
                `High` FLOAT NOT NULL,
                `Low` FLOAT NOT NULL,
                `Close` FLOAT NOT NULL,                
                PRIMARY KEY(`Datetime`)
                );"""

        return sql_query

    @staticmethod
    def insert_data(table_naem: str, result: dict) -> str:
        """
        Args:
            result (dict): 插入資料：
                        {
                        'DateTime': '2024-03-29 05:15:00',
                          'Open': 151.386,
                          'High': 151.386,
                          'Low': 151.385,
                          'Close': 151.385,
                          }

        Returns:
            str: 返回要执行的SQL语句
        """

        sql_query = f"""
                    INSERT INTO `{table_naem}` 
                    (`Datetime`, `Open`, `High`, `Low`, `Close`)
                    VALUES 
                    ('{result['Datetime']}', '{result['Open']}', 
                    '{result['High']}', '{result['Low']}', '{result['Close']}');
                    """

        return sql_query

    # @staticmethod
    # def createUsers() -> str:
    #     sql_query = """
    #         CREATE TABLE users (
    #             phone_number VARCHAR(255) PRIMARY KEY NOT NULL,
    #             binance_api_account VARCHAR(255) NOT NULL,
    #             binance_api_passwd VARCHAR(255) NOT NULL,
    #             line_token VARCHAR(255) NOT NULL
    #         );

    #     """
    #     return sql_query

    # @staticmethod
    # def createlastinitcapital() -> str:
    #     sql_query = """CREATE TABLE `lastinitcapital` (
    #     `ID` varchar(255) NOT NULL,
    #     `capital` int NOT NULL,
    #     PRIMARY KEY (`ID`)
    #     );"""

    #     return sql_query

    # @staticmethod
    # def createsysstatus() -> str:
    #     sql_query = """CREATE TABLE `crypto_data`.`sysstatus`(`ID` varchar(255) NOT NULL,`systeam_datetime` varchar(255) NOT NULL,PRIMARY KEY(`ID`));"""
    #     return sql_query

    # @staticmethod
    # def createorderresult() -> str:
    #     sql_query = """
    #             CREATE TABLE `crypto_data`.`orderresult`(
    #                 `orderId` BIGINT NOT NULL,
    #                 `order_info` TEXT NOT NULL,
    #                 PRIMARY KEY(`orderId`)
    #             );
    #         """
    #     return sql_query

    # @staticmethod
    # def createinterval_record() -> str:
    #     sql_query = """
    #             CREATE TABLE `crypto_data`.`interval_record`(
    #                 `ID` varchar(255) NOT NULL,
    #                 `lastportfolioadjustmenttime` varchar(255) NOT NULL,
    #                 PRIMARY KEY(`ID`));
    #         """
    #     return sql_query
