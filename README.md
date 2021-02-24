# File Hash

- A simple sha-1 file hashing programme
- Written in python
- With a number of tests to confirm its correct function
- Skips big files that would take a long time to hash (see Config setting)
- Creates log file of programme activities (v0.0.2)

# Setup on windows

```commandline
md file-hash
cd file-hash
python -m venv venv
venv\scripts\activate.bat
pip install -f requirements.txt rem (check)
```

# Run 

## From the command line - windows

```commandline
python app\main.py <file path to sha-1> --report <result.csv>
```

# Test

```commandline
pytest ./test/test_main.py
```

# Further work

- [ ] may need to pass string arguments to the main function
- [ ] write each hash to the csv report after each is calculated
- [x] set up logging rather that print (logging branch)
- [ ] tkinter user interface (ui branch)
- [ ] add tests to check the log messages