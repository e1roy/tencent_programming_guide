# Futures

## tl;dr

- 优先使用 `CompletableFuture` 或 `ListenableFuture`，而不是 `Future`。
- 正确使用 `CompletableFuture` 的 API。
- 使用自定义线程池处理阻塞操作。
- 避免不必要的异步调用。

## Future, CompletableFuture 和 ListenableFuture

- Future 是 Java 最初的异步构造。
- CompletableFuture 由 JDK 8 引进。
- ListenableFuture 是 Google Guava 库中提供的 Future 扩展。

避免直接使用 Future，优先选择 CompletableFuture。请按项目的需要谨慎使用 ListenableFuture ，通常，它相对 CompletableFuture 的优势有限，因此，如果没有特殊的原因，应该优先使用 CompletableFuture。

## CompletableFuture 使用指南

### Future 的组合

1.链式异步操作
  - CompletableFuture 提供了一些异步操作方法，如 `thenApplyAsync()` 和 `thenAcceptAsync()` 等，可以避免阻塞当前线程。
  - 如果必须进行阻塞操作，可以使用 `thenApply()` 和 `thenAccept()` 方法，但需要注意阻塞操作可能会影响程序的性能和可伸缩性。
2.组合操作：
  - 依赖关系：使用 `CompletableFuture.thenCompose()`。
  - 并行合并：使用 `CompletableFuture.thenCombine()`。 
3.批量处理：
  - 全完成：`CompletableFuture.allOf()`
  - 任一完成：`CompletableFuture.anyOf()`

### 异常处理

CompletableFuture 提供了三个的异常处理的 API：

1.`exceptionally`：捕获异常并返回替代值
它会捕获本层的异常，并且执行 `exceptionally` 内的函数，返回一个新的值。如果没有异常，exceptionally 会被跳过。

```java
CompletableFuture<Integer> future = CompletableFuture.supplyAsync(() -> {
    // 可能会出现异常的代码
    return 10 / 0;  // 抛出ArithmeticException
}).exceptionally(ex -> {
    // 异常处理代码
    System.out.println("Exception: " + ex.getMessage());
    return 0;  // 默认值
});
```

2.`handle()/handleAsync()`：统一处理结果和异常
会无条件执行，将正常结果与异常作为 handler 的两个入参传入，并且可以返回一个**任意**类型的结果。正常结果和异常只有一个为空。例如：

```java
CompletableFuture<Integer> future = CompletableFuture.supplyAsync(() -> {
    // 可能会出现异常的代码
    return 10 / 0;  // 抛出ArithmeticException
}).handle((result, ex) -> {
    if (ex != null) {
        // 异常处理代码
        System.out.println("Exception: " + ex.getMessage());
        return 0;
    }
    // 正常结果处理代码
    return result;
});
```

3.`whenComplete`：观察结果不影响返回值
接收一个 `BiConsumer`，会无条件**旁路**执行，将正常结果与异常作为 handler 的两个入参传入，并且 `BiConsumer` 不返回结果。`whenComplete` 会返回原 Future。

```java
// 使用 whenComplete
CompletableFuture<Integer> future = CompletableFuture.supplyAsync(() -> {
    return 10 / 2;
}).whenComplete((result, ex) -> {
    if (ex != null) {
        // 异常处理代码
        System.out.println("Exception: " + ex.getMessage());
    } else {
        System.out.println("whenComplete: " + result);
    }
});
System.out.println(future.get()); // get() 返回结果 5
```

### Join vs Get

作为终止阻塞调用，`CompletableFuture` 提供了两个方法： `join()` 和 `get()` 。它们的主要区别是：

- `join()` 会抛出 `CompletionException` 和 `CancellationException`，均为 Unchecked Exception，所以不强制处理。
- `get()` 会抛出 `InterruptedException/ExecutionException` 这两个 Checked Exception，强制处理，同时也会抛出 `CancellationException`。

但是，由于这两个函数都会阻塞直到获得结果。如果希望提供一个 Future 的最长等待时限，使用 `get(long, TimeUnit)`。

```java
// 带超时控制
try {
    int result = future.get(2, TimeUnit.SECONDS);
} catch (InterruptedException e) {
    // 处理中断异常
} catch (ExecutionException e) {
    // 处理执行异常
} catch (TimeoutException e) {
    // 处理超时异常
}
```

### 性能问题

1.使用自定义线程池
`CompletableFuture` 默认使用 `ForkJoinPool` 实现异步操作（类似于 [ParallelStream](https://iwiki.woa.com/pages/viewpage.action?pageId=4007320877)），但是如果异步操作需要执行长时间的计算或阻塞操作，可能会影响整个应用程序的性能。因此，建议使用自定义的线程池来执行 `CompletableFuture` 中的异步操作，以避免影响整个应用程序的性能。

```java
ExecutorService customPool = Executors.newFixedThreadPool(4);

CompletableFuture.supplyAsync(() -> {
    // 阻塞或耗时操作
    return fetchExternalData();
}, customPool); // 指定自定义线程池
```

2.避免不必要的异步
虽然 `CompletableFuture` 提供了很多便利的方法来处理异步操作，但是在使用 `CompletableFuture` 时应该避免滥用。如果操作耗时很低，可同步调用更高效，而不必使用 `CompletableFuture`，`CompletableFuture` 适合I/O操作、远程调用等阻塞场景。

### 反例
```java
// 错误示范：对简单计算使用异步
CompletableFuture<Integer> badFuture = CompletableFuture.supplyAsync(() -> {
    // 简单内存计算（<1ms）
    return 2 + 2;
});

// 实际增加了线程切换开销（约10-100μs），比同步执行慢10倍以上
int result = badFuture.join();
```

### 正例
```java
// 正确示范：适合异步的I/O操作
CompletableFuture<String> fetchDataAsync() {
    return CompletableFuture.supplyAsync(() -> {
        // 网络请求耗时操作
        return requestDataSync();
    }, httpThreadPool); // 使用专用线程池
}

// 调用方
fetchDataAsync().thenAccept(response -> {
    System.out.println("Received: " + response);
});
```

## 扩展阅读

- https://km.woa.com/group/45812/articles/show/522846
