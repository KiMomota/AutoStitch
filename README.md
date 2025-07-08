# AutoStitch Project

## Overview
AutoStitch is a Python project designed for stitching images together seamlessly. It utilizes advanced computer vision techniques to match features, compensate for exposure differences, and blend images into a final composite. This project is particularly useful for creating panoramic images from multiple photographs.

## Features
- **Image Stitching**: Combines multiple images into a single panoramic image.
- **Feature Matching**: Uses various algorithms to identify and match features across images.
- **Exposure Compensation**: Adjusts for differences in exposure between images to create a uniform final output.
- **Image Blending**: Smoothly blends overlapping areas of images to eliminate seams.

## File Structure
```
AutoStitch
├── src
│   ├── main.py          # Main functionality for stitching images
│   ├── Constant.py      # Constants used throughout the project
│   └── __init__.py      # Marks the directory as a Python package
├── requirements.txt      # Lists project dependencies
└── README.md             # Project documentation
```

## Installation
To run the AutoStitch project, you need to have Python installed on your machine. Additionally, you will need to install the required dependencies listed in `requirements.txt`.

1. Clone the repository:
   ```
   git clone <repository-url>
   cd AutoStitch
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage
To use the AutoStitch functionality, run the `main.py` script with the path to the directory containing the images you want to stitch:

```
python src/main.py
```

Make sure to replace `src/main.py` with the correct path if you are executing from a different directory.

## Contributing
Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.