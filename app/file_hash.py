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
__last_modified__ = '25 Feb 2021'

_csv_header = ['file-path', 'sha-1', 'error', 'size']

message_box_on = False


class Config:
    # default
    scan_location = r'.\test files'
    report = r'hash-report.csv'
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
    logfile = 'file-hash.log'

    # Define the log format
    log_format = '[%(asctime)s] %(levelname)-8s %(name)-12s %(lineno)d %(funcName)s - %(message)s'

    log_date_format = '%Y-%m-%d:%H:%M:%S'


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

    parser.add_argument('-report', '--report',
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
        raise Exception('Warning: get_sha1_hash: FileNotFoundError {0}: On file: {1}'.format(fnfe, file))
    except Exception as e:
        raise Exception('Warning: get_sha1_hash: Exception: {0}: On file: {1}'.format(e, file))


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
    # TODO: what to do if it is not a pathlib or string

    # just a single file
    if scan_location.is_file():
        logging.info('Scan location is a file: {0}'.format(str(scan_location)))
        file_list.append(pathlib.Path(scan_location))
        return file_list
    else:
        logging.info('Scan location is a folder: {0}'.format(pathlib.Path(scan_location)))

    if pathlib.Path(scan_location).is_absolute():
        logging.debug('Scan location to hash: {0}'.format(pathlib.Path(scan_location)))
        scan_location = pathlib.Path(scan_location)
    else:
        scan_location = pathlib.Path(scan_location).resolve()
        logging.debug('File (relative) location to hash: {0}'.format(scan_location))

    if not pathlib.Path(scan_location).exists():
        logging.critical('Location to hash is not found: {0}'.format(scan_location))
        exit(1)

    # item_list = scan_location.glob(filter)
    item_list = []
    try:
        item_list = scan_location.rglob('*')
    except Exception as e:
        logging.warning('rglob: {0}'.format(e))
        pass

    item_count = 0

    for item in item_list:
        item_count = item_count + 1
        try:
            # lots of other files system information may be gathered at this point if needed
            if item.is_file():
                file_list.append(item)

        except Exception as e:
            logging.warning('get file list: {0}'.format(e))

    logging.debug('Size of file list to hash: {0}'.format(len(file_list)))
    return file_list


def save_dict_as_csv(data_list: List[dict], file: pathlib):
    """
    Save the **data_list** to a csv **file**
    :param data_list: list of dict with data to write to a csv file
    :param file: output csv file
    :return:
    """
    logging.debug('CSV report file: {0}'.format(file))
    try:
        output_file = open(file, 'w+', encoding='utf-8')
    except Exception as e:
        logging.error('Output file open failure: {0}'.format(e))
        return 1

    csv_writer = csv.DictWriter(output_file, fieldnames=_csv_header, quoting=csv.QUOTE_ALL, lineterminator='\n')
    csv_writer.writeheader()
    logging.debug('Number of file hashes to report: {0}'.format(len(data_list)))
    try:
        for data in data_list:
            csv_writer.writerow(data)

    except Exception as e:
        logging.error('csv dict write error: {0} to file: {1}'.format(e, file))
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
                logging.debug('Hash exception: {0}'.format(e))
        else:
            file_hash_error_count = file_hash_error_count + 1
            result_dict[_csv_header[2]] = 'big-file-skipped > {0} bytes'.format(config.file_size_hash_skip)

        result_dict[_csv_header[3]] = file_size

        # print('d: {result_dict}'.format(result_dict)
        result_list.append(result_dict)
    logging.debug('Files not hashed (due to being too big): {0}'.format(file_hash_error_count))
    save_dict_as_csv(result_list, report)


if __name__ == "__main__":

    if message_box_on:
        message_box.showinfo('File Hash', 'main - {0}'.format(sys.argv))

    config = Config
    args = None
    try:
        args = parse_args(argparse.ArgumentParser(description='File Hash.', prog='file-hash'), config)
    except Exception as e:
        logging.critical('Parse arguments error: {0}'.format(e))

    if args.scan_location is not None:
        config.scan_location = args.scan_location
    else:
        logging.critical('No scan location provided')
        sys.exit(1)

    if args.report is not None:
        config.report_location = args.report

    # to fix the logger not writing to file, see:
    # https://stackoverflow.com/questions/15892946/python-logging-module-is-not-writing-anything-to-file
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Define basic configuration
    logging.basicConfig(
        # Define logging level
        level=config.log_level,
        # Define the date format
        datefmt=config.log_date_format,
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

    logging.info('Version: {0}, Last modified: {1}'.format(__version__, __last_modified__))
    logging.info('Args: {0}'.format(str(sys.argv)))

    main(config.scan_location, config.report_location)
