import ast
from typing import List, Dict
import os

class FunctionVisitor(ast.NodeVisitor):
    def __init__(self):
        self.functions = []

    def visit_FunctionDef(self, node):
        if node.name.startswith("__") and node.name.endswith("__") and node.name not in {"__init__", "__new__"}:
            return
        parameters = []
        for arg in node.args.args:
            if arg.arg != "self":
                parameters.append({
                    "Name": arg.arg,
                    "Type": "None" if arg.annotation is None else self.parse_annotation(arg.annotation)
                })
        return_type = "None" if node.returns is None else self.parse_annotation(node.returns)
        self.functions.append({
            "Function": node.name,
            "Parameters": parameters,
            "Return": return_type
        })
        self.generic_visit(node)

    def parse_annotation(self, annotation):
        if isinstance(annotation, ast.Name):
            return annotation.id
        elif isinstance(annotation, ast.Subscript):
            return f"{annotation.value.id}[{annotation.slice.value.id}]"
        elif isinstance(annotation, ast.Compare):
            left = self.parse_annotation(annotation.left)
            ops = [op.__class__.__name__ for op in annotation.ops]
            comparators = [self.parse_annotation(comp) for comp in annotation.comparators]
            return f"Compare(left={left}, ops={ops}, comparators={comparators})"
        return ast.dump(annotation)

class ClassVisitor(ast.NodeVisitor):
    def __init__(self):
        self.classes = {}

    def visit_ClassDef(self, node):
        function_visitor = FunctionVisitor()
        function_visitor.visit(node)
        self.classes[node.name] = function_visitor.functions

def analyze_file(file_path: str) -> Dict[str, List[Dict]]:
    with open(file_path, "r", encoding="utf-8") as file:
        code = file.read()
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        print(f"Syntax error in {file_path}: {e}")
        return {}
    class_visitor = ClassVisitor()
    class_visitor.visit(tree)
    return class_visitor.classes

def analyze_files(file_paths: List[str]) -> Dict[str, List[Dict]]:
    class_info = {}
    for file_path in file_paths:
        if not file_path.endswith(".py") or file_path == "Ast.py":
            continue
        file_class_info = analyze_file(file_path)
        class_info[file_path] = file_class_info
    return class_info

def generate_markdown(class_info: Dict[str, List[Dict]]) -> str:
    markdown_str = ""
    for file_path, classes in class_info.items():
        markdown_str += f"# FileName: `{file_path}`\n"
        for class_name, functions in classes.items():
            markdown_str += f"## ClassName: {class_name}\n"
            for function_info in functions:
                function_name = function_info['Function']
                markdown_str += f"- Function: `{function_name}("
                params_str = ", ".join([f"{param['Name']}: {param['Type']}" for param in function_info['Parameters']])
                markdown_str += f"{params_str})`\n"
                markdown_str += f"  - Return: `{function_info['Return']}`\n"
                markdown_str += f"  - Description\n"
                markdown_str += "\n"
        markdown_str += "\n\n"
    return markdown_str

def write_to_readme(markdown_str: str):
    with open("README.md", "w", encoding="utf-8") as readme_file:
        readme_file.write(markdown_str)

# 현재 디렉토리에서 .py 파일 목록을 가져옴
py_files = [file for file in os.listdir() if file.endswith(".py")]

# Ast.py를 제외한 모든 .py 파일에 대해 분석을 수행
class_info = analyze_files(py_files)
markdown_str = generate_markdown(class_info)
write_to_readme(markdown_str)
