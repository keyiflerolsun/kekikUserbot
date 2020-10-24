# https://github.com/Skuzzy_xD/TelePyroBot

from Userbot.Edevat._pyrogram.okunabilir_byte import okunabilir_byte
from Userbot.Edevat._pyrogram.zaman_donustur import zaman_donustur
from pyrogram.errors import FloodWait
import math, time, asyncio

async def pyro_progress(gecerli, toplam, olay_turu, mesaj, baslangic):
    simdi = time.time()
    degisim = simdi - baslangic
    if round(degisim % 10.00) == 0 or gecerli == toplam:
        # if round(gecerli / toplam * 100, 0) % 5 == 0:
        yuzde = gecerli * 100 / toplam
        hiz = gecerli / degisim
        gecen_zaman = round(degisim)
        tamamlanma_zamani = round((toplam - gecerli) / hiz)
        tahmini_toplam_sure = tamamlanma_zamani

        # print(f"""
        # simdi       : {zamanDonustur(simdi)}
        # baslangic   : {zamanDonustur(baslangic)}
        # degisim     : {zamanDonustur(degisim)}
        # yuzde       : {round(yuzde, 2)}
        # hiz         : {okunabilir_byte(hiz)}
        # gecen zamn  : {zamanDonustur(gecen_zaman)}
        # tamamlanma  : {zamanDonustur(tamamlanma_zamani)}
        # tahmini     : {zamanDonustur(tahmini_toplam_sure)}
        # """)

        gecen_zaman = zaman_donustur(gecen_zaman)
        tahmini_toplam_sure = zaman_donustur(tahmini_toplam_sure)

        progress = "**[{0}{1}]**\n__%{2}__\t~\t".format(
            "".join(["●" for _ in range(math.floor(yuzde / 5))]),       # 🟥 █ ●
            "".join(["○" for _ in range(20 - math.floor(yuzde / 5))]),  # ⬜ ░ ○
            round(yuzde, 2),
        )

        toparla = progress
        toparla += f"`{okunabilir_byte(gecerli)}` __/__ **{okunabilir_byte(toplam)}**\n\n"
        toparla += f"**Hız:** `{okunabilir_byte(hiz)}/s`\n"
        toparla += f"**Tahmini:** __{tahmini_toplam_sure or 'Bitti de son bi kaç ayar yapıyorum..'}__\n"

        if mesaj.text != toparla:
            try:
                await mesaj.edit(f"{olay_turu}\n {toparla}")
            except FloodWait:
                await asyncio.sleep(5)