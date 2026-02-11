# 📂 AI File Organizer

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![Gemini](https://img.shields.io/badge/AI-Google%20Gemini-orange?style=for-the-badge&logo=google)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

**Automated digital decluttering powered by GenAI.**

> *"Stop manually sorting your Downloads folder. Let AI read, understand, and organize your files for you."*

---

## 📖 Overview

**AI File Organizer** is a smart automation tool that scans a directory, reads the content of your files (PDFs, DOCX, TXT, MD), and uses **Google's Gemini AI** to semantically categorize them.

Unlike traditional scripts that sort by file extension (e.g., putting all `.pdf` files in one folder), this tool **reads the actual content** to distinguish between a "Bank Statement" and a "Resume," moving them into appropriate folders like `Finance/Statements` or `Career/CVs`.

## ✨ Key Features

-   **🧠 Semantic Analysis:** Uses Gemini 2.0 Flash to understand file context, not just extensions.
-   **🛡️ Dry Run Mode:** Previews every change before it happens. **Zero risk** of accidental data loss.
-   **📄 Multi-Format Support:** Natively reads `.txt`, `.pdf`, `.docx`, and `.md` files.
-   **🔒 Privacy Focused:** Only sends small text snippets to the API, never the full file.
-   **⚡ Smart Skipping:** Automatically ignores system folders (`node_modules`, `.git`, `venv`) to speed up processing.

---

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Ruddrayadav/aegis-sort.git
cd aegis-sort
```

### 2. Create a Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Google Gemini API Key
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Create a `.env` file in the project root:
```bash
GEMINI_API_KEY=your_api_key_here
```

---

## 💡 Usage

### Basic Usage
```bash
python main.py --path /path/to/directory
```

### With Dry Run (Preview Mode)
```bash
python main.py --path /path/to/directory --dry-run
```

### Custom Output Directory
```bash
python main.py --path /path/to/directory --output /path/to/organize/into
```

### Example
```bash
python main.py --path ~/Downloads --dry-run
# Preview all changes before confirming
```

---

## 📋 Configuration

Edit `config.py` to customize:
- **Supported file types**
- **Category definitions**
- **Ignored folders**
- **API parameters**

```python
SUPPORTED_FORMATS = ['.pdf', '.docx', '.txt', '.md']
IGNORED_FOLDERS = ['node_modules', '.git', 'venv', '__pycache__']
GEMINI_MODEL = "gemini-2.0-flash"
```

---

## 🔒 Privacy & Security

- **No full files sent to API:** Only the first 2000 characters are sent for analysis
- **No data logging:** Files are processed locally and not stored
- **Reversible operations:** Dry run mode lets you review all changes first
- **API key safety:** Use `.env` files, never commit your API key

---

## 🐛 Troubleshooting

### Issue: "API key not found"
**Solution:** Ensure `.env` file exists with `GEMINI_API_KEY=your_key`

### Issue: "Unsupported file format"
**Solution:** Add the file format to `SUPPORTED_FORMATS` in `config.py`

### Issue: "Permission denied"
**Solution:** Ensure you have read/write permissions for the target directory

---

## 📊 How It Works

1. **Scan:** Directory is scanned for supported file types
2. **Extract:** Text is extracted from files (first 2000 characters)
3. **Analyze:** Gemini AI analyzes content and suggests categories
4. **Organize:** Files are moved to appropriate category folders
5. **Report:** Summary of changes is displayed

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙋 Support

For issues, questions, or suggestions:
- Open an [Issue](https://github.com/Ruddrayadav/aegis-sort/issues)
- Check existing discussions
- Contact the maintainer

---

## ⭐ Show Your Support

If this project helped you, please give it a star! ⭐