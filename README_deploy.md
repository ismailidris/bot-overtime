# Bot Telegram Overtime

Ini adalah bot Telegram untuk menghitung overtime kerja harian kamu.

## Fitur:
- Input jam pulang dengan format `pulang HH:MM` (misal: pulang 15:30)
- Hitung otomatis overtime berdasarkan jadwal kerja kamu
- Simpan data overtime ke file CSV
- Melihat rekap overtime dengan perintah `/rekap`

## Cara deploy di Railway

1. **Buat repository baru di GitHub**  
   Upload file `bot_overtime.py` ke repository tersebut.

2. **Login ke https://railway.app**  
   Buat project baru, pilih **Deploy from GitHub repo**  
   Pilih repository yang sudah kamu buat tadi.

3. **Set environment variable**  
   Di project Railway, buka tab **Settings** -> **Variables**  
   Tambahkan variable:  
   - Key: `YOUR_TELEGRAM_BOT_TOKEN`  
   - Value: (isi dengan token bot Telegram kamu dari @BotFather)

4. **Deploy dan jalankan project**  
   Railway akan otomatis deploy bot kamu.  
   Jika berhasil, bot akan aktif dan siap dipakai.

5. **Cara pakai bot di Telegram**  
   - Kirim `/start` untuk mulai  
   - Kirim `pulang HH:MM` untuk input jam pulang hari ini  
   - Kirim `/rekap` untuk melihat rekap overtime

---

Kalau kamu butuh bantuan, tinggal chat aku lagi ya!
