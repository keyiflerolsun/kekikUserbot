# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

import os
from glob import glob

def icinden_gec(dizin):
    gecici_liste = glob(f"{dizin}/*.*")
    for dosya in gecici_liste:
        os.remove(dosya) 