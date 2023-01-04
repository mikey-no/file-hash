# File Hash

1) Written in python (python version 3.10)
2) With a number of tests to confirm its correct function 
3) Skips big files that would take a long time to hash (see max_hash_size_default or argument --max-file-size)
4) Creates log file of programme activities (since v0.0.2) - one line of code would need to be uncommented

## 20 Oct 2022 1.1.2  

6) Added relative-path to the default output and replaced the simple output file path with relative
path

7) Default run uses multiprocessing on the computer where it's been run taking cpu-count - 1
processes to compute the hash and gather the other file meta-data

- threading was found to be slower and this is best for input output bound tasks this is 
  processor bound (see example code below)
                        
8) Is able to look as the scan_location and only scan the first n files for a hash, which is useful
for testing

9) Almost a complete re-write from earlier versions of this programme


# Setup on Windows

```commandline
md file-hash
cd file-hash
python -m venv venv
venv\scripts\activate.bat
```

# Run 

## From the command line - windows

### Default

```commandline
python app\hash_file --case_label case1 --location ..\..\test-files\001 --report hash_report1.csv
```
Example csv output:
```csv
"case-label","path","sha-1","sha-1-uc","hash-error","size","created","created-time","modified","modified-time","file-name","file-extension"
"case1","C:\Users\n\Documents\vss\python-experiments\test-files\001\cam.ac~mgk25\revelation.txt","0bd3fbc36a4a7098b60267b1e1ac3e66212fa062","0BD3FBC36A4A7098B60267B1E1AC3E66212FA062","","116240","2022-Apr-18","19:41:33","2020-Oct-14","11:28:47","revelation.txt",".txt"
"case1","C:\Users\n\Documents\vss\python-experiments\test-files\001\cam.ac~mgk25\grid-mixed-2.txt","b4bcef4cc28b34163dd98a49c396a2cf62df467c","B4BCEF4CC28B34163DD98A49C396A2CF62DF467C","","5647","2022-Apr-18","19:41:33","2020-Oct-14","11:25:39","grid-mixed-2.txt",".txt"
```
### Simple output format

```commandline
python app\hash_file --case_label case1 --location ..\..\test-files\001 --report hash_report1.csv --simple
```
Example csv output:
```csv
"case-label","relative-path","sha1","hash-error","size","created","modified","file-name","file-extension"
"case1","cam.ac~mgk25\revelation.txt","0bd3fbc36a4a7098b60267b1e1ac3e66212fa062","","116240","2022-Apr-18 19:41:33","2020-Oct-14 11:28:47","revelation.txt",".txt"
"case1","cam.ac~mgk25\grid-mixed-2.txt","b4bcef4cc28b34163dd98a49c396a2cf62df467c","","5647","2022-Apr-18 19:41:33","2020-Oct-14 11:25:39","grid-mixed-2.txt",".txt"
```

# Test

```commandline
pytest ./test/test_hash_file.py
```
- _works from pycharm_ 
- depends on test files are per the development system

# Further work

- [x] write each hash to the csv report after each is calculated
- [x] set up logging rather that print (logging branch)

# Handy references

- parallel processing!!
https://testdriven.io/blog/python-concurrency-parallelism/#cpu-bound-operation

- benchmark
https://stackoverflow.com/questions/739654/how-to-make-function-decorators-and-chain-them-together?rq=1


## Old example of using multithreading processing

```python
thread_workers = 4  # unused, cpu bound task so needs multiprocessor not multithreaded processing

# was working on an earlier version of the programmer but now unused
@benchmark
def run_hash_multithreaded(file_list: List[pathlib.Path],
                           case_label: str = case_label_default,
                           thread_workers=2) -> List[concurrent.futures.Future] | None:
    futures = []
    log.info(f'Processing with multi threaded executor with maximum {thread_workers} thread workers')
    with ThreadPoolExecutor(max_workers=thread_workers) as executor:
        for file in file_list:
            futures.append(executor.submit(get_file_and_hash_data, file, case_label))

    return futures
```

## Example of generic code to do alternative hash functions like md5

This worked for while then stopped work and was abandoned.

```python
def get_hash(file: pathlib.Path) -> str:
    """
    From a pathlib file get the hash in chunks
    hash_function = hashlib.sha1() - default
    return hash as a string
    """
    try:
        with open(file, mode="rb") as f:
            for buffer in iter(partial(f.read, hash_function.block_size), b""):
                hash_function.update(buffer)
        return hash_function.hexdigest()
    except FileNotFoundError as fnfe:
        raise Exception("FileNotFoundError {0}: On file: {1}".format(fnfe, file))
    except Exception as e:
        raise Exception("Exception: {0}: On file: {1}".format(e, file))
```