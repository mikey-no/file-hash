import argparse
import csv
import hashlib
import logging
import os
import pathlib
import sys

from datetime import datetime
from functools import partial
from tkinter import messagebox as message_box
from typing import List

"""tag: v0.0.4"""

__author__ = 'MY'
__version__ = '0.0.4'
__last_modified__ = '03 Mar 2021'

_report_header = [
    'case-label', 'file-path', 'sha-1', 'sha-1-uc', 'error', 'size',
    'created', 'created-time', 'modified', 'modified-time', 'file-name', 'file-extension'
]

use_config_one = False


class Config:
    # default
    scan_location = r'.\test files'
    report = r'hash-report.csv'
    case_label = r'case-001'
    message_box_on = True

    # really big files do not hash (1 GByte) it would be very slow
    file_size_hash_skip = (1024 ** 3)
    # file_size_hash_skip = (1024 ** 1) # small file for test

    # show all messages below in order of seriousness
    log_level = logging.DEBUG  # shows all
    # log_level = logging.INFO  # shows info and below
    # log_level = logging.WARNING
    # log_level = logging.ERROR
    # log_level = logging.CRITICAL

    # Log file location
    logfile = 'file-hash.log'

    # Define the log format
    log_format = '[%(asctime)s] %(levelname)-8s %(name)-12s %(lineno)d %(funcName)s - %(message)s'
    log_date_format = '%Y-%m-%d:%H:%M:%S'


class ConfigOne(Config):
    """ Alternate Configuration """
    scan_location = r'.\Source Files.ILB\test-data-001'
    report = r'hash-report.csv'
    logfile = r'.\Exports.ILB\hash-file.log'


# --------------------- re-usable system functions ----------------------


def simple_parse_args(config: Config) -> None:
    """ Alternate simpler programme argument parser
    replace " for _ in the case label
    replace ' ' for _ in the case label
    """

    #                            0             1             2          3
    #                            1             2             3          4
    usage = r'Usage: python app\file-hash.py a_report.csv scan-location case-label'
    if len(sys.argv) == 4:
        logging.info('{0} args in the correct range'.format(len(sys.argv)))
        config.report = pathlib.Path(sys.argv[1].strip())
        config.scan_location = pathlib.Path(sys.argv[2].strip())
        config.case_label = str(sys.argv[3].strip().replace(r'"', '_').replace(' ', '_'))
    else:
        logging.critical(usage)
        logging.critical('{0} args out of range'.format(len(sys.argv)))
        sys.exit(1)


def check_path_instance(obj: object, name: str) -> pathlib.Path:
    """ Check path instance type then convert and return
    :param obj: object to check and convert
    :param name: name of the object to check (apparently there is no sane way to get the name of the variable)
    :return: pathlib.Path of the object else exit the programme with critical error
    """

    if isinstance(obj, (pathlib.WindowsPath, pathlib.PosixPath)):
        return pathlib.Path(obj)
    else:
        if isinstance(obj, str):
            return pathlib.Path(str(obj))  # TODO: force to utf-8 maybe
        else:
            logging.critical(
                '{0} type is: {1}, not pathlib.WindowsPath, pathlib.PosixPath or str'.format(name, type(obj))
            )
            sys.exit(1)


def setup_logging(logging, config: Config) -> None:
    """
    Setup the logging with all my settings
    :param logging: from import logging
    :param config: config class
    :return: None
    """
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

    logging.debug(str(sys.version_info))
    logging.debug(sys.modules.keys())


# --------------------- end of re-usable system functions ----------------------

def get_time(d: datetime) -> datetime:
    """ get the time (including time zone) from a datetime """
    return d.strftime("%H:%M:%S%z")


def get_date(d: datetime) -> datetime:
    return d.strftime("%Y-%b-%d")


def get_file_size(file: pathlib):
    return os.path.getsize(str(file))


def get_file_name(file: pathlib):
    return file.name


def get_file_extension(file: pathlib):
    return file.suffix


def get_file_created(file):
    return datetime.fromtimestamp(file.stat().st_ctime)


def get_file_modified(file):
    return datetime.fromtimestamp(file.stat().st_mtime)


def get_sha1_hash(file: pathlib):
    """
    From a pathlib file get the hash in chunks
    """

    try:
        with open(str(file), mode='rb') as f:
            hash = hashlib.sha1()
            for buffer in iter(partial(f.read, 128), b''):
                hash.update(buffer)
        return hash.hexdigest()
    except FileNotFoundError as fnfe:
        raise Exception('Warning: get_sha1_hash: FileNotFoundError {0}: On file: {1}'.format(fnfe, file))
    except Exception as e:
        raise Exception('Warning: get_sha1_hash: Exception: {0}: On file: {1}'.format(e, file))


def get_file_list(scan_location: pathlib) -> List[pathlib.Path]:
    """
    Populates the lists of objects (file(s) etc to be catalogued)
    file path -scan_location- to be catalogued (relative or absolute)
    creates a list of all file items
    returns list of pathlib items
    """
    file_list = []
    scan_location = check_path_instance(scan_location, scan_location)

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
    Defaults explicitly to utf-8 encoding (TODO: handle when file names are not UTF-8)
    :param data_list: list of dict with data to write to a csv file
    :param file: output csv file
    :return:
    """
    logging.debug('CSV report file: {0}'.format(file))
    try:
        output_file = open(str(file), 'w+', encoding='utf-8')
    except Exception as e:
        logging.error('Output file open failure: {0}'.format(e))
        return 1

    csv_writer = csv.DictWriter(output_file, fieldnames=_report_header, quoting=csv.QUOTE_ALL, lineterminator='\n')
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
        result_dict = {_report_header[0]: config.case_label}
        result_dict[_report_header[1]] = str(file)
        file_size = get_file_size(file)
        if file_size < config.file_size_hash_skip:
            try:
                hash = get_sha1_hash(file)
                result_dict[_report_header[2]] = hash
                result_dict[_report_header[3]] = hash.upper()
            except Exception as e:
                result_dict[_report_header[4]] = e
                logging.debug('Hash exception: {0}'.format(e))
        else:
            file_hash_error_count = file_hash_error_count + 1
            result_dict[_report_header[4]] = 'big-file-skipped > {0} bytes'.format(config.file_size_hash_skip)

        if file_size < 1:
            result_dict[_report_header[4]] = 'zero-bytes-file'

        # 0               1           2       3           4           5
        # 'case-label', 'file-path', 'sha-1', 'sha-1-uc', 'error', 'size', ..... then....
        #                           6           7                   8               9           10          11
        #                           'created', 'created-time', 'modified', 'modified-time', 'file-name', 'file-extension'
        result_dict[_report_header[5]] = file_size
        datetime_created = get_file_created(file)
        result_dict[_report_header[6]] = get_date(datetime_created)
        result_dict[_report_header[7]] = get_time(datetime_created)
        datetime_modified = get_file_modified(file)
        result_dict[_report_header[8]] = get_date(datetime_modified)
        result_dict[_report_header[9]] = get_time(datetime_modified)
        result_dict[_report_header[10]] = get_file_name(file)
        result_dict[_report_header[11]] = get_file_extension(file)

        result_list.append(result_dict)
    logging.debug('Files not hashed (due to being too big): {0}'.format(file_hash_error_count))
    save_dict_as_csv(result_list, report)


if __name__ == "__main__":

    if use_config_one is True:
        config = ConfigOne
    else:
        config = Config

    if config.message_box_on:
        message_box.showinfo('File Hash', 'main - {0}'.format(sys.argv))

    setup_logging(logging, config)

    simple_parse_args(config)

    logging.info('scan:   {0}'.format(config.scan_location))
    logging.info('report: {0}'.format(config.report))
    logging.info('case-label: {0}'.format(config.case_label))
    config.scan_location = check_path_instance(config.scan_location, 'config.scan_location')
    config.report = check_path_instance(config.report, 'config.report')
    main(config.scan_location, config.report)
    sys.exit(0)