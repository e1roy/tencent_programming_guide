# Constructors 构造函数

## tl;dr

- **职责单一**：构造函数只负责对象初始化，不执行复杂业务逻辑
- **简单构造函数优先**：当参数少于 4 个且逻辑简单时，使用标准构造函数
- **复杂构造函数的替代方案**：
  - 参数过多（4 个以上）→ 考虑使用建造者模式（`Builder`）
  - 构造可能失败 → 考虑使用工厂方法（`Factory` 工厂模式）
  - 构造昂贵或需要缓存 → 考虑使用静态工厂方法
- **构造函数的防御性设计**：
  - 工具类应使用私有构造函数
  - 避免构造函数调用可重写方法
- **依赖注入**：避免在构造函数中硬编码资源依赖
- **构造函数链**：使用 `this()` 调用避免重复代码


## 构造函数的职责边界

构造函数应该：

- ✅ 初始化对象的必要状态
- ✅ 验证参数的有效性
- ✅ 建立不变式（invariants）

构造函数不应该：

- ❌ 执行复杂的业务逻辑
- ❌ 调用可重写的方法
- ❌ 启动线程或进行网络调用
- ❌ 硬编码外部依赖

## 参数验证与异常处理

### 反例：缺少参数验证

```java
public class Person {
    private final String name;
    private final int age;

    public Person(String name, int age) {
        this.name = name;  // 可能为null，会在后续使用时抛出NPE
        this.age = age;    // 可能为负数，违反业务逻辑
    }
}
```

### 正例：构造函数中进行参数验证

```java
public class Person {
    private final String name;
    private final int age;

    public Person(String name, int age) {
        // 参数验证应该在构造函数开始时进行
        this.name = Objects.requireNonNull(name, "姓名不能为空");
        if (age < 0 || age > 150) {
            throw new IllegalArgumentException("年龄必须在0-150之间: " + age);
        }
        this.age = age;
    }
}
```


## 构造函数重载与参数设计

### 反例：重复的验证逻辑

```java
public class Rectangle {
    private final int width;
    private final int height;

    public Rectangle(int width, int height) {
        // 重复的验证逻辑
        if (width <= 0 || height <= 0) {
            throw new IllegalArgumentException("宽度和高度必须为正数");
        }
        this.width = width;
        this.height = height;
    }

    public Rectangle(int side) {
        // 重复的验证逻辑，且可能与主构造函数不一致
        if (side <= 0) {
            throw new IllegalArgumentException("边长必须为正数");
        }
        this.width = side;
        this.height = side;
    }
}
```

### 正例：合理的构造函数重载

```java
public class Rectangle {
    private final int width;
    private final int height;

    // 主构造函数
    public Rectangle(int width, int height) {
        if (width <= 0 || height <= 0) {
            throw new IllegalArgumentException("宽度和高度必须为正数");
        }
        this.width = width;
        this.height = height;
    }

    // 正方形的便利构造函数
    public Rectangle(int side) {
        this(side, side);  // 委托给主构造函数
    }

    // 默认构造函数
    public Rectangle() {
        this(1, 1);  // 委托给主构造函数，提供合理默认值
    }
}
```


## 避免在构造函数中调用可重写方法

### 反例：在构造函数中调用可重写方法

```java
public class Parent {
    public Parent() {
        doSomething();  // 危险：子类可能重写此方法
    }

    public void doSomething() {
        System.out.println("Parent doing something");
    }
}

public class Child extends Parent {
    private final String data;

    public Child() {
        super();  // 调用Parent构造函数
        this.data = "initialized";
    }

    @Override
    public void doSomething() {
        // 此时data还未初始化，可能导致NPE
        System.out.println("Child doing something with " + data.length());
    }
}
```

### 正例：使用私有方法或延迟初始化

```java
public class Parent {
    public Parent() {
        doSomethingInternal();  // 私有方法，不可重写
    }

    private void doSomethingInternal() {
        System.out.println("Parent doing something");
    }
}
```

## 复杂构造函数的替代方案

### 建造者模式（Builder Pattern）
适用于参数较多的情况
```java
public class HttpClient {
    private final String baseUrl;
    private final int timeout;
    private final int retryCount;
    private final boolean enableLogging;
    private final Map<String, String> defaultHeaders;

    // 私有构造函数
    private HttpClient(Builder builder) {
        this.baseUrl = Objects.requireNonNull(builder.baseUrl, "baseUrl不能为空");
        this.timeout = builder.timeout;
        this.retryCount = builder.retryCount;
        this.enableLogging = builder.enableLogging;
        this.defaultHeaders = Collections.unmodifiableMap(
            new HashMap<>(builder.defaultHeaders));
    }

    public static class Builder {
        private String baseUrl;
        private int timeout = 30000;  // 默认值
        private int retryCount = 3;   // 默认值
        private boolean enableLogging = false;  // 默认值
        private Map<String, String> defaultHeaders = new HashMap<>();

        public Builder baseUrl(String baseUrl) {
            this.baseUrl = baseUrl;
            return this;
        }

        public Builder timeout(int timeout) {
            if (timeout <= 0) {
                throw new IllegalArgumentException("timeout必须为正数");
            }
            this.timeout = timeout;
            return this;
        }

        public Builder retryCount(int retryCount) {
            if (retryCount < 0) {
                throw new IllegalArgumentException("retryCount不能为负数");
            }
            this.retryCount = retryCount;
            return this;
        }

        public Builder enableLogging(boolean enableLogging) {
            this.enableLogging = enableLogging;
            return this;
        }

        public Builder addHeader(String key, String value) {
            this.defaultHeaders.put(
                Objects.requireNonNull(key),
                Objects.requireNonNull(value)
            );
            return this;
        }

        public HttpClient build() {
            return new HttpClient(this);
        }
    }
}
```

使用示例

```java
HttpClient client = new HttpClient.Builder()
    .baseUrl("https://api.example.com")
    .timeout(60000)
    .retryCount(5)
    .enableLogging(true)
    .addHeader("User-Agent", "MyApp/1.0")
    .build();
```

### 静态工厂方法

适用于有多种创建方式或需要缓存的情况

```java
public class Color {
    private final int red;
    private final int green;
    private final int blue;

    // 私有构造函数
    private Color(int red, int green, int blue) {
        this.red = validateComponent(red);
        this.green = validateComponent(green);
        this.blue = validateComponent(blue);
    }

    // 静态工厂方法：从RGB值创建
    public static Color fromRGB(int red, int green, int blue) {
        return new Color(red, green, blue);
    }

    // 静态工厂方法：从十六进制字符串创建
    public static Color fromHex(String hex) {
        Objects.requireNonNull(hex, "hex不能为空");
        if (!hex.matches("^#?[0-9A-Fa-f]{6}$")) {
            throw new IllegalArgumentException("无效的十六进制颜色格式: " + hex);
        }

        String cleanHex = hex.startsWith("#") ? hex.substring(1) : hex;
        int rgb = Integer.parseInt(cleanHex, 16);

        return new Color(
            (rgb >> 16) & 0xFF,
            (rgb >> 8) & 0xFF,
            rgb & 0xFF
        );
    }

    // 静态工厂方法：预定义颜色
    public static Color red() {
        return new Color(255, 0, 0);
    }

    public static Color green() {
        return new Color(0, 255, 0);
    }

    public static Color blue() {
        return new Color(0, 0, 255);
    }

    private static int validateComponent(int component) {
        if (component < 0 || component > 255) {
            throw new IllegalArgumentException("颜色分量必须在0-255之间: " + component);
        }
        return component;
    }
}
```

使用示例

```java
Color color1 = Color.fromRGB(255, 128, 0);      // 橙色
Color color2 = Color.fromHex("#FF8000");        // 同样的橙色
Color color3 = Color.red();                     // 预定义的红色
```

## 防止实例化的工具类

### 反例：工具类可以被实例化

```java
public class MathUtils {
    // 缺少私有构造函数，可以被意外实例化
    public static int gcd(int a, int b) {
        return b == 0 ? a : gcd(b, a % b);
    }
}
```

### 正例：使用私有构造函数防止实例化

```java
public final class MathUtils {
    // 私有构造函数防止实例化
    private MathUtils() {
        throw new AssertionError("工具类不应该被实例化");
    }

    public static int gcd(int a, int b) {
        if (b == 0) return a;
        return gcd(b, a % b);
    }

    public static boolean isPrime(int n) {
        if (n < 2) return false;
        for (int i = 2; i * i <= n; i++) {
            if (n % i == 0) return false;
        }
        return true;
    }
}
```


## 依赖注入与构造函数

### 反例：在构造函数中硬编码依赖

```java
public class OrderService {
    private final PaymentProcessor paymentProcessor;
    private final InventoryService inventoryService;

    public OrderService() {
        // 硬编码依赖，难以测试和扩展
        this.paymentProcessor = new CreditCardProcessor();
        this.inventoryService = new DatabaseInventoryService();
    }
}
```

### 正例：通过构造函数注入依赖

```java
public class OrderService {
    private final PaymentProcessor paymentProcessor;
    private final InventoryService inventoryService;
    private final NotificationService notificationService;

    // 依赖通过构造函数注入，便于测试和扩展
    public OrderService(PaymentProcessor paymentProcessor,
                       InventoryService inventoryService,
                       NotificationService notificationService) {
        this.paymentProcessor = Objects.requireNonNull(paymentProcessor);
        this.inventoryService = Objects.requireNonNull(inventoryService);
        this.notificationService = Objects.requireNonNull(notificationService);
    }

    public void processOrder(Order order) {
        // 业务逻辑使用注入的依赖
        inventoryService.reserveItems(order.getItems());
        paymentProcessor.processPayment(order.getPayment());
        notificationService.sendConfirmation(order.getCustomer());
    }
}
```


## 构造函数的性能考虑

### 反例：在构造函数中进行昂贵操作

```java
public class DatabaseConnection {
    private final Connection connection;

    public DatabaseConnection(String url, String username, String password) {
        try {
            // 构造函数中建立连接，可能很慢且容易失败
            this.connection = DriverManager.getConnection(url, username, password);
        } catch (SQLException e) {
            throw new RuntimeException("无法建立数据库连接", e);
        }
    }
}
```

### 正例：避免在构造函数中进行昂贵操作

```java
public class DatabaseConnection {
    private final String url;
    private final String username;
    private final String password;
    private Connection connection;  // 延迟初始化

    public DatabaseConnection(String url, String username, String password) {
        this.url = Objects.requireNonNull(url);
        this.username = Objects.requireNonNull(username);
        this.password = Objects.requireNonNull(password);
        // 不在构造函数中建立连接，避免阻塞
    }

    // 延迟初始化，仅在需要时建立连接
    public Connection getConnection() throws SQLException {
        if (connection == null || connection.isClosed()) {
            connection = DriverManager.getConnection(url, username, password);
        }
        return connection;
    }
}
```


## 最佳实践总结

### 构造函数设计原则

1. **最小化构造函数的职责**：只做必要的初始化工作
2. **参数验证优先**：在构造函数开始时验证所有参数
3. **使用 final 字段**：尽可能使用 `final` 修饰符保证不可变性
4. **避免重复代码**：使用构造函数链（`this()`调用）
5. **考虑替代方案**：复杂情况下使用 `Builder` 或工厂方法

### 何时使用不同的构造模式

| 场景                | 推荐模式     | 理由                     |
| ------------------- | ------------ | ------------------------ |
| 参数少于 4 个且简单 | 标准构造函数 | 简单直接，易于理解       |
| 参数多于 4 个       | `Builder` 模式 | 提高可读性和灵活性       |
| 构造可能失败        | 工厂方法     | 返回 `Optional` 或特定异常 |
| 多种创建方式        | 静态工厂方法 | 方法名称更有表达力       |
| 需要缓存实例        | 静态工厂方法 | 控制实例创建             |
| 工具类              | 私有构造函数 | 防止意外实例化           |



## 扩展阅读

### Effective Java 相关条目

- [Item 1: Consider static factory methods instead of constructors](https://www.oracle.com/java/technologies/javase/codeconventions-contents.html)
- [Item 2: Consider a builder when faced with many constructor parameters](https://www.oracle.com/java/technologies/javase/codeconventions-contents.html)
- [Item 4: Enforce noninstantiability with a private constructor](https://www.oracle.com/java/technologies/javase/codeconventions-contents.html)
- [Item 5: Prefer dependency injection to hardwiring resources](https://www.oracle.com/java/technologies/javase/codeconventions-contents.html)

### Java 语言规范

- [JLS §8.8 Constructor Declarations](https://docs.oracle.com/javase/specs/jls/se17/html/jls-8.html#jls-8.8)
- [JLS §12.5 Creation of New Class Instances](https://docs.oracle.com/javase/specs/jls/se17/html/jls-12.html#jls-12.5)

### 相关 Java 编程指南

- [Factory 工厂模式](factory.md)
- [Builder 建造者模式](builder.md)
- [Dependency Injection 依赖注入](dependency_injection.md)
- [Noninstantiability 不可实例化](noninstantiability.md)
