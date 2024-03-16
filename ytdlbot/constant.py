#!/usr/local/bin/python3
# coding: utf-8

# ytdlbot - constant.py
# 8/16/21 16:59
#

__author__ = "Benny <benny.think@gmail.com>"

import os

from config import (
    AFD_LINK,
    COFFEE_LINK,
    ENABLE_CELERY,
    FREE_DOWNLOAD,
    REQUIRED_MEMBERSHIP,
    TOKEN_PRICE,
)
from database import InfluxDB
from utils import get_func_queue


class BotText:
    start = """
    ✘ ʜᴀʟʟᴏ sᴇʟᴀᴍᴀᴛ ᴅᴀᴛᴀɴɢ ᴅɪ ᴋᴏʙᴏ ʏᴛ ᴅᴏᴡɴʟᴏᴀᴅᴇʀ ᴋᴇᴛɪᴋ /help ᴜɴᴛᴜᴋ ᴍᴇʟɪʜᴀᴛ ʙᴀɴᴛᴜᴀɴ ᴛᴇʀɪᴍᴀᴋᴀsɪʜ ✘"""

    help = f"""
ɢᴜɴᴀᴋᴀɴ ᴄᴏᴍᴍᴀɴᴅ ᴅɪ ʙᴀᴡᴀʜ ɪɴɪ

/ytdl - Unduh video dalam grup 
/settings - Tetapkan preferensi Anda
/Buy - Beli token 
/direct - Unduh file secara langsung 
/sub - Berlangganan Saluran YouTube 
/unsub - Berhenti berlangganan dari Saluran YouTube 
/sub_count - Periksa status berlangganan, hanya pemilik.
/uncache - Hapus cache untuk tautan ini, hanya pemilik. 
/purge - Hapus semua tugas, hanya pemilik.
    """

    about = "ᴏᴡɴᴇʀ : @skytrixsz
ɢʀᴜᴘ : @wibuhouse
ᴄʜᴀɴɴᴇʟ : @skyskykyy
sᴛᴏʀᴇ : @skynokos"

    buy = f"""
**Humm:**
tanya owner deh : @skytrixsz`
    """

    private = "Bot ini untuk penggunaan pribadi"

    membership_require = f"You need to join this group or channel to use this bot\n\nhttps://t.me/{REQUIRED_MEMBERSHIP}"

    settings = """
Silakan pilih format dan kualitas video yang diinginkan untuk video Anda. Setelan ini hanya **berlaku untuk video YouTube**.

Kualitas tinggi direkomendasikan. Kualitas sedang bertujuan untuk 720P, sedangkan kualitas rendah adalah 48
"""
    custom_text = os.getenv("CUSTOM_TEXT", "")

    premium_warning = """
    File Anda terlalu besar, apakah Anda ingin saya mencoba mengirimkannya sebagai pengguna premium?
    Ini adalah fitur eksperimental sehingga Anda hanya dapat menggunakannya sekali sehari.
    Selain itu, pengguna premium akan mengetahui siapa Anda dan siapa Anda
    """

    @staticmethod
    def get_receive_link_text() -> str:
        reserved = get_func_queue("reserved")
        if ENABLE_CELERY and reserved:
            text = f"Tugas Anda telah ditambahkan ke antrean yang dipesan {reserved}. diproses...\n\n"
        else:
            text = "Tugas Anda telah ditambahkan ke antrean aktif.\n Pengolahan...\n\n"

        return text

    @staticmethod
    def ping_worker() -> str:
        from tasks import app as celery_app

        workers = InfluxDB().extract_dashboard_data()
        # [{'celery@BennyのMBP': 'abc'}, {'celery@BennyのMBP': 'abc'}]
        response = celery_app.control.broadcast("ping_revision", reply=True)
        revision = {}
        for item in response:
            revision.update(item)

        text = ""
        for worker in workers:
            fields = worker["fields"]
            hostname = worker["tags"]["hostname"]
            status = {True: "✅"}.get(fields["status"], "❌")
            active = fields["active"]
            load = "{},{},{}".format(fields["load1"], fields["load5"], fields["load15"])
            rev = revision.get(hostname, "")
            text += f"{status}{hostname} **{active}** {load} {rev}\n"

        return text
