# Performance 性能

## tl;dr

- **不要过早优化**。正确性优先，其次是可读性，最后才是性能。
- **避免常见的性能陷阱**。了解并避免常见的资源浪费和性能问题。
- **合理使用缓存和对象池**。在适当的场景下使用缓存和对象池来提升性能。

## 不要过早优化

高德纳（Donald Knuth）的名言："过早优化是万恶之源"。在编程过程中，应该遵循以下优先级：

1. **正确性**：代码必须首先是正确的，能够满足功能需求
2. **可读性**：代码应该易于理解和维护
3. **性能**：在保证正确性和可读性的前提下，再考虑性能优化

### 何时考虑性能优化

- 通过性能测试发现了实际的性能瓶颈
- 系统无法满足预期的性能指标
- 用户体验受到明显影响

### 性能优化的原则

- 先测量，后优化
- 优化最关键的路径（80/20原则）
- 保持代码的可读性和可维护性

## 常见的性能陷阱

### 无谓的对象创建

字符串拼接

```java
// 错误：在循环中使用字符串拼接
String result = "";
for (int i = 0; i < 1000; i++) {
    result += "item" + i;  // 每次都创建新的String对象
}

// 正确：使用StringBuilder
StringBuilder sb = new StringBuilder();
for (int i = 0; i < 1000; i++) {
    sb.append("item").append(i);
}
String result = sb.toString();
```

正则表达式编译

```java
// 错误：每次都编译正则表达式
public boolean isValidEmail(String email) {
    return email.matches("^[A-Za-z0-9+_.-]+@(.+)$");
}

// 正确：预编译正则表达式
private static final Pattern EMAIL_PATTERN = 
    Pattern.compile("^[A-Za-z0-9+_.-]+@(.+)$");

public boolean isValidEmail(String email) {
    return EMAIL_PATTERN.matcher(email).matches();
}
```

装箱和拆箱

```java
// 错误：不必要的装箱
List<Integer> numbers = new ArrayList<>();
for (int i = 0; i < 1000; i++) {
    numbers.add(Integer.valueOf(i));  // 装箱操作
}

// 正确：使用基本类型数组或专门的集合
int[] numbers = new int[1000];
for (int i = 0; i < 1000; i++) {
    numbers[i] = i;
}
```

### 集合使用不当

选择合适的集合类型

```java
// 如果需要频繁随机访问，使用ArrayList而不是LinkedList
List<String> list = new ArrayList<>();  // O(1)随机访问

// 如果需要频繁插入删除，使用LinkedList
List<String> list = new LinkedList<>();  // O(1)插入删除

// 如果需要去重，使用Set
Set<String> uniqueItems = new HashSet<>();

// 如果需要排序，使用TreeSet或排序后的List
Set<String> sortedItems = new TreeSet<>();
```

合理设置初始容量

```java
// 错误：使用默认容量，可能导致多次扩容
List<String> list = new ArrayList<>();  // 默认容量10

// 正确：根据预期大小设置初始容量
List<String> list = new ArrayList<>(1000);  // 避免扩容开销
```

### 异常处理的性能影响

```java
// 错误：使用异常控制正常流程
public int parseInt(String str) {
    try {
        return Integer.parseInt(str);
    } catch (NumberFormatException e) {
        return -1;  // 异常处理开销很大
    }
}

// 正确：先验证再处理
public int parseInt(String str) {
    if (str == null || str.isEmpty()) {
        return -1;
    }
    // 可以添加更多验证逻辑
    try {
        return Integer.parseInt(str);
    } catch (NumberFormatException e) {
        return -1;
    }
}
```

## 性能优化技巧

### 缓存策略

计算结果缓存

```java
public class ExpensiveCalculator {
    private final Map<String, Integer> cache = new ConcurrentHashMap<>();
    
    public int calculate(String input) {
        return cache.computeIfAbsent(input, this::doExpensiveCalculation);
    }
    
    private int doExpensiveCalculation(String input) {
        // 复杂的计算逻辑
        return input.hashCode() * 42;
    }
}
```

懒加载

```java
public class ResourceManager {
    private volatile ExpensiveResource resource;
    
    public ExpensiveResource getResource() {
        if (resource == null) {
            synchronized (this) {
                if (resource == null) {
                    resource = new ExpensiveResource();
                }
            }
        }
        return resource;
    }
}
```

### 对象池

对于创建成本高的对象，可以考虑使用对象池：

```java
public class DatabaseConnectionPool {
    private final BlockingQueue<Connection> pool;
    private final int maxSize;
    
    public DatabaseConnectionPool(int maxSize) {
        this.maxSize = maxSize;
        this.pool = new ArrayBlockingQueue<>(maxSize);
        // 初始化连接池
        for (int i = 0; i < maxSize; i++) {
            pool.offer(createConnection());
        }
    }
    
    public Connection borrowConnection() throws InterruptedException {
        return pool.take();
    }
    
    public void returnConnection(Connection connection) {
        if (connection != null) {
            pool.offer(connection);
        }
    }
    
    private Connection createConnection() {
        // 创建数据库连接的逻辑
        return null;
    }
}
```

### 并发优化

使用并发集合

```java
// 错误：使用同步包装器
Map<String, String> map = Collections.synchronizedMap(new HashMap<>());

// 正确：使用专门的并发集合
Map<String, String> map = new ConcurrentHashMap<>();
```

减少锁的粒度

```java
public class OptimizedCounter {
    private final AtomicLong counter = new AtomicLong(0);
    
    public long increment() {
        return counter.incrementAndGet();  // 无锁操作
    }
    
    public long get() {
        return counter.get();
    }
}
```

## JVM 性能调优

### 垃圾回收优化

```bash
使用G1垃圾回收器
-XX:+UseG1GC

设置堆内存大小 根据实际情况设置
-Xms2g -Xmx4g

设置新生代比例
-XX:NewRatio=2

启用GC日志
-XX:+PrintGC -XX:+PrintGCDetails
```

### JIT编译优化

```bash
降低JIT编译阈值，加快热点代码编译
-XX:CompileThreshold=1000

启用分层编译
-XX:+TieredCompilation
```

### 服务启动优化

JIT启动、模块加载等情况都可能导致性能毛刺，属于正常现象。如果要求启动时延迟快速达标，应该考虑：

```java
public class WarmupService {
    @PostConstruct
    public void warmup() {
        // 发起一些预热请求
        for (int i = 0; i < 100; i++) {
            performTypicalOperation();
        }
    }
    
    private void performTypicalOperation() {
        // 模拟典型的业务操作
    }
}
```

## 性能监控和分析

### 性能指标监控

- **响应时间**：请求处理的时间
- **吞吐量**：单位时间内处理的请求数
- **CPU使用率**：处理器的使用情况
- **内存使用率**：堆内存和非堆内存的使用情况
- **GC频率和时间**：垃圾回收的频率和耗时

### 性能分析工具

- **JProfiler**：商业性能分析工具
- **VisualVM**：免费的性能分析工具
- **JConsole**：JDK自带的监控工具

### Benchmark基准测试

```java
@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.NANOSECONDS)
@State(Scope.Benchmark)
public class StringConcatenationBenchmark {
    
    @Benchmark
    public String stringConcatenation() {
        String result = "";
        for (int i = 0; i < 100; i++) {
            result += "item" + i;
        }
        return result;
    }
    
    @Benchmark
    public String stringBuilderConcatenation() {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < 100; i++) {
            sb.append("item").append(i);
        }
        return sb.toString();
    }
}
```

## 最佳实践

1. **编写性能测试**：为关键路径编写性能测试，建立性能基线
2. **持续监控**：在生产环境中持续监控性能指标
3. **渐进式优化**：一次优化一个问题，验证效果后再进行下一步
4. **文档记录**：记录性能优化的过程和结果，便于后续维护
5. **团队分享**：将性能优化的经验分享给团队成员

## 扩展阅读

- Effective Java Item 67: Optimize judiciously
- Java Performance: The Definitive Guide
- [Java Performance](https://github.com/gdouzwt/java-performance)
- [JVM Performance Optimization](https://docs.oracle.com/javase/8/docs/technotes/guides/vm/performance-enhancements-7.html)
