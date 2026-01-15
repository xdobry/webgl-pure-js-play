from PIL import Image
import math
import sys

def charmap_to_png(
    input_file,
    output_file,
    chars_per_row=16,
    scale=4,
    invert=False,
    num_chars=255
):
    with open(input_file, "rb") as f:
        data = f.read()

    if len(data) % 8 != 0:
        raise ValueError("Input size is not a multiple of 8 bytes")

    rows = math.ceil(num_chars / chars_per_row)

    img_width = chars_per_row * 8
    img_height = rows * 8

    img = Image.new("L", (img_width, img_height), 0)
    pixels = img.load()

    for char_index in range(num_chars):
        char_x = (char_index % chars_per_row) * 8
        char_y = (char_index // chars_per_row) * 8

        for row in range(8):
            byte = data[char_index * 8 + row]

            for col in range(8):
                bit = (byte >> (7 - col)) & 1
                value = 255 if bit else 0
                if invert:
                    value = 255 - value

                pixels[char_x + col, char_y + row] = value

    # scale image for readability
    if scale != 1:
        img = img.resize(
            (img_width * scale, img_height * scale),
            Image.NEAREST
        )

    img.save(output_file)
    print(f"Saved {output_file} ({num_chars} characters)")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python font2png.py input.bin output.png")
        sys.exit(1)

    charmap_to_png(
        input_file=sys.argv[1],
        output_file=sys.argv[2],
        chars_per_row=16,
        scale=1
    )
