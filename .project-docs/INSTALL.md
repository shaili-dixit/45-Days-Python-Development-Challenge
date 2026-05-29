# 📦 INSTALL.md – Setup Guide (45 Days Python Challenge)

Welcome to **45-Days-Python-Development-Challenge** 🐍🚀  
This guide helps you **clone**, **set up Python**, and **run scripts/tests** locally on Windows/macOS/Linux.

---

## ✅ Prerequisites

Install these tools first:

- 🐍 **Python**: 3.10+ (recommended: 3.11 / 3.12)
- 🧰 **Git**: latest stable
- 🧑‍💻 **Editor**: VS Code / Cursor / PyCharm (any is fine)

Optional but helpful:

- 🧪 **pytest** (for tests)
- 📦 **pip** (comes with Python) and/or **conda** (if you prefer `environment.yml`)

---

## 🔁 Clone the Repository

```bash
git clone https://github.com/abhisek2004/45-Days-Python-Development-Challenge.git
cd 45-Days-Python-Development-Challenge
```

---

## 🧪 Set up a Virtual Environment (recommended)

### 🪟 Windows (PowerShell)

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 🐧 macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 📦 Install Dependencies (if needed)

This repo contains many scripts that use the standard library only ✅.  
If a folder or lesson requires packages, it should provide instructions or a `requirements.txt`.

If you see a `requirements.txt`, install it like this:

```bash
pip install -r requirements.txt
```

If you prefer conda and want to use `environment.yml`:

```bash
conda env create -f environment.yml
conda activate <env-name>
```

---

## ▶️ Run Python Scripts

Example:

```bash
python MAIN_CODE_PROJECT/week-1/fetch_details.py
```

📌 Tip: Some scripts expect you to run them from a specific folder (relative paths). If you hit path errors, `cd` into the script’s directory and run again.

---

## 🧪 Run Tests (if present)

If `pytest` is used:

```bash
pytest
```

If you don’t have pytest installed:

```bash
pip install pytest
pytest
```

---

## 🆘 Need Help?

- 🐛 Issues: `https://github.com/abhisek2004/45-Days-Python-Development-Challenge/issues`
- 📘 Contribution guide: `CONTRIBUTING.md`
- ❓ FAQs: `.project-docs/FAQ.md`
- 🔐 Security: `SECURITY.md`

Happy coding — **Code. Commit. Conquer.** 🔥💻
