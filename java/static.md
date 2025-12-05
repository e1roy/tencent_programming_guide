# Static 静态

## tl;dr

- 避免初始化块
- 私有方法应该尽可能 `static`
- Inner class 应该尽可能是 `static`

## 初始化块

避免静态初始化块。考虑使用静态方法返回该值。

## 私有方法应该尽量声明为 `static`

一个不引用所在类的私有方法应该被标为 `static`。如：

```java
class Adapter {
  private final Options options;
  public Result to(Source source) {
    // ...
    Subfield subfield = adaptSomeSubfield(source);
  }
  private Subfield adaptSomeSubfield(Source source) {
    // 逻辑不需要引用 Options
  }
}
```

这时 `adaptSomeSubfield` 应该有 `static` 标识符。

## 尽可能使用 static inner class

Nonstatic inner class 会持有上层对象的引用。所以，除非真的有必要（例如某些回调），否则，通常不需要使用 non-static inner class

## 注意事项

### static final 不总是常量

参考 [Constants 常量](constants.md)
简言之，不可变的才是常量，但 `static final` 的成员未必不可变。

## Static 关键字的实际应用

### 静态工具方法

```java
public final class MathUtils {
    private MathUtils() {
        throw new AssertionError("Utility class");
    }
    
    // ✅ 不依赖实例状态的方法应该是静态的
    public static int gcd(int a, int b) {
        while (b != 0) {
            int temp = b;
            b = a % b;
            a = temp;
        }
        return a;
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

### 静态工厂方法

```java
public class User {
    private final String name;
    private final String email;
    private final LocalDateTime createdAt;
    
    private User(String name, String email, LocalDateTime createdAt) {
        this.name = name;
        this.email = email;
        this.createdAt = createdAt;
    }
    
    // ✅ 静态工厂方法比构造函数更灵活
    public static User create(String name, String email) {
        return new User(name, email, LocalDateTime.now());
    }
    
    public static User createGuest() {
        return new User("Guest", "guest@example.com", LocalDateTime.now());
    }
    
    public static User fromJson(String json) {
        // JSON 解析逻辑
        return new User("parsed_name", "parsed_email", LocalDateTime.now());
    }
    
    // getters...
}
```

### 静态内部类的正确使用

```java
public class OuterClass {
    private String instanceField = "instance";
    
    // ✅ 静态内部类：不需要访问外部类实例
    public static class StaticNestedClass {
        private String nestedField = "nested";
        
        public void doSomething() {
            System.out.println("Static nested: " + nestedField);
            // System.out.println(instanceField); // 编译错误：无法访问外部类实例字段
        }
    }
    
    // ❌ 非静态内部类：持有外部类引用，可能导致内存泄漏
    public class NonStaticInnerClass {
        public void doSomething() {
            System.out.println("Inner: " + instanceField); // 可以访问外部类字段
        }
    }
    
    // ✅ 建造者模式中的静态内部类
    public static class Builder {
        private String name;
        private String email;
        
        public Builder name(String name) {
            this.name = name;
            return this;
        }
        
        public Builder email(String email) {
            this.email = email;
            return this;
        }
        
        public User build() {
            return User.create(name, email);
        }
    }
}
```

### 静态初始化的最佳实践

```java
public class ConfigurationManager {
    // ✅ 使用静态方法而不是静态初始化块
    private static final Map<String, String> CONFIG = loadConfiguration();
    private static final Logger logger = LoggerFactory.getLogger(ConfigurationManager.class);
    
    // ✅ 静态工厂方法进行初始化
    private static Map<String, String> loadConfiguration() {
        try {
            Properties props = new Properties();
            props.load(ConfigurationManager.class.getResourceAsStream("/config.properties"));
            return props.entrySet().stream()
                       .collect(Collectors.toMap(
                           e -> e.getKey().toString(),
                           e -> e.getValue().toString()
                       ));
        } catch (IOException e) {
            logger.error("Failed to load configuration", e);
            return Collections.emptyMap();
        }
    }
    
    // ❌ 避免使用静态初始化块
    /*
    static {
        // 复杂的初始化逻辑应该放在方法中
        CONFIG = new HashMap<>();
        // ... 复杂的初始化代码
    }
    */
    
    public static String getProperty(String key) {
        return CONFIG.get(key);
    }
}
```

### 静态方法与实例方法的选择

```java
public class DataProcessor {
    private final String processorName;
    private final Map<String, Object> cache = new ConcurrentHashMap<>();
    
    public DataProcessor(String processorName) {
        this.processorName = processorName;
    }
    
    // ✅ 不使用实例状态的方法应该是静态的
    public static String sanitizeInput(String input) {
        if (input == null) return "";
        return input.trim().toLowerCase();
    }
    
    public static boolean isValidEmail(String email) {
        return email != null && email.contains("@") && email.contains(".");
    }
    
    // ✅ 使用实例状态的方法不应该是静态的
    public void processData(String data) {
        String sanitized = sanitizeInput(data); // 调用静态方法
        cache.put(sanitized, System.currentTimeMillis());
        System.out.println(processorName + " processed: " + sanitized);
    }
    
    public Object getCachedData(String key) {
        return cache.get(sanitizeInput(key));
    }
    
    // ❌ 错误：这个方法使用了实例字段，不应该是静态的
    /*
    public static void badMethod() {
        System.out.println(processorName); // 编译错误
    }
    */
}
```

### 静态导入的合理使用

```java
// ✅ 合理的静态导入：常用的工具方法
import static java.util.Collections.*;
import static java.util.stream.Collectors.*;
import static org.junit.jupiter.api.Assertions.*;

public class StaticImportExample {
    public void demonstrateStaticImports() {
        List<String> list = singletonList("item");  // Collections.singletonList
        
        List<String> result = list.stream()
                                 .collect(toList());  // Collectors.toList()
        
        assertEquals(1, result.size());  // Assertions.assertEquals
    }
    
    // ❌ 避免过度使用静态导入
    // import static com.example.SomeClass.*;  // 导入所有静态成员可能造成命名冲突
}
```

### 单例模式中的静态使用

```java
public class DatabaseConnection {
    // ✅ 线程安全的单例实现
    private static class Holder {
        private static final DatabaseConnection INSTANCE = new DatabaseConnection();
    }
    
    private DatabaseConnection() {
        // 私有构造函数
    }
    
    public static DatabaseConnection getInstance() {
        return Holder.INSTANCE;  // 延迟初始化，线程安全
    }
    
    // ✅ 枚举单例（推荐）
    public enum DatabaseConnectionEnum {
        INSTANCE;
        
        public void connect() {
            // 连接逻辑
        }
    }
}
```

### 静态常量的组织

```java
public final class Constants {
    private Constants() {
        throw new AssertionError("Constants class");
    }
    
    // ✅ 按功能分组的静态常量
    public static final class Http {
        public static final int OK = 200;
        public static final int NOT_FOUND = 404;
        public static final int INTERNAL_SERVER_ERROR = 500;
    }
    
    public static final class Database {
        public static final int DEFAULT_TIMEOUT = 30;
        public static final int MAX_CONNECTIONS = 100;
        public static final String DEFAULT_CHARSET = "UTF-8";
    }
    
    public static final class Validation {
        public static final int MIN_PASSWORD_LENGTH = 8;
        public static final int MAX_USERNAME_LENGTH = 50;
        public static final Pattern EMAIL_PATTERN = 
            Pattern.compile("^[A-Za-z0-9+_.-]+@(.+)$");
    }
}
```

## `Static` 使用指南

1. **工具方法**：不依赖实例状态的方法应该是静态的
2. **内部类**：优先使用静态内部类，除非需要访问外部类实例
3. **初始化**：使用静态方法而不是静态初始化块
4. **常量组织**：按功能分组静态常量
5. **静态导入**：谨慎使用，避免命名冲突

## 扩展阅读

- https://errorprone.info/bugpattern/MethodCanBeStatic
- Effective Java Item 24: Favor static member classes over nonstatic
- [Java 静态关键字详解](https://docs.oracle.com/javase/tutorial/java/javaOO/classvars.html)
