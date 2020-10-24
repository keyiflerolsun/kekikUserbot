# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Userbot.Edevat.zenginLog import log_yolla, hata_log
from Userbot import DESTEK_KOMUT
from pathlib import Path

DESTEK_KOMUT.update({
    Path(__file__).stem : {
        "aciklama" : "Çeşitli GoogleDrive İşlemleri",
        "kullanim" : [
            "`.gyetki` Komutuyla Yetkilendirme Linki Alın!",
            "`.gtoken kod` Komutuyla Token'inizi tanıtın..",
            "`.gortaklar` Komutuyla ortak drive listenizi alın..",
            "`.gdisk ortak_id` Komutuyla ortak drive dizini belirlenir..",
            "`.gdizin` Komutuyla aktif dizin bilgisini görün..",
            "`.gara bişiy` Komutuyla disk'inizde arama yapın..",
            "`.gyukle` mesaj yanıtlayarak ilgili dizine dosya yüklemesi yapın.."
            ],
        "ornekler" : [
            ".gyetki",
            ".gtoken kod",
            ".gortaklar",
            ".gdisk ortak_id",
            ".gdizin",
            ".gara winrar",
            ".gyukle «Yanıtlanan Dosya/Media»"
            ]
    }
})

from pyrogram import Client, filters
from pyrogram.errors import MessageTooLong
from Userbot.Edevat._drive.yetkilendirme import kod_al, token_olustur, G_DRIVE_TOKEN_DOSYASI, g_yetki
from Userbot.Edevat._drive.drivedaAra import ara_drive
from Userbot.Edevat._drive.ortakDrivelar import ortak_drive_listesi
from oauth2client.client import FlowExchangeError
import os, time
from Userbot.Edevat._drive.driveYukle import yukle_drive
from Userbot import INDIRME_ALANI
from Userbot.Edevat.gecici_alan_temizleyici import icinden_gec
from Userbot.Edevat._pyrogram.progress import pyro_progress
from Userbot.Edevat._pyrogram.pyro_yardimcilari import yanitlanan_mesaj
from datetime import datetime

@Client.on_message(filters.command(['gyetki'],['!','.','/']) & filters.me)
async def gyetki(client, message):
    # < Başlangıç
    await log_yolla(client, message)
    ilk_mesaj = await message.edit("__Bekleyin..__",
        disable_web_page_preview    = True,
        parse_mode                  = "Markdown"
    )
    #------------------------------------------------------------- Başlangıç >

    await kod_al(ilk_mesaj)

@Client.on_message(filters.command(['gtoken'],['!','.','/']) & filters.me)
async def gtoken(client, message):
    # < Başlangıç
    await log_yolla(client, message)
    ilk_mesaj = await message.edit("__Bekleyin..__",
        disable_web_page_preview    = True,
        parse_mode                  = "Markdown"
    )
    #------------------------------------------------------------- Başlangıç >

    try:
        await token_olustur(ilk_mesaj, message.command[1])
    except IndexError as hata:
        await hata_log(hata)
        await ilk_mesaj.edit('`Kod Girmedin..`')
        return
    except FlowExchangeError as hata:
        await hata_log(hata)
        await ilk_mesaj.edit('`Vermiş olduğun kod geçersiz..`')
        return

    await ilk_mesaj.edit('**Drive Yetkilendirme Başarılı!**')

@Client.on_message(filters.command(['gortaklar'],['!','.','/']) & filters.me)
async def gortaklar(client, message):
    # < Başlangıç
    await log_yolla(client, message)
    ilk_mesaj = await message.edit("__Bekleyin..__",
        disable_web_page_preview    = True,
        parse_mode                  = "Markdown"
    )
    #------------------------------------------------------------- Başlangıç >
    if not os.path.exists(G_DRIVE_TOKEN_DOSYASI):
        await kod_al(ilk_mesaj)
        await message.reply('**Önce Yetkilendirme Yapmalısın..**')
        return

    await ilk_mesaj.edit(await ortak_drive_listesi())

@Client.on_message(filters.command(['gdisk'],['!','.','/']) & filters.me)
async def gdisk(client, message):
    # < Başlangıç
    await log_yolla(client, message)
    ilk_mesaj = await message.edit("__Bekleyin..__",
        disable_web_page_preview    = True,
        parse_mode                  = "Markdown"
    )
    #------------------------------------------------------------- Başlangıç >
    try:
        message.command[1]
    except IndexError:
        await ilk_mesaj.edit('__Lütfen ID Giriniz..__')
        return

    if not os.path.exists(G_DRIVE_TOKEN_DOSYASI):
        await kod_al(ilk_mesaj)
        await message.reply('**Önce Yetkilendirme Yapmalısın..**')
        return

    drive_service  = g_yetki()
    ortak_drivelar = drive_service.drives().list(pageSize=10).execute()
    team_liste     = [{
                        "adi" : drive['name'],
                        "id"  : drive['id']
                    } for drive in ortak_drivelar['drives']
                    ]
    drive_adi = [drive['adi'] for drive in team_liste]
    drive_id  = [drive['id'] for drive in team_liste]

    if message.command[1] in drive_id:
        os.environ["ORTAK_DRIVE_ID"]  = message.command[1]
        os.environ["ORTAK_DRIVE_ADI"] = drive_adi[drive_id.index(os.environ["ORTAK_DRIVE_ID"])]
        ORTAK_DRIVE_ADI  = os.environ["ORTAK_DRIVE_ADI"]
    else:
        await message.edit('**Ortak Drive ID Bulunamadı!**')
        return

    await ilk_mesaj.edit(f"`{ORTAK_DRIVE_ADI}` __varsayılan olarak ayarlandı..__")

@Client.on_message(filters.command(['gdizin'],['!','.','/']) & filters.me)
async def gdizin(client, message):
    # < Başlangıç
    await log_yolla(client, message)
    ilk_mesaj = await message.edit("__Bekleyin..__",
        disable_web_page_preview    = True,
        parse_mode                  = "Markdown"
    )
    #------------------------------------------------------------- Başlangıç >
    if not os.path.exists(G_DRIVE_TOKEN_DOSYASI):
        await kod_al(ilk_mesaj)
        await message.reply('**Önce Yetkilendirme Yapmalısın..**')
        return

    try:
        drive_id  = os.environ["ORTAK_DRIVE_ID"]
        drive_adi = os.environ["ORTAK_DRIVE_ADI"]

        await ilk_mesaj.edit(f"__Burdasın kanka;__\n\n**{drive_adi}**\n`{drive_id}`")
    except KeyError:
        await ilk_mesaj.edit(f"__Burdasın kanka;__\n\n**Root**")

@Client.on_message(filters.command(['gara'],['!','.','/']) & filters.me)
async def gara(client, message):
    # < Başlangıç
    await log_yolla(client, message)
    ilk_mesaj = await message.edit("__Bekleyin..__",
        disable_web_page_preview    = True,
        parse_mode                  = "Markdown"
    )
    #------------------------------------------------------------- Başlangıç >
    if not os.path.exists(G_DRIVE_TOKEN_DOSYASI):
        await kod_al(ilk_mesaj)
        await message.reply('**Önce Yetkilendirme Yapmalısın..**')
        return

    try:
        await ilk_mesaj.edit(await ara_drive(arama_kelimesi=message.command[1]),
            disable_web_page_preview = True
        )
    except (MessageTooLong, OSError) as hata:
        await hata_log(hata)
        await ilk_mesaj.edit('__Çıktı çok uzun kanka daha spesifik şekilde aramalısın..__')
        return

@Client.on_message(filters.command(['gyukle'],['!','.','/']) & filters.me)
async def gyukle(client, message):
    # < Başlangıç
    await log_yolla(client, message)
    ilk_mesaj = await message.edit("__Bekleyin..__",
        disable_web_page_preview    = True,
        parse_mode                  = "Markdown"
    )
    #------------------------------------------------------------- Başlangıç >
    if not os.path.exists(G_DRIVE_TOKEN_DOSYASI):
        await kod_al(ilk_mesaj)
        await message.reply('**Önce Yetkilendirme Yapmalısın..**')
        return


    yanitlanacak_mesaj  = yanitlanan_mesaj(message)
    cevaplanan_mesaj    = message.reply_to_message
    girilen_yazi        = message.text

    if not cevaplanan_mesaj or cevaplanan_mesaj.text:
        await ilk_mesaj.edit('__Yalnızca cevaplanan mesajın döküman olması halinde çalışır..__')
        return

    baslangic_zaman = datetime.now()
    if cevaplanan_mesaj:
        simdiki_zaman = time.time()
        gelen_dosya = await client.download_media(
            message         =   cevaplanan_mesaj,
            progress        =   pyro_progress,
            file_name       =   INDIRME_ALANI,
            progress_args   =  ("**__Dosyayı indiriyorum kankamm...__**", ilk_mesaj, simdiki_zaman)
        )
        bitis_zaman = datetime.now()
        sure = (bitis_zaman - baslangic_zaman).seconds
        await ilk_mesaj.edit(
            f"<u>{sure}</u> Saniye'de\n\n<code>{gelen_dosya}</code> buraya indirdim",
            parse_mode="html"
        )
    else:
        await ilk_mesaj.edit('__Şimdilik Sadece yanıtlanan dosyalarda çalışıyorum..__')
        return

    try:
        ORTAK_DRIVE_ADI  = os.environ["ORTAK_DRIVE_ADI"]
    except KeyError:
        ORTAK_DRIVE_ADI = "Root"

    await ilk_mesaj.edit(f'`{gelen_dosya.split("/")[-1]}` __indi kankam,__\n\n**{ORTAK_DRIVE_ADI}** __diskine yüklüyorum..__')

    mesaj, link, dosya_adi = await yukle_drive(gelen_dosya, ilk_mesaj)
    await ilk_mesaj.delete()
    
    mesaj += f"\n\n**[{dosya_adi}]({link})**"
    
    await message.reply(mesaj, reply_to_message_id = yanitlanacak_mesaj, disable_web_page_preview=True)
    
    icinden_gec(INDIRME_ALANI)
