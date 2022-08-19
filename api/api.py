from unicodedata import category
import requests
import re
import xmltodict
import math


def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])


class BetterCinemaAPI():
    def search(self, query, limit=25, category="", sort="largest"):
        url = "https://webshare.cz/api/search/"

        payload={
        'what': query,
        'offset': 0,
        'limit': limit,
        'category': category,
        'sort': sort
        }

        headers = {
        }

        response = requests.request("POST", url, data=payload)

        xml = response.text

        data_dict = xmltodict.parse(xml)

        list = []
        for x in range(limit):
            ident = data_dict["response"]["file"][x]["ident"]
            name = data_dict["response"]["file"][x]["name"]
            size = int(data_dict["response"]["file"][x]["size"])
            size = convert_size(size)
          
            list.append([ident, name, size])
        return list

    def get_link(self, ident, wst):
        url = "https://webshare.cz/api/file_link/"


        payload = f"ident={ident}&wst={wst}&force_https=0&download_type=video_stream&device_vendor=ymovie"
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36'
        }


        response = requests.request("POST", url, headers=headers, data=payload)

        preparsed_link = response.text

        link = re.search(r'<link>(.*)</link>', preparsed_link).group(1)

        return link