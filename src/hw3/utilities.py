from collections import Counter


def get_verbosity(df_arr):
    d = {"twilight": 0,
         "applejack": 0,
         "rarity": 0,
         "pinkie": 0,
         "rainbow": 0,
         "fluttershy": 0}
    names = {"Twilight Sparkle": "twilight",
             "Applejack": "applejack",
             "Rainbow Dash": "rainbow",
             "Pinkie Pie": "pinkie",
             "Rarity": "rarity",
             "Fluttershy": "fluttershy"}
    total_cnt = 0
    for df in df_arr:
        for _, row in df.iterrows():
            total_cnt += 1
            if row["pony"] in names:
                d[names[row["pony"]]] += 1
    #for k in d.keys():
    #    d[k] = round(d[k] / total_cnt,2)
    return count_dict_to_percent_dict(d)

def get_mentions(df_arr):
    d = {"twilight": {"applejack": 0,
                      "rarity": 0,
                      "pinkie": 0,
                      "rainbow": 0,
                      "fluttershy": 0},
         "applejack": {"twilight": 0,
                       "rarity": 0,
                       "pinkie": 0,
                       "rainbow": 0,
                       "fluttershy": 0},
         "rarity": {"twilight": 0,
                    "applejack": 0,
                    "pinkie": 0,
                    "rainbow": 0,
                    "fluttershy": 0},
         "pinkie": {"twilight": 0,
                    "applejack": 0,
                    "rarity": 0,
                    "rainbow": 0,
                    "fluttershy": 0},
         "rainbow": {"twilight": 0,
                     "applejack": 0,
                     "rarity": 0,
                     "pinkie": 0,
                     "fluttershy": 0},
         "fluttershy": {"twilight": 0,
                        "applejack": 0,
                        "rarity": 0,
                        "pinkie": 0,
                        "rainbow": 0}}
    names_speaker = {"Twilight Sparkle": "twilight",
                     "Applejack": "applejack",
                     "Rainbow Dash": "rainbow",
                     "Pinkie Pie": "pinkie",
                     "Rarity": "rarity",
                     "Fluttershy": "fluttershy"}
    names_called = {"Twilight": "twilight",
                    "Sparkle": "twilight",
                    "Applejack": "applejack",
                    "Rainbow": "rainbow",
                    "Dash": "rainbow",
                    "Pinkie": "pinkie",
                    "Pie": "pinkie",
                    "Rarity": "rarity",
                    "Fluttershy": "fluttershy"}
    for df in df_arr:
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


def get_follow_on(df_arr):
    d = {"twilight": {"applejack": 0,
                      "rarity": 0,
                      "pinkie": 0,
                      "rainbow": 0,
                      "fluttershy": 0,
                      "other": 0},
         "applejack": {"twilight": 0,
                       "rarity": 0,
                       "pinkie": 0,
                       "rainbow": 0,
                       "fluttershy": 0,
                       "other": 0},
         "rarity": {"twilight": 0,
                    "applejack": 0,
                    "pinkie": 0,
                    "rainbow": 0,
                    "fluttershy": 0,
                    "other": 0},
         "pinkie": {"twilight": 0,
                    "applejack": 0,
                    "rarity": 0,
                    "rainbow": 0,
                    "fluttershy": 0,
                    "other": 0},
         "rainbow": {"twilight": 0,
                     "applejack": 0,
                     "rarity": 0,
                     "pinkie": 0,
                     "fluttershy": 0,
                     "other": 0},
         "fluttershy": {"twilight": 0,
                        "applejack": 0,
                        "rarity": 0,
                        "pinkie": 0,
                        "rainbow": 0,
                        "other": 0}}
    names = {"Twilight Sparkle": "twilight",
             "Applejack": "applejack",
             "Rainbow Dash": "rainbow",
             "Pinkie Pie": "pinkie",
             "Rarity": "rarity",
             "Fluttershy": "fluttershy"}
    for df in df_arr:
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


def get_non_dict_words(df_arr, dictionary):
    d = {"twilight": Counter(),
         "applejack": Counter(),
         "rarity": Counter(),
         "pinkie": Counter(),
         "rainbow": Counter(),
         "fluttershy": Counter()}
    names = {"Twilight Sparkle": "twilight",
             "Applejack": "applejack",
             "Rainbow Dash": "rainbow",
             "Pinkie Pie": "pinkie",
             "Rarity": "rarity",
             "Fluttershy": "fluttershy"}
    for df in df_arr:
        for _, row in df.iterrows():
            words = row["dialog"]
            if row["pony"] in names:
                speaker = names[row["pony"]]
                for w in words:
                    if w.lower() not in dictionary:
                        d[speaker][w.lower()] += 1
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
            d[k] = round(d[k] / sm,2)
    return d
