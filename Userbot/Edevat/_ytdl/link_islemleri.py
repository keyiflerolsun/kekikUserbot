# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

import re

def link_ayikla(link):
    """ Metindeki linkleri liste halinde return eder """
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

    url = re.findall(regex, link)

    liste = [x[0] for x in url]

    if liste:
        return liste
    else:
        return None

youtubeLinkiMi = lambda link: bool(re.match(r"http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?", link)) 