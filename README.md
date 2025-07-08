# AutoStitch:Panoramic Image Stitching

## Introduction
>This repository demonstrates the implementation of AutoStitch  in Python, based on the traditional image stitching pipeline using SIFT features  and RANSAC  for robust matching. We provide a variety of configurable parameters for key stages >including feature extraction , matching , seam estimation , and image blending . 

>Our method achieves state-of-the-art (SOTA)  performance when compared to both traditional and deep learning-based approaches. Unlike previous methods, users can input all images captured from a single scene, and the system will >automatically stitch them into a seamless panoramic image. 

>On an AMD 8845HS CPU , stitching 10 frames of 2K resolution images  takes less than 3 seconds . If you have access to a GPU, enable CUDA acceleration by setting the parameter try_cuda=True for improved performance. 

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
