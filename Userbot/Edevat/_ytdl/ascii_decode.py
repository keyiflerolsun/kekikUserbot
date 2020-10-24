# https://github.com/django/django/blob/master/django/utils/text.py#L394-#L407

import re, unicodedata

def slugify(deger, allow_unicode=False):
    """
    'Allow_unicode' False ise ASCII'ye dönüştürür.
    Boşlukları veya tekrarlanan kısa çizgileri tek tirelere dönüştürür.
    Alfasayısal, alt çizgi veya kısa çizgi olmayan karakterleri kaldırıp Küçük harfe dönüştür.
    Ayrıca baştaki ve sondaki beyaz boşlukları, tireleri ve alt çizgileri de çıkarır.
    """
    deger = str(deger)
    if allow_unicode:
        deger = unicodedata.normalize('NFKC', deger)
    else:
        deger = unicodedata.normalize('NFKD', deger).encode('ascii', 'ignore').decode('ascii')
    deger = re.sub(r'[^\w\s-]', '', deger.lower())
    return re.sub(r'[-\s]+', '-', deger).strip('-_')