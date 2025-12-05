# Builder 建造者模式

## tl;dr

- 优先使用建造者模式处理参数多、组合复杂的对象构造。
- 避免使用长参数列表的构造函数，提高代码可读性和可维护性。
- 考虑使用 AutoValue 自动生成建造者代码，减少样板代码。
- 工厂方法适合简单场景，复杂场景优先选择建造者模式。


## 问题分析：参数过多的构造函数

考虑以下配置类：

```java
class Options {
    private final String name;
    private final int port;
    // http 或 ip 必须且只能设置一个
    @Nullable private final String httpAddress;
    @Nullable private final String ipAddress;
}
```

怎么构造这个类的对象？理所当然想到构造函数或工厂方法。
我们先来看看**构造函数**的方案。

```java
class Options {
    Options(String name, int port, @Nullable String httpAddress, @Nullable String ipAddress) {
        this.name = name;
        this.port = port;
        checkArgument(httpAddress != null ^ ipAddress != null, 
                "httpAddress和ipAddress必须且只能设置一个");
        this.httpAddress = httpAddress;
        this.ipAddress = ipAddress;
    }
}

// 调用方：参数含义不明确
Options options = new Options("svr", 36000, null, "139.211.231.23");
```

问题分析：
1. 参数过多导致可读性差
2. 无法通过方法名表达构造意图
3. 构造函数中需要参数验证逻辑
4. 无法支持可选参数

特别是，随着参数的数量越来越多，这个长参数列表会越来越难懂。

构建函数**没有名字**。一个类可以存在多个构造函数，但它们都是以重载的形式共存。例如，我们无法构建这样两个构造函数区分 http/ip 两种情况：

```java
class Options {
    Options(String name, int port, @Nullable String httpAddress, @Nullable String ipAddress) {
        // 这里省略实现...
    }

    Options(String name, int port, String httpAddress) {
        this(name, port, httpAddress, null);
    }

    // !!!编译错误，与上个构造方法同名。
    Options(String name, int port, String ipAddress) {
        this(name, port, null, ipAddress);
    }
}
```

另外一种方案是引入**工厂方法**。

```java
class Options {
    private Options(String name, int port, @Nullable String httpAddress, @Nullable String ipAddress) {
        // 构造逻辑
    }
    
    // 明确表达构造意图
    public static Options withHttp(String name, int port, String httpAddress) {
        return new Options(name, port, httpAddress, null);
    }
    
    public static Options withIp(String name, int port, String ipAddress) {
        return new Options(name, port, null, ipAddress);
    }
}

// 调用方：语义更清晰
Options httpOptions = Options.withHttp("svr", 443, "https://www.qq.com");
Options ipOptions = Options.withIp("svr", 36000, "139.211.231.23");
```

虽然解决了以上几个问题，但仍存在以下局限性：
1. 参数组合由于正交性，工厂方法数量会爆炸性增长。
2. 不支持可选参数灵活配置。

## Builder 模式解决方案
理想解决方案是使用Builder模式，标准 Builder 实现：
```java
class Options {
    private final String name;
    private final int port;
    @Nullable private final String httpAddress;
    @Nullable private final String ipAddress;
    
    private Options(Builder builder) {
        this.name = builder.name;
        this.port = builder.port;
        this.httpAddress = builder.httpAddress;
        this.ipAddress = builder.ipAddress;
        
        // 参数验证
        Preconditions.checkArgument(
            !(httpAddress != null && ipAddress != null),
            "httpAddress和ipAddress不能同时设置");
    }
    
    public static Builder builder() {
        return new Builder();
    }
    
    // Builder 内部类
    public static class Builder {
        private String name;
        private int port;
        private String httpAddress;
        private String ipAddress;
        
        public Builder name(String name) {
            this.name = name;
            return this;
        }
        
        public Builder port(int port) {
            this.port = port;
            return this;
        }
        
        public Builder httpAddress(String httpAddress) {
            this.httpAddress = httpAddress;
            this.ipAddress = null; // 确保互斥
            return this;
        }
        
        public Builder ipAddress(String ipAddress) {
            this.ipAddress = ipAddress;
            this.httpAddress = null; // 确保互斥
            return this;
        }
        
        public Options build() {
            Preconditions.checkNotNull(name, "必须设置name");
            Preconditions.checkArgument(port > 0, "port必须大于0");
            return new Options(this);
        }
    }
}

// 调用示例
Options options = Options.builder()
    .name("svr")
    .port(36000)
    .ipAddress("139.211.231.23")
    .build();
```

如此，我们可以优雅地处理多个参数的情况，Builder模式让我们代码具有以下的优势：
1. 参数设置语义清晰
2. 支持可选参数和默认值
3. 参数验证集中处理
4. 支持流畅的链式调用

## 使用 AutoValue 自动生成 Builder
以上 Builder 模式虽然看起来很完美了，但是编写一个 Builder 会有大量的 boilerplate 代码。这时，我们可以使用 Guava 库中的 `AutoValue` 和 `AutoValue.Builder` 来简单地生成 data class 与 data class 的 Builder。

AutoValue 位于： https://github.com/google/auto/blob/main/value/userguide/index.md

AutoValue 支持 Builder，如：
https://github.com/google/auto/blob/main/value/userguide/builders.md

我们使用AutoValue来改造上面的Builder实例代码：
```java
import com.google.auto.value.AutoValue;

@AutoValue
abstract class Options {
    abstract String name();
    abstract int port();
    @Nullable abstract String httpAddress();
    @Nullable abstract String ipAddress();
    
    static Builder builder() {
        return new AutoValue_Options.Builder();
    }
    
    @AutoValue.Builder
    abstract static class Builder {
        abstract Builder name(String value);
        abstract Builder port(int value);
        abstract Builder httpAddress(String value);
        abstract Builder ipAddress(String value);
        abstract Options build();
    }
}

// 使用方式相同
Options options = Options.builder()
    .name("svr")
    .port(36000)
    .ipAddress("139.211.231.23")
    .build();
```


## 扩展阅读

- *Effective Java* Item 2: Consider a builder when faced with many constructor parameters
- *Design Patterns*: Builder Pattern
