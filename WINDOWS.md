# Windows Setup Guide

Step-by-step instructions to get your Python environment running on Windows.

---

## Step 1 — Install Python via pyenv-win

We use `pyenv-win` to manage Python versions cleanly.

Open **PowerShell as Administrator** and run:

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
winget install pyenv-win
```

> If `winget` is not available, use `scoop` instead:
> ```powershell
> irm get.scoop.sh | iex
> scoop install pyenv
> ```

**Restart your terminal**, then verify:

```powershell
pyenv --version
```

---

## Step 2 — Install Python 3.11

```powershell
pyenv install 3.11.9
pyenv global 3.11.9
```

Verify:

```powershell
python --version
```

You should see `Python 3.11.9`.

---

## Step 3 — Clone or open the project

Navigate to your project folder in PowerShell:

```powershell
cd C:\Users\YourName\Projects\savnet-python-ai
```

---

## Step 4 — Create a virtual environment

```powershell
python -m venv .venv
```

This creates a `.venv` folder inside the project — your isolated Python environment.

---

## Step 5 — Activate the virtual environment

**In PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

**In Command Prompt (cmd):**

```cmd
.venv\Scripts\activate.bat
```

Your prompt should now show `(.venv)` at the start — that means it's active.

> ⚠️ **PowerShell permissions error?** Run this once, then try again:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

---

## Step 6 — Install project dependencies

With the venv active:

```powershell
pip install -r requirements.txt
```

This installs everything the project needs: pandas, streamlit, duckdb, plotly, and more.

---

## Step 7 — Verify the setup

```powershell
python -c "import pandas, streamlit, duckdb; print('All good!')"
```

You should see: `All good!`

---

## Daily workflow

Every time you open a new terminal to work on this project:

```powershell
cd C:\Users\YourName\Projects\savnet-python-ai
.venv\Scripts\Activate.ps1
```

To deactivate when you're done:

```powershell
deactivate
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `python` not found | Restart terminal after pyenv install |
| PowerShell script blocked | Run `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| `pip install` fails on a package | Make sure the venv is active (check for `(.venv)` in prompt) |
| Wrong Python version | Run `pyenv global 3.11.9` and restart terminal |
