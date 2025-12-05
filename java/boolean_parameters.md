# Boolean Parameters 布尔类型参数设计规范

## tl;dr

- 布尔型参数通常是不优雅的设计。如果可能，考虑其它方案。
- 如果布尔型参数指示**正交**的执行路径，考虑拆分方法
- 如果布尔型参数表示**两种（但并非完全相反、或者可能扩展）的枚举状态**，考虑改用枚举
- 除此之外，不要过度追求避免布尔型参数
- 布尔型参数本质上是**魔数**。传入参数时，应该尽量为布尔型添加名字作为注释，如 `/* shouldWork= */ true`。（如果是 Kotlin，布尔型参数应该总是带有名字）

## 避免布尔型入参控制函数的两种正交行为：拆分方法或者抽取 Option 参数

既然两个函数是正交的（‘非黑即白’这种明确对立的情况），通常情况下，拆分成两个方法是更好的选择：

### 反例

```java
public void processData(boolean isLegacyMode) {
    if (isLegacyMode) {
        // 旧逻辑(200行代码)
    } else {
        // 新逻辑(完全不同的150行代码)
    }
}
```

### 正例

```java
public void processDataLegacy() {
    // 旧逻辑专有方法
}

public void processDataModern() {
    // 新逻辑专有方法
}
```

考虑以下例子， `runAdditionalChecks` 作为一个成员变量；
因为 `runAdditionalChecks` 并不会正交地控制逻辑行为，只影响其中一小部分；强行拆分函数，则会平添无谓的复杂性而没有实际收益：

### 反例

```java
class Controller {
    private final boolean runAdditionalChecks;

    private Controller(boolean runAdditionalChecks) {
        this.runAdditionalChecks = runAdditionalChecks;
    }

    static Controller create() {
        return new Controller(false);
    }

    static Controller createWithRunAdditionalChecks() {
        return new Controller(true);
    }

    public void processData() {
        // 其他业务逻辑-1
        if (runAdditionalChecks) {
            // 一段小的局部检查逻辑
        }
        // 其他业务逻辑-2
    }
}
```

### 正例

```java
class Controller {
    private final boolean runAdditionalChecks;

    Controller(boolean runAdditionalChecks) {
      this.runAdditionalChecks = runAdditionalChecks;
    }

    public void processData() {
      // 其他业务逻辑-1
      if (runAdditionalChecks) {
          // 一段小的局部检查逻辑

      }
      // 其他业务逻辑-2
    }
}
```

## 避免布尔型入参表示两种状态：应该使用 enum

有时候，一个属性只有两种状态，例如，方向是垂直或者水平。这时，一个常见的模式是使用 boolean 的两个值表示两种状态：

```java
public void setOrientation(boolean vertical) {
  // ...
}
```

这是一个不好的实践。更好的办法是使用 `enum`：

### 反例

```java
public void configure(boolean isHighPriority, boolean isBatchMode) {
    // 难以理解参数含义（2个boolean最多标识4种含义，如果实际业务只有3种，多余的这一种可能就是隐藏bug）
}
```

### 正例

```java
public enum ProcessMode {
    HIGH_PRIORITY,
    BATCH,
    INTERACTIVE
}

public void configure(ProcessMode mode) {
    // 清晰明确
    if (mode == ProcessMode.HIGH_PRIORITY) {
        // do something
    } else if (mode == ProcessMode.BATCH) {
        // do something
    } else if (mode == ProcessMode.INTERACTIVE) {
        // do something
    }
}
```

## 多 boolean 参数使用方式

### 反例

```java
widget.setVisible(true, false, true); // 难以理解参数含义
```

### 正例 1：使用 Builder 模式

```java
widget.setVisibility()
    .showHeader(true)
    .showFooter(false)
    .showBorder(true)
    .apply();
```

### 正例 2：使用参数对象

```java
class VisibilityOptions {
    boolean showHeader;
    boolean showFooter;
    boolean showBorder;
}
VisibilityOptions options = new VisibilityOptions();
options.showHeader = true;
options.showFooter = false;
options.showBorder = true;
widget.setVisibility(options);
```

## 测试友好性考虑

boolean 参数会增加测试用例的组合爆炸：

- 1 个布尔参数：2 种情况
- 2 个布尔参数：4 种情况
- 3 个布尔参数：8 种情况

### 反例：

```java
public void process(boolean validate, boolean log, boolean async) {
    // 需要测试8种组合
    assert validate == true && log == true && async == true;
    assert validate == false && log == false && async == false;
    assert validate == true && log == true && async == false;
    assert validate == true && log == false && async == true;
    assert validate == false && log == true && async == true;
    assert validate == false && log == false && async == true;
    assert validate == false && log == true && async == false;
    assert validate == true && log == false && async == false;
}
```

### 正例：使用策略模式（也可以使用上述的 enum 方式）

```java
public interface ProcessingStrategy {
    void execute();
}

public class AsyncStrategy implements ProcessingStrategy {
    // 单一职责，易于测试
    @Override
    public void execute() {
        // 执行异步处理逻辑
        System.out.println("执行异步处理策略");
    }
}
```

## 布尔参数的命名规范

良好的命名可以让布尔参数的含义更加清晰，减少误解：

### 反例：

```java
public void process(boolean flag) {
    // flag 的含义不明确
}

public void setState(boolean state) {
    // state 的含义模糊
}
```

### 正例：

```java
public void process(boolean shouldValidateInput) {
    // 明确表示是否应该验证输入
}

public void setEnabled(boolean isEnabled) {
    // 明确表示是否启用
}

public void setVisible(boolean shouldBeVisible) {
    // 明确表示是否应该可见
}
```

## API 设计中的布尔参数最佳实践

在公共 API 设计中，应该尽量避免布尔参数，提供更清晰的接口：

### 反例：

```java
// API 中的布尔参数容易引起混淆
public void sendEmail(String to, String subject, String body, boolean isHtml);

// 调用时容易出错
emailService.sendEmail("user@example.com", "Hello", "<h1>World</h1>", false); // 错误！
```

### 正例：

```java
// 使用重载方法提供清晰的接口
public void sendTextEmail(String to, String subject, String body);
public void sendHtmlEmail(String to, String subject, String body);

// 调用时含义明确
emailService.sendTextEmail("user@example.com", "Hello", "World");
emailService.sendHtmlEmail("user@example.com", "Hello", "<h1>World</h1>");
```

## 配置类中的布尔参数处理

在配置类中，多个布尔参数应该使用更结构化的方式：

### 反例：

```java
public class DatabaseConfig {
    private boolean useSSL;
    private boolean useConnectionPool;
    private boolean enableLogging;
    private boolean enableMetrics;

    public DatabaseConfig(boolean useSSL, boolean useConnectionPool,
                         boolean enableLogging, boolean enableMetrics) {
        // 参数顺序容易搞错
    }
}
```

### 正例：

```java
public class DatabaseConfig {
    private final SecurityMode securityMode;
    private final ConnectionMode connectionMode;
    private final LoggingLevel loggingLevel;
    private final MetricsConfig metricsConfig;

    public DatabaseConfig(SecurityMode securityMode, ConnectionMode connectionMode,
                         LoggingLevel loggingLevel, MetricsConfig metricsConfig) {
        // 类型安全，含义明确
    }
}

public enum SecurityMode {
    SSL_ENABLED, SSL_DISABLED
}

public enum ConnectionMode {
    POOLED, DIRECT
}
```

## 扩展阅读

- [Clean Code: Function Arguments](https://learning.oreilly.com/library/view/clean-code/9780136083238/) - Robert Martin 关于函数参数设计的经典论述
- [Effective Java Item 52](https://learning.oreilly.com/library/view/effective-java-3rd/9780134686097/) - 慎用重载和可变参数
- [Kotlin Named Arguments](https://kotlinlang.org/docs/functions.html#named-arguments) - Kotlin 的命名参数解决方案
- [API Design Guidelines](https://swift.org/documentation/api-design-guidelines/) - Swift 语言的 API 设计原则，对布尔参数有独到见解
- [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html) - 布尔参数相关规范
