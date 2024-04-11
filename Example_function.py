from Major.DataProvider import DataProvider
from EIIE.lib import Train_neural_networks
from EIIE.lib.simple_evaluate import evaluate_train_test_performance
from Database import SQL_operate
import matplotlib.pyplot as plt

def example_get_symbolsdata():
    """
        introduction:
            this function is for download history data to experiment.

    """
    app = DataProvider()
    symbols = ['USD.JPY', 'USD.CAD']
    for _each_symbol_name in symbols:
        app.getsymboldata(symbol_name=_each_symbol_name,freq=30,save=True)

def example_Train_neural_networks():
    Train_neural_networks.train(Train_data_path='EIIE/simulation/train_data.csv',
                                Meta_path="",
                                Train_path="EIIE\Train\policy_EIIE.pt",
                                episodes=100000,
                                save=True,
                                pre_train=False,
                                )  # True


def example_simple_evaluate():
    evaluate_train_test_performance(Train_data_path=r'EIIE\simulation\train_data.csv',
                                    Test_data_path=r'EIIE\simulation\test_data.csv',
                                    Meta_path=r'EIIE\Meta\policy_EIIE.pt')





def test_data(symbol:str):
    # 只是想要用來查看資料是否有異常
    SQL = SQL_operate.DB_operate()
    df = SQL.read_Dateframe(f"select * from  `{symbol.lower()}-1m`;")
    df['Close'].plot()
    plt.show()


test_data('usd.jpy')