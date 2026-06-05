import os
from datetime import datetime
from typing import Any, Union
from urllib.parse import urlparse, unquote

# 内容类型到扩展名的映射表（带点号）
CONTENT_TYPE_TO_EXTENSION_WITH_DOT = {
    # 图片格式
    'image/jpeg': '.jpg',
    'image/png': '.png',
    'image/gif': '.gif',
    'image/bmp': '.bmp',
    'image/webp': '.webp',
    'image/svg+xml': '.svg',
    'image/tiff': '.tiff',
    'image/x-icon': '.ico',
    'image/heic': '.heic',
    
    # 音频格式
    'audio/mpeg': '.mp3',
    'audio/wav': '.wav',
    'audio/ogg': '.ogg',
    'audio/flac': '.flac',
    'audio/aac': '.aac',
    'audio/m4a': '.m4a',
    'audio/mp4': '.mp4',
    
    # 视频格式
    'video/mp4': '.mp4',
    'video/mov': '.mov',
    'video/avi': '.avi',
    'video/x-msvideo': '.avi',
    'video/x-ms-wmv': '.wmv',
    'video/webm': '.webm',
    'video/mpeg': '.mpg',
    'video/quicktime': '.mov',
    'video/x-matroska': '.mkv',
    
    # 文档格式
    'application/pdf': '.pdf',
    'application/msword': '.doc',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
    'application/vnd.ms-excel': '.xls',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': '.xlsx',
    'application/vnd.ms-powerpoint': '.ppt',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation': '.pptx',
    'application/rtf': '.rtf',
    'application/vnd.oasis.opendocument.text': '.odt',
    'application/vnd.oasis.opendocument.spreadsheet': '.ods',
    'application/vnd.oasis.opendocument.presentation': '.odp',
    
    # 文本格式
    'text/plain': '.txt',
    'text/csv': '.csv',
    'application/json': '.json',
    'application/xml': '.xml',
    'text/xml': '.xml',
    'text/html': '.html',
    'text/css': '.css',
    'application/javascript': '.js',
    'text/markdown': '.md',
    
    # 压缩格式
    'application/zip': '.zip',
    'application/gzip': '.gz',
    'application/x-rar-compressed': '.rar',
    'application/x-7z-compressed': '.7z',
    'application/x-tar': '.tar',
    'application/x-bzip2': '.bz2',
    
    # 可执行文件
    'application/x-msdownload': '.exe',
    'application/vnd.android.package-archive': '.apk',
    'application/java-archive': '.jar',
    'application/x-shockwave-flash': '.swf',
    
    # 代码文件
    'text/x-python': '.py',
    'text/x-java-source': '.java',
    'text/x-c++src': '.cpp',
    'text/x-csrc': '.c',
    'text/x-csharp': '.cs',
    'text/x-ruby': '.rb',
    'text/x-go': '.go',
    'text/x-rustsrc': '.rs',
    'text/x-swift': '.swift',
    'application/x-php': '.php'
}

# 内容类型到扩展名的映射表（不带点号）
CONTENT_TYPE_TO_EXTENSION = {k: v[1:] for k, v in CONTENT_TYPE_TO_EXTENSION_WITH_DOT.items()}


def get_file_type_from_content_type(content_type: str) -> str:
    """
    根据内容类型获取文件类型（不带点号）
    
    Args:
        content_type: 文件内容类型，如 'image/jpeg'
        
    Returns:
        文件类型，如 'jpg'，如果无法匹配则返回 'unknown'
    """
    # 直接匹配内容类型
    if content_type in CONTENT_TYPE_TO_EXTENSION:
        return CONTENT_TYPE_TO_EXTENSION[content_type]
    
    # 尝试匹配内容类型的前缀（例如 'application/vnd.openxmlformats-officedocument.'）
    for ct, ext in CONTENT_TYPE_TO_EXTENSION.items():
        if content_type.startswith(ct):
            return ext
    
    return "unknown"


def get_extension_from_content_type(content_type: str) -> str:
    """
    根据内容类型获取文件扩展名（带点号）
    
    Args:
        content_type: 文件内容类型，如 'image/jpeg'
        
    Returns:
        文件扩展名，如 '.jpg'，如果无法匹配则返回 '.dat'
    """
    # 直接匹配内容类型
    if content_type in CONTENT_TYPE_TO_EXTENSION_WITH_DOT:
        return CONTENT_TYPE_TO_EXTENSION_WITH_DOT[content_type]
    
    # 尝试匹配内容类型的前缀（例如 'application/vnd.openxmlformats-officedocument.'）
    for ct, ext in CONTENT_TYPE_TO_EXTENSION_WITH_DOT.items():
        if content_type.startswith(ct):
            return ext
    
    return ".dat"


def get_file_type(file: Any) -> str:
    """
    获取文件类型（不带点号）
    
    Args:
        file: 文件对象
        
    Returns:
        文件类型，如 'jpg'，如果无法匹配则返回 'unknown'
    """
    # 1. 首先尝试从文件名获取扩展名
    if hasattr(file, 'name') and file.name:
        _, extension = os.path.splitext(file.name)
        if extension:
            return extension.lower()[1:]  # 移除点号
    
    # 2. 如果无法从文件名获取，尝试从file.filename获取
    if hasattr(file, 'filename') and file.filename:
        _, extension = os.path.splitext(file.filename)
        if extension:
            return extension.lower()[1:]  # 移除点号
    
    # 3. 如果仍然无法获取，尝试从文件内容类型推断
    if hasattr(file, 'content_type') and file.content_type:
        return get_file_type_from_content_type(file.content_type)
    
    return "unknown"


def get_file_extension(file: Any) -> str:
    """
    获取文件扩展名（带点号）
    
    Args:
        file: 文件对象
        
    Returns:
        文件扩展名，如 '.jpg'，如果无法匹配则返回 '.dat'
    """
    # 1. 首先尝试从文件名获取扩展名
    if hasattr(file, 'name') and file.name:
        _, extension = os.path.splitext(file.name)
        if extension:
            return extension.lower()  # 确保是小写
    
    # 2. 如果无法从文件名获取，尝试从file.filename获取
    if hasattr(file, 'filename') and file.filename:
        _, extension = os.path.splitext(file.filename)
        if extension:
            return extension.lower()  # 确保是小写
    
    # 3. 如果仍然无法获取，尝试从文件内容类型推断
    if hasattr(file, 'content_type') and file.content_type:
        return get_extension_from_content_type(file.content_type)
    
    return ".dat"


def generate_object_key(directory: str, directory_mode: str, filename: str) -> str:
    """
    根据目录模式生成完整的对象键

    Args:
        directory: 目录名称
        directory_mode: 目录模式
        filename: 文件名

    Returns:
        完整的对象键
    """
    # 对directory进行前后去空格处理
    directory = directory.strip()

    # 根据目录模式生成路径
    if directory_mode == 'yyyy_mm_dd_hierarchy':
        # 年/月/日 层级目录
        date_path = datetime.now().strftime('%Y/%m/%d')
        object_key = f"{directory}/{date_path}/{filename}"
    elif directory_mode == 'yyyy_mm_dd_combined':
        # 年月日 一体目录
        date_path = datetime.now().strftime('%Y%m%d')
        object_key = f"{directory}/{date_path}/{filename}"
    else:
        # 默认：无子目录
        object_key = f"{directory}/{filename}"

    return object_key


def parse_cos_url(url: str) -> tuple:
    """
    解析COS URL，支持标准格式和自定义域名格式
    标准格式: https://bucket.cos.region.myqcloud.com/object_key
    自定义域名格式: https://custom-domain/object_key
    """
    parsed_url = urlparse(url)

    # 处理URL编码
    object_key = unquote(parsed_url.path.lstrip('/'))

    # 如果是标准COS URL格式 (bucket.cos.region.myqcloud.com)
    if parsed_url.hostname and parsed_url.hostname.endswith('.myqcloud.com'):
        # 提取bucket和region
        hostname_parts = parsed_url.hostname.split('.')
        if len(hostname_parts) >= 4 and hostname_parts[1] == 'cos':
            bucket_name = hostname_parts[0]
            region_name = hostname_parts[2]
            return (bucket_name, region_name, object_key)

    # 对于自定义域名格式，需要额外的region或bucket验证
    # 此处仅返回None作为bucket和region，由调用方处理
    return None, None, object_key