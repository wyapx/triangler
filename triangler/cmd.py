import argparse
import os.path
from typing import Optional

import triangler

from triangler.edge_detectors import EdgeDetector
from triangler.renderers import Renderer
from triangler.samplers import Sampler

from triangler.config import TrianglerConfig


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("input", type=str, help="Input image")
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Output image name",
    )

    parser.add_argument(
        "-p",
        "--points",
        type=int,
        default=1024,
        help="Number of sample points to use",
    )
    parser.add_argument(
        "-e",
        "--edge-detector",
        type=str,
        default="sobel",
        choices=EdgeDetector,
        help="Edge detection algorithm",
    )
    parser.add_argument(
        "-s",
        "--sampler",
        type=str,
        default="poisson_disk",
        choices=Sampler,
        help="Point sampling algorithm",
    )
    parser.add_argument(
        "-r",
        "--renderer",
        type=str,
        default="centroid",
        choices=Renderer,
        help="Color polygon rendering algorithm",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"triangler {triangler.__version__}",
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Enable debug mode",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    triangler_config = TrianglerConfig(
        n_samples=args.points,
        edge_detector=EdgeDetector(args.edge_detector),
        sampler=Sampler(args.sampler),
        renderer=Renderer(args.renderer),
    )

    triangler.convert(
        args.input,
        (
            args.output
            or f"{os.path.dirname(args.input)}/triangler-{os.path.basename(args.input)}"
        ),
        config=triangler_config,
        debug=args.debug,
    )
