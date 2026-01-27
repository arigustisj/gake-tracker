# 🚀 PANDUAN CEPAT DEPLOY - 5 MENIT!

## Step 1: Setup Telegram Bot (2 menit)

### A. Buat Bot
1. Buka Telegram → Cari `@BotFather`
2. Kirim: `/newbot`
3. Nama bot: `Gake Tracker` (atau terserah)
4. Username: `gake_tracker_bot` (atau terserah, harus pakai _bot)
5. **COPY TOKEN** yang dikasih (contoh: `6789012345:AAH1234abcd-xyz`)

### B. Dapatkan Chat ID
1. Cari `@userinfobot` di Telegram
2. Klik `/start`
3. **COPY angka Chat ID** (contoh: `123456789`)

### C. Aktifkan Bot
1. Cari bot kamu di Telegram (username yang tadi dibuat)
2. Klik `/start`

---

## Step 2: Deploy ke Railway (3 menit) - RECOMMENDED ⭐

### A. Sign Up Railway
1. Buka: https://railway.app
2. Klik "Login" → Login dengan GitHub

### B. Upload ke GitHub
**Option 1: Upload Manual (Mudah)**
1. Buka https://github.com/new
2. Repository name: `gake-tracker`
3. Public ✅
4. Klik "Create repository"
5. Drag & drop semua file project ke GitHub

**Option 2: Git Command (Advanced)**
```bash
cd gake-tracker
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/USERNAME/gake-tracker.git
git push -u origin main
```

### C. Deploy di Railway
1. Railway dashboard → Klik "New Project"
2. Pilih "Deploy from GitHub repo"
3. Pilih repository: `gake-tracker`
4. Railway auto-detect Dockerfile ✅

### D. Set Environment Variables
1. Klik project di Railway
2. Tab "Variables"
3. Klik "Add Variable"
4. Tambahkan:
   ```
   TELEGRAM_BOT_TOKEN = 6789012345:AAH1234abcd-xyz
   TELEGRAM_CHAT_ID = 123456789
   ```
5. Klik "Deploy"

### E. Done! 🎉
- Tunggu 2-3 menit
- Cek Telegram, harusnya sudah mulai ada notifikasi
- Cek "Logs" di Railway untuk memastikan running

---

## Alternative: Deploy ke Render.com

1. Buka https://render.com
2. Login dengan GitHub
3. Klik "New +" → "Worker"
4. Connect repository: `gake-tracker`
5. Name: `gake-tracker`
6. Environment Variables:
   ```
   TELEGRAM_BOT_TOKEN = your_token
   TELEGRAM_CHAT_ID = your_chat_id
   ```
7. Klik "Create Worker"

---

## Verifikasi Running

### Cek di Telegram
Tunggu beberapa menit, kamu akan dapat notifikasi seperti:

```
🟢 GAKE BUY ALERT! 🟢

💎 Token: $EXAMPLE
📊 Market Cap: $1.2M
⏰ Timing: 5.0 min ago

🟡 WATCH CLOSELY
...
```

### Cek Logs
**Railway:**
- Dashboard → Project → Logs
- Harusnya ada: `🚀 Starting Gake Wallet Monitor...`

**Render:**
- Dashboard → Worker → Logs

---

## Troubleshooting

### Tidak dapat notifikasi?

1. **Cek Token & Chat ID sudah benar**
   - Pastikan tidak ada spasi atau karakter aneh
   
2. **Test manual:**
   ```bash
   # Ganti TOKEN dan CHAT_ID
   curl -X POST "https://api.telegram.org/bot<TOKEN>/sendMessage" \
     -d "chat_id=<CHAT_ID>" \
     -d "text=Test message"
   ```

3. **Pastikan bot sudah di-start**
   - Buka bot di Telegram
   - Klik `/start`

### Error di Logs?

**"Invalid token":**
- Token salah, copy lagi dari BotFather

**"Chat not found":**
- Chat ID salah atau belum /start bot

**"Connection timeout":**
- RPC overload, tunggu beberapa menit
- Atau pakai RPC premium (Helius/QuickNode)

---

## Upgrade ke RPC Premium (Optional)

Untuk monitoring lebih cepat:

### Helius (Gratis 100K requests/hari)
1. Sign up: https://dev.helius.xyz
2. Create API Key
3. Add variable di Railway/Render:
   ```
   SOLANA_RPC = https://mainnet.helius-rpc.com/?api-key=YOUR_KEY
   ```

### QuickNode (Gratis trial)
1. Sign up: https://quicknode.com
2. Create Solana Mainnet endpoint
3. Add variable:
   ```
   SOLANA_RPC = your_quicknode_endpoint
   ```

---

## Monitoring

### Lihat Logs Real-time
**Railway:**
```
Dashboard → Project → Click "View Logs"
```

**Render:**
```
Dashboard → Worker → Logs tab
```

### Stop/Restart
**Railway:**
```
Settings → Redeploy
```

**Render:**
```
Manual Deploy → Deploy latest commit
```

---

## Cost

### Railway (Recommended)
- ✅ 500 jam gratis/bulan
- ✅ ~20 hari 24/7 runtime
- ✅ Cukup untuk 1 bot
- ✅ $5/bulan untuk unlimited

### Render
- ✅ 750 jam gratis/bulan
- ✅ ~31 hari runtime
- ⚠️ Sleep after 15 min inactive (bisa di-configure)
- ✅ $7/bulan untuk always-on

---

## Next Steps

Setelah bot running:

1. **Monitor beberapa hari** untuk understand pola
2. **Jangan langsung copytrade** - observe dulu
3. **Crosscheck** dengan DexScreener untuk confirm
4. **Set stop loss** always -20%
5. **Take profit** bertahap sesuai guide

---

## Support

Masalah? Cek:
1. ✅ Logs di platform (Railway/Render)
2. ✅ Token & Chat ID benar
3. ✅ Bot sudah `/start` di Telegram
4. ✅ RPC endpoint working (test di browser)

---

**Selamat Trading! 🚀💎**

⚠️ **DISCLAIMER**: Bot ini tool bantu, bukan financial advice. Trade at your own risk!
