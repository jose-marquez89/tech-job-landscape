import unittest
import scrape


class TestScrapeFunctions(unittest.TestCase):

    def test_build_url(self):
        url = scrape.build_url("indeed", "Data Scientist", "Texas", page=50)
        expected = ("https://www.indeed.com/"
                    "jobs?q=Data%20Scientist&l=Texas&start=50")
        self.assertEqual(url, expected)

    def test_fetch_page(self):
        job_data = scrape.fetch_page_listings("Data Scientist",
                                              "Texas", "indeed")
        self.assertNotEqual(len(job_data), 0)
        self.assertIsInstance(job_data, list)
        self.assertIsInstance(job_data[0], dict)

        print(job_data)


if __name__ == '__main__':
    unittest.main()
