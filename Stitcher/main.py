from types import SimpleNamespace
import cv2
import numpy as np
import os
from Constant import *

def get_matcher(args):
    """
    Create a feature matcher based on the given arguments.
    """
    try_cuda = args.try_cuda
    matcher_type = args.matcher
    if args.match_conf is None:
        if args.features == 'orb':
            match_conf = 0.3
        else:
            match_conf = 0.65
    else:
        match_conf = args.match_conf
    range_width = args.rangewidth
    if matcher_type == "affine":
        matcher = cv.detail_AffineBestOf2NearestMatcher(False, try_cuda, match_conf)
    elif range_width == -1:
        matcher = cv.detail.BestOf2NearestMatcher_create(try_cuda, match_conf)
    else:
        pass
    return matcher

def get_compensator(args):
    """
    Create an exposure compensator based on the given arguments.
    """
    expos_comp_type = EXPOS_COMP_CHOICES[args.expos_comp]
    expos_comp_nr_feeds = args.expos_comp_nr_feeds
    expos_comp_block_size = args.expos_comp_block_size

    if expos_comp_type == cv.detail.ExposureCompensator_CHANNELS:
        compensator = cv.detail_ChannelsCompensator(expos_comp_nr_feeds)
    elif expos_comp_type == cv.detail.ExposureCompensator_CHANNELS_BLOCKS:
        compensator = cv.detail_BlocksChannelsCompensator(
            expos_comp_block_size, expos_comp_block_size,
            expos_comp_nr_feeds
        )
    else:
        compensator = cv.detail.ExposureCompensator_createDefault(expos_comp_type)
    return compensator


def main(path):
    """
    Main function for image stitching.

    Args:
        path (str): Path to the folder containing images to be stitched.

    Args details (args):
        try_cuda (bool): Whether to use CUDA acceleration if available.
        work_megapix (float): Resolution (in megapixels) for image feature extraction.
        features (str): Feature type to use ('orb', 'sift', etc.).
        matcher (str): Matcher type ('homography', 'affine', etc.).
        estimator (str): Camera parameter estimator type.
        match_conf (float or None): Confidence threshold for feature matching.
        conf_thresh (float): Confidence threshold for filtering matches.
        ba (str): Bundle adjustment cost function type.
        ba_refine_mask (str): Mask for bundle adjustment parameter refinement.
        wave_correct (str): Wave correction type ('horiz', 'vert', etc.).
        save_graph (str or None): Path to save the matches graph, or None to skip.
        warp (str): Warping type for image projection ('cylindrical', etc.).
        seam_megapix (float): Resolution (in megapixels) for seam estimation.
        seam (str): Seam finding method ('dp_color', etc.).
        compose_megapix (float): Resolution (in megapixels) for final composition.
        expos_comp (str): Exposure compensation method.
        expos_comp_nr_feeds (int): Number of exposure compensation feeds.
        expos_comp_nr_filtering (int): Number of exposure compensation filtering iterations.
        expos_comp_block_size (int): Block size for exposure compensation.
        blend (str): Blending method for panorama ('multiband', 'feather', etc.).
        blend_strength (int): Strength of blending.
        output (str): Output file name for the stitched result.
        timelapse (str or None): Timelapse mode ('as_is', 'crop', or None).
        rangewidth (int): Range width for matching (default -1 for all).
    """
    # Set default arguments for the stitching process
    args = {
        "try_cuda": True,
        "work_megapix": 0.6,
        "features": "orb",
        "matcher": "homography",
        "estimator": "homography",
        "match_conf": None,
        "conf_thresh": 1.0,
        "ba": "ray",
        "ba_refine_mask": "xxxxx",
        "wave_correct": 'horiz',
        "save_graph": None,
        "warp": 'cylindrical',
        "seam_megapix": 0.1,
        "seam": 'dp_color',
        "compose_megapix": 3,
        "expos_comp": "gain_blocks",
        "expos_comp_nr_feeds": 1,
        "expos_comp_nr_filtering": 2,
        "expos_comp_block_size": 32,
        "blend": 'multiband',
        "blend_strength": 5,
        "output": "time_test.jpg",
        "timelapse": None,
        "rangewidth": -1,
    }

    args = SimpleNamespace(**args)

    # Get all image file paths in the directory
    img_names = [path + '/' + folder for folder in os.listdir(path)]
    print(img_names)

    # Extract parameters from args
    work_megapix = args.work_megapix
    seam_megapix = args.seam_megapix
    compose_megapix = args.compose_megapix
    conf_thresh = args.conf_thresh
    ba_refine_mask = args.ba_refine_mask
    wave_correct = WAVE_CORRECT_CHOICES[args.wave_correct]
    if args.save_graph is None:
        save_graph = False
    else:
        save_graph = True
    warp_type = args.warp
    blend_type = args.blend
    blend_strength = args.blend_strength
    result_name = args.output

    # Timelapse mode check
    if args.timelapse is not None:
        timelapse = True
        if args.timelapse == "as_is":
            timelapse_type = cv.detail.Timelapser_AS_IS
        elif args.timelapse == "crop":
            timelapse_type = cv.detail.Timelapser_CROP
        else:
            print("Bad timelapse method")
            exit()
    else:
        timelapse = False

    finder = FEATURES_FIND_CHOICES[args.features]()
    seam_work_aspect = 1
    full_img_sizes = []
    features = []
    images = []
    is_work_scale_set = False
    is_seam_scale_set = False
    is_compose_scale_set = False

    # Read and preprocess all images
    for name in img_names:
        full_img = cv.imread(cv.samples.findFile(name))
        if full_img is None:
            exit()
        full_img_sizes.append((full_img.shape[1], full_img.shape[0]))
        if work_megapix < 0:
            img = full_img
            work_scale = 1
            is_work_scale_set = True
        else:
            if is_work_scale_set is False:
                work_scale = min(1.0, np.sqrt(work_megapix * 1e6 / (full_img.shape[0] * full_img.shape[1])))
                is_work_scale_set = True
            img = cv.resize(src=full_img, dsize=None, fx=work_scale, fy=work_scale, interpolation=cv.INTER_LINEAR_EXACT)
        if is_seam_scale_set is False:
            seam_scale = min(1.0, np.sqrt(seam_megapix * 1e6 / (full_img.shape[0] * full_img.shape[1])))
            seam_work_aspect = seam_scale / work_scale
            is_seam_scale_set = True
        img_feat = cv.detail.computeImageFeatures2(finder, img)
        features.append(img_feat)
        img = cv.resize(src=full_img, dsize=None, fx=seam_scale, fy=seam_scale, interpolation=cv.INTER_LINEAR_EXACT)
        images.append(img)

    # Feature matching
    matcher = get_matcher(args)
    p = matcher.apply2(features)
    matcher.collectGarbage()

    # Optionally save the matches graph
    if save_graph:
        with open(args.save_graph, 'w') as fh:
            fh.write(cv.detail.matchesGraphAsString(img_names, p, conf_thresh))

    # Keep only the largest connected component
    indices = cv.detail.leaveBiggestComponent(features, p, conf_thresh)
    img_subset = []
    img_names_subset = []
    full_img_sizes_subset = []
    for i in range(len(indices)):
        img_names_subset.append(img_names[indices[i]])
        img_subset.append(images[indices[i]])
        full_img_sizes_subset.append(full_img_sizes[indices[i]])
    images = img_subset
    img_names = img_names_subset
    full_img_sizes = full_img_sizes_subset
    num_images = len(img_names)
    if num_images < 2:
        print("Need more images")
        exit()

    # Estimate camera parameters
    estimator = ESTIMATOR_CHOICES[args.estimator]()
    b, cameras = estimator.apply(features, p, None)
    if not b:
        print("Homography estimation failed.")
        exit()
    for cam in cameras:
        # cam.R is the homography matrix of the image
        cam.R = cam.R.astype(np.float32)

    # Bundle adjustment
    adjuster = BA_COST_CHOICES[args.ba]()
    adjuster.setConfThresh(1)
    refine_mask = np.zeros((3, 3), np.uint8)
    if ba_refine_mask[0] == 'x':
        refine_mask[0, 0] = 1
    if ba_refine_mask[1] == 'x':
        refine_mask[0, 1] = 1
    if ba_refine_mask[2] == 'x':
        refine_mask[0, 2] = 1
    if ba_refine_mask[3] == 'x':
        refine_mask[1, 1] = 1
    if ba_refine_mask[4] == 'x':
        refine_mask[1, 2] = 1
    adjuster.setRefinementMask(refine_mask)
    b, cameras = adjuster.apply(features, p, cameras)
    if not b:
        print("Camera parameters adjusting failed.")
        exit()
    focals = []
    for cam in cameras:
        focals.append(cam.focal)
    focals.sort()

    # Calculate warped image scale
    if len(focals) % 2 == 1:
        warped_image_scale = focals[len(focals) // 2]
    else:
        warped_image_scale = (focals[len(focals) // 2] + focals[len(focals) // 2 - 1]) / 2

    # Wave correction
    if wave_correct is not None:
        rmats = []
        for cam in cameras:
            rmats.append(np.copy(cam.R))
        rmats = cv.detail.waveCorrect(rmats, wave_correct)
        for idx, cam in enumerate(cameras):
            cam.R = rmats[idx]

    corners = []
    masks_warped = []
    images_warped = []
    sizes = []
    masks = []
    for i in range(0, num_images):
        um = cv.UMat(255 * np.ones((images[i].shape[0], images[i].shape[1]), np.uint8))
        masks.append(um)

    # Warp images and masks
    warper = cv.PyRotationWarper(warp_type, warped_image_scale * seam_work_aspect)
    for idx in range(0, num_images):
        K = cameras[idx].K().astype(np.float32)
        swa = seam_work_aspect
        K[0, 0] *= swa
        K[0, 2] *= swa
        K[1, 1] *= swa
        K[1, 2] *= swa

        corner, image_wp = warper.warp(images[idx], K, cameras[idx].R, cv.INTER_LINEAR, cv.BORDER_REFLECT)
        corners.append(corner)
        sizes.append((image_wp.shape[1], image_wp.shape[0]))
        images_warped.append(image_wp)
        p, mask_wp = warper.warp(masks[idx], K, cameras[idx].R, cv.INTER_NEAREST, cv.BORDER_CONSTANT)
        masks_warped.append(mask_wp.get())

    # Convert warped images to float32 for seam finding
    images_warped_f = []
    for img in images_warped:
        imgf = img.astype(np.float32)
        images_warped_f.append(imgf)

    # Exposure compensation
    compensator = get_compensator(args)
    compensator.feed(corners=corners, images=images_warped, masks=masks_warped)

    # Seam finding
    seam_finder = SEAM_FIND_CHOICES[args.seam]
    masks_warped = seam_finder.find(images_warped_f, corners, masks_warped)

    compose_scale = 1
    corners = []
    sizes = []
    blender = None
    timelapser = None

    # Compose final panorama
    for idx, name in enumerate(img_names):
        full_img = cv.imread(name)
        if not is_compose_scale_set:
            if compose_megapix > 0:
                compose_scale = min(1.0, np.sqrt(compose_megapix * 1e6 / (full_img.shape[0] * full_img.shape[1])))
            is_compose_scale_set = True
            compose_work_aspect = compose_scale / work_scale
            warped_image_scale *= compose_work_aspect

            warper = cv.PyRotationWarper(warp_type, warped_image_scale)
            for i in range(0, len(img_names)):
                cameras[i].focal *= compose_work_aspect
                cameras[i].ppx *= compose_work_aspect
                cameras[i].ppy *= compose_work_aspect
                sz = (int(round(full_img_sizes[i][0] * compose_scale)),
                      int(round(full_img_sizes[i][1] * compose_scale)))
                K = cameras[i].K().astype(np.float32)
                roi = warper.warpRoi(sz, K, cameras[i].R)
                corners.append(roi[0:2])
                sizes.append(roi[2:4])

        if abs(compose_scale - 1) > 1e-1:
            img = cv.resize(src=full_img, dsize=None, fx=compose_scale, fy=compose_scale,
                            interpolation=cv.INTER_LINEAR_EXACT)
        else:
            img = full_img
        _img_size = (img.shape[1], img.shape[0])
        K = cameras[idx].K().astype(np.float32)

        corner, image_warped = warper.warp(img, K, cameras[idx].R, cv.INTER_LINEAR, cv.BORDER_REFLECT)
        mask = 255 * np.ones((img.shape[0], img.shape[1]), np.uint8)
        p, mask_warped = warper.warp(mask, K, cameras[idx].R, cv.INTER_NEAREST, cv.BORDER_CONSTANT)
        compensator.apply(idx, corners[idx], image_warped, mask_warped)
        image_warped_s = image_warped.astype(np.int16)
        dilated_mask = cv.dilate(masks_warped[idx], None)
        seam_mask = cv.resize(dilated_mask, (mask_warped.shape[1], mask_warped.shape[0]), 0, 0, cv.INTER_LINEAR_EXACT)

        mask_warped = cv.bitwise_and(seam_mask, mask_warped)
        # Blending
        if blender is None and not timelapse:
            # Create default blender
            blender = cv.detail.Blender_createDefault(cv.detail.Blender_NO, try_gpu=True)
            dst_sz = cv.detail.resultRoi(corners=corners, sizes=sizes)
            # Choose blending method
            blend_width = np.sqrt(dst_sz[2] * dst_sz[3]) * blend_strength / 100
            if blend_width < 1:
                blender = cv.detail.Blender_createDefault(cv.detail.Blender_NO)
            elif blend_type == "multiband":
                blender = cv.detail_MultiBandBlender()
                blender.setNumBands((np.log(blend_width) / np.log(2.) - 1.).astype(np.int64))
            elif blend_type == "feather":
                blender = cv.detail_FeatherBlender()
                blender.setSharpness(1. / blend_width)
            blender.prepare(dst_sz)
        elif timelapser is None and timelapse:
            timelapser = cv.detail.Timelapser_createDefault(timelapse_type)
            timelapser.initialize(corners, sizes)
        # Timelapse processing
        if timelapse:
            ma_tones = np.ones((image_warped_s.shape[0], image_warped_s.shape[1]), np.uint8)
            timelapser.process(image_warped_s, ma_tones, corners[idx])
            pos_s = img_names[idx].rfind("/")
            if pos_s == -1:
                fixed_file_name = "fixed_" + img_names[idx]
            else:
                fixed_file_name = img_names[idx][:pos_s + 1] + "fixed_" + img_names[idx][pos_s + 1:]
            cv.imwrite(fixed_file_name, timelapser.getDst())
        else:
            blender.feed(cv.UMat(image_warped_s), mask_warped, corners[idx])
    if not timelapse:
        result = None
        result_mask = None
        result, result_mask = blender.blend(result, result_mask)
        path = r"/AutoStitch/result.jpg"
        cv2.imwrite(path, result)

if __name__ == '__main__':
    import time
    start = time.time()
    path = r"/AutoStitch/images"
    main(path)
    end = time.time()

