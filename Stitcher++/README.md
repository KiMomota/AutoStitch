# Version
   VS2019 + OpenCV 4.4.0 + OpenCV Contrib 4.4.0 + CMake  

# Basic Parameters
    --preview: Enable preview mode (faster speed, lower output resolution)  
    --try_cuda (true | false): Use CUDA acceleration or not (default is false, set to true if a GPU is available)
    --work_megapix <float>: Resolution for feature extraction in megapixels (default: 0.6)
    --features (surf|orb|sift|akaze): Feature detection algorithm (default: surf, fallback to orb if unavailable)
    --match_conf <float>: Matching confidence threshold (surf default 0.65, orb default 0.3)
    --conf_thresh <float>: Panorama confidence threshold (default: 1.0)
    --warp (spherical|plane|...|mercator): Projection method (default: spherical)
    --wave_correct (no|horiz|vert): Wave distortion correction (default: horiz)
    --expos_comp (gain|gain_blocks|...): Exposure compensation method (default: gain_blocks)
    --blend (feather|multiband): Image blending method (default: multiband)
    --blend_strength <float>: Blending strength (range: 0–100, default: 5)
    --output <filename>: Output filename (default: result.jpg)
    --rangewidth <int>: Limit number of adjacent images to match (default: full matching)


# Stitcher++

After compilation, the executable Stitcher.exe will be generated in the following path:
./Stitcher/x64/Release/ 

Open a terminal in this directory and run the stitching command with your own image paths: 

>.\Stitcher.exe --features surf --work_megapix 0.6 --blend multiband --expos_comp gain --compose_megapix 0.3 D:\images\01.jpg D:\images\02.jpg >D:\images\03.jpg D:\images\04.jpg D:\images\05.jpg D:\images\06.jpg D:\images\07.jpg D:\images\08.jpg D:\images\09.jpg D:\images\10.jpg