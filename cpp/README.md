[TOC]

# 腾讯 C++ 语言编程指南

## 简介
### 目标

本文档是腾讯 C++ 程序员在日常 Code Review 中总结的编程实践集合，展示了在 C++ 编程中常见的问题和推荐方案，用于帮助 C++ 程序员写出更简单、更高效、更易于维护的 C++ 代码。

### 非目标

虽然本文档的部分内容不可避免地会涉及 C++ 语法和 C++ 编码规范，但这不是我们的目标，我们更聚焦在实际业务开发过程中的经验，建议读者在阅读本文档之前先熟悉 C++ 语法和 [C++ 编码规范](https://git.woa.com/standards/cpp)。

### 行文风格

本文不是基于类型、函数、类等层级来组织文档，而是基于编程过程中的常见问题来组织。

### 持续演进

本编程指南无法穷举众多业务日常碰到的所有问题，并且一些存在争议的知识点也未列入。本指南对全公司所有同事开放提 MR 和 issue 的权限，欢迎大家一起持续共建。

## 基本原则

### 更少的代码

更少的代码，带来更少的 bug 和更快的阅读效率。在写代码过程中，我们应该遵循一个原则：“非必要不保留”，能去掉的尽量都去掉，直到不能再精简为止。

反例：

```cpp
class Demo {
 private:
  void DoA();
 private:
  void DoB();
 private:
  void DoC();
  ...
}
```

上述例子中，非必要的写了多个 `private:`，应该去掉。

反例：

```yaml
# yaml 配置文件
prompt_service:
  prompt_service_http:
    prompt_service_http_url: http:xxx
    prompt_service_http_token: xxxx
    # ... 更多配置项
```

上述例子配置文件中，下层级 `key` 命名都带着上层级 `key` 作为前缀，去掉前缀 `key` 不影响功能，但能提高阅读效率，应该精简前缀 `key`。

反例：

```cpp
class KeyValueWrapper {
 public:
  KeyValueWrapper() = default;

  void SetValue(...);
  std::string GetValue(...);
  ...
}
```

上述例子中的默认构造函数可以去掉，无需显式声明。

反例：

```cpp
std::string empty_string = "";
```

上述例子中 `std::string` 的默认构造函数会将字符串置为空字符串，不需要显式地赋值。  

反例：

```cpp
std::string ReadTotalFile() {
  std::ifstream in(file_path.c_str());  // 注：反例
  in.seekg(0, in.end);
  std::string content;
  content.resize(in.tellg());
  in.seekg(0, in.beg);
  in.read(content.data(), content.size());
  in.close();  // 注：反例
  return content;
}
```

上述例子中，有两处错误，首先是构造 `std::ifstream` 对象时，非必要地将 `string` 参数转为 C 格式字符串，然后是 `ifstream` 对象非必要地调用了 `close()` 接口。这里 `std::ifstream` 支持 `std::string` 参数，且其析构函数也会执行 `close()`。  

反例：

```cpp
class Demo {
 private:
  void DoA();
  // void DoB();
  // void DoC();
  // void DoD();
  // void DoE();
  // void DoF();
  ...
}
```

上述例子中，废弃代码直接删除即可，后续如需恢复可通过 git 历史版本查看。


### 最少知识原则

让一个函数的参数类型尽可能的“小”，使得函数里的代码没有机会越界，是内聚设计的一种体现，也让读者阅读代码时，减少知识负担，获得更多的确定性。

反例：

```cpp
// 添加调试信息
void AddDebugInfo(const Context& ctx, const std::string& info) {
  ctx->debug_mgr->Add(info);
}
```

上述例子中，`AddDebugInfo` 函数只使用 `ctx` 的 `debug_mgr` 成员，参数应只传递 `debug_mgr` 对象，无需传递 `ctx` 对象。

### 更多的确定性

除了最少知识原则可以让读者有更多的确定性，在函数定义、类型定义时，也有一些“给读者更多确定性”的注意点。

反例：

```cpp
class BaseWorker {
 public:
  virtual void DoHandle() = 0;
};

class SkitWorker : public BaseWorker {
 public:
  // 缺少 override 关键字，读者无法快速确定这是派生类重写的函数
  void DoHandle() {
    ...
  }
};
```

上述例子中，对于派生类重写的函数，应该加上 `override`。

反例：

```cpp
for (auto& item : values) {
  // 以只读的方式使用 item
}
```

上述例子中，`item` 定义为引用，意味着后续的使用可以是只读，也可以是修改，这有不确定性，在实践中，我们通常这样约束：

- 如果是只读，则定义为 `const auto&`
- 如果要修改，则定义为 `auto&`
- 如果要转移所有权，则定义为 `auto&&`


### 一致性

相似的逻辑采用一致的实现，有利于提升阅读效率，也可以避免困惑。

反例：

```cpp
// 系统开关配置
std::string system_close_cache;
trpc::TrpcConf::LoadSingleKvConfig("rainbow", "core.conf", "close_cache", system_close_cache);
...
// 资源开关配置
std::string res_open_cache;
trpc::TrpcConf::LoadSingleKvConfig("rainbow", "res.conf", "open_cache", res_open_cache);
...
```

上述例子中对系统和资源粒度的 `cache` 控制开关，采用了不同的配置设计，系统开关配置的是“关闭 cache”为 `true` 或者 `false`，资源开关配置的是“打开 cache”为 `true` 或者 `false`。作为相似的开关配置，这里应该采用一致的设计，统一为“open_cache”，否则会带来多余的理解负担。

反例：

```cpp
struct Config {
  ExpireConfig expire_config;  // 过期配置
  ... extra_field; // 提取字段
  ... extra_schema;  // 提取 schema
  ... extra_... // 更多和提取相关的配置信息
  ...
};

struct ExpireConfig {
  // 过期相关的配置
};
```

上述例子中对 `Config` 类的设计没有遵循一致性原则，过期相关的配置抽取到了独立的类中，提取相关的配置也应该同样抽取出来。


### 避免潜规则

代码中的潜规则会影响阅读效率，给后续代码修改埋下隐患，面对潜规则，第一选择是消除潜规则，第二选择是添加注释。

反例：

```cpp
void Worker::Init() {
  query_context_->SetInterfaceName();
  query_context_->Init();
  ...
}

void QueryContext::Init() {
  // 使用 interface_name_ 做一些事情
}
```

上述例子中的 `QueryContext::Init()` 函数依赖 `SetInterfaceName()` 先执行，但从 `Init` 函数命名上看不出来有这层依赖，并且命名为 `Init` 的函数是为对象做初始化，应该是对象构造完成后第一个调用的函数。上述的代码将依赖关系隐藏起来，并且其 `Init` 函数和惯用法不符，在代码的可读性、可维护性上较差。

反例：

```cpp
// 获取 AB 实验命中的实验信息
AbtestDetail GetAbtestPolicy(const std::map<std::string, AbtestDetail>& abtest_instances, const std::set<std::string>& req_bucket_ids) {
  for (const auto& [id, detail]: abtest_instances) {
    if (req_bucket_ids.find(id) != req_bucket_ids.end()) {
      return detail;
    }
  }
}
```

上述例子在判断命中哪个实验时，隐藏着一个判断规则：实验 `ID` 字母序排前面的实验优先判断命中。这个策略如果是合理的，应该增加注释说明。

### 直接的表达

茴字有 N 种写法，实现某个功能的代码也一样，我们建议选择不拐弯抹角，更直接地表达。

反例：

```cpp
if (map.count(key) == 0) {
  // not find
}
```

上述例子用 `count` 来实现元素查找，功能上可行，但理解起来会有多层转换，建议不要这么写，应该更直接地表达，用 `contains` 查找元素（C++20 以前可以使用 `find`）。

反例：

```cpp
if (!plugin) {
  // plugin is nullptr
}
```

上述例子用 `!` 运算符做非空判断，不如用 `if (plugin == nullptr)` 表达直接。

在混合使用 C 语言和 C++ 语言 API 的代码中，使用 `!` 运算符也容易写出错误代码，譬如：

反例：

```cpp
int ret_c = CallCApiReturnZeroMeanSuc();
if (!ret_c) {  // 注：错误写法，且容易让读者误以为是判断失败的分支
  // suc
}

bool ret_cpp = CallCppApiReturnTrueMeanSuc();
if (ret_cpp) {  // 注：正确写法
  // suc
}
```

上述例子对 `ret_c` 的判断写法不合理，应该用 `if (ret_c == 0)` 表达更直接，特别是在 C、C++ 风格 API 混用的场合下，用直接表达的写法，让代码更不易出错。

我们提倡更直接地表达，上述的两个例子都是 if 条件里加了 `== x`，但有些场景也需要避免画蛇添足，譬如：`if (ret_cpp == true)` 这种写法就是不合理的，因为 if 原本的语义就是用来判断 `bool` 变量的，无需再添加 `== true/false`。


## 代码规范

### 代码提交日志内容完整可读

不同团队对代码提交日志有不同的格式要求。譬如，有些团队建议采用[约定式提交](https://www.conventionalcommits.org/zh-hans/v1.0.0/)编写代码提交日志，提交日志必须包括三部分。

- 头部一句话总结，同时要带有 `feat|fix|docs|style|refactor|test|chore` 标签
- 中间详细介绍
- 尾部 tapd story id，关联需求详情

有的团队则要求比较简单，只要有标签、tapd story id、做了什么即可。总的来说，无论是什么样的格式要求，都必须讲清楚做了什么。  

反例：

```text
feat: 重构 rpc 管理器
```

上述例子的提交日志标签用错，重构应该是 refactor，不是 feat。  

反例：

```text
fix: 修复 bug
```

上述例子的提交日志，没有说清楚具体修复了什么 bug。  

除了上述要求之外，我们还建议那些不需要程序员阅读的代码单独提交，并且提交日志或者 MR 标题带有明显标记，譬如：用 `[AutoCode]` 前缀标记那些由 IDL 文件生成的代码（通常不建议提交可以在编译期间生成的代码，但假设你有必须提交的场景）。

### 一条提交日志对应一个功能

代码不是一次成型的，有些开发者会多次提交，最终在主干上会看到多条重复的提交日志，这是不合理的，应该合并为一条提交日志。我们有几种方式可以实现提交日志合并

- 在分支开发阶段，使用 git rebase 命令合并多条日志
- 在分支开发阶段，使用 git commit --amend，将当前的修改合并到上次的提交日志中
- 在分支合并阶段，采用 git squash merge，并编辑提交日志；

反例：

```text
11点30分 提交日志1：
feat: 新增视频排序功能

11点20分 提交日志2：
feat: 新增视频排序功能

11点05分 提交日志3：
feat: 新增视频排序功能
```

上述例子的多行提交日志对应同一个功能“新增视频排序功能”，应该合并为一次提交。

### 代码注释风格一致

项目内的注释应该采用统一的注释风格，一致性包括几个方面：

- 哪些地方需要加注释
- 注释的格式

譬如，有些项目会要求：

- 采用 doxygen 注释风格，便于生成文档
- 文件头采用一致的版权、作者、用途说明
- 头文件的函数、类定义、成员变量、成员函数等都必须有注释
- 中英文混写时，英文前后留/不留空格，需采用一致标准

基于这些要求，正例：

```cpp
// Copyright 2023 Tencent Inc.  All rights reserved.
/**
 * @file data_platform/qbsearch_content_bridge/process/preprocess/douban_data_imputer/douban_data_imputer.h
 * @brief 豆瓣信息补全插件
 */
#pragma once

#include "data_platform/qbsearch_content_bridge/process/preprocess/preprocessor.h"

#include "trpc/client/http/http_service_proxy.h"

namespace data_platform {

class DoubanDataImputer : public Preprocessor {
 private:
  bool DoInit() override;

  bool DoProcess(const MessagePtr& message) override;

  /**
   * @brief 获取豆瓣id
   * @param json_data 消息中的json数据
   * @param id_json_key 豆瓣id在json字符串中的key
   * @param douban_id 豆瓣id
   * @return bool 获取状态
   */
  bool GetDoubanId(const sonic_json::Document& json_data, const std::string& id_json_key, std::string* douban_id);

 private:
  std::shared_ptr<trpc::http::HttpServiceProxy> douban_http_proxy_;  ///< 豆瓣http服务代理
};
}  // namespace data_platform

```

### 注释要完整准确简洁

注释也是一种文档，需要注意基本语法，确保能准确表达，核心三要素：完整、准确、简洁。

反例：

```cpp
/**
 * @brief 添加截断迁所有结果的 debug 信息
*/
```

上述例子注释中有错别字“迁”应是“前”。

反例：

```cpp
  if (recorder_->HasEvent(event_id) || !EVENT_LOCKER->LockEvent(event_id)) {
    // 周期任务遇到事件冲突时，以已执行任务优先，直接跳过当前事件
    return true;
  }
```

上述例子注释表达的信息不完整，而且指代不清，容易有理解困惑：什么是“事件冲突”、具体是什么事件之间发生冲突。结合实际功能，更合理地表达是：如果执行过人工干预事件或者 kafka 增量消息事件，则定期更新任务放弃本次更新。  

反例：

```ini
LAST_FILE_SEQ = 1  # 数据文件根据时间戳倒序排序后, 待去重文件的上一份文件序号为1, 因为待去重数据文件(序号0)一定会在相同目录下
```

上述例子注释内容啰嗦，且容易误导，实际上代码里是根据文件名排序，而文件名是时间戳。建议注释修改为：数据文件按照文件名后缀序号逆序排列后，需要参与新旧去重计算的旧文件序号。

### 常量需要注释

常量数字需要说明为什么是这个数字，以便于读者理解和系统的持续可维护。譬如，通过实验得出的常量，则需要记录实验过程，以便后续环境变化时，维护者能够重新构造该常量；通过经验推导得到常量，则需要介绍经验推导逻辑；如果是通过文档、手册得到的，则需要记录来源。  

反例：

```cpp
static constexpr int kQuHotSignalLevel = 2;
```

上述例子缺少注释，为什么是 2 而不是其他数字，需要做说明。

### 特殊逻辑需要注释

代码应该能自解释，如果因为业务策略不得已写出无法自解释的代码，那么需要给出对应的注释说明。

反例：

```cpp
if (ctx->log.cache_status == ResourceCachestatus::kCacheUpdate) {
    Report(ResourceCachestatus::kCacheOff);
}
```

上述例子缺少注释，`cache_status` 为 `kCacheUpdate` 的时候要上报 `kCacheOff`，这个特殊策略需要做注释说明。

### 关键信息需要注释

在接口和成员变量处，给出关键的注释信息，有利于加快阅读效率。

反例：

```cpp
/**
* @brief 匹配器基类
*/
class MatcherBase {
 public:
  virtual void BuildBm25Factor(uint32_t q_tf, float q_term_weight, float boost);
  ...
 private:
  float bm25_q_part_ = 0;
  std::unordered_map<int, std::string> segment_sources_;
}
```

上述例子的接口和成员变量注释不完整。`BuildBm25Factor` 应该增加函数功能和参数的注释，成员变量 `bm25_q_part_` 和 `segment_sources_` 需要说明其内容和用途。同时 `key-value` 类型的变量，建议采用 `${value}_by_${key}` 的命名风格，做到代码自解释。

### 不要有多余的注释

注释不是越多越好，必须让读者得到价值的，有几种情况不需要注释：

- 无法删掉的废弃代码
- 对代码简单的重复

反例：

```cpp
// xxx.proto

/// @deprecated GUID | QUA | CLIENT_IP | QQ |...
map<string, string> user_info = 3;
```

上述例子的注释不是必要的，既然是废弃的协议字段，描述废弃即可，不需要再描述它之前是干什么的。

反例：

```cpp
TRPC_ASSERT(task_flow);  // 强制检查
```

上述例子的注释不是必要的，函数体内的注释要么是说明 why，要么是做阶段性总结，不应该写 what，what 是对代码内容的重复

### 命名风格一致

项目内的各类命名都应该保持一致，包括文件、变量、函数、类等。老项目建议和原命名风格一致，不要强求采用腾讯编码规范，以免出现长期的代码规范混乱，除非能在较短时间内将代码规范统一起来或者已经代码规范混乱，新项目则要求统一遵循腾讯编码规范。

反例：

```cpp
int count = 0;
auto promise_ptr = std::make_shared<trpc::Promise<trpc::Status>>();
```

上述例子的变量名 promise_ptr 不需要加上类型 ptr。

```cpp
virtual bool Work(const Context& ctx) = 0;
virtual bool GetTestInfo(std::set<std::string>& test_info_) = 0;
```

上述例子的形参名 `test_info_` 应该去掉尾部的下划线。

### 命名简洁准确完整

命名应该简洁、准确、完整，既不要有多余的信息，也不要词不达意，更不能不准确。

反例：

```cpp
void SortPolicyHandler::Process() {
    ctx_->time_performance.SetBegin();
    ...
}
```

上述例子的变量名 `time_performance` 啰嗦且不准确。`time_performance` 翻译过来是：时间性能，这里更准确地用意应该是：时间消耗，因此建议修改为 `time_cost`，命名更短，且表达更准确。

反例：

```cpp
// 数据源配置刷新时间间隔
static constexpr int32_t kConfigReloadInterval = 60;
```

上述例子的常量名 `kConfigReloadInterval` 可以加上 `Second` 变成 `kConfigReloadIntervalSecond`，通过命名就能知道时间的单位。

反例：

```cpp
int i = CountFunction();
int j = SumFunction();
...
```

上述例子的变量名 `i`、`j` 这类极短字符的命名，一般只用在 `for` 循环中，用来定义递增变量，其他地方不应该使用，不利于理解变量用途。

### 避免容易混淆的命名

尽量提高命名的辨识度，减少读者误读的机会。

反例：

```cpp
std::string TransDebugInfoToString(DebugInfo&& debug info);
std::string TransDebugInfosToString(DebugInfo&& debug info);
```

上述例子的函数名`TransDebugInfoToString` 和 `TransDebugInfosToString`，两个长字符串只有中间一个 `s` 字符不同，区分度很低，容易误读，建议修改为：`TransDebugInfoArrayToString`、`TransDebugInfoToString`。

### 项目依赖注意事项

依赖的模块应避免出现不受本项目开发者控制的变更。一方面是更安全，避免受依赖库的不兼容升级影响；另一方面是开发过程中的增量编译更快，不会因依赖仓库升级而导致编译缓存失效。实际操作建议：
- 使用 bazel 和 tag。本项目采用 bazel 编译，依赖模块通过 tag 引入。
- 使用 git 子模块和 commit id。如果无法使用 bazel+tag 模式，也可以采用 git 子模块和 commit id 引入依赖。


## 类和接口

### 避免暴露内部细节

在设计一个类以完成特定功能时，建议提供最小限度的接口，并避免将类的内部信息暴露给使用者。使用者只需看到类提供的功能，而无需了解其内部实现。这有两个原因：

- 减轻使用者的负担：如果使用者需要关注功能的内部实现细节，将增加他们的负担，这不是一个易用的设计。
- 实现细节易变：如果使用者知晓这些细节，就可能依赖它们。后续的实现变更将需要与使用者一同修改，增加改动成本，这不是一个易于修改的设计。

反例：

```cpp
// 银行账号
class BankAccount {
 public:
  std::string account_number;
  std::string account_name;
  double balance = 0.0;

  void Deposit(double amount) {
      balance += amount;
  }

  void Withdraw(double amount) {
      balance -= amount;
  }
};
```

上述例子中，`BankAccount` 类暴露了其内部细节，包括`账户号码（account_number）`、`账户姓名（account_name）`和`余额（balance）`。使用者可以直接访问和修改这些成员变量，而无需通过类提供的函数进行操作。

### 过度的封装

有些一两行代码完成的功能，并且未来不会有新的扩展，就没必要做封装。

反例：

```cpp
double ComputeCosine(const std::vector<float>& v1, const std::vector<float>& v2) {
  double v1_norm = ComputeNorm(v1);
  double v2_norm = ComputeNorm(v2);
  if (fabs(v1_norm) < 1e-6 || fabs(v2_norm) < 1e-6) {
    return 0.0;
  }
  return ComputeDotProduct(v1, v2) / (v1_norm * v2_norm);
}

double ComputeNorm(const std::vector<float>& v) {
  return hnswlib::SpaceNorm::GetInstance()->ComputeNorm(v.data(), v.size());
}
```

上述例子中，`ComputeNorm` 函数内只调用了 `hnsw` 的 `ComputeNorm` 函数，逻辑简单且未来不会扩展，因此这里没有必要封装为函数，直接在 `ComputeCosine` 函数中调用 `hnsw` 的 `ComputeNorm` 即可。

### 类的职责需要清晰

一个类应该只有一个用途，其职责是唯一且清晰的，否则会带来两方面的问题：

- 如果一个类在程序中承担多种功能，那么经过一段时间之后，这个类可能会变得特别巨大，进而影响代码阅读效率和需求迭代速度。
- 如果一个类的职责未有明确的约束，那么在新加代码时便容易陷入纠结：这个代码放在哪里更合适？ 这是可以避免的内耗。

反例：

```cpp
 // 请求上下文管理
 struct SessionContext {
  // 上报请求 trace 日志
  void ReportRequestTrace() {
    std::string report_log = GenerateNoticeInfo();
    WriteLocalLog(report_log);
    GAttaReporter->TraceReport(search_req_->header().request_id(), report_log);
  }


  SearchRequestPtr search_req_;  ///< 请求
  DebugMgr debug_mgr_;  ///< debug 管理
  SliderTimePtr slide_time_;  ///< 耗时滑动窗口
  ...
 };
```

上述例子中，`SessionContext` 的职责不清晰，既作为纯数据类，又带有功能函数，应该将功能函数移除，只用作数据承载。

### 内聚性的插件设计

业务的发展往往难以预判，因此在系统中，我们通常会采用“插件化架构”——当有新功能需要开发时，可以像积木一样自由地插入或移除模块。这样的设计使系统具备良好的扩展性与灵活性。

但要让插件系统真正有效，关键在于“内聚性”。当两个组件经常一起变化时，应将它们放在一起——这就是“内聚”；而将关联不紧密的部分强行组合，则会导致“耦合”。高内聚的设计不仅能提升代码的可读性，还能让修改局限于局部范围，从而加快编译速度。

我们设计插件系统时需要考虑足够的内聚性。

反例：

```cpp
// plugin_factory.h
// 插件工厂
class PluginFactory {
 public:
  PluginFactory() {
    Register("plugin_a", PluginA);
    Register("plugin_b", PluginB);
    ...
  }
};

// plugin_a.h
// 插件A
class PluginA : public PluginBase {...};

// plugin_b.h
// 插件B
class PluginB : public PluginBase {...};
```

上述例子中，当新增一个插件时，不止要写插件代码，还需要修改插件工厂，不够內聚，更好的实现可以做到：当源码加入编译时，插件存在，当源码删除时，插件消失。

修正：

```cpp
// plugin_factory.h
// 插件工厂
class PluginFactory {
 public:
  PluginFactory() {}
};

// 自动注册类，构造函数执行注册
class AutoRegister {
 public:
  AutoRegister(name, builder) {
    PluginFactory->RegisterPlugin(name, builder);
  }
}

// plugin_a.h
// 插件 A
class PluginA : public PluginBase {...};

// plugin_a.cc
// 全局变量，构造函数执行注册
AutoRegister register("plugin_a", PluginA);

// plugin_b.h
// 插件 B
class PluginB : public PluginBase {...};

// plugin_b.cc
// 全局变量，构造函数执行注册
AutoRegister register("plugin_b", PluginB);
```

注：插件 A 和 B 的编译需要加上 `alwayslink = True`

上述修正后的代码，通过全局变量的构造函数，实现插件自注册，也就达到了源码级的插件可插拔。

## 表达式和语句

### 使用 for range 结构化绑定

反例：

```cpp
for (const auto& ins: instances) {
  ins.first...
  ins.second...
}
```

我们建议用 `for range` 代替 `for` 循环，在遇到 `unordered_map`/`map` 时使用结构化绑定。

修正：

```cpp
for (const auto& [sid, plugin]: instances) {
  sid...
  plugin...
}
```

修改后的代码为 first、second 取了更清晰的命名，代码更易读懂。


### 使用 lambda 代替 std::bind

当 `lambda` 和 `std::bind` 都可以实现功能时，推荐使用 `lambda` 来做，可读性更强，这也是《Effective Modern C++》的建议。

反例：

```cpp
trpc::TConfConfig tconf;
tconf.SetAsyCallBack(std::bind(&SortPolicyServer::ReInit, this, std::placeholders::_1));
```

修正：

```cpp
trpc::TConfConfig tconf;
tconf.SetAsyCallBack([this](const std::map<std::string, TConf::ConfigValue>& update_config) {
  SortPolicyServer::ReInit(update_config);
});
```

### 合理使用 auto

`auto` 可以让代码看起来更简洁，但有时候也会给代码的阅读理解带来障碍。使用 `auto` 应该遵循如下原则：

- 能够让代码更易于阅读，并且不会引入多余的拷贝和类型转换等意外代价
- 在判断代码是否更易于阅读时，要假设读者是零背景的新人

正例：

```cpp
std::vector<std::string> something;
for (auto it = something.begin(); it != something.end(); ++it) {
  ...
}
```

上述例子里的迭代器使用了 `auto` 之后，代码显得更简洁。

反例：

```cpp
auto something = Function();
auto somebody = something.Body();
auto ...
```

上述例子中，从上下文中无法得知 `somebody` 是什么类型，但又需要访问其接口函数，这里的 `auto` 会给阅读带来障碍，应该指明具体类型。

## 性能

### 合理使用右值引用和 std::move

右值引用常常和 `std::move` 搭配存在，在定义函数时，需要注意是否适合用右值引用，在调用函数时需要注意是否能用 `std::move`。

反例：

```cpp
std::string TransDebugInfoToString(DebugInfo&& debug_info) {
  std::string ret = debug_info.ToString();
  ...
  return ret;
}
```

上述例子中 `debug_info` 的成员变量没有被转移所有权，设计为右值引用容易误解，也可能给使用者带来不便，定义为 `const&` 更贴切。

反例：

```cpp
void DoSomething(const std::string& info) {
  DoSometingInner(std::move(info));
}
```

上述例子错误地对 `const&` 变量使用 `std::move`，`const&` 对象无法被 `move`，实际上执行的还是拷贝，这里的写法容易误导读者。

反例：

```cpp
Demo DoSomething() {
  Demo demo;
  ...
  return std::move(demo);
}
```

上述例子错误地对返回值使用 `std::move`，编译器会做“返回值优化”（NRVO），在函数调用处原地构造返回对象，而此处的 `std::move` 会破坏 NRVO 优化，反而触发移动拷贝构造函数，降低了性能。

### 使用 emplace、try_emplace、emplace_back

`emplace` 系列接口可以实现原地对象构造，消除掉拷贝构造、移动构造等操作。

反例：

```cpp
std::unordered_map<std::string, Demo> demo_group;
demo_group.insert(std::make_pair(key, Demo(value, i)));  // 案例一
demo_group.emplace(std::make_pair(key, Demo(value, i)));  // 案例二
```

上述例子中的两个插入元素举例，都是不高效的写法，其背后执行相同的计算流程： 首先构造 `Demo` 临时对象，然后用 `std::make_pair` 生成 `pair` 临时对象，最后 `pair` 临时对象移进 `demo_group`，这里在多个技术点上有性能浪费。

首先，有多个临时对象构造、移动构造带来的浪费。`Demo` 临时对象构造完之后，会执行两次 `move` 构造，第一次是生成 `pair` 对象时，第二次是进入 `demo_group` 时。`pair` 临时对象构造后也会执行一次移动构造。

然后，键值对插入失败时，也有临时对象构造的消耗。上述代码会先生成 `pair` 对象，然后在 `pair` 对象插入 `demo_group` 时才去判断是否可插入。

修正：

```cpp
std::unordered_map<std::string, Demo> demo_group;
demo_group.try_emplace(key, value, i);
```

如果插入不成功，则所有临时对象都不会构造；如果插入成功，则只会原地构造一次，不会触发移动构造。上述例子中，如果 Demo 对象不需要在插入时实时构造，则可以改为 `demo_group.emplace(key, demo)` 或者 `demo_group.emplace(key, std::move(demo))`。

反例：

```cpp
std::vector<Demo> demo_group;
demo_group.push_back(Demo(value, 1));  // 案例一
demo_group.emplace_back(Demo(value, 1));  // 案例二
```

上述例子中的两个案例，都是不高效的写法，其背后执行相同的计算流程：首先构造 Demo 临时对象，然后将临时对象移进 demo_group。

修正：

```cpp
std::vector<Demo> demo_group;
demo_group.emplace_back(value, 1);
```



### 合理使用 std::string_view

`string_view` 本质是字符串地址和字符串长度组成的结构体，在字符串分割、基于常量 `char*` 的初始化等场景下非常有价值，应该尽量使用，但也要避免过度使用。

正例：

```cpp
constexpr std::string_view kSomething = "a";
constexpr char kSomething2[] = "b";
constexpr const char* kSomething3 = "c";
void DoSomething(std::string_view info);
...
DoSomething(kSomething);
DoSomething(kSomething2);
DoSomething(kSomething3);
```

上述例子中，三个实参都是常量字符串，此时参数类型用 `string_view` 相比 `const std::string&` 消除了临时 `string` 对象的构造，更高效。

反例：

```cpp
void AddBitsetQuery(std::string_view field, std::string_view term) {
  std::string key = std::string(field) + std::string(term);
  ...
}
...
std::string field = ...;
std::string term = ...;
AddBitsetQuery(field, term);
```

上述例子中调用者的 `field` 和 `term` 是经过一系列处理生成的，`AddBitsetQuery` 的形参定义为 `std::string_view` 相比 `const std::string&` 并没有优势，在函数调用时会触发 `std::string_view` 对象的构造，并传递该对象作为实参。而 `const std::string&` 作为形参，在执行时本质上是一个指针的值传递，`AddBitsetQuery` 函数在获取其字符串内容时相比 `std::string_view` 直接传递地址，会多一次寻址跳转，但相比构造 `std::string_view` 对象，`const std::string&` 还是更划算的。总的来说，如果函数调用传参会导致临时对象构造，则需要慎重，很可能是不值得的。

### 复用已有迭代器

在处理容器时，尽量复用已有的迭代器。

反例：

```cpp
value->emplace(key, info);
std::string& info = value->at(key);
...
```

上述例子中先插入 kv 对，然后再用 k 去查找，是不高效的写法。

修正：

```cpp
auto [it, suc] = value->emplace(key, info);
std::string& info = it->second;
...
```

反例：

```cpp
if (map.find(key) != map.end()) {
  std::string value = map[key];
  ...
}
```

上述代码先用 `find` 查找 `key`，然后再通过 `operator[]` 又找了一次 `key`，是不高效的写法。

修正：

```cpp
auto it = map.find(key);
if (it != map.end()) {
  std::string value = it->second;
  ...
}
```

通常我们都会有意识地避免调用两次 `find` 的重复查找，但像上述两类场景，`find` 隐藏在 `emplace` 和 `operator[]` 背后，有一定的隐蔽性。在某些场景下，这会带来较大的性能损失，譬如：使用 `rapidjson` 库时，如果没有开启使用 `map` 的宏，那么 `FindMember` 函数是通过遍历数组实现的，此时重复查找会带来很大开销。

### 延迟计算

在有分支判断的代码流程中，有部分分支不会执行到，因此部分计算可以延迟到必要的时候才执行，减少无意义的计算。

反例：

```cpp
void Run() {
  auto task = std::make_shared<Task>();
  task->SetName(process_name);
  if (!task_flow->Exists(process_name)) {
    return;
  }
  // do something with task
  ...
}
```

上述例子中 `task` 对象的构造和设置可以延迟到判断语句之后。

修正：

```cpp
void Run() {
  if (!task_flow->Exists(process_name)) {
    return;
  }

  auto task = std::make_shared<Task>();
  task->SetName(process_name);
  // do something with task
  ...
}
```

### 提早计算

有延迟计算，相应也有提早计算。在一个需要反复执行的函数中，有部分计算逻辑用于产出多次执行都不会有变化的信息，则这些信息可以提早计算，减少反复执行时的重复运算。

反例：

```cpp
void Worker::RequestHandle(const Task& task) {
  auto graph = BuildExecuteGraph(process_config);  // 使用进程级配置构造任务执行流程图（DAG）
  ExecuteGraph(graph, task);  // 执行流程图
  ...
}
```

上述例子中，`RequestHandle` 是后台服务请求接口的响应函数，每一个请求都会触发一次 `RequestHandle` 函数调用。`BuildExecuteGraph` 函数是基于进程级配置构造执行流程图，只要配置相同，多次调用 `BuildExecuteGraph` 产出的 `graph` 对象都是一样的，因此没有必要每一个请求都去构造流程图，再考虑到 `BuildExecuteGraph` 可能有高耗时计算，因此这个函数适合放在 `Worker` 对象构造函数中执行。

修正：

```cpp
Worker:Worker() {
  graph_ = BuildExecuteGraph(process_config);  // 使用进程级配置构造任务执行流程图（DAG）
}

void Worker::RequestHandle(const Task& task) {
  ExecuteGraph(graph_, task);  // 执行流程图
  ...
}
```

### 减少对象的隐藏拷贝

非必要的对象拷贝是很常见的性能浪费，并且有些时候拷贝是隐藏在背后发生的，不容易发现。比较常见的是函数参数类型定义不合理，引发对象拷贝。

反例：

```cpp
void DoSomething(std::string info) {
  // do something with info string
}
```

上述例子中，很明显 `info` 参数在传参时会触发拷贝，可以修改为 `const&`。有些拷贝会很隐蔽，譬如下面不合理使用 `std::vector` 带来隐藏的对象拷贝。

反例：

```cpp
int main() {
  std::vector<Demo> demos;
  demos.emplace_back("a");
  demos.emplace_back("b");
  demos.emplace_back("c");
  demos.emplace_back("d");
  ...
  std::stable_sort(demos.begin(), demos.end(), [](const Demo& a, const Demo& b) -> bool { return a.info_ < b.info_; });
}
```

上述例子中，有两处地方会触发对象拷贝，第一处是 `std::vector<Demo>` 容器扩容时，第二处是 `std::stable_sort` 时：

- 使用 `vector` 时，如果可以预先知道容器元素个数，应该先用预留空间，然后再插入元素，消除容器扩容。
- 在对 `vector` 做排序时，考虑到数组排序会引发大量的元素移动，应该想办法避免，譬如考虑换成使用 `map`。

修正如下：

```cpp
int main() {
  std::map<std::string, Demo> demos;
  demos.emplace("a", demo_a);
  demos.emplace("b", demo_b);
  demos.emplace("c", demo_c);
  demos.emplace("d", demo_d);
  ...
}
```

修正代码使用 `map` 替换 `vector`，元素在插入时保持有序，不需要再执行排序环节，也就消除了排序带来的隐藏拷贝。隐藏拷贝有时候也会在多个函数的协作场景下发生。

反例：

```cpp
// Factory class
std::string Factory::GetTypeName() {
  return type_name_;  // type_name_ 是成员变量
}

// User class
void User::DoSomething() {
  Factory factory;
  std::string type_name = factory.GetTypeName();
  // type_name 后续只有只读应用
  ...
}
```

上述例子的 `DoSomething` 函数中，`factory` 变量的生命周期不短于使用者函数，因此 `GetTypeName()` 函数可以设计为返回 `const&`，使得函数调用者的 `type_name` 变量也能定义为 `const&`，进而消除字符串拷贝。

减少对象的隐藏拷贝是知识点很广的话题，除了上述的三类例子，前面提到的 C++ `emplace` 系列语法也是为了消除隐藏的对象拷贝。

### 非必要的防御

通常我们写代码会很小心，甚至有时候会小心过头，譬如没有从全局考虑，在一系列函数的执行流程中，每一个函数内部都加上防御判断，显得繁琐又低效。通常有一个原则：只判断一次。譬如：如果一个成员变量是类的关键成员变量，那么其有效性应该在对象构造或其他类似时机做判断，不应该在后续多个函数中重复判断。

反例：

```cpp
using ConfigPtr = std::shared_ptr<Config>;

void Handle(const Context& ctx) {
  ConfigPtr config = GetConfig();
  if (config == nullptr) {
    return;
  }
  CreateTask(ctx, config);
}

void CreateTask(const Context& ctx, const ConfigPtr& config) {
  if (config == nullptr) {
    ...
  }
  ...
}
```

上述例子中，对 `config` 做了两次判空，是有冗余的，应该在获取到 `config` 的地方做一次判断即可。  
另外，当你在使用“只判断一次”规则时，也需要注意防范潜在的风险：函数的调用者和使用者是否有可能各自独立演进，而导致缺失防御？当你不能确信这是多余的判断时，建议遵循“防御编程”，都加上判断，确保程序健壮。

### 进行 cache 友好的内存访问

数据读取效率对程序性能很重要，我们建议在读取数据时采用符合“局部性原理”的方式，譬如：对数组的访问，推荐使用连续读取，避免跳跃读取。

示例

```cpp
int matrix[rows][cols];

// 不好
for (int col = 0; col < cols; ++col)
    for (int row = 0; row < rows; ++row)
        sum += matrix[row][col];

// 好
for (int row = 0; row < rows; ++row)
    for (int col = 0; col < cols; ++col)
        sum += matrix[row][col];
```

### 使用 unordered_map 代替 map

`unordered_map` 是 `C++11` 新引入的 `key-value` 容器，在多数评测下，其平均查找性能都高于 `map`，建议尽量采用 `unordered_map`，除非有以下情况：

- 有对元素按顺序遍历的诉求
- 更关注内存占用，而非读写性能
- 业务场景下的评测发现 `map` 性能更好
 
总的来说，我们建议用 unordered_map，但如果你的业务场景有特殊诉求，应该遵循相关场景下的规范或建议。譬如 `chromium` 就建议大多数场景用 `map` 即可：[map-and-set-selection](https://chromium.googlesource.com/chromium/src/base/+/refs/heads/main/containers/README.md#map-and-set-selection)。

## 并发

并发是现代编程中不可或缺的一部分，它允许多个任务同时执行，从而显著提高程序的吞吐量和响应速度。然而，不良的并发设计（如数据竞争、死锁或过度同步）可能导致严重的性能问题，甚至程序崩溃。因此，理解并正确使用并发工具（如线程、锁和原子操作）是编写高效、可靠程序的关键。

### 优先使用 `std::thread` 和 `std::async` 代替原生线程 API

C++11 之后提供了 `std::thread` 和 `std::async` 等高级并发工具，相比原生线程 API（如 `pthread`），它们更易于使用且不易出错。`std::async` 还能自动管理线程生命周期，避免资源泄漏。

反例：

```cpp
#include <pthread.h>

void* ThreadFunc(void* arg) {
  // 线程逻辑
  return nullptr;
}

int main() {
  pthread_t thread;
  pthread_create(&thread, nullptr, ThreadFunc, nullptr);
  pthread_join(thread, nullptr);
}
```

修正：

```cpp
#include <thread>
#include <future>

void ThreadFunc() {
  // 线程逻辑
}

int main() {
  std::thread t(ThreadFunc);
  t.join();

  // 或者使用 std::async
  auto future = std::async(std::launch::async, ThreadFunc);
  future.get();
}
```

### 使用 `std::jthread` 管理线程生命周期（C++20）

C++20 引入了 `std::jthread`，它是 `std::thread` 的改进版本，主要优势在于析构时会自动调用 `join()`，避免了因忘记调用 `join()` 或 `detach()` 导致的资源泄漏问题。

（1）基本用法
```cpp
#include <thread>
#include <iostream>

void ThreadFunc() {
  std::cout << "线程执行中...\n";
  std::this_thread::sleep_for(std::chrono::seconds(1));
  std::cout << "线程结束\n";
}

int main() {
  std::jthread t(ThreadFunc); // 自动管理线程生命周期
  // 无需显式调用 t.join()
  return 0;
}
```

（2）与 `std::thread` 的对比
- **自动析构**：`std::jthread` 在析构时会自动调用 `join()`，而 `std::thread` 必须手动调用 `join()` 或 `detach()`，否则会引发 `std::terminate`。
- **中断支持**：`std::jthread` 支持通过 `request_stop()` 请求线程停止，适用于协作式线程取消。

（3）适用场景
- 需要确保线程安全退出的场景。
- 协作式线程取消的场景（结合 `std::stop_token`）。

（4）注意事项
- `std::jthread` 是 C++20 新增特性，需确保编译环境支持。
- 如果线程需要长时间运行，仍需确保逻辑正确性，避免资源泄漏。

### 使用 `std::latch` 实现多线程同步（C++20）

`std::latch` 是一种轻量级的同步原语，允许一个或多个线程等待，直到计数器减为零。它适用于一次性同步场景。

（1）基本用法
```cpp
#include <latch>
#include <thread>
#include <vector>
#include <iostream>

void Worker(std::latch& latch, int id) {
  std::cout << "线程 " << id << " 开始工作\n";
  std::this_thread::sleep_for(std::chrono::seconds(1));
  std::cout << "线程 " << id << " 完成工作\n";
  latch.count_down(); // 计数器减一
}

int main() {
  const int num_threads = 3;
  std::latch latch(num_threads); // 初始化计数器为线程数
  std::vector<std::thread> threads;

  for (int i = 0; i < num_threads; ++i) {
    threads.emplace_back(Worker, std::ref(latch), i);
  }

  latch.wait(); // 等待计数器减为零
  std::cout << "所有线程已完成工作\n";

  for (auto& t : threads) {
    t.join();
  }
  return 0;
}
```

（2）适用场景
- 等待多个线程完成初始化任务。
- 多阶段任务中的同步点。

### 使用 `std::barrier` 实现多阶段同步（C++20）

`std::barrier` 是一种更灵活的同步原语，允许多个线程在多个阶段中同步。每个阶段完成后，所有线程会继续执行下一阶段。

（1）基本用法
```cpp
#include <barrier>
#include <thread>
#include <vector>
#include <iostream>

void PhaseWorker(std::barrier<>& barrier, int id) {
  std::cout << "线程 " << id << " 完成阶段1\n";
  barrier.arrive_and_wait(); // 同步点1

  std::cout << "线程 " << id << " 完成阶段2\n";
  barrier.arrive_and_wait(); // 同步点2

  std::cout << "线程 " << id << " 完成阶段3\n";
}

int main() {
  const int num_threads = 3;
  std::barrier barrier(num_threads);
  std::vector<std::thread> threads;

  for (int i = 0; i < num_threads; ++i) {
    threads.emplace_back(PhaseWorker, std::ref(barrier), i);
  }

  for (auto& t : threads) {
    t.join();
  }
  return 0;
}
```

（2）适用场景
- 多阶段并行算法（如并行排序）。
- 需要分阶段同步的多线程任务。

（3）注意事项
- `std::latch` 和 `std::barrier` 是 C++20 新增特性，需确保编译环境支持。
- `std::barrier` 的计数器在构造时固定，不可动态调整。

### 使用 `std::mutex` 和 `std::lock_guard` 管理线程安全

多线程环境下，共享数据的访问必须通过锁机制保护。推荐使用 `std::lock_guard` 或 `std::unique_lock`，它们通过 RAII 机制自动释放锁，避免忘记解锁导致的死锁问题。

反例：

```cpp
std::mutex mtx;
int shared_data = 0;

void UnsafeIncrement() {
  mtx.lock();
  shared_data++;
  // 如果此处抛出异常，锁不会被释放
  mtx.unlock();
}
```

修正：

```cpp
void SafeIncrement() {
  std::lock_guard<std::mutex> lock(mtx);
  shared_data++;
  // 锁在作用域结束时自动释放
}
```

### 使用原子操作避免数据竞争

对于简单的共享变量，优先使用 `std::atomic` 代替锁机制。原子操作性能更高且能避免锁的开销，但仅适用于简单的读写场景。

反例：

```cpp
int counter = 0;
std::mutex mtx;

void Increment() {
  std::lock_guard<std::mutex> lock(mtx);
  counter++;
}
```

修正：

```cpp
std::atomic<int> counter(0);

void Increment() {
  counter++;
}
```

### 使用 `std::atomic_ref` 包装非原子对象

C++20 对原子操作进行了扩展，新增了 `std::atomic_ref` 和 `wait`/`notify` API，提供了更灵活的原子操作方式。

`std::atomic_ref` 允许对非原子对象进行原子操作，适用于无法直接修改为原子类型的场景。

（1）基本用法
```cpp
#include <atomic>
#include <thread>
#include <iostream>

int main() {
  int non_atomic_value = 0;
  std::atomic_ref<int> atomic_value(non_atomic_value);

  std::thread t1([&atomic_value] {
    for (int i = 0; i < 1000; ++i) {
      atomic_value.fetch_add(1, std::memory_order_relaxed);
    }
  });

  std::thread t2([&atomic_value] {
    for (int i = 0; i < 1000; ++i) {
      atomic_value.fetch_add(1, std::memory_order_relaxed);
    }
  });

  t1.join();
  t2.join();

  std::cout << "Final value: " << non_atomic_value << std::endl; // 输出 2000
  return 0;
}
```

（2）适用场景
- 对现有非原子变量临时启用原子操作。
- 无法直接修改为原子类型的场景（如第三方库中的变量）。

### 使用 `wait` 和 `notify` 实现原子等待

C++20 新增了 `wait`/`notify` API，允许线程在原子变量上等待和通知，类似于条件变量但更轻量。

（1）基本用法
```cpp
#include <atomic>
#include <thread>
#include <iostream>

int main() {
  std::atomic<bool> ready(false);

  std::thread worker([&ready] {
    std::cout << "Worker 开始等待...\n";
    ready.wait(false); // 等待 ready 变为 true
    std::cout << "Worker 检测到 ready 为 true\n";
  });

  std::this_thread::sleep_for(std::chrono::seconds(1));
  ready.store(true);
  ready.notify_one(); // 通知等待的线程

  worker.join();
  return 0;
}
```

（2）适用场景
- 轻量级的线程同步，避免条件变量的开销。
- 简单的生产者-消费者模型。

（3）注意事项
- `wait`/`notify` 是 C++20 新增特性，需确保编译环境支持。
- 相比条件变量，`wait`/`notify` 更轻量，但功能也更简单。


### 使用条件变量实现线程间通信

`std::condition_variable` 允许线程在特定条件下等待或唤醒其他线程，是实现生产者-消费者模式的高效工具。注意搭配 `std::unique_lock` 使用。

正例：

```cpp
std::mutex mtx;
std::condition_variable cv;
bool ready = false;

void Producer() {
  std::this_thread::sleep_for(std::chrono::seconds(1));
  {
    std::lock_guard<std::mutex> lock(mtx);
    ready = true;
  }
  cv.notify_one();
}

void Consumer() {
  std::unique_lock<std::mutex> lock(mtx);
  cv.wait(lock, [] { return ready; });
  // 条件满足后继续执行
}
```


### 使用循环检查避免条件变量虚假唤醒

条件变量的唤醒可能是虚假的（spurious wakeup），因此在等待条件变量时，必须使用循环检查条件是否满足。
[spurious wakeup解释](https://en.wikipedia.org/wiki/Spurious_wakeup)

反例：

```cpp
std::unique_lock<std::mutex> lock(mtx);
if (!ready) {
  cv.wait(lock);  // 可能虚假唤醒
}
```

修正：

```cpp
std::unique_lock<std::mutex> lock(mtx);
while (!ready) {
  cv.wait(lock);  // 循环检查条件
}
```

### 使用线程局部存储代替全局变量

全局变量在多线程环境下容易引发问题。如果必须使用，可以通过 `thread_local` 关键字声明线程局部变量，确保每个线程有独立的副本。

反例：

```cpp
int global_counter = 0;

void increment() {
  global_counter++;  // 多线程访问不安全
}
```

修正：

```cpp
thread_local int thread_counter = 0;

void increment() {
  thread_counter++;  // 每个线程有独立副本
}
```

### 合理设置线程数量避免并发过载

线程数量过多会导致上下文切换开销增加。建议根据硬件并发能力（如 `std::thread::hardware_concurrency()`）动态调整线程池大小。

正例：

```cpp
unsigned int num_threads = std::thread::hardware_concurrency();
std::vector<std::thread> threads(num_threads);

for (auto& t : threads) {
  t = std::thread([] {
    // 任务逻辑
  });
}
for (auto& t : threads) {
  t.join();
}
```

### 简单等待异步任务完成的场景可以考虑用 promise-future 代替条件变量

后台程序经常需要在工作线程里定期从外部存储加载数据，这里“定期”最差的做法是用 `sleep`，这会阻塞到进程退出。C++11 之前最佳的做法是使用带有条件变量的 `wait`，当进程退出时，可以激活条件变量，让 `wait` 及时得到通知而退出，这就要求有条件变量和锁，略复杂。现代 C++ 可以使用 `promise-future`，更简单易懂。

反例：

```cpp
void WorkThreadFunction() {
  while (true) {
    LoadData();
    sleep(30);
  }
}
```

上述例子中，为实现 30 秒定期加载数据，在加载数据工作线程中采用了睡眠 30 秒的方式，这是最差的做法，会阻塞进程退出。

使用条件变量：

```cpp
std::mutex mutex;
std::condition_variable cv;
...
void WorkThreadFunction() {
  while (true) {
    LoadData();
    std::unique_lock locker(mutex);
    if (cv.wait_for(locker, std::chrono::seconds(30)) != std::cv_status::timeout) {
      break;
    }
  }
}

void ProcessExit() {
  std::unique_lock locker(mutex);
  cv.notify_all();
}
```

上述例子是 30 秒定期加载数据的条件变量实现方案，在工作线程的循环中使用条件变量的 `wait_for` 接口，同时在进程退出时触发条件变量信号，最终可以实现条件触发和定期触发。这是很传统的方案，有较多的代码，在现代 C++ 标准下，我们可以更优雅地实现。

使用 `promise-future`：

```cpp

std::promise<void> promise;
std::future<void> future = promise.get_future();
...

void WorkThreadFunction() {
  while (true) {
    LoadData();
    if (future.wait_for(std::chrono::seconds(30)) == std::future_status::ready) {
      break;
    }
  }
});

void ProcessExit() {
  promise.set_value();
}
```

`promise-future` 在单次通知的场景上，相比使用条件变量更简单。  
另外，如果使用了 `trpc-cpp` 框架，定期加载数据可以直接用框架提供的定时任务，譬如：

```cpp
trpc::PeripheryTaskScheduler::GetInstance()->SubmitPeriodicalTask([this]() { LoadData(); }, load_interval_ms_);
```

另外也需要注意，`promise-future` 不能在所有场景下代替条件变量：

- `promise` 不允许多次调用 `set_value()`，所以上面示例中的 `ProcessExit` 函数只能调用一次，多次调用时会抛出异常，条件变量则可以多次通知和等待。
- 条件变量在 `wait` 系列函数成功返回后会重置信号，`future` 则会一直保持 “have value” 的状态，所以其行为是不一致的，`promise-future` 只能用于处理类似 “退出循环” 这个单次通知的场景，而条件变量写法则通用得多且具备更好的扩展性。比如多次通知工作进程，实现一个线程安全的阻塞队列等。
- 低版本的 GCC（4.8 及以下），`promise-future` 的标准库实现有 bug：
  - https://github.com/open-telemetry/opentelemetry-cpp/issues/2982
  - https://gcc.gnu.org/bugzilla/show_bug.cgi?id=54297
  - https://stackoverflow.com/questions/28604461/using-c11-futures-nested-calls-of-stdasync-crash-compiler-standard-library

### 进程退出时应主动停止多线程

我们经常会使用多线程来处理一些异步的计算任务、IO 任务，多线程通常封装在类中，并使用 `RAII` 的思想来实现线程关闭和资源释放。这些类应该提供一个 Stop 函数，用于进程退出时被调用，而不要依赖单实例对象的析构来退出工作线程，因为这会导致多个工作线程串行退出，进而拖慢进程整体退出速度。

例子：

```cpp
class WorkerWrapper {
 public:
  WorkerWrapper() : thread_([this] { Work(); }) {}
  ~WorkerWrapper() {
    stop_ = true;
    thread_.join();
  }

  void Stop() { stop_ = true; }

  void Work() {
    while (!stop_) {
      // 工作线程做一些循环执行的工作
      ...
    }
  }

 private:
  bool stop_ = false;
  std::thread thread_;
};

int main() {
  std::vector<WorkerWrapper> workers(10);  // 模拟 10 个工作线程

  // 模拟主线程做一些其他事情
  std::this_thread::sleep_for(std::chrono::seconds(3));

  // 注意：主动通知停止
  for (auto& worker : workers) {
    worker.Stop();
  }
}
```

上述例子模拟多线程退出场景，在进程退出时如果没有主动通知多线程退出，则 10 个工作线程会在 `workers` 对象析构时逐个元素析构触发串行退出，会较长时间的阻塞进程退出。另外，使用 `trpc-cpp` 框架业务也可以考虑使用定时任务功能：`SubmitPeriodicalTask` 代替工作线程。

### 注意多线程场景下变量的生命周期

当我们写简单的串行代码时，通常会注意到变量的生命周期，并避免犯错，譬如：不返回局部变量的地址。但当我们在写多线程程序，并叠加上 `lambda` 语法时，则很容易忽略变量的生命周期，而出现野指针访问。

反例：

```cpp
void DoSomethingAsync() {
  std::string info = "some information";
  std::thread worker([&info] {
    std::this_thread::sleep_for(std::chrono::seconds(1));
    std::cout << info << std::endl;
  });
}
```

上述例子会出现 `coredump`，因为 `info` 是 `lambda` 引用捕获，引用本质上是地址，当 `DoSomethingAsync` 函数执行完时，`info` 对象被析构，而地址还被工作线程拿着并访问。这个例子较容易看出来问题，如果把这个例子的工作线程修改为 `RPC` 调用的异步回包响应，则会更具隐蔽性。

反例：

```cpp
std::string running_info = ...;
...
task_processer->Process(ctx).Then([this, &running_info, &ctx](trpc::Future<>&& fu){...});
```

上述例子和 RPC 的回调交织在一起，野指针问题具有隐蔽性。
多线程下访问有生命周期安全风险的变量，通常有几种解法：

- 将需要跨线程访问的变量定义为长生命周期变量，譬如：全局变量、某个长生命周期对象的成员变量
- 拷贝需要跨线程访问的变量，为每一个跨线程访问者都拷贝一份该变量的副本
- 将需要跨线程访问的变量定义为智能指针，并为每一个跨线程访问者拷贝一份智能指针对象的副本

这几种方式各有优缺点，长生命周期变量需要做好设计；全局变量有可读性减分和析构顺序不可控的隐患；拷贝变量需要付出性能成本；智能指针会有析构时机不可控的代价，总之，没有免费的午餐，在实际应用中，应选择业务代价最小的方案。


## 资源管理\[1\]

资源，是指任何必须先获取、后（显式或隐式）释放的东西，例如内存、文件句柄、套接字和锁。资源必须释放的原因通常是其供给可能有限，因此即便延迟释放也可能造成不良影响。
资源管理的根本目标是确保：一、不发生任何资源泄漏；二、持有资源的时间不超过实际所需。负责释放某一资源的实体被称为 “所有者”。

在少数情况下，资源泄漏可能是可接受的，甚至是最优选择。
例如，若你编写的程序仅根据输入生成输出，且所需内存量与输入大小成比例，那么（从性能和编程便捷性角度出发）最优策略有时就是完全不释放任何内容。只要你的内存足以处理最大规模的输入，即便发生泄漏也无妨，但务必确保在判断失误时能输出清晰的错误提示。本文将暂不讨论此类特殊情况。

### 使用RAII（资源获取即初始化）和资源句柄自动管理资源

RAII：是 C++ 中管理资源的核心思想，其本质是利用对象的生命周期（创建时初始化，销毁时自动执行析构）来绑定资源的 “获取” 与 “释放”，从而避免因忘记手动释放、异常跳转等情况导致的资源泄漏。
资源句柄（Resource Handle）：通常指封装了资源的对象（如 C++ 标准库中的std::unique_ptr、std::shared_ptr、std::fstream等），通过操作句柄来间接管理资源，而非直接操作底层资源（如原始指针、文件描述符），是实现 RAII 的常见方式。

为避免资源泄漏以及手动管理资源带来的复杂性。C++ 语言强制要求的构造函数 / 析构函数对称性，与资源获取 / 释放函数对（如 fopen/fclose、lock/unlock、new/delete）固有的对称性相契合。无论何时，当你需要处理某类资源（这类资源需要成对调用 “获取 / 释放” 函数）都应将该资源封装到一个对象中，由这个对象为你强制实现 “获取 / 释放” 的配对：在对象的构造函数中获取资源，在对象的析构函数中释放资源。

反例：

```cpp
void Send(X* x, string_view destination) {
  auto port = open_port(destination);
  my_mutex.lock();
  // ...
  send(port, x);
  // ...
  my_mutex.unlock();
  close_port(port);
  delete x;
}
```

在这段代码中，你必须确保在所有执行路径上都记得调用 unlock（解锁）、close_port（关闭端口）和 delete（释放内存），并且每个操作都要恰好执行一次。此外，若标记为 “...” 的任意一段代码抛出异常，那么 x（所指向的资源）会发生泄漏，且 my_mutex（互斥锁）会保持锁定状态。

修正：

```cpp
void Send(std::unique_ptr<X> x, std::string_view destination) { // x 拥有X对象的所有权
  Port port{destination};                  // port 拥有PortHandle的所有权
  std::lock_guard<mutex> guard{my_mutex};  // guard 拥有锁的所有权
  // ...
  send(port, x);
  // ...
} // 自动解锁 my_mutex 并释放 x 中指针所指向的内存

class Port {
 public:
  Port(std::string_view destination) : port_{open_port(destination)} { }
  ~Port() { close_port(port_); }
  operator PortHandle() { return port_; }

  // 端口句柄通常无法克隆，因此应禁用复制和赋值操作
  Port(const Port&) = delete;
  Port& operator=(const Port&) = delete;
 private:
  PortHandle port_;
};
```

现在所有资源的清理都实现了自动化，无论是否发生异常，都会在所有执行路径上执行一次清理操作。此外，该函数现在明确表明其会接管该指针的所有权。

### 使用 std::unique_ptr 或 std::shared_ptr 管理资源

使用 std::unique_ptr 或 std::shared_ptr 能够防止资源泄漏。

示例：

```cpp
void f()
{
    X* p1 { new X };                   // 不良写法，p1 指向的资源会泄漏
    auto p2 = std::make_unique<X>();   // 良好写法，独占所有权
    auto p3 = std::make_shared<X>();   // 良好写法，共享所有权
}
```

### 优先使用 std::unique_ptr 而非 std::shared_ptr

当选择智能指针时，除了确实需要共享所有权的场景外，应该优先使用 std::unique_ptr。std::unique_ptr 在概念上更简洁、可预测性更强（你能明确知道析构何时发生），且效率更高（无需隐式维护引用计数）。

反例：

```cpp
void f()
{
    std::shared_ptr<Base> base = std::make_shared<Derived>();
    // 在本地使用 base，未对其进行拷贝——引用计数始终不会超过 1
} // 销毁 base
```

修正：

```cpp
void f() {
  unique_ptr<Base> base = make_unique<Derived>();
  // 在本地使用 base
} // 销毁 base
```
当调用侧确实需要共享所有权时，返回的 std::unique_ptr 也支持被移动到 std::shared_ptr 中。

### 使用 std::make_unique() 创建 std::unique_ptr

std::make_unique 能更简洁地表达构造意图。此外，在 C++17 之前的代码中，它还能确保复杂表达式中的异常安全性。

示例：

```cpp
std::unique_ptr<Foo> p {new Foo{7}};    // 可行，但存在重复代码
auto q = std::make_unique<Foo>(7);      // 更优：无 Foo 的重复书写
```

### 使用 std::unique_ptr<Widget> 参数表示函数接管 Widget 的所有权

通过这种方式使用 std::unique_ptr，既能文档化（明确表明意图）又能强制实施函数调用时的所有权转移。

示例：

```cpp
void Sink(unique_ptr<Widget>); // 接收 Widget 的所有权

void Uses(Widget*);            // 仅使用 Widget，不接管所有权
```

### 使用 std::unique_ptr<Widget>& 参数表示函数会重新绑定 Widget

通过这种方式使用 std::unique_ptr，既能文档化（明确表明意图）又能强制实施函数调用时的重新绑定语义。
重新绑定是指 “使指针或智能指针指向另一个对象”。

示例：

```cpp
void Reseat(std::unique_ptr<Widget>&); // “将会”或“可能会”重新绑定指针
```

### 使用 std::make_shared() 创建 std::shared_ptr

std::make_shared 能更简洁地表达构造意图。它还提供了一个优化机会：通过将 std::shared_ptr 的引用计数与所指向的对象放置在同一块内存中，省去单独为引用计数分配内存的操作。此外，在 C++17 之前的代码中，它还能确保复杂表达式中的异常安全性。

示例：

```cpp
shared_ptr<X> p1 { new X{2} }; // 不良写法
auto p = std::make_shared<X>(2);    // 良好写法
```

make_shared() 版本仅提及一次 X，因此通常比显式使用 new 的版本更简洁（同时效率也更高）。

### 使用 std::shared_ptr<Widget> 参数表示共享所有权

这使得函数的所有权共享意图变得明确。

示例：

```cpp
class WidgetUser {
 public:
  // WidgetUser 将与其他对象共享 Widget 的所有权
  explicit WidgetUser(std::shared_ptr<Widget> w) noexcept
    : widget_{std::move(w)} {}
  // ...
 private:
  std::shared_ptr<Widget> widget_;
};
```

### 使用 std::shared_ptr<Widget>& 参数表示函数可能会重新绑定该共享指针

这使得函数的重新绑定意图变得明确。

示例：

```cpp
void ChangeWidget(std::shared_ptr<Widget>& w) {
  // 这会改变调用者的 Widget
  w = std::make_shared<Widget>(Widget{});
}
```

### 使用 const std::shared_ptr<Widget>& 参数表示该函数可能会增加对对象的引用计数

推荐的写法：

```cpp
void Share(std::shared_ptr<Widget>);            // 共享——"将会"增加引用计数

void Reseat(std::shared_ptr<Widget>&);          // "可能会"重新绑定指针

void MayShare(const std::shared_ptr<Widget>&);  // "可能会"增加引用计数
```

### 使用 std::weak_ptr 打破 shared_ptr 的循环引用

std::shared_ptr 依赖引用计数实现资源管理，而循环引用结构的引用计数永远无法降至零，因此我们需要一种机制来销毁这类循环结构。

示例：

```cpp
#include <memory>

class Bar; // 前向声明

class Foo {
 public:
  // 显式构造函数，接收指向 Bar 的 shared_ptr
  explicit Foo(const std::shared_ptr<Bar>& forward_reference)
    : forward_reference_(forward_reference)
  { }
 private:
  std::shared_ptr<Bar> forward_reference_; // 指向 Bar 的共享指针（构成引用关系）
};

class Bar {
 public:
  // 显式构造函数，接收指向 Foo 的 weak_ptr
  explicit Bar(const std::weak_ptr<Foo>& back_reference)
    : back_reference_(back_reference)
  { }
  
  void DoSomething()
  {
    // 将 weak_ptr 锁定为 shared_ptr，若指向的对象仍存在则执行后续操作
    if (auto shared_back_reference = back_reference_.lock()) {
      // 使用 *shared_back_reference 操作 Foo 对象
    }
  }
 private:
  std::weak_ptr<Foo> back_reference_; // 指向 Foo 的弱指针（打破循环）
};
```

注：如果你的业务场景需要自定义开发智能指针，建议在基本功能、使用方式等方面和标准库（std）中的智能指针保持一致。

## 单元测试

注：以下单元测试代码若无特殊说明均使用 GoogleTest 测试框架编写。

### 异常和边界条件测试

充分测试边界条件和异常情况是发现潜在 bug 的关键。生产环境中的问题往往出现在边界条件和异常场景，只测试正常流程的单测无法提供有效保护。

正例：

```cpp
// 测试边界条件
TEST_F(VectorTest, AtIndexOutOfBoundsThrowsException) {
  std::vector<int> vec{1, 2, 3};
  EXPECT_THROW(vec.at(5), std::out_of_range);
  EXPECT_THROW(vec.at(-1), std::out_of_range);
}

TEST_F(StringTest, SubstringEdgeCasesHandlesGracefully) {
  std::string str = "hello";
  // 测试负数索引
  EXPECT_EQ(GetSubstring(str, -1, 2), "");
  // 测试超出范围
  EXPECT_EQ(GetSubstring(str, 10, 2), "");
  // 测试空字符串
  EXPECT_EQ(GetSubstring("", 0, 1), "");
}

// 测试异常输入
TEST_F(FileReaderTest, ReadFileFileNotExistsReturnsError) {
  FileReader reader;
  auto result = reader.ReadFile("non_existent_file.txt");
  EXPECT_FALSE(result.has_value());
}
```

反例：

```cpp
TEST_F(VectorTest, AtValidIndexReturnsElement) {
  std::vector<int> vec{1, 2, 3};
  EXPECT_EQ(vec.at(1), 2);  // 只测试正常情况，缺少边界测试
}
```

### Mock 和依赖隔离

使用 Mock 隔离外部依赖，确保单元测试的独立性、稳定性和可控性。真正的单元测试应该只测试当前单元，不依赖外部系统。

正例：

```cpp
// 定义 Mock 接口
class MockFileSystem : public FileSystemInterface {
public:
  MOCK_METHOD(bool, FileExists, (const std::string& path), (override));
  MOCK_METHOD(std::string, ReadFile, (const std::string& path), (override));
  MOCK_METHOD(bool, WriteFile, (const std::string& path, const std::string& content), (override));
};

// 使用 Mock 进行测试
TEST_F(ConfigLoaderTest, LoadConfigFileNotExistsReturnsFalse) {
  MockFileSystem mock_fs;
  EXPECT_CALL(mock_fs, FileExists("config.json"))
      .WillOnce(Return(false));
  
  ConfigLoader loader(&mock_fs);
  EXPECT_FALSE(loader.LoadConfig("config.json"));
}

TEST_F(ConfigLoaderTest, LoadConfigFileExistsLoadsSuccessfully) {
  MockFileSystem mock_fs;
  EXPECT_CALL(mock_fs, FileExists("config.json"))
      .WillOnce(Return(true));
  EXPECT_CALL(mock_fs, ReadFile("config.json"))
      .WillOnce(Return("{\"key\": \"value\"}"));
  
  ConfigLoader loader(&mock_fs);
  EXPECT_TRUE(loader.LoadConfig("config.json"));
  EXPECT_EQ(loader.GetValue("key"), "value");
}
```

反例：

```cpp
TEST_F(ConfigLoaderTest, LoadConfigIntegration) {
  ConfigLoader loader;  // 直接依赖真实文件系统
  EXPECT_TRUE(loader.LoadConfig("real_config.json"));  // 依赖外部文件存在
}
```

### 避免虚假的单测

单元测试是为了发现问题，不是为了跑覆盖率。被测函数的核心输出应被检查到，否则就是虚假单测。

反例：

```cpp
bool GetValue(const std::string& key, std::string& value) {
  value = ...;
  return true;
}

TEST_F(KvTest, GetValue) {
  std::string value;
  ASSERT_TRUE(GetValue("key", value));  // 只检查返回值，未检查核心输出
}
```

修正：

```cpp
TEST_F(KvTest, GetValueValidKeyReturnsCorrectValue) {
  std::string value;
  ASSERT_TRUE(GetValue("test_key", value));
  EXPECT_EQ(value, "expected_value");  // 检查核心输出
}
```

### 保持单测的原子性

一个单测函数应该只对应一个功能点，如果一个单测函数测试了多个功能，会导致后续单测的维护非常困难。

反例：

```cpp
TEST_F(DatabaseTest, InitReader) {
  skit::DatabaseImpl database;
  EXPECT_FALSE(database.Init(nullptr, false));
  auto option = GetDatabaseReadOption();
  EXPECT_TRUE(database.Init(option, true));
  EXPECT_TRUE(database.Commit());
  EXPECT_EQ(database.GetDocCount(), 1000);
  EXPECT_EQ(database.GetDBPath(), "xxx");
  // 还有几十行对 database 接口的测试
}
```

修正：

```cpp
TEST_F(DatabaseTest, InitNullOptionReturnsFalse) {
  skit::DatabaseImpl database;
  EXPECT_FALSE(database.Init(nullptr, false));
}

TEST_F(DatabaseTest, InitValidOptionReturnsTrue) {
  skit::DatabaseImpl database;
  auto option = GetDatabaseReadOption();
  EXPECT_TRUE(database.Init(option, true));
}

TEST_F(DatabaseTest, CommitAfterInitReturnsTrue) {
  skit::DatabaseImpl database;
  auto option = GetDatabaseReadOption();
  database.Init(option, true);
  EXPECT_TRUE(database.Commit());
}
```

### 测试数据管理

使用常量或测试夹具管理测试数据，避免硬编码和重复数据，提高测试的可维护性。

正例：

```cpp
class StringUtilsTest : public ::testing::Test {
protected:
  void SetUp() override {
    test_strings_ = {
      {"empty", ""},
      {"single_word", "hello"},
      {"multiple_words", "hello world test"},
      {"with_delimiter", "a,b,c,d"}
    };
  }
  
  std::map<std::string, std::string> test_strings_;
  static constexpr char kDefaultDelimiter[] = ",";
  static constexpr size_t kMaxStringLength = 1000;
};

TEST_F(StringUtilsTest, SplitEmptyStringReturnsEmptyVector) {
  auto result = StringUtils::Split(test_strings_["empty"], kDefaultDelimiter);
  EXPECT_TRUE(result.empty());
}
```

### 参数化测试

对于需要测试多组相似数据的场景，使用参数化测试减少重复代码。

正例：

```cpp
class MathUtilsTest : public ::testing::TestWithParam<std::tuple<int, int, int>> {};

TEST_P(MathUtilsTest, AddValidInputsReturnsCorrectSum) {
  auto [a, b, expected] = GetParam();
  EXPECT_EQ(MathUtils::Add(a, b), expected);
}

INSTANTIATE_TEST_SUITE_P(
  AdditionTests,
  MathUtilsTest,
  ::testing::Values(
    std::make_tuple(1, 2, 3),
    std::make_tuple(-1, 1, 0),
    std::make_tuple(0, 0, 0),
    std::make_tuple(100, -50, 50)
  )
);
```

### 断言选择和错误信息

选择合适的断言宏，并在必要时提供清晰的错误信息，帮助快速定位问题。

正例：

```cpp
TEST_F(ConfigTest, ParseConfigValidJsonParsesCorrectly) {
  std::string json = R"({"timeout": 30, "retries": 3})";
  Config config;
  ASSERT_TRUE(config.Parse(json)) << "Failed to parse valid JSON: " << json;
  
  EXPECT_EQ(config.GetTimeout(), 30) << "Timeout value mismatch";
  EXPECT_EQ(config.GetRetries(), 3) << "Retries value mismatch";
}
```

### 测试环境隔离

确保测试之间相互独立，避免测试顺序依赖和状态污染。

正例：

```cpp
class DatabaseTest : public ::testing::Test {
protected:
  void SetUp() override {
    // 每个测试前创建独立的数据库实例
    db_ = std::make_unique<TestDatabase>();
    db_->Initialize();
  }
  
  void TearDown() override {
    // 每个测试后清理资源
    if (db_) {
      db_->Cleanup();
    }
  }
  
  std::unique_ptr<TestDatabase> db_;
};
```

### 避免单测统计不全

当我们使用 `gcc` 的编译优化时，可能会导致部分函数被内联，进而导致单测覆盖统计不完整。有两种修改方式：

- 将单测的构建修改为：O0，不做编译优化，默认不内联
- 指定编译选项为 `-fno-inline`，取消内联

注：编译选项 `-fno-inline-functions` 只能禁止编译器自动内联。


## 参考文献

[1]. [CppCoreGuidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)
