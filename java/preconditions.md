# Preconditions 预检查条件

## tl;dr

- 对公开方法，应该总是对输入做必要的校验，如果校验失败直接报错或抛出异常。
- 如果预检查内容较多，建议采用检查链模式。

## 函数结构： 检验 - 空行 - 逻辑

通常情况下，一个公开方法应该符合以下结构：

```java
public void perform(T param) {
  Objects.requireNonNull(param);
  // 其它更多的检查，如列表非空，数值必须是非负等。
  // 在预检查与正式逻辑之间应该有一个空行。
  
  // 真正的逻辑。从这里开始，任何仅被此公开方法调用的私有辅助方法都可以假设上述的检查已经完成，而无需重复。
  helper(param);
  // ... 其它逻辑
}

private static void helper(T param) {
  // 如果 param 已经在公开方法中被校验过，那么在 private 方法中不必再做校验。
}
```

## 不要采用很多 `if-else` 分支

如果检查条件多于5个，可以设计检查规则类和检查器链。

```java
import java.util.ArrayList;
import java.util.List;

// 定义检查规则接口
interface CheckRule {
    boolean check(String input);
    String errorMessage();
}

// 检查器类
class Checker {
    private List<CheckRule> rules = new ArrayList<>();

    // 向检查器添加检查规则
    public void addRule(CheckRule rule) {
        rules.add(rule);
    }

    // 检查给定字符串是否符合所有规则并返回错误消息列表或成功的字符串
    public String check(String input) {
        ArrayList<String> errorMessages = new ArrayList<>();
        for (CheckRule rule : rules) {
            if (!rule.check(input)) {
                errorMessages.add(rule.errorMessage());
            }
        }

        if (errorMessages.isEmpty()) {
            return "Passed all checks!";
        } else {
            return String.join("\n", errorMessages);
        }
    }
}

// 自定义检查规则实现：长度规则
class LengthRule implements CheckRule {
    private int minLength;

    public LengthRule(int minLength) {
        this.minLength = minLength;
    }

    @Override
    public boolean check(String input) {
        return input != null && input.length() >= minLength;
    }

    @Override
    public String errorMessage() {
        return "Input length must be at least " + minLength;
    }
}

public class Main {
    public static void main(String[] args) {
        // 创建一个检查器
        Checker checker = new Checker();
        // 向检查器添加规则
        checker.addRule(new LengthRule(5));

        // 进行测试
        System.out.println(checker.check("abcd")); // 输出：Input length must be at least 5
        System.out.println(checker.check("abcde")); // 输出：Passed all checks!
    }
}
```

在上述代码示例中，我们定义了一个  `Checker`  类，用于存储并执行各种检查规则。检查规则实现了一个名为  `CheckRule`  的接口，该接口包含一个检查方法和一个错误消息方法。我们为您提供了一个名为  `LengthRule`  的自定义检查规则实现，用于检查输入字符串的长度最低限制。
可以根据需要创建更多实现  `CheckRule`  接口的规则类。

## 快速失败（Fail-Fast）

一个常见的问题是，既然对空对象的调用方法(如 `null.foo()`)总是会抛出 NPE，那为什么要在函数开始前检查呢？

有几个原因：

- 给用户明确的预期，即入参必须满足预检查条件。
- 便于调试。考虑以下**链式调用** 的例子，实际报错信息会具体到行，但是具体问题是哪个对象为空不明确：

```java
foo.bar().foz().it(); // NPE! But which is null?
```

- 另外，如果采用链式调用。默认的规则是对成员方法强制 `return this` 并且在对象的缺省构造函数中采用`super()`初始化。

## 卫语句

常见方法是使用 卫语句（guard clause） 来处理这类问题，考虑以下例子：

```java
public class OriginalExample {
    public static String getFileContent(File file) {
        String content = "";
        if (file != null && file.exists()) {
            try {
                content = new String(Files.readAllBytes(file.toPath()));
            } catch (IOException e) {
                System.out.println("Error reading file: " + e.getMessage());
            }
        } else {
            System.out.println("File does not exist");
        }
        return content;
    }
}
```

我们可以重构成以下形式：

```java
public class RefactoredExample {
    public static String getFileContent(File file) {
        // 卫语句，检查文件是否存在
        if (file == null || !file.exists()) {
            System.out.println("File does not exist");
            return "";
        }

        // 如果文件存在，则读取内容
        String content = "";
        try {
            content = new String(Files.readAllBytes(file.toPath()));
        } catch (IOException e) {
            System.out.println("Error reading file: " + e.getMessage());
        }
        return content;
    }
}
```

卫语句实际上也是通过关注点分离的方式把参数的合法性和实际的处理逻辑分开来。可以把很多检查的内容放在方法开始处快速失败(Fast-Fail）。让随后的处理逻辑更清晰简单。不会在业务逻辑中混淆很多的检查和判空的值。

## 常用预检查工具

### JDK 内置工具

```java
import java.util.Objects;

public void processUser(String name, Integer age, List<String> tags) {
    // 空值检查
    Objects.requireNonNull(name, "用户名不能为空");
    Objects.requireNonNull(age, "年龄不能为空");
    Objects.requireNonNull(tags, "标签列表不能为空");
    
    // 自定义条件检查
    if (age < 0 || age > 150) {
        throw new IllegalArgumentException("年龄必须在0-150之间");
    }
    
    if (name.trim().isEmpty()) {
        throw new IllegalArgumentException("用户名不能为空字符串");
    }
}
```

### Guava Preconditions

```java
import static com.google.common.base.Preconditions.*;

public void transferMoney(Account from, Account to, BigDecimal amount) {
    checkNotNull(from, "转出账户不能为空");
    checkNotNull(to, "转入账户不能为空");
    checkNotNull(amount, "转账金额不能为空");
    
    checkArgument(amount.compareTo(BigDecimal.ZERO) > 0, 
                  "转账金额必须大于0，当前值: %s", amount);
    checkArgument(!from.equals(to), "不能向同一账户转账");
    
    checkState(from.getBalance().compareTo(amount) >= 0, 
               "账户余额不足，当前余额: %s，转账金额: %s", 
               from.getBalance(), amount);
}
```

### Spring Assert

```java
import org.springframework.util.Assert;

public void createOrder(Customer customer, List<OrderItem> items) {
    Assert.notNull(customer, "客户信息不能为空");
    Assert.notEmpty(items, "订单项不能为空");
    Assert.isTrue(items.stream().allMatch(item -> item.getQuantity() > 0), 
                  "所有订单项数量必须大于0");
}
```

## 预检查模式

### 建造者模式中的预检查

```java
public class User {
    private final String name;
    private final int age;
    private final String email;
    
    private User(Builder builder) {
        this.name = Objects.requireNonNull(builder.name, "姓名不能为空");
        this.age = builder.age;
        this.email = Objects.requireNonNull(builder.email, "邮箱不能为空");
        
        // 复杂验证
        if (age < 0 || age > 150) {
            throw new IllegalArgumentException("年龄必须在0-150之间");
        }
        if (!email.contains("@")) {
            throw new IllegalArgumentException("邮箱格式不正确");
        }
    }
    
    public static class Builder {
        private String name;
        private int age;
        private String email;
        
        public Builder name(String name) {
            this.name = name;
            return this;
        }
        
        public Builder age(int age) {
            this.age = age;
            return this;
        }
        
        public Builder email(String email) {
            this.email = email;
            return this;
        }
        
        public User build() {
            return new User(this);
        }
    }
}
```

### 方法重载中的预检查

```java
public class Calculator {
    public double divide(double dividend, double divisor) {
        checkArgument(divisor != 0.0, "除数不能为0");
        return dividend / divisor;
    }
    
    public double divide(int dividend, int divisor) {
        checkArgument(divisor != 0, "除数不能为0");
        return (double) dividend / divisor;
    }
}
```

## 性能考虑

```java
public class PerformanceOptimizedService {
    private static final boolean ENABLE_PRECONDITIONS = 
        Boolean.parseBoolean(System.getProperty("enable.preconditions", "true"));
    
    public void processLargeDataset(List<Data> dataset) {
        // 在生产环境可以通过系统属性控制是否启用预检查
        if (ENABLE_PRECONDITIONS) {
            Objects.requireNonNull(dataset, "数据集不能为空");
            checkArgument(!dataset.isEmpty(), "数据集不能为空");
        }
        
        // 处理逻辑
        dataset.forEach(this::processData);
    }
    
    private void processData(Data data) {
        // 对于内部方法，可以使用断言而不是异常
        assert data != null : "数据不能为空";
        // 处理逻辑
    }
}
```

## 扩展阅读

- Effective Java Item 49: Check parameters for validity
- https://stackoverflow.com/questions/45632920/why-should-one-use-objects-requirenonnull
- [Guava Preconditions](https://github.com/google/guava/wiki/PreconditionsExplained)
