# 腾讯 Python 语言编程指南

《腾讯 Python 语言编程指南》是腾讯代码委员会 Python 分会在代码审查（Code Review, CR）中总结的编程实践集合，展示了 Python 编程中常见的问题和解决方案。

## 目录

- [腾讯 Python 语言编程指南](#腾讯-python-语言编程指南)
  - [目录](#目录)
  - [前言与指南定位](#前言与指南定位)
    - [前言](#前言)
    - [指南定位](#指南定位)
  - [`Pythonic` 与编码规范](#pythonic-与编码规范)
    - [关于 `Pythonic`](#关于-pythonic)
    - [代码为人而写](#代码为人而写)
    - [关于注释](#关于注释)
    - [严禁硬编码敏感信息](#严禁硬编码敏感信息)
    - [使用表驱动法简化代码](#使用表驱动法简化代码)
    - [条件表达式（三元表达式）](#条件表达式三元表达式)
    - [列表推导](#列表推导)
    - [善用生成器表达式](#善用生成器表达式)
    - [使用 zip 遍历两个列表](#使用-zip-遍历两个列表)
    - [慎用黑魔法](#慎用黑魔法)
    - [命名](#命名)
  - [Python 基础](#python-基础)
    - [版本选择](#版本选择)
    - [解释器](#解释器)
    - [环境管理](#环境管理)
    - [软件源](#软件源)
    - [代码检查工具](#代码检查工具)
    - [屏蔽检查](#屏蔽检查)
    - [代码格式化工具](#代码格式化工具)
    - [Shebang](#shebang)
  - [Python 语法与特性](#python-语法与特性)
    - [缩进的使用](#缩进的使用)
    - [单引号与双引号](#单引号与双引号)
    - [代码最大行宽](#代码最大行宽)
    - [全局变量](#全局变量)
    - [真值测试](#真值测试)
    - [绝对导入和相对导入](#绝对导入和相对导入)
    - [循环依赖的处理](#循环依赖的处理)
    - [延迟绑定](#延迟绑定)
    - [引用赋值、浅拷贝和深拷贝](#引用赋值浅拷贝和深拷贝)
      - [pb 对象的拷贝](#pb-对象的拷贝)
    - [字节与字符串（bytes \& str）](#字节与字符串bytes--str)
    - [序列切片（slicing）](#序列切片slicing)
    - [字符串格式化](#字符串格式化)
    - [分号使用](#分号使用)
    - [错误信息](#错误信息)
    - [数值精度](#数值精度)
    - [字典解包与格式化](#字典解包与格式化)
    - [善用 dataclass](#善用-dataclass)
    - [类型注解（typing）](#类型注解typing)
      - [同一个文件中循环引用注解](#同一个文件中循环引用注解)
      - [跨文件中循环引用注解](#跨文件中循环引用注解)
      - [函数注解](#函数注解)
      - [生成器注解](#生成器注解)
      - [协程注解](#协程注解)
    - [关于 `__future__`](#关于-__future__)
    - [字面量](#字面量)
    - [JSON 字符串处理](#json-字符串处理)
    - [避免浮点数直接比较](#避免浮点数直接比较)
  - [惯用法](#惯用法)
    - [使用 with 语句管理资源](#使用-with-语句管理资源)
    - [优先使用标准库方法](#优先使用标准库方法)
    - [文件存在判断](#文件存在判断)
    - [使用 enumerate 代替手动维护索引](#使用-enumerate-代替手动维护索引)
    - [使用 zip 代替手动并行迭代](#使用-zip-代替手动并行迭代)
    - [使用 `collections.defaultdict` 代替手动检查键是否存在](#使用-collectionsdefaultdict-代替手动检查键是否存在)
    - [使用 `namedtuple` 代替普通元组](#使用-namedtuple-代替普通元组)
    - [使用 `json` 模块代替 `eval` 进行字符串解析](#使用-json-模块代替-eval-进行字符串解析)
    - [避免 `set` 进行数据操作（机器学习）](#避免-set-进行数据操作机器学习)
    - [避免过时用法](#避免过时用法)
    - [列表去重](#列表去重)
  - [性能优化](#性能优化)
    - [循环中避免字符串拼接](#循环中避免字符串拼接)
    - [使用列表推导式代替循环添加元素](#使用列表推导式代替循环添加元素)
    - [使用生成器代替列表（适用于大数据）](#使用生成器代替列表适用于大数据)
    - [使用集合（set）代替列表进行成员检测](#使用集合set代替列表进行成员检测)
    - [减少不必要的属性访问](#减少不必要的属性访问)
  - [数据结构与算法](#数据结构与算法)
    - [`collections` 模块](#collections-模块)
    - [排序](#排序)
  - [面向对象与元编程](#面向对象与元编程)
    - [方法解析顺序（MRO）](#方法解析顺序mro)
    - [私有属性](#私有属性)
    - [Getter、Setter 和 Property](#gettersetter-和-property)
    - [函数式编程](#函数式编程)
    - [装饰器](#装饰器)
      - [装饰器适用场景](#装饰器适用场景)
      - [注意事项](#注意事项)
    - [闭包](#闭包)
      - [命名空间干净](#命名空间干净)
      - [变量始终存在内存](#变量始终存在内存)
      - [陷阱：延迟绑定闭包](#陷阱延迟绑定闭包)
  - [异常、调试与测试](#异常调试与测试)
    - [使用日志](#使用日志)
    - [异常处理](#异常处理)
    - [使用 `pdb` 进行调试](#使用-pdb-进行调试)
    - [使用 `gdb` 进行调试](#使用-gdb-进行调试)
    - [调试 - 程序崩溃/卡死分析](#调试---程序崩溃卡死分析)
    - [测试](#测试)
      - [表格驱动](#表格驱动)
      - [行为驱动](#行为驱动)
      - [Mock建议](#mock建议)
      - [覆盖率建议](#覆盖率建议)
  - [并发编程](#并发编程)
    - [并发与并行的区别](#并发与并行的区别)
    - [Python 实现并发与并行的方法](#python-实现并发与并行的方法)
    - [选择并发/并行模型](#选择并发并行模型)
    - [多线程（Threading）](#多线程threading)
    - [多进程（Multiprocessing）](#多进程multiprocessing)
    - [协程（Coroutine）](#协程coroutine)
    - [使用 `concurrent.futures`](#使用-concurrentfutures)
    - [全局解释器锁（GIL）](#全局解释器锁gil)
    - [协程](#协程)
      - [协程并发调用](#协程并发调用)
      - [协程调度](#协程调度)
      - [协程包装](#协程包装)
      - [协程安全](#协程安全)
      - [协程其他使用方式](#协程其他使用方式)
  - [文件与IO](#文件与io)
    - [序列化与反序列化](#序列化与反序列化)
      - [序列化格式](#序列化格式)
      - [序列化安全](#序列化安全)
  - [高级用法与框架](#高级用法与框架)
    - [跨语言调用](#跨语言调用)
      - [Python 调用其他语言](#python-调用其他语言)
      - [其他语言调用 Python](#其他语言调用-python)
    - [自动化文档生成](#自动化文档生成)
    - [性能分析](#性能分析)
    - [网络编程](#网络编程)
    - [数据库操作](#数据库操作)
  - [安全](#安全)
    - [加密算法](#加密算法)
    - [哈希函数](#哈希函数)
    - [数字签名](#数字签名)
    - [密钥管理](#密钥管理)

## 前言与指南定位

### 前言

Python 语言功能强大且简洁易读，开发者可以快速上手。  
这也导致开发者的学习路径差异较大，很多人容易带着之前的编程习惯，而无法充分发挥 Python 的特性。  
本指南通过 CR 中发现的代表性代码片段进行分析和经验总结，以帮助开发者写出更 **Pythonic** 的代码。

### 指南定位

本指南主要以条目方式定义问题，提出推荐方案，不会涉及具体语言教程、库的使用，以及编码规范。  
目标读者应具备 Python 语言的基本认知。

## `Pythonic` 与编码规范

### 关于 `Pythonic`

Python 开发者用 Pythonic 来描述符合特定风格的代码。  
这种风格既不是严密的规范，也不是由编译器强加给开发者的规则，而是大家在使用 Python 语言协同工作的过程中逐渐形成的习惯。

- [`PEP 20`](https://peps.python.org/pep-0020/)  
  可以通过执行 `import this` 来查看《The Zen of Python》(《Python之禅》)。  
  Python 编程哲学的重要原则：**每件事都应该有一种直白、明显的方法来完成，而且最好只有一种方法。**

- [`PEP 8`](https://peps.python.org/pep-0008/) (Python Enhancement Proposals - 8)  
  这是针对 Python 代码格式制定的规范。许多业内的 Python 编程规范均衍生自此。

- [`腾讯 Python 编码风格与规范`](https://git.woa.com/standards/python)

### 代码为人而写

Python 代码是为人编写的，这意味着可读性和可维护性应该是我们编程时的重要考量。

1. 遵循 PEP 8 规范

    PEP 8 是 Python 的代码风格指南，遵循这些规范可以提高代码的一致性和可读性。

    ```python
    # 好的命名和缩进
    import math

    def calculate_area(radius):
        """Calculate the area of a circle given its radius."""
        return math.pi * radius ** 2
    ```

1. 使用有意义的变量和函数名称

    变量、函数和类的名称应该清晰地描述其用途和功能。

    ```python
    # 不好的命名
    def fun(x):
        return x * x

    # 好的命名
    def calculate_square(number):
        return number * number
    ```

1. 写注释和文档字符串

    注释和文档字符串有助于解释代码的目的和功能，尤其是复杂逻辑的部分。

    ```python
    def calculate_square(number):
        """
        Calculate the square of a number.

        Args:
            number (int or float): The number to be squared.

        Returns:
            int or float: The square of the input number.
        """
        return number * number
    ```

1. 避免魔法数和魔法字符串

    使用常量代替魔法数和魔法字符串，以便理解其意义。

    ```python
    # 魔法数，不推荐
    if error_code == 404:
        print("Not Found")

    # 使用常量，推荐
    NOT_FOUND = 404
    if error_code == NOT_FOUND:
        print("Not Found")
    ```

1. 遵循单一职责原则

    每个函数或类应该仅负责完成一项任务，这有助于代码的可读性和可维护性。

    ```python
    # 不好的设计，一个函数完成太多任务
    def process_data(data):
        # 读取数据
        # 处理数据
        # 保存结果
        pass

    # 好的设计，将任务拆分
    def read_data(source):
        pass

    def process_data(data):
        pass

    def save_results(results):
        pass
    ```

1. 避免过度优化

    提前优化可能会使代码复杂化，导致难以理解和维护。  
    优先编写功能正确且易于理解的代码，只有在确有需要时再进行优化。

    ```python
    # 过度优化，不推荐
    def calculate_sum_optimized(numbers):
        return sum(map(lambda x: x if x % 2 == 0 else 0, numbers))

    # 简单明了，推荐
    def calculate_sum(numbers):
        total = 0
        for number in numbers:
            if number % 2 == 0:
                total += number
        return total
    ```

1. 使用列表推导和生成器表达式

    列表推导和生成器表达式可以使代码更简洁，但要避免过于复杂的表达式。

    ```python
    # 简单的列表推导
    squares = [x * x for x in range(10)]

    # 复杂的列表推导，避免
    complex_list = [x * y for x in range(10) for y in range(10) if x != y]

    # 使用生成器表达式
    squares_gen = (x * x for x in range(10))
    ```

1. 使用上下文管理器

    上下文管理器（如 `with` 语句）可以更好地管理资源，确保资源在使用后正确释放。

    ```python
    # 使用上下文管理器
    with open('file.txt', 'r') as file:
        content = file.read()

    # 不使用上下文管理器
    file = open('file.txt', 'r')
    try:
        content = file.read()
    finally:
        file.close()
    ```

1. 避免深层嵌套

    深层嵌套的代码难以阅读和理解，尽量避免。

    ```python
    # 深层嵌套，不推荐
    if condition1:
        if condition2:
            if condition3:
                do_something()

    # 扁平化代码，推荐
    if condition1 and condition2 and condition3:
        do_something()
    ```

1. 写测试

    编写单元测试和集成测试有助于确保代码的正确性和可维护性。

    ```python
    import unittest
    
    def calculate_square(number):
        return number * number
    
    class TestMathFunctions(unittest.TestCase):
    
        def test_calculate_square(self):
            self.assertEqual(calculate_square(2), 4)
            self.assertEqual(calculate_square(-2), 4)
            self.assertEqual(calculate_square(0), 0)
    
    if __name__ == '__main__':
        unittest.main()
    ```

### 关于注释

- 注释应当简洁明了  
注释的目的是帮助理解代码，因此应该尽量简洁明了，避免过长的段落。

- 避免显而易见的注释  
不要注释那些一眼就能看懂的代码，例如 `i += 1 # 增加1`。  
这样的注释没有实质性帮助。

- 注释解释“为什么”，而不是"怎么样"  
注释应当解释代码的目的或背景，而不是代码本身在做什么。

    ```python
    # 使用二分查找来提高搜索效率
    mid = (low + high) // 2
    ```

- 维护注释的同步性  
如果代码发生了改变，注释也应当相应更新。  
陈旧的注释会导致误解。  

- 避免在代码中包含敏感信息  
注释中不应包含密码、密钥或其他敏感信息。
CodeCC 工具可以扫描出疑似敏感信息内容。

- 使用块注释解释复杂逻辑  
对于复杂的算法或逻辑，可以使用块注释来进行详细解释。

    ```python
    """
    使用动态规划解决背包问题
    weights: 物品重量列表
    values: 物品价值列表
    capacity: 背包容量
    """
    ```

- 在函数和模块中添加文档字符串（Docstring）  
使用文档字符串来描述函数、类和模块的功能。

    ```python
    def add(a, b):
        """
        返回两个数的和
        :param a: 第一个数
        :param b: 第二个数
        :return: a 和 b 的和
        """
        return a + b
    ```

- 遵循项目的注释规范
- 使用TODO注释标记待完成任务  
代码功能不是一蹴而就的，对于部分功能存在不够完美，小的缺陷，需要使用 TODO 注释。  
添加 TODO 应该标注好相关的工单(tapd, issue)链接， 关注人，及简单解释。  
对于修复的问题，需要及时移除TODO，避免引起困扰。

    ```python
    # TODO(tapd_url): @username 关注这里的性能优化
    ```

- 不要使用注释删除代码  
现代工程开发有成熟的代码版本管理系统，不要使用注释来屏蔽代码，可以使用分支来进行管理。  
及时清理淘汰的代码，保持代码健康状态。

### 严禁硬编码敏感信息

对于服务的 IP、域名、账号、密码等信息，应使用配置加载方式进行，严禁将敏感信息硬编码在代码中。  
Python 中配置文件多种多样，包括 `JSON`、`YAML`、`.env` 等。  
小型项目可以使用 `JSON` 进行管理，`YAML` 的好处是可以进一步注释，更易阅读。  
大型项目推荐使用 `Pydantic` 进行管理配置，它带有更丰富的功能，比如校验、类型识别等。  

### 使用表驱动法简化代码

表驱动法是一种编程技巧，通过使用数据表来控制程序的逻辑流，从而减少冗余代码和提高代码的可维护性。

```python
def get_permissions(role):
    if role == "admin":
        return ["read", "write", "delete"]
    elif role == "user":
        return ["read", "write"]
    elif role == "guest":
        return ["read"]
    else:
        return []

# 使用表驱动法简化代码
permissions_table = {
    "admin": ["read", "write", "delete"],
    "user": ["read", "write"],
    "guest": ["read"],
}

def get_permissions(role):
    return permissions_table.get(role, [])

# 测试
print(get_permissions("admin"))  # 输出: ['read', 'write', 'delete']
print(get_permissions("guest"))  # 输出: ['read']
print(get_permissions("unknown"))  # 输出: []
```

### 条件表达式（三元表达式）

Python 里可以使用条件表达式来简化条件语句，但强烈建议不要嵌套使用。

```python
# Bad
# 不推荐将条件表达式嵌套，会降低代码可读性
a = 10
b = 20
c = 30

# 使用嵌套三元表达式计算最大值
max_value = (a if a > b else b) if (a if a > b else b) > c else c

print(max_value)  # 输出: 30

# Good
# 定义一个条件变量
is_sunny = True

# 使用三元表达式
activity = "Go for a walk" if is_sunny else "Stay indoors"

print(activity)  # 输出: Go for a walk

# 与下面的代码等价
if is_sunny:
    activity = "Go for a walk"
else:
    activity = "Stay indoors"

a = 10
b = 20

# 使用三元表达式计算最大值
max_value = a if a > b else b

print(max_value)  # 输出: 20

# 与下面的代码等价
if a > b:
    max_value = a
else:
    max_value = b
```

### 列表推导

`列表推导`（List Comprehension）是 Python 中一种简洁且强大的生成列表的方法。它提供了一种简洁的语法来创建新列表，使代码更具可读性和表达力。

- 列表推导与传统方法比较

    ```python
    # 传统方法
    evens = []
    for x in range(10):
        if x % 2 == 0:
            evens.append(x)
    print(evens)  # 输出: [0, 2, 4, 6, 8]

    # 列表推导
    evens = [x for x in range(10) if x % 2 == 0]
    print(evens)  # 输出: [0, 2, 4, 6, 8]
    ```

- 不要嵌套列表推导

    列表推导简洁，但如果滥用嵌套，可读性反而比传统写法差。

    ```python
    # 嵌套列表推导
    matrix = [[j for j in range(3)] for i in range(3)]
    print(matrix)  # 输出: [[0, 1, 2], [0, 1, 2], [0, 1, 2]]
    
    # 生成一个大矩阵
    matrix = [[x * y for y in range(1000)] for x in range(1000)]
    # 这种操作可能会在大规模数据下导致性能问题
    
    # 带有错误处理的复杂嵌套列表推导
    try:
        result = [[1 / x for x in range(-1, 2)] for y in range(3)]
    except ZeroDivisionError as e:
        print(f"Error: {e}")
    # 这个例子中，错误处理会变得复杂
    
    # 多重嵌套时，传统循环更有可读性
    matrix = []
    for x in range(3):
        row = []
        for y in range(3):
            row.append(x * y)
        matrix.append(row)
    print(matrix)  # 输出: [[0, 0, 0], [0, 1, 2], [0, 2, 4]]
    ```

### 善用生成器表达式

当处理大数据量时，使用生成器表达式（Generator Expressions）可以显著减少内存消耗，因为生成器表达式不会一次性生成整个列表，而是逐个生成元素。  
生成器表达式类似于列表推导，不同之处在于它使用圆括号 () 而不是方括号 []。

- 列表推导与生成器表达式比较

    ```python
    # 列表推导
    squares = [x**2 for x in range(1000000)]
    
    # 生成器表达式
    squares_gen = (x**2 for x in range(1000000))


    # 使用生成器表达式计算总和
    
    # 使用列表推导
    squares = [x**2 for x in range(1000000)]
    total = sum(squares)
    print(total)
    
    # 使用生成器表达式
    squares_gen = (x**2 for x in range(1000000))
    total_gen = sum(squares_gen)
    print(total_gen)
    
    # 迭代生成器
    # 生成器表达式
    squares_gen = (x**2 for x in range(10))
    
    # 迭代生成器
    for square in squares_gen:
        print(square)
    ```

### 使用 zip 遍历两个列表

在 Python 中使用 `zip` 可以简化并行遍历多个列表的操作。  
相比于传统方法，`zip` 提供了一种更加简洁和优雅的方式来处理多个列表的并行迭代。

- 传统方法与 zip 方法比较

    ```python
    list1 = [1, 2, 3]
    list2 = ["a", "b", "c"]
    
    # 传统方法
    for i in range(min(len(list1), len(list2))):
        print(list1[i], list2[i])
    
    # 使用 zip
    result = list(zip(list1, list2))
    print(result)
    
    keys = ["name", "age", "city"]
    values = ["Alice", 25, "New York"]
    
    # 传统方法
    result = {}
    for i in range(min(len(keys), len(values))):
        result[keys[i]] = values[i]
    print(result)  # 输出: {'name': 'Alice', 'age': 25, 'city': 'New York'}
    
    # 使用 zip
    result = dict(zip(keys, values))
    print(result)  # 输出: {'name': 'Alice', 'age': 25, 'city': 'New York'}
    ```

### 慎用黑魔法

在 Python 编程中，有一些被称为“黑魔法”的技巧和方法，它们虽然强大但也非常容易引发混乱和难以维护的代码。

1. 动态修改类和对象

    在运行时动态地添加或修改类和对象的属性和方法。

    - **慎用场景**：动态修改类和对象的行为在某些情况下非常有用，比如在测试中模拟对象行为，但在生产代码中应谨慎使用。
    - **替代方案**：尽量使用继承或组合来扩展类的功能，而不是在运行时修改它们。
    - **维护性**：确保任何动态修改都有清晰的文档和注释，并且限制其作用域。

1. 使用 `eval` 和 `exec`

    用 `eval` 和 `exec` 执行字符串形式的 Python 代码。

    - **安全风险**：这两个函数可能导致安全漏洞，特别是当处理用户输入时。
    - **替代方案**：使用更安全的表达方式，例如 ast.literal_eval 来解析字符串。
    - **可读性和调试**：这类代码难以阅读和调试，应尽可能避免使用。

1. 猴子补丁（Monkey Patching）

    在运行时修改或扩展现有模块或类的行为。

    - **慎用场景**：猴子补丁可以用于修补第三方库的缺陷，但在修改标准库或大型项目时应极其谨慎。
    - **替代方案**：如果可能，提交补丁给原作者或在本地派生出一个修改版。
    - **维护性**：详细记录猴子补丁的目的和影响，并在代码中添加明确的注释。

1. 反射和元编程

    使用反射（如 `getattr`, `setattr`, `hasattr`）和元编程（如元类）来动态操作对象和类。

    - **复杂性**：反射和元编程增加了代码的复杂性和理解难度。
    - **使用场景**：在框架或库开发中，反射和元编程可以提供很大的灵活性，但在应用代码中应尽量避免。
    - **替代方案**：使用更明确的设计模式，如工厂模式或策略模式，来实现动态行为。

1. 过度使用装饰器

    装饰器可以改变函数或方法的行为，但过度使用会导致代码难以理解。

    - **可读性**：装饰器应尽量简单和明确，避免多层嵌套的复杂装饰器链。
    - **使用场景**：装饰器适用于跨切面关注点（如日志、权限检查），但应控制其使用范围。
    - **文档和注释**：确保每个装饰器都有清晰的文档和使用示例。

1. 使用私有变量和方法

    通过命名约定（如 `_var` 和 `__var`）来创建私有变量和方法。

    - **命名约定**：理解和遵循 Python 的命名约定，知道单下划线和双下划线的区别。
    - **封装性**：尊重类的封装性，不轻易访问或修改私有变量和方法。
    - **设计思考**：考虑是否真的需要使用私有变量，或者通过公开的接口来实现相同的功能。

### 命名

建议阅读编码规范，[命名章节](https://git.woa.com/standards/python#118-%E5%91%BD%E5%90%8D)。

常见的模块、变量、函数、方法、参数均需遵守 `snake_case` 风格。  
Python 里仅类和异常会使用 `PascalCase` 风格。

变量的命名应该具备简洁易读特性。  

- 不要创造性使用缩写或拼音，也不宜过于冗余。

    ```python
    # Bad
    the_number_of_items_in_the_user_shopping_cart = 5

    # Good
    item_count = 5
    ```

- 对于一些约定俗称的场景比如文件打开，算法里特定变量，可以遵循已有规范。

    ```python
    # 约定俗成的情况下，这里使用单字母没有问题
    with open(file, "r") as f:
        f.read()

    # 循环使用
    for i in range(5):
        print(i)

    # 对于有意义的场景，尽量避免使用单字母
    user_list = ['zhangsan', 'lisi']
    for user in user_list:
        print(user)
    ```

- 避免保留字和内置函数名

    ```python
    # Bad
    def list():
        pass

    def dict():
        pass

    # Good
    def create_list():
        pass

    def build_dict():
        pass
    ```

- 使用有意义的名称  
    变量名应尽量具备描述性，尤其是在函数参数中，避免使用单字母名称，除非在非常短小且明了的上下文中。

    ```python
    # Good
    def calculate_area(width, height):
        return width * height
    
    # Bad
    def calc(w, h):
        return w * h
    ```

- 使用前缀和后缀  
    可以使用前缀和后缀来提供额外的上下文信息。

    ```python
    # Good
    is_valid = True  # 布尔值变量
    user_list = ["Alice", "Bob"]  # 列表变量
    max_retries = 5  # 数值变量
    
    # Bad
    valid = True
    users = ["Alice", "Bob"]
    retries = 5
    ```

- 避免魔法数字  
    使用具描述性的变量名代替魔法数字，以提高代码的可读性。

    ```python
    # Bad
    for i in range(3):
        print(i)
    
    # Good
    MAX_ITERATIONS = 3
    for i in range(MAX_ITERATIONS):
        print(i)
    ```

## Python 基础

### 版本选择

1. **现状**  
    Python 语言因为一些历史原因，被割裂为 2 和 3 两个大版本。  
    `Python 2` 的最后一个子版本为 [`2.7.18`](https://www.python.org/downloads/release/python-2718/)，该版本已经不再维护。  
    除特殊原因需要维护 `Python 2` 的项目外，强烈建议选择 `Python 3` 进行开发。

1. **版本生命周期**  
    可以在 [`Python 发布周期`](https://devguide.python.org/versions/) 查看各子版本发布状态。  
    目前 `Python 3.9` 之前的版本均已处于 EOL（end of life），不再推荐使用。  
    可以在[`Python 3` 各版本特性](https://docs.python.org/zh-cn/3.12//whatsnew/index.html) 查看相关变化。

1. **特殊情况**  
    尽管对版本做了推荐，但具体到各个业务领域，有可能有特殊情况:  

   - trpc 对版本要求 `3.10`
   - pyspark2 对版本要求 `3.6`
   - pyspark3 对版本要求 `3.8`

### 解释器

除非特殊指定，一般所指的 `Python 解释器` 是 [CPython](https://github.com/python/cpython)。  
业内也有其他语言实现的解释器版本，比如 `Jython`、`IronPython`、`PyPy` 等，应谨慎使用。  
本指南默认在 `CPython` 范畴下。

- **[TPython](https://python.woa.com/)**  
  公司内部也有团队在进行 Python 解释器的定制工作，主要是基于 `CPython` 进行性能优化等。

### 环境管理

推荐使用 `虚拟环境` 来隔离不同项目之间的依赖和环境，以避免干扰。  
虚拟环境允许每个项目拥有自己的依赖包和 Python 解释器版本，而不影响系统全局的 Python 环境。

考虑到跨版本虚拟环境管理、易用性、空间占用、法律合规等因素，推荐使用 [Miniforge](https://github.com/conda-forge/miniforge) 来作为管理工具。  
它拥有近似 `conda` 的命令设计，由开源社区维护，配合腾讯自建的 `PyPI` 镜像源，可以在可用性、安全性、合规性方面，取得比较好的平衡。

### 软件源

Python 拥有一个非常繁荣的软件包市场，[`PyPI`](https://pypi.org/) 是社区维护的包索引源。  
公司内部建有专门的 [软件源](https://mirrors.tencent.com/pypi/simple/)，考虑到安全性，推荐优先使用公司内部的源。

- 上传包  
  参考 [内部PyPI服务](https://iwiki.woa.com/p/50796072) 可以将自己的 Python 包上传到公司内部的软件源。

- 注意事项  
  - 软件源在下载时是不需要配置账号密码的，开发者应通过配置文件管理软件源的 key。
  - 自定义包注意包名，避免与社区包同名，造成冲突。

以下是一个常见配置，位于 `~/.pip/pip.conf` 文件中：

```ini
[global]
# 社区源
index-url=https://mirrors.tencent.com/pypi/simple/
# 内部源
extra-index-url=https://mirrors.tencent.com/repository/pypi/tencent_pypi/simple

[install]
trusted-host=mirrors.tencent.com
```

### 代码检查工具

使用代码检查工具（Linter）可以帮助检查代码质量问题，部分工具具备一定动态推断能力，可以发现一些人力不易察觉的问题。  
常见的 Linter 工具有 Flake8、Pylint、Pyflakes。  

推荐使用 [`Pylint`](https://pylint.pycqa.org/) 检查代码错误（如语法错误、未使用变量等）、代码风格问题、代码复杂度和代码异味。  

**强烈推荐**在项目 CI pipeline 里配置 `CodeCC 腾讯代码分析` [规则集](https://codecc.woa.com/codecc/git_1253738/checkerset/codecc_fast_python/2147483647/manage)进行检查。

### 屏蔽检查

正常情况下，应该充分使用代码检查工具，但在具体实践过程中，这么做会让代码很繁琐，可能需要屏蔽部分检查，可以通过多种方式进行。  

```python
# 行级屏蔽，放在警告行尾
# pylint: disable=broad-except

# 文件级屏蔽，放在文件顶部
# pylint: disable=e731
```

### 代码格式化工具

推荐使用代码格式化工具（Formatter）保持代码风格一致性。  
常见的 Formatter 工具有 Black、YAPF 和 autopep8。  
推荐使用 [`Black`](https://black.readthedocs.io/en/stable/) 来格式化代码。  
Black 的格式化规则是兼容 [`腾讯 Python 编码风格与规范`](https://git.woa.com/standards/python)的。

### Shebang

`Shebang` 是一种传统的指定 Python 运行环境的方式。  
现代社区推荐使用虚拟环境来管理项目依赖和解释器版本。  
对于跨环境使用场景，`Shebang` 指定的路径可能不存在，容易引起误解。  

- Shebang 示例

    在 Python 脚本的第一行添加 Shebang，可以指定运行该脚本所需的解释器。例如：

    ```python
    #!/usr/bin/env python3
    
    print("Hello, world!")
    ```

## Python 语法与特性

### 缩进的使用

Python 编程语言与其他语言最显著的区别即 **强制缩进**，但 Python 并未强制规定使用几个空格，一般需要保证同一个代码块一致即可。  
考虑到代码编程风格统一，Python 社区和 **PEP 8** 建议使用 4 个空格作为缩进标准，并 **强烈反对** 空格与制表符混用。  
同时推荐使用格式化工具来自动格式化代码，保持缩进的一致性。

### 单引号与双引号

Python 字符串的单引号和双引号均可使用，但实际工作中一般推荐使用双引号。  
也可以使用格式化工具如 **Black** 自动保持字符串的一致性。

### 代码最大行宽

编码规范规定每行最大宽度为 `120`，一些工具默认是 `79`，这主要源于早期计算机屏幕的显示限制。  
虽然现代开发环境的硬件已经足够显示更多内容，但仍强烈推荐控制行宽，避免增加阅读负担。

不要用反斜杠（行连接符）来连接一个长的代码行，应使用括号来连接，这样可以让代码更清晰。

```python
# Bad

# 长字符串
long_string = "This is a very long string that we want to break into " \
              "multiple lines for better readability without actually " \
              "introducing newlines into the string."
print(long_string)

# 长表达式
result = 1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9 + 10 + \
         11 + 12 + 13 + 14 + 15 + 16 + 17 + 18 + 19 + 20
print(result)

# 函数定义
def long_function_name(var_one, var_two, var_three, var_four, \
                       var_five, var_six):
    print(var_one)

# Good

# 长字符串
long_string = ("This is a very long string that we want to break into "
               "multiple lines for better readability without actually "
               "introducing newlines into the string.")
print(long_string)

# 长表达式
result = (1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9 + 10 +
          11 + 12 + 13 + 14 + 15 + 16 + 17 + 18 + 19 + 20)
print(result)

# 函数定义
def long_function_name(var_one, var_two, var_three, var_four,
                       var_five, var_six):
    print(var_one)
```

### 全局变量

在编程中，全局变量是指在所有作用域中都可以访问的变量。  
尽管全局变量可以简化代码的编写，但不当使用可能导致代码难以维护和调试。

1. 全局变量实践

    尽管全局变量可以简化某些操作，但过度使用会导致代码难以维护和调试。以下是一些最佳实践：

    - **避免过度使用全局变量**：尽量使用局部变量和函数参数来传递信息。
    - **命名规范**：使用全大写字母和下划线命名全局变量，以便区分。
    - **模块化设计**：将相关全局变量和常量集中在一个配置模块中。
    - **线程安全**：在多线程环境中使用全局变量时，注意同步问题，使用线程锁保护全局变量。

2. 示例

    以下是一个合理使用全局变量的示例，展示如何在一个配置模块中定义全局变量，并在其他模块中使用这些变量。

    - 配置模块 `config.py`

    ```python
    # config.py
    # 全局配置变量
    DATABASE_URI = "sqlite:///example.db"
    DEBUG_MODE = True
    ```

    - 主模块 `main.py`

    ```python
    # main.py
    import config
    
    def connect_to_database():
        print(f"Connecting to database at {config.DATABASE_URI}")
    
    def main():
        if config.DEBUG_MODE:
            print("Debug mode is enabled.")
        connect_to_database()
    
    if __name__ == "__main__":
        main()
    ```

    在这个示例中，全局变量 `DATABASE_URI` 和 `DEBUG_MODE` 被定义在 `config.py` 模块中，并在 `main.py` 中使用。这种做法可以提高代码的可维护性和可读性，同时避免全局变量的滥用。

### 真值测试

Python 中，真值测试（Truth Value Testing）是指将对象用于布尔上下文。例如在条件语句（if、while）或逻辑操作（and、or、not）时，Python 会自动将对象转换为布尔值（True 或 False）。

以下对象会被视为 False：

- None
- False
- 零值（0，0.0）
- 空序列（''，[]，{}，set()，()，range(0)）等

- 真值测试 - 不要通过序列长度判断是否为空

    ```python
    # 对于一个列表
    example_list = [1, 2, 3]

    # Bad
    if len(example_list) != 0:
        print("true")
    else:
        print("false")

    # Good
    if example_list:
        print("true")
    else:
        print("false")
    ```

- 真值测试 - 对于 bool 类型，无需显式的比较判断

    ```python
    # 对于 bool 类型
    example_bool = True

    # Bad
    if example_bool != False:
        print("true")
    else:
        print("false")

    # Good
    if example_bool:
        print("true")
    else:
        print("false")
    ```

- 真值测试 - 内联否定

    `采用内联形式的否定词` 指的是在表达条件时，直接在条件语句中使用否定词，而非通过复杂的逻辑或双重否定来实现。  
    这种形式通常更简洁、直观，且更符合自然语言的表达方式。

    ```python
    # 使用 is not 更符合自然语言习惯
    str1 = "hello"
    str2 = "world"
    
    # Bad
    if not str1 is str2:
        print("str1 is not str2")
    else:
        print("str1 is str2")
    
    # Good
    if str1 is not str2:
        print("str1 is not str2")
    else:
        print("str1 is str2")
    ```

### 绝对导入和相对导入

Python 官方文档和 PEP 8 均强调绝对导入， 因为 `绝对导入的清晰性和可维护性` 。

- 举例

    ```python
    # 项目结构如下
    """
    project
    ├── main.py
    ├── pkg1
    │   ├── __init__.py
    │   ├── module_a.py
    │   └── module_b.py
    └── pkg2
        ├── __init__.py
        ├── module_c.py
        └── module_d.py
    """
    
    # module_a.py
    from pkg2 import module_c
    
    def function_a():
        print("Function A from module_a")
    
    def call_function_c():
        print("Function call_function_c from module_a")
        module_c.function_c()
    
    # module_b.py
    def function_b():
        print("Function B from module_b")
    
    # module_c.py
    def function_c():
        print("Function C from module_c")
    
    # module_d.py
    def function_d():
        print("Function D from module_d")
    
    # main.py
    from pkg1 import module_a, module_b
    from pkg2 import module_c, module_d
    
    def main():
        module_a.function_a()
        module_a.call_function_c()
        module_b.function_b()
        module_c.function_c()
        module_d.function_d()
    
    if __name__ == "__main__":
        main()
    ```

Python 会将库文件目录中.pth文件记录的路径加入到sys.path中。基于此，可以把本地库的绝对路径记录到 xxx.pth 文件中，并拷贝到 site-packages 下，实现将本地库引入任意项目。

- 获取LIB

    ```python
    # 获取当前python的 site-packages 目录
    from distutils.sysconfig import get_python_lib
    print(get_python_lib())
    ```

### 循环依赖的处理

循环依赖（Circular Dependency）是指两个或多个模块互相依赖，最终形成一个环。  
在 Python 中，这种情况可能导致 `ImportError` 或 `AttributeError`，并且会让代码变得难以维护和调试。

可以使用以下几种方式解决：

- 延迟导入

    ```python
    # module_a.py
    def function_a():
        print("Function A from module_a")
        from module_b import function_b
        function_b()

    # module_b.py
    def function_b():
        print("Function B from module_b")
        # 通过将导入语句放在函数内部，而不是模块的顶层，
        # 可以避免在模块加载时发生循环依赖。
        from module_a import function_a
        function_a()
    ```

- 重构代码

    ```python
    # 重构代码，将互相依赖的部分放在一个单独的模块中，从而打破环形依赖。
    # common.py
    def shared_function():
        print("Shared function")

    # module_a.py
    from common import shared_function

    def function_a():
        print("Function A from module_a")
        shared_function()

    # module_b.py
    from common import shared_function

    def function_b():
        print("Function B from module_b")
        shared_function()
    ```

- 使用 importlib

    ```python
    # Python 的 importlib 模块提供了动态导入功能，可以在运行时导入模块，从而避免循环依赖
    # module_a.py
    import importlib
    
    def function_a():
        print("Function A from module_a")
        module_b = importlib.import_module('module_b')
        module_b.function_b()
    
    # module_b.py
    import importlib
    
    def function_b():
        print("Function B from module_b")
        module_a = importlib.import_module('module_a')
        module_a.function_a()
    ```

### 延迟绑定

Python中的延迟绑定，也称为后期绑定（Late Binding）是一种变量解析行为，主要在闭包和函数默认参数等场景中可能引发问题。

- 延迟绑定 - 函数默认参数绑定问题

    函数默认参数使用可变对象（如列表、字典、集合）作为函数参数的默认值时，会在函数定义时绑定，并在后续调用中共享，可能导致意外的副作用。  
    可变对象更容易出现副作用，而不可变对象（如整数、字符串、元组等）在特定情况下也可能出现意外行为。

- 可变对象作为函数默认参数问题举例

    ```python
    # 此处的本意是如果 my_list 参数不填，默认置为空列表，但实际并未如此
    def append_to_list(value, my_list=[]):
        my_list.append(value)
        return my_list

    result1 = append_to_list(1)
    result2 = append_to_list(2)
    result3 = append_to_list(3)

    print(result1)  # 输出: [1]
    print(result2)  # 输出: [1, 2]
    print(result3)  # 输出: [1, 2, 3]

    # 解决方案
    def append_to_list(value, my_list=None):
        if my_list is None:
            my_list = []
        my_list.append(value)
        return my_list

    # 第一次调用
    result1 = append_to_list(1)
    print(result1)  # 输出: [1]

    # 第二次调用
    result2 = append_to_list(2)
    print(result2)  # 输出: [2]
    ```

- 不可变对象作为函数默认参数问题举例

    ```python
    import time

    def log_message(message, timestamp=time.time()):
        print(f"{timestamp}: {message}")

    log_message("First message")
    time.sleep(2)
    log_message("Second message")

    # 这里预期是输出间隔 2 秒的两条日志，但实际上日志时间一样。

    # 解决方案
    def log_message(message, timestamp=None):
        if timestamp is None:
            timestamp = time.time()
        print(f"{timestamp}: {message}")

    log_message("First message")
    time.sleep(2)
    log_message("Second message")
    ```

- 延迟绑定 - 闭包

    在闭包中，内部函数引用的是外部函数的变量名，而不是变量的值。  
    在闭包执行时，变量名会在其作用域内被重新解析，这可能导致意外的结果。

    ```python
    def create_multipliers():
        return [lambda x: i * x for i in range(5)]
    
    for multiplier in create_multipliers():
        print(multiplier(2))
    
    # 上面代码的输出将是 8 五次，而不是 0, 2, 4, 6, 8。
    # 这是因为 lambda 表达式中的 i 是在 lambda 被调用时才解析的，而此时 i 的值已经是 4（循环结束时的值）
    
    # 解决方案
    def create_multipliers():
        return [lambda x, i=i: i * x for i in range(5)]
    
    for multiplier in create_multipliers():
        print(multiplier(2))
    ```

### 引用赋值、浅拷贝和深拷贝

Python 里不少人都会在引用赋值、浅拷贝、深拷贝上踩过坑。

- `引用赋值`：和浅拷贝效果有时候看起来一样，但主要区别在于浅拷贝会创建一个新对象，而引用赋值只是让两个变量指向同一个对象。
- `浅拷贝`：适用于简单对象，速度快，但对于复杂嵌套的对象，浅拷贝只能创建一个顶层的对象，对于内部子元素并没有复制。
- `深拷贝`：适用于复杂的嵌套对象，或者你需要完全独立的副本，确保修改新对象不会影响原对象的情况。深拷贝会递归复制所有嵌套对象，因此速度较慢。

    ```python
    import copy
    
    sub_obj = [1, 2, 3]
    a = {"k": sub_obj}
    
    # 引用赋值
    b = a
    
    # 浅拷贝
    c = copy.copy(a)
    
    # 深拷贝
    d = copy.deepcopy(a)
    
    # 查看对象的 id
    print(id(a))  # 输出: 4312154304
    print(id(b))  # 输出: 4312154304
    print(id(c))  # 输出: 4312571264
    print(id(d))  # 输出: 4313188608
    
    # 可以看到 b 和 a 指向的是同一个对象
    
    # 现在修改 a 的子元素看下变化
    a["k"][0] = 99
    print(a)  # 输出: {'k': [99, 2, 3]}
    print(b)  # 输出: {'k': [99, 2, 3]}
    print(c)  # 输出: {'k': [99, 2, 3]}
    print(d)  # 输出: {'k': [1, 2, 3]}
    ```

#### pb 对象的拷贝

对于 pb（Protocol Buffers）对象，建议使用 `Message.CopyFrom` 方法来拷贝对象，而不是使用 `copy.deepcopy`。在复制 proto 对象时，`Message.CopyFrom` 会更高效。

```python
from my_proto_module import MyProtoMessage

# 假设你已经定义了一个名为 my_proto 的 MyProtoMessage 对象
my_proto = MyProtoMessage()

# 使用 CopyFrom 方法复制 pb 对象
copied_proto = MyProtoMessage()
copied_proto.CopyFrom(my_proto)
```

**常见的 proto 对象复制场景:**

- **并发**：多线程环境中复制 proto 对象避免并发修改，复制 proto 对象可以确保每个线程都有自己的对象副本。
- **函数参数传递**：将 proto 对象作为函数参数传递，为了避免修改原始对象，可以传递对象的副本。

### 字节与字符串（bytes & str）

在 Python 3 中，`bytes` 和 `str` 是两个不同的类型，分别用于处理字节序列和字符串。

`str` 类型表示 Unicode 字符串，用于处理文本数据。
`str` 对象中的每个字符都是一个 Unicode 字符。

`bytes` 类型表示不可变的字节序列，主要用于处理二进制数据。

字符串需要编码（encode）成字节才能传输或存储。
字节需要解码（decode）成字符串才能处理。
编解码需要成对出现，不能用一种字符编码编码，再用另一种字符编码解码。

```python
# 创建一个字符串
text = "Hello, 世界"

# 打印字符串及其类型
print(text)  # 输出: Hello, 世界
print(type(text))  # 输出: <class 'str'>

# 获取字符串的长度
print(len(text))  # 输出: 9 (注意：中文字也只占一个字符)

# 使用 UTF-8 编码将字符串转换为字节序列
utf8_data = text.encode("utf-8")

print(utf8_data)  # 输出: b'Hello, \xe4\xb8\x96\xe7\x95\x8c'
print(type(utf8_data))  # 输出: <class 'bytes'>

_text = utf8_data.decode("utf-8")

print(_text)  # 输出: Hello, 世界
print(type(_text))  # 输出: <class 'str'>

# 使用 GBK 编码将字符串转换为字节序列
gbk_data = text.encode("gbk")

print(gbk_data)  # 输出: b'Hello, \xca\xc0\xbd\xe7'
print(type(gbk_data))  # 输出: <class 'bytes'>

_text = gbk_data.decode("gbk")

print(_text)  # 输出: Hello, 世界
print(type(_text))  # 输出: <class 'str'>
```

### 序列切片（slicing）

序列切片（Slicing）是一种强大而灵活的操作，
可以从各种序列（如字符串、列表、元组等）中提取子序列。
Python 的切片操作借助三个变量 `[start:stop:step]`，就可以实现丰富的切片语义。深入理解这些语义，可以帮助开发者写出更优雅的代码。

和列表推导类似，切片不可滥用，过度嵌套会导致理解困难。

不建议同时使用 step 与 start、stop，防止出现预期外结果。如必须使用，建议先切片赋值，在对赋值实现step。

在一些复杂数据结构中，善用自定义切片类型，可以让代码更具表达力。

```python
# Bad
text = "Hello, World!"

# 嵌套切片
result = text[1:][2:][::-1][:5]
print(result)  # 输出: '!dlro'

# 过度使用负索引
numbers = list(range(10))

subset = numbers[-8:-3]
print(subset)  # [2, 3, 4, 5, 6]

# 不必要的切片
first_five = numbers[:5][:]
print(first_five)

# 修改不可变序列
text = "Hello, World!"

# 尝试修改字符串
try:
    text[7:12] = "Python"
except TypeError as e:
    print(e)

# Good
# 简单清晰的切片
text = "Hello, World!"

# 提取 "Hello"
hello = text[:5]
print(hello)  # 输出: Hello

# 提取 "World"
world = text[7:12]
print(world)  # 输出: World

# 使用步长
numbers = list(range(10))

# 每隔一个元素取一次
evens = numbers[::2]
print(evens)  # 输出: [0, 2, 4, 6, 8]

# 反向取值
reversed_numbers = numbers[::-1]
print(reversed_numbers)  # 输出: [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

# 切片赋值
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# 替换部分列表
numbers[2:5] = [20, 30, 40]
print(numbers)  # 输出: [0, 1, 20, 30, 40, 5, 6, 7, 8, 9]

# 插入新元素
numbers[5:5] = [50, 60]
print(numbers)  # 输出: [0, 1, 20, 30, 40, 50, 60, 5, 6, 7, 8, 9]
```

### 字符串格式化

Python 的字符串格式化有很多种，包括 `%`, `format`, `f-string`, `Template String` 以及更复杂的模版库。

对于简单的字符串，首推 `f-string`，简洁直观，适合大多数场景，但仅支持 `Python 3.6+`。这种方法可以解决 `%` 和 `format` 变量位置对齐的问题。

对于更复杂的、需要自定义的场景，可以使用模板字符串。

```python
name = "Alice"
age = 30

# 不推荐 百分号格式化，旧式字符串格式化，类似 C 语言
formatted_string_1 = "Name: %s, Age: %d" % (name, age)
print(formatted_string_1)

# 不太推荐 str.format() 方法，变量多时，很难对齐
formatted_string_2 = "Name: {}, Age: {}".format(name, age)
print(formatted_string_2)

# 不太推荐 str.format() 方法，变量多时，很难对齐
formatted_string = "My name is {0} and I am {1} years old.".format(name, age)
print(formatted_string)

# 不太推荐 str.format()，用法已经接近 f-string
formatted_string = "My name is {name} and I am {age} years old.".format(
    name=name, age=age
)
print(formatted_string)

# f-strings
formatted_string_3 = f"Name: {name}, Age: {age}"
print(formatted_string_3)

# 模板字符串
from string import Template

t = Template("Name: $name, Age: $age")
formatted_string_4 = t.substitute(name=name, age=age)
print(formatted_string_4)
```

### 分号使用

与其他语言不同，Python 无需在行尾添加分号 `;`。  
也不要使用分号将两个语句合并，即使可以这么做。

```python
# Bad
# 行尾不要加分号
a = 1
# 不要使用分号连接两个语句
# fmt: off
a = 2; b = 3
# fmt: on
```

### 错误信息

- 错误信息需要精确匹配错误条件。
- 错误提示信息需要和错误内容明确分割。
- 错误信息要便于搜索和过滤。

    ```python
    # Bad
    try:
        os.rmdir(workdir)
    except OSError:
        # 问题: 信息中存在错误的揣测，
        # 删除操作可能因为其他原因而失败，此时会误导调试人员。
        logging.warning('文件夹已被删除: %s', workdir)
    
    # Good
    try:
        os.rmdir(workdir)
    except OSError as error:
        logging.warning('无法删除这个文件夹 (原因: %r): %r', error, workdir)
    ```

### 数值精度

`Python` 对双精度浮点数默认提供 17 位数字的精度。

- 要求较小精度

    一般使用 `round()` 内置方法获取较小的精度。但此处注意，此函数并不是简单的四舍五入。在 *`.5`* 时取整，会选择最近的偶数（易错）。

    ```python
    round(2.5)  # 2
    round(3.5)  # 4
    ```

- 要求超过 17 位精度

    在使用更高精度的浮点计算时，使用 `decimal` 模块，配合 `getcontext` 使用

    ```python
    from decimal import *
    print(getcontext())
    """ 输出
    Context(prec=28, rounding=ROUND_HALF_EVEN, Emin=-999999, Emax=999999, capitals=1, clamp=0, flags=[], traps=[InvalidOperation, DivisionByZero, Overflow])
    """
    ```

### 字典解包与格式化

```python
data = {"name": "Alice", "age": 30}

# 使用字典解包和字符串格式化
formatted_string = "Name: {name}, Age: {age}".format(**data)
print(formatted_string)  # 输出: Name: Alice, Age: 30
```

### 善用 dataclass

`dataclass` 是 Python 3.7 引入的一个装饰器，用于简化创建数据类的过程。  
数据类主要用于存储数据，自动生成一些常见的特殊方法（如 `__init__`、`__repr__`、`__eq__` 等）。  
相比于传统方法手动定义这些方法，`dataclass` 提供了更简洁和高效的方式。

```python
# 传统方法
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"Person(name={self.name}, age={self.age})"

    def __eq__(self, other):
        if isinstance(other, Person):
            return self.name == other.name and self.age == other.age
        return False


# 使用
person1 = Person("Alice", 30)
person2 = Person("Bob", 25)

# 使用 dataclass
from dataclasses import dataclass


@dataclass
class Person:
    name: str
    age: int


# 使用
person1 = Person("Alice", 30)
person2 = Person("Bob", 25)

# 复杂场景
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Person:
    name: str
    age: int
    friends: List[str] = field(default_factory=list)
    nickname: Optional[str] = None


# 使用
person1 = Person("Alice", 30, friends=["Bob", "Charlie"])
person2 = Person("Alice", 30)
```

### 类型注解（typing）

`typing` 是 Python 标准库中的一个模块，用于支持类型提示（Type Hints）。  
类型提示是一种静态类型检查工具，帮助开发者在代码中明确变量、函数参数和返回值的类型，从而提高代码的可读性和可靠性。  
虽然 Python 是动态类型语言，但通过类型提示，可以在开发阶段检测潜在的类型错误。

**注意**，`typing` 本身并不会在运行时检查类型，它只是提供了一种在代码中添加类型信息的方式。  
可以尝试使用 `mypy`、`pyright` 等静态类型检查工具检测类型错误。

```python
# 变量注解
from typing import List, Dict

name: str = "Alice"
age: int = 30
scores: List[int] = [95, 88, 76]
person: Dict[str, int] = {"Alice": 30, "Bob": 25}


# 函数注解
def greet(name: str) -> str:
    return f"Hello, {name}"


def sum_numbers(numbers: List[int]) -> int:
    return sum(numbers)


# List 和 Dict 嵌套
from typing import List, Dict


def process_data(data: List[Dict[str, int]]) -> None:
    for item in data:
        for key, value in item.items():
            print(f"{key}: {value}")


data = [{"Alice": 30}, {"Bob": 25}]
process_data(data)

# Optional
from typing import Optional


def find_person(name: str) -> Optional[Dict[str, int]]:
    people = {"Alice": 30, "Bob": 25}
    return {name: people[name]} if name in people else None


result = find_person("Alice")
print(result)  # 输出: {'Alice': 30}

result = find_person("Charlie")
print(result)  # 输出: None

# Union
from typing import Union


def handle_input(data: Union[int, str]) -> str:
    if isinstance(data, int):
        return f"Received an integer: {data}"
    elif isinstance(data, str):
        return f"Received a string: {data}"


print(handle_input(42))  # 输出: Received an integer: 42
print(handle_input("hello"))  # 输出: Received a string: hello

# Any
from typing import Any


def process_value(value: Any) -> None:
    print(f"Processing value: {value}")


process_value(42)
process_value("hello")
process_value([1, 2, 3])
```

#### 同一个文件中循环引用注解

在 Python 项目中，初始化过程中可能出现循环引用，例如：

```python
class A:
    def __init__(self, b):
        self.__b = b


class B:
    def __init__(self, a: A):
        self.__a = a
```

虽说循环引用本身不应该存在，但是当项目比较复杂，有时候比较难以避免；而且一般初始时化过程中的循环引用，只会一次循环引用，所以也不会出现太多内存泄露。当出现这种情况的时候，可以采用以下方式做注释：

```python
class A:
    def __init__(self, b: "B"):
        self.__b = b
```

将 B 注释加上双引号，一般的 IDE 都会进行识别，这样就可以解决了

#### 跨文件中循环引用注解

当项目复杂的时候，多个模块依赖的模块可能存在依赖，例如：

```shell
project
├── main.py
├── pkg1
│   ├── __init__.py
│   ├── module_a.py
│   └── module_b.py
└── pkg2
    ├── __init__.py
    ├── module_c.py
    └── module_d.py
```

在 *module_a.py* 中存在以下代码：

```python
class A:
    def __init__(self, d):
        self.__d = d
```

在 *module_d.py* 中存在以下代码：

```python
class D:
    def __init__(self, a):
        self.__a = a
```

如果不使用 typing，项目可以正常运行，但是如果加上以下 typing 注释

- 错误使用

    ```python
    from pkg2 import module_d

    class A:
        def __init__(self, d: D):
            self.__d = d

    ```

    必然会报循环引用错误，遇到这种问题可以采用

- 正确使用

    ```python
    import typing
    
    if typing.TYPE_CHECKING:  # 运行时不导入
        # For type annotation
        from pkg2 import module_d
    
    class A:
        def __init__(self, d: "D"):
            self.__d = d
    
    ```

    采用这种方式即可解决注释引起的循环引用错误

#### 函数注解

在 Python 项目中，通常会出现回调函数做参数，为了是代码可读，在注释回调函数可以采用以下方式

```python
from typing import Callable

# 自定义类型名称 CallBack
CallBack = Callable[[int], str]

def feeder(get_next_item: CallBack) -> None:
    # Body
    s1 : str = get_next_item(1)
    print(s1)

```

这里的 *CallBack* 是用户自定义类型，通过 typing，阅读可以很便利；  
在 Callable 中分为两部分，第一个中是入参，属于 list（其中的[int]），说明参数可以是多个；  
第二个中是返回值类型是单个，例如上面的 `str`

#### 生成器注解

生成器是 Python 中比较常用的特性，在注释的时候可以采用以下方式：

```python
from typing import Generator


def echo_round() -> Generator[int, float, str]:
    sent = yield 0
    while sent >= 0:
        sent = yield round(sent)
    return "Done"
```

其中 `Generator[YieldType, SendType, ReturnType]` 表示生成器中的三种类型，例子如下：

```python
generator = echo_round()

# 获取 YieldType 的类型，输出 0，属于 int 类型，就是 YieldType
print(next(generator))  # 输出: 0

# 传入 SendType 类型如下，其中 10.0 属于 float 类型，就是 SendType
print(f"res: {generator.send(10.0)}")  # 输出: 10

# 获取 ReturnType 的类型，输出 'Done'，属于 str 类型，就是 ReturnType
try:
    while True:
        value = generator.send(-10.0)
        print(value)
except StopIteration as e:
    result = e.value
    print("Return value:", result)
```

Python3 引入的 `async/await` 协程；当协程函数中出现生成器，注释如下：

```python
from typing import AsyncGenerator


async def echo_round() -> AsyncGenerator[int, float]:
    sent = yield 0
    while sent >= 0.0:
        rounded = await round(sent)
        sent = yield rounded
```

其中注释类型 `AsyncGenerator[YieldType, SendType]`，由于这里没有 *return*，自然没有 *ReturnType*

#### 协程注解

协程是 Python 的一个比较重要的特性，在注释中需要注释，这里给出一个协程注释的例子：

```python
from typing import Coroutine
import asyncio


async def my_coroutine(x: int) -> Coroutine[int, float, str]:
    # x 属于输入类型，是 int 类型
    print(f"Received: {x}")
    # y 是异步返回数据 float 类型
    y = await compute(x)  # 假设这是一个异步操作
    return str(y)


async def compute(x: int) -> float:
    return float(x) / 2  # 这里只是一个简单的计算，实际情况可能会涉及到I/O操作


# 创建一个事件循环
loop = asyncio.get_event_loop()

# 运行协程并获取结果，result 是返回类型 str
result = loop.run_until_complete(my_coroutine(10))
print(f"Result: {result}")
```

`Coroutine[int, float, str]` 是一种类型注解，表示一个协程，它接受一个`int`类型的参数，返回一个`float`类型的结果，最后返回一个`str`类型的结果

### 关于 `__future__`

`__future__` 模块允许开发者在当前 Python 版本中使用未来版本中的新特性。  
通过导入 `__future__` 模块中的特性，可以确保代码在未来版本的 Python 中正常工作。

在代码审查过程中，常发现 Python 3 代码里依然引用了一些特性：

```python
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
```

在 Python 3 中，上述特性已经默认启用，因此在 Python 3 代码中显式引入这些 `__future__` 特性是没有必要的。

### 字面量

字面量（Literal）是指在代码中直接使用的固定值。  
字面量是最简单的表达式类型，表示固定的值而不需要计算。  
Python 支持多种类型的字面量，包括数字、字符串、布尔值、集合类型等。

```python
# 数字字面量
decimal = 42  # 十进制
binary = 0b101010  # 二进制
octal = 0o52  # 八进制
hexadecimal = 0x2A  # 十六进制

float_num = 3.14  # 小数点表示法
scientific = 1.23e4  # 科学计数法

# 字符串字面量
single_quote = "Hello, World!"
double_quote = "Hello, World!"
triple_single_quote = """Hello,
World!"""
triple_double_quote = """Hello,
World!"""

raw_string = r"C:\Users\Alice"

# 布尔值字面量
is_true = True
is_false = False
no_value = None

# 集合类型字面量
list_literal = [1, 2, 3, 4, 5]
tuple_literal = (1, 2, 3, 4, 5)
set_literal = {1, 2, 3, 4, 5}
dict_literal = {"name": "Alice", "age": 30}

# f字符串字面量
name = "Alice"
age = 30
greeting = f"Hello, {name}! You are {age} years old."

# Unicode 字符串
string = "Hello, 世界"  # 默认是 Unicode 字符串
print(type(string))  # <class 'str'>

# \uXXXX 表示一个 16 位的 Unicode 字符，其中 XXXX 是四位十六进制数。
unicode_str = "\u4e16\u754c"  # 表示 "世界"
print(unicode_str)  # 输出: 世界

# \UXXXXXXXX 表示一个 32 位的 Unicode 字符，其中 XXXXXXXX 是八位十六进制数。
unicode_str = "\U0001F600"  # 表示 😀 (U+1F600)
print(unicode_str)  # 输出: 😀

# 十六进制表示字符串
hex_str = "\x48\x65\x6c\x6c\x6f"  # 表示 "Hello"
print(hex_str)  # 输出: Hello

# Unicode 名称表示
unicode_name_str = "\N{GREEK CAPITAL LETTER DELTA}"
print(unicode_name_str)  # 输出: Δ

# 常见转义字符
"""
\\：反斜杠
\'：单引号
\"：双引号
\n：换行符
\t：制表符
\r：回车符
\b：退格符
\f：换页符
\a：响铃
\v：纵向制表符
"""

escape_str = "Line1\nLine2\tTabbed\rCarriage\bBackspace"
print(escape_str)
```

### JSON 字符串处理

Python 内置了 `json` 库，用于处理 JSON 数据。  
在输出序列化字符串时，如果包含中文字符，默认会以 Unicode 转义形式显示。  
可以通过参数设置使其以正常的中文字符显示。

```python
import json

data = {"name": "Alice", "age": 30, "message": "你好，世界"}

# 默认情况下，中文会被转义为 Unicode
json_str = json.dumps(data)
# fmt: off
print(json_str)  # 输出: {"name": "Alice", "age": 30, "message": "\u4f60\u597d\uff0c\u4e16\u754c"}
# fmt: on

# 使用 ensure_ascii=False 参数，中文将正常显示
json_str = json.dumps(data, ensure_ascii=False)
print(json_str)  # 输出: {"name": "Alice", "age": 30, "message": "你好，世界"}

# 反序列化 JSON 字符串
parsed_data = json.loads(json_str)
print(parsed_data)  # 输出: {'name': 'Alice', 'age': 30, 'message': '你好，世界'}
```

### 避免浮点数直接比较

避免浮点数直接比较，这里面会有精度问题，正确的做法是比较两个数的差的绝对值。

```python
# 使用库
import math

a = 0.1 + 0.2
b = 0.3

# 使用 math.isclose 比较浮点数
if math.isclose(a, b, rel_tol=1e-9):
    print("a and b are close enough")
else:
    print("a and b are not close enough")

# 手动
a = 0.1 + 0.2
b = 0.3
epsilon = 1e-9

# 手动比较浮点数
if abs(a * b) < epsilon:
    print("a and b are close enough")
else:
    print("a and b are not close enough")
```

## 惯用法

### 使用 with 语句管理资源

Python 中 `with` 语句通常用于管理资源，尤其是涉及资源申请释放的逻辑。  
`with` 本质上是上下文管理器（Context Manager）语法糖，使开发者能够更优雅且显式地管理资源。  
多用于文件、数据库、线程锁、套接字等。

如果持续未释放这些资源，可能导致：

- 耗尽系统资源，比如文件句柄
- 保持文件开启状态，会导致其他操作无法执行，比如移动、删除等

```python
# Bad, 文件句柄有可能泄露

try:
    f = open("file.json", "r")
    # 其他操作
    json.load(f)
    # 关闭
    f.close()
except json.JSONDecodeError as err:  # 捕获特定的 JSON 解码错误
    print(f"JSON 解码错误: {err}")
except OSError as os_err:  # 捕获操作系统错误，比如文件无法打开
    print(f"操作系统错误: {os_err}")

# Good
# 这种情况下，上下文管理器可以确保文件句柄的释放
# 即使在 json.load(f) 处抛出异常，文件句柄也会被正确关闭
with open("file.json", "r") as f:
    json.load(f)
    # 其他操作
with open("file.json", "r") as f:
    json.load(f)
    # 其他操作
```

借助 `contextlib` 中的 `contextmanager`，可以很容易地构造出一个可用于 `with` 的函数。下面的代码展示了如何通过 `contextmanager` 编写一个计时函数：

```python
import logging

from contextlib import contextmanager
from datetime import datetime


@contextmanager
def timeit():
    """显示代码片段运行时间"""
    now = datetime.now()
    yield
    logging.info(f"Time Cost: {(datetime.now() - now).total_seconds()}s")


with timeit(), open("file.json", "r") as f:
    json.load(f)
```

借助`contextlib`提供的`asynccontextmanager`，可以构造一个可用于`async with`的异步上下文管理器。
下面的代码模拟了如何通过`asynccontextmanager`构建一个用于数据库连接和操作的异步上下文管理器，并且通过`async with`使用它：

```python
import asyncio
from contextlib import asynccontextmanager

class MockDatabaseConnection:
    async def connect(self):
        print("Connecting to database...")
        await asyncio.sleep(1)  # 模拟连接延迟

    async def close(self):
        print("Closing database connection...")
        await asyncio.sleep(1)  # 模拟关闭延迟

@asynccontextmanager
async def database_connection():
    connection = MockDatabaseConnection()
    await connection.connect()
    try:
        yield connection
    finally:
        await connection.close()

async def main():
    async with database_connection() as db:
        print("Performing database operations...")
        await asyncio.sleep(1)  # 模拟数据库操作

# 运行异步主函数
asyncio.run(main())
```

### 优先使用标准库方法

Python 遵循 `每件事都应该有一种直白、明显的方法来完成，而且最好只有一种方法。` 哲学。  
Python 标准库号称内置电池，所以应该优先使用标准库内置方法。

```python
# Bad
# 尝试使用字符串拼接方式拼接路径
# 这种方式既不优雅，也不具备通用性，在跨平台时，会有兼容性问题
file_path = "/data" + "/test" + "/a.txt"
file_path = f"/data/{dir_name}/a.txt"

# Good
# 使用 os.path.join 进行路径拼接
import os

file_path = os.path.join("/data", "test", "a.txt")
print(file_path)

# Better
# 使用 pathlib 模块进行路径拼接，更加面向对象，跨平台兼容性更好
from pathlib import Path

file_path = Path("/data") / "test" / "a.txt"
print(file_path)
```

### 文件存在判断

```python
# Bad
is_exist = None
file_path = "/data/demo.txt"
try:
    f = open(file_path, "r")
    is_exist = True
    f.close()
except Exception as err:
    is_exist = False

# Good
# 使用 os.path.exists 进行文件存在判断
import os

file_path = "/data/demo.txt"
is_exist = os.path.exists(file_path)
print(is_exist)

# Better
# 使用 pathlib 模块进行文件存在判断，更加面向对象
from pathlib import Path

file_path = Path("/data/demo.txt")
is_exist = file_path.exists()
print(is_exist)
```

### 使用 enumerate 代替手动维护索引

```python
# Bad
index = 0
items = ["apple", "banana", "cherry"]
for item in items:
    print(index, item)
    index += 1

# Good 使用 enumerate 代替手动维护索引
items = ["apple", "banana", "cherry"]
for index, item in enumerate(items):
    print(index, item)
```

### 使用 zip 代替手动并行迭代

```python
# Bad
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]
for i in range(len(names)):
    print(names[i], ages[i])

# Good 使用 zip 并行迭代
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]
for name, age in zip(names, ages):
    print(name, age)
```

### 使用 `collections.defaultdict` 代替手动检查键是否存在

```python
# Bad
counts = {}
words = ["apple", "banana", "apple"]
for word in words:
    if word in counts:
        counts[word] += 1
    else:
        counts[word] = 1
print(counts)

# Good 使用 collections.defaultdict
from collections import defaultdict

counts = defaultdict(int)
words = ["apple", "banana", "apple"]
for word in words:
    counts[word] += 1
print(dict(counts))
```

### 使用 `namedtuple` 代替普通元组

```python
# Bad
person = ("Alice", 30, "Engineer")
print(person[0])  # 不直观，不易读

# Good 使用 namedtuple
from collections import namedtuple

Person = namedtuple("Person", ["name", "age", "job"])
person = Person(name="Alice", age=30, job="Engineer")
print(person.name)
```

### 使用 `json` 模块代替 `eval` 进行字符串解析

```python
# Bad 使用 eval 解析字符串（存在安全风险）
data_str = '{"name": "Alice", "age": 30}'
data = eval(data_str)

# Good 使用 json 模块解析字符串
import json

data_str = '{"name": "Alice", "age": 30}'
data = json.loads(data_str)
```

### 避免 `set` 进行数据操作（机器学习）

在机器学习领域中，如果要进行数据操作（如筛选，合并），应避免使用 `set` 来直接进行 `|` 和 `&` 操作，这是因为 `set` 无法保证数据顺序，会对实验的可复现性造成影响

```python
data = [1, 2, 3, 4, 5]
legal_data = [2, 4, 6]

# Bad 使用 & 来进行数据筛选
train_data = set(data) & set(legal_data)

# Good 使用列表遍历或者使用sorted保证数据一致性
train_data = [elem for elem in data if elem in set(legal_data)]
train_data = sorted(set(data) & set(legal_data))
```

### 避免过时用法

语言一直在发展演进，建议使用社区推荐的用法。

```python
# f-string 方便又好用
name = "Alice"
greeting = f"Hello, {name}!"

# 列表推导
squares = [x**2 for x in range(10)]

# 生成器表达式
squares_gen = (x**2 for x in range(10))

# enumerate
for index, value in enumerate(some_list):
    print(index, value)

# zip 合并序列
for item1, item2 in zip(list1, list2):
    print(item1, item2)

# with 打开文件
with open("example.txt", "r") as file:
    data = file.read()

# 字典推导
squares = {x: x**2 for x in range(10)}

# any 和 all
found = any(elem > 10 for elem in some_list)
check = all(elem > 10 for elem in some_list)

# 路径库 - 传统
import os

path = os.path.join("folder", "subfolder", "file.txt")

# 路径库 - pathlib
from pathlib import Path

path = Path("folder") / "subfolder" / "file.txt"

# 遍历目录 性能更好
directory = Path("some_directory")
for file_path in directory.rglob("*"):
    if file_path.is_file():
        print(file_path)
```

### 列表去重

```python
# python版本>=3.7，保持列表原有顺序
res = list(dict.fromkeys(ori))

# 不保持列表原有顺序
res = list(set(ori))
```

## 性能优化

### 循环中避免字符串拼接

在循环里执行字符串拼接是非常低效的，因为每次拼接操作都会创建一个新的字符串对象，导致大量的内存分配和数据复制。  
相反，使用 `str.join` 方法可以显著提高效率，因为它会预先计算出最终字符串的长度，然后一次性分配内存。

```python
# Bad
# 1. 每次循环都会创建新的字符串对象，效率低下。
# 2. 随着字符串长度增大，性能下降会更加明显。
str_list = ["a", "b", "c"]
result_str = ""
for s in str_list:
    result_str += s
print(result_str)  # Output: "abc"

# Good 使用 str.join 方法来拼接字符串
# 1. 预先计算最终字符串长度，一次性分配内存。
# 2. 性能更高，特别是在处理大列表时。
str_list = ["a", "b", "c"]
result_str = "".join(str_list)
print(result_str)  # Output: "abc"
```

### 使用列表推导式代替循环添加元素

```python
# Bad
squares = []
for x in range(10):
    squares.append(x**2)

# Good 使用列表推导式
squares = [x**2 for x in range(10)]
```

### 使用生成器代替列表（适用于大数据）

```python
# Bad 使用列表会占用大量内存
squares = [x**2 for x in range(1000000)]

# Good 使用生成器节省内存
squares = (x**2 for x in range(1000000))
```

### 使用集合（set）代替列表进行成员检测

```python
# Bad 使用列表进行成员检测
items = [1, 2, 3, 4, 5]
if 3 in items:
    print("Found")

# Good 使用集合进行成员检测
items = {1, 2, 3, 4, 5}
if 3 in items:
    print("Found")
```

### 减少不必要的属性访问

```python
# Bad
class MyClass:
    def __init__(self):
        self.value = 10


my_obj = MyClass()
result = 0
for _ in range(1000000):
    result += my_obj.value  # 每次都进行属性访问


# Good
class MyClass:
    def __init__(self):
        self.value = 10


my_obj = MyClass()
result = 0
value = my_obj.value  # 将属性值缓存到局部变量
for _ in range(1000000):
    result += value
```

## 数据结构与算法

### `collections` 模块

`collections` 模块提供了一些额外的数据结构，这些数据结构在某些情况下比内置的数据类型（如列表、字典、元组和集合）更适合使用。

```python
# namedtuple
from collections import namedtuple

# 创建一个名为 'Point' 的 namedtuple，包含 'x' 和 'y' 两个字段
Point = namedtuple("Point", ["x", "y"])

# 创建一个 Point 实例
p = Point(10, 20)

# 访问字段
print(p.x)  # 输出: 10
print(p.y)  # 输出: 20

# namedtuple 也支持索引访问
print(p[0])  # 输出: 10
print(p[1])  # 输出: 20
```

```python
# 双端队列
from collections import deque

# 创建一个空的 deque
d = deque()

# 添加元素
d.append(1)  # 在右端添加
d.appendleft(2)  # 在左端添加

print(d)  # 输出: deque([2, 1])

# 删除元素
d.pop()  # 从右端删除
d.popleft()  # 从左端删除

print(d)  # 输出: deque([])
```

```python
# 有序字典
from collections import OrderedDict

# 创建一个 OrderedDict
od = OrderedDict()

# 插入元素
od["a"] = 1
od["b"] = 2
od["c"] = 3

print(od)  # 输出: OrderedDict([('a', 1), ('b', 2), ('c', 3)])
```

### 排序

Python 提供了多种方法来对序列进行排序，主要包括内置的 `sorted` 函数和列表对象的 `sort` 方法。

- `sorted` 函数

    `sorted` 函数可以对任何可迭代对象进行排序，并返回一个新的排序后的列表。该函数不会修改原始的序列。

```python
# 对列表进行排序
numbers = [5, 2, 9, 1, 5, 6]
sorted_numbers = sorted(numbers)
print(sorted_numbers)  # 输出: [1, 2, 5, 5, 6, 9]

# 对字符串进行排序
string = "python"
sorted_string = sorted(string)
print(sorted_string)  # 输出: ['h', 'n', 'o', 'p', 't', 'y']

# 使用 key 参数按字符串长度排序
words = ["apple", "banana", "cherry", "date"]
sorted_words = sorted(words, key=len)
print(sorted_words)  # 输出: ['date', 'apple', 'banana', 'cherry']

# 降序排序
sorted_numbers_desc = sorted(numbers, reverse=True)
print(sorted_numbers_desc)  # 输出: [9, 6, 5, 5, 2, 1]

# 对字典列表按年龄排序
data = [
    {"name": "Alice", "age": 25, "height": 165},
    {"name": "Bob", "age": 30, "height": 175},
    {"name": "Charlie", "age": 20, "height": 168},
    {"name": "David", "age": 25, "height": 180},
]

sorted_by_age = sorted(data, key=lambda x: x["age"])
print(sorted_by_age)
```

- `sort` 方法

    sort 方法是列表对象的一个方法，用于对列表进行原地排序，即修改原始的列表并不返回新的列表。

```python
# 对列表进行原地排序
numbers = [5, 2, 9, 1, 5, 6]
numbers.sort()
print(numbers)  # 输出: [1, 2, 5, 5, 6, 9]

# 使用 key 参数按字符串长度排序
words = ["apple", "banana", "cherry", "date"]
words.sort(key=len)
print(words)  # 输出: ['date', 'apple', 'banana', 'cherry']

# 降序排序
numbers.sort(reverse=True)
print(numbers)  # 输出: [9, 6, 5, 5, 2, 1]
```

### 二分查找

`bisect`库中提供了有序列表的二分查找、插入等相关操作。

```python
import bisect

# 有序列表
nums = [1, 2, 3, 4, 4, 5]
target = 4
# 使用bisect_left查找元素4应该插入的最左位置
index = bisect.bisect_left(nums, target)
print(index)  # 输出：3

new_num = 3
# 使用insort将新元素插入列表并保持有序
bisect.insort(nums, new_num)
```

### 拓扑排序

python内置了`graphlib`库用于图相关操作，比如拓扑排序：

```python
from graphlib import TopologicalSorter

graph = {"D": {"B", "C"}, "C": {"A"}, "B": {"A"}}
ts = TopologicalSorter(graph)
print(tuple(ts.static_order()))  # 输出：('A', 'C', 'B', 'D')
```

### 堆

python内置的`heapq`库提供了堆相关操作

```python
import heapq

# 原始列表
data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]

# 将列表转换为堆。默认是最小堆。如果需要最大堆，可以把每个值取负数，然后最终返回结果的时候再取反
heapq.heapify(data)

# 弹出并返回堆中的最小元素
smallest = heapq.heappop(data)
print(smallest)  # 输出：1

smallest_three = heapq.nsmallest(3, data)
print(smallest_three)  # 输出：[1, 2, 3]
```

## 面向对象与元编程

### 方法解析顺序（MRO）

类继承的 MRO（Method Resolution Order，方法解析顺序）决定了在多重继承时，属性和方法的搜索顺序。  
Python 使用 C3 线性化算法（也称为 C3 线性化继承顺序）来计算 MRO，这确保了继承关系是单调的且具有一致性。

- C3 线性化算法确保了以下几点：  
一致性：继承关系在整个继承链上是连续且一致的。  
单调性：子类的 MRO 不会改变父类的 MRO 顺序。  

- 使用 MRO 的场景  
多重继承：在多重继承中，MRO 确保了方法和属性查找的顺序是明确且可预测的。  
调试和优化：查看 MRO 可以帮助理解类的继承关系，调试多重继承中的问题。  
设计类层次结构：在设计复杂的类层次结构时，了解 MRO 有助于避免潜在的继承冲突。  

```python
class A:
    def method(self):
        print("A.method")


class B(A):
    def method(self):
        print("B.method")


class C(A):
    def method(self):
        print("C.method")


class D(B, C):
    pass


d = D()
d.method()

print(D.mro())
# 输出: [<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <class 'object'>]
```

### 私有属性

`Python` 对类的成员没有严格的访问控制，通常约定以两个下划线开头的属性/方法是私有的（Private）。

- 定义私有属性/方法

可以通过 `dir()` 函数查看对象内的所有属性和方法。

```python
class Pythoner:
    __language = "Python"

    def __init__(self, username, age):
        self.username = username
        self.__age = age

    def __private_method(self):
        print("这是私有方法")

    def public_method(self):
        print("这是共有方法")


p = Pythoner("test", 18)
dir(p)
"""
['_Pythoner__age', '_Pythoner__language', '_Pythoner__private_method', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'public_method', 'username']
"""
```

注：方法本质上也可以认为是属性，只不过可以通过 () 执行。

- 不要定义混淆类方法名称

    如上可发现，`Python` 解释器对类的私有属性进行了名称混淆，因此不要在类中定义同名方法。

```python
class Pythoner:
    __language = "Python"

    def __init__(self, username, age):
        self.username = username
        self.__age = age

    def __private_method(self):
        print("这是私有方法")

    def public_method(self):
        print("这是共有方法")
        self.__private_method()

    def _Pythoner__private_method(self):
        print("混淆 private_method 方法")


p = Pythoner("test", 18)
p.public_method()
"""输出
这是共有方法
混淆 private_method 方法
"""
```

可以发现，上述中的私有方法 `__private_method()` 被替换掉了，因此非常不建议此种代码实现。

### Getter、Setter 和 Property

在访问和设置变量时，如果当前或可预见的未来，读写某个变量的过程很复杂或者成本高昂，则可以使用 `getter` 和 `setter` 方法。
例如，如果 `setter` 操作会让部分状态无效化或引发重建，建议通过显式的函数调用来表明可能出现的特殊操作。

一般而言，简单逻辑使用 `property` 替代 `getter` `setter`。

```python
class Example:
    def __init__(self, value):
        self._value = value
        self._cache = None

    @property
    def value(self):
        if self._cache is None:
            # 假设这是一个高昂的计算操作
            self._cache = self._value * 2
        return self._cache

    @value.setter
    def value(self, new_value):
        self._value = new_value
        self._cache = None  # 重置缓存


example = Example(10)
print(example.value)  # 输出: 20
example.value = 20
print(example.value)  # 输出: 40
```

### 函数式编程

函数式编程是一种编程范式，强调使用纯函数和不可变数据来编写代码。  
在 Python 中，虽然不是纯粹的函数式编程语言，但它提供了许多函数式编程的特性和工具。  
函数式编程在 Python 中可以提高代码的可读性、可测试性和可维护性。  
通过使用纯函数、不可变数据、高阶函数、递归和 `functools` 模块，可以有效地应用函数式编程的思想来编写高质量的 Python 代码。

1. 使用纯函数

- 纯函数是指相同输入总是产生相同输出，且没有任何副作用的函数。
- 保持函数纯净可以提高代码的可测试性和可预测性。

    ```python
    # 纯函数示例
    def add(x, y):
        return x + y
    
    # 调用函数
    result = add(1, 2)
    print(result)  # 输出: 3
    ```

1. 避免可变数据

- 在函数式编程中，尽量使用不可变的数据结构，如元组、冻结集合等。
- 避免在函数中修改全局变量或传入的可变对象。

    ```python
    # 使用不可变数据结构
    immutable_tuple = (1, 2, 3)
    
    # 尽量使用不可变的数据，避免副作用
    def add_to_tuple(tup, value):
        return tup + (value,)
    
    new_tuple = add_to_tuple(immutable_tuple, 4)
    print(new_tuple)  # 输出: (1, 2, 3, 4)
    ```

1. 高阶函数

- 高阶函数是指可以接受其他函数作为参数或返回函数的函数。
- 常用的高阶函数包括 `map`、`filter` 和 `reduce`。

    ```python
    # 高阶函数示例
    from functools import reduce
    
    # 使用 map
    squares = list(map(lambda x: x * x, [1, 2, 3, 4]))
    print(squares)  # 输出: [1, 4, 9, 16]
    
    # 使用 filter
    numbers = [1, 2, 3, 4]
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    print(evens)  # 输出: [2, 4]
    first_even = next(filter(lambda x: x % 2 == 0, numbers), None)  # filter 和 next 搭配使用，获取第一个偶数
    print(first_even)  # 输出: 2
    
    # 使用 reduce
    sum_result = reduce(lambda x, y: x + y, [1, 2, 3, 4])
    print(sum_result)  # 输出: 10
    ```

1. 递归

- 函数式编程中，递归是常用的迭代方式。
- 在 Python 中，注意递归深度的问题，可能需要优化或使用尾递归等技术。

    ```python
    # 递归函数示例
    def factorial(n):
        if n == 0:
            return 1
        else:
            return n * factorial(n - 1)
    
    print(factorial(5))  # 输出: 120
    ```

1. 使用 `functools` 模块

- `functools` 提供了一些实用工具，可以帮助实现函数式编程，如 `lru_cache`、`partial` 等。

    ```python
    # 使用 functools 模块
    from functools import lru_cache, cache, partial
    
    # 使用 lru_cache 进行缓存
    @lru_cache(maxsize=None)
    def fibonacci(n):
        if n < 2:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)
    
    print(fibonacci(10))  # 输出: 55
    fibonacci.cache_clear()  # 使用cache_clear清除缓存

    # 使用 cache 进行缓存。与lru_cache的区别在于，cache没有容量限制。cache内部实际上也是去调用lru_cache
    @cache
    def fibonacci_new(n):
        if n < 2:
            return n
        return fibonacci_new(n - 1) + fibonacci_new(n - 2)

    print(fibonacci_new(10))  # 输出: 55
    fibonacci_new.cache_clear()  # 同样也可使用cache_clear清除缓存
    
    # 使用 partial 创建部分应用函数
    def multiply(x, y):
        return x * y
    
    double = partial(multiply, 2)
    print(double(5))  # 输出: 10
    ```

### 装饰器

#### 装饰器适用场景

出于**复用、解耦、简化代码**的目的，会在代码中使用装饰器。常见的的使用场景如下：

- 针对特定方法，附加额外的业务逻辑
  - 记录日志
  - 注册路由
  - 验证权限
  - 拦截代理方法
  - 设置缓存
- 针对类
  - 单例模式
  - 填充属性
  - 缓存计算结果

示例如下：

```python
# 1.1 记录日志
def log_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

# 1.2 注册路由、插件，常见于 FastAPI, Flask 等 Python 框架以及公司内的 tRPC-Python 等微服务框架，此处不再赘述

# 1.3 权限验证
def permission_required(permission):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(user, *args, **kwargs):
            if not user.has_permission(permission):
                raise PermissionError("Permission denied")
            return func(user, *args, **kwargs)
        return wrapper
    return decorator

# 1.4 拦截代理，和记录日志类似，例如在特定条件下执行其他逻辑而不执行被装饰的函数，不再赘述

# 1.5 设置缓存，可参考 `functools.lru_cache`
```

#### 注意事项

1. 避免丢失被装饰的函数的元数据，可以使用 `functools` 包中的 `wraps` 方法
2. 装饰器的执行顺序，先执行的是靠近被装饰的函数的装饰器，即自下而上的执行顺序
3. 闭包中的变量捕获可能导致意外的行为，特别是在多次调用装饰器时。需要避免在装饰器内使用可变的全局变量，如有必要考虑使用参数传入
4. 由于装饰器调试困难，可以编写针对装饰器的单元测试函数，充分验证其行为后，再批量使用

示例如下：

```python
import functools


# 1. 保留被装饰函数的元数据
def decorator_function(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Executing {func.__name__}")
        return func(*args, **kwargs)

    return wrapper


# 2. 装饰器顺序
@decorator1
@decorator2
def some_function():
    pass


# 等价于
some_function = decorator1(decorator2(some_function))


# 3. 闭包中变量捕获导致意外共享
# 3.1 反例, 所有装饰器都共用一个 `count` 变量
def call_counter(func):
    count = 0  # 这个变量会被所有使用此装饰器的函数共享！

    def wrapper(*args, **kwargs):
        nonlocal count
        count += 1
        print(f"{func.__name__} has been called {count} times.")
        return func(*args, **kwargs)

    return wrapper


@call_counter
def my_function():
    pass


@call_counter
def another_function():
    pass


# 3.2 正例，为每个被装饰的函数，追加一个属性，避免 `count` 共享
def call_counter(func):
    def wrapper(*args, **kwargs):
        wrapper.count += 1  # 将count变为wrapper的一个属性
        print(f"{func.__name__} has been called {wrapper.count} times.")
        return func(*args, **kwargs)

    wrapper.count = 0  # 初始化count属性
    return wrapper


# 4. 为装饰器编写单元测试
# 4.1 装饰器
def log_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}...")
        result = func(*args, **kwargs)
        print(f"{func.__name__} finished.")
        return result

    return wrapper


# 4.2 单元测试
import unittest
from io import StringIO
from contextlib import redirect_stdout
from functools import wraps


class TestLogDecorator(unittest.TestCase):
    def test_log_decorator(self):
        @log_decorator
        def test_function():
            return "test result"

        # 使用 StringIO 和 redirect_stdout 来捕获打印输出
        f = StringIO()
        with redirect_stdout(f):
            result = test_function()

        # 断言函数返回值
        self.assertEqual(result, "test result")

        # 断言打印输出
        output = f.getvalue()
        self.assertIn("Calling test_function...", output)
        self.assertIn("test_function finished.", output)
```

### 闭包

#### 命名空间干净

为了保证命名空间的的干净，而将一些变量隐藏到函数内部作为局部变量，如果这时候想要外部代码能读取函数内部变量，就可以使用闭包，此处可以理解为轻量级接口封装。

如下给 `content` 加 `tag` 功能的例子，`tag_name` 是什么样子的根据实际需求决定，但对外接口是固定的。

```python
def tag(tag_name):
    def add_tag(content):
        return "<{0}>{1}</{0}>".format(tag_name, content)

    return add_tag


test_add_tag = tag("a")
content = "Hello"
print(test_add_tag(content))
# 输出：<a>Hello</a>

test_add_tag_2 = tag("b")
print(test_add_tag_2(content))
# 输出：<b>Hello</b>
```

#### 变量始终存在内存

一般来讲，函数内部的局部变量在函数运行完成，会被 `Python` 的垃圾回收机制从内存中清除，若我们希望局部变量可以长久保存在内存中，可以用闭包实现这个功能。
如下一个类棋盘游戏的例子，*`player`* 实际上就是闭包函数 *`go`* 中的一个实例对象。

```python
def create(pos=None):
    if pos is None:
        pos = [0, 0]

    def go(direction, step):
        new_x = pos[0] + direction[0] * step
        new_y = pos[1] + direction[1] * step

        pos[0] = new_x
        pos[1] = new_y

        return pos

    return go


player = create()
print(player([1, 0], 10))
print(player([0, 1], 20))
print(player([-1, 0], 10))
```

更进一步，`python` 中带参数的装饰器一般都会生成闭包（类装饰器除外）。

```python
def html_tags(tag_name):
    def wrapper_(func):
        def wrapper(*args, **kwargs):
            content = func(*args, **kwargs)
            return "<{tag}>{content}</{tag}>".format(tag=tag_name, content=content)

        return wrapper

    return wrapper_


@html_tags("b")
def hello(name="Toby"):
    return "Hello {}!".format(name)


print(hello())
# 输出：<b>Hello Toby!</b>
print(hello("world"))
# 输出：<b>Hello world!</b>


# 不用装饰器
def hello_no_decorator(name="Toby"):
    return "Hello {}!".format(name)


hello_2 = html_tags("b")(hello_no_decorator)
print(hello_2())
# 输出：<b>Hello Toby!</b>
print(hello_2("world"))
# 输出：<b>Hello world!</b>
```

#### 陷阱：延迟绑定闭包

`python` 在闭包（或周围全局作用域）绑定变量的方式，如下

```python
def create_multipliers():
    return [lambda x: i * x for i in range(5)]
```

对如下代码

```python
for multiplier in create_multipliers():
    print(multiplier(2))
```

预期创建五个函数的列表，每个函数有封闭变量 *`i`* 乘以他们的参数，得到 0、2、4、6、8。
实际运行结果

```txt
8
8
8
8
8
```

创建的五个函数都被创建为了 4×2。这是因为 `Python` 的闭包是*`迟绑定`*的，这意味着在闭包中用到的变量的值，
是在内部函数被调用时查询得到的，这意味着，不论任何返回的函数如何被调用，*`i`* 的值都是在循环完成后，即 *`i`* 变成了 4。

解决方案有两种：

- 为函数默认参数赋值的方式，创建一个立即绑定参数的闭包

    ```python
    def default_param_create_multipliers():
        return [lambda x, i=i : i * x for i in range(5)]

    for multiplier in default_param_create_multipliers():
        print(multiplier(2))
    """输出
    0
    2
    4
    6
    8
    """
    ```

- 使用 `functools.partial` 函数

    ```python
    from functools import partial
    from operator import mul
    def partial_create_multipliers():
        return [partial(mul, i) for i in range(5)]
    
    for multiplier in partial_create_multipliers():
        print(multiplier(2))
    """输出
    0
    2
    4
    6
    8
    """
    ```

## 异常、调试与测试

### 使用日志

由于 Python 中的 `print` 函数非常方便，导致代码中常常散布着许多 `print` 调用。  
对于临时调试代码，使用 `print` 比较灵活，可以适当使用。  
但在长期运行和生产环境中，建议使用日志。  
日志功能更加全面，可以控制格式、级别、持久化和异步等行为。  
推荐使用第三方日志库 [`loguru`](https://github.com/Delgan/loguru)，非常方便，开箱即用

考虑到和 `logging` 模块的兼容性，可使用如下代码来对 `logging` 进行配置：

```python
import logging

from loguru import logger

class InterceptHandler(logging.Handler):
    def emit(self, record):
        # 获取对应的 Loguru 等级
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # 将日志记录转发给 loguru
        frame, depth = logging.currentframe(), 2
        while frame:
            if frame.f_code.co_filename not in (__file__, logging.__file__):
                break
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def config_logging(name=None, level="INFO"):
    logging.getLogger(name).addHandler(InterceptHandler())
    logging.getLogger(name).setLevel(level.upper())
```

通过此方法配置后，`loguru`的配置也将在`logging`上生效

- 异常堆栈日志

日志通常用于定位问题，当系统出现异常的时候，只打印错误信息，可能难以定位问题，这个时候可能需要打印详细的日志堆栈，对于日志模块而言，提供了打印详细堆栈的功能，如下：

```python
import logging

logger = logging.getLogger(__name__)

def lumberjack():
    bright_side_of_death()

def bright_side_of_death():
    return tuple()[0]

def test():
    try:
        lumberjack()
    except IndexError as e:
        logger.info(f"err: {e}", exc_info=True)

def main():
    logging.basicConfig(filename='test.log', level=logging.INFO)
    logger.info('Started')
    test()
    logger.info('Finished')

if __name__ == '__main__':
    main()
```
在日志打印中加上`exc_info`可以打印出详细的堆栈信息
```txt
INFO:__main__:err: tuple index out of range
Traceback (most recent call last):
  File "log_test.py", line 24, in test
    lumberjack()
  File "log_test.py", line 7, in lumberjack
    bright_side_of_death()
  File "log_test.py", line 10, in bright_side_of_death
    return tuple()[0]
IndexError: tuple index out of range
INFO:__main__:Finished
```

- 日志分析

日志分析是维护和优化软件系统的重要工具。  
通过收集、存储和分析日志，可以及时发现系统中的问题和异常，提升系统的稳定性和性能。  
公司内的 [CLS](https://console.cloud.tencent.com/cls/overview)、[伽利略](https://galileo.woa.com/)，都是一站式接入后可以完成日志的收集，存储，分析，告警等功能。

### 异常处理

异常处理是编程中重要的一部分，用于应对程序运行过程中可能出现的错误情况。  
Python 提供了强大的异常处理机制，使得程序能够优雅地处理各种异常情况。

- EAFP 与 LBYL 对比 （两种异常处理态度）

    EAFP：直接进行操作，然后通过捕获异常来处理错误情况。代码简洁，但可能需要处理更多的异常。  
    LBYL：在操作前进行检查，以避免异常。代码可能更复杂，但更具预防性。

- EAFP（Easier to Ask for Forgiveness than Permission）

    `EAFP` 是 Python 编程中的一个重要理念，代表 “Easier to Ask for Forgiveness than Permission”，翻译为“与其事先请求许可，不如事后请求原谅”。  
这种编程风格强调在操作前不进行过多的检查，而是直接进行操作，然后通过处理可能出现的异常来应对错误情况。

```python
# EAFP 风格示例
def read_file(file_path):
    try:
        with open(file_path, "r") as file:
            content = file.read()
            return content
    except FileNotFoundError:
        return "File not found."
    except IOError:
        return "Error reading file."


file_content = read_file("example.txt")
print(file_content)
```

- LBYL（Look Before You Leap）

    `LBYL` 风格倾向于在操作前进行检查，以避免异常。

```python
import os


# LBYL 风格示例
def read_file(file_path):
    if not os.path.exists(file_path):
        return "File not found."
    if not os.access(file_path, os.R_OK):
        return "File is not readable."

    with open(file_path, "r") as file:
        content = file.read()
        return content


file_content = read_file("example.txt")
print(file_content)
```

- 自定义异常 & 错误码定义

    在某些情况下，我们可能需要定义自己的异常，以便更好地描述和处理特定的错误情况。

```python
from enum import Enum


class ErrorCode(Enum):
    # 定义错误码和错误消息
    USERNAME_EMPTY = (1000, "用户名不能为空")
    FILE_NOT_FOUND = (2000, "文件未找到")
    NETWORK_FAILURE = (3000, "网络连接失败")

    def __init__(self, code, message):
        self._code = code
        self._message = message

    @property
    def code(self):
        return self._code

    @property
    def message(self):
        return self._message


class CustomError(Exception):
    def __init__(self, error_code: ErrorCode):
        self.code = error_code.code
        self.message = error_code.message
        super().__init__(f"Error {self.code}: {self.message}")

    def __str__(self):
        return f"CustomError {self.code}: {self.message}"


# 示例用法
try:
    raise CustomError(ErrorCode.USER_NOT_FOUND)  # 用户不存在
except CustomError as e:
    print(e)  # 输出: CustomError 1002: 用户不存在
    print(f"Error code: {e.code}")  # 输出: Error code: 1002
    print(f"Error message: {e.message}")  # 输出: Error message: 用户不存在
```

### 使用 `pdb` 进行调试

`pdb` 是 Python 内置的交互式调试器。  
在开发和调试 Python 代码时，`pdb` 允许逐行执行代码，检查变量的值，设置断点，追踪程序的执行流，并在程序运行时进行交互式调试。  
`pdb` 支持在源码行间设置（有条件的）断点和单步执行，检视堆栈帧，列出源码列表，以及在任何堆栈帧的上下文中运行任意 Python 代码。  
`pdb` 还支持事后调试，可以在程序控制下调用。适用于需要逐步执行代码和输出任意变量值以找出错误原因的场景。

- 使用方法

1. **在代码中插入断点**

    你可以在代码中插入断点来启动调试器。

    ```python
    import pdb; pdb.set_trace()

    # 在 Python 3.7 以后的版本中，可以使用如下声明，具有相同的效果
    breakpoint()

    # 也可以通过命令行来调试脚本
    python -m pdb myscript.py
    ```

2. **进入断点后的交互式命令**

    进入断点后，可以通过交互式命令调试 Python 代码。交互式命令包括：逐步执行代码、设置断点、检查变量、评估表达式等等。详细命令请参考 [官方文档](https://docs.python.org/zh-cn/3/library/pdb.html#pdbcommand-help)。

    ```python
    # 待调试的代码
    def double(x):
       breakpoint()
       return x * 2
    val = 3
    print(f"{val} * 2 is {double(val)}")

    # 调试交互命令行
    > ...(3)double()
    -> return x * 2
    (Pdb) p x
    3
    (Pdb) continue
    3 * 2 is 6
    ```

3. **调试器执行代码**

    除了设置断点 `set_trace` 以外，`pdb` 还可以直接运行代码进行调试。

    ```python
    >>> import pdb
    >>> def f(x):
    ...    print(1 / x)
    >>> pdb.run("f(2)")
    > <string>(1)<module>()
    (Pdb) continue
    0.5
    >>>
    ```

4. **异常和崩溃检查**

    `pdb` 还可以进行异常和崩溃检查，输出对应的堆栈和上下文信息，同时也可以继续调试崩溃点。

    ```python
    >>> import pdb
    >>> def f(x):
    ...    print(1 / x)
    >>> f(0)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "<stdin>", line 2, in f
    ZeroDivisionError: division by zero
    >>> pdb.pm()
    > <stdin>(2)f()
    (Pdb) p x
    0
    (Pdb)
    ```

- 常用命令

- `list` 或 `l`：列出当前行附近的代码。
- `next` 或 `n`：执行下一行代码。
- `step` 或 `s`：进入函数内部。
- `continue` 或 `c`：继续执行程序直到下一个断点。
- `print` 或 `p`：打印变量的值。
- `quit` 或 `q`：退出调试器。

### 使用 `gdb` 进行调试

虽然 `pdb` 是一个强大的 Python 代码调试工具，但在某些情况下（例如段错误、挂起进程或失控的守护进程），`pdb` 并不适用。  
`gdb` 是一个主要用于调试用 C、C++ 等编写的低级代码的强大调试工具，但它也可以用于调试 Python 解释器本身或涉及到 C 扩展模块的 Python 程序。

- 调试方法

1. **交互式调试**：

    ```shell
    gdb python
    (gdb) run <programname>.py <arguments>
    ```

2. **直接调试**：

    ```shell
    gdb -ex r --args python <programname>.py <arguments>
    ```

3. **通过进程号调试**：

    ```shell
    gdb python <pid of running process>
    ```

- 常用 GDB 命令

- **查看调用栈**：

    ```shell
    (gdb) bt
    ```

- **查看线程信息**：

    ```shell
    (gdb) info threads
    ```

- **切换到特定线程**：

    ```shell
    (gdb) thread <thread-number>
    ```

- **打印变量值**：

    ```shell
    (gdb) print <variable>
    ```

- **设置断点**：

    ```shell
    (gdb) break <location>
    ```

- **继续执行**：

    ```shell
    (gdb) continue
    ```

- 调试 Python 代码

    GDB 也可以调试 Python 代码本身。例如，您可以查看 Python 调用栈、切换线程以及打印变量值。

    ```shell
    # 启动 GDB 并运行 Python 程序
    $ gdb python
    (gdb) run script.py
    
    # 发生段错误时，查看 Python 调用栈
    (gdb) py-bt
    
    # 查看所有 Python 线程
    (gdb) py-list
    
    # 切换到特定的 Python 线程
    (gdb) py-up
    (gdb) py-down
    
    # 打印 Python 对象
    (gdb) py-print <python-variable>
    ```

### 调试 - 程序崩溃/卡死分析

Python 程序崩溃或卡死可能由多种原因引起。以下是快速定位问题的方法：

1. **生成核心转储文件**  
    严重崩溃时，使用 `gdb` 分析核心转储文件。

    ```shell
    ulimit -c unlimited
    python your_script.py
    gdb python core
    ```

2. **堆栈跟踪**  
   程序挂起时，使用 `faulthandler` 和 `signal` 模块输出堆栈跟踪信息。

    ```python
    import faulthandler
    import signal
   
    faulthandler.enable()
    signal.signal(signal.SIGUSR1, faulthandler.dump_traceback)
    ```

3. **PySnooper**  
   为函数添加装饰器，输出详细日志。

    ```shell
    pip install pysnooper
   
    import pysnooper
   
    @pysnooper.snoop()
    def demo_func():
        ...
    ```

4. **objprint**  
   打印对象信息，便于调试自定义对象。

    ```shell
    pip install objprint
   
    from objprint import op
   
    class Player:
        def __init__(self):
            self.name = "John"
            self.score = 100
   
    op(Player())
    ```

5. **line_profiler**  
   逐行分析函数运行时间，找出耗时最多的代码。

    ```shell
    pip install line_profiler
   
    @profile
    def line_profiler_test():
        ...
   
    # 运行 line_profiler
    kernprof -l -v line_profiler_test.py
    ```

6. **memory_profiler**  
   逐行分析内存使用情况，找出占用内存最大的代码。

    ```shell
    pip install memory_profiler
   
    @profile
    def memory_profiler_test():
        ...
   
    # 运行 memory_profiler
    python -m memory_profiler memory_profiler_test.py
    ```

### 测试

#### 表格驱动

表格驱动本质上是数据驱动，对于纯逻辑的代码，可以考虑用这种模式来写单测用例，这样可以充分复用执行用例的代码，也便于管理和扩展测试数据。

使用任意的测试框架（`unittest`, `pytest`, `nose` 等）都可以，下面使用 `unittest` 作为示例：
```python
import unittest

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def test_addition(self):
        test_cases = [
            (2, 3, 5),
            (-1, 1, 0),
            (0, 0, 0),
            (100, -100, 0)
        ]
        for x, y, expected in test_cases:
            with self.subTest(x=x, y=y):
                result = self.calculator.add(x, y)
                self.assertEqual(result, expected)
```

#### 行为驱动

对于业务逻辑更复杂的代码单元，可以考虑从需求出发，分场景使用行为驱动的模式来写单测用例，这样的单测更强调模块行为，便于开发沟通。此外，对于推行 TDD（Test Driven Development 测试驱动开发）的团队，可以考虑使用这种模式，在对需求的过程中确定待测试的场景，并通过代码实现。

行为驱动可以使用开源库 `behave`，示例代码如下：

```python
# 1. 需求
"""
# -* FILE: features/example.feature
Feature: Showing off behave

  Scenario: Run a simple test
    Given we have behave installed
     When we implement 5 tests
     Then behave will test them for us!
"""

# 2. 单测
# -* FILE: features/steps/example_steps.py
from behave import given, when, then, step


@given("we have behave installed")
def step_impl(context):
    pass


@when("we implement {number:d} tests")
def step_impl(context, number):  # -* NOTE: number is converted into integer
    assert number > 1 or number == 0
    context.tests_count = number


@then("behave will test them for us!")
def step_impl(context):
    assert context.failed is False
    assert context.tests_count >= 0
```

#### Mock建议

即使已经对代码单元按照层次、功能等进行了拆分，在对复杂代码进行单测时，也经常会受到外部依赖的影响。为这类代码编写单测时，需要考虑使用 Mock 技术。

- 最佳实践

1. **明确 Mock 的范围**：只 Mock 必要的部分，避免过度Mock导致测试失去实际意义。
2. **使用 Patch 装饰器**：通过 `patch` 装饰器可以简化Mock对象的创建和销毁，确保Mock在测试结束后被还原。
3. **验证 Mock 行为**：不仅要验证被测试函数的输出，还要验证Mock对象的调用情况（如方法调用次数、参数等）。
4. **保持 Mock 对象简单**：尽量避免在 Mock 对象上添加过多复杂的行为和逻辑，保持Mock的简洁性。

- 常见误区

- 问题1：Mock 对象过于复杂
- **解决方案**：审视测试用例，简化 Mock 对象的行为，确保 Mock 对象仅模拟必要的部分。

- 问题2：Mock依赖的对象路径错误
- **解决方案**：确保 `patch` 的路径正确，**路径应指向在测试模块中使用的具体对象**，而非其定义位置。

- 问题3：Mock对象未被还原
- **解决方案**：使用 `patch` 装饰器或上下文管理器来自动管理 Mock 对象的生命周期，避免手动还原的遗漏。

- 问题4：测试结果不稳定
- **解决方案**：避免在 Mock 对象上模拟过多复杂行为，保持 Mock 的简单性和确定性。

#### 覆盖率建议

单元测试覆盖率没有一个固定的“合适”的标准，它取决于代码质量、业务需求、团队偏好。

新项目如果对覆盖率有要求，可以考虑设置 70%～80% 的基准，这可以覆盖大部分重要的功能和逻辑路径，并且后续可以视情况提升覆盖率要求。而对于存量项目，为其补充单元测试代码充满挑战，可以考虑使用 AI 工具批量生成，并在此基础上辅以人工补充即可达到较高的覆盖率。

重业务逻辑的后台服务项目与轻业务逻辑的底层 SDK 对于单元测试覆盖率的要求是不同的，如果一个代码模块会被多个上层业务模块调用，或处于系统的关键路径，则需要考虑设置更高的覆盖率基准，例如超过 90%。

根据经验，当项目开始要求覆盖率指标时，可将历史最高覆盖率作为初次全量覆盖率基准，并为增量代码设置 60% 的覆盖率门槛，这样通过不断的迭代，以及定期的 Review，可以让项目代码的覆盖率维持在一个健康的水位。

## 并发编程

在 Python 中，并行与并发编程是优化程序性能、提高效率的关键技术。

### 并发与并行的区别

- **并发 (Concurrency)**：  
  - 在同一时间段内管理多个任务的执行。
  - 并发主要通过任务切换来实现，看起来像是同时执行，但实际上并不一定是同时进行的；常用于 I/O 密集型任务。

- **并行 (Parallelism)**：  
  - 实际的同时执行多个任务，通常利用多核处理器来实现。
  - 并行主要用于 CPU 密集型任务。

### Python 实现并发与并行的方法

Python 提供了多种实现并发与并行的方法，包括线程、多进程、协程等。  
每种方法都有其优劣势和适用场景。

### 选择并发/并行模型

根据任务的性质和 `GIL` 的影响，选择合适的并发/并行模型非常重要：

- **I/O 密集型任务**：推荐使用多线程或协程（如 `asyncio`）。多线程在处理 I/O 操作时可以让 GIL 释放，多个线程并发执行。协程通过非阻塞 I/O 和事件循环实现高效并发。

- **CPU 密集型任务**：推荐使用多进程。由于每个进程有独立的 GIL，多个进程可以并行执行，充分利用多核 CPU。

### 多线程（Threading）

- **适用场景**：I/O 密集型任务，如文件读写、网络请求等。
- **优点**：轻量级，创建和销毁开销较小。
- **缺点**：受制于 GIL（全局解释器锁），无法充分利用多核 CPU。

```python
import threading


def task():
    print("Task executed")


threads = []
for _ in range(5):
    thread = threading.Thread(target=task)
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
```

### 多进程（Multiprocessing）

- **适用场景**：CPU 密集型任务，如科学计算、图像处理等。
- **优点**：每个进程有独立的 GIL，可以充分利用多核 CPU。
- **缺点**：进程间通信开销大，创建和销毁进程开销较大。

```python
import multiprocessing


def task():
    print("Task executed")


processes = []
for _ in range(5):
    process = multiprocessing.Process(target=task)
    processes.append(process)
    process.start()

for process in processes:
    process.join()
```

### 协程（Coroutine）

- **适用场景**：I/O 密集型任务，尤其是需要大量并发的网络请求。
- **优点**：轻量级，相比线程和进程，协程的切换开销更小。
- **缺点**：需要异步编程模型的支持，代码可读性相对较差。

`Asyncio` 是 Python 的一个标准库，提供了编写单线程并发代码的框架。它使用协程作为其并发模型的基础。`Asyncio` 支持事件循环，这是异步编程的核心，用于调度协程的执行。

`Asyncio` 库使用协程作为其并发模型的基础，但协程的概念不仅限于 Asyncio。其他库（如 `Tornado`、`Twisted`）也可以实现协程。

```python
import asyncio


async def task():
    print("Task executed")


async def main():
    tasks = [task() for _ in range(5)]
    await asyncio.gather(*tasks)


asyncio.run(main())
```

1. **选择合适的并发/并行模型**：根据任务的性质选择合适的并发/并行模型。I/O 密集型任务优先选择多线程或异步编程，CPU 密集型任务优先选择多进程。

2. **避免共享状态**：在并发和并行编程中，尽量避免不同线程或进程共享状态，以减少复杂性和避免竞争条件。可以使用队列、管道等机制进行通信。

3. **使用高级库**：对于复杂的并发和并行任务，考虑使用高级库，如 `concurrent.futures` 提供的 `ThreadPoolExecutor` 和 `ProcessPoolExecutor`，可以简化线程和进程的管理。

4. **性能调优**：并发和并行编程并不总是能提高性能，甚至可能由于上下文切换和通信开销导致性能下降。需要通过实际测试和监控来调优并发和并行程序。

5. **错误处理**：在并发和并行编程中，错误处理尤为重要。确保所有线程、进程或协程中的异常都能正确捕获和处理，避免程序崩溃或死锁。

### 使用 `concurrent.futures`

`concurrent.futures` 提供了一个高级接口来管理线程和进程池，非常适合并发/并行任务。

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def task(x):
    return x * x


# 使用线程池
with ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(task, range(10)))
    print(results)

# 使用进程池
with ProcessPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(task, range(10)))
    print(results)
```

### 全局解释器锁（GIL）

全局解释器锁（Global Interpreter Lock, GIL）是 Python 中一个影响并发和并行行为的重要机制。GIL 是一个互斥锁，保护访问 Python 对象的全局状态。它确保在任意时刻只有一个线程执行 Python 字节码，避免了多线程访问共享数据时出现数据竞争问题。CPython 采用了这种方案，其他解释器如 Jython、IronPython 和 PyPy 由于其底层实现和语言特性，可能不需要 GIL 或以不同方式处理并发和并行问题。

1. **GIL 与多线程**

    - **并发**：Python 的多线程主要用于 I/O 密集型任务，如网络请求、文件读写等。在这些任务中，线程经常处于等待状态，GIL 会释放给其他线程，从而实现并发。即使在有 GIL 的情况下，多线程仍然能提高 I/O 密集型任务的性能。

    - **并行**：由于 GIL 的存在，Python 中的多线程无法实现真正的并行执行（即同时在多个 CPU 核心上运行）。在 CPU 密集型任务中，多线程并不会带来性能提升，因为 GIL 会阻止多个线程同时执行 Python 代码。

2. **GIL 与多进程**

    - **并行**：多进程方式每个进程都有自己的 Python 解释器和 GIL，因此能够实现真正的并行。多进程适用于 CPU 密集型任务，可以充分利用多核 CPU 的能力。

    - **开销**：进程间的通信和创建销毁进程的开销较大，但在需要并行处理的 CPU 密集型任务中，多进程通常能显著提高性能。

3. **GIL 与协程**

    - **并发**：协程（如 `asyncio`）通过非阻塞 I/O 和事件循环实现并发。协程本质上是单线程的，因此不会受到 GIL 的影响。协程适用于 I/O 密集型任务，可以高效地管理大量并发操作。

    - **并行**：协程无法实现真正的并行执行，因为它们在同一个线程内运行。

### 协程

Python 提供语言级别的协程，用户可以通过 `async/await` 关键字来使用协程特性；  
与线程和进程不同，协程更轻量，其调度控制权更多由用户或者库（例如：[asyncio](https://docs.python.org/3/library/asyncio.html)）来决定的；
比较适用于 IO 密集型场景；下面结合`asyncio`介绍几个协程使用的误区

#### 协程并发调用

Python 的协程属于非线程安全，只能在单线程中运行，也即表明协程只能在单线程并发来提升性能，下面给出其并发使用的例子

- 非并发协程

  ```python
  # Bad
  import asyncio
  import time
  
  async def test(info: str):
      await asyncio.sleep(1)
      print(info)
  
  
  async def main():
      t1 = time.time()
      for i in range(3):
          await test(f"{i}")
      t2 = time.time()
      print(f"cost is {t2-t1}")
  
  
  if __name__ == "__main__":
      loop = asyncio.get_event_loop()
      loop.run_until_complete(main())
  ```

  执行一下可以看出耗时为3s，性能并不会因为使用了协程而有提升，说明**并不是使用协程就可以并发**

- 并发协程

  ```python
  # Good
  import asyncio
  import time
  
  async def test(info: str):
      await asyncio.sleep(1)
      print(info)
  
  
  async def main(loop):
    tasks = []
    t1 = time.time()
    for i in range(3):
        tasks.append(loop.create_task(test(f"{i}")))
    await asyncio.gather(*tasks)
    t2 = time.time()
    print(f"main1 cost is {t2-t1}")
  
  
  if __name__ == "__main__":
      loop = asyncio.get_event_loop(loop)
      loop.run_until_complete(main())
  ```

  执行一下可以看出耗时为1s，并发使用了协程，性能有提升

  对比以上两个例子，可以看出并不是协程就一定提升性能，需要看需要多个协程并发调用，才可以提升性能，若是串行执行，并不能发挥协程的优势

#### 协程调度

协程的调度只是相对线程而言要轻量，并不是完全无消耗，程序中频繁调度或者不调度，都会影响程序性能。

- 无协程调度

  ```python
  # Bad
  import asyncio
  import time
  
  async def test(info: str):
      time.sleep(1)
      print(info)
  
  
  async def main(loop):
    tasks = []
    t1 = time.time()
    for i in range(3):
        tasks.append(loop.create_task(test(f"{i}")))
    await asyncio.gather(*tasks)
    t2 = time.time()
    print(f"main1 cost is {t2-t1}")
  
  
  if __name__ == "__main__":
      loop = asyncio.get_event_loop()
      loop.run_until_complete(main(loop))
  ```

  该例子运行耗时是 3s，原因主要是在 `test` 中没有执行 `await` 让出 CPU，本质就是串行执行，没有发挥并发执行的特性；
  所以定义协程函数的时候，并非只有关键字 `async` 就能发挥协程的优势

- 频繁协程调度

  ```python
  # Bad
  import asyncio
  import time
  import math
  
  async def test(info: str, digits: int):
      decimal_places = digits + 1 
      for i in range(0, 10000):
          await asyncio.sleep(0)
          pi = str(math.pi)[:decimal_places]
      print(info)
  
  
  async def main(loop):
    tasks = []
    t1 = time.time()
    for i in range(100):
        tasks.append(loop.create_task(test(f"{i}", i)))
    await asyncio.gather(*tasks)
    t2 = time.time()
    print(f"main1 cost is {t2-t1}")
  
  if __name__ == "__main__":
      loop = asyncio.get_event_loop()
      loop.run_until_complete(main(loop))
  ```

  该例子中，每次进行计算的时候，执行 `await asyncio.sleep(0)` 本质就是让出 cpu，该例子耗时是 `4.5s` ；
  **若是注释 `await asyncio.sleep(0)` 耗时则是 `0.8s`** ；由此可见，频繁的协程调度占了耗时热点，反而会损耗性能

#### 协程包装

用户在做业务开发的时候，可能因为兼容旧业务或者第三方库，对于一些非协程函数需要包装为协程函数，可以采用以下几种方式

- 同步函数包装为协程函数

  ```python
  # Good
   import asyncio
   
   def sync_func():
       # 这里是你的同步代码
       pass
   
   async def async_wrapper():
       loop = asyncio.get_event_loop()
       result = await loop.run_in_executor(None, sync_func)
       return result
  ```

    这里采用 `run_in_executor` 函数包装非协程函数为协程函数。在python 3.9之后，也可以使用`to_thread`简化写法：

  ```python
  import asyncio
  
  def sync_func():
      # 这里是你的同步代码
      pass
  
  async def async_wrapper():
      result = await asyncio.to_thread(sync_func)
      return result
  ```

- 非协程函数并发执行

  ```python
   # Good
   import asyncio
   
   def user_func(args):
       print(f'args : {args}')
       return f"{args}"
   
   async def set_future_result(future, args):
       res = user_func(args)
       future.set_result(res)
   
   async def main():
       future1 = asyncio.Future()
       future2 = asyncio.Future()
       asyncio.create_task(set_future_result(future1, "test1"))
       asyncio.create_task(set_future_result(future2, "test2"))
       results = await asyncio.gather(future1, future2)
       print(f'results: {results}')
   
   asyncio.run(main())
  ```

   这里将用户函数 `user_func` 包装为协程函数并发执行

#### 协程安全

当 `asyncio` 调度多个协程并发运行的时候，也会存在临界资源安全的问题。  
这里就需要对临界资源进行同步保护。

下面给出两个例子：

- 单线程多协程并发

  ```python
  import asyncio
  
  class SharedResource:
      def __init__(self):
          self.value = 0 
          self.lock = asyncio.Lock()
  
      async def safe_increment(self, t):
          # Good
          async with self.lock:
              print(f"Safe incrementing from {self.value}")
              await asyncio.sleep(t)  # 模拟异步操作
              self.value += 1
  
      async def unsafe_increment(self, t):
          # Bad
          print(f"Unsafe incrementing from {self.value}")
          await asyncio.sleep(t)  # 模拟异步操作
          self.value += 1
  
  async def worker(resource, n):
      for t in range(n):
          #await resource.unsafe_increment(t)
          await resource.safe_increment(t)
  
  async def main():
      resource = SharedResource()
      await asyncio.gather(worker(resource, 5), worker(resource, 5))
  
  asyncio.run(main())
  ```

  运行结果：

  ```txt
  # ===========unsafe ========
  Unsafe incrementing from 0
  Unsafe incrementing from 0
  Unsafe incrementing from 1
  Unsafe incrementing from 2
  Unsafe incrementing from 3
  Unsafe incrementing from 4
  Unsafe incrementing from 5
  Unsafe incrementing from 6
  Unsafe incrementing from 7
  Unsafe incrementing from 8
  # ===========safe ========
  Safe incrementing from 0
  Safe incrementing from 1
  Safe incrementing from 2
  Safe incrementing from 3
  Safe incrementing from 4
  Safe incrementing from 5
  Safe incrementing from 6
  Safe incrementing from 7
  Safe incrementing from 8
  Safe incrementing from 9
  ```

  可以看出加锁同步后的数据是符合预期

- 多线程协程运行

  ```python
  # Good
  import asyncio
  import threading
  import time
  
  async def async_task(name, delay):
      print(f"Task {name} started in thread {threading.current_thread().name}")
      await asyncio.sleep(delay)
      print(f"Task {name} finished in thread {threading.current_thread().name}")
      return f"Result of task {name}"
  
  def run_event_loop(loop):
      asyncio.set_event_loop(loop)
      loop.run_forever()
  
  def main():
    # 创建一个事件循环
    loop = asyncio.new_event_loop()
  
    # 创建并启动一个线程来运行事件循环
    thread = threading.Thread(target=run_event_loop, args=(loop,))
    thread.start()
  
    # 在另一个线程中调度协程
    future1 = asyncio.run_coroutine_threadsafe(async_task("A", 2), loop)
    future2 = asyncio.run_coroutine_threadsafe(async_task("B", 3), loop)
  
    # 等待协程完成并获取结果
    print(future1.result())
    print(future2.result())
    # 停止事件循环
    loop.call_soon_threadsafe(loop.stop)
    thread.join()
  
  if __name__ == "__main__":
    main()
  ```

    采用 `run_coroutine_threadsafe` 接口可以在不同线程中安全运行协程

#### 协程其他使用方式

- 判断一个回调函数是否为协程

  ```python
  import inspect
  inspect.isawaitable(handler) or inspect.iscoroutinefunction(handler) or inspect.isasyncgenfunction(handler)
  ```

- 线程池中运行协程

  ```python
  import asyncio
  import concurrent.futures
  
  def create_pool(thread_num: int):
    return concurrent.futures.ThreadPoolExecutor(thread_num)
  
  async def submit(func, *args):
    pool = create_pool(3)
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(pool, func, *args)
  ```

## 文件与IO

### 序列化与反序列化

序列化和反序列化是软件开发中的常见操作，涉及将数据结构或对象转换为可存储或传输的格式，以及将其还原为原始数据结构。本文将详细讨论序列化格式及其安全性问题。

#### 序列化格式

  序列化格式决定了数据在序列化后的表示方式。常见的序列化格式有：

1. **JSON (JavaScript Object Notation)**

    - **特点**：人类可读，广泛支持，轻量级。
    - **优点**：易于理解和调试，跨平台兼容性强。
    - **缺点**：不支持二进制数据，序列化后的数据体积可能较大。

    ```python
    import json

    data = {'name': 'John', 'age': 30}
    serialized_data = json.dumps(data)
    deserialized_data = json.loads(serialized_data)
    ```

2. **XML (eXtensible Markup Language)**

    - **特点**：自描述性强，人类可读。
    - **优点**：灵活，支持复杂的数据结构。
    - **缺点**：冗长，解析效率较低。

    ```python
    import xml.etree.ElementTree as ET

    data = {'name': 'John', 'age': 30}
    root = ET.Element("person")
    ET.SubElement(root, "name").text = data['name']
    ET.SubElement(root, "age").text = str(data['age'])
    serialized_data = ET.tostring(root)
    deserialized_data = {'name': root.find("name").text, 'age': int(root.find("age").text)}
    ```

3. **YAML (YAML Ain't Markup Language)**

    - **特点**：人类可读，类似于 JSON，但更简洁。
    - **优点**：易于编写和阅读，支持复杂数据结构。
    - **缺点**：解析速度较慢，安全性问题较多。

    ```python
    import yaml

    data = {'name': 'John', 'age': 30}
    serialized_data = yaml.dump(data)
    deserialized_data = yaml.safe_load(serialized_data)
    ```

4. **Protocol Buffers (protobuf)**

    - **特点**：二进制格式，高效紧凑。
    - **优点**：序列化后的数据体积小，解析速度快，支持多种编程语言。
    - **缺点**：不人类可读，需要预定义数据结构。

    ```proto
    syntax = "proto3";

    message Person {
      string name = 1;
      int32 age = 2;
    }
    ```

    ```python
    import person_pb2

    data = person_pb2.Person(name='John', age=30)
    serialized_data = data.SerializeToString()
    deserialized_data = person_pb2.Person()
    deserialized_data.ParseFromString(serialized_data)
    ```

5. **MessagePack**

    - **特点**：二进制格式，比 JSON 快且紧凑。
    - **优点**：高效，支持多种编程语言。
    - **缺点**：不人类可读，调试较困难。

    ```python
    import msgpack
    
    data = {'name': 'John', 'age': 30}
    serialized_data = msgpack.packb(data)
    deserialized_data = msgpack.unpackb(serialized_data)
    ```

#### 序列化安全

序列化和反序列化时的安全性问题非常重要，尤其是在处理不受信任的数据时。以下是一些常见的安全问题及其解决方案。

1. **代码执行漏洞**（例如，Python 的 `pickle` 模块）

    - **问题**：某些序列化格式（如 Python 的 `pickle`）允许序列化后的数据执行任意代码，可能被恶意利用。
    - **解决方案**：避免使用不安全的序列化格式处理不受信任的数据。例如，避免使用 `pickle`，而使用更安全的格式如 JSON 或 Protocol Buffers。

    ```python
    import pickle

    # 不要使用 pickle 处理不受信任的数据
    serialized_data = pickle.dumps(data)
    deserialized_data = pickle.loads(serialized_data)
    ```

2. **数据完整性和篡改**

    - **问题**：序列化后的数据在传输或存储过程中可能被篡改。
    - **解决方案**：使用数字签名或哈希校验来验证数据的完整性。例如，使用 HMAC 来验证数据。

    ```python
    import hmac
    import hashlib

    key = b'secret_key'
    data = b'some_data'
    signature = hmac.new(key, data, hashlib.sha256).hexdigest()

    # 验证数据完整性
    if hmac.new(key, data, hashlib.sha256).hexdigest() == signature:
        print("Data is intact")
    ```

3. **数据泄露**

    - **问题**：序列化后的数据可能包含敏感信息，泄露会造成安全问题。
    - **解决方案**：对敏感数据进行加密，并确保加密密钥的安全存储和管理。

    ```python
    from cryptography.fernet import Fernet

    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    data = b'some_sensitive_data'
    encrypted_data = cipher_suite.encrypt(data)

    # 解密数据
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    ```

4. **反序列化攻击**

    - **问题**：通过发送特制的恶意数据包，攻击者可能在反序列化时触发漏洞。
    - **解决方案**：严格验证数据的格式和内容，使用安全的反序列化库。例如，使用 `yaml` 模块的 `safe_load` 方法替代 `load` 方法。

    ```python
    import yaml

    # 不要使用 yaml.load 处理不受信任的数据
    deserialized_data = yaml.safe_load(serialized_data)
    ```

5. **权限问题**

    - **问题**：反序列化后的数据对象可能破坏系统的权限约束。
    - **解决方案**：在反序列化前严格验证数据，确保其符合预期的权限和访问控制。

## 高级用法与框架

### 跨语言调用

在实际开发中，跨语言调用是一个非常常见的需求，尤其是在需要利用不同语言的优势时。  
跨语言调用可以极大地扩展程序的功能和性能，但同时也增加了复杂性。
以下是一些关于 Python 调用其他语言，以及其他语言调用 Python 的经验总结。

#### Python 调用其他语言

Python 可以通过多种方式调用其他语言的代码，这在需要利用其他语言的性能或功能优势时非常有用。

1. 使用 `ctypes` 或 `cffi` 调用 C 语言代码

   - `ctypes` 是 Python 的内建库，允许调用 C 函数库。
   - `cffi` 更强大且更灵活，适用于需要深度集成的场景。

    ```python
    # 使用 ctypes 调用 C 函数示例
    import ctypes

    # 加载共享库
    lib = ctypes.CDLL('./mylib.so')

    # 调用 C 函数
    result = lib.my_c_function(5)
    print(result)
    ```

1. 使用 `subprocess` 调用外部程序

   - 适用于需要调用其他语言编写的命令行工具或脚本。

   ```python
   # 使用 subprocess 调用外部程序示例
   import subprocess

   result = subprocess.run(['my_program', 'arg1', 'arg2'], capture_output=True, text=True)
   print(result.stdout)
   ```

1. 使用 `pybind11` 进行 C++ 集成

   - `pybind11` 使得在 Python 中调用 C++ 代码变得简单且高效。

   ```cpp
   // C++ 代码示例 (example.cpp)
   #include <pybind11/pybind11.h>
   
   int add(int i, int j) {
       return i + j;
   }
   
   PYBIND11_MODULE(example, m) {
       m.def("add", &add, "A function which adds two numbers");
   }
   ```

   ```python
   # Python 代码示例
   import example
   print(example.add(1, 2))
   ```

#### 其他语言调用 Python

有时需要在其他语言的项目中利用 Python 强大的库和功能，例如数据处理和机器学习。

1. 使用 Python 的 C API

   - 适用于需要高性能和紧密集成的场景。

   ```c
   // C 代码示例
   #include <Python.h>

   int main() {
       Py_Initialize();
       PyRun_SimpleString("print('Hello from Python!')");
       Py_Finalize();
       return 0;
   }
   ```

1. 使用 `Jython` 调用 Python 代码（Java）

   - `Jython` 是 Python 的 Java 实现，允许在 Java 中直接运行 Python 代码。

   ```java
   // Java 代码示例
   import org.python.util.PythonInterpreter;

   public class JythonExample {
       public static void main(String[] args) {
           PythonInterpreter interpreter = new PythonInterpreter();
           interpreter.exec("print('Hello from Python!')");
       }
   }
   ```

1. 使用 `py4j` 进行 Java 和 Python 的互操作

    - `py4j` 允许在 Java 中调用 Python 代码，并且可以在 Python 中调用 Java 对象。

    ```python
    # Python 代码示例
    from py4j.java_gateway import JavaGateway
    
    gateway = JavaGateway()
    java_object = gateway.entry_point.getJavaObject()
    java_object.callMethod()
    ```

    ```java
    // Java 代码示例
    import py4j.GatewayServer;
    
    public class EntryPoint {
        public String getJavaObject() {
            return "Hello from Java!";
        }
    
        public static void main(String[] args) {
            GatewayServer gatewayServer = new GatewayServer(new EntryPoint());
            gatewayServer.start();
            System.out.println("Gateway Server Started");
        }
    }
    ```

### 自动化文档生成

在 Python 项目中，自动化文档生成是提高代码可维护性的重要手段。  
通过自动化工具，可以从代码注释中提取信息并生成文档，减少手动维护文档的工作量。

1. 使用 Sphinx 生成文档

    Sphinx 是一个广泛使用的文档生成工具，特别适用于 Python 项目。它可以根据代码中的文档字符串（Docstrings）生成详细的文档。

1. 使用 docstrings 编写文档

    在 Python 代码中使用 docstrings 为函数、类和模块编写文档：

    ```python
    def add(x, y):
        """
        Add two numbers and return the result.

        :param x: First number
        :type x: int
        :param y: Second number
        :type y: int
        :return: Sum of x and y
        :rtype: int
        """
        return x + y
    ```

1. 自动化文档生成和部署

    可以使用 CI/CD 工具（如 蓝盾 Pipeline）自动生成和部署文档。

1. 使用 MkDocs 生成文档

    MkDocs 是另一个流行的文档生成工具，使用 Markdown 格式编写文档，并生成静态网站。

1. 其他有用的工具

   - **pdoc**：一个简单的 Python 文档生成工具，支持 Markdown 和 HTML 输出。
   - **pydoctor**：一个强大的文档生成工具，特别适用于大型 Python 项目。

### 性能分析

在 Python 编程中，性能分析是优化程序运行效率的重要步骤。  
通过适当的性能分析工具和方法，可以识别程序中的性能瓶颈，并进行有针对性的优化。

1. 使用合适的性能分析工具

    Python 提供了多种性能分析工具，每种工具都有其适用的场景和优缺点。常用的工具包括：

    - **cProfile**：内置的性能分析工具，适用于大多数情况，能够生成详细的函数调用统计信息。
    - **timeit**：适用于小代码片段的性能测试，尤其是对比不同实现方案的执行时间。
    - **line_profiler**：针对代码逐行分析，可以精确定位代码中耗时的行。

    ```python
    # 使用 cProfile 进行性能分析
    import cProfile

    def my_function():
        # 函数代码
        pass

    cProfile.run('my_function()')
    ```

1. 关注代码的热点

    性能分析的目标是找到代码中的性能瓶颈，而不是优化每一行代码。使用性能分析工具，找出那些占用大量时间的函数或代码块，然后集中精力优化这些部分。

1. 避免过早优化

    在性能分析之前，不要急于对代码进行优化。过早优化可能会导致代码复杂化，反而影响可读性和维护性。先确保代码能够正确运行，然后再进行性能分析和优化。

1. 优化常见性能瓶颈

    在进行性能优化时，可以关注一些常见的性能瓶颈：

    - **数据结构选择**：选择合适的数据结构，如使用 `list`、`set` 或 `dict`，可以显著提高性能。
    - **算法优化**：优化算法的时间复杂度，如将 `O(n^2)` 的算法优化为 `O(n log n)`。
    - **避免不必要的计算**：缓存重复计算的结果，减少不必要的函数调用。

1. 考虑并行和异步

    对于 I/O 密集型和 CPU 密集型任务，可以考虑使用并行或异步编程来提升性能。Python 提供了多种并行和异步编程工具，如 `threading`、`multiprocessing` 和 `asyncio`。

    ```python
    # 使用 asyncio 进行异步编程
    import asyncio
    
    async def async_function():
        await asyncio.sleep(1)
        print("Hello, World!")
    
    asyncio.run(async_function())
    ```

### 网络编程

在 Python 编程中，网络编程是一个常见且重要的领域。  
无论是开发网络应用、进行数据采集，还是实现分布式系统，都需要一定的网络编程经验。

1. 选择合适的库

    Python 提供了多种网络编程库，每种库都有其适用的场景和特点：

    - **requests**：简单易用，对 HTTP 请求进行封装，是处理 Web 服务请求的首选。
    - **socket**：提供了底层的网络接口，适用于需要更多控制和自定义的场景。
    - **asyncio**：适用于编写高并发的异步网络应用。
    - **http.client** 和 **urllib**：标准库中的 HTTP 客户端和 URL 处理库，适合需要标准库解决方案的场景。

    ```python
    # 使用 requests 进行 HTTP 请求
    import requests

    response = requests.get('https://api.example.com/data')
    print(response.json())
    ```

1. 处理网络异常

    网络请求容易受到各种因素影响而失败，如网络中断、服务器故障等。因此，在编写网络代码时，要做好异常处理，确保程序的健壮性。

    ```python
    import requests
    from requests.exceptions import RequestException

    try:
        response = requests.get('https://api.example.com/data')
        response.raise_for_status()
    except RequestException as e:
        print(f"Network error: {e}")
    ```

1. 使用超时和重试机制

    网络请求可能会因为各种原因变得非常慢或超时。设置合理的超时和重试机制，可以提高程序的健壮性和用户体验。

    ```python
    import requests
    from requests.adapters import HTTPAdapter
    from requests.packages.urllib3.util.retry import Retry

    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))

    try:
        response = session.get('https://api.example.com/data', timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    ```

1. 使用异步编程提高并发

    对于高并发的网络应用，使用异步编程可以显著提高性能。Python 的 `asyncio` 库提供了强大的异步编程支持。

    ```python
    import asyncio
    import aiohttp

    async def fetch(session, url):
        async with session.get(url) as response:
            return await response.text()

    async def main():
        async with aiohttp.ClientSession() as session:
            html = await fetch(session, 'https://www.example.com')
            print(html)

    asyncio.run(main())
    ```

1. 安全和认证

    在进行网络编程时，安全和认证是非常重要的。对于 HTTPS 请求，确保 SSL/TLS 证书的正确性；对于需要身份验证的 API，使用合适的认证方法，如 OAuth。

    ```python
    import requests
    
    response = requests.get('https://api.example.com/secure-data', headers={'Authorization': 'Bearer YOUR_ACCESS_TOKEN'})
    print(response.json())
    ```

### 数据库操作

在 Python 编程中，数据库操作是一个重要且常见的任务，无论是开发 Web 应用、数据分析，还是其他需要持久化数据的场景。

1. 选择合适的数据库和库

    Python 支持多种数据库，每种数据库和库都有其适用的场景：

    - **SQLite**：轻量级嵌入式数据库，适用于小型项目或单用户应用。使用标准库 `sqlite3` 连接。
    - **PostgreSQL**：功能强大的关系型数据库，适用于复杂查询和事务。使用 `psycopg2` 或 `asyncpg` 连接。
    - **MySQL**：广泛使用的关系型数据库，适用于大多数 Web 应用。使用 `mysql-connector-python` 或 `PyMySQL` 连接。
    - **MongoDB**：NoSQL 文档数据库，适用于需要灵活数据结构的应用。使用 `pymongo` 连接。
    - **Redis**：键值对存储数据库，适用于缓存和实时分析。使用 `redis-py` 连接。

    ```python
    # 使用 sqlite3 连接 SQLite 数据库
    import sqlite3

    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)')
    conn.commit()
    conn.close()
    ```

1. 使用 ORM 提高开发效率

    对象关系映射（ORM）可以简化数据库操作，减少手写 SQL 的复杂性，提高代码的可维护性。常用的 ORM 包括：

    - **SQLAlchemy**：功能强大的 ORM，支持多种数据库。
    - **Django ORM**：集成在 Django 框架中的 ORM，适用于 Django 项目。

    ```python
    # 使用 SQLAlchemy ORM
    from sqlalchemy import create_engine, Column, Integer, String
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker

    Base = declarative_base()

    class User(Base):
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True)
        name = Column(String)

    engine = create_engine('sqlite:///example.db')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    new_user = User(name='John Doe')
    session.add(new_user)
    session.commit()
    ```

1. 处理数据库连接和异常

    数据库连接可能会因为网络问题或数据库服务器故障而失败。要做好异常处理，并确保连接在使用后正确关闭。

    ```python
    import sqlite3

    try:
        conn = sqlite3.connect('example.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()
    ```

1. 使用事务确保数据一致性

    在执行多个数据库操作时，使用事务可以确保数据的一致性和完整性。如果任何操作失败，可以回滚整个事务。

    ```python
    import sqlite3

    conn = sqlite3.connect('example.db')
    try:
        conn.execute('BEGIN')
        conn.execute('INSERT INTO users (name) VALUES (?)', ('Alice',))
        conn.execute('INSERT INTO users (name) VALUES (?)', ('Bob',))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Transaction failed: {e}")
    finally:
        conn.close()
    ```

1. 优化查询性能

    在处理大量数据时，优化查询性能非常重要。可以通过以下方法提高性能：

    - **索引**：为经常查询的列创建索引。
    - **批量操作**：使用批量插入或更新，减少数据库交互次数。
    - **查询优化**：使用适当的查询语句，避免不必要的全表扫描。

    ```python
    # 创建索引
    cursor.execute('CREATE INDEX idx_name ON users (name)')
    ```

1. 避免 SQL 注入攻击

    在 Python 编程中，SQL 注入攻击是一个严重的安全问题，可能导致数据库泄露或损坏。  
    SQL 注入通常是由于在拼接 SQL 语句时直接使用用户输入的数据而引发的。

1. 使用参数化查询

    参数化查询是防止 SQL 注入的有效方法。大多数数据库库都支持参数化查询，通过将用户输入作为参数传递给查询而不是直接拼接字符串，可以确保数据被正确转义。

    ```python
    # Bad Case：直接拼接用户输入
    import pymysql

    def get_user_bad(user_id):
        conn = pymysql.connect(host='localhost', user='user', password='passwd', db='example_db')
        cursor = conn.cursor()
        
        # Bad Case: 直接拼接用户输入
        sql = f"SELECT * FROM users WHERE id = {user_id}"
        cursor.execute(sql)
        user = cursor.fetchone()
        
        conn.close()
        return user

    # 用户输入
    user_input = "1 OR 1=1"
    print(get_user_bad(user_input))

    # Good Case：使用参数化查询
    import pymysql

    def get_user_good(user_id):
        conn = pymysql.connect(host='localhost', user='user', password='passwd', db='example_db')
        cursor = conn.cursor()
        
        # Good Case: 使用参数化查询
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        
        conn.close()
        return user

    # 用户输入
    user_input = "1 OR 1=1"
    print(get_user_good(user_input))
    ```

1. 使用 ORM 框架

    ORM 框架（如 SQLAlchemy 和 Django ORM）通常会自动处理参数化查询，从而减少 SQL 注入的风险。使用 ORM 框架可以简化数据库操作并提高安全性。

    ```python
    # 使用 SQLAlchemy ORM 避免 SQL 注入
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine('sqlite:///example.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    user_id = 1
    user = session.query(User).filter_by(id=user_id).first()
    ```

    ```python
    # 使用 sqlalchemy 的 raw execute
    # 定义参数化查询
    query = text("SELECT * FROM users WHERE id = :user_id")

    # 执行查询并传递参数
    user_id = 1
    result = session.execute(query, {'user_id': user_id})
    ```

1. 避免动态生成 SQL 语句

    尽量避免根据用户输入动态生成 SQL 语句，尤其是包含用户输入的部分。动态生成的 SQL 语句容易引发 SQL 注入攻击。

    ```python
    # 不推荐的做法：动态拼接 SQL 语句
    user_id = "1 OR 1=1"
    sql = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(sql)  # 存在 SQL 注入风险
    ```

1. 验证和清理用户输入

    虽然参数化查询是防止 SQL 注入的主要手段，但对用户输入进行验证和清理也是一个良好的习惯。确保输入数据的格式和内容符合预期，可以减少潜在的安全风险。

    ```python
    # 验证用户输入
    user_id = input("Enter user ID: ")
    if not user_id.isdigit():
        raise ValueError("Invalid user ID")
    ```

1. 最小权限原则

    数据库用户应遵循最小权限原则，即只授予完成所需操作的最低权限。  
    即使发生 SQL 注入攻击，也可以将其影响降到最低。

## 安全

在现代软件开发中，安全性是一个至关重要的方面。  
加密算法、散列、签名和秘钥管理是安全性的重要组成部分。

### 加密算法

- 在选择加密算法时，优先选择经过广泛验证并且推荐的标准算法，如 AES（高级加密标准）。
- 避免使用自定义或过时的加密算法，因为它们可能存在未发现的漏洞。
- 使用库时，确保它们是最新版本，以包含最新的安全修补和改进。

```python
# 使用 pycryptodome 进行 AES 加密示例
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# 生成随机密钥
key = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_EAX)

# 加密数据
data = b'Secret data'
nonce = cipher.nonce
ciphertext, tag = cipher.encrypt_and_digest(data)

# 解密数据
cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
plaintext = cipher.decrypt(ciphertext)
print(plaintext)  # 输出: b'Secret data'
```

### 哈希函数

- 哈希函数用于生成数据的唯一固定长度表示，常用于数据完整性校验和密码存储。
- 使用安全的散列算法，如 SHA-256 或更高版本，避免使用 MD5 或 SHA-1 等已知不安全的算法。
- 对于密码存储，使用专门的密码散列算法，如 bcrypt 或 scrypt。

```python
# 使用 hashlib 进行 SHA-256 散列示例
import hashlib

data = b"important data"
hash_object = hashlib.sha256(data)
hex_dig = hash_object.hexdigest()
print(hex_dig)  # 输出: 数据的 SHA-256 散列值
```

### 数字签名

- 数字签名用于验证数据的真实性和完整性，常用于安全通信和身份验证。
- 使用非对称加密算法（如 RSA 或 ECDSA）生成和验证数字签名。
- 确保私钥的安全存储和管理，避免泄露。

```python
# 使用 pycryptodome 进行 RSA 签名示例
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

# 生成 RSA 密钥对
key = RSA.generate(2048)
private_key = key.export_key()
public_key = key.publickey().export_key()

# 生成数据散列
data = b"message to sign"
hash_object = SHA256.new(data)

# 签名数据
signature = pkcs1_15.new(key).sign(hash_object)

# 验证签名
try:
    pkcs1_15.new(key.publickey()).verify(hash_object, signature)
    print("签名验证成功")
except (ValueError, TypeError):
    print("签名验证失败")
```

### 密钥管理

- 安全的秘钥管理是确保加密系统安全的基础。
- 避免硬编码秘钥在代码中，使用环境变量或安全的秘钥管理服务（如公司内的[七彩石](https://rainbow.woa.com/)）。
- 定期轮换秘钥，并确保旧秘钥的安全销毁。

```python
# 使用环境变量管理秘钥示例
import os

# 从环境变量获取密钥
encryption_key = os.getenv("ENCRYPTION_KEY")
if encryption_key is None:
    raise ValueError("未找到加密密钥")

# 使用密钥进行加密操作
# 示例代码见加密算法部分
```
