# 🌿 Environment Setup (Python)

This repository is mostly **learning materials + Python scripts**, so many folders do **not** require environment variables. ✅  
However, some examples (API calls, Flask apps, automation) may need secrets like API keys. This guide shows the safe way to manage them. 🔐

---

## ✅ Golden Rules

- 🚫 **Never commit secrets** (`.env`, tokens, API keys) to git.
- ✅ Use a local `.env` file for development **only**.
- ✅ Prefer `.env.example` files with placeholders (safe to commit).
- ✅ Rotate/revoke any secret that was accidentally committed.

---

## 🧪 Recommended: `.env` for scripts

If a script needs keys (example: weather API), create a `.env` file in the same folder as that script/project:

```env
# Example only — do not use real secrets in documentation
API_KEY=your_api_key_here
BASE_URL=https://example.com
DEBUG=false
```

### 🐍 Loading `.env` in Python (optional)

Some folders may use `python-dotenv`. If used, install and load like this:

```bash
pip install python-dotenv
```

```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")
```

---

## 🧰 Common Environment Variables (examples)

- 🌦️ **APIs**: `API_KEY`, `WEATHER_API_KEY`, `NEWS_API_KEY`
- 🌐 **Flask**: `FLASK_APP`, `FLASK_ENV`, `FLASK_DEBUG`
- 🧪 **Testing**: `PYTHONPATH`, custom flags for test data

---

## 🧹 What should be ignored?

Make sure these are ignored (already typical in `.gitignore`):

- `.env`
- `venv/`
- `__pycache__/`
- `.pytest_cache/`

---

## 🛡️ Security Note

If you discover a leaked secret anywhere in this repo (even inside old commits), report it privately using `SECURITY.md`. 🙏
