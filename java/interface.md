# Interface 接口

## tl;dr

- **谨慎为接口添加 `default` 方法。** 
- 尽可能使用**接口**引用对象，而不引用具体实现。

## 谨慎为接口添加 `default` 方法
`default` 方法主要用于接口演化和向后兼容，但会强制引入行为到所有实现类，因此必须确保所有接口实现方和调用方都能正确处理 `default` 引入的行为。添加前必须确认：
  - 不会与现有接口和实现类的方法冲突，尤其多接口同名default方法。
  - 行为对所有实现类都合理，必要时使用`@Override`强制实现类覆盖。
  - 避免用于高变更频率的方法实现。

多接口同名default方法冲突示例：
```java
interface InterfaceA {
  default void execute() { System.out.println("A"); }
}

interface InterfaceB {
  default void execute() { System.out.println("B"); }
}

class Impl implements InterfaceA, InterfaceB {
  @Override
  public void execute() {
    ......; // 自定义实现来覆盖解决冲突
  }
}
```

Effective Java 中列举了添加`default` 方法对实现类影响典型例子。
Java 8集合接口`Collection`添加了`removeIf` 默认方法， 但Apache Commons 库中实现集合接口的`SynchronizedCollection`类为用户提供了加锁的线程安全集合能力， 但没有覆盖`removeIf`方法。
在多线程并发情况下使用 removeIf 方法就可能导致出现`ConcurrentModificationException`或其他异常行为。
因此向现有接口添加默认方法存在风险，特别是广泛使用的超级接口，需要谨慎评估。

```java
interface Collection<E> {
    default boolean removeIf(Predicate<? super E> filter) {
        // 非线程安全的默认实现
    }
}

// 虽然提供了线程安全的集合类，但因未覆盖 Collection 的默认 removeIf 实现影响，存在并发安全问题。
class SynchronizedCollection<E> implements Collection<E> {
    // 没有显示 @Override 覆盖 default方法
}
```

## 使用接口引用对象

接口是**契约**：

- **调用方**应该按契约调用接口，而不关心背后的实现
- **实现类**应该完整满足接口的规格，而不需要用户理解它的细节

因此，三者关系是 **调用方 -- > 接口 < -- 实现**，即调用方不应“穿透”接口直接依赖实现类。这是遵循“面向接口编程”原则，是Java实现模块化解耦的核心机制。

### 正例
使用接口来引用对象

```java
class Factory {
    // Facroty 只需要依赖 Machine 接口，不关注 Machine 的具体实现
    List<Machine> machines;
    ......
    public void runAll() {
        for (Machine machine : machines) {
            machine.execute(); // 通过接口引用，不依赖具体类
        }
    }
}

interface Machine {
    void execute();
}

class ElectricifiedMachine implements Machine {
    // 具体实现细节（如电气化逻辑）
}
```

### 反例
直接引用实现类，耦合了不必要的实现细节
```java
class Factory {
    // 绑定 ElectricifiedMachine 具体实现！
    private List<ElectricifiedMachine> machines; 
    ......
    public void runAll() {
        // 若需替换实现类，必须修改此处逻辑
        for (ElectricifiedMachine machine : machines) {
            machine.execute(); 
        }
    }
}
```

## 扩展阅读

- Effective Java Item 20: Prefer interfaces to abstract
- Effective Java Item 21: Design interface for posterity
- Effective Java Item 23: Prefer class hierarchies to tagged classes
- Effective Java Item 64: Refer to objects by their interfaces
