# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Userbot.Edevat.zenginLog import log_yolla, hata_log
from Userbot import DESTEK_KOMUT
from pathlib import Path

DESTEK_KOMUT.update({
    Path(__file__).stem : {
        "aciklama" : "KekikSpatula'dan DiscUdemy Kurslarını verir..",
        "kullanim" : [
            "kategori"
            ],
        "ornekler" : [
            ".disc python"
            ]
    }
})

from pyrogram import Client, filters
from pyrogram.types import Message
from KekikSpatula import DiscUdemy

@Client.on_message(filters.command(['disc'],['!','.','/']) & filters.me)
async def disc(client:Client, message:Message):
    # < Başlangıç
    await log_yolla(client, message)
    ilk_mesaj = await message.edit("__Bekleyin..__", disable_web_page_preview = True)
    #------------------------------------------------------------- Başlangıç >
    girilen_yazi = message.command

    if len(girilen_yazi) == 1:
        await ilk_mesaj.edit("__Arama yapabilmek için `kategori` girmelisiniz..__")
        return

    kategori   = girilen_yazi[1].replace('İ', "i").lower()  # komut hariç birinci kelime

    tr2eng     = str.maketrans(" .,-*/+-ıİüÜöÖçÇşŞğĞ", "________iIuUoOcCsSgG")
    kategori   = kategori.translate(tr2eng)

    try:
        udemy = DiscUdemy(kategori).veri['veri']
    except (IndexError, TypeError):
        await ilk_mesaj.edit(f'`{kategori}` __kategorisini bulamadım..__')
        return

    mesaj = f"📼 `{kategori}` __için Udemy Kursları;__\n\n"

    for kurs in udemy:
        mesaj += f"__{kurs['dil']}__\n"
        mesaj += f"**[{kurs['baslik']}]({kurs['baglanti']})**\n\n"

    try:
        await ilk_mesaj.edit(mesaj, disable_web_page_preview = True)
    except Exception as hata:
        await hata_log(hata, ilk_mesaj)
        return