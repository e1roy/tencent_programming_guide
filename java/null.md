# Null 空处理

## tl;dr

- 函数需要返回空值时，考虑使用 `java.util.Optional<T>`。
- 类成员、入参使用 `@Nullable` 标明可空。所有的域默认是非空的。

## 问题描述

Java 所有的参数传递和声明都是引用（原始类型除外）。 Java 无法区分从类型区分一个引用是否是空的(Null)。

空引用的危险众所周知。空指针非常容易被忽略检查，一旦被引用，会立刻引起 NullPointerException(NPE)。更不幸的是，这往往只有在线上造成事故时才会被关注。

空引用的发明者，图灵奖得主 Tony Hoare 称空指针为他犯的 [Billion Dollar Mistake](https://en.wikipedia.org/wiki/Tony_Hoare#Apologies_and_retractions):

> I call it my billion-dollar mistake. It was the invention of the null reference in 1965. At that time, I was designing the first comprehensive type system for references in an object oriented language. My goal was to ensure that all use of references should be absolutely safe, with checking performed automatically by the compiler. But I couldn't resist the temptation to put in a null reference, simply because it was so easy to implement. This has led to innumerable errors, vulnerabilities, and system crashes, which have probably caused a billion dollars of pain and damage in the last forty years.

以下3种处理空引用的方法较为常见：

### 1. 约定所有的引用均可为空

例如，对每个函数，分别处理每个入参为空的情况 -- 允许为空或不允许为空。

```java
/**
* 炸鸡 
*
* @param chicken 可以为空，会返回空值
* @param cookware 必须非空
*/
public FriedChicken fry(Chicken chicken, Cookware cookware) {
    if (user.location().isIn("Shanghai")) {
        logger.atFatal().log("做啥梦呢？");
        return null;
    }
    // 假设 chicken 为空合法，静默处理，直接返回空
    if (chicken == null) {
        return null;
    }
    // 假设 cookware 为空不合法，则在真正调用前预检查
    checkNotNull(cookware);
  
    // 开炸
    // ...
}
```

这样做的坏处是所有方法会有冗长的前置检查。而且很容易遗漏。

### 2. 约定只有带有 `@Nullable` 注解的参数是可空的, 否则全是非空的

在这个假设下，我们可以高效炸鸡了：

```java
/** 炸鸡 */
public Optional<FriedChicken> fry(Chicken chicken, Cookware cookware) {
    if (user.location().isIn("Shanghai")) {
        logger.atFatal().log("做啥梦呢？");
        return Optional.empty();
    }
    // 开炸
    // ...
}
```

注意在之前的例子中，虽然 Chicken 是可空的，但是并没有处理而直接返回。因此，更合理的处理方式是在这里直接假设 Chicken 和 Cookware 都需要是非空的，由上层来处理空的逻辑。

这个方案的优点是对 API 使用者的理解成本会更低，也更不容易出错。缺点是声明可能会更冗长 （想象一个 `@Nullable @ResId @UiThread friedCheckenId`）。同时编写代码的开发有额外成本。

不过，最本质的问题是这个方案里注解只是建议性的，并没有强制力。

### 3. 没有任何约定，开发各凭本事

不幸的是，这是最常见（甚至是笔者所见的项目全是如此）的处理方法。通常，在一个项目里没有上述的约定时，所有人对空引用的处理都会有不同的理解；对每一个引用，都会形成不同的处理方式。经常会看见以下场景：

- 同一个函数，有的入参进行了空指针检验，有的没进行。是否检验空指针可能是凭这个入参长得好看与否。
- 有的函数返回了 `Optional<T>`，有的又返回了空指针
- 同一个类的成员，有的是可空的，有的是不可空的
- 标记 `@Nullable` 和未标记 `@Nullable` 的入参都重新被执行空指针判定

## 如何编码

在 Java 代码层面，通常情况下有如下三种可选使用场景：

- 【推荐】函数需要返回空值时，考虑使用 `java.util.Optional<T>`。较现代的编程语言（例如：TypeScript） 的常见用法。
- 【推荐】类成员、入参使用 `@Nullable` 标明可空。即，所有的域默认是非空的。
- 类成员、入参使用 结合使用 `@Nullable` 和 `@NotNull` ，明确哪些是可空的，哪些是不可空的。

在大多数场景下我们一般会尽量避免同时需要标记 可空和非可空 两类情况，优先保持域对象默认非空的。

## 其它注意项

- Optional 自身永远是 Non-Null 的。一个 `@Nullable Optional<T>` 没有任何意义。
- 类似的，所有的容器(Container)都应该是 Non-Null 的。不要让用户必须区分 Null 容器和 Empty 容器。[注]
- [JSR-305](https://jcp.org/en/jsr/detail?id=305)的注解库有多种实现。但是，在一个项目中应该使用统一的注解库。
- 如果 java.util.Optional 尚不可用，可以使用 Guava [Optional](https://guava.dev/releases/19.0/api/docs/com/google/common/base/Optional.html)。

> [注]: 在日常编程中很自然地会试图使用 Null 容器表示特殊含义，例如，将返回 Null 容器表示执行失败，Empty 容器才是执行成功但没有结果。但是，这种处理对调用方而言非常难以理解，更甚者，调用方事实上不太可能分别处理这两种 case。
> 参考 Protobuf repeated field，不存在 unset repeated field。
> 参考 Golang，nil slice 和 empty slice 在实践中做等价处理。

## 推荐方案 ✓✓✓

作为一个静态类型、支持注解的语言，Java 也可以在编译期进行检查，保证 Null Safety。
业界已有成熟的静态检查方案，例如：

- [The Checker Framework](https://checkerframework.org/)
- [uber/NullAway](https://github.com/uber/NullAway)

它们的原理都是类似的： 用户只要在所有可空的入参/函数/类成员前添加 `@Nullable` 注解，这些框架会作为编译期插件进行类型推断，找出可能的 NPE 场景。

但是，这个方案需要用户所有代码严格地遵守这个语义，否则一旦开启后，代码就无法编译。因此，如若启用这个方案，往往伴随着大量的迁移适配工作。



## 扩展阅读

- KM文章 Writing Java the Kotlin way : https://km.woa.com/articles/view/558676