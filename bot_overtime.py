import csv
from datetime import datetime, time
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Jadwal kerja normal
jadwal_kerja = {
    'sunday': (time(5,0), time(14,0)),
    'monday': (time(5,0), time(14,0)),
    'tuesday': None,  # Libur
    'wednesday': (time(5,0), time(14,0)),
    'thursday': (time(5,0), time(14,0)),
    'friday': (time(6,0), time(14,30)),
    'saturday': (time(6,0), time(14,30)),
}

DATA_FILE = 'overtime_data.csv'

def hitung_overtime(jam_pulang_input, jam_mulai, jam_pulang_normal):
    fmt = '%H:%M'
    pulang_input = datetime.strptime(jam_pulang_input, fmt).time()
    start_dt = datetime.combine(datetime.today(), jam_mulai)
    end_dt = datetime.combine(datetime.today(), pulang_input)
    durasi_kerja = (end_dt - start_dt).total_seconds() / 3600
    normal_start_dt = datetime.combine(datetime.today(), jam_mulai)
    normal_end_dt = datetime.combine(datetime.today(), jam_pulang_normal)
    durasi_normal = (normal_end_dt - normal_start_dt).total_seconds() / 3600
    overtime = max(0, durasi_kerja - durasi_normal)
    return round(overtime, 2)

def simpan_data(tanggal, overtime):
    try:
        with open(DATA_FILE, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([tanggal, overtime])
    except Exception as e:
        print("Error simpan data:", e)

def baca_data():
    data = []
    try:
        with open(DATA_FILE, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        pass
    return data

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Halo! Kirim jam pulang kamu hari ini dengan format:
"
        "`pulang HH:MM`
"
        "Aku akan hitung overtime dan simpan datanya.

"
        "Kamu juga bisa lihat rekap dengan perintah /rekap"
    )

def hitung(update: Update, context: CallbackContext):
    text = update.message.text.lower()
    if text.startswith("pulang"):
        try:
            jam_pulang_input = text.split()[1]
        except IndexError:
            update.message.reply_text("Format salah. Kirim: pulang HH:MM")
            return

        hari_ini = datetime.today().strftime('%A').lower()

        if hari_ini not in jadwal_kerja or jadwal_kerja[hari_ini] is None:
            update.message.reply_text(f"Hari ini ({hari_ini.title()}) kamu libur, tidak ada overtime.")
            return

        jam_mulai, jam_pulang_normal = jadwal_kerja[hari_ini]
        overtime = hitung_overtime(jam_pulang_input, jam_mulai, jam_pulang_normal)
        tanggal = datetime.today().strftime('%Y-%m-%d')
        simpan_data(tanggal, overtime)
        update.message.reply_text(f"Overtime kamu hari ini adalah {overtime} jam. Data sudah disimpan.")
    else:
        update.message.reply_text("Format salah. Kirim jam pulang dengan format: pulang HH:MM")

def rekap(update: Update, context: CallbackContext):
    data = baca_data()
    if not data:
        update.message.reply_text("Belum ada data overtime yang tersimpan.")
        return
    pesan = "Rekap overtime kamu:
"
    total_overtime = 0
    for tanggal, overtime in data:
        pesan += f"{tanggal}: {overtime} jam
"
        total_overtime += float(overtime)
    pesan += f"
Total overtime: {round(total_overtime,2)} jam"
    update.message.reply_text(pesan)

def main():
    import os
    TOKEN = os.getenv('YOUR_TELEGRAM_BOT_TOKEN')
    if not TOKEN:
        print("Error: Environment variable YOUR_TELEGRAM_BOT_TOKEN tidak ditemukan!")
        return

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("rekap", rekap))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, hitung))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
