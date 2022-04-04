import unittest
import requests
from requests.auth import HTTPBasicAuth

BASE_URL = "http://127.0.0.1:5000/"
FAMILY = "family"
FAMILY_MEMBERS = "family_members"
COSTS = "costs"
PROFITS = "profits"


class MyTestCase(unittest.TestCase):
    def tearDown(self):
        BASE_URL = None
        USER = None
        PLAYLIST = None
        MUSIC = None

    def test_get_family(self):
        r = requests.request("GET", BASE_URL + FAMILY)
        self.assertEqual(r.status_code, 200)

    def test_post_family(self):
        r = requests.request("POST", BASE_URL + FAMILY)
        self.assertEqual(r.status_code, 500)

    def test_get_family_by_id(self):
        r = requests.request("GET", BASE_URL + FAMILY + "/1")
        self.assertEqual(r.status_code, 200)

    def test_get_members(self):
        r = requests.request("GET", BASE_URL + FAMILY_MEMBERS)
        self.assertEqual(r.status_code, 200)

    def test_post_member(self):
        r = requests.request("POST", BASE_URL + FAMILY_MEMBERS)
        self.assertEqual(r.status_code, 500)


if __name__ == '__main__':
    unittest.main()
