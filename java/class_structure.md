# Class Structure 类结构

## tl;dr

- 类结构应遵循标准组织顺序：类注释→类声明→静态变量→实例变量→构造器→方法
- 通过最小化访问权限，合理使用访问修饰符
- 方法推荐就近原则组织，重载方法需相邻放置
- 保持代码一致性

## 概述

类结构是 Java 编程中的重要组成部分，良好的类结构不仅影响代码的可读性和可维护性，还直接关系到程序的性能和安全性。根据《Effective Java》和 Java 编程规范，类的成员应该按照特定的顺序和原则进行组织。

## Java 类结构的标准顺序

1. 类和接口文档注释
2. 类或接口声明
3. 类（静态）变量
4. 实例变量
5. 构造函数
6. 方法

在每个类别中，成员应该按照访问修饰符的顺序排列：

- `public` → `protected` → `package-private` → `private`

### 反例：混乱的类结构

```java
// 反例：成员顺序混乱
public class BadUserService {

    // 问题：私有方法在开头
    private void validateUser(User user) {
        // 验证逻辑
    }

    // 问题：实例变量在方法后
    private UserRepository userRepository;

    // 问题：静态变量位置不当
    private static final String DEFAULT_ROLE = "USER";

    // 问题：构造函数位置不当
    public BadUserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public User createUser(String name, String email) {
        User user = new User(name, email);
        validateUser(user);
        return userRepository.save(user);
    }

    public static String getDefaultRole() {
        return DEFAULT_ROLE;
    }
}
```

### 正例：良好的类结构

```java
// 正例：遵循标准顺序
/**
 * 用户服务类，提供用户创建和验证等功能
 * @see UserRepository
 * @see EmailService
 */
public class GoodUserService {

    // 1. 静态变量
    public static final String DEFAULT_ROLE = "USER";
    private static final Logger logger = LoggerFactory.getLogger(GoodUserService.class);

    // 2. 实例变量
    private final UserRepository userRepository;
    private final EmailService emailService;

    // 3. 构造函数
    public GoodUserService(UserRepository userRepository, EmailService emailService) {
        this.userRepository = userRepository;
        this.emailService = emailService;
    }

    // 4. 公共方法
    public User createUser(String name, String email) {
        User user = new User(name, email);
        validateUser(user);
        User savedUser = userRepository.save(user);
        emailService.sendWelcomeEmail(savedUser.getEmail());
        return savedUser;
    }

    public static String getDefaultRole() {
        return DEFAULT_ROLE;
    }

    // 5. 私有方法
    private void validateUser(User user) {
        if (user == null) {
            throw new IllegalArgumentException("用户不能为空");
        }
    }
}
```

## 方法组织策略

### 1. 就近原则（推荐）

该原则强调将私有方法紧邻调用它的公共方法放置，形成功能单元的高度内聚。这种布局符合人类阅读代码的自然逻辑：当阅读一个公共方法时，其依赖的私有辅助方法立即可见，无需跳转查找，能显著降低认知负担，提升代码可读性。

```java
public class OrderService {

    public Order createOrder(Long userId, List<OrderItem> items) {
        validateUserId(userId);
        validateOrderItems(items);

        Order order = new Order(userId);
        calculateTotal(order, items);
        return orderRepository.save(order);
    }

    // 私有方法就近放置
    private void validateUserId(Long userId) {
        if (userId == null || userId <= 0) {
            throw new IllegalArgumentException("用户ID无效");
        }
    }

    private void validateOrderItems(List<OrderItem> items) {
        if (items == null || items.isEmpty()) {
            throw new IllegalArgumentException("订单项不能为空");
        }
    }

    private void calculateTotal(Order order, List<OrderItem> items) {
        BigDecimal total = items.stream()
            .map(item -> item.getPrice().multiply(BigDecimal.valueOf(item.getQuantity())))
            .reduce(BigDecimal.ZERO, BigDecimal::add);
        order.setTotal(total);
    }
}
```

### 2. 公开-私有原则

公共方法前置形成类的外部契约，私有方法后置封装实现细节。这种分离结构明确了API边界，使调用者只需关注公共方法。适用于服务类等需要清晰接口定义的场景。

```java
public class PaymentService {

    // 所有公共方法
    public PaymentResult processPayment(PaymentRequest request) {
        validateRequest(request);
        return executePayment(request);
    }

    public PaymentStatus getPaymentStatus(String paymentId) {
        return paymentRepository.findById(paymentId);
    }

    // 所有私有方法
    private void validateRequest(PaymentRequest request) {
        if (request == null || request.getAmount().compareTo(BigDecimal.ZERO) <= 0) {
            throw new IllegalArgumentException("支付请求无效");
        }
    }

    private PaymentResult executePayment(PaymentRequest request) {
        // 执行支付逻辑
        return new PaymentResult(true, "支付成功");
    }
}
```

## 特殊情况处理

### 1. 内部类和枚举
内部类和枚举应置于类末尾，这是平衡主类结构清晰度与关联类型可见性的最佳实践。通过将嵌套类型后置，既保持了主类核心逻辑的连贯性，又确保了相关类型在需要时可被快速定位。

```java
public class DocumentProcessor {

    private static final int MAX_FILE_SIZE = 10 * 1024 * 1024;
    private final FileValidator fileValidator;

    public DocumentProcessor(FileValidator fileValidator) {
        this.fileValidator = fileValidator;
    }

    public ProcessResult processDocument(File file, DocumentType type) {
        if (!fileValidator.isValid(file)) {
            return ProcessResult.failure("文件验证失败");
        }
        return createHandler(type).process(file);
    }

    private DocumentHandler createHandler(DocumentType type) {
        switch (type) {
            case PDF: return new PdfHandler();
            case WORD: return new WordHandler();
            default: throw new UnsupportedOperationException("不支持的文档类型");
        }
    }

    // 内部枚举放在类末尾
    public enum DocumentType {
        PDF, WORD
    }

    // 内部类放在类末尾
    public static class ProcessResult {
        private final boolean success;
        private final String message;

        private ProcessResult(boolean success, String message) {
            this.success = success;
            this.message = message;
        }

        public static ProcessResult success(String message) {
            return new ProcessResult(true, message);
        }

        public static ProcessResult failure(String message) {
            return new ProcessResult(false, message);
        }
    }
}
```

### 2. 重载方法组织

重载方法必须遵循"相邻放置"的铁律，形成参数渐进扩展的连续区块。这种组织方式凸显了方法族的多态性，使开发者能一目了然地掌握功能演进路径。变参方法作为重载的特殊形式，应置于最末位，因其本质上是前序方法的超集。

```java
public class MathUtils {

    // 重载方法相邻放置
    public static int add(int a, int b) {
        return a + b;
    }

    public static long add(long a, long b) {
        return a + b;
    }

    public static BigDecimal add(BigDecimal a, BigDecimal b) {
        return a.add(b);
    }

    // 变参方法放最后
    public static int add(int... numbers) {
        return Arrays.stream(numbers).sum();
    }
}
```

## 《Effective Java》最佳实践

### 1. 最小化访问权限

此实践是"信息隐藏"原则的具象化：用最严格的访问修饰符（private→package-private→protected→public）约束成员可见性。私有字段与公开方法结合，既保障了数据封装的安全性，又提供了必要的操作灵活性。

```java
public class BankAccount {
    private final String accountNumber;
    private BigDecimal balance;

    public BankAccount(String accountNumber) {
        this.accountNumber = accountNumber;
        this.balance = BigDecimal.ZERO;
    }

    public void deposit(BigDecimal amount) {
        validateAmount(amount);
        balance = balance.add(amount);
    }

    public boolean withdraw(BigDecimal amount) {
        validateAmount(amount);
        if (balance.compareTo(amount) >= 0) {
            balance = balance.subtract(amount);
            return true;
        }
        return false;
    }

    public BigDecimal getBalance() {
        return balance;
    }

    private void validateAmount(BigDecimal amount) {
        if (amount == null || amount.compareTo(BigDecimal.ZERO) <= 0) {
            throw new IllegalArgumentException("金额必须大于0");
        }
    }
}
```

### 2. 合理使用访问修饰符

合理选择修饰符选择，在"开放扩展"与"封闭修改"间取得平衡。包级访问修饰在拥有一定的可见范围的同时，避免污染全局空间。protected方法配合防御性副本返回，在支持继承的同时防止内部状态泄露。

```java
public class UserManager {
    static final int MAX_USERS = 1000; // 包级私有

    private final List<User> users = new ArrayList<>();

    public void addUser(User user) {
        if (users.size() >= MAX_USERS) {
            throw new IllegalStateException("用户数量已达上限");
        }
        users.add(user);
    }

    protected List<User> getUsers() {
        return new ArrayList<>(users); // 返回副本
    }
}
```

## 参考资源

1. **《Effective Java》第三版** - Joshua Bloch

   - 第 15 条：使类和成员的可访问性最小化
   - 第 16 条：要在公有类而非公有域中使用访问方法
   - 第 17 条：使可变性最小化

2. **《Java 编程规范》** - Oracle 官方文档

   - 类结构组织：https://www.oracle.com/java/technologies/javase/codeconventions-fileorganization.html
   - 命名约定：https://www.oracle.com/java/technologies/javase/codeconventions-namingconventions.html

3. **《Clean Code》** - Robert C. Martin

   - 类组织原则
   - 方法排序策略

## 总结

良好的类结构是编写高质量 Java 代码的基础。遵循标准的类成员组织顺序、合理使用访问修饰符、采用就近原则组织方法，可以显著提高代码的可读性和可维护性。最重要的是在团队和项目中保持一致的编码风格，这比具体采用哪种策略更为重要。
