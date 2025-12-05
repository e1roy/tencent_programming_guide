# Finalizer 终结函数

## tl;dr

- 避免使用 Finalizer。如果使用 Finalizer 保证资源回收，请实现 `AutoClosable` 并使用 `try-with-resources` 机制。 （`try-with-resources` 见 [关闭资源](https://iwiki.woa.com/pages/viewpage.action?pageId=4007320737)）

## Finalizer 的问题

> 对于熟悉 C++ 的同学： **Finalizer 不是 Destructor**

- `Finalizer` 的执行时机不确定，是因为 `Finalizer` 的执行是由 GC 算法确定的。所以在一个对象引用变空后和它的 `finalizer` 被执行间，可能会间隔任意时间。
  - 不在 `finalizer` 中执行任何对 **时间要求严格** 的操作。
  - 不应该期待 `finalizer` 会被执行，所以不应该使用 `finalizer` 做资源释放操作。
- `Finalizer` 有巨大的性能损耗。与 `try-with-resources` 相比，耗时多出十倍以上。
- `Finalizer` 有严重的安全问题。 常见如终结器攻击（Finalizer Attack),可能绕过构造过程中的安全检查，导致本应创建失败的不完整对象被保留和利用，引发安全漏洞。

注意[`System.gc()`](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/lang/System.html#gc%28%29) 和 [`System.runFinalization()`](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/lang/System.html#runFinalization%28%29)并不会保证 finalize 被马上执行。它们都是**建议性**的，GC 的实际逻辑受 JVM 自己控制。

所以依赖 `Finalizer` 关闭资源是非常错误的操作。使用 `try-with-resources` 显式地关闭：

```java
// Bad：不要在 finalize 释放资源
class File {
    private void close() {
        // ...
    }
    protected void finalize() {
        close();
    }
}

// Good: 使用 try-with-resources 管理资源
class File implements Closeable {
    @Override
    public void close() {
    }
}

try (File file = new File(...)) {
    // ...
}
```

## 不要在 Finalizer 中 null 成员

不要尝试如下代码：
```java
// Bad： finalizer! Useless.
class Car {
    String name;
    Car() {
        name = "porsche";
    }
    protected void finalize() {
        name = null;
    }
}
```
Finalizer 本来就没有意义，这个操作尤其没有任何意义 -- 它甚至不会加快 GC 的回收。

## 扩展阅读

- Effective Java Item 8: Avoid finalizers and cleaners
- [SpotBugs Finalizer nulls fields](https://spotbugs.readthedocs.io/en/latest/bugDescriptions.html#fi-finalizer-only-nulls-fields-fi-finalizer-only-nulls-fields)
