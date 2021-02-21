# File Hash

- A simple sha-1 file hashing programme
- Written in python
- With a number of tests to confirm its correct function
- Skips big files that would take a long time to hash

# Setup (on windows)

```commandline
md file-hash
cd file-hash
python -m venv venv
venv\scripts\activate.bat
pip install -f requirements.txt rem (check)
```

# Run 

## from the command line - windows

```commandline
python app\main.py <file path to sha-1> <result.csv>
```