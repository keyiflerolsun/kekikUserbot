# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Userbot.Edevat._drive.yetkilendirme import g_yetki
from os import environ, path
from Userbot import SESSION_ADI
from googleapiclient.http import MediaFileUpload
from httplib2 import RedirectMissingLocation
from mimetypes import guess_type
from math import floor


async def yukle_drive(dosya_yolu: str,
                      mesaj_duzenle,
                      drive_id: str = None,
                      drive_adi: str = None,
                      dizin_id: str = None) -> str:
    drive_service = g_yetki()
    mime_turu = guess_type(dosya_yolu)[0]
    mime_turu = mime_turu or "text/plain"
    dosya_adi = path.basename(dosya_yolu)

    try:
        drive_id = environ["ORTAK_DRIVE_ID"]
        drive_adi = environ["ORTAK_DRIVE_ADI"]

        govde = {
            "name": dosya_adi,
            "description": f"{SESSION_ADI} üzerinden yüklenmiştir..",
            "parents": [drive_id]
        }
    except KeyError:
        govde = {
            "name": dosya_adi,
            "description": f"{SESSION_ADI} üzerinden yüklenmiştir.."
        }

    dosya_govde = MediaFileUpload(dosya_yolu,
                                  mimetype=mime_turu,
                                  chunksize=-1,
                                  resumable=True)
    yuklenen_dosya = drive_service.files().create(supportsAllDrives=True,
                                                  body=govde,
                                                  media_body=dosya_govde)

    yanit = None
    gorunen_mesaj = ""
    while yanit is None:
        durum, yanit = yuklenen_dosya.next_chunk()
        if durum:
            yuzde = int(durum.progress() * 100)
            progress_str = "**[{0}{1}]**\n**Süreç** : __%__`{2}`\n".format(
                "".join(["●" for _ in range(floor(yuzde / 5))]),
                "".join(["○" for _ in range(20 - floor(yuzde / 5))]),
                round(yuzde, 2),
            )
            gecerli_mesaj = f"**Arşive yüklüyorum kanka..**\n**Dosya Adı**: `{dosya_adi}`\n{progress_str}"
            if gorunen_mesaj != gecerli_mesaj:
                try:
                    await mesaj_duzenle.edit(gecerli_mesaj)
                    gorunen_mesaj = gecerli_mesaj
                except RedirectMissingLocation:
                    continue

    dosya_id = yanit.get("id")

    mesaj = ""
    mesaj += f"`{drive_adi}` **Diskine** " if drive_adi else "`Root` **Diskine** "
    mesaj += "__Yükledim Kanka.. :__"
    link = f"https://drive.google.com/open?id={dosya_id}"

    return mesaj, link, dosya_adi
