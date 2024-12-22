# Image Enhancement Script

This Python script enhances images by adjusting contrast, color saturation, brightness, and applying an unsharp mask filter. It can process a single image or all images within a directory.

## Features

- **Contrast Enhancement**: Adjust the image's contrast.
- **Color Enhancement**: Boost or reduce color saturation.
- **Brightness Adjustment**: Lighten or darken the image.
- **Unsharp Mask Filter**: Sharpen the image with configurable parameters (`radius`, `percent`, `threshold`).
- **Batch Processing**: If a folder path is provided, the script will enhance all images in that folder (including subfolders).
- **Customizable Quality**: You can set the output image quality (e.g., 100 for the highest quality).

## Prerequisites

1. **Python >= 3.7+**
2. **Pillow** (Python Imaging Library)
   ```bash
   pip install pillow
   ```

## Usage

```bash
python run.py <image_path_or_directory> <contrast> <color> <brightness> <quality> <umask>
```

Where:

1. **image_path_or_directory** (`str`):
    - Path to a single image file (e.g., `image.jpg`)
    - or a directory containing multiple images.
2. **contrast** (`float`):
    - Multiplier for contrast enhancement. E.g., `1.4` means 40% increase over the default.
3. **color** (`float`):
    - Multiplier for color enhancement. E.g., `1.4` means 40% more vivid colors.
4. **brightness** (`float`):
    - Multiplier for brightness. E.g., `0.75` makes the image 25% darker.
5. **quality** (`int`):
    - Output image quality (1–100). E.g., `100` for best quality.
6. **umask** (`str`):
    - Parameters for the unsharp mask in one of the following formats:
        - **JSON string** (e.g., `{"radius": 1, "percent": 65, "threshold": 2}`), or
        - **Comma-separated string** (e.g., `radius=1,percent=65,threshold=2`).

### Valid Ranges

- **radius**: Must be between `0.1` and `250`.
- **percent**: Must be between `0` and `500`.
- **threshold**: Must be between `0` and `255`.

### Example Commands

1. **Single Image**
   ```bash
   python run.py "image.jpg" 1.4 1.4 0.75 100 "radius=1,percent=65,threshold=2"
   ```
   This command will:
    - Open `image.jpg`
    - Increase contrast and color by 40%
    - Decrease brightness to 75% of the original
    - Apply an unsharp mask with radius=1, percent=65, threshold=2
    - Save the enhanced image in the `output` folder with a timestamp in the filename

2. **Multiple Images in a Folder**
   ```bash
   python run.py "/path/to/images" 1.4 1.4 0.75 100 "radius=2,percent=100,threshold=4"
   ```
   This command will:
    - Look for all images in `/path/to/images` (including subfolders)
    - Apply the specified enhancements and unsharp mask
    - Save each enhanced image in the `output` folder with unique timestamped filenames

## Script Details

1. **parse_parameters(param_str)**
    - Parses a comma-separated string (e.g., `"radius=1,percent=65,threshold=2"`) into a dictionary of numeric values.

2. **validate_umask_input(param_str)**
    - Validates and returns the unsharp mask parameter string, ensuring all required keys (`radius`, `percent`, `threshold`) are present and within valid ranges.

3. **enhance(img, contrast, color, brightness, filter_params, filename, quality)**
    - Takes a Pillow `Image` object and applies contrast, color, brightness, and unsharp mask filter settings.
    - Saves the resulting image with a timestamped filename in an `output` folder.

4. **Main Section**
    - Parses command-line arguments.
    - Validates inputs.
    - Processes either a single image or all images in a directory.

## Notes & Tips

- If the input is a directory, the script iterates over all files in the directory (and its subdirectories).
- Ensure that the `output` folder exists in the script directory or you have permissions to create it.
- A timestamp (`YYYYMMDDHHMMSS`) is added to each output image’s filename for easy tracking.
- The script uses Pillow's `ImageEnhance` module to modify contrast, color, and brightness, and `ImageFilter.UnsharpMask` to apply the unsharp mask.

---

**Author**: uriencedric 
**License**: MIT Licence 