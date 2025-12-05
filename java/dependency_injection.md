# Dependency Injection 依赖注入

## tl;dr

- **优先使用构造器注入**。构造器注入保证依赖的不可变性和完整性，是最安全的注入方式。
- **避免循环依赖**。通过合理的设计和接口抽象来避免循环依赖问题。
- **遵循依赖倒置原则**。依赖抽象而不是具体实现，提高代码的可测试性和可维护性。
- **合理选择注入方式**。构造器注入 > Setter注入 > 字段注入，根据场景选择合适的方式。
- **不要过度使用**。简单场景下手动创建对象即可，不需要引入复杂的DI框架。

## 为什么需要依赖注入

- 对象不应该创建它所依赖的对象
- 依赖关系应该由外部容器负责注入
- 依赖抽象而不是具体实现

### 传统方式的问题
### 反例
```java
// ❌ 紧耦合的设计
public class OrderService {
    private EmailService emailService;
    private PaymentService paymentService;
    
    public OrderService() {
        // 直接创建依赖对象，紧耦合
        this.emailService = new EmailService();
        this.paymentService = new PaymentService();
    }
    
    public void processOrder(Order order) {
        paymentService.processPayment(order);
        emailService.sendConfirmation(order);
    }
}
```

**问题：**
1. **难以测试**：无法 `mock` 依赖对象进行单元测试
2. **紧耦合**：直接依赖具体实现，难以替换
3. **违反单一职责**：既要处理业务逻辑，又要管理依赖创建
4. **配置困难**：依赖的配置硬编码在代码中

### 使用依赖注入的改进
### 正例
```java
// ✅ 松耦合的设计
public class OrderService {
    private final EmailService emailService;
    private final PaymentService paymentService;
    
    // 构造器注入
    public OrderService(EmailService emailService, PaymentService paymentService) {
        this.emailService = Objects.requireNonNull(emailService);
        this.paymentService = Objects.requireNonNull(paymentService);
    }
    
    public void processOrder(Order order) {
        paymentService.processPayment(order);
        emailService.sendConfirmation(order);
    }
}
```

## 最佳实践

### 优先使用构造器注入

```java
// ✅ 推荐
public class OrderService {
    private final PaymentService paymentService;
    private final InventoryService inventoryService;
    
    public OrderService(PaymentService paymentService, InventoryService inventoryService) {
        this.paymentService = Objects.requireNonNull(paymentService);
        this.inventoryService = Objects.requireNonNull(inventoryService);
    }
}
```

### 依赖接口而不是实现

```java
// ✅ 依赖抽象
public class UserService {
    private final UserRepository userRepository; // 接口
    private final NotificationService notificationService; // 接口
    
    public UserService(UserRepository userRepository, NotificationService notificationService) {
        this.userRepository = userRepository;
        this.notificationService = notificationService;
    }
}
```

### 避免循环依赖

```java
// ❌ 循环依赖
public class OrderService {
    private final CustomerService customerService;
    
    public OrderService(CustomerService customerService) {
        this.customerService = customerService;
    }
}

public class CustomerService {
    private final OrderService orderService; // 循环依赖
    
    public CustomerService(OrderService orderService) {
        this.orderService = orderService;
    }
}

// ✅ 通过事件解耦
public class OrderService {
    private final CustomerService customerService;
    private final EventPublisher eventPublisher;
    
    public OrderService(CustomerService customerService, EventPublisher eventPublisher) {
        this.customerService = customerService;
        this.eventPublisher = eventPublisher;
    }
    
    public void createOrder(Order order) {
        // 处理订单逻辑
        eventPublisher.publish(new OrderCreatedEvent(order));
    }
}

@EventListener
public class CustomerService {
    public void handleOrderCreated(OrderCreatedEvent event) {
        // 处理订单创建后的客户相关逻辑
    }
}
```

### 合理使用作用域

```java
// Spring示例
@Service
@Scope("singleton") // 默认单例
public class UserService {
    // 无状态服务，适合单例
}

@Component
@Scope("prototype") // 每次创建新实例
public class OrderProcessor {
    private Order currentOrder; // 有状态，需要原型作用域
}
```

### 编写可测试的代码

```java
public class UserServiceTest {
    
    @Test
    public void shouldCreateUserSuccessfully() {
        // 使用mock对象
        UserRepository mockRepository = mock(UserRepository.class);
        EmailService mockEmailService = mock(EmailService.class);
        
        UserService userService = new UserService(mockRepository, mockEmailService);
        
        User user = new User("test@example.com", "Test User");
        when(mockRepository.save(any(User.class))).thenReturn(user);
        
        User result = userService.createUser("test@example.com", "Test User");
        
        assertThat(result).isNotNull();
        verify(mockRepository).save(any(User.class));
        verify(mockEmailService).sendWelcomeEmail(user);
    }
}
```

## 常见误区和陷阱

### 过度使用依赖注入

```java
// ❌ 简单场景过度设计
public class Calculator {
    private final MathService mathService;
    
    public Calculator(MathService mathService) {
        this.mathService = mathService;
    }
    
    public int add(int a, int b) {
        return mathService.add(a, b); // 简单加法不需要注入
    }
}

// ✅ 简单场景直接实现
public class Calculator {
    public int add(int a, int b) {
        return a + b;
    }
}
```

### 忽略依赖验证

```java
// ❌ 没有验证依赖
public class UserService {
    private final UserRepository userRepository;
    
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository; // 可能为null
    }
}

// ✅ 验证依赖
public class UserService {
    private final UserRepository userRepository;
    
    public UserService(UserRepository userRepository) {
        this.userRepository = Objects.requireNonNull(userRepository, "userRepository cannot be null");
    }
}
```

### 依赖过多的服务类

```java
// ❌ 依赖过多，违反单一职责原则
public class OrderService {
    private final PaymentService paymentService;
    private final InventoryService inventoryService;
    private final EmailService emailService;
    private final SmsService smsService;
    private final LoggingService loggingService;
    private final AuditService auditService;
    private final NotificationService notificationService;
    // ... 更多依赖
    
    // 构造器参数过多
}

// ✅ 拆分职责，减少依赖
public class OrderService {
    private final PaymentService paymentService;
    private final InventoryService inventoryService;
    private final OrderNotificationService orderNotificationService; // 组合相关服务
    
    public OrderService(PaymentService paymentService, 
                       InventoryService inventoryService,
                       OrderNotificationService orderNotificationService) {
        this.paymentService = paymentService;
        this.inventoryService = inventoryService;
        this.orderNotificationService = orderNotificationService;
    }
}
```

## 注意事项

1. **性能考虑**：使用依赖注入框架会有轻微的性能开销，但通常可以忽略
2. **调试复杂性**：依赖注入框架会增加调试的复杂性，需要理解框架的工作原理
3. **学习成本**：团队需要学习框架的使用方法和最佳实践
4. **过度设计**：不要为了使用依赖注入而使用，简单的场景手动注入即可
5. **循环依赖**：设计时要避免循环依赖，通过事件、回调等方式解耦
6. **测试友好**：确保依赖可以被mock，便于单元测试

## 框架选择指南

### 轻量级场景
- **手动注入**：适合小型项目，依赖关系简单
- **Google Guice**：轻量级，学习成本低，适合中小型项目

### 企业级场景
- **Spring Framework**：功能全面，生态丰富，适合大型企业应用
- **Spring Boot**：约定优于配置，快速开发，适合微服务架构

### 移动端/性能敏感场景
- **Dagger**：编译时依赖注入，性能最优，适合Android开发

## 总结

依赖注入是一种强大的设计模式，能够显著提高代码的可测试性、可维护性和灵活性。关键要点：

1. **优先使用构造器注入**，确保依赖的完整性和不可变性
2. **依赖抽象而不是具体实现**，提高代码的灵活性
3. **避免循环依赖**，通过合理的架构设计解决依赖问题
4. **不要过度设计**，简单场景使用简单方案
5. **重视测试**，确保依赖可以被轻松mock和替换

## 参考资源

1. **《Effective Java》第三版** - Joshua Bloch
   - 第 5 条：优先考虑依赖注入来引用资源
   - 第 51 条：谨慎设计方法签名

2. **JSR-330 规范** - Java 依赖注入标准
   - 官方文档：https://jcp.org/en/jsr/detail?id=330
   - 标准注解：`@Inject, @Named, @Singleton`等

3. **主流框架文档**：
   - Spring Framework：https://spring.io/projects/spring-framework
   - Spring Boot：https://spring.io/projects/spring-boot
   - Google Guice：https://github.com/google/guice
   - Dagger：https://dagger.dev/

4. **设计模式相关**：
   - 《设计模式：可复用面向对象软件的基础》
   - Martin Fowler 的文章：https://martinfowler.com/articles/injection.html
   - 《Clean Architecture》- Robert C. Martin

5. **SOLID 原则**：
   - 依赖倒置原则详解：https://en.wikipedia.org/wiki/Dependency_inversion_principle
   - 《Clean Code》- Robert C. Martin

6. **测试相关**：
   - Mockito 官方文档：https://javadoc.io/doc/org.mockito/mockito-core/latest/org/mockito/Mockito.html
   - 《Growing Object-Oriented Software, Guided by Tests》
