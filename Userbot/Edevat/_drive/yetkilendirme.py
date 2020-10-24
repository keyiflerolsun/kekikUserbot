# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from pyrogram.types import Message

from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from googleapiclient.discovery import build
import httplib2, os
from dotenv import load_dotenv

load_dotenv("ayar.env")

# Bu kapsamları değiştiriyorsanız, yeniden yetkilendirme almalısınız..
SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive.appdata',
    'https://www.googleapis.com/auth/drive.metadata'
]

# Bu Kısım driveSessionOlusturucu.py'dan temin edilir..
CLIENT_ID               = os.environ.get("CLIENT_ID", None)
CLIENT_SECRET           = os.environ.get("CLIENT_SECRET", None)

# evrensel dosya adı tanımı
G_DRIVE_TOKEN_DOSYASI   = "drive_erisim.json"

# Ortak Drive İşlemleri
ORTAK_DRIVE_ADI  = os.environ.get("ORTAK_DRIVE_ADI", None)
ORTAK_DRIVE_ID   = os.environ.get("ORTAK_DRIVE_ID", None)

async def kod_al(mesaj:Message):
    if os.path.exists(G_DRIVE_TOKEN_DOSYASI):
        await mesaj.edit('__Drive Yetkilendirmesi yapılmış..__')
        return

    flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, SCOPES, redirect_uri="urn:ietf:wg:oauth:2.0:oob")
    yetkilendirme_linki = flow.step1_get_authorize_url()

    await mesaj.edit(f'__Lütfen bağlantıya gidip yetkilendirme aşamalarını tamamlayın.. Ardından verilen kodu kopyalayın,\n\n`.gtoken _yetkilendirme_kodu_`\n\nşeklinde komutu uygulayın..__\n\n🗝 **[Google OAuth 2.0]({yetkilendirme_linki})**')     

async def token_olustur(mesaj:Message, token:str): # fiziksel olarak dosya bağımlılığı yoktur ve drive_erisim.json oluşturur
    flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, SCOPES, redirect_uri="urn:ietf:wg:oauth:2.0:oob")
    yetki_kodu = token.strip()
    kimlik_bilgileri = flow.step2_exchange(yetki_kodu)
    dosya = Storage(G_DRIVE_TOKEN_DOSYASI)
    dosya.put(kimlik_bilgileri)

def g_yetki():
    # Kişisel bilgilei alır
    kimlik_bilgileri = Storage(G_DRIVE_TOKEN_DOSYASI).get()
    # httplib2.Http objesi oluşturur ve kişisel bilgilerinizle yetkilendirir.
    http = httplib2.Http()
    kimlik_bilgileri.refresh(http)
    referans = kimlik_bilgileri.authorize(http)
    return build("drive", "v3", http=referans, cache_discovery=False)