import os.path as osp
import re

import pandas as pd

script_dir = osp.dirname(__file__)


def get_speech_act_df(df_all):
    '''
    df is expected to be read as pd.read_csv(clean_dialog.csv);
    output is a dataframe with 2 columns:
    List[DataFrame: ["pony": str, "dialog": List[str]] ],
    df separated by episode
    '''
    res = []
    episodes = df_all.title.unique()
    df_arr = [df_all[df_all['title'] == title] for title in episodes]

    for df in df_arr:
        pony = []
        dialog = []
        prev_char = ""
        for i, row in df.iterrows():
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
        res.append(pd.DataFrame(data=d))

    return res


def parse_words(dialog):
    '''
    Given a dialog, return an array of words in the dialog
    '''
    filtered_dialog = re.sub(r"<U\+\d{4}>", " ", dialog)
    arr = re.findall(r"\w+|[^\w\s]", filtered_dialog, re.UNICODE)
    for i in range(len(arr))[::-1]:
        if not arr[i].isalnum():
            arr.pop(i)
    return arr
