# Immutability 不可变性

## tl;dr

- **不可变性是优先推荐的编程方式**。不可变对象是线程安全的，易于理解和测试。
- **遵循不可变类设计原则**。不提供变异子、类不可继承、字段私有且final。
- **合理使用防御性拷贝**。当必须暴露可变对象时，返回其拷贝而非原对象。
- **不要过度担心性能开销**。现代JVM的GC性能足以处理不可变对象的创建开销。

## 什么是不可变性

不可变对象是指创建后，状态不可变更的对象。一旦对象被创建，其内部状态就不能被修改。在Java中，`String`、`Integer`、`LocalDate`等都是不可变类的典型例子。

```java
// String是不可变的
String str = "Hello";
String newStr = str.concat(" World");  // 返回新的String对象，原对象不变
System.out.println(str);     // 输出: Hello
System.out.println(newStr);  // 输出: Hello World
```

## 不可变对象的优势

### 线程安全

不可变对象天然线程安全，无需同步机制：

```java
public final class ImmutableCounter {
    private final int value;
    
    public ImmutableCounter(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public ImmutableCounter increment() {
        return new ImmutableCounter(value + 1);  // 返回新对象
    }
}

// 多线程环境下安全使用
ImmutableCounter counter = new ImmutableCounter(0);
// 多个线程可以安全地读取counter.getValue()
// 每次increment()都返回新对象，不影响原对象
```

### 易于理解和测试

```java
public final class Person {
    private final String name;
    private final int age;
    
    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
    
    public String getName() { return name; }
    public int getAge() { return age; }
    
    // 创建新对象来"修改"状态
    public Person withAge(int newAge) {
        return new Person(this.name, newAge);
    }
}

// 测试简单直观
@Test
public void testPersonImmutability() {
    Person person = new Person("Alice", 25);
    Person olderPerson = person.withAge(26);
    
    assertEquals(25, person.getAge());     // 原对象未变
    assertEquals(26, olderPerson.getAge()); // 新对象有新状态
}
```

### 可以安全地用作Map键和Set元素

```java
public final class Point {
    private final int x, y;
    
    public Point(int x, int y) {
        this.x = x;
        this.y = y;
    }
    
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (!(obj instanceof Point)) return false;
        Point point = (Point) obj;
        return x == point.x && y == point.y;
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(x, y);
    }
}

// 安全地用作Map键
Map<Point, String> pointMap = new HashMap<>();
Point point = new Point(1, 2);
pointMap.put(point, "origin");
// point的hashCode不会变化，Map的完整性得到保证
```

### 支持缓存和懒计算

```java
public final class ExpensiveObject {
    private final String data;
    private volatile int hashCode; // 懒计算的hashCode
    
    public ExpensiveObject(String data) {
        this.data = data;
    }
    
    @Override
    public int hashCode() {
        int result = hashCode;
        if (result == 0) {
            result = Objects.hash(data);
            hashCode = result;
        }
        return result;
    }
}
```

### 失败原子性

```java
public final class BankAccount {
    private final String accountNumber;
    private final BigDecimal balance;
    
    public BankAccount(String accountNumber, BigDecimal balance) {
        this.accountNumber = Objects.requireNonNull(accountNumber);
        this.balance = Objects.requireNonNull(balance);
        if (balance.compareTo(BigDecimal.ZERO) < 0) {
            throw new IllegalArgumentException("Balance cannot be negative");
        }
    }
    
    public BankAccount withdraw(BigDecimal amount) {
        BigDecimal newBalance = balance.subtract(amount);
        if (newBalance.compareTo(BigDecimal.ZERO) < 0) {
            throw new IllegalArgumentException("Insufficient funds");
        }
        return new BankAccount(accountNumber, newBalance);
    }
}

// 如果withdraw失败，原对象状态完全不受影响
```

## 创建不可变类的原则

### 不提供任何变异子（mutator）方法

```java
// 错误：提供了setter方法
public class MutablePerson {
    private String name;
    
    public void setName(String name) {  // 变异子方法
        this.name = name;
    }
}

// 正确：只提供访问子方法
public final class ImmutablePerson {
    private final String name;
    
    public ImmutablePerson(String name) {
        this.name = name;
    }
    
    public String getName() {  // 只有访问子方法
        return name;
    }
}
```

### 确保类不能被继承

```java
// 方式1：使用final关键字
public final class ImmutableClass {
    // 类实现
}

// 方式2：私有构造函数 + 静态工厂方法
public class ImmutableClass {
    private ImmutableClass() {
        // 私有构造函数
    }
    
    public static ImmutableClass of(String value) {
        return new ImmutableClass();
    }
}
```

### 所有字段都是private final

```java
public final class ImmutableStudent {
    private final String name;
    private final int age;
    private final List<String> courses;
    
    public ImmutableStudent(String name, int age, List<String> courses) {
        this.name = name;
        this.age = age;
        // 防御性拷贝
        this.courses = new ArrayList<>(courses);
    }
    
    public String getName() { return name; }
    public int getAge() { return age; }
    public List<String> getCourses() { 
        return new ArrayList<>(courses);  // 返回拷贝
    }
}
```

### 对于可变字段，进行防御性拷贝

```java
public final class ImmutableSchedule {
    private final Date startTime;
    private final Date endTime;
    
    public ImmutableSchedule(Date startTime, Date endTime) {
        // 防御性拷贝：Date是可变的
        this.startTime = new Date(startTime.getTime());
        this.endTime = new Date(endTime.getTime());
    }
    
    public Date getStartTime() {
        return new Date(startTime.getTime());  // 返回拷贝
    }
    
    public Date getEndTime() {
        return new Date(endTime.getTime());    // 返回拷贝
    }
}
```

## 防御性拷贝（Defensive Copy）

当类必须包含可变对象的引用时，需要进行防御性拷贝：

### 构造函数中的防御性拷贝

```java
public final class ImmutablePeriod {
    private final Date start;
    private final Date end;
    
    public ImmutablePeriod(Date start, Date end) {
        // 防御性拷贝：防止外部修改传入的Date对象
        this.start = new Date(start.getTime());
        this.end = new Date(end.getTime());
        
        if (this.start.compareTo(this.end) > 0) {
            throw new IllegalArgumentException("Start after end: " + start + ", " + end);
        }
    }
    
    public Date start() {
        return new Date(start.getTime());  // 返回拷贝
    }
    
    public Date end() {
        return new Date(end.getTime());    // 返回拷贝
    }
}

// 使用示例
Date start = new Date();
Date end = new Date(start.getTime() + 1000);
ImmutablePeriod period = new ImmutablePeriod(start, end);

// 修改原始Date对象不会影响ImmutablePeriod
start.setTime(0);
System.out.println(period.start());  // 不受影响
```

### 集合的防御性拷贝

```java
public final class ImmutableClassroom {
    private final List<String> students;
    private final Set<String> subjects;
    
    public ImmutableClassroom(List<String> students, Set<String> subjects) {
        // 深拷贝集合
        this.students = new ArrayList<>(students);
        this.subjects = new HashSet<>(subjects);
    }
    
    public List<String> getStudents() {
        return new ArrayList<>(students);  // 返回拷贝
    }
    
    public Set<String> getSubjects() {
        return new HashSet<>(subjects);    // 返回拷贝
    }
    
    // 或者返回不可修改的视图
    public List<String> getStudentsView() {
        return Collections.unmodifiableList(students);
    }
}
```

## 常见的不可变类实现模式

### Builder模式

对于字段较多的不可变类，使用Builder模式：

```java
public final class ImmutableUser {
    private final String username;
    private final String email;
    private final int age;
    private final List<String> roles;
    
    private ImmutableUser(Builder builder) {
        this.username = builder.username;
        this.email = builder.email;
        this.age = builder.age;
        this.roles = Collections.unmodifiableList(new ArrayList<>(builder.roles));
    }
    
    // 访问子方法
    public String getUsername() { return username; }
    public String getEmail() { return email; }
    public int getAge() { return age; }
    public List<String> getRoles() { return roles; }
    
    public static class Builder {
        private String username;
        private String email;
        private int age;
        private List<String> roles = new ArrayList<>();
        
        public Builder setUsername(String username) {
            this.username = username;
            return this;
        }
        
        public Builder setEmail(String email) {
            this.email = email;
            return this;
        }
        
        public Builder setAge(int age) {
            this.age = age;
            return this;
        }
        
        public Builder addRole(String role) {
            this.roles.add(role);
            return this;
        }
        
        public ImmutableUser build() {
            return new ImmutableUser(this);
        }
    }
}

// 使用示例
ImmutableUser user = new ImmutableUser.Builder()
    .setUsername("alice")
    .setEmail("alice@example.com")
    .setAge(25)
    .addRole("USER")
    .addRole("ADMIN")
    .build();
```

### 工厂方法模式

```java
public final class ImmutablePoint {
    private final int x, y;
    
    private ImmutablePoint(int x, int y) {
        this.x = x;
        this.y = y;
    }
    
    public static ImmutablePoint of(int x, int y) {
        return new ImmutablePoint(x, y);
    }
    
    public static ImmutablePoint origin() {
        return new ImmutablePoint(0, 0);
    }
    
    public int getX() { return x; }
    public int getY() { return y; }
    
    public ImmutablePoint translate(int dx, int dy) {
        return new ImmutablePoint(x + dx, y + dy);
    }
}
```

### 使用Record（Java 14+）

```java
// Java 14+ 的Record自动创建不可变类
public record ImmutablePerson(String name, int age) {
    public ImmutablePerson {
        Objects.requireNonNull(name);
        if (age < 0) {
            throw new IllegalArgumentException("Age cannot be negative");
        }
    }
    
    public ImmutablePerson withAge(int newAge) {
        return new ImmutablePerson(name, newAge);
    }
}
```

## 性能考虑

### 不要过度担心对象创建开销

```java
// 担心：每次操作都创建新对象
public final class ImmutableCounter {
    private final int value;
    
    public ImmutableCounter(int value) {
        this.value = value;
    }
    
    public ImmutableCounter increment() {
        return new ImmutableCounter(value + 1);  // 新对象
    }
}

// 现实：现代JVM的对象创建和GC非常高效
// 不可变对象的优势通常超过创建开销
```

### 对象池和缓存

对于常用的不可变对象，可以考虑缓存：

```java
public final class ImmutableInteger {
    private static final Map<Integer, ImmutableInteger> CACHE = new ConcurrentHashMap<>();
    private final int value;
    
    private ImmutableInteger(int value) {
        this.value = value;
    }
    
    public static ImmutableInteger valueOf(int value) {
        return CACHE.computeIfAbsent(value, ImmutableInteger::new);
    }
    
    public int getValue() { return value; }
}
```

## 常见陷阱和最佳实践

### 避免在构造函数中调用可重写的方法

```java
// 错误：在构造函数中调用可重写的方法
public class BadImmutableClass {
    private final String value;
    
    public BadImmutableClass(String input) {
        this.value = process(input);  // 危险：如果被继承，process可能被重写
    }
    
    protected String process(String input) {
        return input.toUpperCase();
    }
}

// 正确：使用private方法或static方法
public final class GoodImmutableClass {
    private final String value;
    
    public GoodImmutableClass(String input) {
        this.value = processInput(input);  // 安全：private方法
    }
    
    private static String processInput(String input) {
        return input.toUpperCase();
    }
}
```

### 正确实现equals和hashCode

```java
public final class ImmutableBook {
    private final String title;
    private final String author;
    private final int pages;
    
    public ImmutableBook(String title, String author, int pages) {
        this.title = Objects.requireNonNull(title);
        this.author = Objects.requireNonNull(author);
        this.pages = pages;
    }
    
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (!(obj instanceof ImmutableBook)) return false;
        ImmutableBook book = (ImmutableBook) obj;
        return pages == book.pages &&
               Objects.equals(title, book.title) &&
               Objects.equals(author, book.author);
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(title, author, pages);
    }
    
    @Override
    public String toString() {
        return String.format("Book{title='%s', author='%s', pages=%d}", 
                           title, author, pages);
    }
}
```

### 处理null值

```java
public final class ImmutableAddress {
    private final String street;
    private final String city;
    private final String zipCode;
    
    public ImmutableAddress(String street, String city, String zipCode) {
        this.street = Objects.requireNonNull(street, "Street cannot be null");
        this.city = Objects.requireNonNull(city, "City cannot be null");
        this.zipCode = Objects.requireNonNull(zipCode, "Zip code cannot be null");
    }
    
    // 提供Optional返回类型的方法（如果字段可能为null）
    public Optional<String> getApartmentNumber() {
        return Optional.ofNullable(apartmentNumber);
    }
}
```

## 与可变类的互操作

转换方法

```java
public final class ImmutableConfiguration {
    private final Map<String, String> properties;
    
    private ImmutableConfiguration(Map<String, String> properties) {
        this.properties = Collections.unmodifiableMap(new HashMap<>(properties));
    }
    
    public static ImmutableConfiguration of(Map<String, String> properties) {
        return new ImmutableConfiguration(properties);
    }
    
    // 转换为可变Map
    public Map<String, String> toMutableMap() {
        return new HashMap<>(properties);
    }
    
    // 创建修改后的新实例
    public ImmutableConfiguration withProperty(String key, String value) {
        Map<String, String> newProperties = new HashMap<>(properties);
        newProperties.put(key, value);
        return new ImmutableConfiguration(newProperties);
    }
    
    public ImmutableConfiguration withoutProperty(String key) {
        Map<String, String> newProperties = new HashMap<>(properties);
        newProperties.remove(key);
        return new ImmutableConfiguration(newProperties);
    }
}
```

## 函数式编程中的不可变性

```java
public final class ImmutableList<T> {
    private final List<T> items;
    
    private ImmutableList(List<T> items) {
        this.items = Collections.unmodifiableList(new ArrayList<>(items));
    }
    
    public static <T> ImmutableList<T> of(T... items) {
        return new ImmutableList<>(Arrays.asList(items));
    }
    
    public static <T> ImmutableList<T> copyOf(Collection<T> items) {
        return new ImmutableList<>(new ArrayList<>(items));
    }
    
    // 函数式操作，返回新的不可变列表
    public <R> ImmutableList<R> map(Function<T, R> mapper) {
        return items.stream()
                   .map(mapper)
                   .collect(collectingAndThen(toList(), ImmutableList::copyOf));
    }
    
    public ImmutableList<T> filter(Predicate<T> predicate) {
        return items.stream()
                   .filter(predicate)
                   .collect(collectingAndThen(toList(), ImmutableList::copyOf));
    }
    
    public ImmutableList<T> add(T item) {
        List<T> newItems = new ArrayList<>(items);
        newItems.add(item);
        return new ImmutableList<>(newItems);
    }
}
```

## 最佳实践总结

1. **优先选择不可变性**：除非有明确的性能需求，否则优先创建不可变类
2. **使用final关键字**：类、字段都应该尽可能使用final
3. **防御性拷贝**：对于可变字段，在构造函数和访问子中都要进行拷贝
4. **正确实现equals/hashCode**：确保不可变对象可以正确用作Map键
5. **提供便利的创建方法**：使用Builder模式、工厂方法等简化对象创建
6. **文档化不可变性**：在类的Javadoc中明确说明类是不可变的

## 扩展阅读

- Effective Java Item 17: Minimize mutability
- Effective Java Item 50: Make defensive copies when needed
- [Oracle Java Tutorial: Immutable Objects](https://docs.oracle.com/javase/tutorial/essential/concurrency/immutable.html)
- [Google Guava: Immutable Collections](https://github.com/google/guava/wiki/ImmutableCollectionsExplained)

