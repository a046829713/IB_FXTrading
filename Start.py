# 先將資料都建立完成
from Database import BackUP_file
BackUP_file.FilePreparator().check_all_need_file()


# 檢查資料庫
from Database import BackUp
BackUp.DatabasePreparator().checkIfDataBase()


# 檢查各資料庫是否存在
BackUp.DatabasePreparator().check_all_need_table()