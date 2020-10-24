# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Userbot.Edevat.zenginLog import log_yolla, hata_log
from Userbot import DESTEK_KOMUT
from pathlib import Path

DESTEK_KOMUT.update({
    Path(__file__).stem : {
        "aciklama"  : "@QuotLyBot kullanarak stikır yapar..",
        "kullanim"  : [
            "Yanıtlanan Mesaj",
            "Metin"
            ],
        "ornekler"  : [
            ".stik KekikAkademi"
            ]
    }
})

from pyrogram import Client, filters
from Userbot.Edevat._pyrogram.pyro_yardimcilari import yanitlanan_mesaj
import asyncio, random

@Client.on_message(filters.command("stik", ['!','.','/']) & filters.me)
async def stik(client, message):
    # < Başlangıç
    await log_yolla(client, message)
    yanitlanacak_mesaj = yanitlanan_mesaj(message)
    ilk_mesaj = await message.edit("__Bekleyin..__",
        disable_web_page_preview    = True,
        parse_mode                  = "Markdown"
    )
    cevaplanan_mesaj    = message.reply_to_message
    #------------------------------------------------------------- Başlangıç >

    if cevaplanan_mesaj is None:
        await ilk_mesaj.edit("__stikır yapılacak mesajı yanıtlamalısın..__")
        return

    stik_botu = '@QuotLyBot'
    await cevaplanan_mesaj.forward(stik_botu)
    mesaj = await client.get_history(stik_botu, 1)
    await ilk_mesaj.edit("`Stikır yapıyorum`")

    stik_mi = False
    bar = 0
    hata_limit = 0

    while not stik_mi:
        try:
            mesaj = await client.get_history(stik_botu, 1)
            _ = mesaj[0]["sticker"]["file_id"]
            stik_mi = True
        except TypeError:
            await asyncio.sleep(0.5)
            bar += random.randint(0, 10)

            try:
                await ilk_mesaj.edit(f"**Stikır**\n\n`İşleniyor %{bar}`", parse_mode="md")

            except Exception as hata:
                if hata_limit == 3:
                    break

                await hata_log(hata)
                await ilk_mesaj.edit(f'**Hata Var !**\n\n__{hata}')

                hata_limit += 1

    await ilk_mesaj.edit("`Tamamlandı !`", parse_mode="md")
    stik_id = mesaj[0]["sticker"]["file_id"]
    await message.reply_sticker(stik_id, reply_to_message_id=yanitlanacak_mesaj)
    await client.read_history(stik_botu)
    await ilk_mesaj.delete()