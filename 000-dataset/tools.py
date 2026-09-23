
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

IMAGE_SIZE = (512, 512)
FONT_SIZE = 360

def generate_image(
        zi: str, 
        font_path: Path, 
        image_size=IMAGE_SIZE, 
        font_size=FONT_SIZE
        ) -> Image:
    """
    生成单个汉字的图片

    :param zi: 汉字
    :param font_path: 字体路径
    :param image_size: 图片大小
    :param font_size: 字体大小
    :return: PIL Image对象
    """
    assert len(zi) == 1, "只能生成单个汉字的图片"
    img = Image.new("L", image_size, color=255)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(str(font_path), font_size)
    draw.text((image_size[0] / 2, image_size[1] / 2), 
                          zi, font=font, fill=0, anchor="mm")
    return img

def batch_generate_images(
        zi_list: list[str],
        font_path: Path,
        output_path: Path,
        image_size=IMAGE_SIZE,
        font_size=FONT_SIZE
        ) -> tuple[list[Path], list[str]]:
    """
    批量生成汉字图片

    :param zi_list: 汉字列表
    :param font_path: 字体路径
    :param output_path: 输出路径
    :param image_size: 图片大小
    :param font_size: 字体大小
    :return: (生成成功的图片路径列表, 生成失败的汉字列表)
    """

    output_path.mkdir(parents=True, exist_ok=True)

    font = ImageFont.truetype(str(font_path), font_size)

    failed_zi = []
    image_paths = []

    for zi in zi_list:

        if len(zi) != 1:
            failed_zi.append(zi)
            continue
        try:
            img = Image.new("L", image_size, color=255)
            draw = ImageDraw.Draw(img)


            draw.text((image_size[0] / 2, image_size[1] / 2), 
                      zi, font=font, fill=0, anchor="mm")
            
            image_path = output_path / f"{ord(zi):04X}.png"
            img.save(image_path)

            image_paths.append(image_path)

        except Exception:  # noqa: BLE001
            failed_zi.append(zi)

    return image_paths, failed_zi