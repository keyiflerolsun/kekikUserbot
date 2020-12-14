# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Userbot.Edevat.zenginLog import log_yolla, hata_log
from Userbot import DESTEK_KOMUT
from pathlib import Path

DESTEK_KOMUT.update({
    Path(__file__).stem : {
        "aciklama"     : "KekikSpatula'dan nöbetçi eczane bilgilerini verir..",
        "parametreler" : [
            "il ilçe"
            ],
        "ornekler"     : [
            ".nobetci çanakkale merkez"
            ]
    }
})

from pyrogram import Client, filters
from pyrogram.types import Message
from KekikSpatula import NobetciEczane

@Client.on_message(filters.command(['nobetci'],['!','.','/']) & filters.me)
async def nobetci(client:Client, message:Message):
    # < Başlangıç
    await log_yolla(client, message)
    ilk_mesaj = await message.edit("__Bekleyin..__", disable_web_page_preview = True)
    #------------------------------------------------------------- Başlangıç >
    girilen_yazi = message.command

    if len(girilen_yazi) == 1:
        await ilk_mesaj.edit("__Arama yapabilmek için `il` ve `ilçe` girmelisiniz..__")
        return
    elif len(girilen_yazi) == 2:
        await ilk_mesaj.edit("__Arama yapabilmek için `ilçe` **de** girmelisiniz..__")
        return

    il   = girilen_yazi[1].replace('İ', "i").lower()  # komut hariç birinci kelime
    ilce = girilen_yazi[2].replace('İ', "i").lower()  # komut hariç ikinci kelime

    tr2eng  = str.maketrans(" .,-*/+-ıİüÜöÖçÇşŞğĞ", "________iIuUoOcCsSgG")
    il      = il.translate(tr2eng)
    ilce    = ilce.translate(tr2eng)

    mesaj = f"**Aranan Nöbetçi Eczane :** `{ilce}` / `{il}`\n"

    eczaneler = NobetciEczane(il, ilce).veri['veri']
    try:
        for eczane in eczaneler:
            mesaj += f"**\n\t⚕ {eczane['ad']}**"
            mesaj += f"\n📍"
            if eczane['mahalle']:
                mesaj += f"`{eczane['mahalle']}`\n"
            mesaj += f"__{eczane['adres']}__"
            if eczane['tarif']:
                mesaj += f"\n**({eczane['tarif']})**"
            mesaj += f"\n\t☎️ `{eczane['telefon']}`\n\n"

        await ilk_mesaj.edit(mesaj)
    except IndexError:
        await ilk_mesaj.edit(f'__`{ilce}` / `{il}` diye bir yer bulamadım..__')
    except Exception as hata:
        await hata_log(hata, ilk_mesaj)
        return