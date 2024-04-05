import sys, struct
from abc import ABC, abstractmethod
from typing import List

class _Device:
    def __init__(self) -> None:
        self.LBA_VALUE = dict()
        self.__NAND_FILE_NAME = 'nand.txt'
        self.__NAND_LBA_SIZE = 100
        self.__VALUE_BYTE_SIZE = 8
        self.__VALUE_BYTE_LENGTH = self.__VALUE_BYTE_SIZE // 2
        self.__init_File()

    def __init_File(self) -> None:
        try:
            # 파일을 읽기 모드로 엽니다.
            with open(self.__NAND_FILE_NAME, 'rb'):
                pass
        except FileNotFoundError:
            # 파일이 없는 경우, 쓰기 모드로 열어서 빈 파일을 생성합니다.
            with open(self.__NAND_FILE_NAME, 'wb') as file:
                data = b'\0' * self.__NAND_LBA_SIZE * self.__VALUE_BYTE_LENGTH
                file.write(data)

    def read_LBA_VALUE(self, LBA) -> str:
        with open(self.__NAND_FILE_NAME, 'rb') as file:
            file.seek(LBA * self.__VALUE_BYTE_LENGTH)
            data = file.read(self.__VALUE_BYTE_LENGTH)
            format_string = '>{}B'.format(self.__VALUE_BYTE_LENGTH)
            int_values = struct.unpack(format_string, data)
            hex_string = ''.join([format(value, '02X') for value in int_values])
            hex_result = '0X' + hex_string
            return hex_result

    def write_LBA_VALUE(self, LBA, VALUE) -> None:
        try:
            hex_data = int(VALUE[2:], 16)
        except ValueError:
            print(f"Invalid hex value: {VALUE}")
            return
        data = struct.pack('>I', hex_data)

        with open(self.__NAND_FILE_NAME, 'rb+') as file:
            file.seek(LBA * self.__VALUE_BYTE_LENGTH)
            file.write(data)

    def erase_LBA_VALUE(self, LBA, SIZE) -> None:
        with open(self.__NAND_FILE_NAME, 'rb+') as file:
            data = b'0' * SIZE * self.__VALUE_BYTE_LENGTH
            file.seek(LBA * self.__VALUE_BYTE_LENGTH)
            file.write(data)


class _SSDCommand(ABC):
    def __init__(self, CommandLine: str, device: _Device) -> None:
        params = CommandLine.split()
        self.TYPE = params[0]
        self.LBA_LEFT = int(params[1])
        self.LBA_RIGHT = int(params[2])
        self.VALUE = params[3]
        self.device = device

    def __eq__(self, other) -> bool:
        return self.LBA_LEFT == other.LBA_LEFT and self.LBA_RIGHT == other.LBA_RIGHT and self.VALUE == other.VALUE

    def __lt__(self, other) -> bool:
        return (self.LBA_LEFT, self.LBA_RIGHT, self.VALUE) < (other.LBA_LEFT, other.LBA_RIGHT, other.VALUE)

    def __gt__(self, other) -> bool:
        return (self.LBA_LEFT, self.LBA_RIGHT, self.VALUE) > (other.LBA_LEFT, other.LBA_RIGHT, other.VALUE)

    def __le__(self, other) -> bool:
        return (self.LBA_LEFT, self.LBA_RIGHT, self.VALUE) <= (other.LBA_LEFT, other.LBA_RIGHT, other.VALUE)

    def __ge__(self, other) -> bool:
        return (self.LBA_LEFT, self.LBA_RIGHT, self.VALUE) >= (other.LBA_LEFT, other.LBA_RIGHT, other.VALUE)

    def is_Overlap(self, other: '_SSDCommand') -> bool:
        return not (self.LBA_RIGHT < other.LBA_LEFT or other.LBA_RIGHT < self.LBA_LEFT)

    def is_Include(self, other: '_SSDCommand') -> bool:
        return (self.LBA_LEFT <= other.LBA_LEFT and other.LBA_RIGHT <= self.LBA_RIGHT)

    @abstractmethod
    def execute(self) -> None:
        pass

    def to_String(self) -> str:
        return f"{self.TYPE} {self.LBA_LEFT} {self.LBA_RIGHT} {self.VALUE}"


class _SSDWriteCommand(_SSDCommand):
    def split(self, LBA_LEFT, LBA_RIGHT) -> ('_SSDCommand', '_SSDCommand'):
        if LBA_RIGHT < LBA_LEFT:
            LBA_RIGHT, LBA_LEFT = LBA_LEFT, LBA_RIGHT
        if (self.LBA_RIGHT <= LBA_LEFT and LBA_RIGHT <= self.LBA_LEFT):
            return (None, self)

        left, right = None, None
        if self.LBA_LEFT < LBA_LEFT:
            left = _SSDWriteCommand(f"{self.TYPE} {self.LBA_LEFT} {LBA_LEFT - 1} {self.VALUE}")
        if LBA_RIGHT < self.LBA_RIGHT:
            right = _SSDWriteCommand(f"{self.TYPE} {LBA_RIGHT + 1} {self.LBA_RIGHT} {self.VALUE}")
        return (left, right)

    def execute(self) -> None:
        for LBA in range(self.LBA_LEFT, self.LBA_RIGHT + 1):
            self.device.write_LBA_VALUE(LBA, self.VALUE)


class _SSDReadCommand(_SSDCommand):
    def setBuffer(self, buffer) -> None:
        if not isinstance(buffer, _SSDCommandBuffer):
            raise TypeError("buffer must be of type SSDCommandBuffer")
        self.buffer = buffer

    def __write_result(self, text: str) -> None:
        with open("result.txt", 'w') as file:
            file.write(text)

    def execute(self) -> None:
        if not hasattr(self, 'buffer'):
            return
        index = 0
        commandList = self.buffer.get_Command_List()
        for LBA in range(self.LBA_LEFT, self.LBA_RIGHT + 1):
            while index < len(commandList) and commandList[index].LBA_RIGHT < LBA:
                index += 1
            Value = ""
            if index < len(commandList) and commandList[index].LBA_LEFT <= LBA <= commandList[index].LBA_RIGHT:
                Value = commandList[index].VALUE
            else:
                Value = self.device.read_LBA_VALUE(LBA)
            if self.buffer.mode != "test":
                self.__write_result(Value)


class _SSDCommandBuffer:
    def __init__(self, device: _Device, mode="Shell"):
        self.device = device
        self.mode = mode
        self.LBA_VALUE = dict()
        self.__BUFFER_FILE_NAME = 'buffer.txt'
        self.__BUFFER_COUNT_SIZE = 10
        self.__BUFFER_COUNT = 0
        self.__BUFFER_LBA_SIZE = 100
        self.__VALUE_SIZE = 8
        self.__Command_List: List[_SSDCommand] = []
        self.__init_File()
        pass

    def __init_File(self) -> None:
        try:
            with open(self.__BUFFER_FILE_NAME, 'r') as file:
                count_line = file.readline().strip()
                if count_line.isdigit():
                    self.__BUFFER_COUNT = int(count_line)
                for line in file:
                    params = line.split()
                    command_type = params[0]
                    if command_type == 'W':
                        command = _SSDWriteCommand(line.rstrip(), self.device)
                        self.__insert_Command(command)
        except FileNotFoundError:
            with open(self.__BUFFER_FILE_NAME, 'w'):
                pass

    def __insert_Command(self, command: '_SSDCommand') -> None:
        temp_list = []
        for c in self.__Command_List:
            if not c.is_Overlap(command):
                temp_list.append(c)
            elif command.is_Include(c):
                pass
            else:
                left, right = c.split(command.LBA_LEFT, command.LBA_RIGHT)
                if left:
                    temp_list.append(left)
                if right:
                    temp_list.append(right)
        temp_list.append(command)
        temp_list.sort(key=lambda x: (x.LBA_LEFT, x.LBA_RIGHT, x.VALUE))
        self.__Command_List = temp_list

    def __write_Command_List(self) -> None:
        with open(self.__BUFFER_FILE_NAME, 'w') as file:
            file.write(str(self.__BUFFER_COUNT)+"\n")
            for command in self.__Command_List:
                file.write(command.to_String()+"\n")

    def get_Command_List(self) -> List[_SSDCommand]:
        return self.__Command_List

    def insert(self, params) -> None:
        command_type = params[0]
        if command_type == 'W':
            LBA = int(params[1])
            value = params[2]
            command = _SSDWriteCommand(f'{command_type} {LBA} {LBA} {value}', self.device)
            self.__insert_Command(command)
        elif command_type == 'E':
            LBA = int(params[1])
            size = int(params[2])
            command = _SSDWriteCommand(f'{command_type} {LBA} {LBA + size - 1} 0x00000000', self.device)
            self.__insert_Command(command)
        elif command_type == 'R':
            LBA = int(params[1])
            command = _SSDReadCommand(f'{command_type} {LBA} {LBA} 0x00000000', self.device)
            command.setBuffer(self)
            command.execute()
            self.__BUFFER_COUNT = -1
        elif command_type == 'FLUSH':
            self.__BUFFER_COUNT = self.__BUFFER_COUNT_SIZE
        self.__BUFFER_COUNT += 1
        if self.__BUFFER_COUNT >= self.__BUFFER_COUNT_SIZE:
            self.flush()
        self.__write_Command_List()

    def flush(self) -> None:
        self.__BUFFER_COUNT = 0
        for c in self.__Command_List:
            c.execute()
        self.__Command_List = []


class SSD:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls,'instance'):
            cls.instance = super(SSD, cls).__new__(cls)
        return cls.instance

    def __init__(self, mode="Shell"):
        self.mode = mode
        self.device = _Device()
        self.buffer = _SSDCommandBuffer(self.device, mode)

    def __print_Error_Message(self, message: str) -> None:
        if self.mode != "test":
            print(message)

    def __isValid_LBA(self, LBA: str) -> bool:
        if LBA.isdigit():
            lba_num = int(LBA)
            if 0 <= lba_num <= 99:
                return True
        self.__print_Error_Message("LBA must be an integer between 0 and 99.")
        return False

    def __isValid_Value(self, Value: str) -> bool:
        if len(Value) == 10 and Value[0] == '0' and Value[1].upper() == 'X':
            hex_digits = Value[2:]
            if all(c in "0123456789ABCDEF" for c in hex_digits):
                return True
        self.__print_Error_Message("[VALUE] must be eight-digit hexadecimal integer between '0X00000000' and '0XFFFFFFFF'.")
        return False

    def __isValid_Size(self, LBA: str, size: str) -> bool:
        if self.__isValid_LBA(LBA) and size.isdigit():
            lba_num = int(LBA)
            size_num = int(size)
            if 0 <= lba_num <= 99 and 1 <= size_num <= 10:
                if 0 <= lba_num + size_num - 1 <= 99:
                    return True
                else:
                    self.__print_Message("too much [SIZE], '[LBA] + [SIZE]' cannot exceed 100.")
                    return False
        self.__print_Error_Message("[SIZE] must be an integer between 1 and 10.")
        return False

    def __isValid_argv(self, command: List[str]):
        command_type = command[0]
        if command_type == 'W' and len(command) == 3:
            if self.__isValid_LBA(command[1]) and self.__isValid_Value(command[2]):
                return True
        elif command_type == 'R' and len(command) == 2:
            if self.__isValid_LBA(command[1]):
                return True
        elif command_type == 'E' and len(command) == 3:
            if self.__isValid_LBA(command[1]) and self.__isValid_Size(command[1], command[2]):
                return True
        elif command_type == "FLUSH" and len(command) == 2:
            return True
        elif command_type == 'HELP' and len(command) == 2:
            help_text = """
            write   - W [LBA] [VALUE]   : Write [VALUE] at [LBA].
            read    - R [LBA]           : Read VALUE at [LBA].
            erase   - E [LBA] [SIZE]    : Erase VALUES from [LBA] up to [SIZE] count.
            """
            print("\n".join([s.strip() for s in help_text.split("\n")[1:-1]]))
        else:
            self.__print_Error_Message("Invalid Command. To view the list of commands, please enter 'help'.")
        return False

    def run_Command(self, argv: List[str]) -> None:
        upper_argv = [s.upper() for s in argv]
        if self.__isValid_argv(upper_argv):
            self.buffer.insert(upper_argv)


if __name__=="__main__":
    ssd = SSD(mode="main")
    # ssd.runCommand(input())
    ssd.run_Command(sys.argv[1:])
