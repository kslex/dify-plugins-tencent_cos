# Tencent Cloud COS Plugin

A powerful Dify plugin providing seamless integration with Tencent Cloud Object Storage (COS). Enables direct file uploads to Tencent Cloud COS and efficient file retrieval using URLs, with rich configuration options.

### Version Information

- **Current Version**: v0.0.3
- **Release Date**: 2025-12-21
- **Last Updated**: 2025-12-21
- **Compatibility**: Dify Plugin Framework
- **Python Version**: 3.12

#### Version History
- **v0.0.3** (2025-12-21): Added batch file download and public file download capabilities
- **v0.0.2** (2025-09-30): Added multi-file upload functionality with enhanced directory and filename options
- **v0.0.1** (2025-09-30): Initial release with file upload and retrieval capabilities, support for multiple directory structures and filename modes

### Quick Start

1. Download the tencent_cos plugin from the Dify marketplace
2. Configure Tencent Cloud COS authorization information
3. After completing the above configuration, you can immediately use the plugin

### Core Features

#### File Upload to COS
- **Direct File Upload**: Upload any file type directly to Tencent Cloud COS
- **Flexible Directory Structure**: Multiple storage directory organization options
  - Flat structure (no_subdirectory)
  - Hierarchical date structure (yyyy_mm_dd_hierarchy)
  - Combined date structure (yyyy_mm_dd_combined)
- **Filename Customization**: Control how filenames are stored in COS
  - Use original filename
  - Append timestamp to original filename
- **Source File Tracking**: Automatically captures and returns the original filename
- **Smart Extension Detection**: Automatically determine file extensions based on content type

#### File Retrieval by URL
- **Direct Content Access**: Retrieve file content directly using COS URLs
- **Cross-Region Support**: Works with all Tencent Cloud COS regions worldwide

#### Batch File Download
- **Multiple URLs Support**: Download multiple files using a list of URLs separated by semicolons
- **Progress Tracking**: Real-time status updates for each file download
- **Comprehensive Statistics**: Summary of total files, successful downloads, and total size

#### Public File Download
- **No Authentication Required**: Download public files from any platform without API keys
- **Universal Compatibility**: Works with any publicly accessible file URL
- **Smart Filename Detection**: Automatically extracts filenames from URLs or headers

### Technical Advantages

- **Secure Authentication**: Robust credential handling with support for HTTPS
- **Efficient Storage Management**: Intelligent file organization options
- **Comprehensive Error Handling**: Detailed error messages and status reporting
- **Multiple File Type Support**: Works with all common file formats
- **Rich Parameter Configuration**: Extensive options for customized workflows
- **Source File Tracking**: Preserves original filename information

### Requirements

- Python 3.12
- Tencent Cloud COS account with valid SecretId and SecretKey credentials
- Dify Platform access
- Required Python packages (installed via requirements.txt)

### Installation & Configuration

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure the plugin in Dify with the following parameters:
   - **Region**: Your Tencent Cloud COS region (e.g., ap-beijing)
   - **Bucket Name**: Your COS bucket name
   - **SecretId**: Your Tencent Cloud SecretId
   - **SecretKey**: Your Tencent Cloud SecretKey

### Usage

The plugin provides five powerful tools for interacting with Tencent Cloud COS:

#### 1. Upload File to COS (upload_file)

Dedicated tool for uploading files to Tencent Cloud COS.
- **Parameters**:
  - `file`: The local file to upload (required)
  - `directory`: First-level directory under the bucket (required)
  - `directory_mode`: Optional directory structure mode (default: `no_subdirectory`)
    - `no_subdirectory`: Store directly in specified directory
    - `yyyy_mm_dd_hierarchy`: Store in date-based hierarchical structure
    - `yyyy_mm_dd_combined`: Store in combined date directory
  - `filename`: Optional custom filename for COS storage
  - `filename_mode`: Optional filename composition mode (default: `filename`)
    - `filename`: Use original filename
    - `filename_timestamp`: Use original filename plus timestamp

#### 2. Multi-Upload Files to COS (multi_upload_files)

Dedicated tool for uploading multiple files to Tencent Cloud COS.
- **Parameters**:
  - `files`: The local files to upload (required, maximum 10 files)
  - `directory`: First-level directory under the bucket (required)
  - `directory_mode`: Optional directory structure mode (default: `no_subdirectory`)
    - `no_subdirectory`: Store directly in specified directory
    - `yyyy_mm_dd_hierarchy`: Store in date-based hierarchical structure
    - `yyyy_mm_dd_combined`: Store in combined date directory
  - `filename_mode`: Optional filename composition mode (default: `filename`)
    - `filename`: Use original filename
    - `filename_timestamp`: Use original filename plus timestamp

#### 3. Get File by URL (get_file_by_url)

Dedicated tool for retrieving files from Tencent Cloud COS using URLs.
- **Parameters**:
  - `file_url`: The URL of the file in Tencent Cloud COS

#### 4. Batch Download Files by URLs (get_files_by_urls)

Dedicated tool for batch downloading multiple files from Tencent Cloud COS.
- **Parameters**:
  - `file_urls`: Multiple URLs of files in Tencent Cloud COS, separated by semicolon (;)

#### 5. Download Public File by URL (get_public_file_by_url)

Dedicated tool for downloading public files from any platform without authentication.
- **Parameters**:
  - `file_url`: The URL of the public file that can be accessed without authentication

### Examples

#### Upload File
<img width="2026" height="523" alt="upload-001" src="https://github.com/user-attachments/assets/ac7a1539-e7fc-419d-a9b0-273cec761a7d" />

#### Batch Upload Files

<img width="1978" height="954" alt="upload-002" src="https://github.com/user-attachments/assets/ab5755e1-c6df-4b63-8525-a52b1ef1df84" />

#### Get File by URL

<img width="2225" height="487" alt="download-001" src="https://github.com/user-attachments/assets/c4aab17f-5294-4107-8799-f85c3ef1f7cd" />
<img width="2222" height="544" alt="download-002" src="https://github.com/user-attachments/assets/12fbc8ec-4249-46b4-8680-e10761510774" />

### Notes

- Ensure your COS bucket has the correct permissions configured
- The plugin requires valid Tencent Cloud credentials with appropriate COS access permissions
- For very large files, consider using multipart upload functionality (not currently implemented)

### Developer Information

- **Author**: `https://github.com/sawyer-shi`
- **Email**: sawyer36@foxmail.com
- **License**: MIT License
- **Source Code**: `https://github.com/sawyer-shi/dify-plugins-tencent_cos`
- **Support**: Through Dify platform and GitHub Issues

---

**Ready to seamlessly integrate with Tencent Cloud COS?**



