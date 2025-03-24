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
from argparse import ArgumentParser

scenes = ["gardenspheres", "sedan", "toycar"]
rescales = [4, 8, 4]

parser = ArgumentParser(description="Full evaluation script parameters")
parser.add_argument("--skip_training", action="store_true")
parser.add_argument("--skip_rendering", action="store_true")
parser.add_argument("--skip_metrics", action="store_true")
parser.add_argument("--output_path", default="logs/ref_real")
parser.add_argument('--source', "-s", default="data/ref_real")
args, _ = parser.parse_known_args()

if not args.skip_training:
    common_args = " --eval --test_iterations -1"
    for scene, rescale in zip(scenes, rescales):
        source = f"{args.source}/{scene}"
        os.system(f"python train.py -s {source} -i images_{rescale} -m {args.output_path}/{scene} {common_args}")

if not args.skip_rendering:
    sources = []
    for scene in scenes:
        sources.append(f"{args.source}/{scene}")

    common_args = " --quiet --eval --skip_train --skip_mesh"
    for scene, source in zip(scenes, sources):
        os.system(f"python render.py --iteration 30000 -s {source} -m {args.output_path}/{scene} {common_args}")

if not args.skip_metrics:
    scenes_string = ""
    for scene in scenes:
        scenes_string += f" \"{args.output_path}/{scene}\""

    os.system("python metrics.py -m " + scenes_string)