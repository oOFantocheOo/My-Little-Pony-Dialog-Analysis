import argparse
import json
import sys

from hw3.file_handling import *
from hw3.utilities import *

script_dir = osp.dirname(__file__)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("src_file", help="csv file of ponies' dialogs to be analyzed.")
    parser.add_argument("-o", default="", help="Where should the output json file be generated? If not provided, print to stdout")
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    #src_file = osp.join(script_dir, "..", "data", "clean_dialog.csv")
    src_file=args.src_file
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
    if not args.o:
        print(final_json)
    else:
        dictionary={"verbosity": verbosity,
                    "mentions": mentions,
                    "follow_on_comments": follow,
                    "non_dictionary_words": non_dict}
        with open(args.o, 'w', encoding='utf-8') as f:
            json.dump(dictionary, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
