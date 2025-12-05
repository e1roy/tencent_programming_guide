# Javadoc 文档

## tl;dr

- 遵守 HTML 格式的 Javadoc 文档风格。
- 使用标准注解为 API 增加属性。

## Javadoc

JavaDoc是 JDK 提供的代码 API 文档生成工具，可以用于生成程序的接口和说明文档，方便开发者和使用者理解和使用程序。

## 格式

注释的格式必须是 `/** */` ，并且注释文本应该使用 HTML 语法进行编辑。注意 `/* */` 和 `//` 格式是用以注释，他们的内容不生成在 Javadoc 中。

在注释文本中我们应该使用HTML标记对文本进行格式化，如 `<p>, <pre>, <ul>, <ol>`等记号，例如：

```java
/**
 * Represents a bazel version. The version format supported is {RELEASE[SUFFIX]}, where:
 *
 * <ul>
 *   <li>{RELEASE} is a sequence of decimal numbers separated by dots;
 *   <li>{SUFFIX} could be: {@code -pre.*}, {@code rc\d+}, or any other string (which compares equal
 *       to SUFFIX is absent)
 * </ul>
 */
@AutoValue
public abstract class BazelVersion {
...
}
```

## 标准标签

Javadoc 支持一系列标准标签，用以标注代码相关的属性。常见的有：

1. `@param`：用于描述方法或构造函数的参数，包括参数的名称和说明。
2. `@return`：用于描述方法或构造函数的返回值，包括返回值的类型和说明。
3. `@throws`：用于描述方法或构造函数可能抛出的异常，包括异常的类型和说明。
4. `@see`：用于连接到另一个类或方法的文档，可以包含类、方法、属性等。
5. `@link`：用于创建指向其他类或方法的链接。
6. `@code`: 用以表明代码块。
7. `@deprecated`：用于指定类、方法或字段已经被弃用，并且不推荐在新代码中使用。

应该**注意**以下要点：

1. `@param @return` 是可选的：如果应该传递什么样的参数、返回的内容非常清晰，那么不需要添加。只要在入参和返回值需要额外说明时，才需要对相应的参数添加说明。
2. `@throws` 是强烈鼓励的：由于不鼓励使用 Checked Exception，而 Unchecked Exception 通常不会在函数签名上体现，所以可能抛出的异常都应该使用 `@throws` 标注。
3. 注意区分 `@link` 与 `@code`： `@link` 是指出代码中类/方法的链接，通常 IDE 支持沿 link 跳转。而 `@code` 是代码块，并不带有跳转语义。
4. 注意区分 `@link` 与超链接：`@link` 只能作为项目内类/方法的链接。普通的 HTTP 超链接需要使用 HTML `href` 标签声明。
5. `@deprecated` 不同于 `@Deprecated` 注解(Annotation)： 后者是真正的带有语义的注解，并且会被 Javac 理解。（例如，调用标注为 `@Deprecated` 的方法会被 Javac 报警），而前者只是文档。因此，如果要 deprecate 一个类/方法，应该使用 `@Deprecated` 注解，并且通常应该使用 `@deprecate` 标签说明该 API 的**替代方案**是什么。

以下是一个完整的例子：https://cs.opensource.google/bazel/bazel/+/master:src/main/java/com/google/devtools/build/lib/actions/Action.java;l=130?q=Action.java&ss=bazel%2Fbazel

```java
/**
 * Executes this action. This method <i>unconditionally does the work of the Action</i>, although
 * it may delegate some of that work to {@link ActionContext} instances obtained from the {@link
 * ActionExecutionContext}, which may in turn perform caching at smaller granularity than an
 * entire action.
 *
 * <p>This method may not be invoked if an equivalent action (as determined by the hashes of the
 * input files, the list of output files, and the action cache key) has been previously executed,
 * possibly on another machine.
 *
 * <p>The framework guarantees that:
 *
 * <ul>
 *   <li>all declared inputs have already been successfully created,
 *   <li>the output directory for each file in <code>getOutputs()</code> has already been created,
 *   <li>this method is only called by at most one thread at a time, but subsequent calls may be
 *       made from different threads,
 *   <li>for shared actions, at most one instance is executed per build.
 * </ul>
 *
 * <p>Multiple instances of the same action implementation may be called in parallel.
 * Implementations must therefore be thread-compatible. Also see the class documentation for
 * additional invariants.
 *
 * <p>Implementations should attempt to detect interrupts, and exit quickly with an {@link
 * InterruptedException}.
 *
 * @param actionExecutionContext services in the scope of the action, like the output and error
 *     streams to use for messages arising during action execution
 * @return returns an ActionResult containing action execution metadata
 * @throws ActionExecutionException if execution fails for any reason
 * @throws InterruptedException if the execution is interrupted
 */
@ConditionallyThreadCompatible
ActionResult execute(ActionExecutionContext actionExecutionContext)
    throws ActionExecutionException, InterruptedException;
```
