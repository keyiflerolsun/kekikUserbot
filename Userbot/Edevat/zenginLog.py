# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

import datetime, pytz
from Userbot import SESSION_ADI, log_ver

tarih   = lambda : datetime.datetime.now(pytz.timezone("Turkey")).strftime("%d-%m-%Y")
saat    = lambda : datetime.datetime.now(pytz.timezone("Turkey")).strftime("%H:%M:%S")

async def log_yolla(client, message):
    log_dosya   = f"[{saat()} | {tarih()}] "
    sohbet      = await client.get_chat(message.chat.id)

    if message.from_user.username:
        log_konsol  = f"[bold red]@{message.from_user.username}[/] [green]||[/] "
        log_dosya  += f"@{message.from_user.username} | "
    else:
        log_konsol  = f"[bold red]{message.from_user.first_name}[/] [green]||[/] "
        log_dosya   = f"{message.from_user.first_name} | "

    if message.chat.type in ['private', 'bot']:
        log_konsol  += f"[yellow]{message.text}[/] "
        log_dosya   += f"{message.text} "
    else:
        grup_ad      = f'@{sohbet.username}' if sohbet.username else sohbet.title
        log_konsol  += f"[yellow]{message.text}[/]\t[green]||[/] [bold cyan]{grup_ad}[/] "
        log_dosya   += f"{message.text} | {grup_ad} "

    log_konsol  += f"  [green]||[/] [magenta]{message.chat.type}[/]"
    log_dosya   += f"\t| {message.chat.type}\n"

    log_ver(f"{log_konsol}")                                         # zenginKonsol'a log gönder

    with open(f"@{SESSION_ADI}.log", "a+") as log_yaz:               # dosyaya log yaz
        log_yaz.write(log_dosya)

async def hata_log(hata_soyle):
    hata_konsol  = f"\t\t[bold magenta]||[/] [bold grey74]{hata_soyle}[/]"
    hata_dosya   = f"\n\t\t\t\t\t{hata_soyle}\n\n"

    log_ver(f"{hata_konsol}")                                        # zenginKonsol'a log gönder

    with open(f"@{SESSION_ADI}.log", "a+") as log_yaz:               # dosyaya log yaz
        log_yaz.write(hata_dosya)
