# Hashing 哈希函数

## tl;dr

- 哈希函数有多个属性影响选择：**效率**、**冲突率**、**密码安全性**、**稳定性**
- 优先使用 `Guava` Hashing 库，根据场景选择合适算法：
  - **性能优先**：Murmur3、GoodFastHash
  - **密码安全**：SHA-256、SHA-512（避免单次MD5、SHA-1）
  - **校验场景**：CRC32、Adler32
- **布隆过滤器**：使用 `BloomFilter` 进行 URL 去重、缓存穿透防护
- **常见错误**：场景选择不当、参数设置错误、忽略稳定性要求

## Hash 函数的属性

### 固定长度输出

- 通常以位（bit）为单位，例如 32-bit、64-bit、128-bit、256-bit 等
- 更长的输出能在同等输入规模下显著降低碰撞概率

### 确定性与可重复性

- 同样输入应始终产生完全相同的哈希值
- 对于校验、缓存、去重等场景至关重要

### 碰撞率/分布均匀性

- 在合理时间内难以找到两个不同的输入
- 均匀性越好，分桶和负载均衡效果越佳

### 速度与效率

- 包括计算速度、内存占用、并行化能力等
- 包括单次哈希的时间成本和每秒可处理的数据量
- 对大文件、流式数据场景尤其关键

### 密码安全性

- 单向性，攻击者在已知哈希值的情况下，几乎不可能逆推出对应的明文
- 为提高破解成本，引入多次迭代或专用慢哈希算法
- 通常结合盐值（Salt）提升安全性

### Avalanche 效应

- 输入数据的微小变化（如一个比特），应引起输出值的显著变化

|            Hash Function             | Bits | Time  | Recommend |                        Notes                        |
|:------------------------------------:| :--: | :---: | :-------: | :-------------------------------------------------: |
|          `Hashing#adler32`           |  32  | 1.00  |    No     |  Checksumming only (trades reliability for speed)   |
|          ` Hashing#crc32  `          |  32  | 1.52  |    No     |                                                     |
|       `Hashing#goodFastHash(32)`     |  32  | 2.73  |    Yes    |             Not stable between VM runs              |
|         `Hashing#murmur3_32`         |  32  | 2.75  |    Yes    |                                                     |
|      `Hashing#goodFastHash(64)`      |  64  | 5.25  |    Yes    |             Not stable between VM runs              |
|        `Hashing#murmur3_128`         | 128  | 5.26  |    Yes    |                                                     |
|     `Hashing#goodFastHash(128)`      | 128  | 5.41  |    Yes    |             Not stable between VM runs              |
|            `Hashing#md5`             | 128  | 6.03  |    No     | Not cryptographically secure or collision-resistant |
|            `Hashing#sha1`            | 160  | 9.78  |    No     |            Not cryptographically secure             |
|     `Hashing#goodFastHash(256)`      | 256  | 10.41 |    Yes    |             Not stable between VM runs              |
|           `Hashing#sha256`           | 256  | 17.58 |    No     |          Probably cryptographically secure          |
|           `Hashing#sha512`           | 512  | 43.78 |    Yes    |                                                     |
|   `Hashing#goodFastHash(int bits)`   |  N   |  n/a  |    Yes    |     Not stable; user configured N-bit HashCodes     |

### 正例

```java
// 正例：正确的哈希函数选择和使用
public class HashDemo {
    public static void main(String[] args) {
        byte[] data = "Hello, Guava!".getBytes(StandardCharsets.UTF_8);

        // 场景1：非加密、速度优先 - 适合哈希表、缓存键
        HashFunction murmur32 = Hashing.murmur3_32(0); // 0 是 seed，分布均匀且快速
        int hash32 = murmur32.hashBytes(data).asInt();
        System.out.printf("Murmur3_32: 0x%08x%n", hash32);

        // 场景2：通用快速哈希 - 自动选择最优实现
        // 根据要求的 bit 长度，自动选最优实现（FarmHash / CityHash）
        HashFunction fastHash = Hashing.goodFastHash(64);
        long fHash = fastHash.hashBytes(data).asLong();
        System.out.printf("GoodFastHash(64): 0x%016x%n", fHash);

        // 场景3：抗哈希洪水攻击 - 需要密码学安全但速度要求高
        HashFunction sip24 = Hashing.sipHash24(0x10, 0x20); // 两个 64-bit key
        long sip = sip24.hashBytes(data).asLong();
        System.out.printf("SipHash24: 0x%016x%n", sip);

        // 场景4：真正的加密哈希 - 用于密码存储、数字签名
        HashFunction sha512 = Hashing.sha512(); // 高安全要求场景
        String hex = sha512.hashBytes(data).toString();
        System.out.println("SHA-512: " + hex);
    }
}
```

### 反例

```java
// 反例：错误的哈希函数选择和使用
import com.google.common.hash.BloomFilter;
import com.google.common.hash.Funnels;
import java.nio.charset.StandardCharsets;

public class BadHashDemo {
    public static void main(String[] args) {
        byte[] data = "Hello, Guava!".getBytes(StandardCharsets.UTF_8);

        // 错误1：在需要密码安全的场景使用MD5
        HashFunction md5 = Hashing.md5(); // MD5已不安全，不应用于密码存储
        String md5Hash = md5.hashBytes(data).toString();
        System.out.println("MD5 (不安全): " + md5Hash);

        // 错误2：在需要稳定性的场景使用goodFastHash
        HashFunction unstable = Hashing.goodFastHash(32); // 不同VM运行结果不同
        int unstableHash = unstable.hashBytes(data).asInt();
        System.out.println("GoodFastHash (不稳定): " + unstableHash);

        // 错误3：在性能敏感场景使用SHA-256
        long start = System.currentTimeMillis();
        HashFunction sha256 = Hashing.sha256(); // SHA-256性能较差，不适合高频场景
        for (int i = 0; i < 100000; i++) {
            sha256.hashBytes(data).toString();
        }
        long end = System.currentTimeMillis();
        System.out.println("SHA-256 10万次耗时: " + (end - start) + "ms");

        // 错误4：布隆过滤器参数设置不当
        BloomFilter<String> badBloomFilter = BloomFilter.create(
            Funnels.stringFunnel(StandardCharsets.UTF_8),
            1000000,  // 预期元素数量过大
            0.0001    // 误判率过低，会导致内存占用过大
        );
        System.out.println("布隆过滤器内存占用过大: " + badBloomFilter.approximateElementCount());

        // 错误5：在需要精确匹配的场景使用布隆过滤器
        BloomFilter<String> preciseFilter = BloomFilter.create(
            Funnels.stringFunnel(StandardCharsets.UTF_8),
            1000,
            0.01
        );
        preciseFilter.put("exact_match_required");
        // 错误：布隆过滤器可能误判，不适合需要精确匹配的场景
        System.out.println("精确匹配测试: " + preciseFilter.mightContain("exact_match_required"));
    }
}
```

## 适用场景指南

### 不同哈希函数的选择原则

**1. 非加密场景（性能优先）**

- **Murmur3_128**: 通用哈希表、缓存键、分布式系统分片
- **GoodFastHash**: 需要特定位长度的快速哈希
- **SipHash**: 需要抗哈希洪水攻击的场景

**2. 密码安全场景**

- **SHA-256**: 数字签名、证书、密码存储（配合盐值）
- **SHA-512**: 更高安全要求的场景
- **避免**: MD5、SHA-1（已不安全）

**3. 校验和场景**

- **CRC32**: 文件完整性校验、网络传输校验
- **Adler32**: 快速校验（但可靠性较低）

### 正例：实际应用场景示例

```java
// 正例：实际应用场景
public class HashUseCases {

    // 场景1：文件去重
    public static String getFileHash(byte[] fileData) {
        HashFunction hashFunction = Hashing.sha256(); // 需要高碰撞抗性
        return hashFunction.hashBytes(fileData).toString();
    }

    // 场景2：用户ID生成（需要稳定性）
    public static long generateUserId(String email) {
        HashFunction hashFunction = Hashing.murmur3_128(0); // 稳定且快速
        return hashFunction.hashString(email, StandardCharsets.UTF_8).asLong();
    }

    // 场景3：API签名验证
    public static String signApiRequest(String data, String secret) {
        HashFunction hashFunction = Hashing.hmacSha256(secret.getBytes()); // 需要密码安全
        return hashFunction.hashString(data, StandardCharsets.UTF_8).toString();
    }

    // 场景4：布隆过滤器 - 使用Guava的BloomFilter
    public static void bloomFilterExample() {
        // 创建布隆过滤器：预期插入1000个元素，误判率0.01
        BloomFilter<String> bloomFilter = BloomFilter.create(
            Funnels.stringFunnel(StandardCharsets.UTF_8),
            1000,  // 预期元素数量
            0.01   // 误判率
        );

        // 添加元素
        bloomFilter.put("user1@example.com");
        bloomFilter.put("user2@example.com");
        bloomFilter.put("user3@example.com");

        // 检查元素是否存在
        System.out.println("user1@example.com 可能存在: " + bloomFilter.mightContain("user1@example.com"));
        System.out.println("user4@example.com 可能存在: " + bloomFilter.mightContain("user4@example.com"));

        // 获取布隆过滤器的统计信息
        System.out.println("预期误判率: " + bloomFilter.expectedFpp());
    }

}
```

## Guava Hashes

- https://guava.dev/releases/21.0/api/docs/com/google/common/hash/Hashing.html
- https://docs.google.com/spreadsheets/d/1_q2EVcxA2HjcrlVMbaqXwMj31h9M5-Bqj_m8vITOwwk/edit#gid=0
