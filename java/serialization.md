# Serialization 序列化

## tl;dr

- 优先使用 `Protocol Buffer` 序列化。
- 谨慎使用 `Java` 原生序列化（`Serializable`接口）
- 谨慎选择 `JSON` 库：禁用 `FastJson`，推荐 `Jackson/Gson`
- 移动端使用 `Proto Lite` 减少包体积

## JSON 的序列化和反序列化

- 禁止使用 `FastJson`。（历史上高危安全漏洞频发，若必须使用需满足：版本≥1.2.83；开启safemode；配置严格白名单）
- 使用 [Jackson](https://github.com/FasterXML/jackson) 或 [gson](https://github.com/google/gson)。
- `Jackson` 除了序列化 JSON 还可以处理其他的数据类型。

强烈建议：新项目禁止引入 `FastJson`，存量系统应逐步迁移至 `Jackson/Gson`。

## `Protobuf` 序列化与反序列化

### `Java Protobuf` 

`Protobuf` 的特殊性质：
- 不可变性
- `equals` 是实质相等
- `hashCode` 是可用的

```java
// 1. 不可变性示例
PersonProto.Person person = PersonProto.Person.newBuilder()
    .setName("Alice")
    .setId(123)
    .build();

// 以下操作将抛出 UnsupportedOperationException
// person.setName("Bob"); 

// 2. 值相等性
PersonProto.Person copy = person.toBuilder().build();
assertTrue(person.equals(copy));  // 内容相等而非引用相等

// 3. 可用 hashCode
Map<PersonProto.Person, String> personMap = new HashMap<>();
personMap.put(person, "value");
assertNotNull(personMap.get(copy));
```

### `Protobuf Any`

`Protobuf Any` 是一种特殊的泛型消息类型，其核心功能是作为一个类型安全的通用容器，用于存储任意序列化的 `Protocol Buffer` 消息。

```java
// Java 使用示例
UserEvent userEvent = UserEvent.newBuilder()
    .setUserId(1001)
    .setAction("login")
    .build();

Event event = Event.newBuilder()
    .setType("user_activity")
    .setPayload(Any.pack(userEvent))
    .build();

// 反序列化时类型检查
if (event.getPayload().is(UserEvent.class)) {
    UserEvent unpacked = event.getPayload().unpack(UserEvent.class);
    System.out.println("User action: " + unpacked.getAction());
}
```

### `Proto Lite`

移动端应该使用 `Proto Lite`。它有更小的生成代码。

```gradle
// build.gradle 配置
dependencies {
    // 完整版 (服务端使用)，以4.32.0举例
    implementation 'com.google.protobuf:protobuf-java:4.32.0'
    
    // Lite版 (移动端使用)，以4.32.0举例
    implementation 'com.google.protobuf:protobuf-javalite:4.32.0'
}
```


## 谨慎使用 Java 原生序列化

Java原生序列化通过实现`Serializable`接口实现对象与字节流的转换，是`JDK`自带的序列化机制。
由于存在反序列化漏洞、隐式`serialVersionUID`兼容性等风险，并且存在序列化效率和无法跨语言使用的问题，建议谨慎使用。
