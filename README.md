# AutoStitch:Panoramic Image Stitching

## Introduction
>This repository demonstrates the implementation of AutoStitch  in Python, based on the traditional image stitching pipeline using SIFT + RANSAC  for robust matching. We provide a variety of configurable parameters for key stages including feature extraction , matching , seam estimation , and image blending . 

>Our method achieves state-of-the-art (SOTA)  performance when compared to traditional / deep learning-based methods. users can input all images captured from a single scene, and automatically return seamless panoramic image. 

>On an AMD 8845HS CPU , stitching 10 frames of 2K resolution images takes less than 3 seconds . If you have access to a GPU, enable CUDA acceleration by setting the parameter try_cuda=True for improved performance.


## File Structure
```
AutoStitch
├── src
│   ├── main.py          # Main.py for stitching images
│   ├── Constant.py      # Constants used throughout the project
│   └── __init__.py      # Marks the directory as a Python package
├── requirements.txt      # Lists project dependencies
├── Src_images            # source images need to stitch
└── README.md             # Project documentation
```

## Installation
To run the AutoStitch project, you need to have Python installed on your machine. Additionally, you will need to install the required dependencies listed in `requirements.txt`.

1. Clone the repository:
   ```
   git clone https://github.com/KiMomota/AutoStitch.git
   cd AutoStitch
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage
To use the AutoStitch functionality, modify the path to the images you want to stitch. 
Then run the `main.py` script with the path to the directory containing the images you want to stitch:

```
python src/main.py
```

![f4f41e38-65cf-4b42-903c-fe8b7cfdda5e](https://github.com/user-attachments/assets/8fc7b8f9-313d-4f42-8894-d25d09cb1d1d)

## WebUI
We have provided a GUI for users to stitch images. Users can automatically adjust the parameters, and after selecting the input images, the image will display in panorama.
![b5cc9c11eadaa8d023671e7ae5755086](https://github.com/user-attachments/assets/1baf9c8f-9753-4870-aef1-5539c9ba1fef)



## FurtherMore
Furthermore, we will provide an end-to-end transformer-based model for image stitching. The code will become available after the paper is accepted.
You are welcome to contact me via email for any questions or suggestions.
If you find this project helpful, please consider giving it a star ⭐ on GitHub.

