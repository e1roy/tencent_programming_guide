# Varargs 变长参数

## tl;dr

- 通过提供额外参数强制最小数量，而不要依赖运行时检查。

变长参数是 `Java` 的语法糖，允许在调用方法时传入不定数量的参数（包括零个）。其语法为在参数类型后添加省略号（...），在方法内部，变长参数被当作数组处理。

```java
// 变长参数示例：可以传入任意数量的int参数（包括0个）
public void printNumbers(int... numbers) {
    for (int num : numbers) {
        System.out.println(num);
    }
}
```

## 输入安全：强制最小参数数量

变长参数允许传入零个参数，但某些方法要求至少一个参数。如果仅依赖运行时检查参数数量，会导致潜在的错误只能在运行时被发现，而非编译时。

### 反例：运行时检查参数数量
```java
// Bad: 依赖运行时检查最小参数数量
public void input(int... args) {
    if (args.length == 0) { // 运行时检查
        throw new IllegalArgumentException("至少需要一个参数");
    }
    // ...
}

// 调用input变长参数方法
input(); // 正常编译，但运行时抛出IllegalArgumentException
```
这种方法的问题在于，调用方可能传入零个参数，而编译器不会报错，直到运行时才抛出异常。


### 正例：编译时强制最小参数数量
```java
// Good: 编译时强制至少一个参数
public void input(int firstArg, int... remainingArgs) {
    // 不再需要检查参数数量，因为firstArg是必需的
    // 使用firstArg和remainingArgs数组...
}

// 调用input变长参数方法
input();  // 编译出错
```
声明一个必需的参数，后跟变长参数。这样，调用方必须至少提供一个参数（满足必需参数），从而在编译时保证最小数量。


## 扩展阅读

- Effective Java Item 53: Use varargs judiciously
