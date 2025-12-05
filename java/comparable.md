# Comparable 比较函数

## tl;dr

- **实现 `Comparable` 接口以提供这个类的比较能力。**
- **实现 `Comparable`需要保证反对称性、传递性、传递等价性，应该保证与 `equals` 的等效性。**
- `Foo implements Comparable<Bar>` 是错误，只能有 `Foo implements Comparable<Foo>`。

## Comparable 的实现约定

类似于 `hashCode` 会被 `HashSet/HashMap` 等使用，`Comparable` 会被标准库所有的需要进行对象**排序关系比较** 的场景使用，例如标准库的 `sort` API，以及 `TreeMap/TreeSet` 等。

`Comparable` 只有一个方法签名，即 `compareTo`。根据[文档](https://docs.oracle.com/javase/11/docs/api/java/lang/Comparable.html)，需要符合以下性质：

- **反对称性**，即 `x.compareTo(y)` 和 `y.compareTo(x)` 的符号必须是相反的。换言之，如果 `x > y`，那么必须有 `y < x`。对等号同理。
- **传递性**，即如果 `x.compareTo(y)` 和 `y.compareTo(z)` 符号相同，那么必须与 `x.compareTo(z)` 的符号相同。换言之，如果 `x > y` 且 `y > z`，那么必须有 `x > z`。对等号同理。
- **传递等价性**，即如果`x.compareTo(y) == 0`，那么对于任何 `z`， `x.compareTo(z)` 和 `y.compareTo(z）`必须是同符号的。
- **与 `equals` 的等效性**，这不是一个强制要求，但是非常符合直觉，应该总是保证：即 `x.compareTo(y) == 0` 与 `x.equals(y)` 总是相同。换言之，`compareTo` 与 `equals` 应该一致。

### 正例

```java
class Cap implements Comparable<Cap> {
    double threshold;

    @Override
    public int compareTo(Cap o) {
        if (o == null) {
            throw new NullPointerException("Compared Cap is null");
        }
        return Double.compare(threshold, o.threshold);
    }

    @Override
    public boolean equals(Object o) {
        if (o == null || getClass() != o.getClass()) return false;
        Cap cap = (Cap) o;
        return Double.compare(threshold, cap.threshold) == 0;
    }

    @Override
    public int hashCode() {
        return Objects.hash(threshold);
    }
}
```

## Comparable 必须特化为自身

`Comparable<T>` 必须的 `T` 必须是类型**自身**。

```java
// BAD -- 类型不一致
class Foo implements Comparable<Bar> {}

// Good: T 必须是自身:
class Foo implements Comparable<Foo> {}
```

Comparable 只能与自身类型比较，它不能表示两个不同类型之间的比较，因为它无法保证**反对称性**。

### 反例

```java
// 很难去保证
Foo.compareTo(Bar) == Bar.compareTo(Foo)
```

## 实际应用场景

### 在集合排序中使用 Comparable

```java
// 正例：在List排序中使用
public class Student implements Comparable<Student> {
    private final String name;
    private final int grade;

    public Student(String name, int grade) {
        this.name = name;
        this.grade = grade;
    }

    @Override
    public int compareTo(Student other) {
        // 先按成绩排序，成绩相同按姓名排序
        int gradeComparison = Integer.compare(this.grade, other.grade);
        if (gradeComparison != 0) {
            return gradeComparison;
        }
        return this.name.compareTo(other.name);
    }

    @Override
    public String toString() {
        return name + " (" + grade + ")";
    }
}

// 使用示例
List<Student> students = Arrays.asList(
    new Student("Alice", 85),
    new Student("Bob", 90),
    new Student("Charlie", 85)
);
Collections.sort(students); // 自动使用compareTo方法
System.out.println(students); // [Alice (85), Charlie (85), Bob (90)]
```

### 在 TreeSet 和 TreeMap 中使用

```java
// 正例：在TreeSet中使用Comparable
public class Product implements Comparable<Product> {
    private final String name;
    private final double price;

    public Product(String name, double price) {
        this.name = name;
        this.price = price;
    }

    @Override
    public int compareTo(Product other) {
        return Double.compare(this.price, other.price);
    }
}

// 使用示例
Set<Product> products = new TreeSet<>();
products.add(new Product("Laptop", 999.99));
products.add(new Product("Mouse", 29.99));
products.add(new Product("Keyboard", 79.99));

// TreeSet会自动按照price排序
for (Product product : products) {
    System.out.println(product.name + ": $" + product.price);
}
```

## 多字段比较示例

### 复杂对象的比较

```java
// 正例：多字段比较的完整实现
public class Employee implements Comparable<Employee> {
    private final String department;
    private final String name;
    private final int salary;
    private final LocalDate hireDate;

    public Employee(String department, String name, int salary, LocalDate hireDate) {
        this.department = department;
        this.name = name;
        this.salary = salary;
        this.hireDate = hireDate;
    }

    @Override
    public int compareTo(Employee other) {
        // 1. 先按部门排序
        int deptComparison = this.department.compareTo(other.department);
        if (deptComparison != 0) {
            return deptComparison;
        }

        // 2. 部门相同，按薪资降序排序
        int salaryComparison = Integer.compare(other.salary, this.salary);
        if (salaryComparison != 0) {
            return salaryComparison;
        }

        // 3. 薪资相同，按入职日期排序
        int dateComparison = this.hireDate.compareTo(other.hireDate);
        if (dateComparison != 0) {
            return dateComparison;
        }

        // 4. 最后按姓名排序
        return this.name.compareTo(other.name);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Employee employee = (Employee) o;
        return salary == employee.salary &&
               Objects.equals(department, employee.department) &&
               Objects.equals(name, employee.name) &&
               Objects.equals(hireDate, employee.hireDate);
    }

    @Override
    public int hashCode() {
        return Objects.hash(department, name, salary, hireDate);
    }
}
```

## 违反 Comparable 契约的常见问题

### 违反传递性的示例

```java
// 反例：违反传递性的实现
public class BadComparable implements Comparable<BadComparable> {
    private final String name;
    private final int priority;

    public BadComparable(String name, int priority) {
        this.name = name;
        this.priority = priority;
    }

    @Override
    public int compareTo(BadComparable other) {
        // 错误：复杂的比较逻辑可能违反传递性
        if (this.priority == other.priority) {
            // 如果优先级相同，按名称长度比较
            return Integer.compare(this.name.length(), other.name.length());
        }
        return Integer.compare(this.priority, other.priority);
    }
}

// 问题演示：
// A(priority=1, name="a") vs B(priority=1, name="ab") vs C(priority=1, name="abc")
// A < B (长度1 < 2), B < C (长度2 < 3), 但可能 A 不 < C
```

### 违反与 equals 一致性的示例

```java
// 反例：compareTo与equals不一致
public class InconsistentComparable implements Comparable<InconsistentComparable> {
    private final String name;
    private final int version;

    public InconsistentComparable(String name, int version) {
        this.name = name;
        this.version = version;
    }

    @Override
    public int compareTo(InconsistentComparable other) {
        // 只按名称比较，忽略版本
        return this.name.compareTo(other.name);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        InconsistentComparable that = (InconsistentComparable) o;
        return version == that.version && Objects.equals(name, that.name);
    }

    // 问题：两个对象可能compareTo返回0但equals返回false
}

// 问题演示：
// obj1 = new InconsistentComparable("test", 1)
// obj2 = new InconsistentComparable("test", 2)
// obj1.compareTo(obj2) == 0 但 obj1.equals(obj2) == false
```

## Comparable vs Comparator

### 主要区别

| 特性         | Comparable   | Comparator              |
| ------------ | ------------ | ----------------------- |
| **定义位置** | 在类内部实现 | 可以在类外部定义        |
| **排序逻辑** | 类的自然排序 | 可以定义多种排序方式    |
| **使用场景** | 类的默认排序 | 需要多种排序方式时      |
| **修改成本** | 修改类本身   | 可以创建新的 Comparator |

### 使用场景对比

```java
// 正例：使用Comparable（自然排序）
public class Person implements Comparable<Person> {
    private final String name;
    private final int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    @Override
    public int compareTo(Person other) {
        return this.name.compareTo(other.name); // 按姓名自然排序
    }
}

// 正例：使用Comparator（多种排序方式）
public class PersonComparator {
    // 按年龄排序
    public static Comparator<Person> byAge() {
        return Comparator.comparingInt(Person::getAge);
    }

    // 按姓名长度排序
    public static Comparator<Person> byNameLength() {
        return Comparator.comparingInt(p -> p.getName().length());
    }

    // 复合排序：先按年龄，再按姓名
    public static Comparator<Person> byAgeThenName() {
        return Comparator
            .comparingInt(Person::getAge)
            .thenComparing(Person::getName);
    }
}

// 使用示例
List<Person> people = Arrays.asList(
    new Person("Alice", 25),
    new Person("Bob", 30),
    new Person("Charlie", 25)
);

// 使用自然排序（Comparable）
Collections.sort(people);
System.out.println("自然排序: " + people);

// 使用不同Comparator
people.sort(PersonComparator.byAge());
System.out.println("按年龄: " + people);

people.sort(PersonComparator.byNameLength());
System.out.println("按姓名长度: " + people);
```

### 何时使用 Comparable vs Comparator

**使用 Comparable 的情况：**

- 类有明确的自然排序顺序
- 只需要一种排序方式
- 排序逻辑是类的核心特性

**使用 Comparator 的情况：**

- 需要多种排序方式
- 不能修改原类（第三方类）
- 需要临时或特殊的排序逻辑

```java
// 正例：灵活使用Comparator
public class FlexibleSorting {
    public static void demonstrateSorting() {
        List<String> words = Arrays.asList("apple", "banana", "cherry", "date");

        // 自然排序
        words.sort(Comparator.naturalOrder());

        // 反向排序
        words.sort(Comparator.reverseOrder());

        // 按长度排序
        words.sort(Comparator.comparingInt(String::length));

        // 自定义排序：忽略大小写
        words.sort(String.CASE_INSENSITIVE_ORDER);

        // 复合排序：先按长度，再按字母顺序
        words.sort(Comparator
            .comparingInt(String::length)
            .thenComparing(Comparator.naturalOrder()));
    }
}
```

## 扩展阅读

- Effective Java Item 14: Consider implementing Comparable
- [ErrorProne ComparableType](https://errorprone.info/bugpattern/ComparableType)
