import argparse
import json

from hw3.file_handling import *
from hw3.utilities import *

script_dir = osp.dirname(__file__)


def main():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()


    src_file = osp.join(script_dir, "..", "data", "clean_dialog.csv")
    dict_words_path = osp.join(script_dir, "..", "data", "words_alpha.txt")
    dict_words = set()
    with open(dict_words_path) as file:
        for line in file:
            dict_words.add(line.strip())
    df = get_speech_act_df(pd.read_csv(src_file, na_filter=False))
    verbosity = get_verbosity(df)
    mentions = get_mentions(df)
    follow = get_follow_on(df)
    non_dict = get_non_dict_words(df, dict_words)
    final_json = json.dumps({"verbosity": verbosity,
                             "mentions": mentions,
                             "follow_on_comments": follow,
                             "non_dictionary_words": non_dict}, indent=2)
    print(final_json)
    with open("sample.json", "w") as outfile:
        outfile.write(final_json)


if __name__ == "__main__":
    main()
