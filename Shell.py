import sys
from typing import List
from ShellCommand import ShellCommandFactory
import importlib.util
import os

class Runner:
    def __init__(self, mode: str, test_file_list: List[str] = None):
        self.__mode = mode
        self.__TEST_FILE_LIST = test_file_list

    def __run_Command(self, command: List[str]) -> None:
        command_factory = ShellCommandFactory(self.__mode)
        command_object = command_factory.create_Command(command)
        command_object.execute()

    def __run(self) -> None:
        while True:
            command = input().upper().split()
            self.__run_Command(command)

    def __run_test(self, filename: str) -> bool:
        # 파일이 존재하는지 확인
        if not os.path.exists(filename):
            print(f"File '{filename}' does not exist.")
            return

        # 파일 이름에서 모듈 이름 추출
        module_name = os.path.splitext(os.path.basename(filename))[0]

        # 모듈 스펙 생성
        spec = importlib.util.spec_from_file_location(module_name, filename)

        # 모듈 로드
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # 클래스 찾기
        for name in dir(module):
            obj = getattr(module, name)
            if isinstance(obj, type):
                # 클래스 객체 생성
                cls_instance = obj()

                # run 함수 실행 가능 여부 확인 후 실행
                if hasattr(cls_instance, 'run') and callable(getattr(cls_instance, 'run')):
                    return cls_instance.run()

        print(f"No runnable class found in '{filename}'.")
        return False

    def run(self) -> None:
        if self.__mode == "Test":
            for file_name in self.__TEST_FILE_LIST:
                print(file_name, "--- Run ... ", end="")
                if self.__run_test(file_name):
                    print("Pass")
                else:
                    print("FAIL!")
                    sys.exit()
        else:
            self.__run()

class Shell:
    def __init__(self, mode: str, test_file_list: List[str]) -> None:
        self.__mode = mode
        self.__TEST_FILE_LIST = test_file_list

    @classmethod
    def create_Shell(cls, argv: List[str]) -> 'Shell':
        test_file_list = argv[1:]
        if test_file_list:
            if cls.__check_Py_Extension(test_file_list):
                return cls("Test", test_file_list)
            else:
                return None
        else:
            return cls("Shell", None)

    @staticmethod
    def __check_Py_Extension(test_py_files: List[str]) -> bool:
        for file in test_py_files:
            if not file.endswith(".py"):
                return False
        return True

    def run(self):
        runner = Runner(self.__mode, self.__TEST_FILE_LIST)
        runner.run()

if __name__=="__main__":
    shell = Shell.create_Shell(sys.argv)
    if shell:
        shell.run()
