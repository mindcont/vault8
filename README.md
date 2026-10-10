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

- [Hive-Repository-archive.zip](./Hive-Repository-archive.zip)：按 WikiLeaks 公开索引归档的压缩包。
- `manifest.csv`：下载来源、文件大小、SHA-256 和状态清单。
- 下载脚本：[download-vault8.py](./download-vault8.py)。

本次官方索引共发现 2,185 个文件条目，其中 2,172 个成功下载，13 个因站点返回 404、500 或 503 未成功。官方页面展示的 `hive.zip` 下载链接在本次下载时返回 503，因此当前 ZIP 是根据成功获取的公开索引文件生成的归档，不冒充官方 ZIP 原包；缺失项及其错误状态见 `manifest.csv`。

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
