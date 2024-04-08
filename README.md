# FileName: `Logger.py`
로그를 출력하는 module
## ClassName: Logger
- Function: `__init__(mode: None)`
  - Return: `None`
  - Description
    - 기본은 Shell mode로 실행
    - Test로 실행시 로그 출력이 안되도록 구성할 수 있음(현재는 해당 기능을 제외해뒀음)

- Function: `__Compress_File()`
  - Return: `bool`
  - Description
    - 특정 개수 이상의 log file이 생성(현재는 2개)되면 가장 일찍 만들어진 log file을 zip file으로 compression

- Function: `__renaming_latest()`
  - Return: `bool`
  - Description
    - 작성 중이던 `latest.log`가 특정 byte이상 (현재는 10kb)

- Function: `__get_calling_function_and_class(stack_index: int)`
  - Return: `(calling_class: str, calling_function: str)`
  - Description
    - 로그에 `className.functionName`을 출력하기 위하여 write_log를 호출한 className과 functionName을 찾는 함수

- Function: `setLogFileMaxCount(cnt: int)`
  - Return: `None`
  - Description
    - 유지할 log file 개수를 세팅하는 함수
    - 해당 cnt보다 더 많은 개수의 log file이 생성되면 compression 진행

- Function: `setLogFileMaxSize(size: int)`
  - Return: `None`
  - Description
    - `latest.log`를 유지할 크기를 세팅하는 함수
    - 기록된 이후 해당 size KB가 넘어가면 `__renaming_latest()`실행

- Function: `write_log(message: str, stack_index: int)`
  - Return: `None`
  - Description
    - `latest.log`에 message를 기록하는 함수
    - `stack_index`는 기록할 className과 functionName의 깊이 정도



# FileName: `Shell.py`
SSD를 다루는 Shell을 실행하는 module

#### 실행 방법
1. `python Shell.py` : 기본 Shell을 실행하여 Shell Command를 실행
2. `python Shell.py (testModuleName)` : testModuleName의 module을 실행하여 테스트 진행

## ClassName: Shell
mode에 맞게 Shell을 실행하는 class
- Function: `__init__(mode: str, test_file_list: List[str])`
  - Return: `None`
  - Description
    - Shell 초기화 함수

- Function: `create_Shell(cls: None, argv: List[str])`
  - Return: `Shell`
  - Description
    - Shell을 생성하는 함수(일종의 Factory)
    - `argv`가 모두 `.py`확장자일 경우 Test mode로 실행

- Function: `__check_Py_Extension(test_py_files: List[str])`
  - Return: `bool`
  - Description
    - `test_py_files`가 전부 `.py`확장자인지 판별
    - `create_Shell`에서 활용

- Function: `run()`
  - Return: `None`
  - Description
    - 실질적인 Shell Command를 mode에 맞게 실행하는 Runner를 실행하는 함수

## ClassName: Runner
Shell Command를 실행하는 class
- Function: `__init__(mode: str, test_file_list: List[str])`
  - Return: `None`
  - Description
    - mode에 맞게 Shell Command를 실행할 수 있게 초기화
    - `mode` : `Shell` or `Test`
    - `test_file_list` : `Test` mode로 실행시 Shell Command를 불러와 사용할 python file명

- Function: `__run_Command(command: List[str])`
  - Return: `None`
  - Description
    - Shell Command를 생성 및 실행하는 함수

- Function: `__run()`
  - Return: `None`
  - Description
    - `Shell` mode로 실행시 Shell Command를 입력받고, `__run_Command()`를 실행 

- Function: `__run_test(filename: str)`
  - Return: `bool`
  - Description
    - `Test` mode로 실행시 `filename`에 해당하는 module을 실행하여 테스트하는 함수
    - 테스트의 성공 여부에 따라 `True` or `False` 반환

- Function: `run()`
  - Return: `None`
  - Description
    - `Runner`를 mode에 맞게 동작시키는 함수



# FileName: `ShellCommand.py`
Command Pattern으로 이루어진 Shell Command들
## ClassName: _ShellCommand
Shell Command의 추상화된 class
- Function: `__init__(command: List[str], ssd: SSD, mode: str)`
  - Return: `None`
  - Description
    - Shell Command의 기본 세팅
    - command : Command를 실행시킬 때 필요한 parameters
    - ssd : 동작시킬 `SSD`
    - mode : `Test` or `Shell`로 `Test` mode시 Message의 출력 방지

- Function: `_print_Message(message: str)`
  - Return: `None`
  - Description
    - console에 message를 출력하는 함수
    - `Test` mode시 출력 방지
    - Logger를 이용하여 log도 출력

- Function: `_isValid_LBA(LBA: str)`
  - Return: `bool`
  - Description
    - LBA의 유효성 확인

- Function: `_isValid_Value(Value: str)`
  - Return: `bool`
  - Description
    - Value의 유효성 확인

- Function: `_isValid_Size(LBA: str, size: str)`
  - Return: `bool`
  - Description
    - Size의 유효성 확인

- Function: `execute()`
  - Return: `None`
  - Description
    - 추상화된 실행 함수
    - 실제 Command에서 작성

## ClassName: _ShellWriteCommand
- Function: `execute()`
  - Return: `None`
  - Description
    - 유효성을 판단하여 SSD의 `write`명령어 실행
    - SSD의 LBA에 VALUE를 writing

## ClassName: _ShellReadCommand
- Function: `__read_result(LBA: int)`
  - Return: `str`
  - Description
    - SSD의 read 명령어 실행 결과를 읽어오는 함수

- Function: `execute()`
  - Return: `None`
  - Description
    - 유효성을 판단하여 SSD의 `read` 명령어 실행 후 `_ShellReadCommnad`로 VALUE를 가져옴

## ClassName: _ShellEraseCommand
- Function: `execute()`
  - Return: `None`
  - Description
    - 유효성을 판단하여 SSD의 `erase`명령어 실행
    - SSD의 LBA부터 SIZE만큼을 erasing

## ClassName: _ShellEraseRangeCommand
- Function: `execute()`
  - Return: `None`
  - Description
    - 유효성을 판단하여 SSD의 `erase`명령어 실행
    - SSD의 start_LBA부터 end_LBA전까지를 erasing

## ClassName: _ShellExitCommand
- Function: `execute()`
  - Return: `None`
  - Description
    - Shell을 종료

## ClassName: _ShellHelpCommand
- Function: `execute()`
  - Return: `None`
  - Description
    - Shell Command의 목록을 출력

## ClassName: _ShellFullwriteCommand
- Function: `execute()`
  - Return: `None`
  - Description
    - 유효성을 판단하여 SSD의 모든 LBA에 `write`명령어 실행

## ClassName: _ShellFullreadCommand
- Function: `__read_result(LBA: int)`
  - Return: `str`
  - Description
    - SSD의 read 명령어 실행 결과를 읽어오는 함수

- Function: `execute()`
  - Return: `Optional[Dict]`
  - Description
    - 유효성을 판단하여 SSD의 모든 LBA에 `read`명령어 실행
    - 실행 후 dictionary로 LBA, VALUE를 반환

## ClassName: _ShellInvalidCommand
- Function: `execute()`
  - Return: `None`
  - Description
    - 유효하지 않은 명령어에 대한 message를 출력

## ClassName: ShellCommandFactory
- Function: `__init__(mode: str)`
  - Return: `None`
  - Description
    - SSD를 mode에 맞게 세팅하여 Command Factory를 초기화
    - 
- Function: `create_Command(command: List[str])`
  - Return: `_ShellCommand`
  - Description
    - Command에 맞는 Shell Command Object 생성


# FileName: `SSD.py`
## ClassName: _Device
- Function: `__init__()`
  - Return: `None`
  - Description

- Function: `__init_File()`
  - Return: `None`
  - Description

- Function: `read_LBA_VALUE(LBA: None)`
  - Return: `str`
  - Description

- Function: `write_LBA_VALUE(LBA: None, VALUE: None)`
  - Return: `None`
  - Description

- Function: `erase_LBA_VALUE(LBA: None, SIZE: None)`
  - Return: `None`
  - Description

## ClassName: _SSDCommand
- Function: `__init__(CommandLine: str, device: _Device)`
  - Return: `None`
  - Description

- Function: `is_Overlap(other: Str(s='_SSDCommand'))`
  - Return: `bool`
  - Description

- Function: `is_Include(other: Str(s='_SSDCommand'))`
  - Return: `bool`
  - Description

- Function: `execute()`
  - Return: `None`
  - Description

- Function: `to_String()`
  - Return: `str`
  - Description

## ClassName: _SSDWriteCommand
- Function: `split(LBA_LEFT: None, LBA_RIGHT: None)`
  - Return: `(_SSDCommand, _SSDCommand)`
  - Description

- Function: `execute()`
  - Return: `None`
  - Description

## ClassName: _SSDReadCommand
- Function: `setBuffer(buffer: None)`
  - Return: `None`
  - Description

- Function: `__write_result(text: str)`
  - Return: `None`
  - Description

- Function: `execute()`
  - Return: `None`
  - Description

## ClassName: _SSDCommandBuffer
- Function: `__init__(device: _Device, mode: None)`
  - Return: `None`
  - Description

- Function: `__init_File()`
  - Return: `None`
  - Description

- Function: `__insert_Command(command: Str(s='_SSDCommand'))`
  - Return: `None`
  - Description

- Function: `__write_Command_List()`
  - Return: `None`
  - Description

- Function: `get_Command_List()`
  - Return: `List[_SSDCommand]`
  - Description

- Function: `insert(params: None)`
  - Return: `None`
  - Description

- Function: `flush()`
  - Return: `None`
  - Description

## ClassName: SSD
- Function: `__new__(cls: None)`
  - Return: `None`
  - Description

- Function: `__init__(mode: None)`
  - Return: `None`
  - Description

- Function: `__print_Error_Message(message: str)`
  - Return: `None`
  - Description

- Function: `__isValid_LBA(LBA: str)`
  - Return: `bool`
  - Description

- Function: `__isValid_Value(Value: str)`
  - Return: `bool`
  - Description

- Function: `__isValid_Size(LBA: str, size: str)`
  - Return: `bool`
  - Description

- Function: `__isValid_argv(command: List[str])`
  - Return: `None`
  - Description

- Function: `run_Command(argv: List[str])`
  - Return: `None`
  - Description



# FileName: `TestRunner.py`
## ClassName: TestRunner
- Function: `__run_command(command: List[str])`
  - Return: `bool`
  - Description

- Function: `write(LBA: int, value: str)`
  - Return: `None`
  - Description

- Function: `erase(LBA: int, size: int)`
  - Return: `None`
  - Description

- Function: `eraseRange(start_LBA: int, end_LBA: int)`
  - Return: `None`
  - Description

- Function: `fullwrite(value: str)`
  - Return: `None`
  - Description

- Function: `readCompare(LBA: int, value: str)`
  - Return: `bool`
  - Description

- Function: `fullreadCompare(values: Optional[Dict], all_value: str)`
  - Return: `bool`
  - Description

- Function: `run()`
  - Return: `bool`
  - Description



# FileName: `FullWriteReadCompare.py`
fullwrite & fullread 테스트용
## ClassName: FullWriteReadCompare
- Function: `run()`
  - Return: `bool`
  - Description


