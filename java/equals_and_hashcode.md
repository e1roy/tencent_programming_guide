# Equals And HashCode 相等和哈希码

## tl;dr

- **如果没有必要（大部分情况下如此），不要重写（override） `Object.equals` 和 `Object.hashCode` 方法。**
- **如果必须要重写，需要保证 `equals` 满足一致性、对称性、反身性、传递性、排空性。**
- **如果必须要重写，需要保证 `hashCode` 满足一致性和对 `equals` 的等价关系。**
- 重写 `equals` 时必须重写 `hashCode`
- 对于纯数据型类，优先使用 `AutoValue` 自动生成 `equals` 和 `hashCode` 的正确实现。JDK 14 后，可以使用 `Record`。

## Equals 的默认行为

`Object.equals` 默认的实现是比较两个对象是否是同一个引用，即：

```java
public boolean equals(Object other) {
  return this == other;
}
```

虽然看上去不是预期的“相等”（即逻辑上的相等），但是在很多情况下，这个实现可以正常工作。考虑以下五个条件，任何一个条件满足时，都不需要 override：

- 该类的每个实例都是唯一的。典型的例子如 `Thread` -- 每个 `Thread` 都是唯一的。
- 没有任何需要比较两个实例是逻辑上相等。例如 `Pattern`，虽然两个正则表达式可能是逻辑上等价的，但现实中并没有什么场景需要比较两个 `Pattern` 是等价的。
- 父类实现了合理的 `equals`，如 `AbstractSet` 的 `equals` 对大部分实类 `Set` 都是通用的。
- 该类可见范围受控，可以确认代码中不会有任何逻辑会调用 `equals` 方法。
- 除了 API，在大部分项目中一个类的被调都是可见并且可控的，我们几乎总是可以确定 `equals` 是否会被调用。

## `Object` 关于实现 `equals` 的约定

[`Object.equals`](https://docs.oracle.com/javase/11/docs/api/java/lang/Object.html#equals) java.lang.Object 里 equals 提到的 Javadoc 描述如下：

> The `equals` method implements an equivalence relation on non-null object references:
>
> - It is _reflexive_: for any non-null reference value `x` , `x.equals(x)` should return `true` .
> - It is _symmetric_: for any non-null reference values `x` and `y` , `x.equals(y)` should return `true` if and only if `y.equals(x)` returns `true` .
> - It is _transitive_: for any non-null reference values `x` , `y` , and `z` , if `x.equals(y)` returns `true` and `y.equals(z)` returns `true` , then `x.equals(z)` should return `true` .
> - It is _consistent_: for any non-null reference values `x` and `y` , multiple invocations of `x.equals(y)` consistently return `true` or consistently return `false` , provided no information used in `equals` comparisons on the objects is modified.
> - For any non-null reference value `x` , `x.equals(null)` should return `false` .

翻译成中文，也就是：

- **反身性**，即 `x.equals(x)` 对任何非空的 `x` 都成立。
  这个性质正常实现都会成立。
- **对称性**，即，如果 `x.equals(y)`，那么 `y.equals(x)`。
  在两个对象的类型不相同，于是使用了不同的 `equals` 方法时可能会出现。
- **传递性**，即如果 `x.equals(y)` 并且 `y.equals(z)`，那么 `x.equals(z)`。

### 反例

```java
class Cap {
    double threshold;
    Cap(double threshold) {
        this.threshold = threshold;
    }
    @Override
    boolean equals(Object other) {
        // Suppose other is Cap:
        return Math.abs(threshold - other.threshold) < 1e-6;
    }
}
```

虽然使用阈值以规避浮点运算的误差是常见操作，但是在 `equals` 中不能这样操作，因为破坏了传递性。考虑以下情况：

```java
Cap(0.0000006).equals(Cap(0));
Cap(-0.0000006).equals(Cap(0));
// But!
Cap(-0.0000006).equals(Cap(0.0000006))
```

- **一致性**，即任何时间调用 `x.equals(y)`，返回的结果都是一致的。
- **排空性**，即对任何非空的 `x`，应该有 `x.equals(null) == false`。

## 实现 `equals`

考虑到如此多的限制，推荐按以下方式实现 `equals` :

1. 首先先判断入参是否是 `equals` 本身所在的对象。
2. 再用 `instanceof` 判断入参的类型是否正确。
3. 转换入参到正确的类型。
4. 对类里的每个显著的、应该比较的成员，比如它们是否相等。
   - 如果是非浮点类型的原始类型，使用 `==` 比较
   - 浮点类型使用 `Float.compare` 和 `Double.compare`
   - 其它对象使用 `Objects.equals(Object, Object)`

当然，更好的办法是使用 [`AutoValue`](https://github.com/google/auto/blob/main/value/userguide/index.md)。它的功能等于 `JDK 14` 后的 `Record`。

### 正例

```java
class Cap {
    double threshold;

    Cap(double threshold) {
        this.threshold = threshold;
    }

    @Override
    public boolean equals(Object o) {
        if (o == null || getClass() != o.getClass()) return false;
        Cap cap = (Cap) o;
        return Double.compare(threshold, cap.threshold) == 0;
    }

    @Override
    public int hashCode() {
        return Objects.hash(threshold);
    }
}
```

### 注意浮点类型的语义相等与逻辑相等

由于浮点误差，浮点类型的比较非常容易出错。遵守以下两条原则：

- **必须使用精确的方式实现 `equals`**。这使得浮点数的 `==/equals` 通常不尊重浮点误差，所以不符合通常意义上的两个数相等。例如，`0.1 + 0.2 != 0.3`。
- 同时，**不应该使用 `==/equals` 比较两个浮点类型是否逻辑上相等**。使用 `epsilon` 阈值的方式比较两个浮点数是逻辑相等的，如： `abs(0.1 + 0.2 - 0.3) < 1e-9`。

### 反例：违反一致性的示例

```java
// 反例：违反一致性
public class InconsistentEquals {
    private Date date;

    public InconsistentEquals(Date date) {
        this.date = date;
    }

    @Override
    public boolean equals(Object o) {
        if (!(o instanceof InconsistentEquals)) return false;
        InconsistentEquals other = (InconsistentEquals) o;
        // 错误：比较会随时间变化
        return this.date.getTime() == other.date.getTime();
    }
}

// 问题演示：如果Date对象包含毫秒信息，可能会因为创建时间不同而返回false
```

### 反例：违反排空性的示例

```java
// 反例：违反排空性
public class NullUnsafeEquals {
    private String name;

    @Override
    public boolean equals(Object o) {
        // 错误：没有检查null
        return name.equals(((NullUnsafeEquals) o).name);
    }
}

// 问题演示：如果传入null会抛出NullPointerException
```

## Object 关于实现 `hashCode` 的约定

标准库中大量的 `Collection` 使用 `hashCode` 和 `equals` 作为键集合类，如 `HashSet` 和 `HashMap`。 为了使它们正确工作，`Object.equals/hashCode` 必须遵守以下规则：

- `hashCode` 必须有**一致性**，即同一个对象，`Object.hashCode()` 必须永远返回同一个值（即使是无意义的值）。
- 如果 `a.equals(b)`，那么必须有 `a.hashCode() == b.hashCode()`。即 `equals` 必须关于 `hashCode` 也是**等价关系**。

## hashCode 实现详解

### 为什么需要 hashCode

hashCode 主要用于哈希表（如 HashMap、HashSet）中的快速查找。如果两个对象相等，它们必须有相同的 hashCode；但如果两个对象有相同的 hashCode，它们不一定相等。

### 正例：hashCode 实现的最佳实践

```java
// 正例：正确的 hashCode 实现
public class Person {
    private final String name;
    private final int age;
    private final Date birthDate;

    public Person(String name, int age, Date birthDate) {
        this.name = name;
        this.age = age;
        this.birthDate = birthDate;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Person person = (Person) o;
        return age == person.age &&
               Objects.equals(name, person.name) &&
               Objects.equals(birthDate, person.birthDate);
    }

    @Override
    public int hashCode() {
        // 使用 Objects.hash() 自动处理 null 值和组合多个字段
        return Objects.hash(name, age, birthDate);
    }
}
```

### 反例：常见 hashCode 实现错误

```java
// 反例1：违反等价关系
public class BadHashCode1 {
    private String name;

    @Override
    public boolean equals(Object o) {
        if (!(o instanceof BadHashCode1)) return false;
        return Objects.equals(name, ((BadHashCode1) o).name);
    }

    @Override
    public int hashCode() {
        return 42; // 错误：所有对象都有相同的 hashCode
    }
}

// 反例2：包含可变字段
public class BadHashCode2 {
    private String name;
    private int count; // 可变字段

    @Override
    public int hashCode() {
        return Objects.hash(name, count); // 错误：包含可变字段
    }

    public void incrementCount() {
        count++; // 改变 count 会影响 hashCode
    }
}

// 反例3：不一致的 hashCode
public class BadHashCode3 {
    private String name;

    @Override
    public int hashCode() {
        // 错误：hashCode 会随 name 变化
        return name != null ? name.hashCode() : 0;
    }

    public void setName(String name) {
        this.name = name; // 改变 name 会影响 hashCode
    }
}
```

### 正例：不可变对象的最佳实践

```java
// 正例：不可变对象的 hashCode 实现
public final class ImmutablePerson {
    private final String name;
    private final int age;
    private final List<String> hobbies;

    public ImmutablePerson(String name, int age, List<String> hobbies) {
        this.name = name;
        this.age = age;
        this.hobbies = Collections.unmodifiableList(new ArrayList<>(hobbies));
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        ImmutablePerson that = (ImmutablePerson) o;
        return age == that.age &&
               Objects.equals(name, that.name) &&
               Objects.equals(hobbies, that.hobbies);
    }

    @Override
    public int hashCode() {
        return Objects.hash(name, age, hobbies);
    }
}
```

## 扩展阅读

- Effective Java Item 10: Obey the general contract when overriding equals
- Effective Java Item 11: Always override hashCode when you override equals
