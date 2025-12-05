# String Concatenation 字符串拼接

## tl;dr

- 字符串拼接方式选择原则：优先可读性与正确性。
- 简单拼接少量字符串（尤其非循环内）优先使用 `+`，需要格式化时用 `String.format`；
- 在循环内或动态构建大量字符串时必须使用 `StringBuilder`；
- 优先使用 `String.join` 拼接带分隔符的集合；
- 避免使用 `StringBuffer`，其线程安全通常无实际意义且性能较差。

## Java 格式化字符串的方式

- `+` 操作符，即朴素拼接
- [`String.format`](https://docs.oracle.com/javase/7/docs/api/java/lang/String.html#format)及其它类似的字符串格式化方法
- `StringBuilder`，`Builder `模式的可变的字符串构造器
- `StringBuffer`，类似于 `StringBuilder` 但是 `StringBuffer` 线程安全
- `String.join` 支持使用插入自字义分割符的拼接

## 优先可读性和正确性，除非性能是瓶颈

由于 `Java string` 不可变，因此 `+` 操作每次都会生成一个新的字符串。所以一个常见的性能陷阱是使用 `+` 进行海量字符串的连续拼接。这会导致` O(n^2)` 的时间复杂度。
但是，这只有在循环内出现时才会造成显著的时间损耗。通常情况下，代码内的手动拼接字符串，如少于 8 个子串，使用 `+` 的额外损耗是不显著的，遑论编译器可能优化。

大的原则：**如果不在循环中拼接字符串，不要过分担心性能。** 关注以下方面：

- 可读性：即哪种形式在代码中的字符串更容易被读懂。
- 正确性：字符串格式化的结果是否会导致正确性/安全问题，如对 `HTML` 的安全化处理。


## 简单情况：优先使用 `+`

拼接少量字符串时优先使用 `+` 操作符。即使多个字符串的拼接，使用 `+` 如果更清晰也可以使用，编译器会做拼接的优化：

```java
// Good:
String info = "projectId: " + id;
String msg = "userId: " + id + " userName: " + name;
```

## 在需要格式化的情况下，选择 `String.format`

当建立一个带有格式化的复杂字符串时，更倾向于使用 `String.format`。使用大量的 `+` 可能会使该字符串格式化很难读懂。

### 反例
```java
// Bad: " 和 [ ] 等字符混在一起，很难看出来的结果长什么样。
String bad = src + " [" + qos + ":" + mtu + "]-> " + dst;
```

### 正例
```java
// Good:
String str = String.format("%s [%s:%d]-> %s", src, qos, mtu, dst)
```


## 循环内或动态构建大量字符串：使用 `StringBuilder`

在循环体内拼接字符串，或者需要动态地、分步骤地构建一个长字符串时，必须使用 `StringBuilder`。它的可变特性避免了 `+` 在循环中带来的` O(n²)` 性能问题，其均摊时间复杂度为 `O(n)`。

```java
// Good: 在循环内拼接，使用 StringBuilder 是必须的
StringBuilder htmlBuilder = new StringBuilder("<ul>");
for (String item : items) {
    htmlBuilder.append("<li>").append(item).append("</li>");
}
htmlBuilder.append("</ul>");
String html = htmlBuilder.toString();
```


## 拼接带分隔符的集合：优先使用 String.join
`String.join` 可以将一系列字符串通过分隔符拼接在一起，在合适的场合优先使用。例如：

```java
// Good: 使用 String.join 拼接带分隔符的集合
List<String> results = List.of("Alice", "Bob", "Charlie");
String joinedNames = String.join(", ", names); // 结果: "Alice, Bob, Charlie"
```


## 避免使用 StringBuffer

使用 `StringBuilder`。在并发场景下，使用 `StringBuilder` 以及额外的并发语义控制写入顺序和安全性。

`StringBuffer` 是典型的过度设计。一个线程安全的 `StringBuffer` 虽然保证了线程可见性，保证并发写入是安全的，但是谁来保证不同线程写入的顺序呢？结果还是需要不同线程通过锁机制来控制写入顺序，这使得 `StringBuffer` 的线程安全性在绝大多数情况下没有意义。

这是一个很有用的教训：**不要提供过细粒度的线程安全，锁不是越细粒度越好。** 通常情况下，在同一个类中，有多个粒度的锁往往不会增加性能。

## 扩展阅读

- Effective Java Item 63: Beware the performance of string concatenation
