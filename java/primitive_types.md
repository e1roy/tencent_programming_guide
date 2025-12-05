# Primitive Types 原始类型

## tl;dr

- 避免原始类型狂热（Primitive Obsession）
- 比起装箱（Boxed）类型，优先使用原始（未装箱）类型
- 高性能要求场景，要考虑装箱拆箱的性能损耗
- 如果必须使用装箱类，必须注意判空

## 避免原始类型狂热

原始类型狂热是指过度依赖原始类型（如`int`、`boolean`等）来表示业务概念，而不是使用更具表达力的对象。

### 反例

```java
// 反例：原始类型，缺乏业务语义
int userId;
```

### 正例

```java
// 正例：使用有语义的类
class UserId {
    private final int value;
    public UserId(int value) { this.value = value; }
    public int getValue() { return value; }
}
```

## 优先使用未装箱类型

未装箱类型（如`int`、`double`）在性能上优于装箱类型（如`Integer`、`Double`），尤其是在大量计算或高频调用的场景中。

### 反例

```java
// 反例：自动装箱/拆箱导致性能损耗
Integer sum = 0;
for (int i = 0; i < 10000; i++) {
    sum += i; // 自动装箱/拆箱导致性能损耗
}
```

### 正例

```java
// 正例：直接使用原始类型，性能更优
int sum = 0;
for (int i = 0; i < 10000; i++) {
    sum += i; // 直接使用原始类型，性能更优
}
```

## 装箱类型的安全性

装箱类型是可空的，使用时要注意空指针问题，一定要判空

### 反例

```java
// 反例：会在运行时抛出空指针异常
public Float calculatePrice(Float originPrice) {
    return originPrice * 0.5f;
}
calculatePrice(null); // 会在运行时抛出空指针异常
```

### 正例

```java
// 正例1：一种做法是要判空
public Float calculatePrice(Float originPrice) {
    if (originPrice == null) {
        return 0;
    }
    return originPrice * 0.5f;
}
calculatePrice(null); // 运行时虽然不会报错，但是null返回0，这个在业务逻辑层面未必合理，存在争议；这个做法也并非最佳

// 正例2：更好的做法，是不要用无意义的包装类，使用基础类型
public float calculatePrice(float originPrice) {
    return originPrice * 0.5f;
}
calculatePrice(null); // 会在编译时报错，参数类型不对
```

## 装箱类型的比较

永远使用 `equals` 来比较 `Integer` 等装箱类型，而不应该使用 `==`。

### 反例

```java
// 反例：比较的是引用而非值，这个if返回的是false
Integer a = 1000;
Integer b = 1000;
if (a == b) { // 错误：比较的是引用而非值，这个if返回的是false
    System.out.println("Equal");
}
```

### 正例

```java
// 正例：比较的是值，这个if返回的是true
Integer a = 1000;
Integer b = 1000;
if (a.equals(b)) { // 正确：比较的是值，这个if返回的是true
    System.out.println("Equal");
}
```

## 实际业务场景选择指南

### 何时使用原始类型

原始类型适用于以下场景：

**1. 数学计算和算法**

```java
// 正例：数学计算使用原始类型
public class Calculator {
    public double calculateCompoundInterest(double principal, double rate, int years) {
        return principal * Math.pow(1 + rate, years); // 使用double原始类型
    }

    public int fibonacci(int n) {
        if (n <= 1) return n;
        return fibonacci(n - 1) + fibonacci(n - 2); // 使用int原始类型
    }
}
```

**2. 循环计数器**

```java
// 正例：循环计数器使用原始类型
public void processItems(List<String> items) {
    for (int i = 0; i < items.size(); i++) { // 使用int原始类型
        System.out.println("Processing item " + i + ": " + items.get(i));
    }
}
```

**3. 配置参数和标志位**

```java
// 正例：配置参数使用原始类型
public class DatabaseConfig {
    private final int maxConnections; // 使用int原始类型
    private final long timeoutMillis; // 使用long原始类型
    private final boolean enableLogging; // 使用boolean原始类型

    public DatabaseConfig(int maxConnections, long timeoutMillis, boolean enableLogging) {
        this.maxConnections = maxConnections;
        this.timeoutMillis = timeoutMillis;
        this.enableLogging = enableLogging;
    }
}
```

### 何时使用装箱类型

装箱类型适用于以下场景：

**1. 集合中的元素**

```java
// 正例：集合中必须使用装箱类型
public class StudentService {
    private final Map<String, Integer> studentScores = new HashMap<>(); // Integer装箱类型

    public void addScore(String studentId, Integer score) {
        studentScores.put(studentId, score); // 集合中必须使用装箱类型
    }

    public List<Integer> getAllScores() {
        return new ArrayList<>(studentScores.values()); // 返回List<Integer>
    }
}
```

**2. 可选的数值参数**

```java
// 正例：可选参数使用装箱类型
public class UserService {
    public void updateUser(String userId, String name, Integer age, Boolean isActive) {
        // age和isActive可能为null，表示不更新该字段
        if (age != null) {
            // 更新年龄
        }
        if (isActive != null) {
            // 更新状态
        }
    }
}
```

**3. 与外部 API 交互**

```java
// 正例：与外部API交互使用装箱类型
public class ApiClient {
    public void sendData(String endpoint, Integer userId, Double amount, Boolean isUrgent) {
        Map<String, Object> payload = new HashMap<>();
        payload.put("userId", userId); // 可能为null
        payload.put("amount", amount); // 可能为null
        payload.put("isUrgent", isUrgent); // 可能为null

        // 发送到外部API
    }
}
```

## 自动装箱/拆箱陷阱

### 陷阱 1：性能问题

```java
// 反例：自动装箱导致的性能问题
public class PerformanceTrap {
    public void badExample() {
        Long sum = 0L; // 装箱类型
        for (long i = 0; i < 1000000; i++) {
            sum += i; // 每次循环都进行装箱/拆箱操作
        }
    }

    // 正例：使用原始类型避免装箱/拆箱
    public void goodExample() {
        long sum = 0L; // 原始类型
        for (long i = 0; i < 1000000; i++) {
            sum += i; // 直接使用原始类型，无装箱/拆箱开销
        }
    }
}
```

### 陷阱 2：空指针异常

```java
// 反例：自动装箱导致的空指针异常
public class NullPointerTrap {
    public void badExample() {
        Integer count = getCount(); // 可能返回null
        int result = count + 1; // 如果count为null，会抛出NPE
    }

    // 正例：安全处理装箱类型
    public void goodExample() {
        Integer count = getCount();
        if (count != null) {
            int result = count + 1; // 安全拆箱
        } else {
            // 处理null情况
            int result = 0;
        }
    }

    private Integer getCount() {
        return null; // 模拟可能返回null的情况
    }
}
```

### 陷阱 3：集合操作中的陷阱

```java
// 反例：集合操作中的自动装箱陷阱
public class CollectionTrap {
    public void badExample() {
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);

        // 错误：使用原始类型比较装箱类型
        numbers.remove(1); // 移除索引1的元素，不是移除值为1的元素
        System.out.println(numbers); // 输出：[1, 3, 4, 5]
    }

    // 正例：正确使用装箱类型
    public void goodExample() {
        List<Integer> numbers = new ArrayList<>(Arrays.asList(1, 2, 3, 4, 5));

        // 正确：移除值为1的元素
        numbers.remove(Integer.valueOf(1)); // 移除值为1的元素
        System.out.println(numbers); // 输出：[2, 3, 4, 5]
    }
}
```

### 陷阱 4：条件判断中的陷阱

```java
// 反例：条件判断中的自动装箱陷阱
public class ConditionTrap {
    public void badExample() {
        Integer value = getValue();

        // 错误：可能抛出NPE
        if (value > 0) { // 如果value为null，会抛出NPE
            System.out.println("Positive");
        }
    }

    // 正例：安全的条件判断
    public void goodExample() {
        Integer value = getValue();

        // 正确：先判空再比较
        if (value != null && value > 0) {
            System.out.println("Positive");
        } else if (value != null && value <= 0) {
            System.out.println("Non-positive");
        } else {
            System.out.println("Value is null");
        }
    }

    private Integer getValue() {
        return null; // 模拟可能返回null的情况
    }
}
```

### 陷阱 5：方法重载中的陷阱

```java
// 反例：方法重载中的自动装箱陷阱
public class OverloadTrap {
    public void process(int value) {
        System.out.println("Processing int: " + value);
    }

    public void process(Integer value) {
        System.out.println("Processing Integer: " + value);
    }

    public void badExample() {
        process(1); // 调用process(int)
        process(Integer.valueOf(1)); // 调用process(Integer)

        Integer boxed = 1;
        process(boxed); // 调用process(Integer)，不是process(int)
    }

    // 正例：明确指定类型
    public void goodExample() {
        int primitive = 1;
        Integer boxed = Integer.valueOf(1);

        process(primitive); // 明确调用process(int)
        process(boxed); // 明确调用process(Integer)
    }
}
```

## 扩展阅读
- Effective Java Item 61: Prefer primitive types to boxed primitives
- Effective Java Item 62: Avoid strings where other types are more appropriate
- 《Java 编程思想》第 4 章：操作符与控制流
- 《代码整洁之道》第 6 章：对象和数据结构
