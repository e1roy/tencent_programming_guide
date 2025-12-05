# Switch 语句

## tl;dr

- 不要过度使用 `switch`
- 避免滥用表驱动法代替 `switch`
- 合理使用`default`安全网
- 合理使用`switch`表达式简化多场景操作

## 不要过度使用 `switch`
在处理简单的条件逻辑时，`if-else` 语句通常更加直观和灵活。不要为了降低分支复杂度，强行使用 `switch`，反而会更不利于阅读和维护。

### 反例
以下代码基于 `switch` 语句实现 score 得分分类，由于 `switch` 不支持范围比较，因此引入了额外除法计算实现等级分类。
该实现除了可读性问题外，也存在数值风险，不支持处理小于 0 或大于 100 的分数。
```java
String grade;
switch (score / 10) {
  case 10: // fall through
  case 9:
    grade = "A";
    break;
  case 8: // fall through
  case 7: // fall through
    grade = "B";
    break;
  default:
    grade = "C";
    break;
}
```
### 正例
该场景的条件逻辑处理，如下所示，使用 `if-else` 语句更加间接和直观。
```java
String grade;
if (score >= 90) {
  grade = "A";
} else if (score >= 70) {
  grade = "B";
}  else {
  grade = "C";
}
```

## 避免滥用表驱动法代替 `switch`
表驱动（如 `Map` 存储函数）适合于针对一批数据执行同类的动作，其特点是不太关注的数据内容及对应处理逻辑，仅关注这个映射行为。
### 反例
以下代码 使用 `map` 来管理处理逻辑，属于滥用表驱动法来替代 `switch`

```java
Map<String, Runnable> actionMap = new HashMap<>();
actionMap.put("CREATE", () -> onCreate());
actionMap.put("START", () -> onStart());
actionMap.put("RESUME", () -> onResume());
actionMap.put("PAUSE", () -> onPause());
actionMap.put("STOP", () -> onStop());
actionMap.put("DESTROY", () -> onDestroy());
Runnable action = actionMap.get(command);
if (action != null) {
    action.run();
} else {
    onUnknownStatus();
}
```
### 正例
考虑直接使用 `switch` 来表述不同 `status` 下的执行处理逻辑

```java
String status = getStatus();
switch (status) {
    case "CREATE": 
        onCreate(); 
        break;
    case "START": 
        onStart(); 
        break;
    case "RESUME": 
        onResume(); 
        break;
    case "PAUSE": 
        onPause(); 
        break;
    case "STOP":
        onStop(); 
        break;
    case "DESTROY": 
        onDestroy(); 
        break;
    default: 
        onUnknownStatus();
}
```

## 合理使用`default`安全网
在 `switch` 不能穷举的类型场景下且需要保护未知输入时，使用 `default` 完备性兜底
### 正例
在 `String`、`int` 等 `switch` 不能穷举的类型场景下，使用 `default` 兜底
```java
String roleType= ...
switch (roleType) {
    case "ADMIN": 
        showAdminPanel();
        break;
    case "USER": 
        showUserPanel();
        break;
    default:
        throw new IllegalArgumentException("illegal user : " + userRole);
}
```
### 可能的例外考虑：
考虑 `enum` 类型， 假设对应 `enum` 类中添加了新的元素，由于 `default` 安全网保证了编译可成功，很容易在 `switch` 语句中忘记新增对应的 `case` 处理。

## `switch` 表达式简化多场景
`switch` 表达式在 `JDK12` 中以预览版的形式发布，最终在 `JDK14` 中以正式版发布。以下代码展示 `switch` 代码块使用，主要变化包括：
- `switch` 代码块允许出现在了赋值运算符的右侧。
- 支持多场景合并，一个 `case` 语句，可以处理多个类型场景，多个场景之间以逗号,分割。
- 新增 `->` 操作符，操作符右侧可以是表达式、代码块或者异常语句，而不能是其他的形式。
  - 新增 `yield` 关键字，`yield` 语句产生的值可看成是 `switch` 表达式的返回值。

```java
int daysInMonth = switch (month) {
    case Calendar.JANUARY,
        Calendar.MARCH,
        Calendar.MAY,
        Calendar.JULY,
        Calendar.AUGUST,
        Calendar.OCTOBER,
        Calendar.DECEMBER -> 31;
    case Calendar.APRIL,
        Calendar.JUNE,
        Calendar.SEPTEMBER,
        Calendar.NOVEMBER -> 30;
    case Calendar.FEBRUARY -> {
        if (((year % 4 == 0) && !(year % 100 == 0))
            || (year % 400 == 0)) {
            yield 29;
        } else {
            yield 28;
        }
      }
  }
```