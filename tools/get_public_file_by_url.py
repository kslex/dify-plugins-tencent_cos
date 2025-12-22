import os
import re
import requests
from urllib.parse import urlparse, unquote
from typing import Any, Dict, Optional, Generator
from dify_plugin.entities.tool import ToolInvokeMessage

from dify_plugin.interfaces.tool import Tool, ToolProvider
from .utils import get_extension_from_content_type


class GetPublicFileByUrlTool(Tool):
    def _invoke(self, tool_parameters: Dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        try:
            # 执行文件获取操作
            result = self._get_public_file_by_url(tool_parameters)
            
            # 提取文件扩展名
            _, extension = os.path.splitext(result['filename'])
            if not extension:
                # 如果没有扩展名，根据content_type尝试推断
                extension = get_extension_from_content_type(result['content_type'])
                
                # 如果推断出了扩展名，添加到文件名中
                if extension:
                    result['filename'] = result['filename'] + extension
            
            # 规范化 content_type：若为 application/octet-stream，则根据文件名推断
            content_type = result['content_type'] or 'application/octet-stream'
            if content_type in ('application/octet-stream', 'binary/octet-stream'):
                import mimetypes
                guessed, _ = mimetypes.guess_type(result['filename'])
                if guessed:
                    content_type = guessed
            
            # 构建文件元数据，确保包含支持图片显示的所有必要属性
            file_metadata = {
                'filename': result['filename'],
                'content_type': content_type,
                'size': result['file_size'],
                'mime_type': content_type,
                'extension': extension
            }
            
            # 如果是图片类型，添加特定标志以确保在Dify页面正常显示
            if content_type.startswith('image/'):
                file_metadata['is_image'] = True
                file_metadata['display_as_image'] = True
                file_metadata['type'] = 'image'
            
            # 使用create_blob_message返回文件内容
            yield self.create_blob_message(
                result['file_content'],
                file_metadata
            )
            
            # 在text中输出成功消息、文件大小和类型，文件大小以MB为单位 - 英文消息
            file_size_mb = result['file_size'] / (1024 * 1024) if result['file_size'] > 0 else 0
            success_message = f"Public file downloaded successfully: {result['filename']}\nFile size: {file_size_mb:.2f} MB\nFile type: {content_type}"
            yield self.create_text_message(success_message)
        except Exception as e:
            # 失败时在text中输出错误信息 - 英文消息
            yield self.create_text_message(f"Failed to download public file: {str(e)}")
    
    def _get_public_file_by_url(self, parameters: dict[str, Any]) -> dict:
        try:
            # 获取文件URL
            file_url = parameters.get('file_url')
            
            if not file_url:
                raise ValueError("Missing required parameter: file_url")
            
            # 验证URL格式
            parsed_url = urlparse(file_url)
            if not parsed_url.scheme or not parsed_url.netloc:
                raise ValueError("Invalid URL format")
            
            # 发送HTTP请求获取文件
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(file_url, headers=headers, stream=True, timeout=30)
            response.raise_for_status()
            
            # 读取文件内容
            file_content = response.content
            
            # 获取文件大小
            file_size = len(file_content)
            
            # 获取文件类型
            content_type = response.headers.get('Content-Type', 'application/octet-stream')
            
            # 从URL或Content-Disposition头获取文件名
            filename = self._extract_filename_from_url(file_url)
            
            # 尝试从Content-Disposition头获取文件名
            content_disposition = response.headers.get('Content-Disposition')
            if content_disposition:
                filename = self._extract_filename_from_content_disposition(content_disposition, filename)
            
            # 返回结果字典
            return {
                'file_content': file_content,
                'filename': filename,
                'content_type': content_type,
                'file_size': file_size
            }
        except requests.exceptions.RequestException as e:
            error_message = f"HTTP request error: {str(e)}"
            raise ValueError(error_message)
        except Exception as e:
            error_message = f"Failed to retrieve public file: {str(e)}"
            raise ValueError(error_message)
    
    def _extract_filename_from_url(self, url: str) -> str:
        """从URL中提取文件名"""
        parsed_url = urlparse(url)
        # 处理URL编码
        filename = unquote(os.path.basename(parsed_url.path))
        
        # 如果无法从路径获取文件名，尝试从整个URL中提取
        if not filename or filename == '/':
            # 移除查询参数和片段
            clean_url = parsed_url._replace(query="", fragment="").geturl()
            filename = os.path.basename(clean_url)
        
        # 如果仍然没有有效的文件名，使用默认名称
        if not filename or filename == '/':
            filename = "downloaded_file"
        
        return filename
    
    def _extract_filename_from_content_disposition(self, content_disposition: str, default_filename: str) -> str:
        """从Content-Disposition头中提取文件名"""
        try:
            # 查找filename参数
            if 'filename=' in content_disposition:
                # 分割Content-Disposition字符串
                parts = content_disposition.split(';')
                for part in parts:
                    part = part.strip()
                    if part.startswith('filename='):
                        # 提取文件名，处理引号
                        filename = part[len('filename='):].strip()
                        if filename.startswith('"') and filename.endswith('"'):
                            filename = filename[1:-1]
                        elif filename.startswith("'") and filename.endswith("'"):
                            filename = filename[1:-1]
                        
                        # 处理URL编码
                        filename = unquote(filename)
                        
                        if filename:
                            return filename
        except Exception:
            # 如果解析失败，返回默认文件名
            pass
        
        return default_filename