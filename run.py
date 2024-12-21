import json
import os
import sys
from datetime import datetime
from pathlib import Path

from PIL import ImageFilter, ImageEnhance, Image


def parse_parameters(param_str):
    """
    Parse string to return a dict i.e. "radius=1,percent=65,threshold=2" => {"radius": 1, "percent": 65, "threshold": 2}
    :param str param_str:
    :return dict:
    """
    params = dict(item.split('=') for item in param_str.split(','))
    return {key: float(value) if '.' in value else int(value) for key, value in params.items()}


def enhance(img, contrast, color, brightness, filter_params, filename, quality):
    """
    Enhance image quality based on params
    :param Image.Image img: i.e. image.jpg
    :param float contrast: i.e. 1.4
    :param float color: i.e.  1.4
    :param float brightness: 0.75
    :param str filter_params: i.e.  {"radius": 1, "percent": 65, "threshold": 2}
    :param str filename: i.e. file.jpg
    :param int quality: i.e. 100
    :return: void
    """
    contrast_enhancer = ImageEnhance.Contrast(img)
    img = contrast_enhancer.enhance(contrast)  # Increase contrast slightly more

    color_enhancer = ImageEnhance.Color(img)
    img = color_enhancer.enhance(color)

    brightness_enhancer = ImageEnhance.Brightness(img)
    img = brightness_enhancer.enhance(brightness)

    umask_params = parse_parameters(filter_params)
    img = img.filter(ImageFilter.UnsharpMask(**umask_params))

    now = datetime.now()
    # Format datetime as yyyymmddhis
    timestamp = now.strftime("%Y%m%d%H%M%S")
    output_path_improved = f"output/{timestamp}{filename}.jpg"
    img.save(output_path_improved, quality=quality)  # Save with high quality to maintain resolution
    print(output_path_improved)


def validate_umask_input(param_str):
    """
    Validates the input string for UnsharpMask parameters.
    :param str param_str:
    :return: str
    :raise ValueError: If the input is invalid or parameters are out of acceptable ranges.
    """
    try:
        if param_str.startswith('{') and param_str.endswith('}'):
            params = json.loads(param_str)
        else:
            params = dict(item.split('=') for item in param_str.split(','))
            params = {key: float(value) if '.' in value else int(value) for key, value in params.items()}

        # Required keys
        required_keys = {'radius', 'percent', 'threshold'}
        if not required_keys.issubset(params):
            raise ValueError(f"Missing required parameters. Expected keys: {required_keys}")

        # Validate ranges
        if not (0.1 <= params['radius'] <= 250):
            raise ValueError("Radius must be between 0.1 and 250.")
        if not (0 <= params['percent'] <= 500):
            raise ValueError("Percent must be between 0 and 500.")
        if not (0 <= params['threshold'] <= 255):
            raise ValueError("Threshold must be between 0 and 255.")

        return param_str
    except Exception as e:
        raise ValueError(f"Invalid input: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 7:
        print(
            "Usage: py run.py <image_path: str> <contrast: float> <color: float> <brightness: float> <quality: int> "
            "<umask: str> ")
        sys.exit(1)

    args = sys.argv

    filename = Path(args[1]).name
    contrast = float(args[2])  # 1.4
    color = float(args[3])  # 1.4
    brightness = float(args[4])  # 0,75
    quality = int(args[5])  # 100
    umask = validate_umask_input(args[6])

    if os.path.isdir(args[1]):
        print(f"{args[1]} is a folder.")
        for file in Path(args[1]).rglob("*"):  # Use "*.*" to match files with extensions
            if file.is_file():
                image = Image.open(file)
                enhance(image, contrast, color, brightness, umask, file.name, quality)
    elif os.path.isfile(args[1]):
        image = Image.open(args[1])
        filename = Path(args[1]).name
        enhance(image, contrast, color, brightness, umask, filename, quality)
    else:
        raise Exception(f"Cannot parse input. {args[1]}")
