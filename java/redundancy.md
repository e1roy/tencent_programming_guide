# Redundancy 冗余

## tl;dr

- **主动清理所有冗余**：提高代码可读性、可维护性和性能
- **基础语法优化**：钻石操作符(`<>`)、增强型 `for` 循环、`try-with-resources`
- **现代 Java 特性**：`Lambda` 表达式、`Stream API`、`Optional` 消除样板代码
- **代码重构**：消除重复代码、不必要的变量声明、类型转换
- **最佳实践**：通常情况下，声明式编程优于命令式，链式调用优于复杂的嵌套判断

典型的解除冗余的方法包括：

## Diamond Generics

使用钻石操作符(`Diamond Operator`)节省声明长度：

### 反例

```java
// 反例1：重复声明泛型类型
List<String> strings = new ArrayList<String>();  // 冗余：重复声明String类型

// 反例2：使用原始类型（会产生警告）
List<String> strings = new ArrayList();  // 问题：原始类型，编译器警告
```

### 正例

```java
// 正例：使用钻石操作符，简洁明了
List<String> strings = new ArrayList<>();  // 简洁：类型推断，无冗余
```

## 使用增强型 `for` 循环（`for-each`）

避免下标错误，代码更简练易读。

### 反例

```java
// 反例：传统for循环，容易出错且冗余
for (int i = 0; i < list.size(); i++) {
    System.out.println(list.get(i));  // 问题：需要手动管理索引，容易越界
}
```

### 正例

```java
// 正例：增强型for循环，简洁安全
for (String item : list) {
    System.out.println(item);  // 优势：自动处理索引，避免越界错误
}
```

## 使用 `try-with-resources` 自动管理资源

保证资源关闭，减少样板代码（boilerplate）。

### 反例

```java
// 反例：手动管理资源，代码冗余且容易出错
FileInputStream fis = new FileInputStream("file.txt");
try {
    // 读取文件内容
    int data = fis.read();
} finally {
    fis.close();  // 问题：手动关闭资源，容易忘记或异常处理不当
}
```

### 正例

```java
// 正例：自动资源管理，简洁安全
try (FileInputStream fis = new FileInputStream("file.txt")) {
    // 读取文件内容
    int data = fis.read();  // 优势：自动关闭资源，无需手动管理
}  // 资源会自动关闭，即使发生异常
```

## 使用 `Lambda `表达式消除冗余

### 简化匿名内部类

### 反例

```java
// 反例：冗长的匿名内部类
List<String> names = Arrays.asList("Alice", "Bob", "Charlie");
Collections.sort(names, new Comparator<String>() {
    @Override
    public int compare(String a, String b) {
        return a.compareTo(b);  // 冗余：大量样板代码
    }
});
```

### 正例

```java
// 正例：简洁的Lambda表达式
List<String> names = Arrays.asList("Alice", "Bob", "Charlie");
Collections.sort(names, (a, b) -> a.compareTo(b));  // 简洁：一行代码完成
// 或者使用方法引用更简洁
Collections.sort(names, String::compareTo);
```

### 简化事件处理

### 反例

```java
// 反例：冗长的匿名内部类
button.addActionListener(new ActionListener() {
    @Override
    public void actionPerformed(ActionEvent e) {
        System.out.println("按钮被点击");  // 冗余：大量样板代码
    }
});
```

### 正例

```java
// 正例：简洁的Lambda表达式
button.addActionListener(e -> System.out.println("按钮被点击"));  // 简洁：一行代码
```

## 使用 `Stream API` 消除冗余

### 简化集合操作

### 反例

```java
// 反例：传统循环处理集合
List<String> names = Arrays.asList("Alice", "Bob", "Charlie", "David");
List<String> result = new ArrayList<>();
for (String name : names) {
    if (name.length() > 4) {  // 冗余：手动循环和过滤
        result.add(name.toUpperCase());
    }
}
```

### 正例

```java
// 正例：Stream API链式操作
List<String> names = Arrays.asList("Alice", "Bob", "Charlie", "David");
List<String> result = names.stream()
    .filter(name -> name.length() > 4)  // 简洁：声明式编程
    .map(String::toUpperCase)
    .collect(Collectors.toList());
```

### 简化数据统计

### 反例

```java
// 反例：手动统计
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
int sum = 0;
int count = 0;
for (Integer num : numbers) {  // 冗余：手动遍历和统计
    if (num % 2 == 0) {
        sum += num;
        count++;
    }
}
double average = (double) sum / count;
```

### 正例

```java
// 正例：Stream API统计
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
double average = numbers.stream()
    .filter(num -> num % 2 == 0)  // 简洁：声明式过滤和统计
    .mapToInt(Integer::intValue)
    .average()
    .orElse(0.0);
```

## 使用 `Optional` 消除冗余

### 简化 `null` 检查

### 反例

```java
// 反例：多层 null 检查
public String getUserName(User user) {
    if (user != null) {  // 冗余：多层null检查
        if (user.getProfile() != null) {
            if (user.getProfile().getName() != null) {
                return user.getProfile().getName();
            }
        }
    }
    return "Unknown";
}
```

### 正例

```java
// 正例：Optional 链式调用
public String getUserName(User user) {
    return Optional.ofNullable(user)
        .map(User::getProfile)  // 简洁：链式null安全调用
        .map(Profile::getName)
        .orElse("Unknown");
}
```

### 简化条件逻辑

### 反例

```java
// 反例：复杂的条件判断
public void processUser(String userId) {
    User user = userService.findById(userId);
    if (user != null) {  // 冗余：复杂的条件嵌套
        if (user.isActive()) {
            if (user.hasPermission()) {
                // 处理用户
                doProcess(user);
            } else {
                log.warn("用户无权限: " + userId);
            }
        } else {
            log.warn("用户未激活: " + userId);
        }
    } else {
        log.warn("用户不存在: " + userId);
    }
}
```

### 正例

```java
// 正例：Optional 简化条件逻辑
public void processUser(String userId) {
    Optional.ofNullable(userService.findById(userId))
        .filter(User::isActive)  // 简洁：声明式条件过滤
        .filter(User::hasPermission)
        .ifPresentOrElse(
            this::doProcess,
            () -> log.warn("用户不存在、未激活或无权限: " + userId)
        );
}
```

## 其他常见冗余类型

### 不必要的变量声明

### 反例

```java
// 反例：不必要的中间变量
public int calculateTotal(List<Integer> numbers) {
    int sum = 0;  // 冗余：不必要的变量声明
    for (int num : numbers) {
        sum = sum + num;
    }
    return sum;
}
```

### 正例

```java
// 正例：直接返回结果
public int calculateTotal(List<Integer> numbers) {
    return numbers.stream()  // 简洁：直接返回计算结果
        .mapToInt(Integer::intValue)
        .sum();
}
```

### 重复的代码块

### 反例

```java
// 反例：重复的验证逻辑
public void validateUser(User user) {
    if (user.getName() == null || user.getName().trim().isEmpty()) {
        throw new IllegalArgumentException("用户名不能为空");
    }
    if (user.getEmail() == null || user.getEmail().trim().isEmpty()) {
        throw new IllegalArgumentException("邮箱不能为空");  // 冗余：重复的验证逻辑
    }
    if (user.getPhone() == null || user.getPhone().trim().isEmpty()) {
        throw new IllegalArgumentException("电话不能为空");
    }
}
```

### 正例

```java
// 正例：提取通用验证方法
public void validateUser(User user) {
    validateNotEmpty(user.getName(), "用户名不能为空");
    validateNotEmpty(user.getEmail(), "邮箱不能为空");  // 简洁：复用验证方法
    validateNotEmpty(user.getPhone(), "电话不能为空");
}

private void validateNotEmpty(String value, String message) {
    if (value == null || value.trim().isEmpty()) {
        throw new IllegalArgumentException(message);
    }
}
```

### 不必要的类型转换

### 反例

```java
// 反例：不必要的类型转换
public void processNumbers(List<Object> objects) {
    for (Object obj : objects) {
        if (obj instanceof String) {  // 冗余：不必要的类型检查
            String str = (String) obj;
            System.out.println(str.toUpperCase());
        }
    }
}
```

### 正例

```java
// 正例：使用泛型和 Stream API
public void processNumbers(List<String> strings) {
    strings.stream()  // 简洁：类型安全，无需转换
        .map(String::toUpperCase)
        .forEach(System.out::println);
}
```
