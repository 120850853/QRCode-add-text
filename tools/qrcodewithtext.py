from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.file.file import File

import requests
import cv2
import numpy as np
import base64

from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

class QrcodewithtextTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        #print("QrcodewithtextTool invoked")
        print(tool_parameters)

        #获得tool_parameters中的url
        file_url = tool_parameters["image"].url
        text = tool_parameters["text"]

        image_url = f"http://localhost{file_url}"

        print("image_url",image_url)


        # 下载图片
        response = requests.get(image_url)
        response.raise_for_status()
        image_array = np.frombuffer(response.content, np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        # 将 OpenCV 图像转换为 Pillow 图像
        image_height, image_width, _ = image.shape
        new_image_height = image_height + 50
        new_image = np.full((new_image_height, image_width, 3), 255, dtype=np.uint8)
        new_image[:image_height, :] = image
        pil_image = Image.fromarray(new_image)

        # 加载支持汉字的字体文件
        import platform

        # 根据操作系统选择字体路径
        if platform.system() == "Darwin":  # macOS
            font_path = "/System/Library/Fonts/Supplemental/Songti.ttc"
        elif platform.system() == "Linux":  # Ubuntu
            font_path = "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"
        else:
            raise OSError("Unsupported operating system")
        try:
            font = ImageFont.truetype(font_path, size=32)
        except OSError as e:
            raise OSError(f"Failed to load font from path: {font_path}. Ensure the font file exists and the path is correct. Original error: {e}")

        # 绘制文字
        draw = ImageDraw.Draw(pil_image)
        # 计算文字边框信息
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_x = (image_width - text_width) // 2
        text_y = image_height + 10
        draw.text((text_x, text_y), text, font=font, fill=(0, 0, 0))

        # 保存图片到文件
        buffered = BytesIO()
        pil_image.save(buffered, format="PNG")
        buffered.seek(0)
        image_bytes = buffered.read()

        # 包含图片字节和元数据的响应
        yield self.create_blob_message(
            image_bytes,
            meta={"mime_type": "image/png"}
        )
