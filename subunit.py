import json
import requests
import unittest
import sys

uri = "http://127.0.0.1:8080" #"https://blacktechdivisionreward-hrjw5cc7pa-uc.a.run.app"

class SubUnittest(unittest.TestCase):
    def test_fetch_subtitle(self):
        response = requests.get(f"{uri}/api/fetchsubtitle",params={"imdb_id":"tt9335498","season":3,"episode":2})
        print()
        with open("text.txt","w+") as f:
            f.write(response.content.decode())
        #self.assertEqual(response.json().get("error"),None)
    def test_search_subtitle(self):
        response = requests.get(f"{uri}/api/searchsubtitles",params={"query":"Frieren"})
        print(response.json())
        self.assertEqual(response.json().get("error"),None)
    def test_get_available_subtitles(self):
        response = requests.get(f"{uri}/api/getavailablesubtitles",params={"imdb_id":"tt15237152"})
        print(response.json())
        self.assertEqual(response.json().get("error"),None)
    def test_query_available_subtitles(self):
        response = requests.get(f"{uri}/api/queryavailablesubtitles",params={"query":"Frieren"})
        print(response.json())
        self.assertEqual(response.json().get("error"),None)
        


if __name__ == "__main__":
    unittest.main()