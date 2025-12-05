# Magic Number 魔数

## tl;dr

- 优先使用**抽取枚举类型、抽取配置、抽取常量**三种方式处理硬编码。

## 魔数

魔数指的是在代码中硬编码的数字常量，例如：

```java
if (statusCode == 404 || packageSize < 2000) { // Both are magic Number!
    return false
}

```

硬编码会带来以下问题：
- 难以阅读：在代码中 hardcode 的数字经常难以理解。读者不知道这些数字实际上代表什么。
- 难以维护：如果我们硬编码了数字，在以后可能需要改变数字，比如将 404 改为 500。我们必须查找所有使用该数字的函数并更新每个实例。
- 难以修改：hardcode 的数字是在源代码中硬编码的，这意味着我们必须重新编译程序，而无法动态地更改数字。如果这些数字可能会改变，我们必须在代码编辑期间重新编译应用程序。

一个数字是否是魔数，并不取决于它是否是 0 或是 1，而是取决于比起硬编码的数字是否难以阅读、维护和修改。

考虑以下例子：

```java
// 0 表示竖屏， 1 表示 横屏， 2 表示全屏
private int setScreenMode(int mode) {
}

```

这几个数字改成 325， 3342， 343234 也没什么区别。它们的可读性一样差。它们应该被抽取为枚举类型。

对于硬编码的数字，通常有以下四种策略：保持硬编码、替换为枚举(Enum)类型、替换为常量(Constant)、替换为配置(Config)。在选择时，可以考虑以下决策树：

- 适合枚举时，优先考虑枚举。适合枚举的场景是：
  - 只有有限个值、每个值有明确具体含义、相对稳定的属性
- 适合配置时，优先考虑配置。适合配置的场景是：
  - 如果值需要在不同环境下更改
  - 如果值在运行时被计算，使用配置文件
  - 值会因为外部的需求变更进行频繁调整
- 除以上特定情况，在抽取常量和硬编码间做选择。这两者的界限较为模糊，具体地：
  - 有**上下文无关**的明确含义的数字，应该抽取为常量。例如，在 `perimeter = 2 * 3.1415926535 * radius` 中， `3.1415926535` 是有明确含义的 -- 圆周率，应该被抽取为 `pi`，但 `2` 抛离上下文，是没有明确含义的。
  - 如果同一个数字在**多处**被用到，应该抽取为常量
  - 如果只是一次性的、不影响阅读的、用于少量代码，可以使用硬编码。例如，在调用 API 时设置（值并不会变化的）缓冲区大小
  - 数学表达式中的没有确切含义的数字，可以使用硬编码
  - 通常，比起硬编码，倾向于使用常量

## 示例

以下示例简单地说明使用非硬编码的处理方案：

```java
// 使用配置
Config config = Config.readFrom("config.yaml");

// 使用常量
private static final int NOT_FOUND_STATUS_CODE = 404;

if (statusCode == NOT_FOUND_STATUS_CODE || packageSize < config.MaxPackageSize()) {
    return false;
}

// HTTP Code 也可以抽象为枚举
public enum HttpStatus {

    OK(200),
    CREATED(201),
    NO_CONTENT(204),
    NOT_FOUND(404);

    private int code;

    HttpStatus(int code) {
        this.code = code;
    }

    public int getCode() {
        return code;
    }
}
```

## Readability 示例

```java
// 原始代码：
/**
 * cmwap下，http连接方式 0 x-online-host;
 * 根据请求参数决定是否使用：1 直连/x-online-host; 2 默认代理/x-online-host;
 * 忽略请求参数，强制使用：4 直连/x-online-host; 8 默认代理/x-online-host;
 */
public volatile int mCmwapConTypeFromDpc = 4; //因为当前dpc配置值为4，所以这里默认值写为4

// 使用枚举：
public enum ConnectionMode {
    Direct(0), // cmwap下，http连接方式 0 x-online-host;
    // 根据请求参数决定是否使用:
    DirectWithRequest(1),
    DefaultProxyWithRequest(2),
    // 忽略请求参数，强制使用:
    DirectIgnoringRequest(4),
    DefaultProxyIgnoringRequest(8);
}

```

## 常见魔数处理模式

### 业务状态码使用枚举

```java
// ❌ 错误做法
if (orderStatus == 1) {
    // 处理待支付
} else if (orderStatus == 2) {
    // 处理已支付
}

// ✅ 正确做法
public enum OrderStatus {
    PENDING(1, "待支付"),
    PAID(2, "已支付"),
    CANCELLED(3, "已取消");
    
    private final int code;
    private final String description;
    
    OrderStatus(int code, String description) {
        this.code = code;
        this.description = description;
    }
}

if (order.getStatus() == OrderStatus.PENDING) {
    // 处理待支付
}
```

### 配置参数使用配置文件

```java
// ❌ 错误做法
private static final int MAX_RETRY_COUNT = 3;
private static final int TIMEOUT_SECONDS = 30;

// ✅ 正确做法
@ConfigurationProperties("app.retry")
public class RetryConfig {
    private int maxCount = 3;
    private int timeoutSeconds = 30;
    // getters and setters
}
```

### 数学常量使用命名常量

```java
// ❌ 错误做法
double area = 3.14159 * radius * radius;

// ✅ 正确做法
private static final double PI = 3.14159;
double area = PI * radius * radius;

// 或使用标准库
double area = Math.PI * radius * radius;
```

## 何时保留硬编码

以下场景可以保留硬编码：

1. **UI 布局参数**：边距、间距等视觉相关的数值
2. **数组索引**：`array[0]`、`list.get(1)` 等
3. **数学表达式中的系数**：`2 * radius`（表示直径）
4. **一次性使用的缓冲区大小**

```java
// 这些硬编码是可以接受的
button.setPadding(8, 16, 8, 16);  // UI间距
String firstItem = items.get(0);   // 数组索引
int diameter = 2 * radius;         // 数学关系
byte[] buffer = new byte[1024];    // 缓冲区大小
```

## 反模式：过度抽取常量

```java
// ❌ 不要这样做 - 过度抽取
public class Constants {
    public static final int ZERO = 0;
    public static final int ONE = 1;
    public static final int TWO = 2;
    public static final String EMPTY_STRING = "";
}

// 这样的"常量"没有任何意义
if (count == Constants.ZERO) {
    return Constants.EMPTY_STRING;
}
```

## 最佳实践总结

1. **优先级**：枚举 > 配置 > 常量 > 硬编码
2. **命名**：常量名应该表达业务含义，而非数值本身
3. **位置**：相关常量应该组织在一起，便于维护
4. **文档**：复杂的常量应该添加注释说明其用途和来源
