"""Import modules"""
import math
from xml.etree import ElementTree as ET
import xmltodict
import requests




def convert_size(size_bytes):
    """convert size to human readable format"""
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"


class BetterCinemaAPI():
    """Handle request to Webshare api"""
    def search(self, query: dict):
        """search webshare"""
        url = "https://webshare.cz/api/search/"

        payload={
        'what': query['what'],
        'offset': query['offset'],
        'limit': query['limit'],
        'category': query['category'],
        'sort': query['sort']
        }

        response = requests.request("POST", url, data=payload, timeout=30)

        xml = response.text

        data = []
        data_dict = xmltodict.parse(xml)
        try:
            temp_dict = data_dict['response']['file']
        except Exception:
            return None

        data.extend(temp_dict)
        _list = []
        for xvar in range(len(data)):
            ident = data[xvar]["ident"]
            name = data[xvar]["name"]
            postive_votes = data[xvar]["positive_votes"]
            negative_votes = data[xvar]["negative_votes"]
            size = int(data[xvar]["size"])
            size = convert_size(size)

            _list.append([ident, name, size, postive_votes, negative_votes])
        return _list

    def get_link(self, ident, wst):
        """Get link to file"""
        url = "https://webshare.cz/api/file_link/"


        payload = f"ident={ident}&wst={wst}&force_https=0&download_type= \
            video_stream&device_vendor=ymovie"
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36'
        }


        response = requests.request("POST", url, headers=headers, data=payload, timeout=30)

        # preparsed_link
        xml = ET.fromstring(response.text)
        if not xml.find('status').text == 'OK':
            return "Error 403"

        link = xml.find('link').text
        return link

    def get_vip_status(self, wst):
        has_vip = False
        url = "https://webshare.cz/api/user_data/"

        payload = f"wst={wst}"
        headers = {
        'Accept': 'text/xml; charset=UTF-8',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        xml = ET.fromstring(response.text)
        if not xml.find('status').text == 'OK':
            return "403"
        vip = xml.find('vip').text
        if vip == '1':
            has_vip = True
        if has_vip:
            vip_days = xml.find('vip_days').text
            vip_hours = xml.find('vip_hours').text
            vip_minutes = xml.find('vip_minutes').text
            vip_until = xml.find('vip_until').text
            return vip_days, vip_hours, vip_minutes, vip_until
        else:
            return None