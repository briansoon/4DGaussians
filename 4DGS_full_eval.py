import os
import subprocess
import time
from argparse import ArgumentParser

def preprocess(scene, group):
    print(f"Preprocessing scene: {scene}\n")

    if group == "dynerf":
        # First, extract the frames of each video.
        preprocess_cmd = [
            "python", "scripts/preprocess_dynerf.py", 
            "--datadir", f"data/{group}/{scene}"
        ]
        subprocess.run(preprocess_cmd, check=True)

    # Second, generate point clouds from input data.
    colmap_cmd = [
        "bash", "colmap.sh", 
        f"data/{group}/{scene}", "llff"
    ]
    subprocess.run(colmap_cmd, check=True)

    # Third, downsample the point clouds generated in the second step.
    downsample_cmd = [
        "python", "scripts/downsample_point.py", 
        f"data/{group}/{scene}/colmap/dense/workspace/fused.ply", 
        f"data/{group}/{scene}/points3D_downsample2.ply"
    ]
    subprocess.run(downsample_cmd, check=True)

def main():
    dnerf_scenes = ["bouncingballs", "hellwarrior", "hook", "jumpingjacks", "lego", "mutant", "standup", "trex"] 
    dynerf_scenes = ["coffee_martini", "cook_spinach", "cut_roasted_beef", "flame_salmon_1", "flame_steak", "sear_steak"]
    hynerf_intp_scenes = ["aleks-teapot", "chickchicken", "cut-lemon", 
                          "hand", "slice-banana", "torchocolate"]
    hynerf_misc_scenes = ["americano", "cross-hands", "espresso", "keyboard", 
                          "oven-mitts", "split-cookie", "tamping"]
    hynerf_vrig_scenes = ["3dprinter", "broom", "chicken", "peel-banana"]

    # dynerf_scenes = ["flame_salmon_1"]

    hynerf_scenes = []
    hynerf_scenes.extend(hynerf_intp_scenes)
    hynerf_scenes.extend(hynerf_misc_scenes)
    hynerf_scenes.extend(hynerf_vrig_scenes)

    all_scenes = []
    all_scenes.extend(dnerf_scenes)
    all_scenes.extend(dynerf_scenes)
    all_scenes.extend(hynerf_scenes)

    group = "dynerf"

    for scene in dynerf_scenes:
        train_time = 0.0
        if not args.synthetic:
            preprocess(scene, group)

        start_time = time.time()
        print(f"Training scene: {scene}\n")
        train_cmd = [
            "python", "train.py",
            "-s", f"data/{group}/{scene}", 
            "--expname", f"{group}/{scene}", 
            "--configs", f"arguments/{group}/{scene}.py"
        ]
        subprocess.run(train_cmd, check=True)
        train_time = (time.time() - start_time)/60.0

        # For time tracking
        train_time_str = f"Train Time : {train_time:.4f} minutes\n"

        # Output the time taken for each stage
        with open(os.path.join(f"output/{group}/{scene}", "train_time.txt"), 'w') as f:
            f.write(train_time_str)

        print(f"Rendering scene: {scene}\n")
        render_cmd = [
            "python", "render.py",
            "-m", f"output/{group}/{scene}/",
            "--skip_train",
            "--configs", f"arguments/{group}/{scene}.py"
        ]
        subprocess.run(render_cmd, check=True)

        print(f"Evaluating metrics for scene: {scene}\n")
        metrics_cmd = [
            "python", "metrics.py",
            "-m", f"output/{group}/{scene}/"
        ]
        subprocess.run(metrics_cmd, check=True)

if __name__ == "__main__":
    parser = ArgumentParser(description="Full evaluation scipt parameters")
    parser.add_argument('--synthetic', '-syn', action='store_true')
    args = parser.parse_args()
    main()
