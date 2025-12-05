# Money 钱

## tl;dr

- 不要使用**浮点类型**存储货币金额。使用 `BigDecimal` 或是整型。

浮点类型的存储格式会导致浮点误差。因此，它无法准确地存储 `0.01` 元。例如，

```java
System.out.println(1.03 - 0.42)
```

返回的结果是 `0.6100000000000001`。

金钱的准确度非常敏感。少 `0.0000000000000001`，误差累计到不可忽略后，都会有人找你拼命。

因此，使用绝对准确的类型，如整型（以最小货币单位为单位，如 1 = 1 分），或使用 `BigDecimal`。

### 反例

```java
// 反例1：简单的减法运算
System.out.println(1.03 - 0.42);
// 输出：0.6100000000000001 （应为0.61）
// 问题：浮点数无法精确表示十进制小数

// 反例2：累计误差
double total = 0.0;
for (int i = 0; i < 10; i++) {
    total += 0.1;
}
System.out.println(total);
// 输出：0.9999999999999999 （应为1.0）
// 问题：循环累加导致误差累积

// 反例3：错误的金额比较
double price = 2.00;
double discount = 1.10;
System.out.println(price - discount == 0.90);
// 输出：false （应为true）
// 问题：浮点数比较结果不可靠
```

### 正例

```java
// 正例1：使用BigDecimal的精确计算
BigDecimal a = new BigDecimal("1.03");  // 使用字符串构造，避免精度问题
BigDecimal b = new BigDecimal("0.42");
System.out.println(a.subtract(b));
// 输出：0.61 （精确）
// 优势：完全精确的十进制运算

// 正例2：BigDecimal的比较
BigDecimal price = new BigDecimal("2.00");
BigDecimal discount = new BigDecimal("1.10");
System.out.println(price.subtract(discount).equals(new BigDecimal("0.90")));
// 输出：true
// 优势：精确的比较结果

// 正例3：以分为单位存储金额
int totalCents = 103; // 1.03元
int costCents = 42;   // 0.42元
int changeCents = totalCents - costCents;
// 优势：整数运算，完全精确，性能更好
```

## BigDecimal 使用注意事项

### 构造方法选择

```java
// 反例：使用double构造BigDecimal
BigDecimal badDecimal = new BigDecimal(1.03);  // 精度已丢失
System.out.println(badDecimal);  // 输出：1.0300000000000000266453525910037569701671600341796875

// 正例：使用字符串构造BigDecimal
BigDecimal goodDecimal = new BigDecimal("1.03");  // 保持精确
System.out.println(goodDecimal);  // 输出：1.03
```

### 运算精度控制

```java
public class MoneyCalculation {

    // 反例：未指定精度导致异常
    public void badDivision() {
        BigDecimal a = new BigDecimal("10.00");
        BigDecimal b = new BigDecimal("3.00");
        BigDecimal result = a.divide(b);  // 抛出ArithmeticException
    }

    // 正例：指定精度和舍入模式
    public void goodDivision() {
        BigDecimal a = new BigDecimal("10.00");
        BigDecimal b = new BigDecimal("3.00");
        // 保留2位小数，四舍五入
        BigDecimal result = a.divide(b, 2, RoundingMode.HALF_UP);
        System.out.println(result);  // 输出：3.33
    }
}
```

### 比较操作

```java
// 反例：使用equals比较（考虑精度）
BigDecimal a = new BigDecimal("1.00");
BigDecimal b = new BigDecimal("1.000");
System.out.println(a.equals(b));  // 输出：false（精度不同）

// 正例：使用compareTo比较（忽略精度）
System.out.println(a.compareTo(b) == 0);  // 输出：true
```

### 使用整型的货币处理

```java
public class MoneyUtils {
    private static final int CENTS_PER_YUAN = 100;

    // 将元转换为分（假设）
    public static long yuanToCents(BigDecimal yuan) {
        return yuan.multiply(new BigDecimal(CENTS_PER_YUAN))
            .setScale(0, RoundingMode.HALF_UP)
            .longValue();
    }

    // 将分转换为元
    public static BigDecimal centsToYuan(long cents) {
        return new BigDecimal(cents)
            .divide(new BigDecimal(CENTS_PER_YUAN), 2, RoundingMode.HALF_UP);
    }

    // 整数运算示例
    public static void integerCalculationExample() {
        // 以分为单位进行运算
        long priceCents = yuanToCents(new BigDecimal("19.99"));  // 1999分
        long discountCents = yuanToCents(new BigDecimal("5.00")); // 500分
        long finalPriceCents = priceCents - discountCents;        // 1499分

        // 转换回元显示
        BigDecimal finalPrice = centsToYuan(finalPriceCents);     // 14.99元
        System.out.println("最终价格: " + finalPrice + "元");
    }
}
```

### 货币格式化工具

```java
import java.math.BigDecimal;
import java.text.DecimalFormat;
import java.text.NumberFormat;
import java.util.Locale;

public class MoneyFormatter {

    // 格式化货币显示
    public static String formatCurrency(BigDecimal amount, Locale locale) {
        NumberFormat formatter = NumberFormat.getCurrencyInstance(locale);
        return formatter.format(amount);
    }

    // 格式化金额（不带货币符号）
    public static String formatAmount(BigDecimal amount) {
        DecimalFormat formatter = new DecimalFormat("#,##0.00");
        return formatter.format(amount);
    }

    // 中文货币格式化
    public static String formatChineseCurrency(BigDecimal amount) {
        return formatAmount(amount) + "元";
    }

    public static void main(String[] args) {
        BigDecimal amount = new BigDecimal("1234.56");

        System.out.println("美式格式: " + formatCurrency(amount, Locale.US));
        System.out.println("中式格式: " + formatCurrency(amount, Locale.CHINA));
        System.out.println("数字格式: " + formatAmount(amount));
        System.out.println("中文格式: " + formatChineseCurrency(amount));
    }
}
```

## 扩展阅读

- Effective Java Item 60 Avoid `float` and `double` if exact answers are required.
