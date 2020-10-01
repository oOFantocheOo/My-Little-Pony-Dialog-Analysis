import argparse
import os.path as osp

import pandas as pd

script_dir = osp.dirname(__file__)


def main():
    parser = argparse.ArgumentParser()
    default_src_file = osp.join(script_dir, "..", "data", "clean_dialog.csv")
    parser.add_argument("--src_file", required=False, help="csv file to be analyzed",
                        default=default_src_file)
    args = parser.parse_args()
    print(default_src_file)

    src_file = args.src_file
    df = pd.read_csv(src_file)


if __name__ == "__main__":
    main()
