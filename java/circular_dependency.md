# Circular Dependency 循环依赖

## tl;dr

- 循环依赖是模块间相互依赖形成的闭环，应尽量避免
- 主要危害：增加维护难度、编译复杂度、测试困难
- 解决方案：接口解耦、事件驱动、Setter注入、延迟初始化
- 使用ArchUnit等工具进行依赖检测
- 遵循分层架构和依赖注入最佳实践

## 概述

循环依赖是指两个或多个模块、类或包之间相互依赖，形成一个闭环的依赖关系。虽然 Java 在语法上支持循环依赖，但循环依赖通常是代码设计问题的强烈警告信号，预示着：

- **代码结构不清晰**：模块职责划分不明确
- **分层不合理**：违反了分层架构的原则
- **耦合度过高**：增加了代码维护的复杂性
- **测试困难**：难以进行单元测试和模块化测试

## 为什么要避免循环依赖

### 循环依赖的危害

1. **维护困难**：修改一个模块可能影响到整个依赖链
2. **编译复杂**：增加编译时间和复杂度
3. **部署困难**：无法独立部署和升级模块
4. **测试复杂**：难以进行单元测试，必须同时测试多个模块
5. **理解困难**：代码逻辑难以理解和追踪

### 循环依赖的分类

| 依赖类型                 | 严重程度 | 处理建议                         |
| ------------------------ | -------- | -------------------------------- |
| **包内类之间的循环依赖** | 较低     | 通常可以接受，但需要控制复杂度   |
| **包之间的循环依赖**     | 中等     | 需要重构，采用依赖注入等方式解决 |
| **模块之间的循环依赖**   | 高       | 必须避免，违反了模块化设计原则   |

## 存在循环依赖的设计

### 反例 1：包之间的循环依赖

```java
// 包 org.example.user
package org.example.user;

import org.example.order.OrderService;

// 问题：用户服务依赖订单服务
public class UserService {
    private final OrderService orderService;

    public UserService(OrderService orderService) {
        this.orderService = orderService;
    }

    public void updateUserProfile(Long userId, String newEmail) {
        // 更新用户信息...

        // 问题：直接调用订单服务
        orderService.updateOrdersForUser(userId, newEmail);
    }
}
```

```java
// 包 org.example.order
package org.example.order;

import org.example.user.UserService;

// 问题：订单服务依赖用户服务，形成循环依赖
public class OrderService {
    private final UserService userService;

    public OrderService(UserService userService) {
        this.userService = userService;
    }

    public Order createOrder(Long userId, String productId) {
        // 问题：直接调用用户服务
        User user = userService.getUserById(userId);

        if (user == null) {
            throw new IllegalArgumentException("用户不存在");
        }

        return new Order(userId, productId);
    }

    public void updateOrdersForUser(Long userId, String newEmail) {
        // 更新订单逻辑...
    }
}
```

### 反例 2：构造函数循环依赖

```java
// 问题：构造函数循环依赖导致无法创建对象
public class ClassA {
    private final ClassB classB;

    public ClassA(ClassB classB) {
        this.classB = classB;
    }
}

public class ClassB {
    private final ClassA classA;

    public ClassB(ClassA classA) {
        this.classA = classA;
    }
}

// 无法创建对象：ClassA 需要 ClassB，ClassB 需要 ClassA
```

## 解决循环依赖的设计

### 正例 1：使用接口和事件解耦

```java
// 定义领域接口
public interface UserRepository {
    User getUserById(Long userId);
    void updateUser(User user);
}

public interface OrderRepository {
    List<Order> getOrdersByUserId(Long userId);
    void updateOrdersForUser(Long userId, String newEmail);
}

// 定义事件
public class UserProfileUpdatedEvent {
    private final Long userId;
    private final String newEmail;

    public UserProfileUpdatedEvent(Long userId, String newEmail) {
        this.userId = userId;
        this.newEmail = newEmail;
    }

    // getters...
}
```

```java
// 重构后的用户服务 - 只依赖接口
public class UserService {
    private final UserRepository userRepository;
    private final EventPublisher eventPublisher;

    public UserService(UserRepository userRepository, EventPublisher eventPublisher) {
        this.userRepository = userRepository;
        this.eventPublisher = eventPublisher;
    }

    public User getUserById(Long userId) {
        return userRepository.getUserById(userId);
    }

    public void updateUserProfile(Long userId, String newEmail) {
        User user = userRepository.getUserById(userId);
        if (user != null) {
            user.setEmail(newEmail);
            userRepository.updateUser(user);

            // 通过事件通知其他模块
            eventPublisher.publishEvent(new UserProfileUpdatedEvent(userId, newEmail));
        }
    }
}
```

```java
// 重构后的订单服务 - 只依赖接口
public class OrderService {
    private final OrderRepository orderRepository;
    private final UserRepository userRepository;

    public OrderService(OrderRepository orderRepository, UserRepository userRepository) {
        this.orderRepository = orderRepository;
        this.userRepository = userRepository;
    }

    public Order createOrder(Long userId, String productId) {
        User user = userRepository.getUserById(userId);
        if (user == null) {
            throw new IllegalArgumentException("用户不存在");
        }

        return new Order(userId, productId);
    }
}

// 事件处理器 - 监听用户更新事件
@Component
public class OrderEventHandler {
    private final OrderRepository orderRepository;

    public OrderEventHandler(OrderRepository orderRepository) {
        this.orderRepository = orderRepository;
    }

    @EventListener
    public void handleUserProfileUpdated(UserProfileUpdatedEvent event) {
        orderRepository.updateOrdersForUser(event.getUserId(), event.getNewEmail());
    }
}
```

### 正例 2：使用 Setter 注入解决构造函数循环依赖

```java
public class ClassA {
    private ClassB classB;

    public void setClassB(ClassB classB) {
        this.classB = classB;
    }

    public void doSomething() {
        if (classB != null) {
            classB.process();
        }
    }
}

public class ClassB {
    private ClassA classA;

    public void setClassA(ClassA classA) {
        this.classA = classA;
    }

    public void process() {
        if (classA != null) {
            classA.doSomething();
        }
    }
}

// 工厂方法创建相互依赖的对象
public class CircularDependencyFactory {
    public static Pair<ClassA, ClassB> createAAndB() {
        ClassA a = new ClassA();
        ClassB b = new ClassB();

        a.setClassB(b);
        b.setClassA(a);

        return new Pair<>(a, b);
    }
}
```

### 正例 3：使用延迟初始化

```java
public class LazyClassA {
    private final Supplier<ClassB> classBSupplier;

    public LazyClassA(Supplier<ClassB> classBSupplier) {
        this.classBSupplier = classBSupplier;
    }

    public void doSomething() {
        ClassB classB = classBSupplier.get();
        classB.process();
    }
}

public class LazyClassB {
    private final Supplier<ClassA> classASupplier;

    public LazyClassB(Supplier<ClassA> classASupplier) {
        this.classASupplier = classASupplier;
    }

    public void process() {
        ClassA classA = classASupplier.get();
        classA.doSomething();
    }
}
```

## 使用 ArchUnit 检测循环依赖

```java
public class ArchitectureTest {

    @Test
    public void testNoCyclicDependenciesBetweenPackages() {
        JavaClasses importedClasses = new ClassFileImporter()
            .importPackages("org.example");

        SlicesRuleDefinition.slices()
            .matching("org.example.(*)..")
            .should()
            .beFreeOfCycles()
            .check(importedClasses);
    }

    @Test
    public void testLayeredArchitecture() {
        JavaClasses importedClasses = new ClassFileImporter()
            .importPackages("org.example");

        // 控制器层只能依赖服务层
        ArchRuleDefinition.classes()
            .that().resideInAPackage("..controller..")
            .should().onlyDependOnClassesThat()
            .resideInAnyPackage("..service..", "..controller..", "java..")
            .check(importedClasses);

        // 服务层只能依赖仓储层
        ArchRuleDefinition.classes()
            .that().resideInAPackage("..service..")
            .should().onlyDependOnClassesThat()
            .resideInAnyPackage("..repository..", "..service..", "..domain..", "java..")
            .check(importedClasses);
    }

    @Test
    public void testNoDirectDependenciesBetweenModules() {
        JavaClasses importedClasses = new ClassFileImporter()
            .importPackages("org.example");

        // 用户模块不应该直接依赖订单模块
        ArchRuleDefinition.noClasses()
            .that().resideInAPackage("..user..")
            .should().dependOnClassesThat()
            .resideInAPackage("..order..")
            .check(importedClasses);
    }
}
```

## 最佳实践

### 分层架构设计

```java
// 表现层
@RestController
public class UserController {
    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }
}

// 服务层
@Service
public class UserService {
    private final UserRepository userRepository;

    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }
}

// 仓储层
@Repository
public class UserRepositoryImpl implements UserRepository {
    // 数据访问逻辑
}
```

### 事件驱动架构

```java
@Component
public class UserService {
    private final ApplicationEventPublisher eventPublisher;

    public UserService(ApplicationEventPublisher eventPublisher) {
        this.eventPublisher = eventPublisher;
    }

    public void updateUser(User user) {
        // 更新用户...
        eventPublisher.publishEvent(new UserUpdatedEvent(user));
    }
}

@Component
public class OrderService {
    @EventListener
    public void handleUserUpdated(UserUpdatedEvent event) {
        // 更新相关订单...
    }
}
```

### 依赖注入配置

```java
@Configuration
public class ApplicationConfig {

    @Bean
    public UserService userService(UserRepository userRepository, EventPublisher eventPublisher) {
        return new UserService(userRepository, eventPublisher);
    }

    @Bean
    public OrderService orderService(OrderRepository orderRepository, UserRepository userRepository) {
        return new OrderService(orderRepository, userRepository);
    }
}
```

## 参考资源

1. **《Effective Java》第三版** - Joshua Bloch
2. **《Clean Architecture》** - Robert C. Martin
3. **ArchUnit 官方文档**：https://www.archunit.org/
4. **Spring Framework 文档**：https://docs.spring.io/spring-framework/docs/current/reference/html/core.html
5. **设计模式相关**：《设计模式：可复用面向对象软件的基础》

## 总结

循环依赖是软件设计中需要避免的重要问题。通过合理的架构设计、依赖注入、事件驱动等技术手段，可以有效地避免和解决循环依赖问题。使用 ArchUnit 等工具可以帮助我们自动检测和预防循环依赖的产生。
