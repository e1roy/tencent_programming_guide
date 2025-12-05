# Stream 流

## tl;dr

- `ParallelStream` 几乎总是不是你想要的。使用 `Stream`。
- `Stream<T>` 是**中间状态**，不应该作为最终产物。所以不要返回 `Stream<T>` 作为函数结果。
- `Stream` 应该遵守函数式编程的契约 -- 无副作用。


## 原则一：避免使用 `parallelStream`

使用普通 `stream`，清晰明了优先关注可读性和调试性

滥用 `parallelStream` 实际带来的收益微乎其微，表现为：
1. 性能陷阱：对于小数据集、本地流等轻量操作场景下，因为多线程的启动、切换同步开销会比普通 stream 性能可能更差。
2. 并发风险：并发操作时在对流进行有副作用的修改外部集合时，可能会引发 `ConcurrentModificationException`，并且问题难以复现和定位。
3. 资源消耗：可能耗尽线程池影响系统稳定性。

并行流在大多数场景下弊大于利，仅在满足以下条件时才考虑使用并行流：
1. 大量 CPU 密集型的纯计算任务场景。
2. 操作无状态且线程安全。
3. 经过严格性能测试证明有效。


### 正例：使用顺序流
```java
List<Integer> results = data.stream()
                            .filter(this::isValid)
                            .map(this::transform)
                            .collect(Collectors.toList());
```

### 反例：不必要地使用并行流
```java
List<Integer> results = data.parallelStream()  // 小数据集反而更慢
                            .filter(this::isValid)
                            .map(this::transform)
                            .collect(Collectors.toList());
```

## 原则二：不要返回` Stream<T>` 作为 API 结果

`Stream` 本质是中间处理状态，而非最终结果。作为 API 返回值存在以下问题：

1. 破坏封装：暴露内部实现细节
2. 资源泄漏风险：未关闭的流可能占用资源
3. 使用不便：调用方需额外处理流操作
4. 序列化困难：`Stream` 不可序列化

### 反例
返回 `Stream` 类型中间处理过程暴露细节，难于使用
```java
public Stream<User> getActiveUsers() {
    return users.stream().filter(User::isActive);
}
```

### 正例：返回集合（如List）作为结果应用，便于用户直接操作
```java
public List<User> getActiveUsers() {
    return users.stream()
         .filter(User::isActive)
         .collect(Collectors.toList());
}
```

## 原则三：Stream 上操作应该遵守函数式编程的契约-无副作用

`Stream` 上的流式操作默认约定是纯计算场景（如 `.map() .filter() .collect()` ），可保证每次运行结果一致，无需担心修改外部数据造成意外行为。`Stream` 操作应该遵循：

1. 不修改外部状态：避免修改流外部的变量或集合
2. 不依赖可变状态：结果只取决于输入，不受外部变化影响
3. 保持幂等性：相同输入始终产生相同输出

### 反例：流操作 `add` 里修改外部状态，产生副作用，破坏函数式契约
```java
List<Order> orders = ...;
List<Order> paidOrders = new ArrayList<>();

orders.stream()
    .filter(Order::isPaid)
    .forEach(paidOrders::add); 
```


### 正例：使用无副作用函数式流操作
```java
List<Order> orders = ...;
double sum = orders.stream()
    .filter(Order::isPaid)
    .mapToDouble(Order::getAmount)
    .sum();

```


## 扩展阅读
- Effective Java Item 45 Use streams judiciously
- Effective Java Item 46 Prefer side-effect-free functions in streams
- Effective Java Item 47 Prefer Collection to Stream as a return type
- Effective Java Item 48 Use caution when making streams parallel
