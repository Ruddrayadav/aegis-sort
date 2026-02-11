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

---

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
git clone [https://github.com/Ruddrayadav/ai-file-organizer.git](https://github.com/Ruddrayadav/ai-file-organizer.git)
cd ai-file-organizer