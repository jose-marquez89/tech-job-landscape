import unittest
import scrape


class TestScrapeFunctions(unittest.TestCase):

    def test_build_url(self):
        url = scrape.build_url("indeed",
                               "/jobs?q=Data+Scientist&l=Texas&start=10",
                               join_next=True)

        expected = ("https://www.indeed.com/"
                    "jobs?q=Data+Scientist&l=Texas&start=10")
        url2 = scrape.build_url("indeed", job="Data Scientist", state="Texas")
        expected2 = ("https://www.indeed.com/"
                     "jobs?q=Data%20Scientist&l=Texas&start=0")
        self.assertEqual(url, expected)
        self.assertEqual(url2, expected2)

    def test_fetch_page(self):
        fpl = scrape.fetch_page_listings
        job_data = fpl("indeed",
                       job="Data Scientist",
                       state="Texas")
        self.assertNotEqual(len(job_data), 0)
        self.assertIsInstance(job_data, tuple)
        self.assertIsInstance(job_data[0][0], dict)
        self.assertIsInstance(job_data[1], str)
        job_data = fpl("indeed",
                       next_page="/jobs?q=Data+Scientist"
                                 "&l=Texas&start=10")


if __name__ == '__main__':
    unittest.main()
