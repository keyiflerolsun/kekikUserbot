# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Userbot.Edevat._drive.yetkilendirme import g_yetki

async def ortak_drive_listesi():
    """ telegram için ortak drive listesi çıkartır """
    drive_service  = g_yetki()
    ortak_drivelar = drive_service.drives().list(pageSize=10).execute()

    # import json
    # print(json.dumps(ortak_drivelar, indent=2, sort_keys=False, ensure_ascii=False))
    # return

    mesaj = "**Ortak Drive Listesi;**\n​➖​➖​➖​💃​\n\n"
    for drive in ortak_drivelar['drives']:
        mesaj += f"\t__{drive['name']}__\n`{drive['id']}`\n\n"

    return mesaj