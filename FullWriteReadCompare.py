from TestRunner import TestRunner

class FullWriteReadCompare(TestRunner):
    def run(self) -> bool:
        self.fullwrite("0x77777710")
        self.write(99, "0x77777711")
        return self.fullreadCompare(all_value="0x77777710")