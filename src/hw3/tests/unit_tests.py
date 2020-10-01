import unittest

import pandas as pd

from ....scripts import analysis


class HW3TestCase(unittest.TestCase):
    def test_speech_act_1(self):
        d = {"pony": ["a", "a"], "dialog": ["1+1", "= 2"]}
        df = pd.DataFrame(data=d)
        df_speech_act = analysis.get_speech_act_df(df)
        self.assertEqual(df_speech_act.shape[0], 1)

    def test_speech_act_2(self):
        d = {"pony": ["a"], "dialog": ["1+1"]}
        df = pd.DataFrame(data=d)
        df_speech_act = analysis.get_speech_act_df(df)
        self.assertEqual(df_speech_act.shape[0], 1)

    def test_speech_act_3(self):
        d = {"pony": ["a", "a"], "dialog": ["1+1", "= 2"]}
        df = pd.DataFrame(data=d)
        df_speech_act = analysis.get_speech_act_df(df)
        self.assertEqual(df_speech_act["pony"][0], "a")

    def test_speech_act_4(self):
        d = {"pony": ["a", "a"], "dialog": ["1+1", "= 2"]}
        df = pd.DataFrame(data=d)
        df_speech_act = analysis.get_speech_act_df(df)
        self.assertEqual(df_speech_act["dialog"][0], ["1", "1", "2"])

    def test_count_percent_dict_convert_1(self):
        d = {1: 5, 2: 2, 3: 3}
        d = analysis.count_dict_to_percent_dict(d)
        self.assertEqual(d, {1: .5, 2: .2, 3: .3})

    def test_count_percent_dict_convert_2(self):
        d = {1: 9}
        d = analysis.count_dict_to_percent_dict(d)
        self.assertEqual(d, {1: 1.0})

    def test_verbosity_1(self):
        d = {"pony": ["Fluttershy", "Rarity"], "dialog": ["1+1", "= 2"]}
        df = analysis.get_speech_act_df(pd.DataFrame(data=d))
        verbosity = analysis.get_verbosity(df)
        self.assertEqual(verbosity["fluttershy"], 0.5)

    def test_verbosity_2(self):
        d = {"pony": ["Fluttershy", "Rarity"], "dialog": ["1+1", "= 2"]}
        df = analysis.get_speech_act_df(pd.DataFrame(data=d))
        verbosity = analysis.get_verbosity(df)
        self.assertEqual(sum(verbosity[k] for k in verbosity.keys()), 1.0)

    def test_verbosity_3(self):
        d = {"pony": ["Fluttershy", "Rarity"], "dialog": ["1+1", "= 2"]}
        df = analysis.get_speech_act_df(pd.DataFrame(data=d))
        verbosity = analysis.get_verbosity(df)
        self.assertEqual(verbosity["rarity"], 0.5)

    def test_verbosity_4(self):
        d = {"pony": ["Fluttershy", "Rarity"], "dialog": ["1+1", "= 2"]}
        df = analysis.get_speech_act_df(pd.DataFrame(data=d))
        verbosity = analysis.get_verbosity(df)
        self.assertEqual(verbosity["rainbow"], 0.0)

    def test_parse_words_1(self):
        dialog = "I've got a pet."
        arr = analysis.parse_words(dialog)
        self.assertEqual(arr, ["I", "ve", "got", "a", "pet"])

    def test_parse_words_1(self):
        dialog = "I've got a pet."
        arr = analysis.parse_words(dialog)
        self.assertEqual(arr, ["I", "ve", "got", "a", "pet"])

    def test_parse_words_2(self):
        dialog = "I'v0e got a pet."
        arr = analysis.parse_words(dialog)
        self.assertEqual(arr, ["I", "v0e", "got", "a", "pet"])

    def test_parse_words_3(self):
        dialog = "Anti-trump."
        arr = analysis.parse_words(dialog)
        self.assertEqual(arr, ["Anti", "trump"])

    def test_mentions_1(self):
        d = {"pony": ["Fluttershy", "Rarity"], "dialog": ["1+1", "= 2"]}
        df = analysis.get_speech_act_df(pd.DataFrame(data=d))
        mentions = analysis.get_mentions(df)
        self.assertEqual(mentions["rarity"]["rainbow"], 0.0)

    def test_mentions_2(self):
        d = {"pony": ["Fluttershy", "Rarity"], "dialog": ["1+1", "Rainbow"]}
        df = analysis.get_speech_act_df(pd.DataFrame(data=d))
        mentions = analysis.get_mentions(df)
        self.assertEqual(mentions["rarity"]["rainbow"], 1.0)

    def test_mentions_3(self):
        d = {"pony": ["Rarity", "Rarity"], "dialog": ["Pie", "Rainbow"]}
        df = analysis.get_speech_act_df(pd.DataFrame(data=d))
        mentions = analysis.get_mentions(df)
        self.assertEqual(mentions["rarity"]["rainbow"], .5)

    def test_mentions_4(self):
        d = {"pony": ["Rarity", "Rarity"], "dialog": ["Pie", "Rainbow"]}
        df = analysis.get_speech_act_df(pd.DataFrame(data=d))
        mentions = analysis.get_mentions(df)
        self.assertEqual(mentions["rarity"]["pinky"], .5)

    def test_mentions_5(self):
        d = {"pony": ["Rarity", "Rarity"], "dialog": ["Pie", "Rainbow"]}
        df = analysis.get_speech_act_df(pd.DataFrame(data=d))
        mentions = analysis.get_mentions(df)
        self.assertEqual(mentions["rarity"]["fluttershy"], .0)

    def test_follow_1(self):
        d = {"pony": ["Rarity", "Fluttershy"], "dialog": ["Pie", "Rainbow"]}
        df = analysis.get_speech_act_df(pd.DataFrame(data=d))
        follow = analysis.get_follow_on(df)
        self.assertEqual(follow["fluttershy"]["rarity"], 1.0)

    def test_follow_2(self):
        d = {"pony": ["Rdfghj", "Applejack"], "dialog": ["Pie", "Rainbow"]}
        df = analysis.get_speech_act_df(pd.DataFrame(data=d))
        follow = analysis.get_follow_on(df)
        self.assertEqual(follow["applejack"]["rarity"], .0)

    def test_follow_2(self):
        d = {"pony": ["Rdfghj", "Applejack"], "dialog": ["Pie", "Rainbow"]}
        df = analysis.get_speech_act_df(pd.DataFrame(data=d))
        follow = analysis.get_follow_on(df)
        self.assertEqual(follow["applejack"]["other"], 1.0)
