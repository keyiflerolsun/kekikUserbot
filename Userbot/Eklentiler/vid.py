# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Userbot.Edevat.zenginLog import log_yolla
from Userbot import DESTEK_KOMUT
from pathlib import Path

DESTEK_KOMUT.update({
    Path(__file__).stem : {
        "aciklama"  : "Çeşitli platformlardan ytdl kullanarak video indirir..",
        "kullanim"  : [
            "video |mp3| video linki",
            "yanıtlanan mesaj |mp3|"
            ],
        "ornekler"  : [
            ".vid",
            ".vid mp3",
            ".vid http://www.youtube.com/watch?v=kCsq4GAZODc",
            ".vid mp3 http://www.youtube.com/watch?v=kCsq4GAZODc",
            ".vid https://www.dailymotion.com/video/x607vr2",
            ".vid mp3 https://www.dailymotion.com/video/x607vr2",
            "vebenzeri"
            ]
    }
})

from Userbot.Edevat._ytdl.link_islemleri import link_ayikla
from Userbot.Edevat._ytdl.ytdl_indirici import ytdl_indirici
from Userbot.Edevat._pyrogram.progress import pyro_progress
from Userbot.Edevat.gecici_alan_temizleyici import icinden_gec
from Userbot import INDIRME_ALANI, SESSION_ADI
from Userbot.Edevat._pyrogram.pyro_yardimcilari import yanitlanan_mesaj, kullanici
from pyrogram import Client, filters
from pyrogram.types import Message
from asyncio import sleep
import time

@Client.on_message(filters.command(['vid'], ['!','.','/']) & filters.me)
async def vid(client:Client, message:Message):
    # < Başlangıç
    await log_yolla(client, message)
    yanit_id  = await yanitlanan_mesaj(message)
    ilk_mesaj = await message.edit("__Bekleyin..__", disable_web_page_preview = True)
    #------------------------------------------------------------- Başlangıç >
    girilen_yazi        = message.text
    cevaplanan_mesaj    = message.reply_to_message

    kullanici_adi, _ = await kullanici(message)

    try:
        if (not cevaplanan_mesaj) and (len(message.command) == 1):
            await ilk_mesaj.edit("Arama yapabilmek için `Youtube Linki` girmelisiniz, veya @vid __mesajı yanıtlamalısınız..__")
            return

        if not cevaplanan_mesaj:
            verilen_link = await link_ayikla(girilen_yazi)
        elif cevaplanan_mesaj.text:
            try:
                verilen_link = await link_ayikla(cevaplanan_mesaj.text)
            except TypeError:
                verilen_link = await link_ayikla(girilen_yazi)
    except TypeError:
        await ilk_mesaj.edit('__jajajajaj güldük..__')
        return

    simdiki_zaman = time.time()
    if (len(message.command) > 1) and (message.command[1] == 'mp3'):
        try:
            yt_baslik, yt_resim, inen_veri, ilk_mesaj = await ytdl_indirici(ilk_mesaj, verilen_link[0], parametre='mp3')
        except UnboundLocalError:
            await ilk_mesaj.edit('__jajajajaj güldük..__')
            return
        indirdim_kanka = await client.send_audio(
            chat_id             = message.chat.id,
            audio               = inen_veri,
            caption             = f"`{SESSION_ADI}` aracılığıyla __indirdim kankam..__\n\n**{yt_baslik}**",
            title               = yt_baslik,
            performer           = SESSION_ADI,
            thumb               = yt_resim,
            progress            = pyro_progress,
            progress_args       = (f"__{yt_baslik}__\n\n**Yüklüyorum kankamm...**", ilk_mesaj, simdiki_zaman),
            reply_to_message_id = yanit_id
        )
    else:
        try:
            yt_baslik, yt_resim, inen_veri, ilk_mesaj = await ytdl_indirici(ilk_mesaj, verilen_link[0])
        except UnboundLocalError:
            await ilk_mesaj.edit('__jajajajaj güldük..__')
            return
        indirdim_kanka = await client.send_video(
            chat_id             = message.chat.id,
            video               = inen_veri,
            caption             = f"`{SESSION_ADI}` aracılığıyla __indirdim kankam..__\n\n**{yt_baslik}**",
            thumb               = yt_resim,
            progress            = pyro_progress,
            progress_args       = (f"__{yt_baslik}__\n\n**Yüklüyorum kankamm...**", ilk_mesaj, simdiki_zaman),
            reply_to_message_id = yanit_id
        )


    if (cevaplanan_mesaj) and (cevaplanan_mesaj.via_bot):
        await cevaplanan_mesaj.delete()

    print('\n')

    await icinden_gec(INDIRME_ALANI)

    await ilk_mesaj.delete()
    await sleep(5)
    await indirdim_kanka.edit(f"**{yt_baslik}**") 