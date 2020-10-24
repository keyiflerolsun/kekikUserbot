# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Userbot.Edevat.zenginLog import log_yolla, hata_log
from Userbot import DESTEK_KOMUT
from pathlib import Path

DESTEK_KOMUT.update({
    Path(__file__).stem : {
        "aciklama"  : "Yanıtlanan programlama kodunun çıktısını verir..",
        "kullanim"  : [
            "dil | yanıtlanan kod",
            "dil | yanıtlanan döküman"
            ],
        "ornekler"  : [
            ".derle c | yanıtlanan kod veya dosya",
            ".derle go | yanıtlanan kod veya dosya",
            ".derle python | yanıtlanan kod veya dosya"
            ]
    }
})

from pyrogram import Client, filters
from Userbot.Edevat.Spatula.derleyici_spatula import calistir
from os import remove

@Client.on_message(filters.command(['derle'], ['!','.','/']) & filters.me)
async def derle(client, message):
    # < Başlangıç
    await log_yolla(client, message)
    ilk_mesaj = await message.edit("__Bekleyin..__",
        disable_web_page_preview    = True,
        parse_mode                  = "Markdown"
    )
    girilen_yazi        = message.command
    cevaplanan_mesaj    = message.reply_to_message
    #------------------------------------------------------------- Başlangıç >

    if cevaplanan_mesaj is None:
        if len(girilen_yazi) == 1:
            await ilk_mesaj.edit("__Derleyebilmek için `dil` ve `kod` vermelisiniz..__")
            return
        elif len(girilen_yazi) == 2:
            await ilk_mesaj.edit("__Derleyebilmek için `dil` **de** vermelisiniz..__\n\n`.derle c` **kod**")
            return
        kod = " ".join(girilen_yazi[2:]) 

    elif cevaplanan_mesaj and cevaplanan_mesaj.document:
        if len(girilen_yazi) == 1:
            await ilk_mesaj.edit("__Derleyebilmek için `dil` **de** vermelisiniz..__\n\n`.derle java`")
            return

        gelen_dosya = await cevaplanan_mesaj.download()

        veri_listesi = None
        with open(gelen_dosya, "rb") as oku:
            veri_listesi = oku.readlines()

        inen_veri = ""
        for veri in veri_listesi:
            inen_veri += veri.decode("UTF-8")

        kod = inen_veri

        remove(gelen_dosya)

    elif cevaplanan_mesaj.text:
        if len(girilen_yazi) == 1:
            await ilk_mesaj.edit("__Derleyebilmek için `dil` **de** vermelisiniz..__\n\n`.derle java`")
            return
        kod = cevaplanan_mesaj.text

    else:
        await ilk_mesaj.edit("__güldük__")
        return

    uzanti = message.command[1]
    await ilk_mesaj.edit('`Derleniyor..`')

    try:
        await ilk_mesaj.edit(calistir(uzanti, kod))
    except KeyError:
        await ilk_mesaj.edit('__İstediğin dil maalesef benim sözlüğümde yok..__\n\n')
    except Exception as hata:
        await hata_log(hata)
        await ilk_mesaj.edit(f'**Hata Var !**\n\n`{type(hata).__name__}`\n\n__{hata}__')