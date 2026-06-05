from collections.abc import Generator
from typing import Any

from qcloud_cos import CosConfig, CosS3Client
from qcloud_cos.cos_exception import CosServiceError

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from .utils import parse_cos_url


class GeneratePresignedDownloadUrlTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        try:
            # 从 runtime credentials 获取认证信息
            credentials = {
                'region': self.runtime.credentials.get('region'),
                'bucket': self.runtime.credentials.get('bucket'),
                'secret_id': self.runtime.credentials.get('secret_id'),
                'secret_key': self.runtime.credentials.get('secret_key')
            }

            # 验证认证信息
            self._validate_credentials(credentials)

            # 生成预签名下载 URL
            result = self._generate_download_url(tool_parameters, credentials)

            # 返回 JSON 响应
            yield self.create_json_message(result)

            # 返回文本响应
            success_message = "Presigned download URL generated successfully!\n"
            success_message += f"Presigned URL: {result['presigned_url']}\n"
            success_message += f"Object key: {result['object_key']}\n"
            success_message += f"Bucket: {result['bucket']}\n"
            success_message += f"Region: {result['region']}\n"
            success_message += f"Expired: {result['expired']} seconds\n"
            success_message += f"Method: {result['method']}"
            yield self.create_text_message(success_message)
        except Exception as e:
            error_message = str(e)

            # 返回文本错误响应
            yield self.create_text_message(f"Failed to generate presigned download URL: {error_message}")

    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        # 验证必填字段是否存在
        required_fields = ['region', 'bucket', 'secret_id', 'secret_key']
        for field in required_fields:
            if field not in credentials or not credentials[field]:
                raise ValueError(f"Missing required credential: {field}")

    def _generate_download_url(self, parameters: dict[str, Any], credentials: dict[str, Any]) -> dict:
        try:
            # 获取参数
            file_url = parameters.get('file_url')
            object_key_param = parameters.get('object_key')
            expired = parameters.get('expired', 300)

            # 优先使用 file_url 解析
            if file_url:
                # 解析 URL 获取 bucket、region 和 object_key
                url_bucket, url_region, object_key = parse_cos_url(file_url)

                # 如果 URL 中的 bucket 与凭证中的 bucket 不一致，使用 URL 中的 bucket
                if url_bucket and url_bucket != credentials['bucket']:
                    bucket_name = url_bucket
                else:
                    bucket_name = credentials['bucket']

                # 如果 URL 中的 region 与凭证中的 region 不一致，使用 URL 中的 region
                if url_region and url_region != credentials['region']:
                    region_name = url_region
                else:
                    region_name = credentials['region']
            elif object_key_param:
                # 使用 object_key 参数
                bucket_name = credentials['bucket']
                region_name = credentials['region']
                object_key = object_key_param
            else:
                raise ValueError("Missing required parameter: either file_url or object_key must be provided")

            # 创建腾讯云 COS 客户端
            config = CosConfig(
                Region=region_name,
                SecretId=credentials['secret_id'],
                SecretKey=credentials['secret_key']
            )
            client = CosS3Client(config)

            # 生成预签名下载 URL
            url = client.get_presigned_download_url(
                Bucket=bucket_name,
                Key=object_key,
                Expired=int(expired)
            )

            # 构建文件 URL
            file_url_display = f"https://{bucket_name}.cos.{region_name}.myqcloud.com/{object_key}"

            # 返回结果字典
            return {
                'presigned_url': url,
                'file_url': file_url_display,
                'object_key': object_key,
                'bucket': bucket_name,
                'region': region_name,
                'expired': int(expired),
                'method': 'GET',
                'status': 'success'
            }
        except CosServiceError as e:
            error_message = f"COS service error: {str(e)}"
            raise ValueError(error_message)
        except Exception as e:
            error_message = f"Failed to generate presigned download URL: {str(e)}"
            raise ValueError(error_message)
