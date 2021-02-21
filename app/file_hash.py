import argparse
import csv
import hashlib
import logging
import os
import pathlib
import sys

from functools import partial
from tkinter import messagebox as message_box
from typing import List

__author__ = 'MY'
__version__ = '0.0.2'
__last_modified__ = '24 Feb 2021'

# adding logging - branch : logging

_csv_header = ['file-path', 'sha-1', 'error', 'size']

message_box_on = False


class Config:
    # default
    scan_location = r'.\test files'
    report = fr'{os.getcwd()}\hash-report.csv'  # not sure why '$(pwd)' is one directory up
    # really big files do not hash (1 GByte)
    file_size_hash_skip = (1024 ** 3)
    # file_size_hash_skip = (1024 ** 1) # small file for test

    # show all messages below in order of seriousness
    log_level = logging.DEBUG  # shows all
    # log_level = logging.INFO  # shows info and below
    # log_level = logging.ERROR
    # log_level = logging.WARNING

    # Log file location
    # logfile = r'.\Exports.ILB\hash-file-log.txt'
    logfile = f'{os.getcwd()}\\file-hash.log'

    # Define the log format
    log_format = '[%(asctime)s] %(levelname)-8s %(name)-12s %(lineno)d %(funcName)s - %(message)s'


def parse_args(parser: argparse, config: Config):
    """Parse the programme arguments
    :param config:
    :param parser:
    :return: arguments
    """
    location_help = r"""location specifying the start point to scan to recursively hash files.
                        May also be a single file. 
                        """
    report_location_help = r"""location specifying the csv report file in which to write results. """

    parser.add_argument('scan_location',
                        help=location_help)

    parser.add_argument('-report_location', '--report_location',
                        default=config.report,
                        required=False,
                        help=report_location_help)

    args = parser.parse_args()
    logging.debug(str(args))
    return args


def get_file_size(file: pathlib):
    return os.path.getsize(file)


def get_sha1_hash(file: pathlib):
    """
    From a pathlib file get the hash in chunks
    """

    try:
        with open(file, mode='rb') as f:
            hash = hashlib.sha1()
            for buffer in iter(partial(f.read, 128), b''):
                hash.update(buffer)
        return hash.hexdigest()
    except FileNotFoundError as fnfe:
        raise Exception(f'Warning: get_sha1_hash: FileNotFoundError {fnfe}: On file: {file}')
    except Exception as e:
        raise Exception(f'Warning: get_sha1_hash: Exception: {f}: On file: {file}')


def get_file_list(scan_location: pathlib):
    """
    Populates the lists of objects (file(s) etc to be catalogued)
    file path -scan_location- to be catalogued (relative or absolute)
    creates a list of all file and file like items
    returns list of pathlib items
    """
    file_list = []
    if isinstance(scan_location, str):
        scan_location = pathlib.Path(scan_location)

    # just a single file
    if scan_location.is_file():
        logging.info(f'Scan location is a file: {str(scan_location)}')
        file_list.append(pathlib.Path(scan_location))
        return file_list
    else:
        logging.info(f'Scan location is a folder: {pathlib.Path(scan_location)}')

    if pathlib.Path(scan_location).is_absolute():
        logging.debug(f'Scan location to hash: {pathlib.Path(scan_location)}')
        scan_location = pathlib.Path(scan_location)
    else:
        scan_location = pathlib.Path(scan_location).resolve()
        logging.debug(f'File (relative) location to hash: {scan_location}')

    if not pathlib.Path(scan_location).exists():
        logging.critical(f'Location to hash is not found: {scan_location}')
        exit(1)

    # item_list = scan_location.glob(filter)
    try:
        item_list = scan_location.rglob('*')
    except Exception as e:
        logging.warning(f'rglob: {e}')
        pass

    item_count = 0

    for item in item_list:
        item_count = item_count + 1
        try:
            # lots of other files system information may be gathered at this point if needed
            if item.is_file():
                file_list.append(item)

        except Exception as e:
            logging.warning(f'get_file_list: {e}')

    logging.debug(f'Size of file list to hash: {len(file_list)}')
    return file_list


def save_dict_as_csv(data_list: List[dict], file: pathlib):
    """
    Save the **data_list** to a csv **file**
    :param data_list: list of dict with data to write to a csv file
    :param file: output csv file
    :return:
    """
    logging.debug(f'CSV report file: {file}')
    try:
        output_file = open(file, 'w+', encoding='utf-8')
    except Exception as e:
        logging.error(f'print_dict_as_csv: Output file open failure: {e}')
        return 1

    csv_writer = csv.DictWriter(output_file, fieldnames=_csv_header, quoting=csv.QUOTE_ALL, lineterminator='\n')
    csv_writer.writeheader()
    logging.debug(f'Number of file hashes to report: {len(data_list)}')
    try:
        for data in data_list:
            csv_writer.writerow(data)

    except Exception as e:
        logging.error(f'Error: file_hash: print_dict: {e} to file: {file}')
    finally:
        output_file.close()


def main(scan_location: pathlib = Config.scan_location, report: pathlib = Config.report, config=Config):
    """
    main way to run the programme if not run via local command line
    :param config: optional object with default settings
    :param scan_location: location to scan for file(s) - inc sub directories to sha-1 hash
    :param report: csv report
    :return:
    """

    file_list = get_file_list(scan_location)
    result_list = []
    file_hash_error_count = 0
    for file in file_list:
        result_dict = {_csv_header[0]: str(file)}
        file_size = get_file_size(file)
        if file_size < config.file_size_hash_skip:
            try:
                result_dict[_csv_header[1]] = get_sha1_hash(file)
            except Exception as e:
                result_dict[_csv_header[2]] = e
                logging.debug(f'Hash exception: {e}')
        else:
            file_hash_error_count =  file_hash_error_count + 1
            result_dict[_csv_header[2]] = f'big-file-skipped > {config.file_size_hash_skip} bytes'

        result_dict[_csv_header[3]] = file_size

        # print(f'd: {result_dict}')
        result_list.append(result_dict)
    logging.debug(f'Files not hashed (due to being too big): {file_hash_error_count}')
    save_dict_as_csv(result_list, report)


if __name__ == "__main__":

    if message_box_on: message_box.showinfo(f'File Hash', 'main - {sys.argv}')

    config = Config
    try:
        args = parse_args(argparse.ArgumentParser(description='File Hash.', prog='file-hash'), config)
    except Exception as e:
        logging.critical(f'Parse arguments error: {e}')

    if args.scan_location is not None:
        config.scan_location = args.scan_location

    if args.report_location is not None:
        config.report_location = args.report_location

    # to fix the logger not writing to file, see:
    # https://stackoverflow.com/questions/15892946/python-logging-module-is-not-writing-anything-to-file
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Define basic configuration
    logging.basicConfig(
        # Define logging level
        level=config.log_level,
        # Define the date format
        datefmt='%Y-%m-%d:%H:%M:%S',
        # Declare the object we created to format the log messages
        format=config.log_format,
        # Declare handlers
        handlers=[
            logging.FileHandler(config.logfile),
            logging.StreamHandler(sys.stdout),
        ]
    )

    # Define your own logger name
    logging = logging.getLogger('file-hash')

    logging.info(f'Args: {str(sys.argv)}')

    main(config.scan_location, config.report_location)
