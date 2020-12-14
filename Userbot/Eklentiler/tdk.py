# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Userbot.Edevat.zenginLog import log_yolla, hata_log
from Userbot import DESTEK_KOMUT, SESSION_ADI
from pathlib import Path

DESTEK_KOMUT.update({
    Path(__file__).stem : {
        "aciklama"  : "TDK Araması Yapar",
        "kullanim"  : [
            None
            ],
        "ornekler"  : [
            ".tdk kelime"
            ]
    }
})

from pyrogram import Client, filters
from pyrogram.types import Message
import json, aiohttp

class AioHttp:
    @staticmethod
    async def get_json(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.json()

    @staticmethod
    async def get_text(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.text()

    @staticmethod
    async def get_raw(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.read()

@Client.on_message(filters.command(['tdk'], ['!','.','/']) & filters.me)
async def tdk(client:Client, message:Message):
    # < Başlangıç
    await log_yolla(client, message)
    ilk_mesaj = await message.edit("__Bekleyin..__", disable_web_page_preview = True)
    #------------------------------------------------------------- Başlangıç >
    girilen_yazi        = message.text

    if len(girilen_yazi.split()) == 1:
        await ilk_mesaj.edit("Arama yapabilmek için `bişeyler` girmelisiniz")
        return
    
    kelime = " ".join(girilen_yazi.split()[1:])

    if len(kelime.split()) > 1:
        mesaj = "**Lütfen tek kelime girin**"
        return

    raw_veri = await AioHttp().get_raw(f"http://sozluk.gov.tr/gts?ara={kelime}")
    
    kelime_anlamlari = json.loads(raw_veri)

    if "error" in kelime_anlamlari:
        mesaj = f"`{kelime}` `sozluk.gov.tr` __sitesinde bulunamadı..__"
    else:
        mesaj = f"📚 **{kelime}** __Kelimesinin Anlamları:__\n\n"
        anlamlar = kelime_anlamlari[0]["anlamlarListe"]
        for anlam in anlamlar:
            mesaj += f"👉 `{anlam['anlam']}` \n"

    try:
        await ilk_mesaj.edit(mesaj)
    except Exception as hata:
        await hata_log(hata, ilk_mesaj)
        return