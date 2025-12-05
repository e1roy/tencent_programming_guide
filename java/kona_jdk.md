# Kona JDK

## tl;dr

- **新项目**：优先选择 JDK 21，次选 JDK 17
- **遗留项目**：JDK 8 → JDK 11 → JDK 17 → JDK 21 渐进升级
- **生产环境**：使用 Kona JDK 获得更好的性能和稳定性

## 概述

Kona JDK 是腾讯基于 OpenJDK 定制的高性能 Java 运行时环境，针对大数据、机器学习和云计算的超大规模工作负载进行了优化。

## 版本选择指南

| 版本 | 适用场景 | 关键特性 | 支持状态 |
|------|----------|----------|----------|
| **JDK 21** | 新项目、云原生应用 | Virtual Threads、Pattern Matching | LTS，推荐 |
| **JDK 17** | 遗留系统升级 | Records、Sealed Classes | LTS，稳定 |
| **JDK 11** | 遗留系统升级 | HTTP Client、Local-Variable Syntax | LTS，维护中 |
| **JDK 8** | 遗留系统 | Lambda、Stream API | 仅维护 |

## 参考资源

- [Tencent/TencentKona-8](https://github.com/Tencent/TencentKona-8)
- [Tencent/TencentKona-11](https://github.com/Tencent/TencentKona-11)
- [Tencent/TencentKona-17](https://github.com/Tencent/TencentKona-17)
- [Tencent/TencentKona-21](https://github.com/Tencent/TencentKona-21)
