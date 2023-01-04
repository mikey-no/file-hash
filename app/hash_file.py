import argparse
import concurrent
import csv
import hashlib
import logging
import os
import pathlib
import sys
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from functools import partial
from multiprocessing import cpu_count
from typing import List, Generator

app_name = "hash-file-multiprocessor"
__author__ = "MY"
# run python ../update_build.py to auto increment this build number based on git revision number
__app_build_number__ = 74
__version__ = f"1.1.2-{__app_build_number__}"
description = rf"SHA-1 hash all files (with multi processing)"

history = """
20 Oct 2022 1.1.2   1) Added relative-path to the default output and replaced the simple output file path with relative
                        path

                    2) Default run uses multiprocessing on the computer where its been run taking cpu-count - 1
                        processes to compute the hash and gather the other file meta-data
                        - threading was found to be slower and this is best for input output bound tasks this is 
                        processor bound

                    3) Is able to look as the scan_location and only scan the first n files for a hash, which is useful
                        for testing

                    4) Almost a complete re-write from earlier versions of this programme
"""

# time the programme started
programme_start = datetime.now()

A_KB: int = 1024  # 1024 bytes is a kB
A_MB: int = A_KB * A_KB  # 1024 bytes * 1024 is an MB
A_GB: int = A_MB * A_KB
A_TB: int = A_GB * A_KB
max_hash_size_default: int = A_GB  # in bytes - maximum size of file to hash
first_n_files: int | None = None  # process the first n files, for testing
cores = cpu_count() - 1  # processor cpu cores to use - leave one for the OS to use
hash_function = hashlib.sha1()
hash_function_name = hash_function.name
default_scan_location = pathlib.Path(r"C:")
case_label_default: str = "no-case"
simple_output_default: bool = False
report_default: pathlib.Path = pathlib.Path().cwd() / "hash_report.csv"

_csv_report_header_simple_ = [
    "case-label",
    "relative-path",
    hash_function.name,
    "hash-error",
    "size",
    "created",
    "modified",
    "file-name",
    "file-extension",
]

_csv_report_header_ = [
    "case-label",
    "path",
    "sha-1",
    "sha-1-uc",
    "hash-error",
    "size",
    "created",
    "created-time",
    "modified",
    "modified-time",
    "file-name",
    "file-extension",
]

log_format = "[%(asctime)s.%(msecs)03d] %(levelname)-8s %(name)-12s %(lineno)d %(funcName)s - %(message)s"
log_date_format = "%Y-%m-%d %H:%M:%S"

# show all messages below in order of seriousness
log_level = logging.DEBUG  # shows all
# log_level = logging.INFO  # shows info and below
# log_level = logging.WARNING
# log_level = logging.ERROR
# log_level = logging.CRITICAL

logging.basicConfig(
    # Define logging level
    level=log_level,
    # Define the date format
    datefmt=log_date_format,
    # Declare the object we created to format the log messages
    format=log_format,
    # Force this log handler to take over the others that may have been declared in other modules
    # see: https://github.com/python/cpython/blob/3.8/Lib/logging/__init__.py#L1912
    force=True,
    # Declare handlers
    handlers=[
        # logging.FileHandler(f"{app_name}.log", encoding="UTF-8"),
        logging.StreamHandler(sys.stdout),
    ],
)

log = logging.getLogger(__name__)


# https://stackoverflow.com/questions/739654/how-to-make-function-decorators-and-chain-them-together?rq=1
def benchmark(func):
    """
    A decorator that prints the time a function takes
    to execute.
    """
    import time

    def wrapper(*args, **kwargs):
        t = time.perf_counter()
        res = func(*args, **kwargs)
        # print(
        #     "====== {func.__name__} - {time.perf_counter() - t} ======"
        #     )
        # )
        log.debug(
            "======> function: {0} - run time: {1}".format(
                func.__name__, time.perf_counter() - t
            )
        )
        return res

    return wrapper


def parse_args(parser):
    """Parse the programme arguments
    :param parser:
    :return: arguments
    """

    parser.add_argument(
        "-c",
        "--case",
        "--case-label",
        "--case_label",
        "--label",
        dest="case_label",
        help="case label",
        type=str,
    )

    parser.add_argument(
        "-r",
        "--report",
        help="output report file",
        dest="report",
        type=pathlib.Path,
    )

    parser.add_argument(
        "-s",
        "--scan",
        "--scan_location",
        "--scan-location",
        "--location",
        dest="scan",
        type=pathlib.Path,
        help="location to recursively scan for file(s)",
    )

    parser.add_argument(
        "-m",
        "--max",
        "--max-file-size",
        "--max_file_size",
        "--max-file",
        "--max_hash_size",
        "--max-hash-size",
        dest="max_hash_size",
        type=int,
        default=max_hash_size_default,
        help=f"change the maximum size of a file that will be hashed, "
             "default size is: {max_hash_size_default} bytes",
    )

    parser.add_argument(
        "-b",
        "--simple",
        "--simple-output",
        "--simple_output",
        "--basic",
        dest="simple",
        help="produce the output file with minimal fields (date and time in one field not two, "
             "no uppercase hash, relative path from scan location etc)",
        action="store_true",  # no extra value after the parameter
    )

    parser.add_argument(
        "-v",
        "--version",
        dest="version",
        help="get version information then exit",
        action="store_true",  # no extra value after the parameter
    )

    args = parser.parse_args()
    logging.debug(str(args))
    return args


def get_sha1_hash(file: pathlib.Path) -> str:
    """
    From a pathlib file get the hash in chunks
    """

    try:
        with open(file, mode="rb") as f:
            hash = hashlib.sha1()
            for buffer in iter(partial(f.read, hashlib.sha1().block_size), b""):
                hash.update(buffer)
        return hash.hexdigest()
    except FileNotFoundError as fnfe:
        raise Exception("FileNotFoundError {0}: On file: {1}".format(fnfe, file))
    except Exception as e:
        raise Exception("Exception: {0}: On file: {1}".format(e, file))


def get_time(d: datetime) -> str:
    """get the time (including time zone) from a datetime"""
    return d.strftime("%H:%M:%S%z")


def get_date(d: datetime) -> str:
    return d.strftime("%Y-%b-%d")


def get_date_time(d: datetime) -> str:
    return f"{get_date(d)} {get_time(d)}"


def get_file_size(file: pathlib.Path | str) -> int:
    try:
        if isinstance(file, pathlib.Path):
            return file.stat().st_size
        elif isinstance(file, str):
            return os.path.getsize(file)
        else:
            logging.error(f"invalid file: {file}")
    except Exception as e:
        logging.error(f"Exception: {e}")


def get_file_name(file: pathlib.Path) -> str:
    try:
        return file.name
    except Exception as e:
        logging.error(f"Exception: {e}")


def get_file_extension(file: pathlib.Path) -> str:
    try:
        return file.suffix
    except Exception as e:
        logging.error(f"Exception: {e}")


def get_file_created(file: pathlib.Path) -> datetime:
    return datetime.fromtimestamp(file.stat().st_ctime)


def get_file_modified(file: pathlib.Path) -> datetime:
    try:
        if isinstance(file, str):
            file = pathlib.Path(file)
            return datetime.fromtimestamp(file.stat().st_mtime)
        elif isinstance(file, pathlib.Path):
            return datetime.fromtimestamp(file.stat().st_mtime)
        else:
            logging.error("invalid file: {file}")
        return datetime.fromtimestamp(file.stat().st_mtime)
    except Exception as e:
        logging.error(f"Exception: {e}")


def get_relative_path(
        file: pathlib.Path,
        scan_location: pathlib.Path = default_scan_location,
) -> pathlib.Path | None:
    r"""
    from the file path directory subtract the parts of the path that match the scan_location directory and file
    to be used when we want a hash of a file that has been copied to a new disk or path, we do not want the hash
    result to refer to the new disk or path
    e.g.
    file = c:\windows\temp\parrot.txt
    scan_location = c:\windows\temp
    return = temp\parrot.txt

    if a scan_location is a single file then return None (based on testing str(file) == str(scan_location)
    """
    try:
        if str(scan_location) == str(file):
            # log.debug(f'matching string file and scan_location: {file} == {scan_location} -> {str(scan_location) == str(file)}')
            return None
        return file.parent.relative_to(scan_location) / get_file_name(file)

    except ValueError as ve:
        # Compute a version of this path relative to the path represented by other.
        # If it’s impossible, ValueError is raised
        logging.warning(f"{ve} - {file} - {scan_location}")
        return None
    except Exception as e:
        logging.error(f"Exception: {e} - {file} - {scan_location}")
        return None


def get_file_and_hash_data(
        file: pathlib.Path,
        case_label,
        simple_output,
        max_hash_size: int = max_hash_size_default,
        scan_location=default_scan_location,
) -> dict:
    """
    Simple is default true so only report:
     - the hash in default lower case, not lower and uppercase as the default output
     - create date and time single value not separately as the default output
    """
    file_size: int = get_file_size(file)
    file_data = {
        "case-label": case_label,
        "file-name": get_file_name(file),
        "size": file_size,
        "file-extension": get_file_extension(file),
        "hash-error": "",
    }
    try:
        if simple_output:
            file_data["relative-path"] = str(get_relative_path(file, scan_location))
            file_data["created"] = get_date_time(get_file_created(file))
            file_data["modified"] = get_date_time(get_file_modified(file))
        else:
            file_data["path"] = str(file)
            file_data["created"] = get_date(get_file_created(file))
            file_data["created-time"] = get_time(get_file_created(file))
            file_data["modified"] = get_date(get_file_modified(file))
            file_data["modified-time"] = get_time(get_file_modified(file))

        if file_size > max_hash_size:
            file_data[
                "hash-error"
            ] = f"file size, {file_size} > {max_hash_size}, hash skipped"
            log.debug(f"big file: {file}: size: {file_size} > {max_hash_size}")
        else:
            # file size is ok, do the hash
            if simple_output:
                file_data[hash_function_name] = get_sha1_hash(file)
            else:
                hash_val = get_sha1_hash(file)
                file_data["sha-1"] = hash_val
                file_data[f"sha-1-uc"] = hash_val.upper()

        if file_size < 1:
            file_data["hash-error"] = "file size is 0 bytes"
            log.debug(f"zero bytes file: {file}: size: {file_size}")

    except Exception as e:
        file_data["hash-error"] = e

    return file_data


def get_file_list(
        scan_location: pathlib.Path,
        first_n_files: int | None = first_n_files,
) -> List[pathlib.Path]:
    """
    Populates the lists of objects (file(s) etc to be catalogued)
    file path -scan_location- to be catalogued (relative or absolute)
    creates a list of all file items
    yield pathlib items
    """
    file_list = []

    # just a single file
    if scan_location.is_file():
        log.info("Scan location is a file: {0}".format(str(scan_location)))
        # file_list.append(pathlib.Path(scan_location))
        yield scan_location
    else:
        log.info("Scan location is a folder: {0}".format(pathlib.Path(scan_location)))

    if pathlib.Path(scan_location).is_absolute():
        # log.debug('Scan location to hash: {0}'.format(pathlib.Path(scan_location)))
        scan_location = pathlib.Path(scan_location)
    else:
        scan_location = pathlib.Path(scan_location).resolve()
        # log.debug('File (relative) location to hash: {0}'.format(scan_location))

    if not pathlib.Path(scan_location).exists():
        log.critical("Location to hash is not found: {0}".format(scan_location))
        exit(1)

    # item_list = scan_location.glob(filter)
    item_list: Generator[pathlib.Path, None, None] | None = None
    try:
        item_list = scan_location.rglob("*")

    except Exception as e:
        logging.warning("rglob: {0}".format(e))

    count = 1
    for item in item_list:
        try:
            # lots of other files system information may be gathered at this point if needed
            if item.is_file():
                # file_list.append(item)
                yield item
                if first_n_files is not None:
                    count = count + 1
                    if count > first_n_files:
                        log.info(
                            f"Only attempting to hash the first: {first_n_files} at the scan_location: {scan_location}"
                        )
                        break

        except Exception as e:
            logging.warning("get file list: {0}".format(e))

    # logging.debug('Size of file list to hash: {0}'.format(len(file_list)))
    # return file_list


def run_hash_multiprocessor_yield(
        file_list: List[pathlib.Path],
        case_label: str,
        simple_output: bool,
        cores: int | None = None,
        max_hash_size: int = max_hash_size_default,
        scan_location: pathlib.Path = default_scan_location,
) -> Generator[int, None, None]:
    futures = []
    if cores is None:
        cores = cpu_count() - 1
    log.info(
        f"Processing with multi processor executor with {cores} out of {cpu_count()} cores"
    )
    with ProcessPoolExecutor(cores) as executor:
        for file in file_list:
            futures.append(
                executor.submit(
                    get_file_and_hash_data,
                    file,
                    case_label,
                    simple_output,
                    max_hash_size,
                    scan_location,
                )
            )

    for future in concurrent.futures.as_completed(futures):
        try:
            hash_object = future.result()
        except Exception as e:
            log.error(f"hash generated an exception: {e}")
        else:
            yield hash_object


@benchmark
def run_hash(file_list: List[pathlib.Path], case_label):
    """used for testing - simple single processor core hash"""
    for file in file_list:
        result = get_file_and_hash_data(
            file, case_label, simple_output=simple_output_default
        )
        print(result)


@benchmark
def main(
        scan_location: pathlib.Path,
        report: pathlib.Path,
        case_label: str,
        simple_output: bool = simple_output_default,
        first_n_files: int = None,
        cores: int | None = cores,
        max_hash_size: int = max_hash_size_default,
) -> pathlib.Path:
    logging.debug(f"CSV report file: {report}")
    if report.exists():
        log.warning(f"Overwriting existing report file: {report}")
    output_file = None

    if simple_output:
        csv_head = _csv_report_header_simple_
    else:
        csv_head = _csv_report_header_
    log.debug(f"CSV output format: {csv_head} - simple output: {simple_output}")
    try:
        with open(report, "w", encoding="utf-8") as output_file:
            csv_writer = csv.DictWriter(
                output_file,
                fieldnames=csv_head,
                quoting=csv.QUOTE_ALL,
                lineterminator="\n",
            )
            csv_writer.writeheader()

            hash_generator = run_hash_multiprocessor_yield(
                get_file_list(
                    scan_location,
                    first_n_files=first_n_files,
                ),
                case_label,
                simple_output,
                cores=cores,
                max_hash_size=max_hash_size,
                scan_location=scan_location,
            )
            index = None
            for index, result in enumerate(hash_generator, start=1):
                # log.debug(f'index: {index} - {result}')
                # result_specifics = {key: value for key, value in result.items() if key in csv_head}
                # print('result as dict', '- ', result_specifics)
                # result_errors = {key: value for key, value in result.items() if key not in csv_head}
                # pprint('result as dict', '- ', result_errors)
                csv_writer.writerow(result)
            log.info(f"{index} files hashed")
    except Exception as e:
        log.error(f"Exception: {e} - report file: {report}")

    return report


if __name__ == "__main__":

    args = parse_args(argparse.ArgumentParser(description=description, prog=app_name))

    if args.version:
        logging.info(f"Application: {app_name}, Version: {__version__}")
        print(f"Application: {app_name}, Version: {__version__}")
        sys.exit(0)

    if args.scan is None:
        logging.critical(
            f"Scan location not provided, please provide a directory or file to scan for files to hash."
        )
        sys.exit(1)

    if args.case_label is None:
        case_label = case_label_default
        logging.warning(f"Case label not provided, using default: {case_label}")
    else:
        case_label = args.case_label
        log.info(f"Using case label: {case_label}")

    if args.report is None:
        log.warning(
            f"Output report file not specified, using default: {report_default}"
        )
        report = report_default
    else:
        report = args.report
        # log.info(f'Using output report: {report}')

    if args.simple:
        logging.info(f"Simplified basic output")
        simple = True
    else:
        simple = simple_output_default
        log.info(f"Using default output format: {simple}")

    if args.max_hash_size is None:
        max_hash_size = max_hash_size_default
        log.warning(f"Maximum file size to hash is default:  {max_hash_size} bytes")
    else:
        max_hash_size = args.max_hash_size
        log.warning(f"Maximum file size to hash is:  {max_hash_size} bytes")
    # # works (single core)
    # run_hash(get_file_list(scan_location, first_n_files=first_n_files), case_label_default)

    # for cores in range(1, 10):
    # works with error catching
    # run_hash_multiprocessor(get_file_list(scan_location, first_n_files=first_n_files), cores=cores)

    report_file = main(
        args.scan,
        report,
        case_label,
        simple_output=simple,
        first_n_files=first_n_files,
        cores=cores,
        max_hash_size=max_hash_size,
    )
    log.info(f"Output report: {report_file}")
    logging.info(
        "Programme stop: {0}, running time: {1}".format(
            datetime.now(), datetime.now() - programme_start
        )
    )
    sys.exit(0)
