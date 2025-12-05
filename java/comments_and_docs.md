# Comments & Documentation 注释及文档

## tl;dr

- 文档应该面向使用者，强调如何使用，以及使用的注意事项
- 注释应该面向维护者，强调无法从代码中推断出的内容，例如意图，和注意事项

## 文档：写给使用者

- 例如：标准类 Javadoc 说明，公开函数 Javadoc，成员变量说明
- 需要描述：使用用途，如何正确用，以及有哪些注意事项
- 不建议描述：为什么这样，实现细节
关于如何正确编写 Javadoc ，见 [Javadoc](https://iwiki.woa.com/pages/viewpage.action?pageId=4007320823) 页面。

## 注释：写给维护者

- 例如：类设计注释，函数/代码段实现注释
- 需要描述：描述这里的意图是什么？为什么是这样，这里会受什么限制，有哪些 TODO
- 不建议描述：在代码可直接理解的基础上解释在做什么

注释是以 `/* */` 以及 `//` 编注的内容块。

注释的编写原则：
1. 注释必须要比代码可提供更多的增值信息
2. 优先表达意图和原因，非必要不表达过程步骤

### 正例
```java
/**
 * 工具类：提供字符串相关的功能。
 */
public class StringUtils {

    /**
     * 去除字符串两端的空白字符。
     *
     * @param input 需要处理的原字符串
     * @return 去除头尾空白后的字符串。如果输入为 null，则返回 null。
     * @throws IllegalArgumentException 如果输入字符串长度超过 MAX_LENGTH 则返回异常
     *
     * <p>使用说明：推荐用于用户输入的预处理。</p>
     * <p>注意事项：处理 null 输入不会抛错，但超长字符串会抛 IllegalArgumentException。</p>
     */
    public static String trim(String input) {
        if (input != null && input.length() > MAX_LENGTH ) {
            throw new IllegalArgumentException("字符串太长");
        }
        return input == null ? null : input.trim();
    }
}
```

### 反例
Javadoc 中不需要描述实现细节
```java
public class StringUtils {

    /**
     * 去掉字符串头尾的空格，实现采用了双指针遍历字符串，然后逐步移动指针直到遇到非空格字符为止。
     * 为什么用双指针，是因为这样效率最高。
     *
     * @param input 输入字符串
     * @return 处理后的字符串
     */
    public static String trim(String input) {
        // ... 具体实现
    }
}
```


