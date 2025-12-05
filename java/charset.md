# Charset 字符集

## tl;dr

- 总是使用 UTF-8 作为 Charset。
- 代码应该总是使用 UTF-8 进行编码。

## Charset in Java

使用 `nio.charset.Charset`， 即 https://docs.oracle.com/javase/11/docs/api/java/nio/charset/Charset.html 。

`Charset` 支持使用名字指定字符集，也支持标准字符集。应该总是使用标准字符集，即:

|Charset | Description |
| -- |--|
|US-ASCII |Seven-bit ASCII, a.k.a. ISO646-US, a.k.a. the Basic Latin block of the Unicode character set |
|ISO-8859-1 |ISO Latin Alphabet No. 1, a.k.a. ISO-LATIN-1 |
|UTF-8 |Eight-bit UCS Transformation Format |
|UTF-16BE |Sixteen-bit UCS Transformation Format, big-endian byte order |
|UTF-16LE |Sixteen-bit UCS Transformation Format, little-endian byte order |
|UTF-16 |Sixteen-bit UCS Transformation Format, byte order identified by an optional byte-order mark |

## 代码的字符集

使用 UTF-8。

## 总是使用 Line Feed(LF)，永远不要使用 Carriage Return Line Feed(CLRF)

一个经常出现的令人困惑的问题在于回车与换行。具体地：

- Line Feed(LF) 是一个 ASCII 不可见字符 10，escape 为 `\n`，指换到下一行
- Carriage Return(CR) 是一个 ASCII 不可见字符 13，escape 为 `\r`，指移动到行开头

因此，UNIX 默认换行只使用 LF，即 `\n`。而 Windows 默认使用 CRLF，即 `\r\n`。

但是不同的操作系统之间的换行符通常会导致无法正常编译，且非常诡异的报错信息。因此，不管使用哪种操作系统，代码的换行符应该总是 `\n`。

考虑在持续集成上添加 Presubmit 检查，禁用 CRLF。

## 扩展阅读

- [Rob Pike: Utf-8 History](http://doc.cat-v.org/bell_labs/utf-8_history)
- https://en.wikipedia.org/wiki/UTF-8
- [The Absolute Minimum Every Software Developer Absolutely, Positively Must Know About Unicode and Character Sets](https://www.joelonsoftware.com/2003/10/08/the-absolute-minimum-every-software-developer-absolutely-positively-must-know-about-unicode-and-character-sets-no-excuses/)
