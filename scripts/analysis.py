import argparse
import json
import os.path as osp
import re
from collections import Counter

import pandas as pd

script_dir = osp.dirname(__file__)


def get_verbosity(df):
    d = {"twilight": 0,
         "applejack": 0,
         "rarity": 0,
         "pinky": 0,
         "rainbow": 0,
         "fluttershy": 0}
    names = {"Twilight Sparkle": "twilight",
             "Applejack": "applejack",
             "Rainbow Dash": "rainbow",
             "Pinkie Pie": "pinky",
             "Rarity": "rarity",
             "Fluttershy": "fluttershy"}
    for _, row in df.iterrows():
        if row["pony"] in names:
            d[names[row["pony"]]] += 1
    return count_dict_to_percent_dict(d)


def get_mentions(df):
    d = {"twilight": {"applejack": 0,
                      "rarity": 0,
                      "pinky": 0,
                      "rainbow": 0,
                      "fluttershy": 0},
         "applejack": {"twilight": 0,
                       "rarity": 0,
                       "pinky": 0,
                       "rainbow": 0,
                       "fluttershy": 0},
         "rarity": {"twilight": 0,
                    "applejack": 0,
                    "pinky": 0,
                    "rainbow": 0,
                    "fluttershy": 0},
         "pinky": {"twilight": 0,
                   "applejack": 0,
                   "rarity": 0,
                   "rainbow": 0,
                   "fluttershy": 0},
         "rainbow": {"twilight": 0,
                     "applejack": 0,
                     "rarity": 0,
                     "pinky": 0,
                     "fluttershy": 0},
         "fluttershy": {"twilight": 0,
                        "applejack": 0,
                        "rarity": 0,
                        "pinky": 0,
                        "rainbow": 0}}
    names_speaker = {"Twilight Sparkle": "twilight",
                     "Applejack": "applejack",
                     "Rainbow Dash": "rainbow",
                     "Pinkie Pie": "pinky",
                     "Rarity": "rarity",
                     "Fluttershy": "fluttershy"}

    names_called = {"Twilight": "twilight",
                    "Sparkle": "twilight",
                    "Applejack": "applejack",
                    "Rainbow": "rainbow",
                    "Dash": "rainbow",
                    "Pinkie": "pinky",
                    "Pie": "pinky",
                    "Rarity": "rarity",
                    "Fluttershy": "fluttershy"}

    for _, row in df.iterrows():
        if row["pony"] in names_speaker:
            words = row["dialog"]
            for w in words:
                if w in names_called:
                    speaker = names_speaker[row["pony"]]
                    called = names_called[w]
                    if speaker != called:
                        d[speaker][called] += 1
    for k in d.keys():
        d[k] = count_dict_to_percent_dict(d[k])
    return d


def get_follow_on(df):
    d = {"twilight": {"applejack": 0,
                      "rarity": 0,
                      "pinky": 0,
                      "rainbow": 0,
                      "fluttershy": 0,
                      "other": 0},
         "applejack": {"twilight": 0,
                       "rarity": 0,
                       "pinky": 0,
                       "rainbow": 0,
                       "fluttershy": 0,
                       "other": 0},
         "rarity": {"twilight": 0,
                    "applejack": 0,
                    "pinky": 0,
                    "rainbow": 0,
                    "fluttershy": 0,
                    "other": 0},
         "pinky": {"twilight": 0,
                   "applejack": 0,
                   "rarity": 0,
                   "rainbow": 0,
                   "fluttershy": 0,
                   "other": 0},
         "rainbow": {"twilight": 0,
                     "applejack": 0,
                     "rarity": 0,
                     "pinky": 0,
                     "fluttershy": 0,
                     "other": 0},
         "fluttershy": {"twilight": 0,
                        "applejack": 0,
                        "rarity": 0,
                        "pinky": 0,
                        "rainbow": 0,
                        "other": 0}}
    names = {"Twilight Sparkle": "twilight",
             "Applejack": "applejack",
             "Rainbow Dash": "rainbow",
             "Pinkie Pie": "pinky",
             "Rarity": "rarity",
             "Fluttershy": "fluttershy"}
    for idx, row in df.iterrows():
        if idx == 0:
            prev = names[row["pony"]] if row["pony"] in names else "other"
        else:
            if row["pony"] in names:
                d[names[row["pony"]]][prev] += 1
            prev = names[row["pony"]] if row["pony"] in names else "other"
    for k in d.keys():
        d[k] = count_dict_to_percent_dict(d[k])
    return d


def get_non_dict_words(df, dictionary):
    d = {"twilight": Counter(),
         "applejack": Counter(),
         "rarity": Counter(),
         "pinky": Counter(),
         "rainbow": Counter(),
         "fluttershy": Counter()}
    names = {"Twilight Sparkle": "twilight",
             "Applejack": "applejack",
             "Rainbow Dash": "rainbow",
             "Pinkie Pie": "pinky",
             "Rarity": "rarity",
             "Fluttershy": "fluttershy"}
    for _, row in df.iterrows():
        words = row["dialog"]
        if row["pony"] in names:
            speaker = names[row["pony"]]
            for w in words:
                if w.lower() not in dictionary:
                    d[speaker][w] += 1
    res = {}
    for k in d.keys():
        most_common_tuple = d[k].most_common(5)
        cur = [i[0] for i in most_common_tuple]
        res[k] = cur

    return res


def count_dict_to_percent_dict(d):
    '''
    Given a dict of count of each element,
    modifies the dict inplace, changing the count to percentage,
    returns the dict
    '''
    sm = sum(d[k] for k in d.keys())
    if sm == 0:
        for k in d.keys():
            d[k] = 0.0
    else:
        for k in d.keys():
            d[k] = d[k] / sm
    return d


def get_speech_act_df(df):
    '''
    df is expected to be read as pd.read_csv(clean_dialog.csv);
    output is a dataframe with 2 columns:
    "pony": str, "dialog": List[str]
    '''

    pony = []
    dialog = []
    prev_char = ""
    for i in range(df.shape[0]):
        cur_char = df["pony"][i]
        cur_dial = df["dialog"][i]
        if prev_char != cur_char:
            prev_char = cur_char
            pony.append(cur_char)
            dialog.append(cur_dial)
        else:
            dialog[-1] = dialog[-1] + " " + cur_dial
    for i in range(len(dialog)):
        dialog[i] = parse_words(dialog[i])
    d = {"pony": pony, "dialog": dialog}
    return pd.DataFrame(data=d)


def parse_words(dialog):
    '''
    Given a dialog, return an array of words in the dialog
    '''
    arr = re.findall(r"\w+|[^\w\s]", dialog, re.UNICODE)
    for i in range(len(arr))[::-1]:
        if not arr[i].isalnum():
            arr.pop(i)
    return arr


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
