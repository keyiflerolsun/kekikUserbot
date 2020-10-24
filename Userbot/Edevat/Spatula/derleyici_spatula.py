# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from requests import get, post
from bs4 import BeautifulSoup
from time import sleep

def calistir(dil, kod, _input=None):
    base_link = "https://www.ideone.com"
    post_link = "https://www.ideone.com/ideone/Index/submit/"
    ajax_link = "https://www.ideone.com/ideone/Index/view/id"

    ilk_istek = get(base_link)
    ilk_corba = BeautifulSoup(ilk_istek.content, "html.parser")

    p1 = ilk_corba.find(id="p1").get("value")
    p2 = int(ilk_corba.find(id="p2").get("value"))
    p3 = int(ilk_corba.find(id="p3").get("value"))
    p4 = int((p2 * p3 * (p3 - 1)) / 2)

    desteklenen_diller = {
        "bash"               : "28",
        "pascal"             : "22",
        "c"                  : "11",
        "perl"               : "3",
        "c#"                 : "27",
        "php"                : "29",
        "c++"                : "1",
        "cpython"            : "4",
        "c++14"              : "44",
        "python"             : "116",
        "haskell"            : "21",
        "ruby"               : "17",
        "java_hotspot"       : "10",
        "sqlite"             : "40",
        "objectivec"         : "43",
        "swift"              : "85",
        "pascal_gpc"         : "2",
        "vb.net"             : "50",
        "ada95"              : "7",
        "commonlisp_sb"      : "31",
        "java"               : "55",
        "prolog_swi"         : "15",
        "asm32"              : "45",
        "commonlisp"         : "32",
        "js"                 : "35",
        "python2"            : "99",
        "asm32_nasm"         : "13",
        "d"                  : "20",
        "js_monkey"          : "112",
        "python3_nbc"        : "126",
        "asm"                : "42",
        "d_ldc"              : "84",
        "kotlin"             : "47",
        "r"                  : "117",
        "awk"                : "104",
        "d_dmd"              : "102",
        "lua"                : "26",
        "racket"             : "95",
        "awk_mawk"           : "105",
        "dart"               : "48",
        "nemerle"            : "30",
        "rust"               : "93",
        "bc"                 : "110",
        "elixir"             : "96",
        "nice"               : "25",
        "scala"              : "39",
        "brainf**k"          : "12",
        "erlang"             : "36",
        "nim"                : "122",
        "scheme"             : "33",
        "c_clang"            : "81",
        "f#"                 : "124",
        "node"               : "56",
        "scheme_stalin"      : "18",
        "c++_gcc4"           : "41",
        "fantom"             : "92",
        "objectivec_clang"   : "83",
        "scheme_c"           : "97",
        "c++14_c"            : "82",
        "forth"              : "107",
        "ocaml"              : "8",
        "smalltalk"          : "23",
        "c99"                : "34",
        "fortran"            : "5",
        "octave"             : "127",
        "tcl"                : "38",
        "clips"              : "14",
        "go"                 : "114",
        "perl_2018"          : "54",
        "text"               : "62",
        "clojure"            : "111",
        "gosu"               : "98",
        "picolisp"           : "94",
        "unlambda"           : "115",
        "cobol"              : "118",
        "groovy"             : "121",
        "pike"               : "19",
        "vb.net_3"           : "101",
        "cobol85"            : "106",
        "icon"               : "16",
        "prolog"             : "108",
        "whitespace"         : "6",
        "coffeescript"       : "91",
        "intercal"           : "9"
    }

    post_data = {
        'p1': p1,
        'p2': str(p2),
        'p3': str(p3),
        'p4': str(p4),
        'file': kod,
        '_lang': desteklenen_diller[dil],
        'input': _input,
        'run': 1
    }

    post_istek = post(post_link, data=post_data, allow_redirects=False, cookies=ilk_istek.cookies)

    while True:
        sleep(1)
        ajax_istek = post(ajax_link + post_istek.headers["location"] + "+/ajax/1/lp/1").json()
        if (int(ajax_istek['status']) == 0):
            break

    if (len(ajax_istek['stdout']) > 0):
        return f"**Output :** \n\n__{ajax_istek['stdout']}__"

    if (len(ajax_istek['stderr']) > 0):
        return f"**Stderr :** \n\n__{ajax_istek['stderr']}__"

    if (len(ajax_istek['cmperr']) > 0):
        return f"**Compiler Error** : \n\n__{ajax_istek['cmperr']}__"

# print(calistir("c", """
# #include <stdio.h>
# int main() 
# {
#   printf("Biz mafyamıyız, iş adamıyız..");
#   return 0;
# }
# """))