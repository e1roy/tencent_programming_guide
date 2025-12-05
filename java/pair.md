# Pair “对”结构

## tl;dr

- **Java 标准库有意不提供 `Pair`**：避免语义模糊和误用，鼓励使用有明确语义的专用类
- **根据实际语义选择实现**：坐标点用 Record、键值对用 Map.Entry、业务数据用专用类
- **避免通用 Pair 类**：语义不明确，无法添加业务方法，降低代码可读性
- **优先使用 Record（JDK14+）**：简洁、不可变、支持验证，替代传统 data class

## 为什么 Java 不提供 Pair

Java 标准库有意不提供通用的 `Pair` 数据结构，主要原因包括：

### 语义模糊性

- **通用 Pair 缺乏语义**：`Pair<String, Integer>` 无法表达具体含义（是坐标？是键值对？是姓名年龄？）
- **字段命名问题**：`first/second` 或 `left/right` 无法准确描述数据含义
- **维护困难**：时间久了，开发者难以理解当初的设计意图

### 类型安全性问题

- **无法添加约束**：通用 Pair 无法对字段进行业务相关的验证
- **扩展性差**：无法添加业务方法，如 `distanceTo()`、`isAdult()` 等
- **IDE 支持有限**：自动补全和重构工具无法提供有意义的提示

### 设计哲学

- **鼓励明确语义**：Java 鼓励开发者创建有明确语义的专用类
- **提高代码质量**：专用类能更好地表达业务逻辑和领域概念

## 正确的替代方案

根据具体需求选择合适的数据结构：

- **二元 tuple**：使用二元的 data class，JDK 14+ 优先使用 `Record`
- **键值对结构**：使用 `Map.Entry` 或自定义 data class
- **同类物品对**：如坐标 `(x, y)`，使用自定义 `Pair<T>` 或 data class
- **项目公共库**：自定义 `Pair<T>` 应作为项目公共库，避免重复实现

## Record vs 传统 Data Class 对比

### Record 的优势（JDK 14+）

```java
// 传统 data class - 需要大量样板代码
@AutoValue
public abstract class LabelAndLocation {
    public static LabelAndLocation of(Target target) {
        return new AutoValue_LabelAndLocation(target.getLabel(), target.getLocation());
    }

    public abstract Label getLabel();
    public abstract Location getLocation();

    // 需要手动实现 equals, hashCode, toString
    // AutoValue 会自动生成，但仍需要注解处理
}
```

### Record 的简洁性

```java
// Record - 简洁且功能完整
public record LabelAndLocation(Label label, Location location) {
    public static LabelAndLocation of(Target target) {
        return new LabelAndLocation(target.getLabel(), target.getLocation());
    }

    // equals, hashCode, toString 自动生成
    // 构造函数、getter 方法自动生成
    // 支持紧凑构造函数进行验证
}
```

### Record 的优势对比

| 特性                | 传统 Data Class        | Record       |
| ------------------- | ---------------------- | ------------ |
| **代码量**          | 大量样板代码           | 极简声明     |
| **不可变性**        | 需要手动实现           | 天然不可变   |
| **equals/hashCode** | 需要手动实现或工具生成 | 自动生成     |
| **验证逻辑**        | 需要在构造函数中实现   | 紧凑构造函数 |
| **序列化**          | 需要额外配置           | 天然支持     |
| **性能**            | 依赖工具生成           | 编译器优化   |

## 不要混用二元结构的类

### 语义混淆问题

```java
class OuterClass {
    static class Point<T> {
        T x;  // 表示坐标的 x 轴
        T y;  // 表示坐标的 y 轴
    }
}
```

**问题**：`Point` 类设计用于表示坐标点，具有明确的几何语义。如果用它来表示键值对，会导致：

- **语义混乱**：`x` 和 `y` 本应表示坐标，却被用作键值
- **代码可读性差**：其他开发者难以理解 `point.x` 实际是 key 还是 value
- **维护困难**：后续修改时容易产生误解

### 正确的做法

```java
// 坐标点：使用专门的 Point 类
Point<Double> coordinate = new Point<>(1.0, 2.0);

// 键值对：使用 Map.Entry
Map.Entry<String, Integer> keyValue = Map.entry("username", 12345);

// 即使两者结构相同，语义完全不同，不应混用
```

## 不要使用 `javafx.util.Pair`

### 为什么不应该使用

1. **已被移除**：`javafx` 模块在 JDK 11+ 中已从 JRE 移除，依赖可能不存在
2. **设计局限性**：虽然名为 `Pair`，但实际设计更接近 `Map.Entry`，主要用于键值对场景
3. **功能受限**：无法添加业务方法，缺乏验证逻辑，扩展性差
4. **语义不明确**：`getKey()` 和 `getValue()` 方法暗示键值关系，不适合表示坐标等概念

### 正确的替代方案

### 反例

```java
// 反例：使用 javafx.util.Pair
javafx.util.Pair<String, Integer> pair = new javafx.util.Pair<>("name", 25);
```

### 正例

```java
// 正例：根据实际语义选择合适的数据结构
// 如果是键值对
Map.Entry<String, Integer> entry = Map.entry("name", 25);

// 如果是姓名年龄
public record Person(String name, int age) {}

// 如果是坐标
public record Point(double x, double y) {}
```

## 实际应用示例

### 正例：使用 Record 表示坐标点（JDK14+）

```java
// 正例：使用Record明确表示坐标点，有清晰的语义和不可变性
public record Point(double x, double y) {
    // 紧凑构造函数：可以添加校验逻辑
    public Point {
        if (Double.isInfinite(x) || Double.isInfinite(y)) {
            throw new IllegalArgumentException("坐标值不能为无限大");
        }
    }

    // 可以添加业务方法
    public double distanceTo(Point other) {
        return Math.hypot(x - other.x, y - other.y);
    }

    // 可以添加静态工厂方法
    public static Point origin() {
        return new Point(0.0, 0.0);
    }
}

// 使用示例
Point p = new Point(1.0, 2.0);
double dist = p.distanceTo(new Point(4.0, 6.0));
System.out.println("距离：" + dist);  // 输出：距离：5.0
```

### 正例：使用 Map.Entry 表示键值对

```java
// 正例：使用Map.Entry明确表示键值关系，语义清晰
Map.Entry<String, Integer> ageEntry = Map.entry("张三", 25);
Map.Entry<String, Double> priceEntry = Map.entry("苹果", 5.99);

// 可以用于构建 Map
Map<String, Integer> ages = Map.ofEntries(
    Map.entry("张三", 25),
    Map.entry("李四", 30)
);

// 优势：明确表达了键值关系，可以使用 Map 的工具方法
ages.entrySet().stream()
    .sorted(Map.Entry.comparingByValue())
    .forEach(entry -> System.out.println(entry.getKey() + ": " + entry.getValue()));
```

### 正例：使用专用类表示业务数据

```java
// 正例：专用类可以包含业务逻辑和验证，语义明确
public record Person(String name, int age) {
    // 紧凑构造函数：添加数据验证
    public Person {
        if (age < 0 || age > 150) {
            throw new IllegalArgumentException("无效年龄：" + age);
        }
        if (name == null || name.trim().isEmpty()) {
            throw new IllegalArgumentException("姓名不能为空");
        }
        name = name.trim();  // 自动去除前后空格
    }

    // 业务方法：提供领域逻辑
    public boolean isAdult() {
        return age >= 18;
    }

    public String getAgeGroup() {
        if (age < 13) return "儿童";
        if (age < 20) return "青少年";
        if (age < 65) return "成年人";
        return "老年人";
    }
}

// 使用示例
Person person = new Person("张三", 25);
if (person.isAdult()) {
    System.out.println(person.name() + "是" + person.getAgeGroup());
}
```

### 反例：滥用通用 Pair 类

```java
// 反例：使用同一个Pair类表示不同语义的数据，导致语义混乱
// 注意：这里假设存在一个通用的Pair类（实际Java标准库不提供）
Pair<Double, Double> coordinate = new Pair<>(1.0, 2.0);  // 坐标点
Pair<String, Integer> personInfo = new Pair<>("张三", 25); // 个人信息
Pair<String, Double> productInfo = new Pair<>("苹果", 5.99); // 商品信息

// 问题1：无法添加业务方法，如distanceTo()、isAdult()等
// 问题2：字段名只能是first/second，没有语义，可读性差
// 问题3：无法添加数据校验，如坐标范围检查、年龄合理性检查
// 问题4：IDE无法提供有意义的自动补全提示
```

### 反例：混用不同语义的数据结构

```java
// 反例1：用Point类表示键值对，语义混乱
class Point<T> {
    T x;  // 本应表示坐标x轴
    T y;  // 本应表示坐标y轴
}

// 错误用法：用坐标类表示键值对
Point<String> kvPair = new Point<>();
kvPair.x = "username";  // 本应是key，但用x表示很别扭
kvPair.y = "password";  // 本应是value，但用y表示很别扭
// 问题：语义混乱，x/y本应表示坐标，这里却用作键值，容易误解
```

### 反例：用通用 Pair 代替 Map.Entry

```java
// 反例：用通用Pair代替Map.Entry，失去键值概念
// 假设的通用Pair类
Pair<String, Integer> populationPair = new Pair<>("Beijing", 21_540_000);

// 问题1：无法明确区分key和value的语义
// 问题2：其他开发者可能误用first/second，不知道哪个是key
// 问题3：无法使用Map生态的工具方法

// 对比：使用Map.Entry的清晰性
Map.Entry<String, Integer> populationEntry = Map.entry("Beijing", 21_540_000);
// 优势：getKey()和getValue()语义明确，可以使用Map.Entry.comparingByKey()等工具方法
```

### 反例：代码格式问题

```java
// 反例：代码格式不规范，缺少换行和注释
List<Pair<String, Integer>> pairs = Arrays.asList(
    new Pair<>("Beijing", 21_540_000),
    new Pair<>("Shanghai", 24_280_000)
);
pairs.sort(Comparator.comparing(Pair::getFirst)); // 问题：Pair::getFirst语义模糊

// 问题1：无法明确表达是按Key排序，可读性差
// 问题2：无法直接使用Map.Entry的工具方法（如Entry.comparingByKey()）
// 问题3：代码格式不规范，缺少必要的换行和注释
```

### 反例：使用已废弃的 javafx.util.Pair

```java
// 反例：使用已从JDK移除的javafx.util.Pair
javafx.util.Pair<String, String> credentials =
    new javafx.util.Pair<>("admin", "123456");

// 问题1：javafx模块在JDK 11+中已移除，依赖可能不存在
// 问题2：设计上更适合表示Map.Entry，不适合通用场景
// 问题3：无法扩展功能，缺乏验证逻辑
// 问题4：getKey()和getValue()方法暗示键值关系，不适合表示坐标等概念
```

## 扩展阅读

- [Java Records - JEP 395](https://openjdk.java.net/jeps/395)
- [Effective Java - Item 14: Consider implementing Comparable](https://docs.oracle.com/javase/tutorial/java/generics/index.html)
- [Map.Entry Documentation](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/util/Map.Entry.html)
