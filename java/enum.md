# Enum 枚举

## tl;dr

- **比起 int 常量，鼓励使用 enum**。枚举提供类型安全、命名空间和更好的可读性。
- **永远不要使用 `ordinal()` 方法**。使用实例字段存储与枚举常量关联的数据，使用 Instance Field。
- **谨慎判断 `default` 语句是否需要**。如果 enum 使用范围可控，不要使用 `default`。
- **使用 EnumSet 替代位字段**。EnumSet 提供更好的性能和类型安全。
- **使用 EnumMap 替代序数索引数组**。EnumMap 是专为枚举键设计的高效映射实现。

## 比起 int 常量，鼓励使用 enum

### 整型常量模式的问题
### 反例
```java
// ❌ 整型常量模式（不推荐）
public class IntConstantExample {
    // 苹果品种
    public static final int APPLE_FUJI = 0;
    public static final int APPLE_PIPPIN = 1;
    public static final int APPLE_GRANNY_SMITH = 2;
    
    // 橘子品种
    public static final int ORANGE_NAVEL = 0;
    public static final int ORANGE_TEMPLE = 1;
    public static final int ORANGE_BLOOD = 2;
    
    // 问题1：类型不安全
    public void compareApples(int apple1, int apple2) {
        // 编译器无法阻止这种错误用法
        if (apple1 == ORANGE_NAVEL) {  // 比较苹果和橘子！
            System.out.println("This shouldn't happen!");
        }
    }
    
    // 问题2：命名空间污染
    // APPLE_FUJI 和 ORANGE_NAVEL 都是 0，容易混淆
    
    // 问题3：脆弱性
    // 如果改变常量值，所有使用该常量的客户端都需要重新编译
    
    // 问题4：难以调试
    public void printApple(int apple) {
        System.out.println(apple);  // 输出 "0"，没有意义
    }
}
```

### 正例
```java
// ✅ 枚举模式（推荐）
public enum Apple {
    FUJI, PIPPIN, GRANNY_SMITH
}

public enum Orange {
    NAVEL, TEMPLE, BLOOD
}

public class EnumExample {
    // 类型安全：编译时检查
    public void compareApples(Apple apple1, Apple apple2) {
        // if (apple1 == Orange.NAVEL) {  // 编译错误！
        if (apple1 == Apple.FUJI) {
            System.out.println("It's a Fuji apple!");
        }
    }
    
    // 有意义的字符串表示
    public void printApple(Apple apple) {
        System.out.println(apple);  // 输出 "FUJI"，清晰明了
    }
    
    // 可以在 switch 中使用
    public String getAppleDescription(Apple apple) {
        switch (apple) {
            case FUJI:
                return "Sweet and crispy";
            case PIPPIN:
                return "Tart and firm";
            case GRANNY_SMITH:
                return "Very tart";
            default:
                throw new AssertionError("Unknown apple: " + apple);
        }
    }
}
```

## 永远不要使用 ordinal() 方法

`ordinal()` 方法返回枚举常量在枚举声明中的位置（从0开始）。**永远不要根据枚举的序数来派生与它关联的值**。

### ordinal() 的问题
### 反例
```java
// ❌ 错误：依赖 ordinal() 方法
public enum Ensemble {
    SOLO, DUET, TRIO, QUARTET, QUINTET, SEXTET, SEPTET, OCTET, NONET, DECTET;
    
    // 危险的实现
    public int numberOfMusicians() {
        return ordinal() + 1;
    }
}

// 问题：如果重新排序或添加新常量，ordinal 值会改变
public enum EnsembleWithProblems {
    // 如果添加一个新的常量到开头
    DOUBLE_QUARTET(8),  // 想要表示8个音乐家的组合
    SOLO, DUET, TRIO, QUARTET, QUINTET, SEXTET, SEPTET, OCTET, NONET, DECTET;
    
    // 现在 SOLO.ordinal() 返回 1 而不是 0！
    public int numberOfMusicians() {
        return ordinal() + 1;  // SOLO 现在返回 2，错误！
    }
}
```

### 正确做法：使用实例字段
### 正例
```java
// ✅ 正确：使用实例字段
public enum Ensemble {
    SOLO(1), DUET(2), TRIO(3), QUARTET(4), QUINTET(5),
    SEXTET(6), SEPTET(7), OCTET(8), DOUBLE_QUARTET(8),
    NONET(9), DECTET(10), TRIPLE_QUARTET(12);
    
    private final int numberOfMusicians;
    
    Ensemble(int size) {
        this.numberOfMusicians = size;
    }
    
    public int numberOfMusicians() {
        return numberOfMusicians;
    }
}

// 使用示例
public class MusicExample {
    public void demonstrateEnsemble() {
        System.out.println(Ensemble.QUARTET.numberOfMusicians());      // 4
        System.out.println(Ensemble.DOUBLE_QUARTET.numberOfMusicians()); // 8
        
        // 即使重新排序枚举常量，结果也不会改变
    }
}
```

## 枚举中的字段和方法

### 基本字段和方法
### 正例
```java
public enum HttpStatus {
    // 2xx Success
    OK(200, "OK"),
    CREATED(201, "Created"),
    ACCEPTED(202, "Accepted"),
    
    // 4xx Client Error
    BAD_REQUEST(400, "Bad Request"),
    UNAUTHORIZED(401, "Unauthorized"),
    FORBIDDEN(403, "Forbidden"),
    NOT_FOUND(404, "Not Found"),
    
    // 5xx Server Error
    INTERNAL_SERVER_ERROR(500, "Internal Server Error"),
    BAD_GATEWAY(502, "Bad Gateway"),
    SERVICE_UNAVAILABLE(503, "Service Unavailable");
    
    private final int code;
    private final String reasonPhrase;
    
    HttpStatus(int code, String reasonPhrase) {
        this.code = code;
        this.reasonPhrase = reasonPhrase;
    }
    
    public int getCode() {
        return code;
    }
    
    public String getReasonPhrase() {
        return reasonPhrase;
    }
    
    public boolean isSuccessful() {
        return code >= 200 && code < 300;
    }
    
    public boolean isClientError() {
        return code >= 400 && code < 500;
    }
    
    public boolean isServerError() {
        return code >= 500 && code < 600;
    }
    
    // 根据状态码查找枚举
    public static HttpStatus valueOf(int code) {
        for (HttpStatus status : values()) {
            if (status.code == code) {
                return status;
            }
        }
        throw new IllegalArgumentException("Unknown HTTP status code: " + code);
    }
    
    @Override
    public String toString() {
        return code + " " + reasonPhrase;
    }
}
```

### 抽象方法和特定于常量的方法实现
### 正例
```java
public enum Operation {
    PLUS("+") {
        @Override
        public double apply(double x, double y) {
            return x + y;
        }
    },
    MINUS("-") {
        @Override
        public double apply(double x, double y) {
            return x - y;
        }
    },
    TIMES("*") {
        @Override
        public double apply(double x, double y) {
            return x * y;
        }
    },
    DIVIDE("/") {
        @Override
        public double apply(double x, double y) {
            return x / y;
        }
    };
    
    private final String symbol;
    
    Operation(String symbol) {
        this.symbol = symbol;
    }
    
    @Override
    public String toString() {
        return symbol;
    }
    
    // 抽象方法，每个枚举常量必须实现
    public abstract double apply(double x, double y);
    
    // 使用示例
    public static void main(String[] args) {
        double x = 2.0;
        double y = 4.0;
        
        for (Operation op : Operation.values()) {
            System.out.printf("%.1f %s %.1f = %.1f%n", x, op, y, op.apply(x, y));
        }
        // 输出：
        // 2.0 + 4.0 = 6.0
        // 2.0 - 4.0 = -2.0
        // 2.0 * 4.0 = 8.0
        // 2.0 / 4.0 = 0.5
    }
}
```

### 策略枚举模式
### 正例
```java
public enum PayrollDay {
    MONDAY(PayType.WEEKDAY),
    TUESDAY(PayType.WEEKDAY),
    WEDNESDAY(PayType.WEEKDAY),
    THURSDAY(PayType.WEEKDAY),
    FRIDAY(PayType.WEEKDAY),
    SATURDAY(PayType.WEEKEND),
    SUNDAY(PayType.WEEKEND);
    
    private final PayType payType;
    
    PayrollDay(PayType payType) {
        this.payType = payType;
    }
    
    public int pay(int minutesWorked, int payRate) {
        return payType.pay(minutesWorked, payRate);
    }
    
    // 策略枚举
    private enum PayType {
        WEEKDAY {
            @Override
            int overtimePay(int minutesWorked, int payRate) {
                return minutesWorked <= MINUTES_PER_SHIFT ? 0 :
                    (minutesWorked - MINUTES_PER_SHIFT) * payRate / 2;
            }
        },
        WEEKEND {
            @Override
            int overtimePay(int minutesWorked, int payRate) {
                return minutesWorked * payRate / 2;
            }
        };
        
        abstract int overtimePay(int minutesWorked, int payRate);
        private static final int MINUTES_PER_SHIFT = 8 * 60;
        
        int pay(int minutesWorked, int payRate) {
            int basePay = minutesWorked * payRate;
            return basePay + overtimePay(minutesWorked, payRate);
        }
    }
}
```

## 谨慎判断 `default` 语句是否需要

### 何时省略 `default` 分支

```java
public enum Color {
    RED, GREEN, BLUE
}

public class ColorProcessor {
    // ✅ 推荐：省略 default，获得编译时检查
    public String getColorDescription(Color color) {
        switch (color) {
            case RED:
                return "The color of passion";
            case GREEN:
                return "The color of nature";
            case BLUE:
                return "The color of sky";
            // 故意省略 default
        }
        // 如果添加新的 Color 枚举值，编译器会警告这里可能到达
        throw new AssertionError("Unknown color: " + color);
    }
    
    // ❌ 不推荐：使用 default 会掩盖新增枚举值的问题
    public String getColorDescriptionWithDefault(Color color) {
        switch (color) {
            case RED:
                return "The color of passion";
            case GREEN:
                return "The color of nature";
            case BLUE:
                return "The color of sky";
            default:
                return "Unknown color";  // 新增枚举值会默默地走到这里
        }
    }
}
```

### 何时使用 `default` 分支
### 正例
```java
public class ColorProcessor {
    // ✅ 适合使用 default：处理外部输入或向后兼容
    public String processExternalColor(Color color) {
        switch (color) {
            case RED:
                return "Process red";
            case GREEN:
                return "Process green";
            case BLUE:
                return "Process blue";
            default:
                // 处理可能的新枚举值或损坏的数据
                logger.warn("Unexpected color value: {}", color);
                return "Process as default";
        }
    }
    
    // ✅ 适合使用 default：部分处理场景
    public boolean isPrimaryColor(Color color) {
        switch (color) {
            case RED: // fall through
            case GREEN: // fall through
            case BLUE: // fall through
                // 以上三种颜色都是原色，返回true
                return true;
            default:
                return false;  // 其他所有颜色都不是原色
        }
    }
}
```

## EnumSet：替代位字段的最佳选择

### 传统位字段的问题
### 反例
```java
// ❌ 传统位字段模式（不推荐）
public class Text {
    public static final int STYLE_BOLD = 1 << 0;        // 1
    public static final int STYLE_ITALIC = 1 << 1;      // 2
    public static final int STYLE_UNDERLINE = 1 << 2;   // 4
    public static final int STYLE_STRIKETHROUGH = 1 << 3; // 8
    
    // 问题1：类型不安全
    public void applyStyles(int styles) {
        // 可以传入任意 int 值，包括无效组合
    }
    
    // 问题2：难以调试
    public void printStyles(int styles) {
        System.out.println(styles);  // 输出数字，如 "5"，不直观
    }
    
    // 问题3：固定位数限制
    // 最多只能有 32 个选项（int 的位数）
    
    // 使用示例
    public static void main(String[] args) {
        Text text = new Text();
        // 应用粗体和斜体
        text.applyStyles(STYLE_BOLD | STYLE_ITALIC);  // 传入 3
    }
}
```

### EnumSet 的优势
### 正例
```java
// ✅ 使用 EnumSet（推荐）
public enum Style {
    BOLD, ITALIC, UNDERLINE, STRIKETHROUGH
}

public class Text {
    // 类型安全的方法签名
    public void applyStyles(Set<Style> styles) {
        System.out.println("Applying styles: " + styles);
        // 输出：Applying styles: [BOLD, ITALIC]，清晰直观
        
        for (Style style : styles) {
            switch (style) {
                case BOLD:
                    System.out.println("Making text bold");
                    break;
                case ITALIC:
                    System.out.println("Making text italic");
                    break;
                case UNDERLINE:
                    System.out.println("Underlining text");
                    break;
                case STRIKETHROUGH:
                    System.out.println("Striking through text");
                    break;
            }
        }
    }
    
    // 使用示例
    public static void main(String[] args) {
        Text text = new Text();
        
        // 创建 EnumSet 的多种方式
        Set<Style> styles1 = EnumSet.of(Style.BOLD, Style.ITALIC);
        Set<Style> styles2 = EnumSet.allOf(Style.class);
        Set<Style> styles3 = EnumSet.noneOf(Style.class);
        Set<Style> styles4 = EnumSet.complementOf(EnumSet.of(Style.BOLD));
        
        text.applyStyles(styles1);
        
        // EnumSet 支持所有 Set 操作
        styles1.add(Style.UNDERLINE);
        styles1.remove(Style.ITALIC);
        
        // 高效的批量操作
        Set<Style> boldAndItalic = EnumSet.of(Style.BOLD, Style.ITALIC);
        Set<Style> underlineAndStrike = EnumSet.of(Style.UNDERLINE, Style.STRIKETHROUGH);
        
        Set<Style> union = EnumSet.copyOf(boldAndItalic);
        union.addAll(underlineAndStrike);  // 并集
        
        Set<Style> intersection = EnumSet.copyOf(boldAndItalic);
        intersection.retainAll(underlineAndStrike);  // 交集
    }
}
```

### EnumSet 的性能特点
### 正例
```java
public class EnumSetPerformance {
    public enum LargeEnum {
        // 假设有很多枚举值
        VALUE_1, VALUE_2, VALUE_3, /* ... */ VALUE_100
    }
    
    public void demonstratePerformance() {
        // EnumSet 内部使用位向量实现
        // 对于枚举值 <= 64 个，使用单个 long
        // 对于枚举值 > 64 个，使用 long 数组
        
        Set<LargeEnum> enumSet = EnumSet.noneOf(LargeEnum.class);
        Set<LargeEnum> hashSet = new HashSet<>();
        
        // EnumSet 的优势：
        // 1. 空间效率：每个枚举值只占用一个位
        // 2. 时间效率：所有基本操作都是常数时间
        // 3. 批量操作：如 addAll, removeAll, retainAll 都非常高效
        
        long startTime = System.nanoTime();
        
        // EnumSet 操作
        for (LargeEnum value : LargeEnum.values()) {
            enumSet.add(value);
        }
        
        long enumSetTime = System.nanoTime() - startTime;
        
        startTime = System.nanoTime();
        
        // HashSet 操作
        for (LargeEnum value : LargeEnum.values()) {
            hashSet.add(value);
        }
        
        long hashSetTime = System.nanoTime() - startTime;
        
        System.out.println("EnumSet time: " + enumSetTime + " ns");
        System.out.println("HashSet time: " + hashSetTime + " ns");
        // EnumSet 通常比 HashSet 快得多
    }
}
```

## EnumMap：专为枚举键设计的映射

### 传统数组索引的问题
### 反例
```java
// ❌ 使用 ordinal() 作为数组索引（不推荐）
public enum Phase {
    SOLID, LIQUID, GAS
}

public class PhaseTransition {
    // 危险的实现
    private static final String[][] TRANSITIONS = {
        {"N/A", "melt", "sublime"},      // SOLID
        {"freeze", "N/A", "boil"},       // LIQUID  
        {"deposit", "condense", "N/A"}   // GAS
    };
    
    // 脆弱的方法
    public static String transition(Phase from, Phase to) {
        return TRANSITIONS[from.ordinal()][to.ordinal()];
    }
    
    // 问题：
    // 1. 如果枚举顺序改变，数组索引就错了
    // 2. 如果添加新的 Phase，必须记住更新数组
    // 3. 数组大小必须是 n²，即使很多组合无效
    // 4. 编译器无法检查数组和枚举的对应关系
}
```

### EnumMap 的优势
### 正例
```java
// ✅ 使用 EnumMap（推荐）
public enum Phase {
    SOLID, LIQUID, GAS;
    
    public enum Transition {
        MELT(SOLID, LIQUID),
        FREEZE(LIQUID, SOLID),
        BOIL(LIQUID, GAS),
        CONDENSE(GAS, LIQUID),
        SUBLIME(SOLID, GAS),
        DEPOSIT(GAS, SOLID);
        
        private final Phase from;
        private final Phase to;
        
        Transition(Phase from, Phase to) {
            this.from = from;
            this.to = to;
        }
        
        // 使用嵌套 EnumMap 构建转换表
        private static final Map<Phase, Map<Phase, Transition>> transitions =
            Stream.of(values())
                .collect(groupingBy(
                    t -> t.from,
                    () -> new EnumMap<>(Phase.class),
                    toMap(t -> t.to, t -> t, (x, y) -> y, () -> new EnumMap<>(Phase.class))
                ));
        
        public static Transition from(Phase from, Phase to) {
            return transitions.get(from).get(to);
        }
    }
}

// 使用示例
public class PhaseTransitionExample {
    public static void main(String[] args) {
        // 类型安全的查找
        Phase.Transition transition = Phase.Transition.from(Phase.SOLID, Phase.LIQUID);
        System.out.println(transition);  // 输出：MELT
        
        // 如果添加新的 Phase，编译器会强制更新所有相关代码
    }
}
```

### EnumMap 的基本用法
### 正例
```java
public class EnumMapExample {
    public enum Day {
        MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY
    }
    
    public void demonstrateEnumMap() {
        // 创建 EnumMap
        Map<Day, String> activities = new EnumMap<>(Day.class);
        
        // 添加映射
        activities.put(Day.MONDAY, "Start the week");
        activities.put(Day.TUESDAY, "Team meeting");
        activities.put(Day.WEDNESDAY, "Mid-week check");
        activities.put(Day.THURSDAY, "Project review");
        activities.put(Day.FRIDAY, "Week wrap-up");
        activities.put(Day.SATURDAY, "Weekend fun");
        activities.put(Day.SUNDAY, "Rest day");
        
        // 遍历（按枚举声明顺序）
        for (Map.Entry<Day, String> entry : activities.entrySet()) {
            System.out.println(entry.getKey() + ": " + entry.getValue());
        }
        
        // EnumMap 的特点：
        // 1. 键必须是同一个枚举类型
        // 2. 内部使用数组实现，性能优异
        // 3. 遍历顺序与枚举声明顺序一致
        // 4. 不允许 null 键，但允许 null 值
        
        System.out.println("Size: " + activities.size());
        System.out.println("Contains MONDAY: " + activities.containsKey(Day.MONDAY));
        System.out.println("Activity for FRIDAY: " + activities.get(Day.FRIDAY));
    }
    
    // 实际应用示例：统计枚举值出现次数
    public Map<Day, Integer> countDays(List<Day> days) {
        Map<Day, Integer> counts = new EnumMap<>(Day.class);
        
        // 初始化所有枚举值的计数为0
        for (Day day : Day.values()) {
            counts.put(day, 0);
        }
        
        // 统计
        for (Day day : days) {
            counts.put(day, counts.get(day) + 1);
        }
        
        return counts;
    }
}
```

## 枚举的高级特性

### 实现接口
### 正例
```java
public interface Describable {
    String getDescription();
}

public enum Planet implements Describable {
    MERCURY("The smallest planet"),
    VENUS("The hottest planet"),
    EARTH("Our home planet"),
    MARS("The red planet");
    
    private final String description;
    
    Planet(String description) {
        this.description = description;
    }
    
    @Override
    public String getDescription() {
        return description;
    }
    
    // 枚举还可以实现多个接口
}

// 使用接口引用
public class PlanetExample {
    public void printDescriptions(Describable[] items) {
        for (Describable item : items) {
            System.out.println(item.getDescription());
        }
    }
    
    public static void main(String[] args) {
        PlanetExample example = new PlanetExample();
        example.printDescriptions(Planet.values());
    }
}
```

### 枚举中的静态方法
### 正例
```java
public enum Currency {
    USD("US Dollar", "$"),
    EUR("Euro", "€"),
    GBP("British Pound", "£"),
    JPY("Japanese Yen", "¥"),
    CNY("Chinese Yuan", "¥");
    
    private final String fullName;
    private final String symbol;
    
    Currency(String fullName, String symbol) {
        this.fullName = fullName;
        this.symbol = symbol;
    }
    
    public String getFullName() { return fullName; }
    public String getSymbol() { return symbol; }
    
    // 静态方法：根据符号查找货币
    public static Currency findBySymbol(String symbol) {
        for (Currency currency : values()) {
            if (currency.symbol.equals(symbol)) {
                return currency;
            }
        }
        throw new IllegalArgumentException("No currency with symbol: " + symbol);
    }
    
    // 静态方法：获取所有符号
    public static Set<String> getAllSymbols() {
        return Arrays.stream(values())
                .map(Currency::getSymbol)
                .collect(Collectors.toSet());
    }
    
    // 静态方法：按全名排序
    public static List<Currency> sortedByFullName() {
        return Arrays.stream(values())
                .sorted(Comparator.comparing(Currency::getFullName))
                .collect(Collectors.toList());
    }
}
```

### 枚举单例模式
### 正例
```java
// ✅ 最佳的单例实现方式
public enum DatabaseConnection {
    INSTANCE;
    
    private Connection connection;
    
    // 枚举构造函数在类加载时调用，且只调用一次
    DatabaseConnection() {
        try {
            // 初始化数据库连接
            this.connection = DriverManager.getConnection(
                "jdbc:mysql:xx...);
        } catch (SQLException e) {
            throw new RuntimeException("Failed to create database connection", e);
        }
    }
    
    public Connection getConnection() {
        return connection;
    }
    
    public void executeQuery(String sql) {
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            // 处理结果
        } catch (SQLException e) {
            throw new RuntimeException("Query execution failed", e);
        }
    }
}

// 使用示例
public class DatabaseExample {
    public void useDatabase() {
        // 获取单例实例
        DatabaseConnection db = DatabaseConnection.INSTANCE;
        db.executeQuery("SELECT * FROM users");
        
        // 枚举单例的优势：
        // 1. 线程安全（JVM 保证）
        // 2. 序列化安全（防止反序列化创建新实例）
        // 3. 反射安全（无法通过反射创建新实例）
        // 4. 简洁明了
    }
}
```

## 枚举的序列化
### 正例
```java
public enum Status {
    ACTIVE(1, "Active"),
    INACTIVE(0, "Inactive"),
    PENDING(2, "Pending");
    
    private final int code;
    private final String description;
    
    Status(int code, String description) {
        this.code = code;
        this.description = description;
    }
    
    public int getCode() { return code; }
    public String getDescription() { return description; }
    
    // 枚举的序列化是安全的
    // JVM 保证反序列化时返回相同的枚举实例
    
    // 如果需要自定义序列化行为，可以实现这些方法：
    
    // 控制序列化时写入的内容
    private Object writeReplace() throws ObjectStreamException {
        // 默认情况下，只序列化枚举常量的名称
        return this;
    }
    
    // 控制反序列化时的行为
    private Object readResolve() throws ObjectStreamException {
        // 确保返回正确的枚举实例
        return Status.valueOf(this.name());
    }
}

// 序列化示例
public class SerializationExample {
    public void demonstrateSerialization() throws Exception {
        Status original = Status.ACTIVE;
        
        // 序列化
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        ObjectOutputStream oos = new ObjectOutputStream(baos);
        oos.writeObject(original);
        oos.close();
        
        // 反序列化
        ByteArrayInputStream bais = new ByteArrayInputStream(baos.toByteArray());
        ObjectInputStream ois = new ObjectInputStream(bais);
        Status deserialized = (Status) ois.readObject();
        ois.close();
        
        // 验证是同一个实例
        System.out.println(original == deserialized);  // true
        System.out.println(original.equals(deserialized));  // true
    }
}
```

## 枚举的性能考虑

### 内存使用
### 正例
```java
public class EnumMemoryUsage {
    // 枚举实例是单例，所有引用都指向同一个对象
    public void demonstrateMemoryEfficiency() {
        Status status1 = Status.ACTIVE;
        Status status2 = Status.ACTIVE;
        Status status3 = Status.ACTIVE;
        
        // 所有变量都引用同一个对象
        System.out.println(status1 == status2);  // true
        System.out.println(status2 == status3);  // true
        
        // 内存中只有一个 Status.ACTIVE 实例
    }
    
    // 枚举比较使用 == 而不是 equals()
    public void demonstrateComparison() {
        Status status = Status.ACTIVE;
        
        // ✅ 推荐：使用 == 比较枚举
        if (status == Status.ACTIVE) {
            System.out.println("Status is active");
        }
        
        // ✅ 也可以使用 equals()，但 == 更快
        if (status.equals(Status.ACTIVE)) {
            System.out.println("Status is active");
        }
        
        // == 比较的优势：
        // 1. 更快（直接比较引用）
        // 2. 空安全（如果 status 为 null，== 返回 false）
        // 3. 编译时检查
    }
}
```

### 性能最佳实践

```java
public class EnumPerformanceTips {
    public enum Color {
        RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, BLACK, WHITE
    }
    
    // ✅ 缓存 values() 结果
    private static final Color[] COLORS = Color.values();
    
    public void efficientIteration() {
        // ❌ 低效：每次调用 values() 都会创建新数组
        for (Color color : Color.values()) {
            process(color);
        }
        
        // ✅ 高效：使用缓存的数组
        for (Color color : COLORS) {
            process(color);
        }
    }
    
    // ✅ 使用 EnumSet 进行集合操作
    private static final Set<Color> WARM_COLORS = EnumSet.of(Color.RED, Color.YELLOW, Color.ORANGE);
    
    public boolean isWarmColor(Color color) {
        return WARM_COLORS.contains(color);  // O(1) 时间复杂度
    }
    
    // ✅ 使用 EnumMap 进行映射
    private static final Map<Color, String> COLOR_NAMES = new EnumMap<>(Color.class);
    static {
        COLOR_NAMES.put(Color.RED, "红色");
        COLOR_NAMES.put(Color.GREEN, "绿色");
        COLOR_NAMES.put(Color.BLUE, "蓝色");
        // ...
    }
    
    public String getColorName(Color color) {
        return COLOR_NAMES.get(color);  // O(1) 时间复杂度
    }
    
    private void process(Color color) {
        // 处理颜色
    }
}
```

## 常见陷阱和最佳实践

### 避免在枚举中使用可变字段

```java
// ❌ 错误：可变字段破坏了枚举的不变性
public enum BadExample {
    INSTANCE;
    
    private List<String> items = new ArrayList<>();  // 可变字段
    
    public void addItem(String item) {
        items.add(item);  // 修改枚举状态
    }
    
    public List<String> getItems() {
        return items;  // 暴露可变引用
    }
}

// ✅ 正确：使用不可变字段
public enum GoodExample {
    INSTANCE;
    
    private final List<String> items;
    
    GoodExample() {
        List<String> temp = new ArrayList<>();
        temp.add("default item");
        this.items = Collections.unmodifiableList(temp);
    }
    
    public List<String> getItems() {
        return items;  // 返回不可变视图
    }
}
```

### 正确处理枚举的 null 值

```java
public class NullHandling {
    public enum Status {
        ACTIVE, INACTIVE, PENDING
    }
    
    // ✅ 安全的枚举处理
    public String getStatusDescription(Status status) {
        if (status == null) {
            return "Unknown status";
        }
        
        switch (status) {
            case ACTIVE:
                return "Currently active";
            case INACTIVE:
                return "Currently inactive";
            case PENDING:
                return "Waiting for approval";
            default:
                return "Unexpected status: " + status;
        }
    }
    
    // ✅ 使用 Optional 处理可能为 null 的枚举
    public Optional<Status> parseStatus(String input) {
        if (input == null || input.trim().isEmpty()) {
            return Optional.empty();
        }
        
        try {
            return Optional.of(Status.valueOf(input.toUpperCase()));
        } catch (IllegalArgumentException e) {
            return Optional.empty();
        }
    }
}
```

### 枚举的扩展性考虑

```java
// ✅ 设计可扩展的枚举
public interface Operation {
    double apply(double x, double y);
}

public enum BasicOperation implements Operation {
    PLUS("+") {
        @Override
        public double apply(double x, double y) { return x + y; }
    },
    MINUS("-") {
        @Override
        public double apply(double x, double y) { return x - y; }
    };
    
    private final String symbol;
    
    BasicOperation(String symbol) {
        this.symbol = symbol;
    }
    
    @Override
    public String toString() { return symbol; }
}

// 扩展操作
public enum ExtendedOperation implements Operation {
    EXP("^") {
        @Override
        public double apply(double x, double y) { return Math.pow(x, y); }
    },
    REMAINDER("%") {
        @Override
        public double apply(double x, double y) { return x % y; }
    };
    
    private final String symbol;
    
    ExtendedOperation(String symbol) {
        this.symbol = symbol;
    }
    
    @Override
    public String toString() { return symbol; }
}

// 通用的操作处理
public class OperationProcessor {
    public static void test(Class<? extends Enum<? extends Operation>> opEnumType,
                           double x, double y) {
        for (Operation op : opEnumType.getEnumConstants()) {
            System.out.printf("%.1f %s %.1f = %.1f%n", x, op, y, op.apply(x, y));
        }
    }
    
    public static void main(String[] args) {
        test(BasicOperation.class, 4.0, 2.0);
        test(ExtendedOperation.class, 4.0, 2.0);
    }
}
```

## 枚举与其他模式的比较

### 枚举 vs 常量类

```java
// ❌ 常量类模式
public final class StatusConstants {
    public static final int ACTIVE = 1;
    public static final int INACTIVE = 0;
    public static final int PENDING = 2;
    
    private StatusConstants() {}
    
    // 问题：
    // 1. 类型不安全
    // 2. 没有命名空间
    // 3. 不能添加行为
    // 4. 难以调试
}

// ✅ 枚举模式
public enum Status {
    ACTIVE(1, "Active", true),
    INACTIVE(0, "Inactive", false),
    PENDING(2, "Pending", true);
    
    private final int code;
    private final String description;
    private final boolean allowsTransition;
    
    Status(int code, String description, boolean allowsTransition) {
        this.code = code;
        this.description = description;
        this.allowsTransition = allowsTransition;
    }
    
    // 类型安全的方法
    public boolean canTransitionTo(Status newStatus) {
        return this.allowsTransition && newStatus != this;
    }
    
    // 有意义的字符串表示
    @Override
    public String toString() {
        return description;
    }
    
    // 根据代码查找
    public static Status fromCode(int code) {
        for (Status status : values()) {
            if (status.code == code) {
                return status;
            }
        }
        throw new IllegalArgumentException("Invalid status code: " + code);
    }
}
```

### 枚举 vs 字符串常量

```java
// ❌ 字符串常量模式
public class StringConstantExample {
    public static final String STATUS_ACTIVE = "ACTIVE";
    public static final String STATUS_INACTIVE = "INACTIVE";
    
    public void processStatus(String status) {
        // 问题：容易出现拼写错误
        if ("ACTIV".equals(status)) {  // 拼写错误，编译器无法发现
            // 处理逻辑
        }
    }
}

// ✅ 枚举模式
public enum Status {
    ACTIVE, INACTIVE;
    
    public void process() {
        switch (this) {
            case ACTIVE:
                // 处理激活状态
                break;
            case INACTIVE:
                // 处理非激活状态
                break;
            // 编译器确保所有情况都被处理
        }
    }
}
```

## 测试枚举

```java
public class EnumTest {
    @Test
    public void testEnumValues() {
        // 测试枚举值的数量
        assertEquals(3, Status.values().length);
        
        // 测试特定枚举值的存在
        assertTrue(Arrays.asList(Status.values()).contains(Status.ACTIVE));
        
        // 测试枚举的字符串表示
        assertEquals("ACTIVE", Status.ACTIVE.name());
    }
    
    @Test
    public void testEnumMethods() {
        Status status = Status.ACTIVE;
        
        // 测试自定义方法
        assertEquals(1, status.getCode());
        assertEquals("Active", status.getDescription());
        assertTrue(status.isAllowsTransition());
    }
    
    @Test
    public void testEnumComparison() {
        // 测试枚举比较
        assertTrue(Status.ACTIVE == Status.ACTIVE);
        assertFalse(Status.ACTIVE == Status.INACTIVE);
        
        // 测试 equals 方法
        assertTrue(Status.ACTIVE.equals(Status.ACTIVE));
        assertFalse(Status.ACTIVE.equals(Status.INACTIVE));
        
        // 测试 null 安全性
        assertFalse(Status.ACTIVE.equals(null));
    }
    
    @Test
    public void testEnumSerialization() throws Exception {
        Status original = Status.ACTIVE;
        
        // 序列化
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        ObjectOutputStream oos = new ObjectOutputStream(baos);
        oos.writeObject(original);
        oos.close();
        
        // 反序列化
        ByteArrayInputStream bais = new ByteArrayInputStream(baos.toByteArray());
        ObjectInputStream ois = new ObjectInputStream(bais);
        Status deserialized = (Status) ois.readObject();
        ois.close();
        
        // 验证是同一个实例
        assertSame(original, deserialized);
    }
    
    @Test
    public void testEnumSet() {
        Set<Status> activeStatuses = EnumSet.of(Status.ACTIVE, Status.PENDING);
        
        assertTrue(activeStatuses.contains(Status.ACTIVE));
        assertTrue(activeStatuses.contains(Status.PENDING));
        assertFalse(activeStatuses.contains(Status.INACTIVE));
        
        assertEquals(2, activeStatuses.size());
    }
    
    @Test
    public void testEnumMap() {
        Map<Status, String> statusMessages = new EnumMap<>(Status.class);
        statusMessages.put(Status.ACTIVE, "System is running");
        statusMessages.put(Status.INACTIVE, "System is stopped");
        
        assertEquals("System is running", statusMessages.get(Status.ACTIVE));
        assertEquals("System is stopped", statusMessages.get(Status.INACTIVE));
        assertNull(statusMessages.get(Status.PENDING));
    }
}
```

## 总结

### 枚举的核心优势

1. **类型安全**：编译时检查，防止无效值
2. **可读性强**：有意义的名称，清晰的代码
3. **功能丰富**：可以添加字段、方法和构造函数
4. **性能优异**：单例实现，高效比较
5. **线程安全**：天然的线程安全特性
6. **序列化安全**：正确的序列化/反序列化支持

### 最佳实践总结

1. **优先使用枚举**：替代整型常量和字符串常量
2. **避免使用 ordinal()**：使用实例字段存储关联数据
3. **合理使用 switch**：在可控范围内省略 default 分支
4. **选择合适的集合**：使用 EnumSet 和 EnumMap 获得最佳性能
5. **设计不可变枚举**：避免可变字段，确保线程安全
6. **添加有意义的方法**：让枚举承担相关的业务逻辑
7. **考虑扩展性**：通过接口实现可扩展的枚举设计
8. **编写完整测试**：验证枚举的各种行为和边界情况

### 常见错误避免

- 不要依赖 `ordinal()` 方法的返回值
- 不要在枚举中使用可变字段
- 不要忽略 null 值的处理
- 不要在性能敏感的代码中重复调用 `values()`
- 不要将枚举用作位标志（使用 EnumSet 代替）

通过遵循这些原则和最佳实践，可以充分发挥Java枚举的强大功能，编写出更加安全、清晰和高效的代码。

## 扩展阅读

- Effective Java Item 34: Use enums instead of int constants
- Effective Java Item 35: Use instance fields instead of ordinals  
- Effective Java Item 36: Use EnumSet instead of bit fields
- Effective Java Item 37: Use EnumMap instead of ordinal indexing
- Effective Java Item 38: Emulate extensible enums with interfaces
- Java Language Specification: Enum Types
- Oracle Java Documentation: Enum Types Tutorial
