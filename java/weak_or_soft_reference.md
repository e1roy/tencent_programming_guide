# Weak/Soft Reference 弱/软引用

## tl;dr

- 当引用可以（且应该）随时被回收，使用 `Weak Reference`。
- 当引用可以随时被回收，但希望尽可能地保留，使用 `Soft Reference`。
- 当引用不应该被回收，使用常规引用，即 `Strong Reference`。

## 理解 `Weak Reference` 与 `Soft Reference`

`WeakReference` 和 `SoftReference` 有相似的意图：

> 我并不太需要这个引用。如果其它所有的对这个对象的引用都不存在了，那我也可以放弃这个引用，使之被 GC 回收。

但是，弱引用相对更“积极”地交出所有权，而软引用相对更“坚持”所有权：

- 只要 `WeakReference<T>` 是对象唯一的引用，GC 可以随时收回这个对象。
- `SoftReference<T>` 则会尽可能地保持住这个对象，直到内存不足，GC 必须回收。

需要使用非强引用的场景主要来自回调，考虑如下代码：
```java
class Activity {
    Context context;
    
    // 返回一个对 ClickEvent 的 handler。注意到这个 handler 持有所在 Activity 的引用。
    public Consumer<ClickEvent> onClickEventHandler() {
        return (h) -> {
            this.context.showToast();
        }
    }
}
```

这样非常自然的做法，但会导致内存泄漏。一个外部的对象可能会始终持有 `Activity`，即使当该 `Activity` 已经被彻底关闭。

这时应该使用 `WeakReference` 而不是 `SoftReference`。当我不需要拿到强引用时，我往往不希望这个引用生存周期因我而变。

### 正例
使用 `WeakReference<Activity>` 来弱引用 `activity`, 允许外部直接释放回收对象
```java
class Activity {
    Context context;

    // 返回一个对 ClickEvent 的 handler，使用 WeakReference< Activity >
    public Consumer<ClickEvent> onClickEventHandler() {
        WeakReference<Activity> weakThis = new WeakReference<>(this);
        return (h) -> {
            Activity activity = weakThis.get();
            if (activity != null && activity.context != null) {
                activity.context.showToast();
            }
            // else: activity 已经被回收，无需操作，避免内存泄漏
        };
    }
}
```

## Soft Reference 使用
`SoftReference` 推荐适用的场景主要是 `Cache`。

但是也要注意：显式地设置缓存过期时间并清理，例如使用 `LRU`，往往会是更好的主意。
毕竟，JVM 的特点是一旦堆中出现了大量的对象未被回收，GC 往往会表现糟糕。
