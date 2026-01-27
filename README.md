# 🚀 Gake Wallet Tracker - Panduan Lengkap

Sistem monitoring otomatis untuk tracking wallet Gake dengan notifikasi Telegram real-time dan analisa timing optimal untuk entry/exit.

## ✨ Fitur

- ✅ **Real-time Monitoring**: Track semua transaksi Gake dalam real-time
- 📊 **Smart Analysis**: Analisa otomatis untuk BUY/SELL/REBUY dengan timing optimal
- 📱 **Telegram Notifications**: Alert langsung ke Telegram dengan rekomendasi aksi
- 🎯 **Entry/Exit Timing**: Kalkulasi timing terbaik berdasarkan pola Gake
- 💎 **Token Information**: Data market cap, price, liquidity dari DexScreener/Birdeye
- ⚠️ **Risk Assessment**: Level risiko untuk setiap trade
- 🔄 **Rebuy Detection**: Deteksi otomatis saat Gake rebuy token

## 📋 Persiapan

### 1. Buat Telegram Bot

1. Buka Telegram, cari **@BotFather**
2. Kirim command `/newbot`
3. Ikuti instruksi untuk nama bot
4. **Simpan Token** yang diberikan (contoh: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

### 2. Dapatkan Chat ID

1. Cari bot **@userinfobot** di Telegram
2. Klik `/start`
3. Bot akan mengirim Chat ID kamu (contoh: `123456789`)
4. **Simpan angka ini**

### 3. Start Bot Kamu

1. Cari bot yang kamu buat tadi di Telegram
2. Klik `/start` agar bot bisa mengirim pesan ke kamu

## 🚀 Deployment (GRATIS)

### Option A: Railway.app (Recommended) ⭐

**Kenapa Railway?**
- ✅ 500 jam gratis per bulan
- ✅ Setup super mudah
- ✅ Auto-restart jika crash
- ✅ Logs tersedia

**Langkah-langkah:**

1. **Sign Up Railway**
   - Kunjungi https://railway.app
   - Login dengan GitHub

2. **Upload Project ke GitHub**
   ```bash
   # Di komputer kamu, masuk ke folder project
   cd gake-tracker
   
   # Init git repository
   git init
   git add .
   git commit -m "Initial commit"
   
   # Buat repository baru di GitHub (github.com/new)
   # Nama: gake-tracker
   
   # Push ke GitHub
   git remote add origin https://github.com/USERNAME/gake-tracker.git
   git push -u origin main
   ```

3. **Deploy di Railway**
   - Klik "New Project" di Railway
   - Pilih "Deploy from GitHub repo"
   - Pilih repository `gake-tracker`
   - Railway akan auto-detect Dockerfile

4. **Set Environment Variables**
   - Di Railway dashboard, klik project kamu
   - Pilih tab "Variables"
   - Tambahkan:
     ```
     TELEGRAM_BOT_TOKEN=token_dari_botfather
     TELEGRAM_CHAT_ID=chat_id_kamu
     ```

5. **Deploy!**
   - Railway akan auto-deploy
   - Tunggu 2-3 menit
   - Cek logs untuk memastikan running

### Option B: Render.com

**Langkah-langkah:**

1. **Sign Up Render**
   - Kunjungi https://render.com
   - Login dengan GitHub

2. **Upload ke GitHub** (sama seperti Railway di atas)

3. **Deploy di Render**
   - Klik "New +" → "Worker"
   - Connect GitHub repository
   - Name: `gake-tracker`
   - Render akan detect `render.yaml`

4. **Set Environment Variables**
   - Scroll ke "Environment Variables"
   - Add:
     ```
     TELEGRAM_BOT_TOKEN=token_dari_botfather
     TELEGRAM_CHAT_ID=chat_id_kamu
     ```

5. **Create Worker**
   - Klik "Create Worker"
   - Tunggu deployment selesai

### Option C: Fly.io

1. **Install Fly CLI**
   ```bash
   # Windows (PowerShell)
   iwr https://fly.io/install.ps1 -useb | iex
   
   # macOS/Linux
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login & Deploy**
   ```bash
   fly auth login
   fly launch
   
   # Pilih nama app
   # Pilih region terdekat (Singapore untuk Indonesia)
   
   fly secrets set TELEGRAM_BOT_TOKEN=your_token
   fly secrets set TELEGRAM_CHAT_ID=your_chat_id
   
   fly deploy
   ```

## 🧪 Test Lokal (Optional)

Sebelum deploy, kamu bisa test dulu di komputer:

```bash
# Install dependencies
pip install -r requirements.txt

# Copy .env.example ke .env
cp .env.example .env

# Edit .env, isi token & chat ID
nano .env  # atau pakai text editor

# Run tracker
python tracker.py
```

Kamu akan mulai menerima notifikasi Telegram!

## 📱 Cara Pakai

Setelah deploy, bot akan otomatis:

1. **Monitor wallet Gake** setiap 30 detik
2. **Deteksi transaksi** BUY/SELL/REBUY
3. **Analisa token** (market cap, price, liquidity)
4. **Kirim alert ke Telegram** dengan:
   - Info token lengkap
   - Timing analysis
   - Rekomendasi entry/exit
   - Risk level
   - Link ke DexScreener & Solscan

### Contoh Notifikasi

```
🟢 GAKE BUY ALERT! 🟢

💎 Token: $AIDOG (AI Dog Meme)
🔗 Mint: 7xKXtg2C...8CvR3kj

📊 Market Data:
├ Market Cap: $850K
├ Price: $0.00085000
└ Liquidity: $125K

⏰ Timing: 2.5 min ago

🟡 WATCH CLOSELY

Analysis:
Initial pump phase. Wait for consolidation.

Recommended Action:
Enter on dip at 30-90 min mark

Risk Level: HIGH

🔍 DexScreener | Solscan

⚠️ Remember:
• DON'T blindly copy trade
• Use stop loss (-20%)
• Take profits gradually
• DYOR before entry
```

## ⚙️ Konfigurasi Advanced

### Pakai RPC Lebih Cepat (Optional)

Untuk monitoring lebih cepat dan reliable, gunakan RPC premium:

**Helius (Recommended):**
1. Sign up: https://helius.dev
2. Dapatkan API key gratis
3. Set environment variable:
   ```
   SOLANA_RPC=https://mainnet.helius-rpc.com/?api-key=YOUR_KEY
   ```

**QuickNode:**
1. Sign up: https://quicknode.com
2. Create endpoint (Solana Mainnet)
3. Set:
   ```
   SOLANA_RPC=your_quicknode_url
   ```

### Birdeye API (Optional)

Untuk data token lebih detail:

1. Sign up: https://birdeye.so
2. Dapatkan API key
3. Set:
   ```
   BIRDEYE_API_KEY=your_birdeye_key
   ```

## 🔍 Monitoring & Logs

### Railway
- Dashboard → Project → Logs
- Real-time logs tersedia

### Render
- Dashboard → Worker → Logs
- Live tail available

### Fly.io
```bash
fly logs
```

## 🛠️ Troubleshooting

### Bot tidak kirim notifikasi

1. **Cek Token & Chat ID sudah benar**
   ```bash
   # Test di terminal
   curl -X POST https://api.telegram.org/bot<TOKEN>/sendMessage \
     -d chat_id=<CHAT_ID> \
     -d text="Test message"
   ```

2. **Pastikan sudah start bot**
   - Buka bot di Telegram
   - Klik `/start`

3. **Cek logs untuk error**
   - Lihat logs di Railway/Render
   - Cari pesan error

### RPC Rate Limit

Jika terlalu banyak request:
- Upgrade ke RPC premium (Helius/QuickNode)
- Atau increase sleep time di code (ganti 30 jadi 60 detik)

### Memory Issues

Jika app crash karena memory:
- Railway: Upgrade plan (tapi free tier biasanya cukup)
- Render: Sama, tapi 512MB free tier biasanya oke

## 📊 Strategi Trading

Bot memberikan rekomendasi, tapi keputusan akhir di kamu:

### ✅ DO's:
- ✅ Tunggu timing optimal (30-120 min setelah Gake buy)
- ✅ Pakai stop loss -20%
- ✅ Take profit bertahap (25-30-40%)
- ✅ Crosscheck dengan chart & volume
- ✅ DYOR sebelum entry

### ❌ DON'Ts:
- ❌ JANGAN auto-copytrade
- ❌ JANGAN buy immediately setelah alert
- ❌ JANGAN all-in satu token
- ❌ JANGAN FOMO chase pump
- ❌ JANGAN trade tanpa stop loss

## 🔄 Update Bot

Jika ada update di GitHub:

**Railway/Render:**
- Auto-deploy saat push ke GitHub
- Atau manual redeploy di dashboard

**Fly.io:**
```bash
fly deploy
```

## 💰 Biaya

### Gratis Tier Limits:

**Railway:**
- 500 jam/bulan gratis
- ~20 hari 24/7 runtime
- Cukup untuk 1 bot

**Render:**
- 750 jam/bulan gratis
- ~31 hari full runtime
- Sleep setelah 15 min inactive (bisa di-configure)

**Fly.io:**
- 3 shared-cpu-1x VMs gratis
- 160GB egress/bulan
- Cukup buat production

### Rekomendasi:
Pakai **Railway** atau **Render** dulu. Kalau butuh lebih, baru upgrade atau combine dengan Fly.io.

## 🆘 Support

Jika ada masalah:

1. **Cek logs** untuk error message
2. **Validasi** TELEGRAM_BOT_TOKEN & TELEGRAM_CHAT_ID
3. **Test** bot dengan `/start` di Telegram
4. **Verify** RPC endpoint working

## 📝 Notes

- Bot monitor setiap **30 detik** (balance antara speed & RPC limits)
- Transaction cache: **100 transaksi terakhir**
- Token data dari **DexScreener** (fallback) atau **Birdeye** (jika API key ada)
- Support **Solana mainnet** only

## ⚖️ Disclaimer

Bot ini adalah **TOOL BANTU**, bukan financial advisor:

- ⚠️ Trading crypto sangat berisiko
- ⚠️ Bisa kehilangan semua modal
- ⚠️ DYOR (Do Your Own Research)
- ⚠️ Never invest lebih dari yang kamu bisa lose
- ⚠️ Bot bisa false positive/negative
- ⚠️ Network delays bisa terjadi

**USE AT YOUR OWN RISK!**

## 📜 License

MIT License - Free to use, modify, distribute

---

**Happy Trading! 🚀**

Made with ❤️ for Indonesian Solana memecoin traders
