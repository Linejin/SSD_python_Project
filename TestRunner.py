import sys
from typing import List, Dict, Optional
from ShellCommand import ShellCommandFactory
from abc import ABC, abstractmethod

class TestRunner(ABC):
    def __run_command(self, command: List[str]) -> bool:
        command_factory = ShellCommandFactory("Test")
        command_object = command_factory.create_Command(command)
        return command_object.execute()

    def write(self, LBA: int, value: str) -> None:
        command = ["WRITE", str(LBA), value.upper()]
        self.__run_command(command)

    def erase(self, LBA: int, size: int) -> None:
        command = ["ERASE", str(LBA), str(size)]
        self.__run_command(command)

    def eraseRange(self, start_LBA: int, end_LBA: int) -> None:
        command = ["ERASE_RANGE", str(start_LBA), str(start_LBA)]
        self.__run_command(command)

    def fullwrite(self, value: str) -> None:
        command = ["FULLWRITE", value.upper()]
        self.__run_command(command)

    def readCompare(self, LBA: int, value: str) -> bool:
        command = ["READ", str(LBA)]
        return value == self.__run_command(command)[LBA]

    def fullreadCompare(self, values: Optional[Dict] = None, all_value: str = "") -> bool:
        command = ["FULLREAD"]
        run_result = self.__run_command(command)
        if values:
            for key in values:
                values[key] = values[key].upper()
            return values == run_result
        else:
            all_value = all_value.upper()
            for key in run_result:
                if run_result[key] != all_value.upper():
                    return False
            return True

    @abstractmethod
    def run(self) -> bool:
        pass

