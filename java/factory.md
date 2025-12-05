# Factory 工厂模式

## tl;dr

- 优先使用静态工厂方法而非复杂的工厂类。避免过度抽象，例如简单对象也用工厂类
- 用 `Optional` 优雅处理创建失败，避免异常滥用
- 方法命名要体现创建意图，如 `createForProduction()` 而非 `create()`
- 考虑线程安全和性能，合理使用缓存
- 不要忽略资源管理，例如工厂创建的对象需要正确释放
- 避免职责不清，例如工厂承担过多业务逻辑。

## 为什么需要工厂模式

### 传统构造函数的问题

传统的构造函数存在如下几个问题：

1. **失败处理不灵活**：由于构造函数的特性，开发者无法干预返回值，导致无法返回 null，若构造失败只能抛出异常，不利于业务逻辑的流畅处理
2. **复杂的参数验证**：传统构造函数中，可能有较多的参数验证逻辑，导致业务代码复杂化
3. **缺乏语义表达**：因为构造函数的名称不具备区分性，多个构造函数的参数类型相似或者相近时，容易混淆
4. **难以扩展**：当需要增加新的创建逻辑时需要修改类的现有构造代码

### 工厂模式的优势

1. **优雅处理失败**：可以控制返回 `Optional` 或 `null` 来表示创建失败，让代码更流畅
2. **清晰的语义**：工厂的方法能够根据意图进行定制化命名，可以有效的消除歧义，易于理解
3. **参数验证集中**：对于参数的验证可以在工厂中更加集中的处理，让类的逻辑更加简单
4. **易于扩展**：符合开闭原则，便于添加新的创建方式，职责也更为明确

## 核心最佳实践

### 静态工厂方法优先原则

**推荐**：对于大多数场景，静态工厂方法比复杂的工厂类更合适。

```java
// ✅ 好的做法：静态工厂方法
public class DatabaseConnection {
    private DatabaseConnection(String url) { /* ... */ }
    
    public static Optional<DatabaseConnection> createForDevelopment() {
        return create("jdbc:mysql:xxx...");
    }
    
    public static Optional<DatabaseConnection> createForProduction(String host) {
        return create("jdbc:mysql:xxx...");
    }
}

// ❌ 过度设计：不必要的工厂类
public class DatabaseConnectionFactory {
    public DatabaseConnection create(String type) { /* ... */ }
}
```

### 优雅的失败处理

**推荐**：使用 `Optional` 而非异常来处理创建失败。

```java
// ✅ 好的做法：返回 Optional
public static Optional<User> createUser(String email) {
    if (!isValidEmail(email)) {
        return Optional.empty();
    }
    return Optional.of(new User(email));
}

// ❌ 不好的做法：滥用异常
public static User createUser(String email) throws InvalidEmailException {
    if (!isValidEmail(email)) {
        throw new InvalidEmailException("Invalid email: " + email);
    }
    return new User(email);
}
```

### 清晰的方法命名

**推荐**：方法名要体现创建意图和上下文。

```java
// ✅ 好的做法：语义清晰
public static HttpClient createForProduction() { /* ... */ }
public static HttpClient createForTesting() { /* ... */ }
public static HttpClient createWithTimeout(Duration timeout) { /* ... */ }

// ❌ 不好的做法：语义模糊
public static HttpClient create(String type) { /* ... */ }
public static HttpClient getInstance() { /* ... */ }
```

### 合理的缓存策略

**推荐**：对于创建成本高的对象，考虑缓存，但要注意线程安全。

```java
// ✅ 好的做法：线程安全的缓存
public class ExpensiveResourceFactory {
    private static final ConcurrentHashMap<String, ExpensiveResource> cache = 
        new ConcurrentHashMap<>();
    
    public static ExpensiveResource getInstance(String key) {
        return cache.computeIfAbsent(key, ExpensiveResource::new);
    }
}
```

## 常见误区和陷阱

### 过度抽象陷阱

**问题**：为简单对象创建复杂的工厂层次结构。

```java
// ❌ 过度设计：简单对象用复杂工厂
public abstract class PersonFactory {
    public abstract Person createPerson();
}

public class StudentFactory extends PersonFactory {
    @Override
    public Person createPerson() {
        return new Student();
    }
}

// ✅ 简单直接：直接使用构造函数
Student student = new Student();
// 或者简单的静态方法
Student student = Student.createDefault();
```

### 资源管理陷阱

**问题**：工厂创建的资源未正确管理，导致内存泄漏。

```java
// ❌ 危险：资源未管理
public class ConnectionFactory {
    public static Connection createConnection() {
        return DriverManager.getConnection(url, user, password);
        // 问题：谁负责关闭连接？
    }
}

// ✅ 安全：明确资源管理责任
public class ConnectionFactory {
    public static Connection createConnection() {
        // 文档说明：调用者负责关闭连接
        return DriverManager.getConnection(url, user, password);
    }
    
    // 或者提供资源管理的便利方法
    public static <T> T withConnection(Function<Connection, T> action) {
        try (Connection conn = createConnection()) {
            return action.apply(conn);
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
    }
}
```

### 命名混乱陷阱

**问题**：工厂方法命名不清晰，增加使用难度。

```java
// ❌ 混乱的命名
public class UserFactory {
    public static User create() { /* ... */ }           // 创建什么样的用户？
    public static User getInstance() { /* ... */ }      // 单例还是新实例？
    public static User build(String type) { /* ... */ } // type 是什么？
}

// ✅ 清晰的命名
public class UserFactory {
    public static User createGuest() { /* ... */ }
    public static User createAdmin(String name) { /* ... */ }
    public static Optional<User> createFromEmail(String email) { /* ... */ }
}
```

### 职责混乱陷阱

**问题**：工厂承担了过多的业务逻辑。

```java
// ❌ 职责过重：工厂做了太多事情
public class OrderFactory {
    public static Order createOrder(Customer customer, List<Item> items) {
        // 验证客户
        if (!customer.isActive()) {
            throw new IllegalArgumentException("客户未激活");
        }
        
        // 计算价格
        BigDecimal total = items.stream()
            .map(Item::getPrice)
            .reduce(BigDecimal.ZERO, BigDecimal::add);
        
        // 应用折扣
        if (customer.isVip()) {
            total = total.multiply(new BigDecimal("0.9"));
        }
        
        // 发送通知
        NotificationService.sendOrderConfirmation(customer.getEmail());
        
        return new Order(customer, items, total);
    }
}

// ✅ 职责清晰：工厂只负责创建
public class OrderFactory {
    public static Optional<Order> createOrder(Customer customer, List<Item> items) {
        if (!isValidForOrder(customer, items)) {
            return Optional.empty();
        }
        return Optional.of(new Order(customer, items));
    }
    
    private static boolean isValidForOrder(Customer customer, List<Item> items) {
        return customer.isActive() && !items.isEmpty();
    }
}

// 业务逻辑在服务层处理
public class OrderService {
    public Order processOrder(Customer customer, List<Item> items) {
        Optional<Order> orderOpt = OrderFactory.createOrder(customer, items);
        if (orderOpt.isEmpty()) {
            throw new IllegalArgumentException("无法创建订单");
        }
        
        Order order = orderOpt.get();
        order.calculateTotal();
        order.applyDiscounts();
        notificationService.sendConfirmation(order);
        
        return order;
    }
}
```

## 性能考虑

### 线程安全

**问题**：多线程环境下的工厂方法可能存在竞态条件。

```java
// ❌ 线程不安全的单例工厂
public class DatabaseConnectionFactory {
    private static DatabaseConnection instance;
    
    public static DatabaseConnection getInstance() {
        if (instance == null) {
            instance = new DatabaseConnection(); // 竞态条件
        }
        return instance;
    }
}

// ✅ 线程安全的实现
public class DatabaseConnectionFactory {
    private static volatile DatabaseConnection instance;
    
    public static DatabaseConnection getInstance() {
        if (instance == null) {
            synchronized (DatabaseConnectionFactory.class) {
                if (instance == null) {
                    instance = new DatabaseConnection();
                }
            }
        }
        return instance;
    }
    
    // 或者更简单的方式：使用枚举
    public enum SingletonConnection {
        INSTANCE;
        
        private final DatabaseConnection connection = new DatabaseConnection();
        
        public DatabaseConnection getConnection() {
            return connection;
        }
    }
}
```

### 缓存策略

**推荐**：合理使用缓存，但要考虑内存泄漏风险。

```java
// ✅ 带有清理机制的缓存
public class ConnectionFactory {
    private static final Map<String, WeakReference<Connection>> cache = 
        new ConcurrentHashMap<>();
    
    public static Connection getConnection(String url) {
        WeakReference<Connection> ref = cache.get(url);
        Connection conn = (ref != null) ? ref.get() : null;
        
        if (conn == null || conn.isClosed()) {
            conn = createNewConnection(url);
            cache.put(url, new WeakReference<>(conn));
        }
        
        return conn;
    }
    
    // 定期清理失效的缓存项
    public static void cleanupCache() {
        cache.entrySet().removeIf(entry -> entry.getValue().get() == null);
    }
}
```

## 实际应用场景

### 与建造者模式结合

**适用场景**：复杂对象需要多种预设配置。

```java
public class HttpClientConfig {
    private final Duration timeout;
    private final int maxRetries;
    private final boolean followRedirects;
    
    private HttpClientConfig(Builder builder) {
        this.timeout = builder.timeout;
        this.maxRetries = builder.maxRetries;
        this.followRedirects = builder.followRedirects;
    }
    
    // 工厂方法提供常用配置
    public static HttpClientConfig forProduction() {
        return new Builder()
            .timeout(Duration.ofSeconds(30))
            .maxRetries(3)
            .followRedirects(true)
            .build();
    }
    
    public static HttpClientConfig forTesting() {
        return new Builder()
            .timeout(Duration.ofSeconds(5))
            .maxRetries(1)
            .followRedirects(false)
            .build();
    }
    
    public static Builder builder() {
        return new Builder();
    }
    
    public static class Builder {
        private Duration timeout = Duration.ofSeconds(10);
        private int maxRetries = 0;
        private boolean followRedirects = true;
        
        public Builder timeout(Duration timeout) {
            this.timeout = timeout;
            return this;
        }
        
        public Builder maxRetries(int maxRetries) {
            this.maxRetries = maxRetries;
            return this;
        }
        
        public Builder followRedirects(boolean followRedirects) {
            this.followRedirects = followRedirects;
            return this;
        }
        
        public HttpClientConfig build() {
            return new HttpClientConfig(this);
        }
    }
}
```

### 条件创建模式

**适用场景**：根据运行时条件选择不同的实现。

```java
public class LoggerFactory {
    public static Logger createLogger(String environment) {
        switch (environment.toLowerCase()) {
            case "production":
                return new FileLogger("/var/log/app.log");
            case "development":
                return new ConsoleLogger();
            case "testing":
                return new NoOpLogger();
            default:
                return new ConsoleLogger();
        }
    }
    
    // 更好的方式：使用枚举
    public enum Environment {
        PRODUCTION(() -> new FileLogger("/var/log/app.log")),
        DEVELOPMENT(ConsoleLogger::new),
        TESTING(NoOpLogger::new);
        
        private final Supplier<Logger> loggerSupplier;
        
        Environment(Supplier<Logger> loggerSupplier) {
            this.loggerSupplier = loggerSupplier;
        }
        
        public Logger createLogger() {
            return loggerSupplier.get();
        }
    }
}
```

## 总结

工厂模式的价值在于**在合适的时机提供合适的抽象**，而不是替代所有的对象创建。

**核心原则**：
- 不要为了使用模式而使用模式
- 简单的场景用简单的方法
- 复杂的场景才需要复杂的抽象

**决策指南**：
- 对象创建简单且稳定 → 直接使用构造函数
- 需要多种创建方式或条件创建 → 静态工厂方法
- 需要运行时决定创建哪种类型 → 工厂方法模式
- 需要创建一系列相关对象 → 抽象工厂模式

**避免的陷阱**：
- 过度抽象导致代码复杂化
- 忽略资源管理责任
- 工厂承担过多业务逻辑
- 线程安全问题

## 参考资源

1. **《Effective Java》第三版** - Joshua Bloch
2. **《设计模式：可复用面向对象软件的基础》** - Gang of Four
3. **Java 官方文档**：https://docs.oracle.com/javase/8/docs/api/java/util/Optional.html
4. **相关设计原则**：开闭原则、依赖倒置原则
5. **实际应用示例**：Spring Framework 中的 BeanFactory、Java 集合框架中的工厂方法
