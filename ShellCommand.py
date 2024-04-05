import sys, struct
from abc import ABC, abstractmethod
from typing import List
from SSD import SSD
from Logger import Logger

class _ShellCommand(ABC):
    def __init__(self, command: List[str], ssd: SSD, mode: str) -> None:
        self._command = command
        self._ssd = ssd
        self._mode = mode

    def _print_Message(self, message: str) -> None:
        logger = Logger()
        if self._mode != "Test":
            print(message)
        logger.write_log(message, stack_index = 1)

    def _isValid_LBA(self, LBA: str) -> bool:
        if LBA.isdigit():
            lba_num = int(LBA)
            if 0 <= lba_num <= 99:
                return True
        self._print_Message("LBA must be an integer between 0 and 99.")
        return False

    def _isValid_Value(self, Value: str) -> bool:
        if len(Value) == 10 and Value[0] == '0' and Value[1].upper() == 'X':
            hex_digits = Value[2:]
            if all(c in "0123456789ABCDEF" for c in hex_digits):
                return True
        self._print_Message("[VALUE] must be eight-digit hexadecimal integer between '0X00000000' and '0XFFFFFFFF'.")
        return False

    def _isValid_Size(self, LBA: str, size: str) -> bool:
        if self._isValid_LBA(LBA) and size.isdigit():
            lba_num = int(LBA)
            size_num = int(size)
            if 0 <= lba_num <= 99 and 1 <= size_num <= 10:
                if 0 <= lba_num + size_num - 1 <= 99:
                    return True
                else:
                    self._print_Message("too much [SIZE], '[LBA] + [SIZE]' cannot exceed 100.")
                    return False
        self._print_Message("[SIZE] must be an integer between 1 and 10.")
        return False

    @abstractmethod
    def execute(self) -> None:
        pass


class _ShellWriteCommand(_ShellCommand):
    def execute(self) -> None:
        if self._command[0] == "WRITE" and len(self._command) == 3:
            if self._isValid_LBA(self._command[1]) and self._isValid_Value(self._command[2]):
                self._ssd.run_Command(["W"] + self._command[1:])
                return
        else:
            self._print_Message("Please use the format 'write [LBA] [VALUE]'.")


class _ShellReadCommand(_ShellCommand):
    def __read_result(self, LBA: int) -> str:
        value = None
        try:
            with open("result.txt", 'r') as file:
                value = file.readline()
                self._print_Message(f"[{LBA:02d}]{value}")
        except FileNotFoundError:
            pass
        return value

    def execute(self) -> None:
        if self._command[0] == "READ" and len(self._command) == 2:
            if self._isValid_LBA(self._command[1]):
                self._ssd.run_Command(["R"] + self._command[1:])
                LBA = int(self._command[1])
                return self.__read_result(LBA)
        else:
            self._print_Message("Please use the format 'read [LBA]'.")


class _ShellEraseCommand(_ShellCommand):
    def execute(self) -> None:
        if self._command[0] == "ERASE" and len(self._command) == 3:
            if self._isValid_LBA(self._command[1]) and self._isValid_Size(self._command[1], self._command[2]):
                self._ssd.run_Command(["E"] + self._command[1:])
                return
        else:
            self._print_Message("Please use the format 'erase [LBA] [VALUE]'.")


class _ShellEraseRangeCommand(_ShellCommand):
    def execute(self) -> None:
        if self._command[0] == "ERASE_RANGE" and len(self._command) == 3:
            if self._isValid_LBA(self._command[1]) and self._isValid_LBA(str(int(self._command[2])-1)):
                if self._command[1] < self._command[2]:
                    size = int(self._command[2]) - int(self._command[1]) + 1
                    for i in range((size+9) // 10):
                        start_LBA = int(self._command[1]) + (i * 10)
                        now_size = min(10, int(self._command[2]) - (int(self._command[1]) + (i * 10)) + 1)
                        self._ssd.run_Command(["E", str(start_LBA), str(now_size)])
                else:
                    self._print_Message("[Start_LBA] must less than or equal to [End_LBA].")
                return
        else:
            self._print_Message("Please use the format 'erase_range [Start_LBA] [End_LBA]'.")


class _ShellExitCommand(_ShellCommand):
    def execute(self) -> None:
        if self._command[0] == "EXIT" and len(self._command) == 1:
            self._print_Message("Bye Bye")
            sys.exit()
        else:
            self._print_Message("Please use the format 'exit'.")


class _ShellHelpCommand(_ShellCommand):
    def execute(self) -> None:
        if self._command[0] == "HELP" and len(self._command) == 1:
            help_text = """
            write [LBA] [VALUE]                     : Write [VALUE] at [LBA].
            read [LBA]                              : Read VALUE at [LBA].
            erase [LBA] [SIZE]                      : Erase VALUES from [LBA] up to [SIZE] count.
            erase_range [Start_LBA] [End_LBA]       : Erase VALUES from [Start_LBA] to [End_LBA].
            fullwrite [VALUE]                       : Write [VALUE] to all LBAs of the SSD.
            fullread                                : Read VALUEs from all LBAs of the SSD.
            help                                    : Display available shell commands.
            exit                                    : Exit Shell.
            """
            self._print_Message("\n".join([s.strip() for s in help_text.split("\n")[1:-1]]))
        else:
            self._print_Message("Please use the format 'help'.")


class _ShellFullwriteCommand(_ShellCommand):
    def execute(self) -> None:
        if self._command[0] == "FULLWRITE" and len(self._command) == 2:
            if self._isValid_Value(self._command[1]):
                for LBA in range(100):
                    self._ssd.run_Command(["W", str(LBA), self._command[1]])
        else:
            self._print_Message("Please use the format 'fullwrite [VALUE]'.")


class _ShellFullreadCommand(_ShellCommand):
    def __read_result(self, LBA: int) -> str:
        value = None
        try:
            with open("result.txt", 'r') as file:
                value = file.readline()
                message = f"[{LBA:02d}]{value}"
                self._print_Message(message)
        except FileNotFoundError:
            pass
        return value

    def execute(self) -> None:
        result = dict()
        if self._command[0] == "FULLREAD" and len(self._command) == 1:
            for LBA in range(100):
                self._ssd.run_Command(["R", str(LBA)])
                result[LBA] = self.__read_result(LBA)
            return result
        else:
            self._print_Message("Please use the format 'fullread'.")


class _ShellInvalidCommand(_ShellCommand):
    def execute(self) -> None:
        self._print_Message("Invalid Command. To view the list of commands, please enter 'help'.")


class ShellCommandFactory:
    def __init__(self, mode: str) -> None:
        self.__mode = mode
        self.ssd = SSD(mode)

    def create_Command(self, command: List[str]) -> '_ShellCommand':
        command_type = command[0]
        if command_type == "WRITE":
            return _ShellWriteCommand(command, self.ssd, self.__mode)
        elif command_type == "READ":
            return _ShellReadCommand(command, self.ssd, self.__mode)
        elif command_type == "ERASE":
            return _ShellEraseCommand(command, self.ssd, self.__mode)
        elif command_type == "ERASE_RANGE":
            return _ShellEraseRangeCommand(command, self.ssd, self.__mode)
        elif command_type == "EXIT":
            return _ShellExitCommand(command, self.ssd, self.__mode)
        elif command_type == "HELP":
            return _ShellHelpCommand(command, self.ssd, self.__mode)
        elif command_type == "FULLWRITE":
            return _ShellFullwriteCommand(command, self.ssd, self.__mode)
        elif command_type == "FULLREAD":
            return _ShellFullreadCommand(command, self.ssd, self.__mode)
        else:
            return _ShellInvalidCommand(command, self.ssd, self.__mode)