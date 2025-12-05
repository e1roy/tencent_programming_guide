# 常见命名辞典

## tl;dr
- 命名是一门平衡准确性和简洁性的艺术：名字应该包含足够的信息能够表达完整的含义，又应该不包含冗余的信息。
- 命名考虑 准确、简洁、一致的基础原则
- 命名优先考虑复用现有成熟代码词汇表

下文按用途归类了常见动词和名词，并对同义近义词进行了辨析。

## 类/名词

### 类继承： Interface / Abstract class / Implementation

**Java**:

- Interface: 通常不需要额外的表示。不要加 `I` 前缀，或后缀 `FooInterface`。
- Abstract class: 通常会添加 `Abstract/Base` 前缀以明确属性。这是因为 Interface/Impl 是常见的，Class 也是常见的，但是基于继承的抽象类是特殊的、应该予以避免的，应该给予特殊标记。
- Implementation:
    1. 如果不实现接口，通常不需要任何特殊修饰符。
    2. 如果以 "is-a" 的方式实现了某个接口，那么通常实现会以 `{InterfaceName}Impl` 的方式命名。
    3. 如果一个类实现了多个接口，那么通常这个类应该是以作为主要目标的接口为基础命名。例如 `class BazelBuilderImpl implements BazelBuilder, AutoClosable, Serializable`。
    4. 如果一个接口有多个实现，通常会基于它们本身的实现特点命名，并且**不**使用 `Impl` 后缀。`Default` 通常用来命名默认的实现，即其它实现如果不存在会 fallback 到的实现。如果所有的实现都是平等地位，那么不要使用 `Default` 命名。

```java

// https://github.com/bazelbuild/bazel with some fake examples

public interface SkyFunction {}

public abstract class AbstractFileChainUniquenessFunction implements SkyFunction {}

public class DefaultSkyFunction implements SkyFunction {}

public class BazelModuleInspectorFunction implements SkyFunction {}

public interface VisibilityProvider {}

public final class VisibilityProviderImpl {}
```

**C++**:

- C++ 的 interface 是通过抽象类不存在基类成员变量模拟。通常接口所有的成员函数都是公开纯虚函数。
- 使用 `Impl` 表示实现。
- Abstract class: 通常会添加 `Base` 后缀以明确属性。这是因为 Interface/Impl 是常见的，Class 也是常见的，但是基于继承的抽象类是特殊的、应该予以避免的，应该给予特殊标记。

```C++
// levelDB
// includes/db.h
class DB {
 public:
  virtual ~DB(); // MUST!
  virtual Status Delete(const WriteOptions&, const Slice&) = 0;
}

// db/db_impl.h
class DBImpl : public DB {}

// rocksDB
// Base class
class CacheShardBase {}
```

**Go**:

- Go 的 `interface` 从来不是用来做 "is-a" 定义的。Go 的 `interface` 契约通过 **duck typing** 满足。`interface` 应该在消费方定义，而非提供方。因此， `interface Foo/struct FooImpl` **不应该出现**。
- Go 也并没有抽象类，虽然可以将一个结构体嵌入到另一个结构体中。所以 `Base/Abstract` 也极少出现。
- 原则上，Go 的类关系更为简化，命名更强调意义优先，因此在命名时避免使用修饰性前后缀。

## 异常: Exception/Error

**Java**:

所有的**异常**扩展应该以 `Exception` 为后缀。所有的**错误**应该以 `Error` 为后缀。
对异常和错误的区别请参见 https://docs.oracle.com/javase/7/docs/api/java/lang/Throwable.html

```java
public class IllegalArgumentException;

public class OutOfMemoryError;
```

**C++**:

C++ 的 `exception` 通常指语法特性，与 `throw` 对应，而 `error` 可以用来表示具体的异常错误。

```C++
// stdlib
std::exception;
std::runtime_error
```

**Go**:

所有的错误都是 `error`。因此，所有自定义的对 `error` 的扩展都以 `Error` 作为后缀。

```Go
os.PathError
```

## 测试：Test / Spec

Java/Go/C++/TypeScript/Python 使用 `Test` 作为测试类的后缀。

Java/C++/TypeScript/Python 有时使用 `Spec` 作为自动化验收测试类的后缀，用于和单元测试做区分。

## 模块：Module/Component

`Module/Component` 通常会在框架中使用。不同的语言/框架对于 `Module/Component` 有不同的定义。
在非框架代码中应该减少使用 `Module/Componenet` 等命名，因为可能与已有框架冲突，并且 `Module/Componenet` 过于宽泛而缺少实质意义。

`Module/Component` 是意义相近的词，都可以表示“模块”或者“组件”。两者虽然有细微的分别，但是框架通常都显式（即在文档中指定，或者通过框架语义约束）地把它们定义为框架语境下的某些结构层级。

总结，`Module/Component` 命名应该注意：

- 只应该在框架代码中使用。
- `Module/Component` 应该在框架的语境中给出确切的定义。

## 服务:Service

Service 通常用于作为 C-S 架构下的服务提供者的名称的后缀，如：

```java
HelloService
```

但除此之外，Service 可以表示任何**长期存活的、提供功能的组件**。例如：

```java
BackgroundService // Android 后台服务

ExecutorService // 线程池执行服务，也是服务
```

BAD: 不要使用 Svr 缩写。使用全称。

## 容器：Holder/Container/Wrapper

Holder/Container/Wrapper 都表示“容器”，具有同一个意图：为一个类增加额外的数据/功能，例如：

- 添加某些语境下的元数据(Decorator 模式)
- 做适配以在另一个环境中使用（Adapter 模式）

通常的结构如下：

```java
class ObjectHolder {
  private final Object object;
  // other stuff ...
  
  public Object object() {}

  // Other methods
}
```

这三个词没有区别。在同一个项目中，应该**保持一致**。

## 控制类 ：Manager/Controller

Manager 和 Controller 是同义词。它们通常用来表示专门控制某些类的类。

这两个词有以下几个常见场景：

- Manager 管理资源，如 `DownloadManager`, `PackageManager`。
- Manager 通常特指管理对象的生命周期，从创建到销毁。
- Controller 通常在某些架构中，尤其是 MVC (Model-View-Controller）。

即使如此，Manager/Controller 是无意义词汇，出现时充满了可疑的味道 -- 类应该管理它们自己。 Controller/Manager 多了一层抽象，而这很可能是多余的。
认真考虑是否需要 Manager/Controller。

## 辅助类：Util/Utility/Utils/Helper/{ClassName}s

辅助类是强制 OOP 的语言(i.e. Java) 所需要的特殊类。通常它们是一些辅助方法的合集。

**Java**:

将与某个类型相关的辅助方法放在一个类中，并且以复数形式命名辅助类。如：

```java
// Java std lib
public final class Strings {}

public final class Lists {}

public final class Collections {}
```

避免使用 `Util/Utility/Utils/Helper`。它们是无意义词汇。

**C++**:

使用全局方法。如果担心命名污染，将之置入更细粒度的 namespace。

**go**:

使用全局方法。

## 函数式 ：Function/Predicate/Callback

Function 通常表示任意函数。
Predicate 表示命题，即通常返回类型为 `bool`。
Callback 指回调函数，指将函数作为参数传递到其它代码的某段代码的引用。换言之， Function 可以作为 Callback 使用。因此，Callback 在现代函数式编程概念流行后，通常很少使用。

**Java**:

熟悉 Java 8 开始提供的函数式语义。如果可以使用标准库的语义，不要自己创建名词。
注意 `Function` 指单入参、单出参的函数。如果是多入参的函数，直接定义 FunctionalInterface 并且按用途命名，例如 `OnClickListener.listen(Context, ClickEvent)`。

```java
// java.util.function
Predicate<T>   // f(T) -> bool
Function<T, R> // f(T) -> R
Consumer<T>    // f(T) -> void
Supplier<T>    // f() -> T
```

**C++**:

first-class 函数的标准类型为 `std::function`。

C++ 表示命名函数对象的惯用法是 `fun`。Stdlib 中会缩写 `function` 为 `fun`，如 `pmem_fun_ref`，因此与 stdlib 一致，在代码中不要使用 `fn` 或是 `func` 。

**Go**:

Go 通常使用 `Func` 或是 `Fn` 表示函数类型。

```Go
type ProviderFunc func(config ConfigSource, source PassPhraseSource) (Provider, error)

type cancelFn func(context.Context) error
```

在同一个项目中，应该**保持一致**。

作为参数时，函数不会特意标明 `Fn`，而是遵从普通的参数命名方式：

```Go
func Sort(less func(a, b string) int)
```

## 设计模式类

类/方法通常都按它们的行为模式来命名。恰好，设计模式就归类抽象了很多行为模式。所以设计模式提供了很多好的名字。

### 创建式

Factory: 工厂模式。通常，使用工厂方法即可，不需要一个额外的工厂类。只有当工厂特别复杂，或者工厂有状态时再考虑使用工厂类。

Builder：构建者模式。一般来说 Builder 都是作为 inner class，如

```java
class Foo {
  static class FooBuilder {}
}
```

### 行为式

Adapter: 适配器

在 GoF 中 Adapter 本来是将一个类封装以可以被作为另一个类型被调用，这样调用方不需要额外改变代码。这种用途通常被内化到容器上，见上文[容器类]部分。

在现代，Adapter 更多地被作为 数据类 -> 数据类的转化，如常见的 pb -> pb：

```java
class ProtoAdapter<S, T extends Message> {}
```

Decorator：装饰器

在 GoF 中 Decorator 本来是将一个类作为抽象类，通过组合+继承实现添加功能。实际上现代的编程实践中往往通过直接提供一个容器的封装提供装饰功能，见上文 [容器类]部分。
所以 GoF 式 Decorator 并不常见，除非像 Python 在语法层面提供了装饰器。在 Java 中类似的功能是**注解**。

Delegation：委派模式

GoF 中是非常基本的模式：由一个类负责接受请求，并把请求转发到合适的实例类中执行。

```java
class RealPrinter {}

class Printer {
  RealPrinter printer;
}
```

Delegate 非常常见，也提供了两个名字，请注意区分：

- `Delegate` 是**被委任**的对象。
- `Delegator` 是**委任**对象。

所以，通常情况下 `Delegator` 在命名中会更常见，类似于 `Dispatcher`。`Delegate` 更多作为一个类型或是接口被实现。具体的选择参见 [编排] 部分。

Facade: 外观模式

GoF 中 Facade Pattern 通常是指为子系统提供一个更高层的统一界面，屏蔽子系统的独有的细节。
在现实中，Facade 通常用来为非常复杂的类/系统定义一个较为简化的界面，如：

```java

// proto, extremely complicated TripResponse
message TripResponse {
  // ...
  // ...
  string last_message = 3279;
}

class TripResponseFacade {
  private final TripResponse response;

  Trip trip();

  Endpoint source(); // Abstracted and processed
  Endpoint target(); // Abstracted and processed
}
```

Facade 与 Adapter 的主要区别在于 Facade 的主要目的是为了**简化**，或者说更高层次的抽象，并且通常简化的界面不服务于专门的对接类。 Adapter 通常是为了一个特定的对接类实现。

注意 `Facade` 命名通常可以省略。仅当你的意图是明确告知用户这是关于某个类的外观时使用。

Proxy：代理模式

GoF 中代理模式用来添加一层抽象，以对实际类进行控制，并添加某些行为（如 lazy/memoized），或是隐藏某些信息（例如可见性或是执行远程调用）。

Proxy 与 Facade 的区别在于 Proxy 通常是为了额外的控制/记录等行为，而非只是为了更高的抽象/简化。

注意 Proxy 作为代码模式时，通常不应该出现在命名之中。使用具体的 Proxy 的目的作为命名，如 `LazyCar` 或是 `TracedRuntime`，而非 `CarProxy` 或是 `RuntimeProxy`。

Proxy 还有另一个含义就是真正的“代理”，如代理服务器。在这种情况下，使用 Proxy 是合适且应该的。这也是另一个为什么代理模式不应该用 Proxy 命名的原因。

Iterator: 迭代器

时至今日仍然最常见的模式之一。Interator 有以下两个术语，不要混淆：

- Iterable： 迭代容器
- Iterator： 迭代器

Visitor: 访问者模式

访问者模式用来遍历一个结构内的多个对象。对象提供 `accept(Visitor)` 方法，调用 `Visitor.visit` 方法。

即使如此，`Visitor` 应该并不常见，因为它可以简单地被函数式的写法替换：

```java
class Car {
  void accept(Consumer<Car> visitor); // No longer need to define Visitor class.
}
```

Observer/Observable: 观察者模式

> Observer/Publisher/Subscriber/Producer/Consumer

时至今日最常见的模式之一。和事件驱动编程(Event-based)有紧密关系 -- Oberservable 发布消息，所有注册的 Obeserver 会接收消息。
Publisher/Subscriber 也是类似的，它们的区别在于 Observer 模式往往是强绑定的 -- 注册和分发通常在 Observable 类中实现； 而 PubSub 模式通常有专门的 Message Broker，即 Publisher 与 Subscriber 是完全解耦的。

PubSub 与 Producer/Consumer 的区别是：

- Publisher/Subscriber: 在事件流系统中，表示 **1:N** 广播/订阅。
- Producer/Consumer: 在整个流系统中，专指 **1:1** 生产/消费。Producer/Consumer 也是 Pub/Sub 系统的组件（广播也是一对一广播的）。
    1. 有些系统(Kafka)使用 Consumer Group 表示 Subscriber。

所有的消息注册的模式由三部分组成：

- Notification： 消息本身
- Sender：消息发送者/注册
- Receiver： 消息接收者

关于命名参见 [事件] 部分。

Strategy：策略模式

> Strategy/Policy

策略模式在 GoF 中用以指定某个行为在不同场景下的不同实现，作为“策略”。

Strategy 模式往往不是很显式。现代通常使用 Strategy 表示实际的“策略”，即对信息不同的处理策略，而不采取 Strategy 模式的含义。

在“策略”这个语义中，Strategy/Policy 没有区别。在同一个项目中，应该**保持一致**。

Command：命令模式

命令模式在 GoF 中以类开代表实际行动，将行动封装，以支持重复、取消等操作。

Command 在现代编程实践中可以通过简单的函数式方案替换，如：

```C++
Function<T, T> command; // Java

std::function<const T&(const T&)> command; // C++

type Command func(T*) T* // Go
```

现代通常使用 Command 表示实际的“命令”，而不采取 Command 模式的含义。

Null Object 模式

> Tombstone

Null Object 模式不在 GoF 当中。它是一个用来代替 null 的 object，对其所有的操作都会被吞掉。 Null Object 主要是为了避免空指针。
合理的**零值**，例如 go time.Time = 0，也可以理解为一种 Null Object。

通常会有一个专门的对象表示 Null Object。可以借用 `Tombstone` 表示 Null Object。

Object Pool 对象池模式

> Pool

对象池模式不在 GoF 当中。它是将一系列昂贵的对象创建好放在一个池子中，并使用户通过向池子申请对象，而不再自己手动地创建/销毁对象。最著名的池化的例子是线程池，即 ThreadPool。

Pool 通常用来表示对象池子，例如 `ThreadPool, ConnectionPool`。

> Arena

Arena 是指 [Region-based memory management](https://en.wikipedia.org/wiki/Region-based_memory_management)，是指一片连续的内存空间，用户在其中分配创建对象，管理内存。

## 前/后缀

### 并发/异步

>Concurrent
 Synchronized
 Async

有时候我们需要特别标明一个类是线程安全的。通常这是特意为了与另一个线程不安全的实现做区分。典型的例子是 `HashMap` 和 `ConcurrentHashMap`。如果一个类只是单纯是线程安全的，那么通常不需要在名字里特意说明，在文档里说明即可。

例如：

```C++
/** This class is designed to be thread safe. */
class SomeClassThreadSafe {}

/** This class is immutable thus thread safe. */
class SomeClassImmutable {}
```

`Concurrent` 通常是用来说明该类是线程安全的前缀。`Synchronized` 是另一个在 Java 中可用的标明类是线程安全的前缀。但是，这通常说明这个类是通过 `synchronized` 机制来保证线程安全的，所以只在 Java 中使用。

另一个常见的场景是同一个**方法**有两种实现：同步阻塞和异步不阻塞的。在这种情况下，通常会命名异常不阻塞的方法为 `{synchronizedMethod}Async`，例如：

```java
public T exec();
public Future<T> execAsync();
```

如果一个异步的方法并没有对应的同步方法，通常不需要加 `Async` 后缀。

在 Go 中，如果一个方法是意图在其它协程中异步执行，不需要加 `Async` 后缀。

### 缓存/惰性

>Cached/Buffered
Lazy
Memoized

名词辨析：

- Cached 表示**获取**的对象会被缓存，保留一段时间，在缓存期间不会重新获取。
- Buffered 与 Cached 同义。
- Lazy 表示这个对象会被在第一次调用时**创建**，之后一直保留
- Memoized 通常表示执行结果会在第一次**计算**后被记忆，之后不会再重复计算

> 注意 Buffered 不应该与 Buffer 混淆。 Buffer 作为名词专指“缓冲区”。
> 注意 Cached 不应该与 Cache 混淆。 Cache 作为名词专指“缓存”。

Cached/Buffered 应该在项目中是**一致**的。
Cached/Lazy/Memoized 取决于对象是被获取的，还是创建的，还是计算获得的。

### 不可变性

>Mutable
Immutable

Mutable 显式地声明一个类是可变的，Immutable 显式地声明一个类是不可变的。
通常情况下，类似于并发安全性，是否可变应该在类文档中说明，而不应该在类名中，显得臃肿。只有当一个类同时有可变/不可变版本时，可以使用 `Class/ImmutableClass`。

## 存储/数据/处理

### 数据类

>Object
Data
Value
Record
Entity
Instance

上面几个都可以用来表示一个表示数据的类。但是这些词是典型的“无意义词汇”，如果把它们从名字中删除，仍然可以表示完整意义，那么应该删掉。

```java
class CarObject {} // Bad
class CarEntity {} // Bad
class CarInstance {} // Bad
class Car {} // Good

class MapKey {}
class MapValue {} // OK. Couldn't be shortened.


class LoggingMetricsData {} // Bad
class LoggingMetricsValue {} // Bad
class LoggingMetricsRecord {} // Bad
class Logging Metrics {} // Good

class DrivingRecord {} // OK. Couldn't be shortened.
```

>Statistics/Stats

表示“统计数据”。 Stats 是公认的可用的 Statistics 的缩写，Java/C++/Go 均可。

### 存储

>Storage / Database / Store / DB
>Cache
Verbs: save/store/put

Storage/Database/Store/DB 都可以作为“存储服务”，即广义上的“数据库”（不是必须是完整的 DBMS）。
其中，在 C++/Go 中 DB 是常见且可接受的。在 Java 中通常使用全称。

项目内应该选择一个术语保持一致。

`save/store/put` 在数据库类中是同义词。同一个项目中应该保持**一致**。

### 数据格式

>Schema
Index
Format
Pattern

名词辨析：

- Schema 借用数据库的概念，指数据的**结构**模式。
- Index 借用数据库的概念，专指数据的**索引**。
- Format/Pattern 通常是泛指的“模式/格式”概念。实际出现时，Format/Pattern 往往和字符串相关，如 Java 使用 Pattern 表示正则表达式。在非公共代码中，Format/Pattern 通常过于宽泛，应该考虑选用更细化的名词。

### 哈希

> Hash/Digest/Fingerprint/Checksum

Hash/Digest 哈希是一种将任何数据映射到一个较小的空间的方法。映射通常被称为**哈希函数(Hash Function)**，映射值通常被称为**摘要(Digest)**。

```java
Hash(Data) = Digest
```

Checksum 出自编码论，可以理解为一种特殊的哈希函数，用来检查文件的**完整性**。换言之，如果一份数据出现了任何变动，Checksum 应该期待会改变。（但是 Checksum 实际上并不要求唯一性，见 Fingerprint）

Fingerprint 类似于 Checksum，但是 Fingerprint 通常更严格，它通常要求最少有 64-bit，使得任何两个文件只要不同，几乎（概率意义上接近 2^-64）不可能有同一份指纹，即**唯一性**。（但是 Fingerprint 的定义不要求密码安全性即 cryptographic）

所以 Checksum 只是作为文件变更校验，而 Fingerprint 可以作为数据的唯一标记。

在命名时，优先使用 Fingerprint/Checksum，或其它概念。当两者均不合适时，回退到更泛化的概念，即 Digest。

### 流式编程

>Stream
>Source/Sink
>Pipe/Piped

流式编程通常有自己的专有词汇表。具体地：

- Stream 表示流式
- Source 表示数据源（输入），Sink 表示 数据汇（输出）。
- 动词词汇表，如 map/reduce/join/filter/iterate/do/window/key/evict/peek/trigger/slide/...

原则是：选择你的团队里最常使用的流式处理系统所使用的词汇表。

### 状态

>State/Status

很讽刺地，很多人认为这两个词有区别，但是他们认为区别的点各不相同。见下文参考文献。笔者倾向于认为它们其实没什么本质区别。

鼓励使用 State 表示状态。因为 HTTP 和 RPC 已经占用了 Status 这个术语，为了避免误解，使用 State 表示自定义状态。

参考：

- https://stackoverflow.com/questions/1162816/naming-conventions-state-versus-status
- https://softwareengineering.stackexchange.com/questions/219351/state-or-status-when-should-a-variable-name-contain-the-word-state-and-w
- 鼓励使用 State: https://google.aip.dev/216

>Num/Count/Size/Length/Capacity

- Num/Count 表示数量，但不强制是某个 collection 的长度。推荐使用 Count。
- Size/Length 表示容器(容器在这里泛指“能容纳多个对象的类型”，不特指标准库的容器。)的**当前**容量。遵循语言惯例，通常使用 Size。
- Capacity 通常表示容器的**最大**容量。

## 方法/动词

动词是句子的精髓。选择精准的动词是代码可读性的关键。
本章对动作做了分类，并且提供了部分备选。如果动词有反义词，它们会被聚合在一个词条中。
本章的词汇有两种：

- 动词
- 以执行一个动作为主的某些行为类，即 -er 模式，如 Producer。 -able 模式，如 Writable 是类似的，因为不再赘述。

### 创建/提供

>Producer/Provider/Supplier/Generator/Constructor/Factory
>Builder.build
>
Verbs:
> create/from/of/with/valueOf/instance/getInstance/newInstance/getFoo/newFoo
> get/peek
> make/generate

创建/提供名词辨析：

1. Producer/Supplier/Provider 同义词，都表示“提供一个对象”。这些提供者可能是惰性的(Lazy)。实例未必由这些提供者创建（虽然通常是）。
    - 它们对应的动词是工厂方法的常见命名，即:
    - create/from/of/with/valueOf/instance/getInstance/newInstance/getFoo/newFoo
    - 推荐在项目中使用同一种命名。推荐使用 of/from，更短。
2. Generator 通常专指某些需要经过计算的、特殊的对象，例如 ID。
    - 对应的动词是 generate，强调全新生成。
3. Constructor 通常是指一个复杂对象的构建器，不是指构造函数。它通常用于比 Builder 更复杂的构建 (Builder 通常不会附带逻辑）。
4. Factory 是专职的工厂类。当工厂方法较为复杂，需要抽出，或者有状态的工厂时使用。
    - 对应上文工厂方法的常见命名。
5. Builder 见 [Builder 建造者模式](https://iwiki.woa.com/pages/viewpage.action?pageId=4008385340)

动词辨析：

1. get vs peek
    - get 是广义的“获取”，在绝大部分场景下适用
    - peek 也是“获取”对象，但是这里强调的是对原对象**无副作用**。在函数式编程中会用来作为不破坏数据流的旁路操作。
2. create vs make vs generate
    - 同义词，表创建。推荐在项目中保持**一致**。

### 消费

>Consumer.accept

消费名词：

- Consumer 是最常见的“消费者”，通常表示某个数据流的终端消费方。
    1. 对应的动词是 accept 或是 consume，遵守所使用消息队列框架的命名风格，否则，项目内保持**一致**。
    2. poll 特指数据是通过轮询(poll)，即 Consumer 通常主动获取消息，而非被推送(push)后处理。

! 注意区分*轮 xun* 中文的歧义：

- poll 翻译为轮询，指一个客户端间断性地向外进行获取数据的**行为**策略。
- round-robin 翻译为轮循，指以单一的方向循环接受信息/资源的**分发**策略。

! 注意轮询是 poll 不是 pull，虽然后者直觉上是**拉取**，但 **poll** 强制间断性地主动地采样/获取数据，是正式的计算机术语。

### 查找

Verbs:
> find/search/query

同义词。推荐在项目中保持**一致**。
具体地，这几个词实际上有细微的不一致。通常情况下它们可能有以下区分：

- find 查询单个结果，search 查询一列符合条件的结果
- find 表示“找到”，即终态，search 表“搜索”，即行为。
- query 表示“查询”，类似于 search，但是暗示可能会有更高的成本。
但是，不要做这种程度的细分，大部分人认为它们是同义词。

参考 https://stackoverflow.com/questions/480811/semantic-difference-between-find-and-search

### 拷贝

Verbs:
> copy/clone

同义词。遵循语言惯例。

Java 使用 clone。 Go/C++ 使用 copy。

### 添加

Verbs:
> add/append/put/insert/push

动词辨析：

- append 专指添加到列表末。
- insert 强调可以插入到列表的任何位置。
- add 是通用的列表添加方案，`add(E)` 等同于 `append`，`add(index, E)` 等同于 `insert`。`addAll` 用于批量添加。
- put 通常用于列表之外的添加场景。如 map, iostream。
- push 仅用于某些数据结构，如栈、队列、vector。

对于自定义的可添加 api，应该贴近底层的标准库的数据结构所使用的动词。作为泛用的添加，使用 add。

### 更新

Verbs:
> set/update/edit

同义词。在代码 API 中使用 set，在 RPC API 中使用 update。

### 删除

Verbs:

> remove/delete/erase/clear/pop

动词辨析：

- remove/delete/erase 是同义词。严格来说，remove 指移除，即暂时从容器中取出放置在一边，delete/erase 指删除，即将对象整个清除。但是在日常编程中不需要做这种区分。通常，代码 API 中使用 remove（或依语言惯例），RPC API 中使用 delete 作为标准方法。
- clear 通常表示 1) 清理列表，等效于 removeAll 2）清理状态，即恢复类到初始化状态。
- pop 只在数据结构中使用，如栈、队列。

### 编排

>Scheduler/Dispatcher/Coordinator/Orchestrator/Delegator

Verb:
> schedule/dispatch/orchestrate

Scheduler/Dispatcher 均借用于操作系统概念。

名词辨析：

1. Scheduler: 通常 Scheduler 用于分发**中长期 Job**。换言之，Scheduler 通常涉及到资源分配。
    - 对应动词为 schedule
2. Dispatcher: 通常只负责接受事件，采用某些固定的策略分发任务，例如 round-robin。不涉及资源分配。
    - 对应动词为 dispatch
3. Coordinator: 通常作为 Scheduler/Dispatcher 的同义词。鉴于其模糊性，推荐使用更细化的 Scheduler/Dispatcher
    - 对应动词为 coordinate
4. Orchstrator：执行比简单的分发，即 scheduler/dispatcher 更复杂的任务/流程编排。通常，这些任务有前后依赖关系，会形成一个有向无环图。
    - 对应动词为 orchestrate。 Orchestrator 的输出通常是工作流，即 Workflow。
5. Delegator: 专指委任。虽然形式类似，但是 Delegator 强调单纯的委任。参见 [Delegattion: 委派模式]。
    - 对应动词为 delegate，但通常不会使用。

### 检查/验证

>Validator/Checker/Verifier

Verb:
> validate/check/verify/assert

Validation/Verification 的明确区分来自于软件测试。

- Validation 通常指对产品符合用户/顾客预期的验证。外部用户会参与。
- Verification 通常指产品合规/符合给定规范。通常是内部流程。

在程序中，不沿用这种区分。通常：

- Validator 用于输入检测
- Verifier 用于运行的不变量检测

具体地：

- check 用于输入校验。 validate 用于复杂的输入校验。
- assert/verify 用于不变量验证，尤其在单元测试中

```java

public void process(String s, ComplicatedObject co) {
  checkNotNull(s); // check
  validateComplicatedObject(co); // validate
}


@Test
public void testProcess() {
  process("ss", co);

  Truth.assertThat(...); // assert
  verifyZeroInvocations(co); // verify
}
```

### 执行/操作

>Task/Job/Runnable
>Executor/Operator/Processor/Runner

Verb:
> exec/execute/do/process/run

名词辨析：

- Runnable 是泛用的“带上文的可执行代码块”。
- Task 粒度比 Job 更细
- Job 通常是耗时更长的任务

但是，推荐不做区分，认为它们都是同义词。使用 Task 或者 Job 作为类名。

名词辨析：
Process/Executor/Operator 是从计算机架构借用的概念。

1. Executor: 常见。通常对应 Job/Task
    - 对应 execute。 exec 是可接受的公认的缩写。
2. Operator: 通常对应某些具体的操作类。更多使用本义，即操作符。
    - 对应 do。
3. Processor：更多在文本文档(work/document processor)、数据处理(data processor) 语境下使用。
    - 对应 process。
4. Runner: 通常对应 Runnable
    - 对应 run

但是，推荐不做区分，认为它们都是同义词。日常编程中，使用 Executor 作为 Job 执行器。

### 开启 vs 关闭

> toggle/switch/enable/disable/turnOn/turnOff/activate/deactivate

二元状态的开启关闭。上述全是同义词。

在项目中保持统一。注意比起 `toggle(bool)` 和 `switch(bool)`，更推荐分离的 `enable/disable`。

### 读取 vs 写入

>Reader/Prefetcher/Fetcher/Downloader/Loader

Verb:
> read/get/fetch/load/retrieve

Noun:
>Writer/Uploader

Verb:
> write/upload

Lifecycle:
> open/close

名词辨析：

1. Reader 通常是从 stdio/文件/其它 Source 中读取。
    - 对应动词 read
2. Fetcher 通常是从远端拉取数据
    - 对应动词  fetch
3. Downloader 类似于 Fetcher，但是通常内容是文件等 blob，而非结构化数据
    - 对应动词 download
4. Prefetcher 强调预热拉取，通常是拉取到缓存中。
    - 对应动词 prefetch 或是简单的 fetch
5. Loader 是泛用词汇，表示广义的“加载”。通常可以表示上述的任何一种。
    - 对应动词 load

- Retrieve 是 Fetch 的同义词。
- 具体地，fetch/load 是有语义的细微差别。但是，不需要做具体的细分。

优先使用 read/fetch/download，当均不合适时，回退到 load。

### 序列化 vs 反序列化

Noun:
>Serializer

Verb:
> serialize/pack/marshal

Noun:
>Deserializer

Verb:
> deserialize/unpack/unmarshal

动词辨析：

- pack 指打包，将数据打包为一个不可拆分的（通常是不透明的）对象
- serialize 指序列化，将数据转换为可以被存储/传输的（通常是二进制）格式。
- marshal 强调意图 -- 将一个对象从程序 A 转移到程序 B 中。

但是，不需要做这个区分。可以认为它们都是**同义词**。按语言惯例使用：

- C++: Serialize
- Java: Serialize
- Go: Marshal
- Python: Pack

注意反序列化是 deserialize, 比 unserialize 更常见。 但 pack -> unpack, marshal -> unmarshal。

- https://en.wikipedia.org/wiki/Marshalling_(computer_science)
- https://en.wikipedia.org/wiki/Serialization

### 转换

>Applier/Converter/Transformer/Mapper

Verb:
> apply/convert/transform/map/to/translate

可以认为它们都是**同义词**。在项目中应该保持一致。
严格来说，Mapper 更多指同一数据的两种形式的双向映射，例如数据库存储和运行时对象。
在 Applier/Converter/Transformer 中，Applier 最为常见，因为源自设计模式。
Mapper 在框架中较常见。

### 匹配

>Filter/Matcher

Verb:
> query/filter/match

可以认为它们都是**同义词**。 在项目中应该保持一致。

### 事件

>Event
>
>Listener/Notifier Verbs: notify
>Observer/Observable Verbs: observe
>Handler Verbs: handle
> Publisher/Subscriber
> Publisher/Consumer

在 [Observer Pattern: 观察者模式] 中已经解释。

- Observer 是正宗的观察者
- Listener/Notifier 通常可以用来作为 Observer/Observable 的同义词。但是 Listener 也可能表示其它含义，如 TraceListener，视框架而定。
- Handler 也是同义词。它与 Listener/Observer 的区别在于，它表示**唯一**的事件处理器。而 Listener/Observer 可能有多个。
- Publisher/Subscriber: 在事件流系统中，表示 **1:N** 广播/订阅。
- Producer/Consumer: 在整个流系统中，专指 **1:1** 生产/消费。

见 https://stackoverflow.com/questions/42471870/publish-subscribe-vs-producer-consumer

### 文本处理

>Regex/Pattern/Template
>
>Pruner/Stripper/Trimmer
>Formatter/Prettier
>Resolver/Parser/Expander
>
>- Verb: compile/parse/resolve/expand
>- Verb: format/split/separate/merge/join

通常，一个程序中有 20% 的代码在处理字符串。所以与文本相关的内容非常多。这里没有列出全部。

“模板”名词解析：

1. Regex 专指正则表达式。另一个常见的缩写是 Regexp。应该与语言保持一致。C++ 使用 Regex。Go 使用 Regexp。
    - 编译使用 compile。 正则本身就是一种 formal language，因此使用 compile 是正统。
    - 匹配对应动词为 expand/match/match
2. Pattern 在 Java 中表示正则表达式。虽然 Pattern 可能通指“模式”，但是通常不在编程中使用。
    - 编译使用 compile
    - 对应动词为 match/split
3. Template 指模板，通常不是正则形式的，而是简单的匹配替换模板，如 HTML 模板。
    - 对应动词为 expand

“修剪”动名词解析：

- Pruner.prune: 指清理掉过时的、不应存在的内容
- Stripper.strip: 指清理掉多余的、过度生长的内容
- Trimmer.trim: 泛指修剪，使其更好看。

但是，Prune/Strip/Trim 在编程中通常认为是**同义词**。它们通常情况下：

- Strip/Trim 指去掉头尾的多余空格
- Prune 可能会进行其它的裁剪

语言可能会为之赋予特殊含义，例如在 Java 11 中，Trim 会清理掉所有的普通空格，而 Strip 会清理掉所有的 Unicode 空格。

- https://stackoverflow.com/questions/51266582/difference-between-string-trim-and-strip-methods-in-java-11

“格式化”动名词解析：

- Formatter.format 是将对象进行格式化。通用名词。
- Prettier.pprint 专指将数据整理为便于人类可读的的输出格式。典型的例子是 Python 的 pprint。

“解析”动名词解析：

- Expander.expand 通常用于 DSL/Schema 解析，专指将某些 DSL **展开**，如变量替换，展开 glob。
- Parser.parse 类似于 parse，但强调将文本进行句法解析，形成格式化的中间层表示。借用了编译器术语。
- Resolver.resolve Resolve 通常指从人类可读的定义（可能有歧义或不精确）向机器可读的定义（精确的、可解析的）的转换。例如，域名 -> ip 的解析，依赖包的版本号的解析（打平）。(!) resolve 不同于 expand/parse 的文本**解析**。这是一个相同中文不同英文的易混淆例子。

### 生命周期

>Lifecycle
>
>Initializer/Finalizer
>

Verb:
> init/setup/prepare
> pause/resume
> start/begin
> end/terminate/stop/halt
> destroy/release/shutdown/teardown

生命周期解析：
一个对象的生命周期，称为 Lifecycle，通常有以下流程：

1. 创建。通常由语言特性支持，不属于生命周期管理范围。
2. 初始化：init。init 是 initialize 的全称，通常用来初始化一个类到可用状态。应该尽量避免创建之外的额外初始化步骤，一个对象应该尽可能在创建后就处于已初始化状态。额外的状态会让这个类更难正确使用。
    - setup/prepare 是 init 的**同义词**。应该在项目内统一，推荐为 init。setUp 通常在测试中使用，用于作为每个测试用例设计的前置步骤。
3. 开始： start/begin。通常用于这个对象正式开始正常工作，即切换到 running 状态。在切换到其它状态之前这个类会一直保持在 running 状态。
    - start/begin 是同义词。通常使用 start 作为动词“开始”，使用 begin 作为列表的头。
4. 暂停： pause。pause 应该使得类暂停运行，从 running 状态切换到 paused 状态。这段时间这个类应该不再工作。
5. 恢复：resume。resume 与 pause 是成对的。 resume 会恢复 paused 到 running 状态。通常，pause/resume 可以无限次随时切换。
6. 停止：stop/end/terminate/halt。停止类运行，与 start 对应。通常情况下，一个类 stop 意味着不会再重新启动。通常情况下，停止状态的类应该拒绝任何请求。
    - stop/end/terminate/halt 是**同义词**。不要做区分处理，在项目中保持一致。
7. 销毁：destroy/release/shutdown/teardown/exit。彻底销毁对象。此后，对象不再处于可用状态。
    - destroy/release/shutdown/teardown 是**近义词**。具体地：
        - destroy 强调销毁对象。
        - release 强调释放资源。
        - teardown 通常与 setup 对应。
        - exit 通常指程序退出。
        - shutdown 是通用“彻底关闭”的动词。当 destroy/release 不合适时，回退到 shutdown。
            - 使用 gracefullyShutdown 表示优雅关闭。这通常意味着是前几个行为的集合：停止服务、释放资源、刷新缓冲区、销毁对象。

### 计算

>Calculator

Verb:
> compute/calculate/calc

使用 Calculator 而非 Computer 表示某个运算的执行器。Computer 虽然也是“计算器”，但是在代码语境下有歧义。

compute/calculate/calc 可以认为是**同义词**。如果是 Calculator，使用 calculate。其它情况下，使用 compute。

### 元数据（配置/环境/...）

>Option/Config/Configuration/Setting/Preference/Property/Parameter/Argument
>Context/Environment
>Info/Metadata/Manifest/Version

配置名词解析：
这个有类似的名词辨析，但是它们在编程时通常认为都是“配置”的同义词。它们还会出现在用户界面，尤其是 Settings/Options/Preferences。

在编程的角度，Option/Config/Configuration 是同义词，均表示配置。惯例使用 `Options` 作为子类定义一个类所需的配置，尤其是作为依赖注入时。

使用 Property 表示单个属性, 而且通常是 k-v 结构。换言之，Option/Config 通常由多个 Properties 组织。只有当 Property 是动态属性时，才定义特殊的 Property 类，否则，在 Option 中定义具体的域表示 Property。

```C++
struct Options {
  int fur_layer_count; // Good
  int fur_layer_count_property; // Bad! Property unnecessary
  
  struct ColorProperty {
    int a;
    int r;
    int g;
    int b;
  } // Bad! Prefer Color.
  ColorProperty color; 
}
```

参数解析：

- Parameter：通常表示在接口处定义的参数
- Argument：指实际传入接口的参数

例如：

```Go
func foo(param string)

foo(arg)
```

https://stackoverflow.com/questions/156767/whats-the-difference-between-an-argument-and-a-parameter

上下文名词辨析：

- Context 指上下文，通常用于在 API 之间传递与一次执行相关的信息。在 RPC 处理中非常常见，例如 https://pkg.go.dev/context。
- Environment 指环境。这个名词从系统环境变量而来。通常，这表示在程序启动后保持稳定的环境数据，不随所执行的内容（如 rpc 请求）变化而变化。

元数据辨析：

- Info 泛指**信息**。而元数据相当于特定的“关于数据”的信息。
- Metadata 标准用语，专指**元数据**。避免使用 Info 代表元数据。
- Manifest 专指**文件清单**，描述一个模块中的文件/功能/其它组成结构的**列表**。Manifest 来自于货运术语，Ship Manifest 用以列出所有的船员和船队所有的船只。
- Version 专指程序的**版本元数据**，例如 `TrpcVersion`。如果一个类专指版本，使用 Version 是最精确合适的。

### 可观测性

Monitor/Recorder (metrics)/Counter/Reporter/Logger/Profiler/Tracer

### 过载保护

Retrier/Backoff/Timeout/CircuitBreaker/Throttler/RateLimiter

### 杂项

Register/Registry

- Verb: register/deregister

Accumulator/Aggregator
