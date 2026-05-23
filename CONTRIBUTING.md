# Contributing to 45-Days-Python-Development-Challenge 

Welcome! 🎉 We are thrilled that you want to contribute to the **45-Days-Python-Development-Challenge**. This project is a comprehensive beginner-to-advanced roadmap designed to help developers master Python through practical automation, APIs, GUIs, and Data Science/ML frameworks.

By contributing, you help make this resource better for the entire open-source community. Please take a moment to review these guidelines before getting started.

---

## 📜 Code of Conduct

By participating in this project, you agree to maintain a respectful, inclusive, and welcoming environment for everyone. Please be helpful, polite, and constructive in your comments and reviews.

---

## 🚀 Getting Started

### 1. Fork and Clone the Repository

First, fork the repository to your own GitHub account, then clone it locally:

```bash
git clone https://github.com/YOUR-USERNAME/45-Days-Python-Development-Challenge.git
cd 45-Days-Python-Development-Challenge
```

---

### 2. Set Up a Virtual Environment

To keep your global Python dependencies clean, create and activate a virtual environment:

**On Windows:**

```bash
python -m venv venv
.\venv\Scripts\activate
```

**On macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Track with Main Branch

Always keep your local main branch synced with the upstream repository:

```bash
git remote add upstream https://github.com/abhisek2004/45-Days-Python-Development-Challenge.git
git checkout main
git pull upstream main
```

---

## 🛠️ Contribution Workflow

We follow a strict **issue-first workflow** to keep track of all contributions, especially during programs like NSoC'26.

#### Step 1 — Find or Open an Issue

- Look through the [Issues Page](https://github.com/abhisek2004/45-Days-Python-Development-Challenge/issues) for existing bugs, documentation tasks, or feature requests.
- If you want to propose something new, open a new issue describing the feature or bug clearly.

> ⚠️ Do not start working on a task until a Project Maintainer formally assigns the issue to you.

#### Step 2 — Create a Feature Branch

Never make changes directly to the `main` branch. Create a descriptive branch for your task:

```bash
git checkout -b feat/your-feature-name
# OR for bug fixes
git checkout -b fix/bug-description
# OR for documentation
git checkout -b docs/short-description
```

#### Step 3 — Implement Your Changes & Commit

- Write clean, readable, and well-commented Python code.
- Follow standard Python styling conventions (PEP 8).
- Commit your changes using meaningful commit messages:

```bash
git add .
git commit -m "docs: add comprehensive CONTRIBUTING.md guidelines"
```

#### Step 4 — Push and Open a Pull Request (PR)

Push your branch to your forked repository:

```bash
git push origin your-branch-name
```

Go to the original repository on GitHub, click on **Compare & pull request**, and fill out the PR template:

- Reference the issue number you solved (e.g., `Closes #3`)
- Provide a clear description of the changes you made

---

## 🌿 Branch Naming & Commit Conventions

To maintain a clean git history, please follow these prefix guidelines:

| Type | Description | Example Branch | Example Commit |
|---|---|---|---|
| `feat` | Adding a new day/topic or feature | `feat/day-05-loops` | `feat: add day 5 practice problems` |
| `fix` | Bug fixes in code or scripts | `fix/broken-api-link` | `fix: resolve script execution error` |
| `docs` | Updates to documentation or readmes | `docs/contributing-guide` | `docs: add contributing guidelines` |
| `refactor` | Code restructuring without changing behavior | `refactor/clean-imports` | `refactor: optimize python imports` |

---

## 💡 Guidelines for Adding Daily Challenges

If you are contributing new days or modules to the Python challenge:

- 📁 Create a well-structured folder for that day (e.g., `Day-01-Introduction/`)
- 📝 Include a `README.md` explaining the concepts taught on that day
- 🐍 Provide working Python scripts (`.py` files) or Jupyter Notebooks (`.ipynb`) with clean comments
- 🔒 Ensure no sensitive data (like API keys or local configurations) is committed

---

🐍✨ **Thank you for contributing and happy coding!**
