# 📄 Telegram Document Converter Bot

A simple and interactive Telegram bot that converts uploaded documents into various formats using the Cloudmersive API.

## 🚀 Features

- Convert documents like DOC, DOCX, PDF, XLSX, PPTX, etc.
- Supports multiple output formats (PDF, DOCX, TXT, HTML, etc.)
- Uses inline buttons for selecting the target format
- Only accepts files when user is prompted via `/start` or `/convert`
- Cleans up files after conversion to avoid storage bloat

## 🧰 Built With

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) (v20+)
- [Cloudmersive Convert API](https://www.cloudmersive.com/convert-api)
- [python-dotenv](https://github.com/theskumar/python-dotenv)

## 💡 Supported Conversions

- **DOC ➜** PDF, DOCX, TXT
- **DOCX ➜** PDF, DOC, TXT, HTML
- **ODT ➜** PDF, DOCX
- **XLS, XLSX ➜** PDF, CSV, XLS, TXT, HTML
- **PPT, PPTX ➜** PDF, PPT, PPTX, TXT
- **PDF ➜** DOCX, PPTX, TXT
- **KEY ➜** PDF, PPTX
- **ODS ➜** PDF, XLSX
- **ODP ➜** PDF, PPTX

📦 *Max file size:* 10 MB  
🔒 *Files are deleted after conversion for privacy and storage reasons.*

## 📦 Setup Instructions

### 1. Clone the repository

```bash
git clone  https://github.com/zhudiana/Document-Converting-Telegram-Bot.git
cd DocumentConverterBot
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file

```env
TOKEN=your_telegram_bot_token
CLOUDMERSIVE_API_KEY=your_cloudmersive_api_key
```

### 5. Run the bot

```bash
python main.py
```

> 📝 If you plan to deploy this, check out free options like Railway, Replit, or a VPS.

## 📁 Project Structure

```
.
├── main.py               # Bot logic and handlers
├── convert_api.py        # Cloudmersive API integration
├── requirements.txt
└── .env                  # Environment variables (not tracked)
```

## 👤 Author

**Yodit** – [GitHub Profile](https://github.com/zhudiana)

---

Feel free to use, share, and modify this bot for your own projects.
