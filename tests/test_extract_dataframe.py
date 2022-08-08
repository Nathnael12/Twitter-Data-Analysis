import sys
import os
sys.path.append(os.path.abspath(os.path.join("")))
from ntpath import join
import unittest
import pandas as pd
import json
from pathlib import Path
from extract_dataframe import TweetDfExtractor
from extract_dataframe import read_json



# For unit testing the data reading and processing codes,
# we will need about 5 tweet samples.
# Create a sample not more than 10 tweets and place it in a json file.
# Provide the path to the samples tweets file you created below

# put here the path to where you placed the file e.g. ./sampletweets.json.
sampletweetsjsonfile = "./tests/sample_africa_tweets.json"

path = Path(sampletweetsjsonfile)
file_exists = path.is_file()

if not file_exists:
    _, all_tweets_list = read_json("./data/africa_twitter_data.json")
    tss = all_tweets_list[:10]
    with open(sampletweetsjsonfile, 'a') as output_file:
        for tweet in all_tweets_list[:10]:
            output_file.write(json.dumps(tweet))
            output_file.write("\n")

    print('Sample tweets saved!')

_, tweet_list = read_json(sampletweetsjsonfile)

# remove the array wrapper aded by json.dumps()
# tweet_list=tweet_list[0]

columns = [
    "created_at",
    "source",
    "original_text",
    "clean_text",
    "sentiment",
    "polarity",
    "subjectivity",
    "lang",
    "favorite_count",
    "retweet_count",
    "original_author",
    "screen_count",
    "followers_count",
    "friends_count",
    "possibly_sensitive",
    "hashtags",
    "user_mentions",
    "place",
    "place_coord_boundaries",
]


class TestTweetDfExtractor(unittest.TestCase):
    """
                A class for unit-testing function in the fix_clean_tweets_dataframe.py file

                Args:
        -----
                        unittest.TestCase this allows the new class to inherit
                        from the unittest module
        """

    def setUp(self) -> pd.DataFrame:
        self.df = TweetDfExtractor(tweet_list[:5])
        # tweet_df = self.df.get_tweet_df()

    def test_find_statuses_count(self):
        self.assertEqual(
            self.df.find_statuses_count(), [888, 1597, 2293, 44, 1313]
        )

    def test_find_full_text(self):
        text = ['#Pelosi airplane landed safely in #Taiwan 🇹🇼  \n1) - Both 🇨🇳 &amp;  🇺🇸 are playing "win win" on financial markets. 2) - Taiwan may be the future Asian   Cuba  3) - 🇺🇸 &amp; 🇨🇳 need an Asian #NATO / #5G\nWhat\'s your thoughts?',
                "Watch the video of the beginning of the Chinese bombing of Taiwan during Pelosi visit from here : https://t.co/twah6WU4fZ\n\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\n#Pelosi #\u30de\u30c4\u30b3\u306e\u77e5\u3089\u306a\u3044\u4e16\u754c #Yediiklim #BadDecisionsTrailer1 #LawnBowls #\u795d_CALL119_MV900\u4e07\u56de #\u0e21\u0e32\u0e01\u0e2d\u0e14\u0e01\u0e31\u0e19\u0e19\u0e30\u0e0b\u0e35\u0e1e\u0e24\u0e01\u0e29\u0e4c https://t.co/m4CXfyZRS7",
                "#Pelosi \n#Taipei \n#taiwan\n#XiJinping \n#China \nOn a verge of another war https://t.co/DuqDiSnWcd",
                '#HOBIPALOOZA #LaAcademiaExpulsion #WEURO2022 #jhopeAtLollapalooza #SuzukiPakistan #Fantastico #Taiwan #breastfeeding #Kosovo #BORNPINK  strong ✍️💜 https://t.co/GtZeNL24rm',
                '#Pelosi\n#china\nChina Time ✌️ https://t.co/tEDjzTlszu']
        dd=self.df.find_full_text()
        self.assertEqual(self.df.find_full_text(), text)

    def test_find_sentiments(self):
        self.assertEqual(
            self.df.find_sentiments(self.df.find_full_text()),
            (
                [0.3, 0.0, 0.0, 0.4333333333333333, 0.0],
                [0.20357142857142857, 0.0, 0.0, 0.7333333333333333, 0.0]
            ),
        )

    def test_find_screen_name(self):
        name = ['DzCritical', 'toopsat', 'NassimaLilEmy',
                'd_dhayae', 'Mohamme65404115']
        self.assertEqual(self.df.find_screen_name(), name)

    def test_find_followers_count(self):
        f_count = [318, 764, 64, 60, 39]
        self.assertEqual(self.df.find_followers_count(), f_count)

    def test_find_friends_count(self):
        friends_count = [373, 144, 47, 463, 206]
        self.assertEqual(self.df.find_friends_count(), friends_count)

    def test_find_is_sensitive(self):
        self.assertEqual(self.df.is_sensitive(), [
                         None, False, False, False, False])

    # def test_find_hashtags(self):
    #     self.assertEqual(self.df.find_hashtags(), )

    # def test_find_mentions(self):
    #     self.assertEqual(self.df.find_mentions(), )


if __name__ == "__main__":
    unittest.main()
