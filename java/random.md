# Random 随机数

## tl;dr

- **优先使用 `ThreadLocalRandom`**：线程安全、高性能、无需锁竞争
- **安全场景使用 `SecureRandom`**：密码学安全，用于 Token、Key、加密协议
- **避免频繁重新 Seed**：伪随机数无需重复设置种子
- **注意边界问题**：`nextInt(bound)` 生成 [0, bound)，注意差一错误
- **高并发场景**：避免使用单例 `Random`，选择 `ThreadLocalRandom`

## 推荐的随机数生成器：

[ThreadLocalRandom](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/util/concurrent/ThreadLocalRandom.html)

- 优点：使用 ThreadLocal 随机数种子，无需锁、线程安全、性能优、使用简单。
- 适用场景：大多数并发场景下的随机数需求。

[SecureRandom](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/security/SecureRandom.html)

- 优点：密码学安全，满足不可预测要求。
- 适用场景：Token、Key、加密协议等安全需求。

## 使用随机数的常见误区

### 频繁重新 Seed

正常使用无需在每次调用获取随机数前重新 Seed，一次性 Seed 即可。

我们平时使用的大部分随机数是伪随机数，即算术生成随机数。它的原理是通过算术运算，迭代地生成一系列统计上均匀分布的结果，重置随机数种子并没有必要。

### 反例：每次 new Random、频繁重设种子

```java
for (int i = 0; i < 1000; i++) {
    // 反例：每轮都用当前时间重设种子，本质上，这相当于不再使用 rand 生成的随机数，而是使用时间作为随机数
    Random rand = new Random(System.currentTimeMillis());
    int x = rand.nextInt(100);
    // 问题：每次创建新的Random实例，性能差且种子可能重复
}
```

### 正例：复用 ThreadLocalRandom

```java
for (int i = 0; i < 1000; i++) {
    // ThreadLocalRandom 内部维护种子，无需重复创建
    int x = ThreadLocalRandom.current().nextInt(100);
    // 优势：线程安全、高性能、无需锁竞争
}
```

### 不要在高并发下使用单例`Random`

`java.util.Random`在多线程竞争下会有锁竞争（在 Java 8+ 中，不再用`synchronized `，而使用`AtomicLong + CAS`，但仍存在激烈竞争），吞吐量下降。

若非安全随机，优先用 ThreadLocalRandom.current()。

### 反例：在多线程用 java.util.Random

```java
public class Counter {
    private Random rand = new Random(); // 多线程共享，存在竞争

    public void process() {
        // 多线程下会争用内部锁，性能下降
        int x = rand.nextInt(100);
        // 问题：高并发时吞吐量显著下降
    }
}
```

### 正例：使用`ThreadLocalRandom`

```java
public void process() {
    // 每个线程独立的随机数生成器，无锁竞争
    int x = ThreadLocalRandom.current().nextInt(100);
    // 优势：线程安全、高性能、适合高并发场景
}
```

### 差一错误(Off-by-one error)

误用闭区间／开区间边界，导致实际阈值比预期大。

- `nextInt(bound)` 生成的是 [0, bound)
- `nextInt(origin, bound)` 生成的是 [origin, bound)

### 反例：实际概率与预期概率不同

```java
// 预期概率
private static final int THRESHOLD = 80;

public void process() {
    int probability = ThreadLocalRandom.current().nextInt(100); // 生成 [0, 100)
    // 执行概率为 81%，而不是 80%
    if (probability <= THRESHOLD) { // 错误：使用了 <= 导致概率偏高
        // ...
    }
}
```

### 正例：这个场景下须使用 `probability < THRESHOLD`

```java
public void process() {
    int probability = ThreadLocalRandom.current().nextInt(100); // 生成 [0, 100)
    if (probability < THRESHOLD) { // 正确：使用 < 确保概率准确
        // ...
    }
}
```

## 实际应用场景示例

### 游戏开发中的随机数使用

```java
import java.util.concurrent.ThreadLocalRandom;

public class GameRandomExample {

    // 场景1：随机生成敌人属性
    public Enemy generateRandomEnemy() {
        ThreadLocalRandom random = ThreadLocalRandom.current();

        // 随机生命值：50-200
        int health = random.nextInt(50, 201);

        // 随机攻击力：10-50
        int attack = random.nextInt(10, 51);

        // 随机掉落物品概率：10%
        boolean hasDrop = random.nextInt(100) < 10;

        return new Enemy(health, attack, hasDrop);
    }

    // 场景2：随机地图生成
    public void generateRandomMap() {
        ThreadLocalRandom random = ThreadLocalRandom.current();

        for (int x = 0; x < 100; x++) {
            for (int y = 0; y < 100; y++) {
                // 随机地形类型：0-3
                int terrainType = random.nextInt(4);
                setTerrain(x, y, terrainType);
            }
        }
    }
}
```

### 测试数据生成

```java
import java.util.concurrent.ThreadLocalRandom;
import java.util.ArrayList;
import java.util.List;

public class TestDataGenerator {

    // 场景1：生成随机用户数据
    public List<User> generateRandomUsers(int count) {
        List<User> users = new ArrayList<>();
        ThreadLocalRandom random = ThreadLocalRandom.current();

        for (int i = 0; i < count; i++) {
            // 随机年龄：18-65
            int age = random.nextInt(18, 66);

            // 随机姓名长度：3-10
            int nameLength = random.nextInt(3, 11);
            String name = generateRandomName(nameLength);

            // 随机邮箱
            String email = generateRandomEmail();

            users.add(new User(name, age, email));
        }

        return users;
    }

    // 场景2：随机选择测试用例
    public void runRandomTests() {
        List<TestCase> testCases = getAllTestCases();
        ThreadLocalRandom random = ThreadLocalRandom.current();

        // 随机选择20%的测试用例运行
        int runCount = (int) (testCases.size() * 0.2);

        for (int i = 0; i < runCount; i++) {
            int randomIndex = random.nextInt(testCases.size());
            TestCase testCase = testCases.get(randomIndex);
            testCase.run();
        }
    }
}
```

## 扩展阅读

- [正确使用随机数](https://km.woa.com/articles/view/557803)
