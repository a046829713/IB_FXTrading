import os


class FilePreparator:
    def __init__(self, backup_folder="backup", log_folder='LogRecord'):
        self.backup_folder = backup_folder
        self.log_folder = log_folder

    def check_file(self, filename: str):
        """ 檢查檔案是否存在 否則創建 """
        if not os.path.exists(filename):
            os.mkdir(filename)

    def check_all_need_file(self):
        # 檢查備份資料夾是否存在
        self.check_file(self.backup_folder)
        # 檢查log資料夾是否存在
        self.check_file(self.log_folder)
