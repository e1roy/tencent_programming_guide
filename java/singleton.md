# Singleton 单例

## tl;dr

- 谨慎使用单例模式，优先考虑按需创建
- 优先使用静态内部类方式，谨慎使用双重检查锁方式
- 避免使用 **`ThreadLocal`** 来解决单例模式下的线程安全问题


## 谨慎使用单例

单例是具有明显风险的模式。但它可以带来以下好处：

- 可以节省内存
- 有效控制实例数量
- 方便全局管理

但是，在大部分情况下，单例带来的麻烦都大于它带来的好处：

- 单例创建后会永远占用内存。如果单例的实例对象过于庞大或者单例的使用频率不高，那么极大可能会造成不必要的内存浪费，影响程序的性能。
- 单例不利于线程安全性。当单例对象是**可变对象**时，频繁的读写需要通过同步机制保证，而这不但易出错，而且可能反而因为锁竞争降低性能。
- 单元测试困难：全局状态难以隔离测试，单例也难以模拟和替换。

## 替代方案

你应该总是优先考虑**按需创建**。

- 虽然现代计算机的CPU资源往往比内存更充足，但是对于一些短暂而频繁的操作（例如锁、IO操作、调用外部 `WebService`等），按需创建对象可能比单例更加友好，因为这些短暂的操作可能会在单例模式下被长时间的锁住。


## 如何实现单例

### 饿汉式（Eager Initialization）

最简单的方案也就是将类的一个实例放在一个静态成员中，即：

```java
public class Singleton {
    private static Singleton instance = new Singleton();
    
    public static Singleton getInstance() {
        return instance;
    }
}
```

这样做是线程安全的，但是坏处是无法懒加载。

注意: 如果你的单例需要懒加载，这是个信号提醒你是否真的需要单例。是否只要按需创建就好了？

### 双重检测锁（Double Checked Locking）

Double Checked Locking 是一种线程安全并且可懒加载的单例实现方式，但容易出错。考虑以下例子：

```java
// 错误: instance 对象缺少  volatile 关键字
public class Singleton {
    private static Singleton instance = null; // 缺少 volatile 关键字

    private Singleton() {}

    public static Singleton getInstance() {
        if (instance == null) {
            synchronized(Singleton.class) {
                if (instance == null) {
                    instance = new Singleton(); // 存在指令重排序问题
                }
            }
        }
        return instance;
    }
}
```

这个实现看上去很正常，但是因 `instance` 缺少 `volatile`可能会引起 并发可见性问题。并且这个问题是 **Heisenbug** (较难发现、重现和调试的隐蔽bug).


### 静态内部类（Static Inner Class）【推荐】
Static Inner Class 方式实现单例是一种懒加载、线程安全且高性能的单例模式。
它利用了 Java 类加载的机制，天然地保证了线程安全和单例唯一性，而且不需要加锁，不会有锁开销，可读性也较高，是单例实现的推荐方式。

```java
public final class Singleton {
    private Singleton() {}
    
    private static class Holder {
        static final Singleton INSTANCE = new Singleton();
    }
    
    public static Singleton getInstance() {
        return Holder.INSTANCE;  // 首次调用时加载Holder类
    }
}
```

## 谨慎使用 `ThreadLocal` 对象

如果使用`ThreadLocal`来解决单例模式下的线程安全问题，则可能会带来更多的问题。因为`ThreadLocal`往往会把对象实例存储在线程局部变量中，这可能会导致线程之间的逻辑耦合度增加，导致代码难以维护和理解。

```java
// 错误：使用ThreadLocal，当线程复用时可能导致 `userSession` 数据泄露或逻辑错误
public class SessionManager {
    private static final ThreadLocal<UserSession> userSession = new ThreadLocal<>();

    // 单例实例
    private static final SessionManager INSTANCE = new SessionManager();

    private SessionManager() {}

    public static SessionManager getInstance() {
        return INSTANCE;
    }

    public void setUserSession(UserSession session) {
        userSession.set(session);
    }

    public UserSession getUserSession() {
        return userSession.get();
    }
}
```


