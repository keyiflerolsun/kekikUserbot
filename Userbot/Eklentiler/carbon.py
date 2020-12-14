# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Userbot.Edevat.zenginLog import log_yolla, hata_log
from Userbot import DESTEK_KOMUT, SESSION_ADI
from pathlib import Path

DESTEK_KOMUT.update({
    Path(__file__).stem : {
        "aciklama"  : "`carbon.now.sh` Apisi..",
        "kullanim"  : [
            "Yanıtlanan Mesaj",
            "Yanıtlanan Dosya",
            "Metin"
            ],
        "ornekler"  : [
            ".carbon"
            ]
    }
})

from pyrogram import Client, filters
from pyrogram.types import Message
from Userbot.Edevat._pyrogram.pyro_yardimcilari import yanitlanan_mesaj
from requests import post
import shutil, os, urllib

@Client.on_message(filters.command(['carbon'], ['!','.','/']) & filters.me)
async def carbon_api(client:Client, message:Message):
    # < Başlangıç
    await log_yolla(client, message)
    yanit_id  = await yanitlanan_mesaj(message)
    ilk_mesaj = await message.edit("__Bekleyin..__", disable_web_page_preview = True)
    #------------------------------------------------------------- Başlangıç >
    girilen_yazi        = message.text
    cevaplanan_mesaj    = message.reply_to_message

    json = {
        "backgroundColor": "rgba(31, 129, 109, 1)",
        "theme": "monokai",
        "exportSize": "4x",
        "language": "auto"
    }

    # 'https://carbon.now.sh/?t={theme}&l={lang}&code={code}&bg={bg}'

    if not cevaplanan_mesaj and len(girilen_yazi.split()) == 1:
        await ilk_mesaj.edit("__Carbon'a yönlendirebilmem için bişeyler verin ya da mesaj yanıtlayın..__")
        return

    if not cevaplanan_mesaj:
        json['code'] = urllib.parse.quote(girilen_yazi.split(" ", 1)[1])

    elif cevaplanan_mesaj.document:
        gelen_dosya = await cevaplanan_mesaj.download()

        veri_listesi = None
        with open(gelen_dosya, "rb") as oku:
            veri_listesi = oku.readlines()

        inen_veri = "".join(veri.decode("UTF-8") for veri in veri_listesi)
        json['code'] = urllib.parse.quote(inen_veri)

        os.remove(gelen_dosya)

    elif cevaplanan_mesaj.text:
        json['code'] = urllib.parse.quote(cevaplanan_mesaj.text)
    else:
        await ilk_mesaj.edit("__güldük__")
        return


    await ilk_mesaj.edit('`Carbon yapılıyor..`')


    api_url = "http://carbonnowsh.herokuapp.com"
    istek   = post(api_url, json=json, stream=True)
    gorsel  = "carbon.png"

    if istek.status_code == 200:
        istek.raw.decode_content = True

        with open(gorsel, "wb") as carbon_yazdir:
            shutil.copyfileobj(istek.raw, carbon_yazdir)

        await client.send_photo(
            message.chat.id,
            gorsel,
            caption             = f'`{SESSION_ADI}` __tarafından dönüştürülmüştür..__',
            reply_to_message_id = yanit_id,
        )
        await ilk_mesaj.delete()
    else:
        await ilk_mesaj.edit("**Görsel Alınamadı..**")

    os.remove(gorsel)