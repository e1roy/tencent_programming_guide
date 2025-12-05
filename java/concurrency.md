# Concurrency 并发

## tl;dr

- 健壮性比高性能更重要
- **读和写都要被同步**
- 尽量使用`Immutability`
- 优先使用虚线程处理高并发I/O密集型（open JDK21+,Kona JDK8+）
- 优先使用先进且成熟的并发工具库，如：java.util.concurrent
- 优先使用 executors、streams 而不是 threads
- 线程安全文档化，清楚地说明当前程序支持的线程安全级别

## 健壮性比高性能更重要

这里的健壮性既包括程序的正确性，同时也包含程序的可维护性。
并发编程首先要保证的是正确性，而并非是高性能。性能调优是建立在程序可以正确运行基础之上的，否则出现错误可能是灾难性的。

当多个线程共享可变数据的时候，每个读或写数据的线程都必须执行同步。
### 反例1
只加锁写方法，不加锁读方法，可能会出现多线程问题或隐患。

```java
private static int count = 0;

// Broken - get method requires synchronization!
public static int getCount() {
    return count;
}

public static synchronized void increment() {
    count++;
}
```


### 反例2
使用`volatile`时务必要小心，因为它并不是原子的。

```java
// Broken - requires synchronization!
private static volatile int nextSerialNumber = 0;

public static int generateSerialNumber() {
    return nextSerialNumber++;
}
```
解决方法有多种，其中一种方式是在`generateSerialNumber`方法中添加`synchronized`关键字。另一种更优雅的方式是使用`AtomicLong`。

### 正例

```java
// Lock-free synchronization with java.util.concurrent.atomic
private static final AtomicLong nextSerialNum = new AtomicLong();

public static long generateSerialNumber() {
    return nextSerialNum.getAndIncrement();
}
```

如果没有同步，就无法保证一个线程所做的修改可以被另一个线程获知。
未能同步共享可变数据会造成程序的活性失败（ liveness failure）和安全性失败（ safety failure ）。


## 尽量使用`Immutability`

避免并发问题一个有效的方式是`Immutability`。它的核心思想是：用消息传递，而非共享内存。
通过限制修改来换取程序的简洁性、安全性和可预测性。

Immutability**不可变对象是无副作用的**。**我们可以在多个线程之间安全地共享它**。

### 正例
设计无状态的类，使用`private final`修饰成员变量，尽可能使用`final`修饰类，如果类成员指向可变对象，不提供对外访问。

```java
public final class Money {
    private final double amount;
    private final Currency currency;
    // ...
}
```

## 优先使用虚线程处理高并发I/O密集型

虚线程（Virtual Threads）是Java 21引入的轻量级线程实现，特别适合处理高并发I/O密集型任务。在腾讯Kona JDK 8+中也提供了支持。


### 正例：使用虚线程

```java
// 使用虚线程处理大量I/O任务
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    List<Future<String>> futures = new ArrayList<>();
    
    for (int i = 0; i < 10000; i++) {
        futures.add(executor.submit(() -> {
            // I/O密集型任务，如HTTP请求
            return httpClient.send(request, HttpResponse.BodyHandlers.ofString()).body();
        }));
    }
    
    // 收集结果
    for (Future<String> future : futures) {
        String result = future.get();
        // 处理结果
    }
}
```

### 何时使用虚线程

- 适用场景：I/O密集型任务、高并发网络服务、大量阻塞操作
- 不适用场景：CPU密集型任务、需要线程本地存储的场景

## 使用先进且成熟的并发工具库

正确地使用 `wait` 和 `notify` 比较困难，就应该用更高级的并发工具来代替。
java.util.concurrent 中更高级的工具分成三类： 
- Executor Framework 
- 并发集合（ Concurrent Collection ）
- 同步器（ Synchronizer）

并发集合为标准的集合接口（如 List 、Queue 和 Map ）提供了高性能的并发实现。 为了提供高并发性，优先使用这些高性能的并发库。

## 优先使用 `executors`、`streams` 而不是 `threads`

你可以利用 `executor service` 完成更多的工作。例如：
- 可以等待完成一项特殊的任务
- 可以等待executor service 优雅地完成终止（利用 awaitTermination 方法）
- 可以在任务完成时逐个地获取这些任务的结果（利用 ExecutorCompletionService ）
- 可以调度在某个特殊的时间段定时运行或者阶段性地运行的任务（利用ScheduledThreadPoolExecutor ）。

executor service 它可以支持 fork-join 任务，这些任务是通过一种称作 fork-join 池的特殊 executor 服务运行的。
fork-join 任务用 ForkJoinTask 实例表示，可以被分成更小的子任务，包含 ForkJoinPool 的线程不仅要处理这些任务，还要从另一个线程中“偷”任务，以确保所有的线程保持忙碌，从而提高CPU 使用率、提高吞吐量，并降低延迟。
并发的 stream 是在 fork join 池上编写的，我们不费什么力气就能享受到它们的性能优势，前提是假设它们正好适用于我们手边的任务。

### Executor Framework的优势

你可以利用 `executor service` 完成更多的工作：
- 可以等待完成一项特殊的任务
- 可以等待executor service 优雅地完成终止（利用 awaitTermination 方法）
- 可以在任务完成时逐个地获取这些任务的结果（利用 ExecutorCompletionService ）
- 可以调度在某个特殊的时间段定时运行或者阶段性地运行的任务（利用ScheduledThreadPoolExecutor ）

### 正例：使用ExecutorService

```java
// 推荐：使用ExecutorService
ExecutorService executor = Executors.newFixedThreadPool(10);

List<Future<Integer>> futures = new ArrayList<>();
for (int i = 0; i < 100; i++) {
    final int taskId = i;
    futures.add(executor.submit(() -> {
        // 执行任务
        return processTask(taskId);
    }));
}

// 等待所有任务完成
for (Future<Integer> future : futures) {
    Integer result = future.get();
    // 处理结果
}

executor.shutdown();
```

### 反例：直接使用Thread

```java
// 不推荐：直接使用Thread
List<Thread> threads = new ArrayList<>();
for (int i = 0; i < 100; i++) {
    final int taskId = i;
    Thread thread = new Thread(() -> {
        processTask(taskId);
    });
    threads.add(thread);
    thread.start();
}

// 等待所有线程完成
for (Thread thread : threads) {
    thread.join();
}
```

### Fork-Join框架和并行Stream

executor service 它可以支持 fork-join 任务，这些任务是通过一种称作 fork-join 池的特殊 executor 服务运行的。
fork-join 任务用 ForkJoinTask 实例表示，可以被分成更小的子任务，包含 ForkJoinPool 的线程不仅要处理这些任务，还要从另一个线程中"偷"任务，以确保所有的线程保持忙碌，从而提高CPU 使用率、提高吞吐量，并降低延迟。

并发的 stream 是在 fork join 池上编写的，我们不费什么力气就能享受到它们的性能优势，前提是假设它们正好适用于我们手边的任务。

### 正例：使用并行Stream

```java
// 使用并行Stream处理CPU密集型任务
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

// 并行处理
List<Integer> results = numbers.parallelStream()
    .map(this::expensiveComputation)
    .collect(Collectors.toList());
```


## 线程安全文档化

方法声明中 synchronized 修饰符的存在是实现细节，而不是其 API 的一部分。它不能可靠地表明方法是线程安全的。
要启用安全的并发使用，类必须清楚地记录它支持的线程安全级别。

涵盖以下常见情况：

- **不可变的** — 这个类的实例看起来是常量。不需要外部同步。例如 String、Long 和 BigInteger。
- **无条件线程安全** — 该类的实例是可变的，但是该类具有足够的内部同步，因此无需任何外部同步即可并发地使用该类的实例。例如 AtomicLong 和 ConcurrentHashMap。
- **有条件的线程安全** — 与无条件线程安全类似，只是有些方法需要外部同步才能安全并发使用。例如 Collections.synchronized 包装器返回的集合，其迭代器需要外部同步。
- **非线程安全** — 该类的实例是可变的。要并发地使用它们，客户端必须使用外部同步来包围每个方法调用（或调用序列）。这样的例子包括通用的集合实现，例如 ArrayList 和 HashMap。
- **线程对立** — 即使每个方法调用都被外部同步包围，该类对于并发使用也是不安全的。线程对立通常是由于没有充分考虑并发性而导致的。当发现类或方法与线程不相容时，通常将其修复或弃用。

## 扩展阅读

- [Writing Java the Kotlin way](https://km.woa.com/group/45812/articles/show/522846)
- Java Concurrency in Practice
- Effective Java Item 78 - 84: Concurrency
