# Security Policy

Thank you for helping keep **45-Days-Python-Development-Challenge** safe for learners and contributors. This repository contains learning materials, Python scripts, and small projects; security issues usually involve **malicious code**, **dependency risks**, or **leaked secrets**.

---

## Reporting a Vulnerability

Please follow responsible disclosure. Do **not** open a public GitHub issue for security reports.

### Preferred (GitHub)

- Use **GitHub Security Advisories** (private reporting): go to the repo → **Security** → **Report a vulnerability**

### Alternative (Email)

- Email the maintainer privately at `abhisek2004panda@gmail.com`

### Include in your report

- What you found and why it’s a security risk
- Exact file path(s) / folder(s) affected
- Steps to reproduce (safe PoC if possible)
- Suggested fix or mitigation (optional)
- Whether any secrets/credentials were exposed

### Response expectations

- Initial response: typically **within 48–72 hours**
- Fix timeline depends on severity and complexity (critical issues prioritized)

---

## Supported Versions

| Version / Branch | Status | Notes |
| --- | --- | --- |
| `main` | Supported | Security fixes are applied here |
| Feature branches / forks | Not supported | Please reproduce against `main` |

If you are using a fork, keep it synced with `main` to receive security updates.

---

## Scope (What we consider a security issue)

### In scope

- **Accidental secrets** committed to the repo (API keys, tokens, credentials)
- **Malicious code** (backdoors, credential stealers, obfuscated payloads)
- **Unsafe patterns** in runnable examples (e.g., `eval` on untrusted input, insecure deserialization) when presented as recommended practice
- **Supply-chain issues** in project dependencies (if this repo introduces them)
- **GitHub Actions / CI** workflow vulnerabilities (if present)

### Out of scope (usually)

- General code style or correctness issues without security impact
- Vulnerabilities in third-party services not controlled by this repo
- Issues in forks or downstream copies not maintained here

---

## Handling Secrets

- Never commit real secrets to the repository.
- If you discover a secret in the repo history, report it **privately** (advisory/email) and avoid spreading it further (screenshots, logs, re-posting the value).
- Maintainers may rotate/revoke secrets and rewrite history if needed.

---

## Coordinated Disclosure

If you report a valid vulnerability, we may:

1. Confirm and triage severity
2. Prepare a fix on `main`
3. Publish an advisory / release note (when appropriate)
4. Credit the reporter (optional, only with permission)

---

## Maintainer Contact

- Email: `abhisek2004panda@gmail.com`
- Repository: `https://github.com/abhisek2004/45-Days-Python-Development-Challenge`
