# 실행 방법

## Shell 실행
1. 기본적인 Shell
   ```
   python Shell.py
   ```
   Shell 실행 후 help로 명령어를 확인하여 사용

2. Test Shell mode
   ```
   python Shell.py [testScript fileNames]
   ``` 


## SSD만 독립적으로 실행
```
python SSD.py [Command]
```



---

# FileName: `SSD.py`
SSD를 관리하는 module
<details>

## ClassName: _Device
실질적으로 SSD를 관리하는 함수를 갖고 있는 class

nand.txt를 관리

- Function: `__init__()`
  - Return: `None`
<br>

- Function: `__init_File()`
  - Return: `None`
  - Description
    - 관리할 SSD file을 읽습니다.
    - 해당 SSD file이 없으면 생성합니다.
<br>

- Function: `read_LBA_VALUE(LBA: int)`
  - Return: `str`
  - Description
    - SSD file로 부터 LBA의 VALUE를 읽어옵니다.
<br>

- Function: `write_LBA_VALUE(LBA: int, VALUE: str)`
  - Return: `None`
  - Description
    - SSD file의 LBA에 VALUE를 씁니다.
<br>

- Function: `erase_LBA_VALUE(LBA: int, SIZE: int)`
  - Return: `None`
  - Description
    -  SSD file의 LBA에서부터 SIZE만큼의 VALUE를 삭제합니다.
<br>

## ClassName: _SSDCommand
SSD를 관리하는 Command에 대한 추상화 class

SSD명령어 간의 LBA적 관계를 비교할 수 있는 기능이 들어간 Command pattern 구조

- Function: `__init__(CommandLine: str, device: _Device)`
  - Return: `None`
  - Description
    - `_Device`에 CommandLine이라는 명령어로 세팅
    - CommandLine은 `CommandType StartLBA EndLBA VALUE` 형태로 주어짐
<br>

- Function: `is_Overlap(other: _SSDCommand)`
  - Return: `bool`
  - Description
    - `other`와 LBA가 겹치는지 확인
<br>
  
- Function: `is_Include(other: _SSDCommand)`
  - Return: `bool`
  - Description
    - `other`를 내포하고 있는지 확인
<br>

- Function: `execute()`
  - Return: `None`
  - Description
    - 해당 SSDCommand를 실행
<br>

- Function: `to_String()`
  - Return: `str`
  - Description
    - 해당 Command를 문자열로 표현하여 반환
<br>

## ClassName: _SSDWriteCommand
- Function: `split(LBA_LEFT: None, LBA_RIGHT: None)`
  - Return: `(_SSDCommand, _SSDCommand)`
  - Description
    - LBA_LEFT~LBA_RIGHT 구간인 명령어와 겹치는 구간을 지우고, 그 외의 두 구간으로 명령어를 쪼갭니다.
<br>

- Function: `execute()`
  - Return: `None`
  - Description
    - SSD write 실행
<br>

## ClassName: _SSDReadCommand
- Function: `setBuffer(buffer: None)`
  - Return: `None`
  - Description
    - Fast read를 위한 buffer 세팅
<br>

- Function: `__write_result(text: str)`
  - Return: `None`
  - Description
    - `result.txt`에 read된 Value 쓰기
<br>

- Function: `execute()`
  - Return: `None`
  - Description
    - SSD read 실행
    - SSD의 mode가 `main`인 경우 console에 출력
<br>

## ClassName: _SSDCommandBuffer
`_SSDCommand`들을 관리하는 Buffer

erase 명령어는 write 명령어로 변환하여 사용

- Function: `__init__(device: _Device, mode: None)`
  - Return: `None`
  - Description
    - device에 해당하는 명령어들을 관리하는 buffer
<br>

- Function: `__init_File()`
  - Return: `None`
  - Description
    - buffer를 관리할 file 세팅
<br>

- Function: `__insert_Command(command: _SSDCommand)`
  - Return: `None`
  - Description
    - buffer에 `_SSDCommand`를 추가하는 내부 명령어
<br>

- Function: `__write_Command_List()`
  - Return: `None`
  - Description
    - buffer를 관리하는 file에 명령어 기록
<br>

- Function: `get_Command_List()`
  - Return: `List[_SSDCommand]`
  - Description
    - 내부적으로 관리하는 Command List를 반환
<br>

- Function: `insert(params: List[str])`
  - Return: `None`
  - Description
    - 외부에서 명령어를 주면 그에 맞게 Factory 형식처럼 Command를 생성하여 Command List에 등록
<br>

- Function: `flush()`
  - Return: `None`
  - Description
    - 내부에 관리하고 있던 Command들을 강제 실행 및 내부 Command List 비우기
<br>

## ClassName: SSD
SSD를 전체적으로 관리하는 class

mode에 맞게 `_device`, `buffer`를 생성 및 관리

- Function: `__new__(cls: None)`
  - Return: `None`
  - Description
    - Singleton 구조의 SSD를 생성
<br>

- Function: `__init__(mode: None)`
  - Return: `None`
  - Description
    - SSD의 mode 및 _Device, Buffer 세팅
<br>

- Function: `__print_Error_Message(message: str)`
  - Return: `None`
  - Description
    - `message`에 해당하는 에러 메시지 출력
    - 단, `Test` mode에서는 출력하지 않음
<br>

- Function: `__isValid_LBA(LBA: str)`
  - Return: `bool`
  - Description
    - LBA의 유효성 확인
<br>

- Function: `__isValid_Value(Value: str)`
  - Return: `bool`
  - Description
    - Valud의 유효성 확인
<br>

- Function: `__isValid_Size(LBA: str, size: str)`
  - Return: `bool`
  - Description
    - Size의 유효성 확인
<br>

- Function: `__isValid_argv(command: List[str])`
  - Return: `None`
  - Description
    - argv형태의 명령어 유효성 확인
<br>

- Function: `run_Command(argv: List[str])`
  - Return: `None`
  - Description
    - 명령어를 SSDCommand에 맞게 변환 후 buffer에 등록
<br>

<summary>접기/펼치기</summary>
</details>


---

# FileName: `Shell.py`
SSD를 다루는 Shell을 실행하는 module

<details>

## ClassName: Shell
mode에 맞게 Shell을 실행하는 class
- Function: `__init__(mode: str, test_file_list: List[str])`
  - Return: `None`
  - Description
    - Shell 초기화 함수
<br>

- Function: `create_Shell(cls: None, argv: List[str])`
  - Return: `Shell`
  - Description
    - Shell을 생성하는 함수(일종의 Factory)
    - `argv`가 모두 `.py`확장자일 경우 Test mode로 실행
<br>

- Function: `__check_Py_Extension(test_py_files: List[str])`
  - Return: `bool`
  - Description
    - `test_py_files`가 전부 `.py`확장자인지 판별
    - `create_Shell`에서 활용
<br>

- Function: `run()`
  - Return: `None`
  - Description
    - 실질적인 Shell Command를 mode에 맞게 실행하는 Runner를 실행하는 함수
<br>

## ClassName: Runner
Shell Command를 실행하는 class
- Function: `__init__(mode: str, test_file_list: List[str])`
  - Return: `None`
  - Description
    - mode에 맞게 Shell Command를 실행할 수 있게 초기화
    - `mode` : `Shell` or `Test`
    - `test_file_list` : `Test` mode로 실행시 Shell Command를 불러와 사용할 python file명
<br>

- Function: `__run_Command(command: List[str])`
  - Return: `None`
  - Description
    - Shell Command를 생성 및 실행하는 함수
<br>

- Function: `__run()`
  - Return: `None`
  - Description
    - `Shell` mode로 실행시 Shell Command를 입력받고, `__run_Command()`를 실행 
<br>

- Function: `__run_test(filename: str)`
  - Return: `bool`
  - Description
    - `Test` mode로 실행시 `filename`에 해당하는 module을 실행하여 테스트하는 함수
    - 테스트의 성공 여부에 따라 `True` or `False` 반환
<br>

- Function: `run()`
  - Return: `None`
  - Description
    - `Runner`를 mode에 맞게 동작시키는 함수
<br>


<summary>접기/펼치기</summary>
</details>

---


# FileName: `ShellCommand.py`
Command Pattern으로 이루어진 Shell Command module

<details>

## ClassName: _ShellCommand
Shell Command의 추상화된 class
- Function: `__init__(command: List[str], ssd: SSD, mode: str)`
  - Return: `None`
  - Description
    - Shell Command의 기본 세팅
    - command : Command를 실행시킬 때 필요한 parameters
    - ssd : 동작시킬 `SSD`
    - mode : `Test` or `Shell`로 `Test` mode시 Message의 출력 방지
<br>

- Function: `_print_Message(message: str)`
  - Return: `None`
  - Description
    - console에 message를 출력하는 함수
    - `Test` mode시 출력 방지
    - Logger를 이용하여 log도 출력
<br>

- Function: `_isValid_LBA(LBA: str)`
  - Return: `bool`
  - Description
    - LBA의 유효성 확인
<br>

- Function: `_isValid_Value(Value: str)`
  - Return: `bool`
  - Description
    - Value의 유효성 확인
<br>

- Function: `_isValid_Size(LBA: str, size: str)`
  - Return: `bool`
  - Description
    - Size의 유효성 확인
<br>

- Function: `execute()`
  - Return: `None`
  - Description
    - 추상화된 실행 함수
    - 실제 Command에서 작성
<br>

## ClassName: _ShellWriteCommand
- Function: `execute()`
  - Return: `None`
  - Description
    - 유효성을 판단하여 SSD의 `write`명령어 실행
    - SSD의 LBA에 VALUE를 writing
<br>

## ClassName: _ShellReadCommand
- Function: `__read_result(LBA: int)`
  - Return: `str`
  - Description
    - SSD의 read 명령어 실행 결과를 읽어오는 함수
<br>

- Function: `execute()`
  - Return: `None`
  - Description
    - 유효성을 판단하여 SSD의 `read` 명령어 실행 후 `_ShellReadCommnad`로 VALUE를 가져옴
<br>

## ClassName: _ShellEraseCommand
- Function: `execute()`
  - Return: `None`
  - Description
    - 유효성을 판단하여 SSD의 `erase`명령어 실행
    - SSD의 LBA부터 SIZE만큼을 erasing
<br>

## ClassName: _ShellEraseRangeCommand
- Function: `execute()`
  - Return: `None`
  - Description
    - 유효성을 판단하여 SSD의 `erase`명령어 실행
    - SSD의 start_LBA부터 end_LBA전까지를 erasing
<br>

## ClassName: _ShellExitCommand
- Function: `execute()`
  - Return: `None`
  - Description
    - Shell을 종료
<br>

## ClassName: _ShellHelpCommand
- Function: `execute()`
  - Return: `None`
  - Description
    - Shell Command의 목록을 출력
<br>

## ClassName: _ShellFullwriteCommand
- Function: `execute()`
  - Return: `None`
  - Description
    - 유효성을 판단하여 SSD의 모든 LBA에 `write`명령어 실행
<br>

## ClassName: _ShellFullreadCommand
- Function: `__read_result(LBA: int)`
  - Return: `str`
  - Description
    - SSD의 read 명령어 실행 결과를 읽어오는 함수
<br>

- Function: `execute()`
  - Return: `Optional[Dict]`
  - Description
    - 유효성을 판단하여 SSD의 모든 LBA에 `read`명령어 실행
    - 실행 후 dictionary로 LBA, VALUE를 반환
<br>

## ClassName: _ShellInvalidCommand
- Function: `execute()`
  - Return: `None`
  - Description
    - 유효하지 않은 명령어에 대한 message를 출력
<br>

## ClassName: ShellCommandFactory
- Function: `__init__(mode: str)`
  - Return: `None`
  - Description
    - SSD를 mode에 맞게 세팅하여 Command Factory를 초기화
<br>

- Function: `create_Command(command: List[str])`
  - Return: `_ShellCommand`
  - Description
    - Command에 맞는 Shell Command Object 생성
<br>

<summary>접기/펼치기</summary>
</details>

---

# FileName: `Logger.py`
로그를 출력하는 module

<details close>

## ClassName: Logger

- Function: `__init__(mode: None)`
  - Return: `None`
  - Description
    - 기본은 Shell mode로 실행
    - Test로 실행시 로그 출력이 안되도록 구성할 수 있음(현재는 해당 기능을 제외해뒀음)
<br>

- Function: `__Compress_File()`
  - Return: `bool`
  - Description
    - 특정 개수 이상의 log file이 생성(현재는 2개)되면 가장 일찍 만들어진 log file을 zip file으로 compression
<br>

- Function: `__renaming_latest()`
  - Return: `bool`
  - Description
    - 작성 중이던 `latest.log`가 특정 byte이상 (현재는 10kb)
<br>

- Function: `__get_calling_function_and_class(stack_index: int)`
  - Return: `(calling_class: str, calling_function: str)`
  - Description
    - 로그에 `className.functionName`을 출력하기 위하여 write_log를 호출한 className과 functionName을 찾는 함수
<br>

- Function: `setLogFileMaxCount(cnt: int)`
  - Return: `None`
  - Description
    - 유지할 log file 개수를 세팅하는 함수
    - 해당 cnt보다 더 많은 개수의 log file이 생성되면 compression 진행
<br>

- Function: `setLogFileMaxSize(size: int)`
  - Return: `None`
  - Description
    - `latest.log`를 유지할 크기를 세팅하는 함수
    - 기록된 이후 해당 size KB가 넘어가면 `__renaming_latest()`실행
<br>

- Function: `write_log(message: str, stack_index: int)`
  - Return: `None`
  - Description
    - `latest.log`에 message를 기록하는 함수
    - `stack_index`는 기록할 className과 functionName의 깊이 정도
<br>

<summary>접기/펼치기</summary>
</details>

---

# FileName: `TestRunner.py`
Test Script를 작성하기 위한 API를 제공하는 module

추상화된 `run()` 함수를 작성하여 사용
<details>

## ClassName: TestRunner
- Function: `__run_command(command: List[str])`
  - Return: `bool`
  - Description
    - Shell Command를 실질적으로 생성하여 실행하는 함수
<br>

- Function: `write(LBA: int, value: str)`
  - Return: `None`
  - Description
    - 외부에서 `write` 명령어를 호출하여 사용할 수 있는 함수
<br>

- Function: `erase(LBA: int, size: int)`
  - Return: `None`
  - Description
    - 외부에서 `erase` 명령어를 호출하여 사용할 수 있는 함수
<br>

- Function: `eraseRange(start_LBA: int, end_LBA: int)`
  - Return: `None`
  - Description
    - 외부에서 `eraseRange` 명령어를 호출하여 사용할 수 있는 함수
<br>

- Function: `fullwrite(value: str)`
  - Return: `None`
  - Description
    - 외부에서 `fullwrite` 명령어를 호출하여 사용할 수 있는 함수
<br>

- Function: `readCompare(LBA: int, value: str)`
  - Return: `bool`
  - Description
    - 외부에서 `readCompare` 명령어를 호출하여 사용할 수 있는 함수
    - `LBA`의 값을 읽어 `value`와 일치하는지 확인
<br>

- Function: `fullreadCompare(values: Optional[Dict], all_value: str)`
  - Return: `bool`
  - Description
    - 외부에서 `fullreadCompare` 명령어를 호출하여 사용할 수 있는 함수
    - `values` : 각각의 LBA별 값을 세팅하여 비교할 때 사용
    - `all_values` : 전체 LBA가 동일한 값을 읽어오는지 확인할 때 사용
<br>

- Function: `run()`
  - Return: `bool`
  - Description
    - 제공하는 API들을 활용하여 Test Script에서 실행할 Scenario를 작성할 함수
<br>

<summary>접기/펼치기</summary>
</details>

---

# FileName: `FullWriteReadCompare.py`

fullwrite & fullread 테스트용

<details>

## ClassName: FullWriteReadCompare
- Function: `run()`
  - Return: `bool`
  - Description
<br>

<summary>접기/펼치기</summary>
</details>


