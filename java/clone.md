# Clone() 方法

## tl;dr

- 避免实现 `Clone`，这是 `Java` 的失败设计。
- 如果有需要，优先使用复制构造函数（Copy Constructor）或复制工厂方法（Copy Factory）。

## 避免使用 `Clone`

- ❌ 避免实现`Cloneable`接口（Java 的失败设计）
- ✅ 优先使用复制构造函数或静态工厂方法实现对象复制

为什么避免使用 Clone()？

1. `浅拷贝问题`：默认实现是浅拷贝，可能引发数据不一致
2. `类型不安全`：返回 `Object` 类型需要强制转换
3. `契约脆弱`：未声明 `CloneNotSupportedException` 时可能抛出运行时异常

### 反例

```java
// 反例：仅复制数组引用，浅拷贝问题
public class Problem implements Cloneable {
    private int[] data;

    @Override
    public Object clone() throws CloneNotSupportedException {
        return super.clone(); // 仅复制数组引用
    }
}
```

## 优先使用复制构造函数或工厂方法

复制构造函数和工厂方法更灵活，且能避免 `Clone` 的问题。

### 正例

```java
// 正例1：复制构造函数（类层次结构简单时）
public class Solution {
    private final int[] data;

    // 复制构造函数
    public Solution(Solution other) {
        this.data = Arrays.copyOf(other.data, other.data.length); // 深拷贝
    }
}

// 【正例2】静态工厂方法（需要更灵活的对象创建控制时）
public class Advanced {
    private List<String> items;

    public static Advanced newInstance(Advanced proto) {
        Advanced obj = new Advanced();
        List<MutableObject> newList = new ArrayList<>();// 深拷贝单个数组对象
        for (MutableObject item : proto.originalList) {
            newList.add(new MutableObject(item)); // 深拷贝每个元素
        }
        obj.items = new ArrayList<>(newList);
        return obj;
    }
}

## 扩展阅读

1. 《Effective Java 3rd》Item 13: 谨慎覆盖 clone
2. Oracle 官方文档: Object Copying in Java
3. 《Java 编程思想》第 6 章：复用类
4. 《代码整洁之道》第 10 章：类设计原则
5. Joshua Bloch 演讲: How to Design a Good API https://static.googleusercontent.com/media/research.google.com/zh-CN//pubs/archive/32713.pdf
```
