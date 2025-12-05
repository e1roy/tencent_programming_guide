# Static Analysis 静态分析检查

## tl;dr

- 鼓励开启静态分析检查

代码规范类 Linters: 组织和团队可根据自身风格偏好设置制定编程规范，并选择性开启对应检测项硬约束团队成员的编程风格，提高整体代码的一致性、可读性、可维护性。

| 应用场景       | 工具          | 能力       | 开启阶段       | 检测规则                                                                 | 修复                               | 链接文档                                                                                                                         |
| -------------- | ------------- | ---------- | -------------- | ------------------------------------------------------------------------ | ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| Java应用       | CheckStyle    | 编程规范   | IDE/precommit  | [CheckStyle规则](https://checkstyle.sourceforge.io/checks.html)         | 借助openrewrite可实现部分规则autofix | [IDEA插件](https://plugins.jetbrains.com/plugin/1065-checkstyle-idea) [vsCode插件](https://marketplace.visualstudio.com/items?itemName=shengchen.vscode-checkstyle) |
| 安卓应用       | AndroidLint   | 编程规范   | IDE/precommit  | [AndroidLint规则](http://googlesamples.github.io/android-custom-lint-rules/checks/index.md.html) | 支持部分规则autofix                | [vsCode插件](https://marketplace.visualstudio.com/items?itemName=AntonyDalmiere.android-support) [Android Studio文档](https://developer.android.com/studio/write/lint?hl=zh-cn) |
| Kotlin应用     | Ktlint        | 编程规范   | IDE/precommit  | [Ktlint规则](https://pinterest.github.io/ktlint/rules/standard/)         | 支持部分规则autofix                | [IDEA配置](https://pinterest.github.io/ktlint/rules/configuration-intellij-idea/) [Android Studio配置](https://thiagolopessilva.medium.com/configuring-and-running-ktlin-on-android-studio-990ce19b50b6) |

- 推荐的静态检查有 [ErrorProne](https://errorprone.info/)
