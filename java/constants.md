# Constants 常量

## tl;dr

- **常量必须是不可变对象**。`static final` 不等于常量，只有不可变对象才是真正的常量。
- **使用工具类而非接口定义常量**。接口是为了定义类型，不应用于定义常量。
- **遵循常量命名规范**。使用 `CONSTANT_CASE` 风格，全部大写，下划线分隔单词。
- **合理组织常量**。按功能分组，使用嵌套类或枚举来组织相关常量。
- **避免魔法数字**。所有有意义的数字都应该定义为常量。

## 什么是常量

常量是指在程序运行期间值不会改变的量。在Java中，常量通常使用 `static final` 修饰符声明，但并非所有 `static final` 字段都是常量。

**真正的常量必须满足以下条件：**
1. 使用 `static final` 修饰
2. 引用的对象是不可变的
3. 在编译时或类加载时就能确定其值

## static final != 常量

只有**不可变**的对象才是常量。

常量一定应该标注为 `static final`，`static final` 未必是常量。典型的例子：

```java
public class ConfigurationExample {
    // ✅ 这些是常量
    public static final int DEFAULT_TIMEOUT = 30000;
    public static final String APPLICATION_NAME = "MyApp";
    public static final BigDecimal TAX_RATE = new BigDecimal("0.08");
    
    // ❌ 这些不是常量（对象是可变的）
    private static final Logger logger = LoggerFactory.getLogger(ConfigurationExample.class);
    private static final List<String> mutableList = new ArrayList<>();
    private static final Date creationTime = new Date();
    private static final AtomicInteger counter = new AtomicInteger(0);
    
    // ✅ 这样才是常量（不可变集合）
    public static final Set<String> VALID_STATUSES = 
        Collections.unmodifiableSet(new HashSet<>(Arrays.asList("ACTIVE", "INACTIVE", "PENDING")));
}
```

## 常量的类型和使用场景

### 基本类型常量

```java
public class MathConstants {
    public static final double PI = 3.14159265359;
    public static final int CIRCLE_DEGREES = 360;
    public static final long MILLISECONDS_PER_DAY = 24L * 60L * 60L * 1000L;
    public static final boolean DEBUG_MODE = false;
}
```

### 字符串常量

```java
public class MessageConstants {
    public static final String SUCCESS_MESSAGE = "Operation completed successfully";
    public static final String ERROR_PREFIX = "ERROR: ";
    public static final String DEFAULT_ENCODING = "UTF-8";
    
    // 避免重复的字符串字面量
    public static final String EMPTY_STRING = "";
    public static final String SPACE = " ";
    public static final String COMMA = ",";
}
```

### 集合常量

```java
public class CollectionConstants {
    // 不可变列表
    public static final List<String> SUPPORTED_LANGUAGES = 
        Collections.unmodifiableList(Arrays.asList("Java", "Python", "JavaScript"));
    
    // 不可变集合
    public static final Set<Integer> PRIME_NUMBERS = 
        Collections.unmodifiableSet(new HashSet<>(Arrays.asList(2, 3, 5, 7, 11, 13)));
    
    // 不可变映射
    public static final Map<String, String> HTTP_STATUS_MESSAGES = 
        Collections.unmodifiableMap(new HashMap<String, String>() {{
            put("200", "OK");
            put("404", "Not Found");
            put("500", "Internal Server Error");
        }});
    
    // Java 9+ 更简洁的方式
    public static final List<String> WEEKDAYS = 
        List.of("Monday", "Tuesday", "Wednesday", "Thursday", "Friday");
    
    public static final Map<String, Integer> MONTH_DAYS = 
        Map.of("January", 31, "February", 28, "March", 31);
}
```

### 枚举常量

```java
// 推荐：使用枚举定义相关常量
public enum Status {
    ACTIVE("A", "Active"),
    INACTIVE("I", "Inactive"),
    PENDING("P", "Pending");
    
    private final String code;
    private final String description;
    
    Status(String code, String description) {
        this.code = code;
        this.description = description;
    }
    
    public String getCode() { return code; }
    public String getDescription() { return description; }
}

// 不推荐：使用常量类定义相关常量
public class StatusConstants {
    public static final String ACTIVE = "A";
    public static final String INACTIVE = "I";
    public static final String PENDING = "P";
}
```

## 常量的组织方式

### 使用工具类组织常量

```java
public final class ApplicationConstants {
    // 防止实例化
    private ApplicationConstants() {
        throw new AssertionError("Utility class should not be instantiated");
    }
    
    // 数据库相关常量
    public static final class Database {
        public static final int DEFAULT_CONNECTION_TIMEOUT = 30000;
        public static final int MAX_POOL_SIZE = 20;
        public static final String DEFAULT_SCHEMA = "public";
        
        private Database() {}
    }
    
    // HTTP相关常量
    public static final class Http {
        public static final int DEFAULT_PORT = 8080;
        public static final String CONTENT_TYPE_JSON = "application/json";
        public static final String HEADER_AUTHORIZATION = "Authorization";
        
        private Http() {}
    }
    
    // 业务相关常量
    public static final class Business {
        public static final int MAX_RETRY_ATTEMPTS = 3;
        public static final long CACHE_EXPIRY_MINUTES = 60;
        public static final BigDecimal DEFAULT_DISCOUNT_RATE = new BigDecimal("0.05");
        
        private Business() {}
    }
}

// 使用示例
int timeout = ApplicationConstants.Database.DEFAULT_CONNECTION_TIMEOUT;
String contentType = ApplicationConstants.Http.CONTENT_TYPE_JSON;
```

### 按功能模块分离常量

```java
// 文件操作相关常量
public final class FileConstants {
    private FileConstants() {}
    
    public static final String DEFAULT_ENCODING = "UTF-8";
    public static final int BUFFER_SIZE = 8192;
    public static final String TEMP_DIR_PREFIX = "app_temp_";
    
    public static final Set<String> ALLOWED_EXTENSIONS = 
        Set.of(".txt", ".csv", ".json", ".xml");
}

// 验证相关常量
public final class ValidationConstants {
    private ValidationConstants() {}
    
    public static final int MIN_PASSWORD_LENGTH = 8;
    public static final int MAX_USERNAME_LENGTH = 50;
    public static final String EMAIL_REGEX = "^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$";
    
    public static final Pattern EMAIL_PATTERN = Pattern.compile(EMAIL_REGEX);
}
```

## 不要使用接口定义常量

虽然看上去接口符合常量类定义的所有要求 -- 不可实例、无状态，但接口(interface) 是为了定义**类型**，而常量不属于一个类型。

```java
// ❌ 错误：使用接口定义常量（常量接口反模式）
public interface Constants {
    int MAX_SIZE = 100;
    String DEFAULT_NAME = "Unknown";
    double TAX_RATE = 0.08;
}

// 问题：
// 1. 违反了接口的设计目的
// 2. 实现该接口的类会"污染"其命名空间
// 3. 这些常量成为了类的公共API的一部分
// 4. 无法阻止客户端实现这个接口

class MyClass implements Constants {
    // 现在MyClass的所有实例都"拥有"了这些常量
    public void someMethod() {
        System.out.println(MAX_SIZE); // 直接访问，没有类名限定
    }
}
```

**正确做法：使用不可实例化的工具类**

```java
// ✅ 正确：使用工具类定义常量
public final class Constants {
    private Constants() {
        throw new AssertionError("Utility class should not be instantiated");
    }
    
    public static final int MAX_SIZE = 100;
    public static final String DEFAULT_NAME = "Unknown";
    public static final double TAX_RATE = 0.08;
}

// 使用时需要类名限定，清晰明确
class MyClass {
    public void someMethod() {
        System.out.println(Constants.MAX_SIZE);
    }
}
```

## 常量命名规范

### 基本命名规则

```java
public final class NamingExamples {
    // ✅ 正确：CONSTANT_CASE风格
    public static final int MAX_RETRY_COUNT = 3;
    public static final String DEFAULT_USER_NAME = "guest";
    public static final double PI_VALUE = 3.14159;
    public static final long TIMEOUT_IN_MILLISECONDS = 30000L;
    
    // ❌ 错误：不符合命名规范
    public static final int maxRetryCount = 3;        // 应该全大写
    public static final String DefaultUserName = "guest"; // 应该全大写加下划线
    public static final double pi = 3.14159;         // 应该全大写
}
```

### 有意义的命名

```java
public final class MeaningfulNames {
    // ✅ 好的命名：清晰表达意图
    public static final int HTTP_STATUS_OK = 200;
    public static final int HTTP_STATUS_NOT_FOUND = 404;
    public static final int HTTP_STATUS_INTERNAL_ERROR = 500;
    
    public static final String DATE_FORMAT_ISO = "yyyy-MM-dd";
    public static final String DATETIME_FORMAT_FULL = "yyyy-MM-dd HH:mm:ss";
    
    public static final int CONNECTION_TIMEOUT_SECONDS = 30;
    public static final int MAX_UPLOAD_SIZE_MB = 10;
    
    // ❌ 不好的命名：含义不清
    public static final int STATUS_1 = 200;  // 什么状态？
    public static final int STATUS_2 = 404;
    public static final String FORMAT_1 = "yyyy-MM-dd";  // 什么格式？
    public static final int TIMEOUT = 30;    // 什么的超时？单位是什么？
}
```

## 避免魔法数字

魔法数字是指在代码中直接出现的数字字面量，没有明确的含义说明。

```java
// ❌ 充满魔法数字的代码
public class BadExample {
    public boolean isValidAge(int age) {
        return age >= 0 && age <= 150;  // 150是什么意思？
    }
    
    public String formatFileSize(long bytes) {
        if (bytes < 1024) {
            return bytes + " B";
        } else if (bytes < 1048576) {  // 1048576是什么？
            return (bytes / 1024) + " KB";
        } else {
            return (bytes / 1048576) + " MB";
        }
    }
    
    public void processData() {
        for (int i = 0; i < 10; i++) {  // 为什么是10？
            // 处理逻辑
            Thread.sleep(5000);  // 为什么睡眠5秒？
        }
    }
}

// ✅ 使用常量消除魔法数字
public class GoodExample {
    private static final int MIN_VALID_AGE = 0;
    private static final int MAX_VALID_AGE = 150;
    
    private static final long BYTES_PER_KB = 1024L;
    private static final long BYTES_PER_MB = BYTES_PER_KB * 1024L;
    
    private static final int MAX_RETRY_ATTEMPTS = 10;
    private static final long RETRY_DELAY_MS = 5000L;
    
    public boolean isValidAge(int age) {
        return age >= MIN_VALID_AGE && age <= MAX_VALID_AGE;
    }
    
    public String formatFileSize(long bytes) {
        if (bytes < BYTES_PER_KB) {
            return bytes + " B";
        } else if (bytes < BYTES_PER_MB) {
            return (bytes / BYTES_PER_KB) + " KB";
        } else {
            return (bytes / BYTES_PER_MB) + " MB";
        }
    }
    
    public void processData() throws InterruptedException {
        for (int i = 0; i < MAX_RETRY_ATTEMPTS; i++) {
            // 处理逻辑
            Thread.sleep(RETRY_DELAY_MS);
        }
    }
}
```

## 常量的初始化和加载

### 编译时常量 vs 运行时常量

```java
public class ConstantInitialization {
    // 编译时常量：在编译时就能确定值
    public static final int COMPILE_TIME_CONSTANT = 42;
    public static final String COMPILE_TIME_STRING = "Hello";
    
    // 运行时常量：需要在运行时计算
    public static final long CURRENT_TIME = System.currentTimeMillis();
    public static final String SYSTEM_PROPERTY = System.getProperty("user.home");
    public static final List<String> RUNTIME_LIST = Arrays.asList("a", "b", "c");
    
    // 静态初始化块
    public static final Map<String, Integer> MONTH_DAYS;
    static {
        Map<String, Integer> map = new HashMap<>();
        map.put("January", 31);
        map.put("February", 28);
        map.put("March", 31);
        // ... 其他月份
        MONTH_DAYS = Collections.unmodifiableMap(map);
    }
}
```

### 延迟初始化的常量

```java
public class LazyConstants {
    // 使用静态内部类实现延迟初始化
    private static class ExpensiveConstantHolder {
        private static final ExpensiveObject EXPENSIVE_CONSTANT = createExpensiveObject();
        
        private static ExpensiveObject createExpensiveObject() {
            // 昂贵的初始化操作
            return new ExpensiveObject();
        }
    }
    
    public static ExpensiveObject getExpensiveConstant() {
        return ExpensiveConstantHolder.EXPENSIVE_CONSTANT;
    }
}
```

## 常量的测试

```java
public class ConstantsTest {
    @Test
    public void testConstantValues() {
        // 测试常量值的正确性
        assertEquals(100, ApplicationConstants.MAX_SIZE);
        assertEquals("UTF-8", ApplicationConstants.DEFAULT_ENCODING);
        assertTrue(ApplicationConstants.TIMEOUT_SECONDS > 0);
    }
    
    @Test
    public void testConstantImmutability() {
        // 测试集合常量的不可变性
        List<String> languages = ApplicationConstants.SUPPORTED_LANGUAGES;
        
        assertThrows(UnsupportedOperationException.class, () -> {
            languages.add("C++");  // 应该抛出异常
        });
        
        assertThrows(UnsupportedOperationException.class, () -> {
            languages.remove(0);   // 应该抛出异常
        });
    }
    
    @Test
    public void testUtilityClassCannotBeInstantiated() {
        // 测试工具类不能被实例化
        assertThrows(AssertionError.class, () -> {
            Constructor<ApplicationConstants> constructor = 
                ApplicationConstants.class.getDeclaredConstructor();
            constructor.setAccessible(true);
            constructor.newInstance();
        });
    }
}
```

## 常见陷阱和最佳实践

### 避免可变对象作为常量

```java
// ❌ 错误：可变对象不是真正的常量
public static final List<String> MUTABLE_LIST = new ArrayList<>();
public static final Date MUTABLE_DATE = new Date();
public static final StringBuilder MUTABLE_BUILDER = new StringBuilder();

// ✅ 正确：使用不可变对象
public static final List<String> IMMUTABLE_LIST = 
    Collections.unmodifiableList(Arrays.asList("a", "b", "c"));
public static final LocalDate IMMUTABLE_DATE = LocalDate.of(2023, 1, 1);
public static final String IMMUTABLE_STRING = "constant value";
```

### 合理使用枚举替代常量

```java
// ❌ 不推荐：使用多个相关常量
public static final int STATUS_PENDING = 0;
public static final int STATUS_APPROVED = 1;
public static final int STATUS_REJECTED = 2;

// ✅ 推荐：使用枚举
public enum Status {
    PENDING(0, "Pending"),
    APPROVED(1, "Approved"),
    REJECTED(2, "Rejected");
    
    private final int code;
    private final String description;
    
    Status(int code, String description) {
        this.code = code;
        this.description = description;
    }
    
    public int getCode() { return code; }
    public String getDescription() { return description; }
}
```

### 常量的文档化

```java
/**
 * 应用程序配置常量
 */
public final class ConfigConstants {
    private ConfigConstants() {}
    
    /**
     * 默认连接超时时间（毫秒）
     * 
     * <p>该值基于网络延迟的统计分析确定，
     * 在99%的情况下能够成功建立连接。
     */
    public static final int DEFAULT_CONNECTION_TIMEOUT_MS = 30000;
    
    /**
     * 支持的文件格式列表
     * 
     * <p>只有这些格式的文件才能被系统处理。
     * 添加新格式需要同时更新解析器。
     */
    public static final Set<String> SUPPORTED_FILE_FORMATS = 
        Set.of("json", "xml", "csv", "txt");
}
```

## 性能考虑

### 常量池的使用

```java
public class ConstantPool {
    // 字符串常量会进入字符串常量池
    public static final String POOLED_STRING = "Hello World";
    
    // 基本类型包装类的缓存
    public static final Integer CACHED_INTEGER = 127;  // 在缓存范围内
    public static final Integer LARGE_INTEGER = 1000;  // 超出缓存范围
    
    public void demonstratePooling() {
        // 字符串常量池
        String s1 = "Hello World";
        String s2 = POOLED_STRING;
        System.out.println(s1 == s2);  // true，引用相同对象
        
        // Integer缓存（-128到127）
        Integer i1 = 127;
        Integer i2 = CACHED_INTEGER;
        System.out.println(i1 == i2);  // true，引用相同对象
        
        Integer i3 = 1000;
        Integer i4 = LARGE_INTEGER;
        System.out.println(i3 == i4);  // false，不同对象
    }
}
```

### 避免重复计算

```java
public class CalculationConstants {
    // ✅ 预计算复杂表达式
    public static final double SQRT_2 = Math.sqrt(2.0);
    public static final long MILLISECONDS_PER_DAY = 24L * 60L * 60L * 1000L;
    public static final Pattern EMAIL_PATTERN = Pattern.compile(
        "^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$"
    );
    
    // ❌ 避免在使用时重复计算
    public void badExample() {
        for (int i = 0; i < 1000; i++) {
            double value = Math.sqrt(2.0);  // 重复计算
            Pattern pattern = Pattern.compile("...");  // 重复编译
        }
    }
    
    // ✅ 使用预定义常量
    public void goodExample() {
        for (int i = 0; i < 1000; i++) {
            double value = SQRT_2;  // 使用预计算值
            Matcher matcher = EMAIL_PATTERN.matcher(email);  // 使用预编译模式
        }
    }
}
```

## 总结

### 最佳实践清单

1. **明确常量定义**：只有不可变对象才是真正的常量
2. **使用工具类**：通过不可实例化的工具类组织常量，而非接口
3. **遵循命名规范**：使用 `CONSTANT_CASE` 风格，名称要有意义
4. **消除魔法数字**：所有有意义的数字都应定义为常量
5. **合理分组**：按功能模块组织常量，使用嵌套类或独立类
6. **选择合适类型**：优先使用枚举定义相关常量组
7. **确保不可变性**：集合常量要使用不可修改的包装
8. **添加文档**：为复杂常量添加必要的注释说明
9. **考虑性能**：利用常量池，避免重复计算
10. **编写测试**：验证常量值的正确性和不可变性

### 常见错误总结

- 将可变对象声明为 `static final`
- 使用接口定义常量（常量接口反模式）
- 不遵循 `CONSTANT_CASE` 命名规范
- 在代码中使用魔法数字
- 没有合理组织和分类常量
- 忽略集合常量的不可变性要求

通过遵循这些原则和最佳实践，可以编写出更加清晰、可维护和高效的Java代码。

## 扩展阅读

- Effective Java Item 22: Use interfaces only to define types
- Effective Java Item 25: Limit source files to a single top-level class
- Java Language Specification: Constants
- Google Java Style Guide: Constants
- Clean Code: Meaningful Names
