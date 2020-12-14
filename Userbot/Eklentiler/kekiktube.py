# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Userbot.Edevat.zenginLog import log_yolla, hata_log
from Userbot import DESTEK_KOMUT
from pathlib import Path

DESTEK_KOMUT.update({
    Path(__file__).stem : {
        "aciklama" : "KekikSpatula'dan YouTube Video bilgilerini verir..",
        "kullanim" : [
            "link"
            ],
        "ornekler" : [
            ".kekiktube link"
            ]
    }
})

from pyrogram import Client, filters
from pyrogram.types import Message
from KekikSpatula import KekikTube

@Client.on_message(filters.command(['kekiktube'],['!','.','/']) & filters.me)
async def kekiktube(client:Client, message:Message):
    # < Başlangıç
    await log_yolla(client, message)
    ilk_mesaj = await message.edit("__Bekleyin..__", disable_web_page_preview = True)
    #------------------------------------------------------------- Başlangıç >
    girilen_yazi = message.command

    if len(girilen_yazi) == 1:
        await ilk_mesaj.edit("__Arama yapabilmek için `link` girmelisiniz..__")
        return

    link   = girilen_yazi[1]

    try:
        kekik = KekikTube(link).veri['veri'][0]
    except IndexError:
        await ilk_mesaj.edit(f'`{link}` __bulunamadı..__')
        return

    await ilk_mesaj.delete()

    mesaj = f"""
**Sahip :** __{kekik['sahip']}__
**Başlık :** __{kekik['baslik']}__
**Süre :** __{kekik['sure']}__
**İzlenme :** __{kekik['izlenme']}__
**Açıklama :** __{kekik['aciklama'][:500]}...__


**Kalite :** __{kekik['kalite']}__
**Boyut :** __{kekik['boyut']}__
[Video'yu İndir]({kekik['url']})
"""

    try:
        await message.reply_photo(
            photo   = kekik['resim'],
            caption = mesaj
        )
    except Exception as hata:
        await hata_log(hata, ilk_mesaj)
        return