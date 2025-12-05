# Final 关键字

## tl;dr

- 所有的类成员： 优先使用 final。
- 所有的入参和本地变量：不需要标明 final，除非有必要，例如当会被闭包捕获时。

## final 类

`final` 关键字可以修饰类，使得此类无法被**继承**。由于不鼓励使用继承，而应该优先于使用组合，因此，默认情况下，所有的类应该是 `final` 的。

由于 `final` 类无法被 Mock，而 Mock 在 Java 单元测试中被大量使用，因此，在这种情况下，我们通常不使用 `final` 关键字强制不可继承，而是约定类实质上不可继承。换言之，我们通常约定**所有的非抽象类(non-`abstract`)都是不可继承的**。如需继承，应该认真审查继承类的设计，并再次确定类的继承是有必要的。

任何情况下都不应该被 Mock 的类应该显式地被标记为 `final`，例如：

- 不可变类，尤其是数据类。
- 辅助类，如 `Strings`，或是仅包含常量的类。

## final 类成员

为了最小化可变性，所有的类成员默认应该是 final 的，除非他们的引用必须是可变的。

通常，IDE 会对此进行静态分析并作出提示。

## final 入参和本地变量

通常情况下，即使入参和本地变量的引用实质是不可变的，即可以添加 `final` 关键字，也不需要添加 final 修饰符。

这是因此，入参的 `final` 关键字通常并没有实质的意义：它声明入参的引用在子例程中是不可变的，但入参本身就**复制**了原引用，所以对入参这个引用所做的任何修改不会影响原引用。例如：

```java
void modify(String str) {
  str = "Das";
}

public static void main() {
  String s = "Hello";
  modify(s);
  System.out.println(s); // "Hello".
}
```

因此，强制入参引用不可变意义不大。

类似的，所有的本地变量的作用域不会逃域出子例程，因此，为每个本地变量声明 `final` 的作用也不大。

特例在 JDK 8 之前，本地**引用**会被某个回调捕获时，必须是 `final` 的。在 JDK 8 及以后，只要是实质 `final` 即可。

## 注意事项


static final 不总是常量，参考 [Constants 常量](constants.md)

简言之，不可变的才是常量，但 `static final` 的成员未必不可变。

## Final 关键字的实际应用

### Final 类的设计

```java
// ✅ 不可变数据类应该是 final 的
public final class Money {
    private final BigDecimal amount;
    private final Currency currency;
    
    public Money(BigDecimal amount, Currency currency) {
        this.amount = Objects.requireNonNull(amount);
        this.currency = Objects.requireNonNull(currency);
    }
    
    public BigDecimal getAmount() {
        return amount;
    }
    
    public Currency getCurrency() {
        return currency;
    }
    
    // 不可变类的操作返回新实例
    public Money add(Money other) {
        if (!this.currency.equals(other.currency)) {
            throw new IllegalArgumentException("Currency mismatch");
        }
        return new Money(this.amount.add(other.amount), this.currency);
    }
}

// ✅ 工具类应该是 final 的
public final class StringUtils {
    private StringUtils() {
        throw new AssertionError("Utility class should not be instantiated");
    }
    
    public static boolean isEmpty(String str) {
        return str == null || str.isEmpty();
    }
    
    public static String capitalize(String str) {
        if (isEmpty(str)) {
            return str;
        }
        return str.substring(0, 1).toUpperCase() + str.substring(1).toLowerCase();
    }
}
```

### Final 成员变量的最佳实践

```java
public class OrderService {
    // ✅ 配置常量应该是 final 的
    private static final int MAX_RETRY_ATTEMPTS = 3;
    private static final Duration TIMEOUT = Duration.ofSeconds(30);

    // ✅ 不可变集合应该是 final 的
    private static final Set<OrderStatus> VALID_STATUSES = Set.of(
            OrderStatus.PENDING,
            OrderStatus.CONFIRMED,
            OrderStatus.SHIPPED
    );
    
    // ✅ 依赖注入的字段应该是 final 的
    private final OrderRepository orderRepository;
    private final PaymentService paymentService;
    private final EmailService emailService;
    
    public OrderService(OrderRepository orderRepository,
                       PaymentService paymentService,
                       EmailService emailService) {
        this.orderRepository = Objects.requireNonNull(orderRepository);
        this.paymentService = Objects.requireNonNull(paymentService);
        this.emailService = Objects.requireNonNull(emailService);
    }
    
    // ✅ 可变状态不应该是 final 的
    private int processedOrderCount = 0;  // 这个值会改变
    
    public void processOrder(Order order) {
        // 处理逻辑
        processedOrderCount++;
    }
}
```

### Final 参数和局部变量的使用场景

```java
public class FileProcessor {
    // ✅ Lambda 中使用的变量必须是 effectively final
    public void processFiles(List<String> filenames) {
        final String logPrefix = "Processing: ";  // 被 lambda 捕获，必须是 final
        
        filenames.stream()
                .map(filename -> logPrefix + filename)  // 使用 final 变量
                .forEach(System.out::println);
    }
    
    // ✅ 在复杂方法中，final 参数可以防止意外修改
    public Result processComplexData(final List<Data> inputData) {
        // inputData = new ArrayList<>();  // 编译错误，防止意外重新赋值
        
        // 长的处理逻辑...
        for (int i = 0; i < 100; i++) {
            // 复杂的处理逻辑
            // final 确保 inputData 引用不会被意外修改
        }
        
        return new Result(inputData);
    }
    
    // ✅ 资源管理中的 final 变量
    public String readFileContent(String filename) throws IOException {
        final StringBuilder content = new StringBuilder();
        
        // 表明reader是只读资源变量，不应在操作中被替换，减少错误（如误关闭错误的资源）
        // 资源变量默认被隐式视为final，但显式声明是防御性编程的体现
        try (final BufferedReader reader = Files.newBufferedReader(Paths.get(filename))) {
            String line;
            while ((line = reader.readLine()) != null) {
                content.append(line).append('\n');
            }
        }
        
        return content.toString();
    }
}
```

### Final 与继承设计

```java
// ✅ 模板方法模式：部分方法是 final 的
public abstract class AbstractProcessor {
    // final 方法定义了不可变的算法骨架
    public final void process() {
        initialize();
        doProcess();
        cleanup();
    }
    
    // 子类可以重写的方法
    protected abstract void initialize();
    protected abstract void doProcess();
    
    // 默认实现，子类可以重写
    protected void cleanup() {
        // 默认清理逻辑
    }
}

// ✅ 策略模式：接口实现通常是 final 类
public final class QuickSortStrategy implements SortStrategy {
    @Override
    public void sort(int[] array) {
        quickSort(array, 0, array.length - 1);
    }
    
    private void quickSort(int[] array, int low, int high) {
        // 快速排序实现
    }
}
```

### Final 与性能优化

```java
public class PerformanceExample {
    // ✅ final 字段可能有性能优势
    private final String constantValue = "CONSTANT";
    private final Map<String, String> cache = new ConcurrentHashMap<>();
    
    // ✅ final 方法可以被内联优化
    public final int calculateHash(String input) {
        return input.hashCode() * 31;
    }
    
    // ✅ final 局部变量在某些情况下性能更好
    public void processLargeDataset(List<String> data) {
        final int size = data.size();  // 避免重复调用 size()
        final String prefix = getPrefix();  // 避免重复调用方法
        
        for (int i = 0; i < size; i++) {
            String processed = prefix + data.get(i);
            // 处理逻辑
        }
    }
    
    private String getPrefix() {
        return "PREFIX_";
    }
}
```

### Final 的常见误区

```java
public class FinalMisconceptions {
    // ❌ 误区：认为 final 集合是不可变的
    private final List<String> items = new ArrayList<>();
    
    public void addItem(String item) {
        items.add(item);  // ✅ 这是允许的！final 只是引用不可变
    }
    
    // ✅ 正确：真正的不可变集合
    private final List<String> immutableItems = List.of("item1", "item2");
    
    // ❌ 误区：所有参数都加 final
    public void unnecessaryFinal(final int a, final String b, final List<String> c) {
        // 对于简单方法，这样做没有必要，反而增加了代码噪音
        System.out.println(a + b + c.size());
    }
    
    // ✅ 正确：只在必要时使用 final 参数
    public void appropriateFinal(List<String> items) {
        final String prefix = "Item: ";  // 被 lambda 使用，需要 final
        
        items.stream()
             .map(item -> prefix + item)
             .forEach(System.out::println);
    }
}
```

## Final 使用指南

1. **类设计**：默认使用 final，除非明确需要继承
2. **成员变量**：依赖注入和不可变字段使用 final
3. **方法参数**：通常不需要 final，除非被闭包捕获
4. **局部变量**：被 lambda 使用时必须是 effectively final
5. **性能考虑**：final 可能带来微小的性能提升

## 扩展阅读

- https://en.wikipedia.org/wiki/Final_(Java)
- [Effective Java Item 17: Minimize mutability](https://www.oreilly.com/library/view/effective-java-3rd/9780134686097/)
