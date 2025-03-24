# Freelance Parser

An automated tool that scrapes and aggregates job listings from multiple freelance platforms:
- **Kwork**  
- **Freelancehunt**  
- **FL.ru**  

---

## 🚀 Features  
✅ Real-time job monitoring  
✅ Keyword-based filtering  
✅ Excel output with formatting  
✅ Automatic backups  
✅ Error handling and logging  
✅ Proxy support  
✅ Captcha handling  

---

## 🛠️ Setup  

### 1️⃣ Create a Virtual Environment  
```bash
python -m venv venv
venv\Scripts\activate
```

### 2️⃣ Install Dependencies  
```bash
pip install -r requirements.txt
```

### 3️⃣ Create a `.env` File with Credentials  
```env
FLRU_LOGIN=your_login
FLRU_PASSWORD=your_password
```

---

## ▶️ Usage  

Run the parser with:  
```bash
python src\main.py
```

🔹 The parser will:  
- Check job listings **every 5 minutes**  
- Save results to `data/freelance_jobs.xlsx`  
- Create backups in `data/backups/`  
- Log activities in `parser.log`  

---

## 📊 Excel Output Format  

Each entry includes:  
- **Title**  
- **Description**  
- **Price**  
- **Client**  
- **URL**  
- **Date**  
- **Platform**  

🔹 **Excel Features:**  
✅ Sortable columns  
✅ Filters  
✅ Highlighted new entries  
✅ Formatted prices and dates  
✅ Auto-adjusted column widths  

---

## ⚙️ Customization  

Edit **`src/config.py`** to:  
- Modify **search keywords**  
- Adjust **parsing interval**  
- Change **file paths**  
- Configure **backup settings**  

---

## 📝 Logs  

Check **`parser.log`** for:  
- ✅ New jobs found  
- ❌ Errors  
- 📡 Platform status  
- 📊 Total job counts  

---

### 🎯 Happy parsing! 🚀  