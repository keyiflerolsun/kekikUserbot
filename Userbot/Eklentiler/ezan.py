# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Userbot.Edevat.zenginLog import log_yolla, hata_log
from Userbot import DESTEK_KOMUT
from pathlib import Path

DESTEK_KOMUT.update({
    Path(__file__).stem : {
        "aciklama" : "sabah.com.tr'den ezan vakti bilgilerini verir..",
        "kullanim" : [
            "il"
            ],
        "ornekler" : [
            ".ezan çanakkale"
            ]
    }
})

from pyrogram import Client, filters
from Userbot.Edevat.Spatula.ezan_spatula import ezan_vakti

@Client.on_message(filters.command(['ezan'],['!','.','/']) & filters.me)
async def ezan(client, message):
    # < Başlangıç
    await log_yolla(client, message)
    ilk_mesaj = await message.edit("__Bekleyin..__",
        disable_web_page_preview    = True,
        parse_mode                  = "Markdown"
    )
    girilen_yazi = message.command
    #------------------------------------------------------------- Başlangıç >

    if len(girilen_yazi) == 1:
        await ilk_mesaj.edit("__Arama yapabilmek için `il` ve `ilçe` girmelisiniz..__")
        return

    il   = girilen_yazi[1].lower()  # komut hariç birinci kelime

    tr2eng  = str.maketrans(" .,-*/+-ıİüÜöÖçÇşŞğĞ", "________iIuUoOcCsSgG")
    il      = il.translate(tr2eng)

    try:
        await ilk_mesaj.edit(ezan_vakti(il))
    except IndexError:
        await ilk_mesaj.edit(f'`{il}` __diye bir yer bulamadım..__')
    except Exception as hata:
        await hata_log(hata)
        await ilk_mesaj.edit(f'**Hata Var !**\n\n`{type(hata).__name__}`\n\n__{hata}__')