# Unit Testing 单元测试

## tl;dr

- 项目内保持测试框架一致
- 单元测试应该是稳定的，需要对外部依赖进行隔离：可以采用接口桩实现(`stub`)或者 `Mock` 的方式。
- 测试行为，不要测试实现。
- 使用 `Mockito` 作为 `Mock` 框架。
- 注意单元测试的可读性，单元测试要提供充分的信息而非噪音。
- 注意重构并整合单元测试的逻辑，避免冗余测试。
- 推荐使用 `TDD` 的方式编写出更容易测试的代码。

## 项目内保持测试框架一致

测试框架是编写测试代码的脚手架，这脚手架本身也是有学习和适应成本的，一般而言，只要不是太早期的测试框架，功能范围都大致能满足需求。
不建议在同一项目中因个人偏好而使用功能相同的不同框架，避免不必要的维护成本，比如 `JMockito` 和 `Mockito` 不要同时在一个项目中混用。

### 反例
混用不同测试框架
```java
import org.junit.Test;                    // JUnit 4
import org.junit.jupiter.api.BeforeEach;  // JUnit 5  
import static org.easymock.EasyMock.*;    // EasyMock
import static org.mockito.Mockito.*;      // Mockito

class MixedFrameworkTest {
    @Test 
    public void testWithMixedFrameworks() {  // JUnit 4风格
        UserRepository repo = createMock(UserRepository.class);  // EasyMock
        UserService service = new UserService(repo, null);
        // 混乱的框架使用增加了维护难度
    }
}
```

### 正例
统一使用 JUnit 5 + Mockito
```java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import static org.mockito.Mockito.*;

class ConsistentFrameworkTest {
    @Test
    void testWithStandardStack() {
        // 使用项目约定的框架组合
        UserRepository repo = mock(UserRepository.class);
        // ... 测试逻辑
    }
}
```


## 单元测试的稳定性

稳定性并不是指测试永远不应该失败，而是指**不应该在不应失败的情况下失败**.即:所测的功能逻辑没发生变化时，其测试也不应该失败了。
这看似是理所当然的，但实际上很多自动化测试的成本就浪费在这上面。

常见稳定性破坏场景包括：
- 依赖外部服务（网络/数据库）
- 未隔离时间敏感操作
- 测试用例之间存在隐式依赖


### 反例
直接调用外部 API 进行测试
```java
@Test
void processOrder_WithRealHttpCall_ShouldFailRandomly() {
    // 反例：直接调用外部 API
    String response = callRealApi("https://api.payment.com/process");
    // 测试结果依赖网络状况和第三方服务可用性
    assertTrue(response.contains("success"));
}

private String callRealApi(String url) {
    // 实际网络调用 - 测试不稳定根源
    return HttpClient.newHttpClient()
                     .send(request, HttpResponse.BodyHandlers.ofString())
                     .body();
}
```

单元测试的稳定性关键在于依赖隔离，而接口实现替换是比直接`Mock` 更符合设计原则的解决方案。
### 正例

```java
// 定义支付网关抽象
public interface PaymentGateway {
    PaymentResult process(PaymentRequest request);
}

// 真实网络实现（生产环境使用）
public class NetworkPaymentGateway implements PaymentGateway {
    @Override
    public PaymentResult process(PaymentRequest request) {
        // 实际网络调用逻辑
        return HttpClient.newHttpClient()
                         .send(createRequest(request), HttpResponse.BodyHandlers.ofString())
                         .body();
    }
}

// 测试桩实现（单元测试使用）
public class StubPaymentGateway implements PaymentGateway {
    private final boolean shouldSucceed;
    
    public StubPaymentGateway(boolean shouldSucceed) {
        this.shouldSucceed = shouldSucceed;
    }
    
    @Override
    public PaymentResult process(PaymentRequest request) {
        return new PaymentResult(shouldSucceed);
    }
}

// 被测服务通过接口依赖
public class OrderService {
    private final PaymentGateway paymentGateway;
    
    // 依赖注入入口
    public OrderService(PaymentGateway paymentGateway) {
        this.paymentGateway = paymentGateway;
    }
    
    public boolean processOrder(Order order) {
        PaymentResult result = paymentGateway.process(order.toPaymentRequest());
        return result.isSuccess();
    }
}

// 测试用例
@Test
void processOrder_WithStubGateway_ShouldSucceed() {
    // Given - 使用桩实现替换
    PaymentGateway stubGateway = new StubPaymentGateway(true);
    
    OrderService service = new OrderService(stubGateway);
    
    // When
    boolean result = service.processOrder(new Order());
    
    // Then
    assertTrue(result);
}
```

## 避免片面追求覆盖率

无意义测试（如测试简单`getter/setter`）的危害：
1. 增加维护成本
2. 产生虚假安全感（高覆盖率≠高可靠性）
3. 阻碍重构（过度绑定实现细节）


### 反例
```java
@Test
void uselessTests_ForCoverageOnly() {
    // 反例：测试简单getter/setter
    User user = new User();
    user.setName("John");
    assertEquals("John", user.getName());  // 无业务价值
    
    // 反例：测试自动生成的方法
    assertNotNull(user.toString());  // 这里 User.toString 方法为Object默认实现
    assertNotNull(user.hashCode());  // 这里 User.hashCode 方法为Object默认实现
    
    // 反例：测试明显正确的逻辑
    List<String> list = new ArrayList<>();
    assertTrue(list.isEmpty());  // 测试语言/框架的基本行为
}
```

### 正例
```java
@Test
void calculateDiscount_ComplexBusinessLogic_ShouldApplyCorrectRules() {
    // 测试有价值的业务逻辑
    DiscountCalculator calculator = new DiscountCalculator();
    
    // 测试各种边界条件
    assertEquals(0.1, calculator.calculate("VIP", 1000, LocalDate.now()));
    assertEquals(0.05, calculator.calculate("NORMAL", 500, LocalDate.now()));
    assertEquals(0.0, calculator.calculate("GUEST", 100, LocalDate.now()));
}
```

## 使用`Mockito`而非`PowerMock`

`Mockito`是`Java`生态的标准`Mock`框架，推荐应优先使用。
`PowerMock`违反单元测试的初衷，通过修改字节码来突破`Java` 的限制，反而可能掩盖代码设计上的问题。
因此，如果强依赖`PowerMock`通常是设计缺陷的信号，建议遗留代码上谨慎使用`PowerMock`，如果有，要做出清理掉的计划：
1. 优先重依赖`PowerMock`代码
2. 新增测试用`Mockito`
3. 制定`PowerMock`清理路线图

### 反例
```java
// 反例：滥用 PowerMock 测试不可测试的代码
@RunWith(PowerMockRunner.class)
@PrepareForTest({StaticUtils.class, FinalClass.class})
public class PowerMockAbuseTest {
    
    @Test
    public void testUntestableCode() {
        // 错误：Mock 静态方法
        mockStatic(StaticUtils.class);
        when(StaticUtils.getConfig()).thenReturn("fake");
        
        // 错误：Mock final 类
        FinalClass tricky = mock(FinalClass.class);
        when(tricky.finalMethod()).thenReturn("hacked");
        
        // 这种测试说明代码设计需要重构
    }
}
```

### 正例
```java
// 使用 Mockito 进行标准依赖注入测试
@Test
void userRegistration_WithMockito_ShouldWork() {
    UserRepository repo = mock(UserRepository.class);
    EmailService email = mock(EmailService.class);
    UserService service = new UserService(repo, email);  // 依赖注入
    
    when(repo.save(any())).thenReturn(true);
    
    boolean result = service.register(new User());
    
    assertTrue(result);
    verify(email).sendWelcome(any());
}
```

## 推荐TDD实践
测试驱动开发是一种软件开发方法，要求开发者在编写功能代码之前先编写测试代码，然后编写最少量的代码使测试通过，最后重构代码以达到设计要求。
测试驱动开发（`TDD`）通过"红-绿-重构"循环，帮助编写可测试、设计良好的代码。

使用TDD的好处：
1. **缺陷大幅提前暴露**：在编码阶段即时发现逻辑错误，将`bug`消灭在萌芽状态。
2. **驱动出更优秀的设计**：先写测试迫使你从调用者角度思考接口，自然产生松耦合、高内聚的代码结构。
3. **构建可靠的安全网**：完整的测试套件为重构和功能扩展提供坚实保障，修改代码时充满信心。
4. **获得即时设计反馈**：如果测试难以编写，通常意味着设计存在问题，`TDD` 成为代码质量的"实时检测仪"。
5. **创建活的文档**：测试用例本身就是最新、最准确的功能规格说明，新人通过阅读测试即可理解系统行为。
6. **提升开发节奏与专注度**：红-绿-重构的小循环保持高效节奏，避免陷入长时间调试的泥潭。
7. **精确界定“完成”标准**：所有测试通过即代表功能完成，消除“差不多做完”的模糊地带，保证交付质量。

更多关于`TDD`实践可以见 iCode Project中TDD文档：[《TDD-测试驱动开发实战》](https://km.woa.com/articles/show/453243?kmref=search&from_page=1&no=1)


## 最佳实践
1. **测试命名规范**：
   `[被测方法]_[测试场景]_[预期结果]`

```java
// 命名规范示例
@Test
void saveUser_WhenEmailInvalid_ThrowsException() {
    // 具体方法实现省略...
}
```

2. **行为验证要点**：
- 验证状态：`assertEquals(expected, actual)`
- 验证行为：`verify(mock, times(n)).method()`
- 验证异常：`assertThrows(Exception.class, ()->{})`

### 被测试的代码
```java
// 业务代码
public class UserService {
    private final UserRepository userRepository;
    private final EmailSender emailSender;

    public UserService(UserRepository userRepository, EmailSender emailSender) {
        this.userRepository = userRepository;
        this.emailSender = emailSender;
    }

    /**
     * 注册新用户并发送欢迎邮件
     * @param user 新用户
     * @return 是否注册成功
     */
    public boolean register(User user) {
        boolean saved = userRepository.save(user);
        if (saved) {
            emailSender.sendWelcomeEmail(user);
        }
        return saved;
    }
}
```

### 测试代码反例
```java
import org.junit.Test;
import static org.junit.Assert.*;
import static org.easymock.EasyMock.*; // 混用EasyMock
import java.net.HttpURLConnection;
import java.net.URL;

public class UserServiceTest {

    @Test
    public void testRegister_WithHttp() throws Exception {
        // bad:违反直接访问外部网络
        URL url = new URL("https://google.com");
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        assertEquals(200, conn.getResponseCode());
    }

    @Test
    public void testRegister_Coverage() {
        // bad:追求覆盖率，测试没意义的代码(toString)
        UserService userService = new UserService(null, null);
        assertNull(userService.toString()); 

        // bad: 重复、无意义测试
        User user = new User();
        user.setName("test");
        user.setName("test"); 
    }

    @Test
    public void shouldTestImplementationDetails() {
        // bad:直接取私有变量，测试实现细节，重构难
        UserRepository repo = createMock(UserRepository.class);
        EmailSender sender = createMock(EmailSender.class);
        UserService service = new UserService(repo, sender);
        assertEquals(repo, TestUtils.getField(service, "userRepository"));
    }
}
```

### 测试代码正例
```java
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

class UserServiceTest {

    private UserRepository userRepository;
    private EmailSender emailSender;
    private UserService userService;

    @BeforeEach
    void setUp() {
        userRepository = mock(UserRepository.class);
        emailSender = mock(EmailSender.class);
        userService = new UserService(userRepository, emailSender);
    }

    @Test
    void register_WhenSaveSuccessful_ShouldSendWelcomeEmailAndReturnTrue() {
        User user = new User("alice@example.com");
        when(userRepository.save(user)).thenReturn(true);

        boolean result = userService.register(user);

        assertTrue(result, "注册成功应该返回true");
        verify(userRepository).save(user);
        verify(emailSender).sendWelcomeEmail(user);
    }

    @Test
    void register_WhenSaveFailed_ShouldNotSendWelcomeEmailAndReturnFalse() {
        User user = new User("bob@example.com");
        when(userRepository.save(user)).thenReturn(false);

        boolean result = userService.register(user);

        assertFalse(result, "注册失败应该返回false");
        verify(userRepository).save(user);
        verify(emailSender, never()).sendWelcomeEmail(any());
    }
}
```



