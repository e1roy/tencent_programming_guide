# Time 时间

## tl;dr

- **时间编程非常复杂**：涉及时区、闰秒、夏令时等复杂概念
- **优先使用 `java.time.*`**：JDK 8+ 的最佳选择，JDK 8 之前使用 Joda Time
- **避免旧 API**：不要使用 `java.util.Date` 和 `java.util.Calendar`
- **绝对时间优于民用时间**：便于计算、存储和传输
- **始终明确时区**：不要假设本地时间，优先使用 UTC 存储

## 通用原则

### 时间表示

优先使用**绝对时间（Absolute Time）**而非**民用时间（Civil Time）**。即**优先使用 Unix Time 风格的时间戳**。

绝对时间在以下方面优于民用时间：

- 便于数值计算，例如比较两个时刻的先后关系（time 1 < time 2），或是计算 Instant + Duration。这个计算对人类友好 -- 我们可以轻易地判断出两个时间戳的前后，并不比民用时间更困难。
- 节省空间，例如存储或是传输。通常民用时间的表示至少会需要（Y,M,D,H,M,S,NS,TZ）八个域，相比绝对时间 (S, NS) 的空间多。如果民间时间用字符串表示，则额外空间开销更高。
- 无关时区，系统应该尽可能不依赖时区，如无必要，毋添时区。

当以下条件满足时，适宜使用绝对时间：

- 存储或传输已经发生。过去的时间是已经“被盖章（stamped）” 的，即不再可变，所以使用绝对时间可以保持完整信息（不考虑闰秒）。
- 对未来时刻的精确性要求不高，或者业务允许时区/闰秒等因素造成的微小误差。
- 时区并不重要。

以下场合可能更适合使用民用时间：

- 必须记录时区。
- 记录 1970-01-01 之前的时间，例如记录生日时。
- 记录日期而非时刻。使用该日的零点指示该天虽然可行，但是很 hacky，并且容易受时区变动的影响。更好的办法是使用日期类型，见下。
- 指向未来的某个民用时刻，例如 2025-11-11T13:22:44。这可以不受时区变动的影响。
- 需要记录闰秒事件，即出现 24:00:00 这种时刻。

（换言之，除了这些小众情况，使用绝对时间通常是更好的选择。）

### 如何表示绝对时间

优先使用类型表示时间戳。语言或者传输协议通常都有提供标准的时间类型，如：

- Go: `time.Time`
- Java: `java.time.Instant`
- protobuf: `google.protobuf.Timestamp`

它们通常都是对绝对时间的封装，不会带来显著的额外性能开销。

如果必须使用原始数值类型时（例如兼容历史代码，或有严格的性能要求必须使用），命名中应该包含对应的单位。
为了保证算术安全性，尽量使用有符号类型，而非无符号类型。

安全的选项是使用 int64 表示秒数，用 int32 表示纳秒数，即（seconds: int64, nanoseconds: int32）二元组。

### 如何表示民用时间

永远标明所在时区，不要假设“本地时间”。即使显式设置了本地时区 `TZ="Asia/Shanghai"` 也是如此，因为并非所有依赖的系统都会尊重本地时区 -- 系统可能会自动 fallback 到 UTC 时间。

优先使用 UTC 储存时间，展示和输入时应明确时区。UTC 是大部分系统都默认使用的时间，可以减少很多可能导致的麻烦。即使使用北京时间可能更方便，使用 UTC 时间通常更安全。

对闰秒、时区的介绍可参考[历法复杂性](https://km.woa.com/posts/show/560262?kmref=kb_categories)。

对民用时间、绝对时间的介绍可参考[编程复杂性](https://km.woa.com/group/45812/articles/show/526849?kmref=kb_categories)。

## 测试相关

时钟是测试不稳定的来源。例如如果在一个方法中取 `time.Now()` 并作为实现的一部分，则可能会因为 `Now()` 的不确定性导致测试不稳定。通常情况下，有三种解决方案：

依赖注入 `Clock` 接口。`Clock` 可以只有提供当前时间的接口。这样测试时可以使用 `Fake Clock` 保证确定性的行为。

强制修改系统本地时钟时间。可能需要一些全局性的方法，如：[DateTimeUtils(Joda-Time 2.12.1 API)](https://www.joda.org/joda-time/apidocs/org/joda/time/DateTimeUtils.html)。注意并发执行可能会有问题，另外需要在 tear down 时重置。

基于当前时间测试。这种处理方案通常会选择不再测试时间相关的行为，避免不确定性。例如，基于 Diff 的测试，如 RPC Replay/Diff Testing/... ，通常情况下在结果对比时应该忽略所有的时间戳字段。

## 单调时钟

[编程复杂性](https://km.woa.com/group/45812/articles/show/526849?kmref=kb_categories)前文提及，`Wall Clock` 挂钟时间是不单调的，可能受 NTP/闰秒/settime 等因素影响。所以，应该确保服务器采取了足够的保证时钟同步([Clock synchronization](https://en.wikipedia.org/wiki/Clock_synchronization))的措施，并依据这些措施所提供的 SLA 的假设处理时间。

但是，即使如此，也不应该使用挂钟时间计时。应该总是使用单调时钟进行计时。绝大多数操作系统提供了单调时钟的 API，且大部分语言都支持单调时钟 API。应当单调时钟在对应语言/时间库的 API。

## 时间运算

如前文所述，最重要的一点是区分 Period 与 Duration。这一点在出海业务，需要处理夏令时的时候，尤为重要。

大部分时间库会提供 Duration 的支持，但未必会支持 Period。当后者不被支持时，通常需要回退到本地日期/本地时间后进行计算。
Period 与 Duration 的区别请参阅[编程复杂性](https://km.woa.com/group/45812/articles/show/526849?kmref=kb_categories)。

## 日期表示

优先使用 Date only 的类型。

如果要表示日期，虽然可以使用时刻（如用 Day 00:00:00）模拟，但是如同编程复杂性所解释的，这样做相当于对时间做朴素的算术运算，可能会导致问题。如果有 Date 类型，并且支持 add(days) 操作，相对更安全。

这本质上等同于 Duration/Period 问题。Period 与 Duration 的区别请参阅编程复杂性。

## 选择时间库的不完全检查清单

使用时间库。永远不要进行自己处理时间，尤其**不要自己处理时区**。

前文提及，您永远完整地无法理解时间。在实际开发中，我们通常采取近似的时间处理。您可能需要认真地选择您对时钟和时间系统的要求，抛弃对业务实际上并没有影响的假设（例如可以处理未来时间、具有高精度、需要处理闰秒等），以此选择简化的时间系统。（然后，等出现和时间相关的故障时，再来对照这个系列文章复盘判断哪些假设实际上必须成立）

1.a 和 2 是一个有效的时间库的最低配置，即时刻和时区，以此达成绝对时间与民用时的转化。其它的假设通常都是可选并且由业务形态决定。

以下是 Checklist：

1. 是否包含了足够所需的时间概念的抽象？
   - 是否提供 “Instant” （时刻）类型？
   - 是否支持 “Duration” （时间段）类型？是否区分了 Duration 与 Period (或 Interval)？
   - 是否提供 “Local Date”类型（一个抽象的、与时区无关、与时分秒无关的日期），并支持相关的计算？
   - 是否提供 “Time Of Day”类型（一个与日期无关、与时区无关的挂钟时间），并支持相关的计算？
2. 是否正确地处理了时区？
   - 是否正确地处理了夏令时？
   - 如果民用时间和绝对时间的转换（例如由于夏令时，或时区更新）出现了二义性（Overlap）或不存在的时间（Gap），是如何处理的？
   - 是否可以正确地更新 tzdata？
3. 如何处理闰秒？
4. 是否具有足够的时间精度？
5. 是否支持单调时钟以测量时长？
6. 是否支持星期？
7. 是包含时钟界面，还是仅提供静态的时间提供方法？
8. 是否支持所需的非公历的历法？例如，是否需要支持阴历？

## 实际应用示例

### 反例：使用旧的时间 API

```java
// 反例：使用 java.util.Date 和 Calendar 的问题
import java.util.Date;
import java.util.Calendar;
import java.text.SimpleDateFormat;

public class BadTimeExample {

    // 反例1：Date 的月份从0开始，容易出错
    public void badDateCreation() {
        // 错误：想要创建2023年1月1日，但实际是2023年2月1日
        Date date = new Date(123, 0, 1);  // 年份从1900开始，月份从0开始
        System.out.println(date);  // 输出：Thu Feb 01 00:00:00 CST 2023

        // 问题1：月份从0开始，容易混淆
        // 问题2：年份从1900开始，需要手动计算
        // 问题3：Date 实际上是时间戳，不是日期
    }

    // 反例2：SimpleDateFormat 线程不安全
    public void badDateFormatting() {
        SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");

        // 问题：SimpleDateFormat 不是线程安全的
        // 在多线程环境下可能出现数据竞争和异常
        String formatted = formatter.format(new Date());
        System.out.println(formatted);
    }

    // 反例3：Calendar 的复杂性和性能问题
    public void badCalendarUsage() {
        Calendar calendar = Calendar.getInstance();
        calendar.set(2023, Calendar.JANUARY, 1, 10, 30, 0);  // 月份仍然从0开始

        // 问题1：API 设计复杂，容易出错
        // 问题2：Calendar 是可变的，可能导致意外修改
        // 问题3：性能较差，创建开销大
        // 问题4：时区处理困难
    }
}
```

### 正例：使用 java.time.\* API

```java
// 正例：使用 java.time.* 的正确方式
import java.time.*;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoUnit;

public class GoodTimeExample {

    // 正例1：创建和操作时间
    public void goodTimeCreation() {
        // 创建当前时间
        Instant now = Instant.now();  // 绝对时间戳，UTC

        // 创建特定时间
        LocalDate date = LocalDate.of(2023, 1, 1);  // 2023年1月1日
        LocalTime time = LocalTime.of(10, 30, 0);   // 10:30:00
        LocalDateTime dateTime = LocalDateTime.of(date, time);  // 2023-01-01T10:30:00

        // 创建带时区的时间
        ZonedDateTime zonedDateTime = ZonedDateTime.of(
            dateTime, ZoneId.of("Asia/Shanghai")
        );  // 2023-01-01T10:30:00+08:00[Asia/Shanghai]

        System.out.println("当前时间戳: " + now);
        System.out.println("日期: " + date);
        System.out.println("时间: " + time);
        System.out.println("日期时间: " + dateTime);
        System.out.println("带时区时间: " + zonedDateTime);
    }

    // 正例2：时间计算和比较
    public void goodTimeCalculation() {
        LocalDateTime start = LocalDateTime.of(2023, 1, 1, 10, 0);
        LocalDateTime end = LocalDateTime.of(2023, 1, 1, 12, 30);

        // 计算时间差
        Duration duration = Duration.between(start, end);
        System.out.println("时间差: " + duration);  // PT2H30M (2小时30分钟)
        System.out.println("总秒数: " + duration.getSeconds());  // 9000秒

        // 时间比较
        boolean isAfter = end.isAfter(start);  // true
        boolean isBefore = start.isBefore(end);  // true

        // 时间加减
        LocalDateTime future = start.plusHours(2).plusMinutes(30);
        LocalDateTime past = end.minusDays(1);

        System.out.println("未来时间: " + future);
        System.out.println("过去时间: " + past);
    }

    // 正例3：时区处理
    public void goodTimeZoneHandling() {
        // 获取当前UTC时间
        Instant utcNow = Instant.now();

        // 转换为不同时区
        ZonedDateTime tokyoTime = utcNow.atZone(ZoneId.of("Asia/Tokyo"));
        ZonedDateTime newYorkTime = utcNow.atZone(ZoneId.of("America/New_York"));
        ZonedDateTime londonTime = utcNow.atZone(ZoneId.of("Europe/London"));

        System.out.println("UTC时间: " + utcNow);
        System.out.println("东京时间: " + tokyoTime);
        System.out.println("纽约时间: " + newYorkTime);
        System.out.println("伦敦时间: " + londonTime);

        // 时区转换
        ZonedDateTime shanghaiTime = ZonedDateTime.now(ZoneId.of("Asia/Shanghai"));
        ZonedDateTime utcTime = shanghaiTime.withZoneSameInstant(ZoneId.of("UTC"));

        System.out.println("上海时间: " + shanghaiTime);
        System.out.println("转换为UTC: " + utcTime);
    }

    // 正例4：格式化
    public void goodFormatting() {
        LocalDateTime dateTime = LocalDateTime.of(2023, 1, 1, 10, 30, 45);

        // 使用预定义格式
        DateTimeFormatter formatter1 = DateTimeFormatter.ISO_LOCAL_DATE_TIME;
        String formatted1 = dateTime.format(formatter1);

        // 自定义格式
        DateTimeFormatter formatter2 = DateTimeFormatter.ofPattern("yyyy年MM月dd日 HH:mm:ss");
        String formatted2 = dateTime.format(formatter2);

        // 线程安全的格式化
        System.out.println("ISO格式: " + formatted1);  // 2023-01-01T10:30:45
        System.out.println("中文格式: " + formatted2);  // 2023年01月01日 10:30:45

        // 解析字符串
        LocalDateTime parsed = LocalDateTime.parse("2023-01-01T10:30:45", formatter1);
        System.out.println("解析结果: " + parsed);
    }
}
```

## 注意事项

java.util.Date/Calendar/GregorianCalendar 的有诸多缺陷，简述如下：

1. Date/Calendar 是可变对象。
   - SimpleDateFormat 是线程不安全的。
2. API 容易误用。
   - Date 是一个时间，而不是一个日期
   - 月份从 0 开始（即 1 月 index = 0）
   - 年份从 1900 开始
3. Calendar 有性能问题
4. 处理时区很困难

PS: **“这些 API 很糟糕”**不是笔者的主观判断，而是 Java 社区的普遍认知：

> Class Date represents a specific instant in time, with millisecond precision. The design of this class is a very bad joke - a sobering example of how even good programmers screw up.
> Most of the methods in Date are now deprecated, replaced by methods in the classes below.
>
> Class Calendar is an abstract class for converting between a Date object and a set of integer fields such as year, month, day, and hour.
>
> Class GregorianCalendar is the only subclass of Calendar in the JDK. It does the Date-to-fields conversions for the calendar system in common use. Sun licensed this overengineered junk from Taligent - a sobering example of how average programmers screw up.
>
> -- Java Programmers FAQ

更多可参见：

- https://stackoverflow.com/questions/1571265/why-is-the-java-date-api-java-util-date-calendar-such-a-mess
- https://javarevisited.blogspot.com/2017/04/5-reasons-why-javas-old-date-and-Calendar-API-bad.html#axzz7mUgCccJ0

### `JodaTime`的用法

在 Java 8 以前，由于官方库过于糟糕，公认的 Java 最优秀的时间库是 [Joda-Time - Home](https://www.joda.org/joda-time/)。

`JodaTime` 解决了上述 API 的大部分问题。 `JodaTime` 引入了很多新的概念，令方案看上去很复杂，但这只是因为 `JodaTime` 充分考虑和支持了前述清单里的各种场景。

`JSR 310` 引入了 `java.time.*` 新的时间 API，于 `JDK 1.8` 正式加入。作者正是 `Joda Time` 的作者。[The Java Community Process(SM) Program - JSRs: Java Specification Requests - detail JSR#310](https://jcp.org/en/jsr/detail?id=310)

java.time (Java Platform SE 11 ) 检查如下：

- 是否包含了足够所需的时间概念的抽象？
- 是否提供 “Instant”类型？
- 是否支持 “Duration”类型？
- 是否区分了 Duration 与 Period(Interval)？
- 是否提供 “Local Date”类型（即一个抽象的、与时区无关、与时分秒无关的日期），并支持相关的计算？
- 是否提供 “Time Of Day”类型（即一个与日期无关的时间），并支持相关的计算？

`java.time.*` 均有提供:

- `java.time.Instant` 是数值的时间戳，如 1670245951000000000 = 2022-12-05T13:12:31+00:00。
- `java.time.Duration` 是一段绝对的时间，如 42 seconds。
- `java.time.LocalDate` 存储了一个无时钟时间的日期，如 2022-12-05。
- `java.time.LocalTime` 存储了一个无日期的时钟时间，如 11:30。
- `java.time.LocalDateTime` 存储了一个无时区的日期+时钟时间，如 2022-12-05T11:30。
- `java.time.ZonedDateTime` 存储了一个有时区信息的完整时间。ZonedDateTime 与 Instant 可以互相切换（ Instant -> ZonedDateTime 需要附加时区信息）。

`JodaTime` 类似:

- 是否正确地处理了时区？
- 是否正确地处理了夏令时？
- 如果民用时间和绝对时间的转换（例如由于夏令时，或时区更新）出现了二义性/Overlap 或不存在的时间/Gap，是如何处理的？
- 是否可以正确地更新 tzdata？

`java.time.*`正确处理了时区。`java.time.*` 使用 JRE 自带的 `tzdata`。
`java.time.*` 可以正确处理夏令时:

- Overlap: 通常情况下，`java.time.*` 会转换到两个相同时刻的靠前的时刻。
- Gap：通常情况下，`java.time.*` 会将该时间后移 **夏令时与标准时时差**，通常为一小时，以获得一个存在的时刻。

更多参见 [ZonedDateTime (Java Platform SE 11 )](https://docs.oracle.com/javase/11/docs/api/java/time/ZonedDateTime.html)

JRE 可以使用 TZUpdater 更新 tzdata 信息。[Timezone Updater Tool](https://www.oracle.com/java/technologies/javase/tzupdater-readme.html)

JodaTime 对时区的处理基本一致。但是 `JodaTime` 维护了自己的 `tzdata` 库，所以需要定期更新 `JodaTime` 库。

> 如何处理闰秒？

`java.time.*` 忽略闰秒。
这是指当闰秒出现时，`java.time.*` 不做任何特殊处理，而是由操作系统层面处理。`java.time.*` 认为闰秒出现两次。换言之，与 Unix Time 的处理方式相同。

`JodaTime` 亦然。

> 是否具有足够的时间精度？

`java.time.Instant` 的精度是纳秒（即 1e-9 秒）， `java.time.Duration` 的精度也是纳秒。

但 `JodaTime` 的时间精度只到微秒（即 1e-6 秒）

> 是否支持单调时钟？

`java.time.*` 不支持单调时钟。

使用 `System.nanoTime()` 以获取单调时钟。

[System.nanoTime() (Java Platform SE 7 )](https://docs.oracle.com/javase/7/docs/api/java/lang/System.html#nanoTime)

nanoTime 有两个值得注意的点：

- nanoTime 是与某一个锚定时间的以纳秒计的时差，但 nanoTime 并不是从启动以来的纳秒数。 nanoTime 甚至可能是负的 -- 因为锚定点可能在未来。
- nanoTime 是 JVM 能返回的最高准度的时间。但仍然很可能低于其精度（纳秒）。不过，nanoTime 保证准度不低于 `System.currentTimeMillis()`

安卓端可以使用 `SystemClock` 类获得更多的单调时钟。以下两个 API 尤其有用：

- `SystemClock.uptimeMillis` 返回自启动以来的毫秒数，但不计入系统深度睡眠时间。
- `SystemClock.elapsedRealtime` 返回自启动以来的毫秒数，并计入系统深度睡眠时间。

> 是否支持星期？

`java.time.*` 支持星期，并提供了 DayOfWeek enum 作为 Weekday。

[DayOfWeek (Java Platform SE 11 )](https://docs.oracle.com/javase/11/docs/api/java/time/DayOfWeek.html)

> 是包含时钟界面，还是仅提供静态的时间提供方法？

`java.time.Clock` 提供了抽象 `Clock` 类。可以通过注入 `Fake Deterministic Clock` 依赖以便于单元测试。

是否支持所需的非公历的历法？例如，是否需要支持阴历？

`java.time.*` 只支持 `ISO-8601` 历法，也就是 proleptic Gregorian rules（即支持格里高里历扩展到 1582 年以前）。

## 扩展阅读

《你永远无法理解时间》系列文章：

1. [导语](https://km.woa.com/posts/show/559864?kmref=author_post)
2. [基本概念](https://km.woa.com/posts/show/559874?kmref=author_post)
3. [历法复杂性](https://km.woa.com/posts/show/560262?kmref=author_post)
4. [编程复杂性](https://km.woa.com/posts/show/562484?kmref=author_post)
5. [编程实践](https://km.woa.com/articles/show/566975?ts=1670330437)
