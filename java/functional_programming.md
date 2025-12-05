# Functional Programming 函数式编程

## tl;dr

- 优先使用 [lambda](lambdas.md)。
- 使用 [stream](stream.md)，如果它们能让你的代码变得更可读。 否则，使用“朴素”的写法。
- 优先使用标准库的**函数式接口(functional interface)**。

## 不要使用函数式编程降低圈复杂度

某友商的[一篇关于优化圈复杂度的文章](https://zhuanlan.zhihu.com/p/555275693)里有这样一个（正面）例子：

```java
//修改前
List list = XXX;
if (!CollectionUtils.isEmpty(list)) {
    for (XX item : list) {
        if (item == null) {
            return;
        } else {
        // 逻辑a
        }
    }
}
 
//修改后
List list = XX;
list = Optional.ofNullable(list).orElse(new ArrayList<>());
list.stream().filter(Objects::nonNull).forEach(item -> {
    //逻辑a
});
```

**不要这样做。** 圈复杂度不是代码可读性的全部。朴素地编写会好得多：

```java
List<T> list = XXX;
// 注意到 For-loop 之前的判空是没有必要的，可以省略
for (T item : list) {
    if (item == null) {
        return;
    }
    // 逻辑a
}
```

## 标准函数式接口

比起自定义的函数式接口，优先使用标准函数式接口。

| Interface | Function Signature | Example |
| ------ | ------ | ------ |
| `UnaryOperator<T>` | `T apply(T t)` | `String::toLowerCase` |
| `BinaryOperator<T>` | `T apply(T t1, T, t2)` | `BigInteger::add` |
| `Predicate<T>` | `boolean test(T t)` | `Collection::isEmpty` |
| `Function<T, R>` | `R apply(T t)` | `Arrays::asList` |
| `Supplier<T>` | `T get()` | `Instant::now()` |
| `Consumer<T>` | `void accept(T t)` | `System.out::println` |

如果有自定义的函数式接口，应该添加 `@FunctionalInterface` 注解。

## 函数式编程实践

### 不可变性和纯函数

```java
// ✅ 纯函数：无副作用，相同输入总是产生相同输出
public class MathUtils {
    public static int add(int a, int b) {
        return a + b;
    }
    
    public static List<String> toUpperCase(List<String> strings) {
        return strings.stream()
                     .map(String::toUpperCase)
                     .collect(Collectors.toList());
    }
}

// ❌ 有副作用的函数
public class BadExample {
    private int counter = 0;
    
    public int increment() {
        return ++counter; // 修改了外部状态
    }
}
```

### 高阶函数的使用

```java
public class OrderProcessor {
    // 接受函数作为参数
    public List<Order> filterOrders(List<Order> orders, Predicate<Order> filter) {
        return orders.stream()
                    .filter(filter)
                    .collect(Collectors.toList());
    }
    
    // 返回函数
    public Function<Order, BigDecimal> createTaxCalculator(BigDecimal taxRate) {
        return order -> order.getAmount().multiply(taxRate);
    }
    
    // 使用示例
    public void processOrders() {
        List<Order> orders = getOrders();
        
        // 使用方法引用
        List<Order> paidOrders = filterOrders(orders, Order::isPaid);
        
        // 使用lambda表达式
        List<Order> largeOrders = filterOrders(orders, 
            order -> order.getAmount().compareTo(new BigDecimal("1000")) > 0);
        
        // 使用返回的函数
        Function<Order, BigDecimal> taxCalculator = createTaxCalculator(new BigDecimal("0.1"));
        BigDecimal totalTax = orders.stream()
                                   .map(taxCalculator)
                                   .reduce(BigDecimal.ZERO, BigDecimal::add);
    }
}
```

### 函数组合

```java
public class DataProcessor {
    // 基础函数
    private static final Function<String, String> trim = String::trim;
    private static final Function<String, String> toLowerCase = String::toLowerCase;
    private static final Predicate<String> isNotEmpty = s -> !s.isEmpty();
    
    // 函数组合
    public List<String> processStrings(List<String> strings) {
        Function<String, String> processor = trim.andThen(toLowerCase);
        
        return strings.stream()
                     .map(processor)
                     .filter(isNotEmpty)
                     .collect(Collectors.toList());
    }
    
    // 复杂的函数组合
    public Function<User, String> createUserDisplayName() {
        return user -> Optional.ofNullable(user.getFirstName())
                              .map(String::trim)
                              .filter(s -> !s.isEmpty())
                              .map(firstName -> firstName + " " + 
                                   Optional.ofNullable(user.getLastName())
                                          .orElse(""))
                              .orElse("Anonymous");
    }
}
```

### Optional 的函数式使用

```java
public class UserService {
    public Optional<User> findUserByEmail(String email) {
        return userRepository.findByEmail(email);
    }
    
    public String getUserDisplayName(String email) {
        return findUserByEmail(email)
                .map(User::getFullName)
                .filter(name -> !name.trim().isEmpty())
                .orElse("Unknown User");
    }
    
    public void processUser(String email) {
        findUserByEmail(email)
            .filter(User::isActive)
            .ifPresentOrElse(
                this::sendWelcomeEmail,
                () -> logger.warn("用户不存在或未激活: {}", email)
            );
    }
    
    private void sendWelcomeEmail(User user) {
        emailService.sendWelcome(user.getEmail());
    }
}
```

### 错误处理的函数式方法

```java
public class Result<T> {
    private final T value;
    private final Exception error;
    
    private Result(T value, Exception error) {
        this.value = value;
        this.error = error;
    }
    
    public static <T> Result<T> success(T value) {
        return new Result<>(value, null);
    }
    
    public static <T> Result<T> failure(Exception error) {
        return new Result<>(null, error);
    }
    
    public <U> Result<U> map(Function<T, U> mapper) {
        if (isSuccess()) {
            try {
                return success(mapper.apply(value));
            } catch (Exception e) {
                return failure(e);
            }
        }
        return failure(error);
    }
    
    public <U> Result<U> flatMap(Function<T, Result<U>> mapper) {
        if (isSuccess()) {
            try {
                return mapper.apply(value);
            } catch (Exception e) {
                return failure(e);
            }
        }
        return failure(error);
    }
    
    public boolean isSuccess() {
        return error == null;
    }
    
    public T orElse(T defaultValue) {
        return isSuccess() ? value : defaultValue;
    }
}

// 使用示例
public class FileProcessor {
    public Result<String> readFile(String filename) {
        try {
            String content = Files.readString(Paths.get(filename));
            return Result.success(content);
        } catch (IOException e) {
            return Result.failure(e);
        }
    }
    
    public Result<Integer> countLines(String content) {
        try {
            int lines = content.split("\n").length;
            return Result.success(lines);
        } catch (Exception e) {
            return Result.failure(e);
        }
    }
    
    public void processFile(String filename) {
        Result<Integer> result = readFile(filename)
                                   .flatMap(this::countLines);
        
        if (result.isSuccess()) {
            System.out.println("文件行数: " + result.orElse(0));
        } else {
            System.err.println("处理失败");
        }
    }
}
```

## 函数式编程原则

1. **不可变性**：优先使用不可变对象和数据结构
2. **纯函数**：函数应该没有副作用，相同输入产生相同输出
3. **函数组合**：通过组合简单函数构建复杂功能
4. **声明式编程**：描述"做什么"而不是"怎么做"
5. **延迟计算**：只在需要时才进行计算

## 扩展阅读

- Effective Java Item 44: Favor the use of standard functional interfaces
- [Java 8 函数式编程](https://www.oracle.com/technical-resources/articles/java/lambda.html)
- [Vavr - Java函数式编程库](https://www.vavr.io/)
