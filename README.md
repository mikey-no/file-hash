# File Hash

- A simple sha-1 file hashing programme
- Written in python
- With a number of tests to confirm it works - makes use of Markus Kuhn's work
  <http://www.cl.cam.ac.uk/~mgk25/> - 2015-08-28 - CC BY 4.0
- Skips big files that would take a long time to hash (see Config setting)
- Creates log file of programme activities (v0.0.2)
- See ConfigOne for alternate configuration
- Has simplified parse command line argument parser (check which is being used)
- Only use minimal external python dependencies
- (v0.0.3 on 28 Feb deployed and work in prod environment)

## File Hash v0.0.4

- added case label
- added created, modified file time info to the output csv
- removed the full argparser, only using the simple parser
- added the file name and extension as additional separate fields
- added duplicate sha-1 hash field sha-1-uc to provide the same hash with uppercase hex values


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

- [ ] tkinter user interface (ui branch) **<- customer suggested this is the next priority on the backlog**
- [ ] write each hash to the csv report after each is calculated
- [x] set up logging rather that print (logging branch)
- [ ] add tests to check the log messages
- [ ] deal with none utf-8 file names and paths
- [ ] write out to calling programme native database format
- [x] provide further file information ("created","modified","file-name","file-extension"
), details to be confirmed
- [ ] reduce the number of external dependencies in test, particularly in test_main

# Further reading

Found [RealPython argparse - sha1](https://realpython.com/python-command-line-arguments/#two-utilities-from-the-unix-world).
Techniques in this tutorial may help with "write each hash to the csv report after each is calculated"