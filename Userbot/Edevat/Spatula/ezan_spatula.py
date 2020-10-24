# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from requests import get
from datetime import datetime

def ezan_vakti(il):
    ezan_api  = f'https://www.sabah.com.tr/json/getpraytimes/{il}'
    json_veri = get(ezan_api).json()['List'][0]

    imsak   = datetime.fromtimestamp(int(json_veri['Imsak'].split('(')[1][:-5]))
    gunes   = datetime.fromtimestamp(int(json_veri['Gunes'].split('(')[1][:-5]))
    ogle    = datetime.fromtimestamp(int(json_veri['Ogle'].split('(')[1][:-5]))
    ikindi  = datetime.fromtimestamp(int(json_veri['Ikindi'].split('(')[1][:-5]))
    aksam   = datetime.fromtimestamp(int(json_veri['Aksam'].split('(')[1][:-5]))
    yatsi   = datetime.fromtimestamp(int(json_veri['Yatsi'].split('(')[1][:-5]))

    mesaj = f"📍 `{il.capitalize()}` __için Ezan Vakitleri;__\n\n"
    mesaj += f"🏙 **İmsak   :** `{str(imsak).split()[1][:-3]}`\n"
    mesaj += f"🌅 **Güneş   :** `{str(gunes).split()[1][:-3]}`\n"
    mesaj += f"🌇 **Öğle    :** `{str(ogle).split()[1][:-3]}`\n"
    mesaj += f"🌆 **İkindi  :** `{str(ikindi).split()[1][:-3]}`\n"
    mesaj += f"🌃 **Akşam   :** `{str(aksam).split()[1][:-3]}`\n"
    mesaj += f"🌌 **Yatsı   :** `{str(yatsi).split()[1][:-3]}`\n"

    return mesaj