# Visibility 可见性

## tl;dr

- 最小化**类**的可见性
- 除了全局常量（`public static final` 的不可变对象），任何**类成员**都不应该是公开的。提供 `Getter` 和 `Setter`，而不要直接暴露类成员。
- 类**成员方法**应该最小化可见性
- **局部变量**应该最小化可见性。方法应该小而集中，不使局部变量的生命周期过长。

## 最小化类的可见性
类应优先使用默认包级私有（无修饰符）或 private 访问级别，仅在必要时使用 public。

### 正例
遵循最小化类的可见性，对于包级私有工具类，仅限同一包内使用
```java
class VideoInnerUtils {  
    public static String formatVideoName(String s) { 
        return s.trim();
    }
}
```
### 反例
违反最小化类的可见性，实际只需在包内使用，但在全局公开工具类
```java
public class VideoInnerUtils {  
    public static String formatVideoName(String s) {
         return s.trim(); 
    }
}
```

## 类成员变量规范
除了全局常量（`public static final` 的不可变对象），任何**类成员**都不应该是公开的。提供 `Getter` 和 `Setter`，而不要直接暴露类成员。

### 正例
遵循类成员变量不公开，封装成员，通过方法控制访问
```java
public class User {
    private String name;
    private int age;

    public void setName(String name) {
        if (name != null) this.name = name;
    }
    public String getName() { return name; }
}
```
### 反例
内部成员可直接外部访问并修改内部状态，违反类成员封装原则
```java
public class User {
    public String name;  // 直接暴露，破坏封装
    public int age;
}
// 外部代码：user.name = null; // 外部直接可修改，可能导致数据不一致
```

## 类成员方法规范
类**成员方法**应该最小化可见性，方法应使用最严格的访问修饰符（优先 private，其次包级私有、protected）

### 正例
非对外开放类成员方法保持 private 最小化可见性
```java
public class Calculator {
    public int add(int a, int b) { 
        logCalculation(); 
        return a + b;
    }
    private void logCalculation() {
       /* 内部使用 */ 
    }
}
```
### 反例
违反类成员方法最小化可见性,将内部方法进行非必要公开
```java
public class Calculator {
    // 外部可调用，无意义
    public void logCalculation() { 
      /* 内部日志逻辑 */ 
    }  
    public int add(int a, int b) { 
      logCalculation(); 
      return a + b; 
    }
}
```
## 局部变量规范
**局部变量**应该最小化可见性。方法应该小而集中，不使局部变量的生命周期过长。
### 正例
变量作用域最小化在代码块中
```java
public void processData(List<String> data) {
    for (String s : data) {
        // s 和 processed 作用域限于循环块内
        String processed = s.toUpperCase();  
        handleResult(processed);
        ......
    }
}
```
### 反例
违反局部变量最小化可见性，变量作用域过大，易被误修改
```java
public void processData(List<String> data) {
    // result 声明过早作用域过大
    String result = "";  
    for (String s : data) {
        result = s.toUpperCase();  
        handleResult(result);
        // ... 其他操作
    }
    // ... 后续代码无需要操作 result
}
```

## 思考：类方法的可见性是否应该不高于类的可见性？

考虑一个包可见的类：

```java
class Foo {

  void packageVisibleMethod() { ... }
  
  public publicMethod() { ... }
}
```

理论上，一个类的方法的可见性是**方法可见性与类可见性的较低者**。那么，一个 `package private` 的类的 `public` 方法事实上是没有意义的。上文的两种处理方案分别代表两种哲学：

- 方法的可见性是 `package priavte`。因为方法的可见性**应该等于实际可见性**。既然这个方法只对 `Package` 可见，那么它应该就是 `package private`。
- 方法的可见性是 `public`。 因为这个方法的意图是公开的 `API`，至于这个类应该在哪里使用不是这个方法应该关心的。使用 `public` 声明这是一个公开的 `API`。

两种方案都可行。重要的是**一致性**：同一个项目中应该使用统一的处理方案。

## 扩展阅读

- Effective Java Item 15: Minimize the accessibility of classes and members
- Effective Java Item 16: In public classes, use accessor methods, not public fields
- Effective Java Item 57: Minimize the scope of local variables
