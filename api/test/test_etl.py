import unittest
import pandas as pd
from pandas.util.testing import assert_series_equal, assert_frame_equal
from src.etl import WhatsAppDataParser


class InitChatStat(unittest.TestCase):

    def setUp(self):
        self.assertFrameEqual = assert_frame_equal
        self.assertSeriesEqual = assert_series_equal
        self.input_str_ios = (
                "[22-11-13 19:08:14] Master: Berichten die naar deze groep "
                "worden verzonden, zijn nu beveiligd met end-to-end encryptie."
                "[22-11-13 19:08:14] Henk heeft deze groep aangemaakt"
                "[24-11-17 14:36:50] Mi heeft Yu toegevoegd"
                "[24-11-17 14:37:22] Yu: Thanks Mi!"
                "[24-11-17 14:38:41] Mi: Welkom!"
                )
        self.input_str_android = (
                "22-11-2013 19:08 Master: Berichten die naar deze groep "
                "worden verzonden, zijn nu beveiligd met end-to-end encryptie."
                "22-11-2013 19:08 Henk heeft deze groep aangemaakt"
                "24-11-2017 14:36 Mi heeft Yu toegevoegd"
                "24-11-2017 14:37 Yu: Thanks Mi!"
                "24-11-2017 14:38 Mi: Welkom!"
                )
        self.parser = WhatsAppDataParser(source='stream')


class TestWhatsAppDataParser(InitChatStat):

    # overall test, still necessary to unittest all individual transformations?
    def test_transform(self):
        output_df = self.parser.transform(self.input_str_ios)
        correct_df = pd.DataFrame(data={
            "sender": ["Yu", "Mi"],
            "message": ["Thanks Mi!", "Welkom!"],
            "timestamp": [pd.to_datetime("2017-11-24 14:37:22"),
                          pd.to_datetime("2017-11-24 14:38:41")]
        })
        self.assertEqual(output_df.shape, (2, 3))
        self.assertSeriesEqual(output_df.dtypes, correct_df.dtypes, check_names=True)
        self.assertFrameEqual(output_df, correct_df)

    def test_guess_regex_format(self):
        regex_format_1 = self.parser.guess_regex_format(self.input_str_ios)
        correct_1 = r"\[(\d{2}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] "
        self.assertEqual(regex_format_1, correct_1)

        regex_format_2 = self.parser.guess_regex_format(self.input_str_android)
        correct_2 = r"(\d{2}-\d{2}-\d{4} \d{2}:\d{2} )"
        self.assertEqual(regex_format_2, correct_2)

        false_input = "{24-11-2017 14:38:41} Mi: Welkom!"
        self.assertRaises(ValueError, self.parser.guess_regex_format, false_input)