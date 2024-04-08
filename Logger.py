import os
from pathlib import Path
import glob
from datetime import datetime
import inspect

class Logger:
    def __init__(self, mode="Shell") -> None:
        self.__mode = mode
        self.__LOG_FILE_MAX_COUNT = 1
        self.__LOG_FILE_MAX_SIZE = 10 * 1024
        self.__LOG_FILE_NAME = 'latest.log'
        self.__LOG_DIRECTORY = './log'
        self.__LOG_FULLPATH = f'{self.__LOG_DIRECTORY}/{self.__LOG_FILE_NAME}'
        Path(self.__LOG_DIRECTORY).mkdir(parents=True, exist_ok=True)
        pass

    def __Compress_File(self) -> bool:
        try:
            log_files = glob.glob(f'{self.__LOG_DIRECTORY}/*.log')
            if len(log_files) < self.__LOG_FILE_MAX_COUNT:
                return False
            sorted(log_files)
            for log_file in log_files[:-self.__LOG_FILE_MAX_COUNT]:
                old_log_name = Path(f"{log_file}")
                new_log_name = Path(f"{log_file[:-4]}.zip")
                old_log_name.rename(new_log_name)
        except:
            return False

    def __renaming_latest(self) -> bool:
        if self.__LOG_FILE_MAX_SIZE > os.path.getsize(self.__LOG_FULLPATH):
            return False
        try:
            current_datetime = datetime.now()
            formatted_datetime = current_datetime.strftime("%y%m%d_%Hh%Mm%Ss")
            old_log_name = Path(self.__LOG_FULLPATH)
            new_log_name = Path(f"{self.__LOG_DIRECTORY}/until_{formatted_datetime}.log")
            old_log_name.rename(new_log_name)
            return True
        except:
            return False

    def __get_calling_function_and_class(self, stack_index: int = 0) -> (str, str):
        stack = inspect.stack()

        frame = stack[2 + stack_index]
        calling_class = frame.frame.f_locals.get('self', None).__class__.__name__ if 'self' in frame.frame.f_locals else None
        calling_function = frame.function

        return calling_class, calling_function

    def setLogFileMaxCount(self, cnt: int) -> None:
        self.__LOG_FILE_MAX_COUNT = cnt

    def setLogFileMaxSize(self, size: int) -> None:
        self.__LOG_FILE_MAX_SIZE = size * 1024

    def write_log(self, message: str, stack_index: int = 0) -> None:
        with open(self.__LOG_FULLPATH, 'a') as file:
            current_datetime = datetime.now()
            formatted_datetime = current_datetime.strftime("%y.%m.%d %H:%M:%S")
            calling_class, calling_function = self.__get_calling_function_and_class(stack_index)
            formatted_calling = f"{calling_class or 'None'}.{calling_function or 'None'}()"
            file.write(f'[{formatted_datetime}] {formatted_calling:45} : {message}\n')
        if self.__renaming_latest():
            self.__Compress_File()