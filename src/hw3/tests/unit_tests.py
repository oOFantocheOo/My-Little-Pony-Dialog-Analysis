import unittest

from hw3.file_handling import *
from hw3.utilities import *


class HW3TestCase(unittest.TestCase):
    def test_speech_act_1(self):
        d = {"pony": ["a", "a"], "dialog": ["1+1", "= 2"], "title": ["t", "t"]}
        df = pd.DataFrame(data=d)
        df_speech_act = get_speech_act_df(df)[0]
        self.assertEqual(df_speech_act.shape[0], 1)

    def test_speech_act_2(self):
        d = {"pony": ["a"], "dialog": ["1+1"], "title": ["t"]}
        df = pd.DataFrame(data=d)
        df_speech_act = get_speech_act_df(df)[0]
        self.assertEqual(df_speech_act.shape[0], 1)

    def test_speech_act_3(self):
        d = {"pony": ["a", "a"], "dialog": ["1+1", "= 2"], "title": ["t", "t"]}
        df = pd.DataFrame(data=d)
        df_speech_act = get_speech_act_df(df)[0]
        self.assertEqual(df_speech_act["pony"][0], "a")

    def test_speech_act_4(self):
        d = {"pony": ["a", "a"], "dialog": ["1+1", "= 2"], "title": ["t", "t"]}
        df = pd.DataFrame(data=d)
        df_speech_act = get_speech_act_df(df)[0]
        self.assertEqual(df_speech_act["dialog"][0], ["1", "1", "2"])

    def test_speech_act_5(self):
        d = {"pony": ["a", "a", "a"], "dialog": ["1+1", "= 2", "p"], "title": ["p", "t", "t"]}
        df = pd.DataFrame(data=d)
        df_speech_act = get_speech_act_df(df)
        self.assertEqual(len(df_speech_act), 2)

    def test_speech_act_6(self):
        d = {"pony": ["a", "a", "a"], "dialog": ["1+1", "= 2", "p"], "title": ["p", "t", "t"]}
        df = pd.DataFrame(data=d)
        df_speech_act = get_speech_act_df(df)
        self.assertEqual(df_speech_act[0]["dialog"][0], ["1", "1"])

    def test_speech_act_7(self):
        d = {"pony": ["a", "a", "a"], "dialog": ["1+1", "= 2", "p"], "title": ["p", "t", "t"]}
        df = pd.DataFrame(data=d)
        df_speech_act = get_speech_act_df(df)
        self.assertEqual(df_speech_act[1]["dialog"][0], ["2", "p"])

    def test_count_percent_dict_convert_1(self):
        d = {1: 5, 2: 2, 3: 3}
        d = count_dict_to_percent_dict(d)
        self.assertEqual(d, {1: .5, 2: .2, 3: .3})

    def test_count_percent_dict_convert_2(self):
        d = {1: 9}
        d = count_dict_to_percent_dict(d)
        self.assertEqual(d, {1: 1.0})

    def test_verbosity_1(self):
        d = {"pony": ["Fluttershy", "Rarity"], "dialog": ["1+1", "= 2"], "title": ["t", "t"]}
        df = get_speech_act_df(pd.DataFrame(data=d))
        verbosity = get_verbosity(df)
        self.assertEqual(verbosity["fluttershy"], 0.5)

    def test_verbosity_2(self):
        d = {"pony": ["Fluttershy", "Rarity"], "dialog": ["1+1", "= 2"], "title": ["t", "t"]}
        df = get_speech_act_df(pd.DataFrame(data=d))
        verbosity = get_verbosity(df)
        self.assertEqual(sum(verbosity[k] for k in verbosity.keys()), 1.0)

    def test_verbosity_3(self):
        d = {"pony": ["Fluttershy", "Rarity"], "dialog": ["1+1", "= 2"], "title": ["t", "t"]}
        df = get_speech_act_df(pd.DataFrame(data=d))
        verbosity = get_verbosity(df)
        self.assertEqual(verbosity["rarity"], 0.5)

    def test_verbosity_4(self):
        d = {"pony": ["Fluttershy", "Rarity"], "dialog": ["1+1", "= 2"], "title": ["t", "t"]}
        df = get_speech_act_df(pd.DataFrame(data=d))
        verbosity = get_verbosity(df)
        self.assertEqual(verbosity["rainbow"], 0.0)

    def test_parse_words_1(self):
        dialog = "I've got a pet."
        arr = parse_words(dialog)
        self.assertEqual(arr, ["I", "ve", "got", "a", "pet"])

    def test_parse_words_1(self):
        dialog = "I've got a pet."
        arr = parse_words(dialog)
        self.assertEqual(arr, ["I", "ve", "got", "a", "pet"])

    def test_parse_words_2(self):
        dialog = "I'v0e got a pet."
        arr = parse_words(dialog)
        self.assertEqual(arr, ["I", "v0e", "got", "a", "pet"])

    def test_parse_words_3(self):
        dialog = "Anti-trump."
        arr = parse_words(dialog)
        self.assertEqual(arr, ["Anti", "trump"])

    def test_mentions_1(self):
        d = {"pony": ["Fluttershy", "Rarity"], "dialog": ["1+1", "= 2"], "title": ["t", "t"]}
        df = get_speech_act_df(pd.DataFrame(data=d))
        mentions = get_mentions(df)
        self.assertEqual(mentions["rarity"]["rainbow"], 0.0)

    def test_mentions_2(self):
        d = {"pony": ["Fluttershy", "Rarity"], "dialog": ["1+1", "Rainbow"], "title": ["t", "t"]}
        df = get_speech_act_df(pd.DataFrame(data=d))
        mentions = get_mentions(df)
        self.assertEqual(mentions["rarity"]["rainbow"], 1.0)

    def test_mentions_3(self):
        d = {"pony": ["Rarity", "Rarity"], "dialog": ["Pie", "Rainbow"], "title": ["t", "t"]}
        df = get_speech_act_df(pd.DataFrame(data=d))
        mentions = get_mentions(df)
        self.assertEqual(mentions["rarity"]["rainbow"], .5)

    def test_mentions_4(self):
        d = {"pony": ["Rarity", "Rarity"], "dialog": ["Pie", "Rainbow"], "title": ["t", "t"]}
        df = get_speech_act_df(pd.DataFrame(data=d))
        mentions = get_mentions(df)
        self.assertEqual(mentions["rarity"]["pinkie"], .5)

    def test_mentions_5(self):
        d = {"pony": ["Rarity", "Rarity"], "dialog": ["Pie", "Rainbow"], "title": ["t", "t"]}
        df = get_speech_act_df(pd.DataFrame(data=d))
        mentions = get_mentions(df)
        self.assertEqual(mentions["rarity"]["fluttershy"], .0)

    def test_follow_1(self):
        d = {"pony": ["Rarity", "Fluttershy"], "dialog": ["Pie", "Rainbow"], "title": ["t", "t"]}
        df = get_speech_act_df(pd.DataFrame(data=d))
        follow = get_follow_on(df)
        self.assertEqual(follow["fluttershy"]["rarity"], 1.0)

    def test_follow_2(self):
        d = {"pony": ["Rdfghj", "Applejack"], "dialog": ["Pie", "Rainbow"], "title": ["t", "t"]}
        df = get_speech_act_df(pd.DataFrame(data=d))
        follow = get_follow_on(df)
        self.assertEqual(follow["applejack"]["rarity"], .0)

    def test_follow_2(self):
        d = {"pony": ["Rdfghj", "Applejack"], "dialog": ["Pie", "Rainbow"], "title": ["t", "t"]}
        df = get_speech_act_df(pd.DataFrame(data=d))
        follow = get_follow_on(df)
        self.assertEqual(follow["applejack"]["other"], 1.0)
