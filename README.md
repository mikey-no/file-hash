# File Hash

- A simple sha-1 file hashing programme
- Written in python
- With a number of tests to confirm it works
- Skips big files that would take a long time to hash (see Config setting)
- Creates log file of programme activities (v0.0.2)
- See ConfigOne for alternate configuration
- Has simplified parse command line argument parser (check which is being used)
- Only using minimal external python dependencies

# Setup on windows 

```commandline
md file-hash
cd file-hash
python -m venv venv
venv\scripts\activate.bat
pip install -r requirements.txt
```

# Run 

## From the command line - windows

```commandline
python app\file_hash.py [result.csv] <file path to sha-1>
```

## From windows with the full parse
See:
```commandline
python app\file_hash.py --help
```

# Test

```commandline
pytest ./test/file_hash.py
```

# Further work

- [ ] write each hash to the csv report after each is calculated
- [x] set up logging rather that print (logging branch)
- [ ] tkinter user interface (ui branch)
- [ ] add tests to check the log messages
- [ ] deal with none utf-8 file names and paths
- [ ] write out to calling programme native database format

# Further reading

Found [RealPython argparse - sha1](https://realpython.com/python-command-line-arguments/#two-utilities-from-the-unix-world).
Techniques in this tutorial may help with "write each hash to the csv report after each is calculated"