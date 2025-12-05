# Lambdas 表达式

## tl;dr

- 比起匿名类，优先使用 Lambda 表达式
- 比起 Lambda，优先使用 Method Reference

## Method Reference > Lambda > 匿名类

JDK 8 引入了 Method Reference 和 Lambda  用以实现函数是一等成员。

Method Reference 优于 Lambda 表达式。 Method Reference 有以下几种形式：

- Static: `Integer::parseInt`
- Bound: `Instant.now()::isAfter`
- Unbound: `String::toLowerCase`
- Class constructor: `TreeMap<K, V>::new`
- Array constructor: `int[]::new`

Lambda 全面优于匿名类，除非 Lambda 不支持的场合，如 Lambda 只能实现 Functional Interface。

下面是采用这三个方法对 Collection 的字符串长度进行排序的例子：

```java
// 匿名类作为一个函数对象
Collections.sort(words, new Comparator<String>() {
    public int compare(String s1, String s2) {
        return Integer.compare(s1.length(), s2.length());
    }
});

// Lambda 表达式作为一个函数对象，替换匿名类
Collections.sort(words,
        (s1, s2) -> Integer.compare(s1.length(), s2.length()));

// 采用 Method reference, 替换 lambda.
Collections.sort(words, comparingInt(String::length));
```

## Lambda 注意事项

- Lambda 的最大建议长度是 **3** 行。超过 3 行就会影响可读性，考虑抽象成一个私有方法。
- Lambda 不应该被**序列化**。和匿名类一样。

## Lambda 表达式最佳实践

### 类型推断和简化

```java
// ✅ 利用类型推断
List<String> names = Arrays.asList("Alice", "Bob", "Charlie");

// 好：简洁明了
names.stream()
     .filter(name -> name.length() > 3)
     .map(String::toUpperCase)
     .forEach(System.out::println);

// ❌ 避免：不必要的类型声明
names.stream()
     .filter((String name) -> name.length() > 3)
     .map((String name) -> name.toUpperCase())
     .forEach((String name) -> System.out.println(name));
```

### 复杂 Lambda 的重构

```java
public class OrderProcessor {
    // ❌ 避免：过长的 Lambda
    public void badExample(List<Order> orders) {
        orders.stream()
              .filter(order -> {
                  if (order.getStatus() == OrderStatus.PENDING) {
                      BigDecimal total = order.getItems().stream()
                                             .map(item -> item.getPrice().multiply(
                                                 BigDecimal.valueOf(item.getQuantity())))
                                             .reduce(BigDecimal.ZERO, BigDecimal::add);
                      return total.compareTo(new BigDecimal("100")) > 0;
                  }
                  return false;
              })
              .forEach(this::processOrder);
    }
    
    // ✅ 好：提取为私有方法
    public void goodExample(List<Order> orders) {
        orders.stream()
              .filter(this::isPendingLargeOrder)
              .forEach(this::processOrder);
    }
    
    private boolean isPendingLargeOrder(Order order) {
        if (order.getStatus() != OrderStatus.PENDING) {
            return false;
        }
        
        BigDecimal total = calculateOrderTotal(order);
        return total.compareTo(new BigDecimal("100")) > 0;
    }
    
    private BigDecimal calculateOrderTotal(Order order) {
        return order.getItems().stream()
                   .map(this::calculateItemTotal)
                   .reduce(BigDecimal.ZERO, BigDecimal::add);
    }
    
    private BigDecimal calculateItemTotal(OrderItem item) {
        return item.getPrice().multiply(BigDecimal.valueOf(item.getQuantity()));
    }
}
```

### 方法引用的各种形式

```java
public class MethodReferenceExamples {
    public void demonstrateMethodReferences() {
        List<String> strings = Arrays.asList("apple", "banana", "cherry");
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
        
        // 1. 静态方法引用
        numbers.stream()
               .map(String::valueOf)  // 等价于 n -> String.valueOf(n)
               .collect(Collectors.toList());
        
        // 2. 实例方法引用（绑定）
        String prefix = "Item: ";
        strings.stream()
               .map(prefix::concat)   // 等价于 s -> prefix.concat(s)
               .collect(Collectors.toList());
        
        // 3. 实例方法引用（未绑定）
        strings.stream()
               .map(String::toUpperCase)  // 等价于 s -> s.toUpperCase()
               .collect(Collectors.toList());
        
        // 4. 构造函数引用
        strings.stream()
               .map(StringBuilder::new)   // 等价于 s -> new StringBuilder(s)
               .collect(Collectors.toList());
        
        // 5. 数组构造函数引用
        String[] array = strings.stream()
                               .toArray(String[]::new);  // 等价于 size -> new String[size]
    }
}
```

### Lambda 与异常处理

```java
public class LambdaExceptionHandling {
    // 包装受检异常的工具方法
    @FunctionalInterface
    public interface ThrowingFunction<T, R> {
        R apply(T t) throws Exception;
    }
    
    public static <T, R> Function<T, R> unchecked(ThrowingFunction<T, R> f) {
        return t -> {
            try {
                return f.apply(t);
            } catch (Exception e) {
                throw new RuntimeException(e);
            }
        };
    }
    
    // 使用示例
    public void processFiles(List<String> filenames) {
        List<String> contents = filenames.stream()
                                        .map(unchecked(this::readFile))
                                        .collect(Collectors.toList());
    }
    
    private String readFile(String filename) throws IOException {
        return Files.readString(Paths.get(filename));
    }
    
    // 或者使用 Optional 处理异常
    public Optional<String> safeReadFile(String filename) {
        try {
            return Optional.of(Files.readString(Paths.get(filename)));
        } catch (IOException e) {
            return Optional.empty();
        }
    }
    
    public void processFilesWithOptional(List<String> filenames) {
        List<String> contents = filenames.stream()
                                        .map(this::safeReadFile)
                                        .filter(Optional::isPresent)
                                        .map(Optional::get)
                                        .collect(Collectors.toList());
    }
}
```

### Lambda 表达式的性能考虑

```java
public class LambdaPerformance {
    private static final Predicate<String> IS_NOT_EMPTY = s -> !s.isEmpty();
    private static final Function<String, String> TO_UPPER = String::toUpperCase;
    
    // ✅ 好：重用 Lambda 表达式
    public List<String> processStrings(List<String> strings) {
        return strings.stream()
                     .filter(IS_NOT_EMPTY)
                     .map(TO_UPPER)
                     .collect(Collectors.toList());
    }
    
    // ❌ 避免：在循环中创建 Lambda
    public void badPerformance(List<List<String>> listOfLists) {
        for (List<String> list : listOfLists) {
            // 每次循环都创建新的 Lambda 对象
            list.stream()
                .filter(s -> !s.isEmpty())  // 应该提取为常量
                .forEach(System.out::println);
        }
    }
    
    // ✅ 好：提取为常量或方法引用
    public void goodPerformance(List<List<String>> listOfLists) {
        for (List<String> list : listOfLists) {
            list.stream()
                .filter(IS_NOT_EMPTY)
                .forEach(System.out::println);
        }
    }
}
```

### 函数式接口的自定义

```java
@FunctionalInterface
public interface TriFunction<T, U, V, R> {
    R apply(T t, U u, V v);
    
    // 可以有默认方法
    default <W> TriFunction<T, U, V, W> andThen(Function<? super R, ? extends W> after) {
        Objects.requireNonNull(after);
        return (T t, U u, V v) -> after.apply(apply(t, u, v));
    }
}

// 使用示例
public class CustomFunctionalInterface {
    public void demonstrateTriFunction() {
        TriFunction<String, String, String, String> concat3 = 
            (a, b, c) -> a + b + c;
        
        String result = concat3.apply("Hello", " ", "World");
        System.out.println(result); // "Hello World"
        
        // 使用 andThen
        TriFunction<String, String, String, String> concat3AndUpper = 
            concat3.andThen(String::toUpperCase);
        
        String upperResult = concat3AndUpper.apply("hello", " ", "world");
        System.out.println(upperResult); // "HELLO WORLD"
    }
}
```

## Lambda 使用指南

1. **优先级**：方法引用 > Lambda > 匿名类
2. **长度限制**：Lambda 表达式最好不超过 3 行
3. **类型推断**：让编译器推断类型，避免显式声明
4. **异常处理**：使用工具方法包装受检异常
5. **性能优化**：重用 Lambda 表达式，避免在循环中创建

## 扩展阅读

- Effective Java Item 42: Prefer lambdas to anonymous classes
- Effective Java Item 43: Prefer method references to lambdas
- [Java Lambda 表达式教程](https://docs.oracle.com/javase/tutorial/java/javaOO/lambdaexpressions.html)
