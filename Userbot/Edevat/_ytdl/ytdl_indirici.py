# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Userbot.Edevat._ytdl.link_islemleri import link_ayikla
from Userbot import INDIRME_ALANI
import youtube_dl, os, wget
from PIL import Image
from youtube_dl.utils import sanitize_filename

class LogYok(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        pass

async def ytdl_indirici(mesaj, link, parametre=None):
    parametreler = {
        'outtmpl' : os.path.join(f"{INDIRME_ALANI}/", '%(title)s.%(ext)s'),
        'writethumbnail': True,
        'cachedir': False,
        'logger' : LogYok(),
    }

    if parametre and parametre == 'mp3':
        parametreler.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
        })
    else:
        parametreler.update({
            'format': 'best',
        })

    ytdl = youtube_dl.YoutubeDL(parametreler)

    link = link_ayikla(link)[0]

    try:
        bilgiler = ytdl.extract_info(link, download=False)
    except Exception as hata:
        return hata

    yt_baslik   = sanitize_filename(bilgiler.get('title'))

    yt_resim    = wget.download(bilgiler.get('thumbnail'), os.path.join(f"{INDIRME_ALANI}/", f"{yt_baslik}.jpg"))
    Image.open(yt_resim).convert("RGB").save(f"{yt_resim.split('.')[0]}.jpeg", "JPEG")
    yt_resim    = f"{yt_resim.split('.')[0]}.jpeg"

    await mesaj.edit(f"**{yt_baslik}**\n\n\t__İndiriliyor__")
    _ = ytdl.download([link])
    await mesaj.delete()

    ilk_mesaj = await mesaj.reply(f"**{yt_baslik}**\n\n\t__Yükleniyor__")

    if parametre and parametre == 'mp3':
        inen_veri = f"{INDIRME_ALANI}/{yt_baslik}.mp3"
    else:
        inen_veri = f"{INDIRME_ALANI}/{yt_baslik}.mp4"

    return yt_baslik, yt_resim, inen_veri, ilk_mesaj