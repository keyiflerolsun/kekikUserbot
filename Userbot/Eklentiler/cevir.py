# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Userbot.Edevat.zenginLog import log_yolla, hata_log
from Userbot import DESTEK_KOMUT
from pathlib import Path

DESTEK_KOMUT.update({
    Path(__file__).stem : {
        "aciklama"  : "Türkçeye Çeviri yapmanıza olanak tanır.",
        "kullanim"  : [
            "Yanıtlanan Mesaj",
            "Metin"
            ],
        "ornekler"  : [
            ".cevir"
            ]
    }
})

from pyrogram import Client, filters
from pyrogram.types import Message
from googletrans import Translator
from langcodes import Language
import os

cevirici:Translator = Translator()

@Client.on_message(filters.command(['cevir'], ['!','.','/']) & filters.me)
async def cevir(client:Client, message:Message):
    # < Başlangıç
    await log_yolla(client, message)
    ilk_mesaj = await message.edit("__Bekleyin..__", disable_web_page_preview = True)
    #------------------------------------------------------------- Başlangıç >
    girilen_yazi        = message.text
    cevaplanan_mesaj    = message.reply_to_message

    if not cevaplanan_mesaj and len(girilen_yazi.split()) == 1:
        await ilk_mesaj.edit("__Çeviri yapabilmem için bişeyler söyleyin ya da mesaj yanıtlayın..__")
        return

    if not cevaplanan_mesaj:
        girdi = girilen_yazi.split(" ", 1)[1]

    elif cevaplanan_mesaj.document:
        gelen_dosya = await cevaplanan_mesaj.download()

        veri_listesi = None
        with open(gelen_dosya, "rb") as oku:
            veri_listesi = oku.readlines()

        girdi = "".join(veri.decode("UTF-8") for veri in veri_listesi)

        os.remove(gelen_dosya)

    elif cevaplanan_mesaj.text:
        girdi = cevaplanan_mesaj.text
    else:
        await ilk_mesaj.edit("__güldük__")
        return

    await ilk_mesaj.edit("Çevriliyor...")

    gelen_mesaj_dili = Language.make(language=cevirici.detect(girdi).lang).display_name()
    cevrilmis_mesaj  = cevirici.translate(girdi, dest='tr').text

    await ilk_mesaj.edit(f'`{gelen_mesaj_dili}`\n\n__{cevrilmis_mesaj}__')