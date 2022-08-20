from unicodedata import category
import requests
import re
import xmltodict
import math
from xml.etree import ElementTree as ET

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])


class BetterCinemaAPI():
    def search(self, query, limit=25, category="", offset=0, sort="largest"):
        url = "https://webshare.cz/api/search/"

        payload={
        'what': query,
        'offset': offset,
        'limit': limit,
        'category': category,
        'sort': sort
        }

        response = requests.request("POST", url, data=payload)

        xml = response.text

        data = []
        data_dict = xmltodict.parse(xml)
        temp_dict = data_dict['response']['file']
        data.extend(temp_dict)
        list = []
        for x in range(len(data)):
            ident = data[x]["ident"]
            name = data[x]["name"]
            postive_votes = data[x]["positive_votes"]
            negative_votes = data[x]["negative_votes"]
            size = int(data[x]["size"])
            size = convert_size(size)
          
            list.append([ident, name, size, postive_votes, negative_votes])
        return list

    def get_link(self, ident, wst):
        url = "https://webshare.cz/api/file_link/"


        payload = f"ident={ident}&wst={wst}&force_https=0&download_type=video_stream&device_vendor=ymovie"
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36'
        }


        response = requests.request("POST", url, headers=headers, data=payload)

        # preparsed_link
        xml = ET.fromstring(response.text)
        if not xml.find('status').text == 'OK':
            return "Error 403"
        
        else:
            pass

        link = xml.find('link').text
        return link