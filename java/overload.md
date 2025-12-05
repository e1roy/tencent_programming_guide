# Overload 重载

## tl;dr

- 尽量不使用重载，优先使用不同的函数名字。
- 使用 Interface 作为参数的类型，推迟设计决策。
- 如果必须重载，任何两个重载函数不要有**相同数量** 的参数。
- 工厂方法替代构造函数，避免构造函数重载问题

## Overload 会由于类型隐式转换造成困惑

### 反例：提供多个参数类型相似的多个重载函数，对使用者造成困惑
```java
class Window {

    void setWidth(double w) {
        System.out.println("with double");
    }

    void setWidth(float w) {
        System.out.println("with float");
    }

    void setWidth(int w) {
        System.out.println("with int");
    }
}

Window w = new Window();
w.setWidth(2.3);   //  到底调用了哪个？
w.setWidth(2);     // 
w.setWidth(2.3f);  // 
```

### 正例1：使用不同的方法名来显示区分

```java
class Window {

    void setWidthDouble(double w) {
        System.out.println("with double");
    }

    void setWidthFloat(float w) {
        System.out.println("with float");
    }

    // 注意：如果有一个常见的主方法，可以把它作为主要函数。
    void setWidth(int w) {
        System.out.println("with int");
    }
}
```

### 正例2：使用接口作为统一参数

此外，也可以采用 Interface 来推迟决策：

```java
interface WindowWidth {

    int parseInt();

    int parseDouble();

    int parseLong();
}

class Window {

    void setWidth(WindowWidth width) {
        System.out.println("with int:" + width.parseInt());
    }
}
```

### 正例3：对于多个同名的构造函数优先考虑工厂方法替代构造函数

```java
class Coordinate {

    private final double x, y;

    private Coordinate(double x, double y) {
        this.x = x;
        this.y = y;
    }
  
    public static Coordinate fromDoubles(double x, double y) {
        return new Coordinate(x, y);
    }

    public static Coordinate fromArray(double[] values) {
        return new Coordinate(values[0], values[1]);
    }

    public static Coordinate fromString(String input) {
        String[] parts = input.split(",");
        return new Coordinate(
                Double.parseDouble(parts[0]),
                Double.parseDouble(parts[1])
        );
    }
}

// 清晰且无歧义的创建方式
Coordinate c1 = Coordinate.fromDoubles(1.2, 3.4);
Coordinate c2 = Coordinate.fromArray(new double[]{5.6, 7.8});
Coordinate c3 = Coordinate.fromString("9.1,2.3");

```

## 扩展阅读

- Effective Java Item 52: Use overloading judiciously
- Java Puzzlers: Puzzle 46 - The Case of the Confusing Constructor
