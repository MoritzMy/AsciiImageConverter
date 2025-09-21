#!/usr/bin/env python3
# Converts an image to ASCII art and saves it as a new image file

from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import numpy as np
import argparse

def main():
    parser = argparse.ArgumentParser(description="Convert an image to ASCII art.")
    parser.add_argument("input_image", help="Path to the input image file.")
    parser.add_argument("output_image", default=".", help="Path to save the output ASCII art image.")
    parser.add_argument("--width", type=int, default=200, help="Width of the output image in characters.")
    parser.add_argument("--height", type=int, default=100, help="Height of the output image in characters.")
    args = parser.parse_args()

    # Load and resize image
    img = Image.open(args.input_image).convert("RGB")
    W, H = args.width, args.height
    img = img.resize((W, H))
    img = ImageEnhance.Color(img).enhance(1)
    pixel_arr = np.array(img) # 2D array of RGB values
    brightness = np.mean(pixel_arr, axis=2) # Averages RGB values

    cellsize = 6
    ascii_img = Image.new("RGB", (W * cellsize, H * cellsize), (0, 0, 0))
    draw = ImageDraw.Draw(ascii_img)
    font = ImageFont.load_default()

    # Brightness can be from 0 to 255, but i want it to be from 0 to 9

    char_list = [" ", ":", "+", "=", "§", "%", "$", "&", "#", "@"]
    scaled_brightness = ((brightness / 255) * (len(char_list) - 1)).astype(int) # Normalize to 0-9 and floor the Values

    for y in range(W):
        for x in range(H):
            char = char_list[scaled_brightness[x, y]]
            r, g, b = pixel_arr[x, y]
            draw.text((y * cellsize, x * cellsize), char, fill=(r, g, b), font=font)
            
    ascii_img.save(args.output_image)
    print(f"Successfully converted image to ASCII Art! Saved as {args.output_image}")

if __name__ == "__main__":
    main()