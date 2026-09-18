#
# Copyright (C) 2023, Inria
# GRAPHDECO research group, https://team.inria.fr/graphdeco
# All rights reserved.
#
# This software is free for non-commercial, research and evaluation use 
# under the terms of the LICENSE.md file.
#
# For inquiries contact  george.drettakis@inria.fr
#

import os
import time
from argparse import ArgumentParser
from utils.system_utils import run_command

def main():
    # mipnerf360_outdoor_scenes = ["bicycle", "flowers", "garden", "stump", "treehill"]
    # mipnerf360_indoor_scenes = ["room", "counter", "kitchen", "bonsai"]
    # tanks_and_temples_scenes = ["truck", "train"]
    # deep_blending_scenes = ["drjohnson", "playroom"]
    dnerf_scenes = ["bouncingballs", "hellwarrior", "hook", "jumpingjacks", "lego", "mutant", "standup", "trex"] 
    dynerf_scenes = ["coffee_martini", "cook_spinach", "cut_roasted_beef", "flame_salmon_1", "flame_steak", "sear_steak"]
    hynerf_intp_scenes = ["aleks-teapot", "chickchicken", "cut-lemon", 
                          "hand", "slice-banana", "torchocolate"]
    hynerf_misc_scenes = ["americano", "cross-hands", "espresso", "keyboard", 
                          "oven-mitts", "split-cookie", "tamping"]
    hynerf_vrig_scenes = ["3dprinter", "broom", "chicken", "peel-banana"]

    hynerf_scenes = []
    hynerf_scenes.extend(hynerf_intp_scenes)
    hynerf_scenes.extend(hynerf_misc_scenes)
    hynerf_scenes.extend(hynerf_vrig_scenes)

    all_scenes = []
    # all_scenes.extend(mipnerf360_outdoor_scenes)
    # all_scenes.extend(mipnerf360_indoor_scenes)
    # all_scenes.extend(tanks_and_temples_scenes)
    # all_scenes.extend(deep_blending_scenes)
    all_scenes.extend(dnerf_scenes)
    all_scenes.extend(dynerf_scenes)
    all_scenes.extend(hynerf_scenes)

    group = "dynerf"

    # if not args.skip_training or not args.skip_rendering:
    #     parser.add_argument('--mipnerf360', "-m360", required=True, type=str)
    #     parser.add_argument("--tanksandtemples", "-tat", required=True, type=str)
    #     parser.add_argument("--deepblending", "-db", required=True, type=str)
    #     args = parser.parse_args()

    for scene in dynerf_scenes:
        if not args.skip_training:
            train_time = 0.0
            common_args = " --quiet --eval --test_iterations -1 "

            start_time = time.time()
            print(f"Training scene: {scene}\n")

            # for scene in mipnerf360_outdoor_scenes:
            #     source = args.mipnerf360 + "/" + scene
            #     os.system("python train.py -s " + source + " -i images_4 -m " + args.output_path + "/" + scene + common_args)
            # for scene in mipnerf360_indoor_scenes:
            #     source = args.mipnerf360 + "/" + scene
            #     os.system("python train.py -s " + source + " -i images_2 -m " + args.output_path + "/" + scene + common_args)
            # for scene in tanks_and_temples_scenes:
            #     source = args.tanksandtemples + "/" + scene
            #     os.system("python train.py -s " + source + " -m " + args.output_path + "/" + scene + common_args)
            # for scene in deep_blending_scenes:
            #     source = args.deepblending + "/" + scene
            #     os.system("python train.py -s " + source + " -m " + args.output_path + "/" + scene + common_args)
            train_cmd = [
                "python", "train.py",
                "-s", f"data/{group}/{scene}", 
                "--expname", f"{group}/{scene}", 
                "--configs", f"arguments/{group}/{scene}.py"
            ]
            run_command(train_cmd)
            train_time = (time.time() - start_time)/60.0

            # For time tracking
            train_time_str = f"Train Time : {train_time:.4f} minutes\n"
            
            # Output the time taken for each stage
            with open(os.path.join(f"{args.output_path}/{group}/{scene}", "train_time.txt"), 'w') as f:
                f.write(train_time_str)

        if not args.skip_rendering:
            # all_sources = []
            # # for scene in mipnerf360_outdoor_scenes:
            # #     all_sources.append(args.mipnerf360 + "/" + scene)
            # # for scene in mipnerf360_indoor_scenes:
            # #     all_sources.append(args.mipnerf360 + "/" + scene)
            # # for scene in tanks_and_temples_scenes:
            # #     all_sources.append(args.tanksandtemples + "/" + scene)
            # # for scene in deep_blending_scenes:
            # #     all_sources.append(args.deepblending + "/" + scene)
            # for scene in dnerf_scenes:
            #     all_sources.append(args.deepblending + "/" + scene)

            # common_args = " --quiet --eval --skip_train"
            # for scene, source in zip(all_scenes, all_sources):
            #     os.system("python render.py --iteration 7000 -s " + source + " -m " + args.output_path + "/" + scene + common_args)
            #     os.system("python render.py --iteration 30000 -s " + source + " -m " + args.output_path + "/" + scene + common_args)

            print(f"Rendering scene: {scene}\n")
            render_cmd = [
                "python", "render.py",
                "-m", f"output/{group}/{scene}/",
                "--skip_train",
                "--configs", f"arguments/{group}/{scene}.py"
            ]
            run_command(render_cmd)

        if not args.skip_metrics:
            # scenes_string = ""
            # for scene in all_scenes:
            #     scenes_string += "\"" + args.output_path + "/" + scene + "\" "

            # os.system("python metrics.py -m " + scenes_string)
            print(f"Evaluating metrics for scene: {scene}\n")
            metrics_cmd = [
                "python", "metrics.py",
                "-m", f"output/{group}/{scene}/"
            ]
            run_command(metrics_cmd)

if __name__ == "__main__":
    parser = ArgumentParser(description="Full evaluation script parameters")
    parser.add_argument("--skip_training", action="store_true")
    parser.add_argument("--skip_rendering", action="store_true")
    parser.add_argument("--skip_metrics", action="store_true")
    parser.add_argument("--output_path", default="./eval")
    args, _ = parser.parse_known_args()

    # Run full evaluation
    main()