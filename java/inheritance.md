# Inheritance 继承

## tl;dr

- **组合优于继承**。仅在纯 is-a 关系下考虑继承，尽可能不使用继承。
- **使用接口，非必要不使用纯抽象类来继承实现**。
- **如果应该继承，父类方法应该写明如何正确继承的文档；如果不应该继承，显式地采用 final 禁止。**

## 组合优于继承
我们鼓励组合优于继承、面向接口编程而非实现，关注如下场景：

灵活性：
- 继承 会在父类和子类之间创建紧密的耦合。父类的变化可能会影响到所有子类，从而增加了维护和扩展代码的难度。
- 组合 通过组合其他类型的对象来创建复杂类型。它通过接口或契约连接对象，而不是具体的实现，从而实现松耦合。这样可以更容易地改变和替换组件，而不会影响整个系统。

复用性：
- 继承 通过扩展现有类来促进代码复用，但这可能导致脆弱的基类问题，即基类的变化会意外地影响子类。
- 组合 通过对象引用来组合行为和功能，而不是继承它们，从而实现更灵活的复用。这样更容易通过不同方式组合现有的行为来创建新行为。

封装性：
- 继承 可能会通过将父类的内部细节暴露给子类来破坏封装。
- 组合 保持了封装性，因为对象通过定义良好的接口相互作用，而隐藏了它们的内部实现。

假设有一个 Bird 类需要同时具备飞行和行走的行为。
```java
class Bird {
    void fly() {
        // 基础飞行逻辑
    }

    void walk() {
        // 基础行走逻辑
    }
}
```

### 反例1
不满足 is A 语义时，禁止使用继承

考虑一种仿生鸟的场景，他的飞行行为和行走行为即使和鸟类的真实行为基本一样，但仿生鸟不属于鸟，不能使用继承体系。
```java
// 仅因复用实现的目的，不满足继承体系基础原则
class BionicBird extends Bird {
}
```

### 反例2 
优先考虑组合行为，而不是直接使用继承

如果有一种特殊类型的鸟比如驼鸟，虽然也属于鸟，但他没有飞行技能，行走技能也可能与一般鸟不太相同
若使用继承体系，则需继承基类 bird 的实现后完全重写 fly 和 walk , 实际并不复用基类的任类行为。
还有更多其他不同类型的鸟类，有的行走技能不一样，有的飞行技能有差异，整个继承体系的实现行为均不稳定，维护上有更大成本。
```java
class Ostrich extends Bird {
    void fly() {
        // 禁用基类实现，一个特殊的不会飞行的技能
    }
    void walk() {
        // 实现自定义行走逻辑
    }
}

class XXBird extends Bird {
    void fly() {
        // 特殊飞行方式
    }
    void walk() {
        // 自定义行走逻辑
    }
}
```

### 正例
使用组合将行为分离到接口中，并进行组合。
```java
interface Flyable {
    void fly();
}

interface Walkable {
    void walk();
}

class Bird implements Flyable, Walkable {
    private Flyable flyingBehavior;
    private Walkable walkingBehavior;

    public Bird(Flyable flyingBehavior, Walkable walkingBehavior) {
        this.flyingBehavior = flyingBehavior;
        this.walkingBehavior = walkingBehavior;
    }

    public void fly() {
        flyingBehavior.fly();
    }

    public void walk() {
        walkingBehavior.walk();
    }
}

class SimpleFlyingBehavior implements Flyable {
    public void fly() {
        // 简单的飞行逻辑
    }
}

class SimpleWalkingBehavior implements Walkable {
    public void walk() {
        // 简单的行走逻辑
    }
}
class NoneFlyingBehavior implements Flyable {
    public void fly() {
        // 不会飞行逻辑
    }
}
class SpecialFlyingBehavior implements Flyable {
    public void fly() {
        // 特殊的飞行逻辑
    }
}
class SpecialWalkingBehavior implements Walkable {
    public void walk() {
        // 特殊的行走逻辑
    }
}

// 使用示例
Bird bird = new Bird(new SimpleFlyingBehavior(), new SimpleWalkingBehavior());
bird.fly();
bird.walk();
Bird ostrich = new Bird(new NoneFlyingBehavior(), new SpecialWalkingBehavior());
ostrich.walk();
```

## 优先使用接口，尽可能不使用抽象类。

### 反例
抽象类强制子类继承冗余方法

```java
// 反例：抽象类强制子类继承冗余方法
public abstract class AbstractPayment {
    // 支付
    public abstract void processPayment();
    // 上报
    public abstract void reportPayment();
}

public class CreditCardPayment extends AbstractPayment {
    @Override
    public void processPayment() {
         /* 信用卡处理逻辑 */ 
    }

    @Override
    public void reportPayment() {
         /* 信用卡上报逻辑 */ 
    }
}

public class WeChatPayment extends AbstractPayment {
    @Override
    public void processPayment() {
         /* 微信支付处理逻辑 */ 
    }
    // 但WeChatPayment不需要上报功能，却无法移除，只能添加空实现处理
    // 该方法也会对外暴露，对调用者调用时也会造成困惑
    @Override
    public void reportPayment() {
         /* 空 */
    }
```


### 正例
使用接口来分离不同的职责定义，按需要实现接口

```java
public interface IPaymentProcessor {
    // 支付核心方法
    void processPayment(); 
}

public interface IBankReporter {
    // 支付上报，仅银行类支付需要
    void reportPayment();
}

// CreditCardPayment 需要实现支付与上报，因此实现 IPaymentProcessor与IBankReporter 接口
public class CreditCardPayment implements IPaymentProcessor, IBankReporter {
    @Override
    public void processPayment() {
         /* 支付逻辑 */ 
    }

    @Override
    public void reportPayment() {
         /* 上报逻辑 */ 
    }
}

// WeChatPayment 无需进行上报，则不需要实现 IBankReporter
public class WeChatPayment implements IPaymentProcessor {
    @Override
    public void processPayment() { 
        /* 逻辑 */ 
    }
}
```


## 显式控制继承的实现方式

### 使用抽象类和抽象方法明确子类的实现约束
明确声明需要子类实现的抽象方法和可以直接使用的具体方法。

```java
abstract class Animal {
    abstract void makeSound();

    public void eat() {
        System.out.println("Animal eats");
    }
}

class Dog extends Animal {
    @Override
    public void makeSound() {
        System.out.println("Dog barks");
    }
}
```

### 方法重写时应当确认是否应该通过 `super` 调用父类的方法实现，重写时，应该使用 `@Override` 注解，以确保正确性。

```java
class Animal {
    String name;

    public Animal(String name) {
        this.name = name;
    }

    public void makeSound() {
        System.out.println("Animal makes sound");
    }
}

class Dog extends Animal {
    public Dog(String name) {
        // 调用父类的构造方法
        super(name); 
    }
    
    @Override
    public void makeSound() {
        System.out.println("Dog barks");
    }
}
```



### 文档化 并 使用 final 关键字约束类和方法
将类声明为 final，防止该类被继承，将方法声明为 final，防止该方法被重写。

```java
public class SafeHashSet<E> {
    /**
     * 添加单个元素，子类可重写此方法但不可修改计数逻辑。
     * 注意：addAll()方法依赖此方法实现。
     */
    protected boolean add(E e) { 
        /* 基础实现 */ 
    }

    /**
     * 添加集合，子类禁止重写此方法。
     */
    public final boolean addAll(Collection<? extends E> c) {
        // 明确依赖add()方法
        for (E e : c) {
            add(e);
        } 
        return true;
    }
}

// 禁止继承的类
public final class SecurityCriticalClass {
    // 此类涉及安全逻辑，禁止子类化
}
```


## 扩展阅读

- Effective Java Item 18: Favor Composition Over Inheritance
- Effective Java Item 19: Design and Document for inheritance or else prohibit it
- Effective Java Item 20: Prefer inheritance to abstract classes
- Design Patterns: Elements of Reusable Object-Oriented Software
