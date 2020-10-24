# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Userbot.Edevat.zenginLog import log_yolla
from Userbot import DESTEK_KOMUT
from pathlib import Path

DESTEK_KOMUT.update({
    Path(__file__).stem : {
        "aciklama"  : "yanıtlanan mesajdan itibaren temizlik yapar..",
        "kullanim"  : [
            "yanıtlanan mesaj"
            ],
        "ornekler"  : [
            ".dell"
            ]
    }
})

from pyrogram import Client, filters
from pyrogram.types import Message
from Userbot import SESSION_ADI
import asyncio

async def admin_kontrol(client:Client, message:Message) -> bool:
    chat_id = message.chat.id
    user_id = message.from_user.id

    durum_kontrol = await client.get_chat_member(
        chat_id =   chat_id,
        user_id =   user_id
    )

    yonetici = ["creator", "administrator"]

    return durum_kontrol.status in yonetici

@Client.on_message(filters.command("imha", ['!','.','/']) & filters.me)
async def imha(client, message):
    # < Başlangıç
    await log_yolla(client, message)
    ilk_mesaj = await message.edit("__Bekleyin..__",
        disable_web_page_preview    = True,
        parse_mode                  = "Markdown"
    )
    cevaplanan_mesaj    = message.reply_to_message
    #------------------------------------------------------------- Başlangıç >

    if cevaplanan_mesaj is None:
        await ilk_mesaj.edit("__içinden geçmek istediğiniz yerden mesaj yanıtlayın__")
        return

    if message.chat.type in ("supergroup", "channel"):
        if not await admin_kontrol(client, message):
            await ilk_mesaj.edit("__Admin değilmişim :)__")
            await asyncio.sleep(2)
            await ilk_mesaj.delete()
            return

    elif message.chat.type in ["private", "bot", "group"]:
        await ilk_mesaj.edit("`Bu komutu burda kullanamazsın..`")
        await asyncio.sleep(2)
        await ilk_mesaj.delete()
        return

    silinecek_mesaj_idleri = []
    silinen_mesaj_sayisi = 0

    for gecerli_mesaj_id in range(cevaplanan_mesaj.message_id, message.message_id):
        silinecek_mesaj_idleri.append(gecerli_mesaj_id)

        # Eğer 100 tane seçtiysen;
        if len(silinecek_mesaj_idleri) == 100: #TG_MAX_SELECT_LEN
            await client.delete_messages(
                chat_id     = message.chat.id,
                message_ids = silinecek_mesaj_idleri,
                revoke      = True
            )
            silinen_mesaj_sayisi += len(silinecek_mesaj_idleri)
            silinecek_mesaj_idleri = []

    # Eğer 100'den az kaldıysa;
    if silinecek_mesaj_idleri:
        await client.delete_messages(
            chat_id     = message.chat.id,
            message_ids = silinecek_mesaj_idleri,
            revoke      = True
        )
        silinen_mesaj_sayisi += len(silinecek_mesaj_idleri)

    mesaj = f"`<u>{silinen_mesaj_sayisi}</u> Adet Mesaj Silindi..`"
    await ilk_mesaj.edit(f"{mesaj}\n\n__{SESSION_ADI} `.imha` Eklentisi..__")
    await asyncio.sleep(3)
    await ilk_mesaj.edit(mesaj)