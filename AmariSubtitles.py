
import requests
import json

class SubtitleEpisodeDoesNotExist(Exception):
    def __init__(self, message):            
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
class SubtitleDoesNotExist(Exception):
    def __init__(self, message):            
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
class IncorrectFileId(Exception):
    def __init__(self, message):            
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
            
class AmariSubtitles:
    def __init__(self) -> None:
        self.app_name = "AmariDev v1.2.3"
        self.__api_key = "5xmYVG9frIy7QTnyxtkhF2hI3eTNsRb0"
    def fetch_subs(self,imdb_id,search=0,movie=0):
        if search == 0:
            param = "parent_imdb_id"
        if movie == 1:
            param = "imdb_id"
        if search == 1:
            param = "query"
        url = f"https://api.opensubtitles.com/api/v1/subtitles?{param}={imdb_id}"

        headers = {
            "User-Agent": self.app_name,
            "Api-Key": self.__api_key
        }

        response = requests.get(url, headers=headers)

        result= response.json()["data"]
        english_subs = list(filter(lambda x:x["attributes"]["language"] == "en",result))
        if len(english_subs) == 0:
            raise SubtitleDoesNotExist("Query does not exist. As a result can't provide Subtitle.")
        return english_subs

    def get_available_episodes(self,imdb_id,search=0):
        return len(self.fetch_subs(imdb_id,search))
    def get_file_id(self,sub,season,episode):
        num_available = len(sub)
        
        
        result = list(filter(lambda x: x["attributes"]["feature_details"]["episode_number"] == episode and x["attributes"]["feature_details"]["season_number"] == season,sub))
        if len(result) == 0:
            raise SubtitleEpisodeDoesNotExist(f"Season or Episode does not exist. Please Check number of available subs is {num_available}.")
        return result[0]["attributes"]["files"][0]["file_id"]

    def get_file_id_movie(self,subs):
        num_available = len(subs)
        

        if len(subs) == 0:
            raise SubtitleEpisodeDoesNotExist(f"Season or Episode does not exist. Please Check number of available subs is {num_available}.")
        return subs[0]["attributes"]["files"][0]["file_id"]

            
            
    def get_sub_url(self,file_id):
        url = "https://api.opensubtitles.com/api/v1/download"

        payload = { "file_id": file_id }
        headers = {
            "User-Agent": self.app_name,
            "Api-Key": self.__api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        response = requests.post(url, json=payload, headers=headers)
        result = response.json()
        if result.get("message") == "Invalid file_id":
            raise IncorrectFileId("Incorrect File Id.")
        return result["file_name"],result["link"]


     
    def search_and_get_url(self,imdb_id,season,episode):
        english_subs = self.fetch_subs(imdb_id)
        file_id = self.get_file_id(english_subs,season,episode)
        filename,link = self.get_sub_url(file_id)
        return filename,link
    def search_and_get_url_movie(self,imdb_id):
        english_subs = self.fetch_subs(imdb_id,movie=1)
        file_id = self.get_file_id_movie(english_subs)
        filename,link = self.get_sub_url(file_id)
        return filename,link
