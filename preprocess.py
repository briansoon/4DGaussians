from argparse import ArgumentParser
from utils.system_utils import run_command

def preprocess(scene, group):
    print(f"Preprocessing scene: {scene}\n")

    data_path = f"data/{group}/{scene}"

    if group == "dynerf":
        # First, extract the frames of each video.
        preprocess_cmd = [
            "python", "scripts/preprocess_dynerf.py", 
            "--datadir", f"{data_path}"
        ]
        run_command(preprocess_cmd)

    # Second, generate point clouds from input data.
    colmap_cmd = [
        "bash", "colmap.sh", 
        f"{data_path}", "llff"
    ]
    run_command(colmap_cmd)

    # Third, downsample the point clouds generated in the second step.
    downsample_cmd = [
        "python", "scripts/downsample_point.py", 
        f"{data_path}/colmap/dense/workspace/fused.ply", 
        f"{data_path}/points3D_downsample2.ply"
    ]
    run_command(downsample_cmd)

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
        preprocess(scene, group)

if __name__ == "__main__":
    # Set up command line argument parser
    # parser = ArgumentParser(description="Preprocess script parameters")
    # parser.add_argument()
    # args = parser.parse_known_args()

    # Dataset preprocess
    main()
