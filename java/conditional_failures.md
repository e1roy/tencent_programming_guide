# Conditional Failures 条件失败

## tl;dr

- Precondition: 检查调用者的入参是否符合预期。
- Assertion： 检查类自身状态是否出现了不应该出现的错误。
- Verification： 在你的代码处，当对你调用的 API 没有强的信心按你的理解工作时，对 API 的调用结果进行验证。换言之，验证你的**依赖**。
- Test assertion：测试中的断言，确保被测代码遵守它宣称所遵守的规范。
- Impossible-condition： 不可能条件检查，用来进行不可能出错（或者我们假设一定不应该出错）的条件的检查。
- Exceptional result： 异常结果，指这个方法无法给出预期的结果，但是没有代码**犯错**，只是单纯的失败。典型的例子是按行读文件内容，但所给的文件是空的，这与预期返回行内容相悖，但代码本身没问题，这时有两个选择，返回一个默认的空字符串或抛出异常。除非 API 名称和业务有明确指定，否则我们倾向抛出空文件异常。

## 失败种类不在于条件，在于语境

同一个断言条件在系统的不同条件下可能会是不同的条件失败类型。根据语境选择合理的处理方式。

一个完整的例子：

```java
class Car {
      private final Engine engine;
      private int totalDistanceTravelled;
      
      
      public void drive(int distance) {
        checkArgument(distance >= 0); // 1. Precondition
        
        int before = totalDistanceTravelled;
        
        if (!engine.started()) {
            throw new VerifyException("The engine is not working"); // 3. Verification
        }
        engine.run(distance);
        totalDistanceTravelled += distance;
        
        assert totalDistanceTravelled >= before; // 2. Assertion
        if (totalDistanceTravelled < 0) {
            throw new AssertionError("Car invariant violated!"); // 5. Impossible condition
        }
      }
    
    
      public static void main(String[] args) {
          Car car = new Car();
          try {
              car.drive(1000);
          } catch (OutOfMemoryError e) {
                // 6. Exceptional Result.
          }
      }
        
      class CarTest {
          @Test
          public void run() {
             // Setup ...
            
             // Action ...
             Truth.assertThat(car.didRun());  // 4. Test assertion
          }
      }
}
```

## 实际应用指南

### Precondition 示例

```java
public void withdraw(double amount) {
    checkArgument(amount > 0, "提取金额必须大于0");
    checkArgument(amount <= balance, "余额不足");
    // 业务逻辑
}
```

### Assertion 示例

```java
public void processOrder(Order order) {
    // 处理订单逻辑
    
    // 断言：确保内部状态一致性
    assert order.getItems().size() > 0 : "订单不能为空";
    assert order.getTotalAmount() >= 0 : "订单总额不能为负";
}
```

### Verification 示例

```java
public User getUserById(Long id) {
    User user = userRepository.findById(id);
    
    // 验证外部依赖的返回结果
    if (user == null) {
        throw new VerifyException("用户数据库返回了null，用户ID: " + id);
    }
    
    return user;
}
```

### Impossible Condition 示例

```java
public String getStatusName(OrderStatus status) {
    switch (status) {
        case PENDING: return "待处理";
        case COMPLETED: return "已完成";
        case CANCELLED: return "已取消";
        default:
            // 这种情况理论上不应该发生
            throw new AssertionError("未知的订单状态: " + status);
    }
}
```

### Exceptional Result 示例

```java
public String readFirstLine(File file) throws IOException {
    try (BufferedReader reader = Files.newBufferedReader(file.toPath())) {
        String line = reader.readLine();
        if (line == null) {
            throw new IOException("文件为空，无法读取第一行");
        }
        return line;
    }
}
```

## 选择策略

| 失败类型 | 使用场景 | 推荐处理方式 |
|---------|---------|-------------|
| Precondition | 验证调用者输入 | `checkArgument()`, `checkNotNull()` |
| Assertion | 验证内部状态 | `assert` 语句 |
| Verification | 验证外部依赖 | 抛出 `VerifyException` |
| Test Assertion | 单元测试验证 | `assertThat()`, `assertEquals()` |
| Impossible Condition | 理论上不可能的情况 | 抛出 `AssertionError` |
| Exceptional Result | 正常失败情况 | 抛出业务异常或返回 `Optional` |

## 扩展阅读

- https://github.com/google/guava/wiki/ConditionalFailuresExplained
