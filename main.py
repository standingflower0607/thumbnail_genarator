from PIL import Image, ImageDraw, ImageFont
import textwrap


class TooLongError(Exception):
    """Raised when title text is too long to genarate a thumbnail. That means it broke a design of thunmbnail due to the long text"""

    pass


def generateThunbnail(
    size=(1200, 630),
    color=(232, 232, 232),
    titleText="Pythonでアイキャッチ画像を自動生成する方法",
    font_size=80,
):
    img = Image.new("RGB", size, color)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("/System/Library/Fonts/ヒラギノ丸ゴ ProN W4.ttc", font_size)
    # 画像サイズ
    W, H = size
    # 全体のテキストサイズ
    all_w, all_h = draw.textsize(titleText, font=font)
    # サイドの余白
    horizontal_margin = 100
    vertical_margin = 20
    # サイドの余白を差し引いたときの画像サイズ
    container_width = W - horizontal_margin * 2
    container_height = H - vertical_margin * 2
    px_per_word = round(all_w / len(titleText))
    width = round(container_width / px_per_word)
    print(width)
    wrap_list = textwrap.wrap(titleText, width=width)
    print(wrap_list)
    line_counter = 0

    for line in wrap_list:

        w, h = draw.textsize(line, font=font)
        y = line_counter * (font_size + 10)
        coordinate_x = (W - w) / 2
        coordinate_y = ((H - all_h) / 2) - (len(wrap_list) - 1) * font_size + y

        if (
            coordinate_y <= vertical_margin
            or coordinate_y + font_size >= container_height
        ):
            raise TooLongError("This text is too long to generate a thumbnail")
        draw.multiline_text(
            (coordinate_x, coordinate_y), line, fill=(0, 0, 0), font=font,
        )
        line_counter += 1
    img.save("example.jpg", "JPEG", quality=100, optimize=True)


if __name__ == "__main__":
    generateThunbnail()
