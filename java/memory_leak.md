# Memory Leak 内存泄漏

## tl;dr

- 及时清理无用的引用，特别是对于静态变量和集合类。
- 使用弱引用`WeakReference`来引用可回收的对象。
- 使用缓存库来实现缓存过期策略。
- 在监听器、观察者模式中，确保注销对象。
- 在多线程场景中，正确管理线程池资源，避免创建过多线程或管理不当。
- 使用内存监控工具和分析器定期检测潜在内存泄漏。

## 为什么存在内存泄漏：
虽然 Java 有垃圾回收(Garbage Collection, GC)机制，而且 JVM 的垃圾回收是表现最好的垃圾回收的语言之一（尤其在 ZGC 之后），但是我们仍然需要注意无意识的内存泄漏。
一个对象的生存周期比我们预想的时间要长。在某些特殊场景如移动端开发，这个问题尤为显著：安卓对对象有明确的生命周期的预期，当一个对象在生命周期外仍然存活并且被调用，可能会出现预料之外的后果。

在 Java 中，内存泄漏通常是指对象不再被使用，但仍然被引用，导致内存无法被垃圾回收器回收。
这可能导致程序运行速度变慢、内存占用过高甚至引发崩溃。以下是一些可能导致 Java 内存泄漏的场景：

1. 静态集合类：如 `HashMap`、`ArrayList` 等静态集合类，如果没有适时地清理它们的引用，它们将一直存在于内存中，无法被回收。
2. 缓存：为提高性能和响应速度，可以将部分数据缓存在内存中，但如果没有适当的缓存处理和过期机制，未使用的缓存数据无法在内存中释放。
3. 监听器或者观察者模式：当在对象中添加监听器或观察者，但没有在适当时机删除，可能导致对象无法被回收。这些对象将一直被监听器或观察者对象引用。
4. 常驻线程：如果未设置线程池，长时间运行的线程如果不正确关闭，也可能导致内存泄漏。线程池中线程在运行时可能引用了一些对象，若不正确返还线程到池或关闭线程，未能正确释放的资源将一直存在。
5. Java类加载器：多次加载同样的类，但未能适时卸载，也可能导致内存泄漏。这可能出现在热部署或动态加载扩展模块的场景中。

## 最佳实践
### 静态集合类，提供删除引用方法并在合适时机调用

```java
public class UserManager {
    private static List<User> userList = new ArrayList<>();

    public void addUser(User user) {
        userList.add(user);
    }

    // 提供 removeUser 用来主动释放内存
    public void removeUser(User user) {
        userList.remove(user);
    }
}
```

在上述示例中， `userList` 是一个静态的集合。如果用户添加后不再使用，但没有调用  `removeUser`  方法移除，就会导致内存泄漏。

### 缓存管理，在缓存失效时考虑主动清理，或使用有自动过期策略的缓存库

```java
public class CacheManager {
    private Map<String, Object> cache = new HashMap<>();

    public Object get(String key) {
        return cache.get(key);
    }

    public void put(String key, Object value) {
        cache.put(key, value);
    }

    public void remove(String key) {
        cache.remove(key);
    }
}
```

在上述示例中， `cache`  存储数据用于提高性能。如果不适时调用  `remove`  方法删除缓存数据，可能发生内存泄漏。这种场景下，可以考虑使用支持过期策略的缓存库。

### 监听器或者观察者模式，在合适时机下注销监听对象（一般与添加监听对象对称处理）

```java
public class DataObserver {
    private List<EventListener> listeners = new ArrayList<>();

    public void addListener(EventListener listener) {
        listeners.add(listener);
    }

    public void removeListener(EventListener listener) {
        listeners.remove(listener);
    }
}
```

在此示例中，如果向  `DataObserver`  添加了  `EventListener` ，但未在适当时机调用  `removeListener`  移除，可能导致内存泄漏。

### 常驻线程，使用线程池来替代来动态的创建独立线程

```java
public class Worker implements Runnable {

    @Override
    public void run() {
        while (true) {
            // 执行任务
        }
    }
}

public class Main {
    public static void main(String[] args) {
        new Thread(new Worker()).start();
    }
}
```

在上述示例中， `Worker`  中的  `run`  方法会一直执行，导致线程不会被正确释放。此种情况下，可以使用线程池进行管理以防止内存泄露。

### Java 类加载器，避免重复多次加载

```java
public class DynamicClassLoaderExample {

    public static void main(String[] args) throws ClassNotFoundException, IllegalAccessException, InstantiationException {
        while (true) {
            URLClassLoader classLoader = new URLClassLoader(new URL[]{new URL("file:///path_to_your_jar/example.jar")});
            Class cls = classLoader.loadClass("com.example.TestClass");
            Object obj = cls.newInstance();
            // Do something with obj
        }
    }
}
```

在上述示例中，我们循环加载了同一个jar文件。如果没有正确释放卸载类加载器，可能导致内存泄漏。

## 扩展阅读

- Effective Java Item 7: Eliminate obsolete object references
