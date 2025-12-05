# Generics Wildcards 泛型通配符

## tl;dr

- 遵守 PECS 原则：Producer-extends, Consumer-super
- 避免无界通配符滥用（如 `<?>` 应仅在不需要类型操作时使用）

## PECS 原则
简而言之，如果这个泛型具象化的时候会是 `E` 的超类，应该用 `? super E`。而这通常发生在泛型声明对象被**消费**时：

### 正例：遵循 PECS 原则
```java
// 生产者：从 src 读取数据（生产 E）
public void pushAll(ArrayList<? extends E> src) {
    for (E e : src) push(e);
}

// 消费者：向 dst 写入数据（消费 E）
public void popAll(ArrayList<? super E> dst) {
    while (!empty()) dst.add(pop());
}
```

### 反例：违反 PECS 原则
```java
// Bad：尝试向生产者写入
public void addNumbers(ArrayList<? extends Number> list) {
    list.add(Integer.valueOf(1));  // 编译错误
    // <? extends Number> 可能是Double，不能安全添加Integer
}

// Bad：尝试从消费者读取
public void printFirst(ArrayList<? super Number> list) {
    Number num = list.get(0);  // 编译错误
    // <? super Number> 可能是ArrayList<Object>，get()返回Object
}
```

## 详细的 PECS 示例

### Producer Extends 示例

```java
public class NumberProcessor {
    // ✅ 使用 ? extends Number，可以接受任何 Number 的子类集合
    public double sum(List<? extends Number> numbers) {
        double total = 0.0;
        for (Number num : numbers) {
            total += num.doubleValue();  // 只能读取，作为 Number 使用
        }
        return total;
    }
    
    // 使用示例
    public void demonstrateProducerExtends() {
        List<Integer> integers = Arrays.asList(1, 2, 3);
        List<Double> doubles = Arrays.asList(1.1, 2.2, 3.3);
        List<BigDecimal> decimals = Arrays.asList(
            new BigDecimal("1.0"), 
            new BigDecimal("2.0")
        );
        
        // 所有这些都可以传递给 sum 方法
        double intSum = sum(integers);     // ✅ 可以
        double doubleSum = sum(doubles);   // ✅ 可以
        double decimalSum = sum(decimals); // ✅ 可以
    }
}
```

### Consumer Super 示例

```java
public class CollectionUtils {
    // ✅ 使用 ? super Integer，可以接受 Integer 及其父类的集合
    public void addNumbers(List<? super Integer> list) {
        list.add(1);        // ✅ 可以添加 Integer
        list.add(42);       // ✅ 可以添加 Integer
        // list.add(1.5);   // ❌ 编译错误：不能添加 Double
    }
    
    // 使用示例
    public void demonstrateConsumerSuper() {
        List<Integer> integers = new ArrayList<>();
        List<Number> numbers = new ArrayList<>();
        List<Object> objects = new ArrayList<>();
        
        addNumbers(integers);  // ✅ 可以
        addNumbers(numbers);   // ✅ 可以
        addNumbers(objects);   // ✅ 可以
        
        // List<Double> doubles = new ArrayList<>();
        // addNumbers(doubles);  // ❌ 编译错误
    }
}
```

### 复杂的泛型通配符场景

```java
public class AdvancedGenerics {
    // 复制方法：从 src 复制到 dest
    public static <T> void copy(List<? extends T> src, List<? super T> dest) {
        for (T item : src) {
            dest.add(item);
        }
    }
    
    // 使用示例
    public void demonstrateCopy() {
        List<Integer> integers = Arrays.asList(1, 2, 3);
        List<Number> numbers = new ArrayList<>();
        List<Object> objects = new ArrayList<>();
        
        copy(integers, numbers);  // ✅ Integer extends Number
        copy(integers, objects);  // ✅ Integer 是 Object 的子类
        copy(numbers, objects);   // ✅ Number 是 Object 的子类
    }
    
    // 查找最大值
    public static <T extends Comparable<? super T>> T max(List<? extends T> list) {
        if (list.isEmpty()) {
            throw new IllegalArgumentException("Empty list");
        }
        
        T max = list.get(0);
        for (T item : list) {
            if (item.compareTo(max) > 0) {
                max = item;
            }
        }
        return max;
    }
    
    // 使用示例
    public void demonstrateMax() {
        List<Integer> integers = Arrays.asList(1, 5, 3, 2);
        List<String> strings = Arrays.asList("apple", "banana", "cherry");
        
        Integer maxInt = max(integers);     // 返回 5
        String maxString = max(strings);    // 返回 "cherry"
    }
}
```

### 实际应用场景

```java
public class EventProcessor<T> {
    private final List<EventHandler<? super T>> handlers = new ArrayList<>();
    
    // 添加处理器：可以处理 T 或 T 的父类的处理器
    public void addHandler(EventHandler<? super T> handler) {
        handlers.add(handler);
    }
    
    // 处理事件
    public void process(T event) {
        for (EventHandler<? super T> handler : handlers) {
            handler.handle(event);
        }
    }
    
    // 批量处理：接受 T 或 T 的子类的事件列表
    public void processAll(List<? extends T> events) {
        for (T event : events) {
            process(event);
        }
    }
}

interface EventHandler<T> {
    void handle(T event);
}

// 使用示例
class UserEvent {
    private final String username;
    
    public UserEvent(String username) {
        this.username = username;
    }
    
    public String getUsername() {
        return username;
    }
}

class LoginEvent extends UserEvent {
    public LoginEvent(String username) {
        super(username);
    }
}

public class EventProcessorDemo {
    public void demonstrate() {
        EventProcessor<UserEvent> processor = new EventProcessor<>();
        
        // 添加可以处理 UserEvent 或其父类的处理器
        processor.addHandler((UserEvent event) -> 
            System.out.println("User event: " + event.getUsername()));
        
        processor.addHandler((Object event) -> 
            System.out.println("Generic event: " + event));
        
        // 处理 UserEvent 及其子类的事件
        List<LoginEvent> loginEvents = Arrays.asList(
            new LoginEvent("alice"),
            new LoginEvent("bob")
        );
        
        processor.processAll(loginEvents);  // ✅ LoginEvent extends UserEvent
    }
}
```

### 常见错误和解决方案

```java
public class CommonMistakes {
    // ❌ 错误：不必要的通配符
    public void badExample1(List<?> list) {
        // 无法对 list 进行任何有意义的操作
        // Object item = list.get(0);  // 只能作为 Object 使用
    }
    
    // ✅ 正确：使用具体类型或有界通配符
    public void goodExample1(List<String> list) {
        String item = list.get(0);  // 可以作为 String 使用
    }
    
    // ❌ 错误：混淆 extends 和 super
    public void badExample2(List<? extends Number> numbers) {
        // numbers.add(42);  // 编译错误！不能添加元素
    }
    
    // ✅ 正确：使用 super 进行添加操作
    public void goodExample2(List<? super Integer> numbers) {
        numbers.add(42);  // ✅ 可以添加 Integer
    }
    
    // ❌ 错误：过度使用通配符
    public List<?> badExample3(List<?> input) {
        List<?> result = new ArrayList<>();
        // 无法进行有意义的操作
        return result;
    }
    
    // ✅ 正确：使用泛型方法
    public <T> List<T> goodExample3(List<T> input) {
        List<T> result = new ArrayList<>();
        result.addAll(input);
        return result;
    }
}
```

## 通配符使用指南

1. **PECS 原则**：Producer-extends, Consumer-super
2. **只读操作**：使用 `? extends T`
3. **只写操作**：使用 `? super T`
4. **读写操作**：使用具体类型 `T`
5. **无界通配符 `?`**：当不关心类型参数时使用

## 记忆技巧

- **GET** 和 **PUT** 原则：
  - **GET**：从集合中获取元素时使用 `extends`
  - **PUT**：向集合中放入元素时使用 `super`

## 扩展阅读

- Effective Java Item 31: Use bounded wildcards to increase API flexibility
- [Java 泛型教程](https://docs.oracle.com/javase/tutorial/java/generics/)
