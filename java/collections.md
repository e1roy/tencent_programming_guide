# Java 集合框架使用规范

## tl;dr

- 认识常用的 Java 标准库中的集合类，按需选用
- 优先返回空集合而不是 null，避免 NPE
- 性能敏感场景下，创建集合时要考虑初始 size、遍历及增删等性能，选用合适实现类
- 使用集合类时，要考虑是否有并发场景

## 集合的空安全：

1. 不要在返回值中区分 Null 集合和空（长度为 0）的集合
2. 约定：优先返回非 Null 的空集合，以避免 NPE，避免区分 `empty collection` 和 `null collection`

### 反例

```java
// 反例：返回null导致调用方必须判空
public List<String> getItems() {
    if (noItems()) {
        return null;
    }
    return new ArrayList<>(items);
}
```

### 正例

```java
// 正例1：返回不可变空集合
public List<String> getItems() {
    return noItems() ? Collections.emptyList() : new ArrayList<>(items);
}

// 正例2：Java 9+的List.of()
public List<String> getItems() {
    return noItems() ? List.of() : new ArrayList<>(items);
}
```

## 集合的初始化

### 初始容量问题：

### 反例

```java
// 反例：未指定初始容量导致频繁扩容
List<String> list = new ArrayList<>(); // 默认容量10
for (int i = 0; i < 1000; i++) {
    list.add("item"); // 多次扩容影响性能
}
```

### 正例

```java
// 正例：根据预估大小初始化
List<String> optimizedList = new ArrayList<>(1000);
for (int i = 0; i < 1000; i++) {
    optimizedList.add("item"); // 不会触发扩容
}
```

### 集合可变性：

### 反例

```java
// 反例：直接使用Arrays.asList()返回的不可变列表
List<String> fixedList = Arrays.asList("a", "b");
fixedList.add("c"); // 抛出UnsupportedOperationException
```

### 正例

```java
// 正例：需要可变性时新建集合
List<String> mutableList = new ArrayList<>(Arrays.asList("a", "b"));
```

## 一个好的设计：不可变集合的使用

- 对外暴露的 List，优先提供`不可变的集合`：防止在自身逻辑控制范围之外，有人能修改 List 数据
- 遵循开放封闭原则：List 的修改对外封闭，仅业务自身 class 能修改
- 可以封装或使用一些工具库提供的`ImmutableList`，不对外暴露 add 或 remove 方法
- 可以借助泛型：List<? extends Data>，间接禁止他人 add （但是这种方式禁用不了 remove）
- 创建不可修改的 List 实例，如果有人外部修改，会抛出 crash

### 创建不可变 List 实例

```java
// Java 8及之前
immutableList = Collections.unmodifiableList(new ArrayList<>());
// Java 9+
immutableList = List.of("a", "b", "c");
// Java 10+
immutableList = List.copyOf(someList);
```

### 不可变集合的优势

- 线程安全 - 无需同步
- 防御性编程 - 防止意外修改
- 性能优化 - 可缓存哈希值
- 更简洁的代码 - 明确设计意图

## 集合并发问题

Java 中线程安全的集合类型有 Vector、Hashtable、ConcurrentHashMap、CopyOnWriteArrayList 等。

### List 的并发安全性：

### 反例

```java
// 反例：错误使用非线程安全集合
List<String> sharedList = new ArrayList<>();

// 多线程同时修改会抛出ConcurrentModificationException
IntStream.range(0, 10).parallel().forEach(i -> {
    sharedList.add("item" + i);
});
```

### 正例

```java
// 正例1：使用CopyOnWriteArrayList
List<String> safeList = new CopyOnWriteArrayList<>();
IntStream.range(0, 10).parallel().forEach(i -> {
    safeList.add("item" + i);
});

// 正例2：使用同步包装器
List<String> syncedList = Collections.synchronizedList(new ArrayList<>());
IntStream.range(0, 10).parallel().forEach(i -> {
    syncedList.add("item" + i);
});
```

### 复合操作的并发安全性（以 迭代器 为例）：

- 并发安全性 不等于 迭代器安全性
- 例如：Vector 是线程安全，指的是它的 add、remove、get 等方法在多线程情况下是安全的
- 如何进行复合操作（尤其是迭代器），仍然有线程安全问题，需要自行加锁

### 反例

```java
// 反例1：即使使用Vector，复合操作仍然不安全
if (!vector.contains(element)) {
    vector.add(element);        // 仍然可能产生竞态条件
}

// 反例2：迭代器过程中，进行修改，仍然不安全
Vector<Integer> vector = new Vector<>();
vector.add(1);
vector.add(2);
vector.add(3);

for (Integer i : vector) {
    System.out.println(i);
    if (someCondition) {
        vector.remove(i); // 会抛出 ConcurrentModificationException 异常（即使不是多线程，这里也会抛异常）
    }
}
```

### 正例

```java
// 正例1：对于复合操作，自己主动加锁
synchronized(lock) {
    if (!vector.contains(element)) {
        vector.add(element);    // 可以保证安全（所有对 element 的操作，都要基于lock对象加锁）
    }
}

// 正例2：迭代结束后，再统一进行remove
Vector<Integer> dataToRemove = new Vector<>();
for (Integer i : vector) {
    System.out.println(i);
    if (someCondition) {
        dataToRemove.add(i);
    }
}
vector.removeAll(dataToRemove);
```

### 在并发情况下，可能会出现数据不一致的问题。

例如，多个线程同时对一个 Hashtable 进行修改，可能会出现数据覆盖的情况。

```java
Hashtable<String, Integer> hashtable = new Hashtable<>();
hashtable.put("A", 1);

// 线程1：让 A 自增 10000 次
new Thread(() -> {
    for (int i = 0; i < 10000; i++) {
        hashtable.put("A", hashtable.get("A") + 1);
    }
}).start();

// 线程2：让 A 自增 10000 次
new Thread(() -> {
    for (int i = 0; i < 10000; i++) {
        hashtable.put("A", hashtable.get("A") + 1);
    }
}).start();

Thread.sleep(1000);
System.out.println(hashtable.get("A")); // 输出结果可能 < 20001
```

原因同样在于复合操作：hashtable 的 get 和 put，2 个操作并不是原子性的，如果想严格控制，也需要自行加锁：

```java
Object lock = new Object();

// 线程1：让 A 自增 10000 次
new Thread(() -> {
    for (int i = 0; i < 10000; i++) {
        synchronized(lock) {
            hashtable.put("A", hashtable.get("A") + 1);
        }
    }
}).start();

// 线程2：让 A 自增 10000 次
new Thread(() -> {
    for (int i = 0; i < 10000; i++) {
        synchronized(lock) {
            hashtable.put("A", hashtable.get("A") + 1);
        }
    }
}).start();
```

### 在高并发情况下，线程安全的集合类型可能会出现性能问题。

例如，`ConcurrentHashMap` 的性能在高并发情况下会优于 `Hashtable`，但在低并发情况下会劣于 `Hashtable`。

```java
ConcurrentHashMap<String, Integer> concurrentHashMap = new ConcurrentHashMap<>();
Hashtable<String, Integer> hashtable = new Hashtable<>();

long start1 = System.currentTimeMillis();
for (int i = 0; i < 10000000; i++) {
    concurrentHashMap.put("A" + i, i);
}
long end1 = System.currentTimeMillis();
System.out.println("ConcurrentHashMap: " + (end1 - start1));

long start2 = System.currentTimeMillis();
for (int i = 0; i < 10000000; i++) {
    hashtable.put("A" + i, i);
}
long end2 = System.currentTimeMillis();
System.out.println("Hashtable: " + (end2 - start2));
```

## 扩展阅读

- [Java Collections Framework 官方文档](https://docs.oracle.com/javase/11/docs/technotes/guides/collections/reference.html)
- [Effective Java 3rd Edition](https://learning.oreilly.com/library/view/effective-java-3rd/9780134686097/) - 多项关于集合的最佳实践
- [Java Concurrency in Practice](https://learning.oreilly.com/library/view/java-concurrency-in/0321349601/) - 并发集合的深入解析
- [Java Performance: The Definitive Guide](https://learning.oreilly.com/library/view/java-performance-the/9781449358457/) - 集合性能优化
- [Modern Java in Action](https://learning.oreilly.com/library/view/modern-java-in/9781617293566/) - Stream API 与集合的配合使用
