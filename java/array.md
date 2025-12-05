# Array 数组

## tl;dr

- 尽量避免使用 Array（基础类型除外），使用 `List<T>`。如果希望 `List` 是不可变的，使用 `ImmutableList`。

## 数组与 List 的不同

除了数组长度不可变，List 通常长度可变之外，它们的一个重要区别在于对参数多态的处理：

- 数组是**协变(covariant)** 的。List 是**不变(invariant)** 的。
  换言之，假设 `SubType` 是 `BaseType` 的子类，那么：
  - `SubType[]` 是 `BaseType[]` 的子类
  - `List<SubType>` 不是 `List<BaseType>` 的子类
- 数组是**实化(reified)** 的。List 是通过泛型的**类型擦除(type erasuer)** 的。

相对而言，数组无法做到**编译时检查**，更多地依赖**运行时检查**。而尽可能地在编译期发现错误，能够降低测试的成本和上线的风险。

关于“编译时检查”和“运行时检查”，参考下面的例子：

```java
Object[] objectArray = new Long[1];     // 正例。因为 Object[] 是 Long[] 的超类。
objectArray[0] = "I don't fit in";      // 反例。错误！只有运行时才能发现；因为 objectArray 的实例其实是 Long数组，存入 String 会导致非法

List<Object> objectList = new ArrayList<Long>(); // 编译时就会报错！
objectList.add("I don't fit in");       // 自然这个错误就可以避免了。
```

另外，List 的泛型保护的是 List 对象本身，从编译的角度防止篡改 List 的泛型类型；

如果上述 case，想向 List<Object> 添加 Long 类型的对象，是合法的：

```java
List<Object> objectList = new ArrayList<>();
List<Long> longList = new ArrayList<>();
objectList.addAll(longList);            // 可以添加
```

## 数组是可变的

数组是可变的是指，永远可以为数组中的某一个元素重新赋值。甚至并没有显式禁止数组可变的方法。即：

```java
String[] names = new String[]{"1", "2", "3"};

names[1] = "Haruhi Suzumiya";           // 可以修改
```

这通常是一个劣势。但是，这可以作为一个在回调间传递值的 Hack，即回调中所有的引用需要是 `final` 对象，因为我们无法传入一个 `final` 对象并完成赋值：
## 反例
```java
// Bad -- Won't compile！
Event event;
var.onClick(e -> event = e);
```

这时，可以将需要传递的值包在一个数组内，利用数组的可变性完成值的传递：

```java
// OK -- but a hack:
Event[] event = new Event[1];
var.onClick(e -> event[0] = e);
```

当然，上述做法是一种比较取巧的方式，它的可读性并不好，建议仅作为了解即可；

实践中，一个更好的做法还是自己包装一个 class 对象，在方法回调中传值：

```java
class ValueHolder<T> {
  T value;
}

ValueHolder<Event> eventHolder = new ValueHolder<>();
onClick(e -> eventHolder.value = e);
```

如果觉得自行封装比较麻烦，java 官方的 concurrent 工具库，也提供了类似机制的 class 可以借用：

```java
AtomicReference<Event> event = new AtomicReference<>(null);
onClick(e -> event.set(e));
```

## 何时使用数组

虽然一般情况下推荐使用 List，但在以下特定场景中，数组仍然是更好的选择：

### 与遗留代码或第三方库交互

当需要与只接受数组参数的 API 交互时：

### 反例

```java
// 反例：强制转换可能导致类型安全问题
List<String> list = Arrays.asList("a", "b", "c");
String[] array = (String[]) list.toArray(); // 会抛出 ClassCastException
```

### 正例

```java
// 正例：使用类型安全的转换方法
List<String> list = Arrays.asList("a", "b", "c");
String[] array = list.toArray(new String[0]); // 类型安全，推荐写法
```

### 数学计算和科学计算

在需要进行大量数值计算的场景中，数组通常有更好的性能：

```java
// 正例：矩阵运算等数学计算场景
public class MatrixOperations {
    public static double[][] multiply(double[][] a, double[][] b) {
        int rows = a.length;
        int cols = b[0].length;
        double[][] result = new double[rows][cols];

        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                for (int k = 0; k < a[0].length; k++) {
                    result[i][j] += a[i][k] * b[k][j];
                }
            }
        }
        return result;
    }
}
```

### 固定大小的数据结构

当数据结构大小在创建时就确定且不会改变时：

```java
// 正例：表示坐标点、颜色等固定大小的数据
public class Point3D {
    private final double[] coordinates = new double[3]; // 固定3个坐标

    public Point3D(double x, double y, double z) {
        coordinates[0] = x;
        coordinates[1] = y;
        coordinates[2] = z;
    }

    public double[] getCoordinates() {
        return coordinates.clone(); // 返回副本避免外部修改
    }
}
```

### 内存敏感的应用

在内存使用极其受限的环境中：

```java
// 正例：游戏开发中的性能关键代码
public class ParticleSystem {
    private final float[] positions;    // 使用数组减少对象开销
    private final float[] velocities;
    private final int[] colors;

    public ParticleSystem(int particleCount) {
        positions = new float[particleCount * 3];  // x, y, z
        velocities = new float[particleCount * 3];
        colors = new int[particleCount];           // RGBA packed as int
    }
}
```

## 性能考虑

- 对性能极其敏感的代码才考虑使用数组
- 大多数情况下 List 的性能差异可以忽略不计

## API 设计建议

- 公共 API 应尽量使用 List 接口，而非数组或某种 List 的实现类
- 内部实现可根据需要选择
   > Effective Java 中的建议："当你遇到数组和泛型不能很好地混合使用时，你的第一反应应该是用列表代替数组"

### 反例

```java
String[] objectArray = new String[]{"1"};   // 声明为数组类型，不易扩展

ArrayList<String> data = new ArrayList<>(); // 变量声明为具体实现类型 ArrayList，不推荐
```

### 正例

```java
// 声明为抽象 List 接口后，可以根据需求替换对应的实现类，而不影响已有代码的编译，例如：

List<String> data = new ArrayList<>();      // 变量声明为抽象接口类型，便于后续修改实现

List<String> data = new LinkedList<>();     // 根据不同需求，例如频繁增删的场景，可以替换为链表

List<String> data = new CustomList<>();     // 可以替换为自定义实现，用于拦截List操作，或数据加工 等特殊逻辑

String value = data.get(0);                 // 以上3种List的实现，都不影响这行代码的编译
```

## 扩展阅读

- Effective Java Item 28：Prefer lists to arrays
