# Closing Resources 关闭资源

## tl;dr

- 优先使用`try-with-resources`来管理资源，使其可以正确关闭，避免资源泄漏。


日常开发中*开/关资源* 是一个常见的模式，即一个资源必须显式地 `open`（或创建） 后才能开始正确工作，并且在使用结束后必须显式地 `close`。

不同于 Go 语言中会专门安排一个 `defer` 关键字以便正确地关闭资源，Java 是通过 `try-with-resources` 语法实现。

## 优先使用`try-with-resources`进行资源管理
### 正例
```java
static String firstLineOfFile(String path) throws IOException {
    try (BufferedReader br = new BufferedReader(new FileReader(path))) {
        return br.readLine();
    } catch (IOException e) {
        // 处理异常代码
         ...
    }
```
`try-with-resources`  在结束时可以调用  `br.close()`， 保障资源会被正常关闭处理


## 对于无法直接使用 `try-with-resources`的场景，至少保障 `try-finally` 语句块的完整
### 正例
```java
static String firstLineOfFile(String path) throws IOException {
    BufferedReader br = new BufferedReader(new FileReader(path));
    try {
        return br.readLine();
    } catch (IOException e) {
        // 处理异常代码
        ...
    } finally {
        br.close();
}
```

## 使资源支持 try-with-resources
所有实现了 `AutoClosable` 的资源都可以使用 `try-with-resources`:
 https://docs.oracle.com/javase/11/docs/api/java/lang/AutoCloseable.html


## 扩展阅读
- https://docs.oracle.com/javase/tutorial/essential/exceptions/tryResourceClose.html
- Effective Java Item 9: Prefer try-with-resources to try-finally
- [Java Language Specification](https://docs.oracle.com/javase/specs/jls/se8/jls8.pdf) 14.20.3 `try-with-resources`
