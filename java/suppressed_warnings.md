# Suppressed Warnings 静默警告

## tl;dr

- 不要在编译选项中忽略警告
- 如果必须要忽略警告，使用 `@SuppressWarnings` 而不要无视编译器警告

## 静默警告

编译器的警告作为静态分析通常很有用，它可以帮助我们找出潜在的错误。你不应该忽略编译器警告，甚至应该考虑将特定类型的编译器警告级别调整为 ERROR，即阻碍编译。例如，`unchecked` 通常是不安全的，不应该通过编译。

但是，编译器可能会误报。当编译器误报，我们可以通过使用 `@SuppressWarnings` 注解来抑制对应类型的编译器警告。例如：`@SuppresseWarnings(value="unchecked")` 会忽略所有的未通过 Type Checking 的泛型转换警告。

需要注意的是，如果对一个类进行了静默警告的标注，那么在该类内的所有方法和成员触发的对应警告都会被编译器忽略。因此，最佳实践是只在最细粒度的方法或成员上进行标注，而不是在类上进行标注。这样能更好地指导我们发现和修复代码中的潜在问题。

https://docs.oracle.com/javase/11/docs/api/java/lang/SuppressWarnings.html

## 常见静默警告

### 标准类型

Java SE 预定义的标准警告类型有四种：

- “unchecked”：消除未经过` Type Checking `的强制类型转换警告。

```java
@SuppressWarnings("unchecked")
List<String> myList = (List<String>) getObject();
```

- “deprecation”：表示程序使用了已经废弃的方法、类、字段等。

```java
@SuppressWarnings("deprecation")
Date date = new Date(2020, 1, 1);
```

- "removal": 表示已经被 `deprecated` 的、最终将被移除的 API。

- "preview": `Java SE` 专用，表示已定义的、已实现的、但尚未定型的功能。

### 非标准类型

其它的非标准的、与具体编译器相关的常见警告有：

- “rawtypes”：用于泛型未定义时产生的警告。

```java
@SuppressWarnings("rawtypes")
List myList = new ArrayList();
```

- “fallthrough”：表示在`switch`语句中，每个`case`缺少`break`语句。

```java
@SuppressWarnings("fallthrough")
switch (num) {
  case 1:
    System.out.println("Number is 1");
  case 2:
    System.out.println("Number is 2");
    break;
  default:
    System.out.println("Number is not 1 or 2");
    break;
}
```

- “unused”：表示代码中定义的变量、方法或类没有被使用。

```java
@SuppressWarnings("unused")
private void method() {
  int i = 0;
  System.out.println("This is a method");
}
```

## 扩展阅读

- [StackOverflow - List of valid suppresswarnings](https://stackoverflow.com/questions/1205995/what-is-the-list-of-valid-suppresswarnings-warning-names-in-java)
- [Java Language Specification Java SE 20 9.6.4.5 SuppressWarnings](https://docs.oracle.com/javase/specs/jls/se11/jls11.pdf)
