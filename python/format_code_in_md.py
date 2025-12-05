#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
本脚本用于格式化 markdown 文件中的 python 代码
原理：识别 python 代码块，使用 black 格式化代码块
"""
import re
import subprocess
from pathlib import Path


def format_markdown_python_code(markdown_file: str):
    """格式化 markdown 文件中的 python 代码

    :param markdown_file: `markdown` 文件路径
    """
    with open(markdown_file, "r") as file:
        content = file.read()

    # 使用正则表达式找到所有的Python代码块
    pattern = r"```python\n(.*?)\n```"
    matches = re.findall(pattern, content, re.DOTALL)

    for match in matches:
        # 将找到的代码块写入临时文件
        temp_file = Path("temp_code.py")
        with temp_file.open("w+") as temp:
            temp.write(match)

        # 使用black格式化临时文件中的代码
        subprocess.run(["black", str(temp_file)])

        # 读取格式化后的代码
        with temp_file.open("r") as temp:
            formatted_code = temp.read()

        # PEP8 要求在文件末尾添加一个空行，在 `markdown` 文件中，无需添加
        formatted_code = formatted_code.rstrip("\n")

        # 替换原始内容中的代码块为格式化后的代码
        content = content.replace(
            f"```python\n{match}\n```", f"```python\n{formatted_code}\n```"
        )

    # 将格式化后的内容写回Markdown文件
    with open(markdown_file, "w") as file:
        file.write(content)

    # 删除临时文件
    temp_file.unlink()


markdown_file = "README.md"
format_markdown_python_code(markdown_file)
