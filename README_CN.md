# 腾讯云COS云存储插件

一个功能强大的Dify插件，提供与腾讯云对象存储（COS）的无缝集成。支持将文件直接上传到腾讯云COS，并使用URL高效检索文件，提供丰富的配置选项。

### 版本信息

- **当前版本**: v0.0.3
- **发布日期**: 2025-12-21
- **最新更新时间**: 2025-12-21
- **兼容性**: Dify Plugin Framework
- **Python版本**: 3.12

#### 版本历史
- **v0.0.3** (2025-12-21): 新增批量文件下载和公共文件下载功能
- **v0.0.2** (2025-09-30): 新增多文件上传功能，增强目录和文件名选项
- **v0.0.1** (2025-09-30): 初始版本，支持文件上传和检索功能，支持多种目录结构和文件名模式

### 快速开始

1. 从Dify市场下载该插件tencent_cos
2. 配置腾讯云COS的授权信息
3. 完成上述配置即可马上使用该插件

### 核心特性

#### 文件上传至COS
- **直接文件上传**: 将任何类型的文件直接上传到腾讯云COS
- **灵活的目录结构**: 多种存储目录组织选项
  - 扁平结构 (no_subdirectory)
  - 分层日期结构 (yyyy_mm_dd_hierarchy)
  - 合并日期结构 (yyyy_mm_dd_combined)
- **文件名自定义**: 控制文件在COS中的存储名称
  - 使用原始文件名
  - 在原始文件名后附加时间戳
- **源文件追踪**: 自动捕获并返回原始文件名
- **智能扩展名检测**: 基于内容类型自动确定文件扩展名

#### 通过URL获取文件
- **直接内容访问**: 使用COS URL直接检索文件内容
- **跨区域支持**: 适用于全球所有腾讯云COS区域

#### 批量文件下载
- **多URL支持**: 使用分号分隔的URL列表下载多个文件
- **进度跟踪**: 每个文件下载的实时状态更新
- **全面统计**: 总文件数、成功下载和总大小的摘要

#### 公共文件下载
- **无需认证**: 从任何平台下载公共文件，无需API密钥
- **通用兼容性**: 适用于任何可公开访问的文件URL
- **智能文件名检测**: 自动从URL或标头中提取文件名

### 技术优势

- **安全认证**: 强大的凭证处理，支持HTTPS
- **高效存储管理**: 智能文件组织选项
- **全面的错误处理**: 详细的错误消息和状态报告
- **多种文件类型支持**: 适用于所有常见文件格式
- **丰富的参数配置**: 用于自定义工作流程的广泛选项
- **源文件追踪**: 保留原始文件名信息

### 要求

- Python 3.12
- 具有有效SecretId和SecretKey凭证的腾讯云COS账户
- Dify平台访问权限
- 所需的Python包（通过requirements.txt安装）

### 安装与配置

1. 安装所需依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 在Dify中配置插件，输入以下参数：
   - **Region**: 您的腾讯云COS地域（例如：ap-beijing）
   - **Bucket Name**: 您的COS存储桶名称
   - **SecretId**: 您的腾讯云SecretId
   - **SecretKey**: 您的腾讯云SecretKey

### 使用方法

该插件提供五个强大的工具用于与腾讯云COS交互：

#### 1. 上传文件至COS (upload_file)

用于将文件上传到腾讯云COS的专用工具。
- **参数**:
  - `file`: 要上传的本地文件（必填）
  - `directory`: 存储桶下的一级目录（必填）
  - `directory_mode`: 可选的目录结构模式（默认：`no_subdirectory`）
    - `no_subdirectory`: 直接存储在指定目录中
    - `yyyy_mm_dd_hierarchy`: 存储在基于日期的分层结构中
    - `yyyy_mm_dd_combined`: 存储在合并日期目录中
  - `filename`: 用于COS存储的可选自定义文件名
  - `filename_mode`: 可选的文件名组成模式（默认：`filename`）
    - `filename`: 使用原始文件名
    - `filename_timestamp`: 使用原始文件名加上时间戳

#### 2. 批量上传文件至COS (multi_upload_files)

用于将多个文件上传到腾讯云COS的专用工具。
- **参数**:
  - `files`: 要上传的本地文件（必填，最多10个文件）
  - `directory`: 存储桶下的一级目录（必填）
  - `directory_mode`: 可选的目录结构模式（默认：`no_subdirectory`）
    - `no_subdirectory`: 直接存储在指定目录中
    - `yyyy_mm_dd_hierarchy`: 存储在基于日期的分层结构中
    - `yyyy_mm_dd_combined`: 存储在合并日期目录中
  - `filename_mode`: 可选的文件名组成模式（默认：`filename`）
    - `filename`: 使用原始文件名
    - `filename_timestamp`: 使用原始文件名加上时间戳

#### 3. 通过URL获取文件 (get_file_by_url)

用于使用URL从腾讯云COS检索文件的专用工具。
- **参数**:
  - `file_url`: 腾讯云COS中文件的URL

#### 4. 批量下载文件 (get_files_by_urls)

用于批量下载腾讯云COS中多个文件的专用工具。
- **参数**:
  - `file_urls`: 腾讯云COS中多个文件的URL，使用分号(;)分隔

#### 5. 下载公共文件 (get_public_file_by_url)

用于从任何平台下载公共文件的专用工具，无需身份验证。
- **参数**:
  - `file_url`: 无需身份验证即可访问的公共文件的URL

### 示例

#### 上传文件
<img width="2026" height="523" alt="upload-001" src="https://github.com/user-attachments/assets/ac7a1539-e7fc-419d-a9b0-273cec761a7d" />

#### 批量上传文件

<img width="1978" height="954" alt="upload-002" src="https://github.com/user-attachments/assets/ab5755e1-c6df-4b63-8525-a52b1ef1df84" />

#### 获取(下载)文件

<img width="2225" height="487" alt="download-001" src="https://github.com/user-attachments/assets/c4aab17f-5294-4107-8799-f85c3ef1f7cd" />
<img width="2222" height="544" alt="download-002" src="https://github.com/user-attachments/assets/12fbc8ec-4249-46b4-8680-e10761510774" />

### 注意事项

- 确保您的COS存储桶配置了正确的权限
- 该插件需要具有适当COS访问权限的有效腾讯云凭证
- 对于非常大的文件，请考虑使用分片上传功能（目前未实现）

### 开发者信息

- **作者**: `https://github.com/sawyer-shi`
- **邮箱**: sawyer36@foxmail.com
- **许可证**: MIT License
- **源码地址**: `https://github.com/sawyer-shi/dify-plugins-tencent_cos`
- **支持**: 通过Dify平台和GitHub Issues

---

**准备好与腾讯云COS无缝集成了吗？**