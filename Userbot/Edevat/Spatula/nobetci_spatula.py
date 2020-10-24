# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

import requests, json
from bs4 import BeautifulSoup
from tabulate import tabulate

kullanim =  {
    'kullanim' : [
        'nobetciEczane("canakkale", "merkez", "json_veri")',
        'nobetciEczane("canakkale", "merkez", "json_gorsel")',
        'nobetciEczane("canakkale", "merkez", "gorsel_veri")',
        'nobetciEczane("canakkale", "merkez", "basliklar")'
    ]
}

def nobetci_eczane(il=None, ilce=None, cikti='gorsel_veri'):
    """
    eczaneler.gen.tr Nöbetçi Eczane Verileri
        Kullanım;
                nobetciEczane("canakkale", "merkez", "json_veri")
                nobetciEczane("canakkale", "merkez", "json_gorsel")
                nobetciEczane("canakkale", "merkez", "gorsel_veri")
                nobetciEczane("canakkale", "merkez", "basliklar")
    """
    il = il.lower()
    try:
        ilce = ilce.lower()
    except AttributeError:
        return kullanim

    tr2eng = str.maketrans(" .,-*/+-ıİüÜöÖçÇşŞğĞ", "________iIuUoOcCsSgG")
    il = il.translate(tr2eng)
    ilce = ilce.translate(tr2eng)

    url = f"https://www.eczaneler.gen.tr/nobetci-{il}-{ilce}"
    kimlik = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

    istek = requests.get(url, headers=kimlik)
    # print(istek)
    # print(istek.headers)

    corba = BeautifulSoup(istek.content, "lxml")
    bugun = corba.find('div', id='nav-bugun')

    liste = []
    for bak in bugun.findAll('tr')[1:]:
        ad    = bak.find('span', class_='isim').text
        mah   = None if bak.find('div', class_='my-2') == None else bak.find('div', class_='my-2').text
        adres = bak.find('span', class_='text-capitalize').text
        tarif = None if bak.find('span', class_='text-secondary font-italic') == None else bak.find('span', class_='text-secondary font-italic').text
        telf  = bak.find('div', class_='col-lg-3 py-lg-2').text

        liste.append({
            'ad'        : ad,
            'mahalle'   : mah,
            'adres'     : adres,
            'tarif'     : tarif,
            'telefon'   : telf
        })

    basliklar = [anahtar for anahtar in liste[0].keys()]

    if cikti == 'json_veri':
        return liste

    elif cikti == 'json_gorsel':
        return json.dumps(liste, indent=2, sort_keys=False, ensure_ascii=False)

    elif cikti == 'gorsel_veri':
        return tabulate(liste, headers='keys', tablefmt='psql')

    elif cikti == 'basliklar':
        return basliklar

    else:
        return kullanim