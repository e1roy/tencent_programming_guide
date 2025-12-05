# Exception

## tl;dr

- 对 API 设计者：如无必要，不要抛异常
- 对 API 使用者：永远不要忽略受检异常
- 精确捕获异常类型
- 在可恢复时用受检异常，默认使用非受检异常
- 异常不是控制流工具
- 优先复用标准异常类型

Java 受检异常 (Checked Exception) 本身的存在就是一个广受争议的话题，
但身在 Java 讨论其存在的意义是无意义的，本文主要讨论如何高效地使用异常。

## 精确捕获所有的异常

逐个列出要处理的异常，不要泛泛处理异常。应该避免以下做法：
### 反例
```java
try {
    ....
} catch (Exception e) {
    ....
}
```

建议做法如下,逐个列出要处理的异常：
### 正例
```java
try {
    ....
} catch (TheCheckedException1 e) {
    ....
} catch (TheCheckedException2 e) {
    ....
}
```

或
### 正例
```java
try {
    ....
} catch (TheCheckedException1 | TheCheckedException2 e) {
    ....
} 
```

## 无论是否发生异常都需要执行的代码时，用finally块
当我们使用 `try-catch` 块捕获异常时，可以在 `finally` 块中释放资源。例如，关闭文件、数据库连接或网络连接等。这样可以确保资源在异常发生时也能被正确关闭。
当我们在方法中抛出异常时，可以使用 `finally` 块来确保在异常抛出之前执行必要的清理操作。例如，关闭数据库连接或释放其他资源。
### 正例
```java
FileInputStream fis = null;
try {
    fis = new FileInputStream("file.txt");
    // 读取文件内容
} catch (IOException e) {
    // 处理异常
} finally {
    if (fis != null) {
        try {
            fis.close();
        } catch (IOException e) {
            // 处理关闭文件时的异常
        }
    }
}
```

## 对可恢复的情况使用Checked Exception，默认使用Unchecked Exception

如果期望调用者能够适当地恢复，对于这种情况建议使用Checked Exception，其他情况使用Unchecked Exception。
`RuntimeException` 是Unchecked Exception。用 `RuntimeException` 或他的子类表明存在有编程错误。

通过Throws Checked Exception，强迫调用者在一个 `catch` 子句中处理该异常，或者将它继续向调用方传播出去。因此代表一种潜在的指示：与异常相关联，是调用这个方法的一种可能的结果，以强制用户从这个异常中恢复。
大多数情况下都应该使用Unchecked Exception，因为要处理的场景是非常少的。程序错误、不确定是否恢复的场景更多，这类情况请使用Unchecked Exception。
此外，异常的设计是一种告知责任，而非处理责任。如果抛出异常，则需要在 Javadoc 中对异常进行说明。

## 避免不必要使用Checked Exception

如果过度使用Checked Exception，API将会让使用者非常痛苦。如果调用者无法恢复失败，就应该抛出Unchecked Exception。

## 异常不应该用于控制流程

异常应该只用于异常的情况，永远不应该用于正常的控制流。
不要在 `catch` 块中做业务逻辑运算，因为异常是用来解决程序中不可控的意外情况，而不是做条件分支的，同时异常的处理效率比条件判断方式要慢很多。

## 优先使用标准的异常

常见可重用异常：

| 异常 |使用场合 |
| ------ | ------ |
| `IllegalArgumentException` | 非null的参数值不正确 |
|`IllegalStateException` | 不适合方法调用的对象状态 |
| `NullPointerException` | 在禁止使用null 的情况下参数值为 null |
| `IndexOut0fBoundsException` | 下标参数值越界 |
| `ConcurrentModificationException` | 在禁止并发修改的情况下，检测到对象的并发修改 |
| `UnsupportedOperationException` | 对象不支持用户请求的方法 |

## 区分 `IllegalArgumentException` 与 `IllegalStateException`

如果任何输入都无法使类正常工作，换言之，这个类当前"状态"有问题，应该用 `IllegalStateException`。
- 否则，说明只是当前的输入有问题。应该用 `IllegalArgumentException`。
- 如果输入要求非空，但是用户传入了空对象，虽然是*不合法输入*，应该使用 `NullPointerException`。

## `IndexOutOfBoundsException` 只用于标明数组/Collection 的下标的异常

如果对输入的数值类型要求必须处于某个区间，而实际的入参超出了这个区间，使用 `IllegalArgumentException`。

## 使用 `UnsupportedOperationException` 声明未实现方法

在开发过程中，我们有时会先声明接口，之前再完成实现。与其返回空，这时通常可以使用 `UnsupportedOperationException` 声明该方法尚未实现：
### 正例
```java
interface BookReader {
    List<String> allBooks();
}

class appleBookReader implements BookReader {
    @Override
    List<String> allBooks() {
        // 尚未实现。可先抛出异常：
        throw new UnsupportedOperationException("Unimplemented!");
    }
}
```

## 使用自定义异常的情形
### **提高代码可读性和可维护性**

当标准异常类（如 `IllegalArgumentException`、`NullPointerException` 等）不能准确描述你的业务逻辑中的错误情况时，自定义异常可以使代码更具可读性和可维护性。
### 正例
```java
public class InsufficientFundsException extends Exception {
    public InsufficientFundsException(String message) {
        super(message);
    }
}
```
### **表达特定的业务逻辑错误**

在业务逻辑中，有时需要表达特定的错误情况，这些情况可能无法通过标准异常类来准确描述。自定义异常可以帮助你明确地表达这些错误。
### 正例
```java
public class UserNotFoundException extends Exception {
    public UserNotFoundException(String message) {
        super(message);
    }
}
```
### **分离不同类型的错误**

通过自定义异常，可以将不同类型的错误分离开来，使得异常处理更加精细化。例如，在一个银行系统中，可以有不同的异常类来表示不同的错误情况。
### 正例
```java
public class AccountNotFoundException extends Exception {
    public AccountNotFoundException(String message) {
        super(message);
    }
}

public class InsufficientBalanceException extends Exception {
    public InsufficientBalanceException(String message) {
        super(message);
    }
}
```
### **提供更多的上下文信息**

自定义异常类可以包含更多的上下文信息，帮助调试和日志记录。例如，可以在异常类中添加额外的字段来存储错误的详细信息。
### 正例
```java
public class InvalidTransactionException extends Exception {
    private int transactionId;

    public InvalidTransactionException(String message, int transactionId) {
        super(message);
        this.transactionId = transactionId;
    }

    public int getTransactionId() {
        return transactionId;
    }
}
```

### **避免滥用标准异常**

标准异常类如 RuntimeException、Exception 等，虽然可以用于大多数情况，但滥用这些异常会使得代码难以理解和维护。自定义异常可以帮助你避免这种情况。


## 避免直接重用`Exception`、`RuntimeException`、`Throwable`、`Error`

因为他们是一个方法可能抛出的其它异常的超类，所以你无法可靠地测试这些异常。对待这些类要像对待抽象类一样。

## 不要 catch 后忽略异常

如果必须要忽略时需要做两件事：
1.注释说明。
2.变量命名为 `ignored`

这个建议是显而易见的，应该避免类似的做法：因为空的catch块会使异常达不到应有的目的。
### 反例
```java
try {
    ....
} catch (Exception e) {
}
```

如果选择忽略异常一定要在catch块中包含注释，并且异常的变量名为`ignored`。
### 正例
```java
try {
    // ... 实际逻辑
} catch (IOException ignored) {
    // 详细说明为什么这个异常是可以忽略的
}
```

## 用文档记录方法抛出的异常

利用 Javadoc 的 `@throws` 标签，准确记录抛出每个异常的条件。

如果一个类中许多方法处于相同的原因而抛出同一个异常，则该class的注释中对应有这个异常的说明，是可以接受的。

永远不要直接`throws Exception` 更不要`throws Throwable`
### 正例
```java
/**
 * ...方法注释
 * @throws IOException 如果发生磁盘IO异常或文件IO异常，抛到上层进行统一处理。
 */
public void deal() throws IOException {
}
```

## 异常处理最佳实践

### 异常链和上下文信息
### 正例
```java
public class OrderService {
    public void processOrder(Long orderId) throws OrderProcessingException {
        try {
            Order order = orderRepository.findById(orderId);
            paymentService.processPayment(order);
            inventoryService.updateInventory(order);
        } catch (PaymentException e) {
            // 保留原始异常信息，添加业务上下文
            throw new OrderProcessingException(
                "订单支付失败，订单ID: " + orderId, e);
        } catch (InventoryException e) {
            throw new OrderProcessingException(
                "库存更新失败，订单ID: " + orderId, e);
        }
    }
}
```

### 资源管理和异常安全
### 正例
```java
// ✅ 使用 try-with-resources
public String readFile(String filename) throws IOException {
    try (BufferedReader reader = Files.newBufferedReader(Paths.get(filename))) {
        return reader.lines().collect(Collectors.joining("\n"));
    }
    // 资源会自动关闭，即使发生异常
}

// ✅ 手动资源管理的正确方式
public void processFiles(List<String> filenames) throws IOException {
    List<FileInputStream> streams = new ArrayList<>();
    try {
        for (String filename : filenames) {
            streams.add(new FileInputStream(filename));
        }
        // 处理文件
    } finally {
        // 确保所有资源都被关闭
        for (FileInputStream stream : streams) {
            try {
                if (stream != null) {
                    stream.close();
                }
            } catch (IOException e) {
                // 记录日志，但不抛出异常
                logger.warn("关闭文件流失败", e);
            }
        }
    }
}
```

### 异常转换和抽象层次
### 正例
```java
// 数据访问层
public class UserRepository {
    public User findById(Long id) throws DataAccessException {
        try {
            // 数据库操作
            return jdbcTemplate.queryForObject(sql, User.class, id);
        } catch (SQLException e) {
            // 将底层异常转换为业务层异常
            throw new DataAccessException("查询用户失败，ID: " + id, e);
        }
    }
}

// 业务服务层
public class UserService {
    public UserDto getUser(Long id) throws UserNotFoundException {
        try {
            User user = userRepository.findById(id);
            return convertToDto(user);
        } catch (DataAccessException e) {
            // 转换为更具体的业务异常
            throw new UserNotFoundException("用户不存在，ID: " + id, e);
        }
    }
}
```

### 异常处理策略
### 正例
```java
public class RobustService {

    // 降级策略
    public List<Product> getRecommendations(Long userId) {
        try {
            return recommendationService.getRecommendations(userId);
        } catch (Exception e) {
            logger.error("推荐服务异常，使用默认推荐", e);
            return getDefaultRecommendations();
        }
    }
    
    private List<Product> getDefaultRecommendations() {
        // 返回默认推荐列表
        return Collections.emptyList();
    }
}
```

### 异常监控和日志
### 正例
```java
@Component
public class ExceptionHandler {
    private final Logger logger = LoggerFactory.getLogger(ExceptionHandler.class);
    private final MeterRegistry meterRegistry;
    
    @EventListener
    public void handleException(ExceptionEvent event) {
        Exception exception = event.getException();
        
        // 记录详细日志
        logger.error("异常发生: {}, 用户: {}, 请求: {}", 
                    exception.getMessage(), 
                    event.getUserId(), 
                    event.getRequestInfo(), 
                    exception);
        
        // 监控指标
        meterRegistry.counter("exception.count", 
                             "type", exception.getClass().getSimpleName(),
                             "severity", getSeverity(exception))
                     .increment();
        
        // 告警通知
        if (isCritical(exception)) {
            alertService.sendAlert("严重异常", exception);
        }
    }
    
    private String getSeverity(Exception exception) {
        if (exception instanceof SecurityException) {
            return "CRITICAL";
        } else if (exception instanceof BusinessException) {
            return "WARN";
        } else {
            return "ERROR";
        }
    }
}
```

## 异常性能考虑

### 避免在循环中抛出异常
异常的创建和抛出是昂贵的操作，应避免在高频调用的代码中使用异常。

### 反例
```java
public void processItems(List<String> items) {
    for (String item : items) {
        try {
            processItem(item);
        } catch (ProcessingException e) {
            // 每次循环都可能抛出异常，性能很差
            handleError(item, e);
        }
    }
}
```

### 正例
```java
public void processItems(List<String> items) {
    // 预先验证，避免在循环中抛出异常
    List<String> validItems = items.stream()
        .filter(this::isValidItem)
        .collect(Collectors.toList());
    
    for (String item : validItems) {
        processItem(item); // 不会抛出异常
    }
}
```

### 异常栈轨迹的性能影响
创建异常时会生成栈轨迹，这是性能开销的主要来源。对于某些高频场景，可以考虑重用异常实例。

### 正例
```java
public class ValidationException extends RuntimeException {
    // 对于频繁抛出的异常，可以考虑预创建实例
    public static final ValidationException INVALID_EMAIL = 
        new ValidationException("邮箱格式无效");
    
    private ValidationException(String message) {
        super(message);
    }
    
    // 禁用栈轨迹生成以提高性能（谨慎使用）
    @Override
    public synchronized Throwable fillInStackTrace() {
        return this;
    }
}
```

## 多线程环境下的异常处理

### 线程池中的异常处理
### 正例
```java
@Component
public class AsyncTaskProcessor {
    private final ExecutorService executor = Executors.newFixedThreadPool(10);
    private final Logger logger = LoggerFactory.getLogger(AsyncTaskProcessor.class);
    
    public void processAsync(Task task) {
        executor.submit(() -> {
            try {
                task.execute();
            } catch (Exception e) {
                // 线程池中的异常必须被捕获，否则会被吞掉
                logger.error("异步任务执行失败: {}", task.getId(), e);
                // 可以考虑重试或降级处理
                handleTaskFailure(task, e);
            }
        });
    }
    
    private void handleTaskFailure(Task task, Exception e) {
        // 异常处理逻辑：重试、告警、记录等
    }
}
```

### CompletableFuture异常处理
### 正例
```java
public CompletableFuture<String> processDataAsync(String input) {
    return CompletableFuture
        .supplyAsync(() -> {
            // 可能抛出异常的操作
            return heavyComputation(input);
        })
        .exceptionally(throwable -> {
            logger.error("异步处理失败", throwable);
            return "默认值"; // 提供降级结果
        })
        .whenComplete((result, throwable) -> {
            if (throwable != null) {
                // 记录异常但不影响结果
                logger.warn("处理完成但有异常", throwable);
            }
        });
}
```

## 异常的单元测试

### 测试异常抛出
### 正例
```java
@Test
public void shouldThrowExceptionWhenInvalidInput() {
    // 使用JUnit 5的assertThrows
    IllegalArgumentException exception = assertThrows(
        IllegalArgumentException.class,
        () -> calculator.divide(10, 0)
    );
    
    assertEquals("除数不能为零", exception.getMessage());
}

@Test
public void shouldHandleExceptionGracefully() {
    // 测试异常处理逻辑
    when(externalService.getData()).thenThrow(new ServiceException("服务不可用"));
    
    Result result = businessService.processData();
    
    assertNotNull(result);
    assertTrue(result.isError());
    assertEquals("服务暂时不可用，请稍后重试", result.getMessage());
}
```

### 测试异常链
### 正例
```java
@Test
public void shouldPreserveExceptionChain() {
    RuntimeException rootCause = new RuntimeException("根本原因");
    when(repository.save(any())).thenThrow(rootCause);
    
    BusinessException exception = assertThrows(
        BusinessException.class,
        () -> service.saveData(testData)
    );
    
    assertEquals("保存数据失败", exception.getMessage());
    assertEquals(rootCause, exception.getCause());
}
```

## 异常处理的代码审查要点

### 【必须】检查项
1. **异常不能被忽略**：所有catch块都必须有适当的处理
2. **资源必须释放**：使用try-with-resources或finally块
3. **异常信息完整**：包含足够的上下文信息
4. **异常类型准确**：使用最具体的异常类型

### 【推荐】检查项
1. **异常转换合理**：底层异常转换为业务异常
2. **日志记录完整**：关键异常都有日志记录
3. **降级策略**：对于非关键功能有降级处理
4. **监控告警**：重要异常有监控和告警

### 代码审查清单
```java
// ✅ 好的异常处理示例
public UserProfile getUserProfile(Long userId) throws UserNotFoundException {
    try {
        // 1. 参数验证
        if (userId == null || userId <= 0) {
            throw new IllegalArgumentException("用户ID无效: " + userId);
        }
        
        // 2. 业务逻辑
        User user = userRepository.findById(userId);
        if (user == null) {
            throw new UserNotFoundException("用户不存在: " + userId);
        }
        
        return buildUserProfile(user);
        
    } catch (DataAccessException e) {
        // 3. 异常转换和日志
        logger.error("查询用户资料失败, userId: {}", userId, e);
        throw new UserNotFoundException("获取用户资料失败", e);
    }
}
```

## 异常处理反模式

### 异常吞噬
### 反例
```java
try {
    riskyOperation();
} catch (Exception e) {
    // 什么都不做，异常被吞噬
}
```

### 异常转换丢失信息
### 反例
```java
try {
    databaseOperation();
} catch (SQLException e) {
    // 丢失了原始异常信息
    throw new BusinessException("操作失败");
}
```

### 过度使用受检异常
### 反例
```java
// 强制调用者处理不可恢复的异常
public void validateEmail(String email) throws InvalidEmailException {
    if (!email.contains("@")) {
        throw new InvalidEmailException("邮箱格式无效");
    }
}
```

### 在finally块中抛出异常
### 反例
```java
try {
    return processData();
} finally {
    cleanup(); // 如果cleanup()抛出异常，会覆盖try块的返回值或异常
}
```

## 异常设计原则

1. **异常应该是异常的**：不要用异常处理正常的业务流程
2. **快速失败**：尽早发现和报告错误
3. **异常安全**：确保程序在异常情况下仍能保持一致状态
4. **信息丰富**：异常消息应包含足够的上下文信息
5. **适当的抽象层次**：异常应该与抛出它的抽象层次相匹配

## 异常处理总结

异常处理是Java编程中的重要主题，正确的异常处理能够：
- 提高程序的健壮性和可维护性
- 提供清晰的错误信息和调试线索
- 确保资源的正确释放
- 支持优雅的降级和恢复机制

记住异常处理的核心原则：**异常应该是异常的，快速失败，提供丰富信息，确保程序安全**。

## 扩展阅读

- Effective Java Item 69: Use exceptions only for exceptional conditions
- Effective Java Item 70: Use checked exceptions for recoverable conditions and runtime exceptions for programming errors
- Effective Java Item 71: Avoid unnecessary use of checked exceptions
- Effective Java Item 72: Favor the use of standard exceptions
- Effective Java Item 73: Throw exceptions appropriate to the abstraction
- Effective Java Item 74: Document all exceptions thrown by each method
- Effective Java Item 75: Include failure-capture information in detail messages
- Effective Java Item 76: Strive for failure atomicity
- Effective Java Item 77: Don't ignore exceptions
- [Oracle: Effective Exceptions](https://www.oracle.com/technical-resources/articles/enterprise-architecture/effective-exceptions-part1.html)