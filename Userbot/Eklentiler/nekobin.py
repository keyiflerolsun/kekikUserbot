# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Userbot.Edevat.zenginLog import log_yolla, hata_log
from Userbot import DESTEK_KOMUT, SESSION_ADI
from pathlib import Path

DESTEK_KOMUT.update({
    Path(__file__).stem : {
        "aciklama"  : "nekobin.com ile entegreli paste hizmeti..\nkodu paste yapar, paste linkini betiğe çevirir..",
        "kullanim"  : [
            "Yanıtlanan Mesaj",
            "Yanıtlanan Dosya",
            "Metin"
            ],
        "ornekler"  : [
            ".nekover py «__yanıtlanan kod__»",
            ".nekover go «__yanıtlanan dosya__»",
            ".nekoal «__yanıtlanan nekobin linki__»"
            ]
    }
})

from pyrogram import Client, filters
from Userbot.Edevat._pyrogram.pyro_yardimcilari import yanitlanan_mesaj
from Userbot.Edevat.link_ayikla import link_ayikla
import aiohttp, os, requests

@Client.on_message(filters.command(['nekover'], ['!','.','/']) & filters.me)
async def nekover(client, message):
    # < Başlangıç
    await log_yolla(client, message)
    ilk_mesaj = await message.edit("__Bekleyin..__",
        disable_web_page_preview    = True,
        parse_mode                  = "Markdown"
    )
    girilen_yazi        = message.command
    cevaplanan_mesaj    = message.reply_to_message
    yanitlanacak_mesaj  = yanitlanan_mesaj(message)
    #------------------------------------------------------------- Başlangıç >

    if cevaplanan_mesaj is None:
        if len(girilen_yazi) == 1:
            await ilk_mesaj.edit("__Paste yapabilmek için `uzantı` ve `kod` vermelisiniz..__")
            return
        elif len(girilen_yazi) == 2:
            await ilk_mesaj.edit("__Paste yapabilmek için `uzantı` **da** vermelisiniz..__\n\n`.nekover py` **kod**")
            return

        kod = " ".join(girilen_yazi[2:]) 

    elif cevaplanan_mesaj and cevaplanan_mesaj.document:
        if len(girilen_yazi) == 1:
            await ilk_mesaj.edit("__Paste yapabilmek için `uzantı` **da** vermelisiniz..__\n\n`.nekover py`")
            return

        gelen_dosya = await cevaplanan_mesaj.download()

        veri_listesi = None
        with open(gelen_dosya, "rb") as oku:
            veri_listesi = oku.readlines()

        inen_veri = ""
        for veri in veri_listesi:
            inen_veri += veri.decode("UTF-8")

        kod = inen_veri

        os.remove(gelen_dosya)

    elif cevaplanan_mesaj.text:
        if len(girilen_yazi) == 1:
            await ilk_mesaj.edit("__Paste yapabilmek için `uzantı` **da** vermelisiniz..__\n\n`.nekover py`")
            return
        kod = cevaplanan_mesaj.text

    else:
        await ilk_mesaj.edit("__güldük__")
        return

    uzanti = message.command[1]
    await ilk_mesaj.delete()

    async with aiohttp.ClientSession() as session:
        async with session.post(
                'https://nekobin.com/api/documents',
                json={"content": kod},
                timeout=3
        ) as response:
            key = (await response.json())["result"]["key"]

    await message.reply(f'`{SESSION_ADI}` __tarafından dönüştürülmüştür..__\n\n**https://nekobin.com/{key}.{uzanti}**',
                  disable_web_page_preview  = True,
                  reply_to_message_id       = yanitlanacak_mesaj
    )

@Client.on_message(filters.command(['nekoal'], ['!','.','/']) & filters.me)
async def nekoal(client, message):
    # < Başlangıç
    await log_yolla(client, message)
    ilk_mesaj = await message.edit("__Bekleyin..__",
        disable_web_page_preview    = True,
        parse_mode                  = "Markdown"
    )
    cevaplanan_mesaj    = message.reply_to_message
    ayiklanan_linkler   = link_ayikla(cevaplanan_mesaj.text)
    #------------------------------------------------------------- Başlangıç >

    if cevaplanan_mesaj is None:
        await ilk_mesaj.edit("__script'e çevrilecek nekobin linki yanıtlamanız gerekli..__")
        return
    elif not ayiklanan_linkler[0].startswith("https://nekobin.com"):
        await ilk_mesaj.edit("__sadece nekobin linki yanıtlaman gerekli..__\n\n`.nekoal`")
        return

    kod = cevaplanan_mesaj.text.split('/')[-1]
    raw = 'https://nekobin.com/raw/' + kod

    try:
        data = requests.get(raw).content
    except Exception as hata:
        await hata_log(hata)
        await ilk_mesaj.edit(f'**Hata Var !**\n\n`{type(hata).__name__}`\n\n__{hata}__')
        return

    await ilk_mesaj.delete()

    with open(f'{kod}', "wb+") as dosya: dosya.write(data)

    await message.reply_document(
            document                    = f"{kod}",
            caption                     = f'__{SESSION_ADI} tarafından dönüştürülmüştür..__',
            disable_notification        = True,
            reply_to_message_id         = cevaplanan_mesaj.message_id
    )
    os.remove(f"{kod}")