# CleanSlate
A data ingestion pipeline that fetches news articles, cleans and normalizes them, and generates semantic embeddings.

## Setup

### 1. Activate Virtual Environment

**For PowerShell:**
```powershell
# Option 1: Use the custom activation script
. .\activate.ps1

# Option 2: Use the venv Python directly (no activation needed)
.\venv\Scripts\python.exe main.py

# Option 3: If you get execution policy errors, use:
.\venv\Scripts\activate.bat
# Then in the same session, use:
python main.py
```

**For Command Prompt (cmd):**
```cmd
.\venv\Scripts\activate.bat
python main.py
```

### 2. Install Dependencies (if needed)

Dependencies are already installed in the venv. If you need to reinstall:
```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```
### 3. Configure API Key

Create a `.env` file in the project root:

```bash
API_KEY=your_newsdata_io_api_key_here
```

**Important:** The `.env` file is already in `.gitignore` and will not be committed to git.

You can copy the example file:
```powershell
Copy-Item .env.example .env
```

Then edit `.env` and add your actual API key.
## Running the Pipeline

```powershell
# Using venv Python directly (recommended for PowerShell)
.\venv\Scripts\python.exe main.py

# Or if venv is activated:
python main.py
```

## Troubleshooting

### PowerShell Execution Policy Error

If you get an execution policy error when trying to activate:
- Use `.\venv\Scripts\activate.bat` instead
- Or use `.\venv\Scripts\python.exe` directly without activation
- Or run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### Module Not Found Error

Make sure you're using the venv's Python:
```powershell
# Check which Python is being used
where.exe python

# Should show venv\Scripts\python.exe first
```

### API Errors

If you get 422 errors, check:
- API key is valid in `config.py`
- API endpoint parameters are correct
- Free tier limitations (rate limits, article limits)

## Project Structure

```
MiniProjectOne/
├── api_ingestion.py          # Fetch news from API
├── raw_storage.py            # Save raw JSON
├── cleaning.py               # Clean and normalize
├── feature_extraction.py     # Extract features
├── semantic_representation.py # Generate embeddings
├── dataset_output.py         # Create final dataset
├── config.py                # Configuration
├── main.py                  # Orchestrator
├── activate.ps1             # PowerShell activation helper
└── data/                   # Data directories
    ├── raw/                # Raw JSON files
    ├── cleaned/            # Cleaned data
    └── output/             # Final datasets
```

