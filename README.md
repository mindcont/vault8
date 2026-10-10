# Vault 8 中文说明

## 资料定位

Vault 8 是 WikiLeaks 于 2017 年 11 月发布的 Vault 7 后续资料系列，主题是 CIA 软件项目的源代码和开发分析。官方页面明确说明，Vault 8 的首个发布项目是 **Hive**，包括源码和开发日志。

- 官方主页：[WikiLeaks Vault 8](https://wikileaks.org/vault8/)
- 官方 Hive Repository：[Hive Repository](https://wikileaks.org/vault8/document/repo_hive/)
- 官方开发日志：[Hive Development Logs](https://wikileaks.org/vault8/document/hive-log/)
- 相关 Vault 7 文档：[Hive User Guide](https://wikileaks.org/vault7/document/hive-UsersGuide/hive-UsersGuide.pdf)

## Hive 是什么

Hive 是 CIA 恶意软件基础设施中的隐蔽通信平台，用于让目标端植入程序向控制端发送信息并接收任务。官方说明将其描述为覆盖多种植入程序的通信平台，包含公开伪装域名、HTTP/HTTPS 中继、隐藏的后端服务器、Beacon 验证和操作员管理网关等组件。

仓库文件涉及客户端、服务端、Honeycomb、通信协议、加密/证书材料、构建文件、第三方库和多个开发分支。Hive 的重点不是单个目标端功能，而是植入程序与控制基础设施之间的通信、认证、转发和运维。

## 本地归档

- [hive.zip](./hive.zip)：从用户下载的官方 Hive Repository 压缩包，按原始 ZIP 保留，不拆分、不改名、不重新打包。

该 ZIP 内含 `.git` 目录、Git 对象、分支和标签，能够保留官方仓库的历史结构。文件大小为 100,666,724 字节，SHA-256 为 `5DEC53517FCBD5D7F9F2780AD7B7B9CC94092190744EB1F1AA60D4698836AE36`。

此前按网页条目抓取的分散文件和人工生成归档已移除，避免与官方 ZIP 混用。官方网页索引仍显示 2,185 个条目；本仓库现在以单一原始 ZIP 作为 Hive Repository 的唯一数据文件。

## 文件类型

公开仓库中可以看到：

- C 源文件和头文件；
- Makefile 和构建配置；
- Linux、Solaris、MIPS、ARM 等平台相关代码；
- 客户端、服务端和 Honeycomb 组件；
- OpenSSL/PolarSSL 等依赖或修改内容；
- 证书、密钥、测试数据和开发日志；
- Git 分支和提交历史的网页化记录。

## 安全说明

本目录仅用于历史研究、静态分析和完整性保存：

- 不要编译或运行其中的源码、脚本、二进制和证书工具；
- 不要把测试域名、密钥或配置用于真实网络；
- 如需研究，应使用离线虚拟机和无敏感数据的隔离环境；
- ZIP 解压前后都应保留原始哈希和清单；
- 本仓库不代表对 WikiLeaks 内容真实性、归因或当前有效性的独立鉴定。

## 与 Vault 7 的关系

Vault 7 主要提供项目设计文档、用户指南和技术说明；Vault 8 则进一步公开了 Hive 的源码和开发日志。两者保持为独立 Git 仓库，避免源码、二进制和文档混合管理。

## 客户端、服务端与控制链路

Hive 不是传统的 Web 客户端/服务端应用，而是一套分层的远程通信与控制平台。仓库中同时存在目标端、控制端、Beacon 接收端和网络中继相关组件：

| 组件 | 目录 | 主要职责 |
|---|---|---|
| 目标端植入程序 | `client/`、部分 `server/` | 在目标设备上运行，主动回连、发送 Beacon 并接收任务 |
| 操作员控制端 | `ilm-client/` | 向目标端发送命令、管理会话和文件传输 |
| Beacon 接收与解析 | `honeycomb/` | 接收、解密、解析 Beacon，并输出 XML `.rsi` 文件 |
| 网络中继设施 | `infrastructure/` | 提供重定向和通信转发配置 |

这里的 `server/` 更接近目标端服务程序和多平台构建代码；操作员侧的控制逻辑主要位于 `ilm-client/`，而不是一个常规意义上的中心 Web 服务。

## 远程控制功能

根据 `ilm-client/Command.cpp`、`File.h`、`honeycomb.py` 以及相关配置和构建文件，代码中可以确认以下能力：

- `Command::Execute`：向远端发送命令并接收执行结果；
- `Command::Session` 和 `Command::LaunchTrueShell`：建立交互式远程 Shell，会使用加密的 `cryptcat` 通道；
- `File::Get`、`File::Put`、`File::Delete`：从目标端获取文件、上传文件和删除文件；
- Beacon 信息收集：MAC 地址、系统类型、运行时间、进程列表、IP 配置、路由表、网络连接、Hive 版本和下次 Beacon 时间；
- `Command::Exit` 和 `Command::ShutDown`：关闭会话、终止相关进程或停止植入端；
- 更新与维护：`hiveUpdater.py`、`hiveReset.py`、`hive-patcher` 等组件提供更新、重置和补丁相关流程。

这些结论来自源码中的函数、命令注册和数据结构定义，未通过编译或实际联网运行验证。

## 自定义二进制信令解析

Hive 使用自定义的二进制协议承载 Beacon 和控制数据，而不是直接传输明文命令。`honeycomb/honeycomb.py` 展示了较完整的接收端解析流程：

1. 接收连接和初始数据，读取自定义协议头；
2. 解析主头和附加头，取得代理标识、Beacon 地址、目标地址、代理地址以及数据长度；
3. 根据协议版本判断数据格式，并按块接收较大的 Beacon 数据；
4. 通过随机数据派生会话密钥，使用 XTEA 解密数据；
5. 对较新版本的数据使用 Bzip2 解压；
6. 解析 Beacon 头和 TLV 风格的类型/长度字段；
7. 将系统信息写入 XML 格式的 `.rsi` 文件，并记录日志。

源码中可见的协议字段包括：

- 主协议头：版本、消息类型、头长度、数据长度、代理标识；
- 附加头：字段类型和字段长度；
- Beacon 头：Hive 协议版本和目标操作系统编号；
- Beacon 数据项：MAC 地址、运行时间、进程列表、IP 配置、路由表、网络连接和后续 Beacon 信息。

`honeycomb` 中还定义了 `BTHP_HDR`、`BTHP_ADDL_HDR`、`BEACON_HDR` 和 `ADDL_HDR` 等结构，以及 `parse_bthp_packet`、`parse_beacon_data` 等解析函数。通信过程包含分块确认机制，接收端会返回已接收字节数，用于处理较大的 Beacon 数据。

从代码结构看，该协议同时承担三类职责：连接封装、会话级加密/压缩以及 Beacon 元数据编码。它是 Hive 各平台植入端与控制端之间的核心信令层。

## 代码开发时间

Git 历史显示，仓库至少覆盖以下时期：

- 2013 年 8 月 8 日：导入 `Hive 2.6.1`，此前代码来自旧的 Subversion 仓库；
- 2013—2015 年：持续进行多平台、构建系统、通信和维护功能开发；
- 2015 年 11 月 13 日：Git 历史中仍有构建和平台适配相关提交；
- 2017 年 11 月：WikiLeaks 公开 Vault8 Hive Repository。

因此，2013 年是当前公开 Git 历史的起点，不一定是 Hive 项目的真正起始年份。
