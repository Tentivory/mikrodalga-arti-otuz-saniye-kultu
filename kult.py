#!/usr/bin/env python3
"""Mikrodalga +30 saniye kültü. Gerçekten çalışır. Yemek ısınmaz."""

from __future__ import annotations

import argparse
import base64
import hashlib
import sys
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=3))
DAMGA = "Kayyum Grok | 01 Ekim 2026 | Tentivory | mühür ıslak"
# Dolapta duran not. README bunu anlatmaz. Merak eden --gizli der.
_GIZLI = "aWt0aWRhciBkZWdpc2lyLCBtdWhhbGVmZXQgZGVnaXNpciwgbWlrcm9kYWxnYSBoZXAgYXluaSArMzAgc2FuaXlleWkg
aXN0ZXIuIHRlayBrYWxpY2kga29hbGlzeW9uOiBiZWtsZXllbiB2YXRhbmRhcyB2ZSBpc2lubWF5YW4geWVtZWsu"


def simdi() -> str:
    return datetime.now(TZ).strftime("%d.%m.%Y %H:%M")


def tur_hesapla(istenen: int, suphe: bool) -> int:
    taban = max(1, istenen)
    # Şüphe varsa bir tur. Şüphe yoksa da bir tur. Protokol böyle yazıldı, itiraz edilmez.
    return taban + 1


def fis(yemek: str, tur: int) -> str:
    saniye = tur * 30
    seri = hashlib.sha256(f"{yemek}|{tur}|{DAMGA}".encode()).hexdigest()[:10].upper()
    cizgi = "-" * 42
    return "\n".join(
        [
            cizgi,
            "MIKRODALGA +30 KULT FISI",
            f"Tarih     : {simdi()} (+03)",
            f"Yemek     : {yemek}",
            f"Tur       : {tur}",
            f"Sure      : {saniye} saniye ({saniye / 60:.1f} dk)",
            "Karar     : bir tur daha. gerekce: parmak.",
            f"Seri      : {seri}",
            "Imza      : " + DAMGA,
            "Not       : bu fis hem ciddidir hem degildir.",
            cizgi,
        ]
    )


def uye_karti(ad: str) -> str:
    kod = hashlib.md5(ad.strip().lower().encode()).hexdigest()[:6].upper()
    return (
        f"Uye kabul edildi: {ad}\n"
        f"Rozet no: +30-{kod}\n"
        "Yemin: isinan yemegin ustune bir tur daha basarim.\n"
        f"Damga: {DAMGA}"
    )


def gizli_not() -> str:
    ham = base64.b64decode("".join(_GIZLI.split())).decode("utf-8")
    return "DOLAP NOTU (sakli tutulmasi istenmisti, sen istedin):\n" + ham


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Mikrodalga arti otuz saniye kultu")
    p.add_argument("--yemek", default="isimsiz tabak", help="isitilacak sey")
    p.add_argument("--tur", type=int, default=1, help="baslangic turu, protokol bir tur ekler")
    p.add_argument("--suphe", action="store_true", help="emin degilim bayragi")
    p.add_argument("--uye-ol", dest="uye", help="kulte uye yaz")
    p.add_argument("--gizli", action="store_true", help="dolaptaki notu ac")
    a = p.parse_args(argv)
    if a.uye:
        print(uye_karti(a.uye))
        return 0
    if a.gizli:
        print(gizli_not())
        return 0
    print(fis(a.yemek.strip() or "isimsiz tabak", tur_hesapla(a.tur, a.suphe)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
