# Noninstantiability 不可实例化

## tl;dr

- 使用**私有构造函数**保证类不可实例化。

## 对于不允许实例化的类,通过显式的私有化构造函数来保障
例如常见的 `XXXUtils` 这样的类，建议采用私有构造函数避免被实例化造成不当使用。

### 反例
未显示定义构造函数，但默认的构造器仍会支持直接实例化
我们通常不希望实例化 Utility Class，但不幸的是 Java 强制要求所有的方法都声明在类里，如：
```java
class Strings {
  public static String trim() {
    // ...
  }
}
```
如果用户实例化了 `Strings`，是我们未预期的行为，可能会导致意外发生。

### 正例
显式地添加一个私有的构造函数禁止实例化：
```java
class Strings {
  // Non-instantiable.
  private Strings() {}
 
  // ...
}
```
也可以在构造函数中加入不可进入断言，通过断言可以有效阻止类内部进行实例化。如：

```java
class Strings {
  // Non-instantiable.
  private Strings() {
    // 断言添加信息说明来引导开发者正确使用
    throw new AssertionError("Non-instantiable. because reason XXX.");
  }
  // ...
}
```
这通常是可选的。 私有构造方法即可提供足够的不可实例的保证和共识。
