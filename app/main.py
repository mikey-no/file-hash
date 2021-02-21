import argparse
import csv
import hashlib
import os
import pathlib

from functools import partial

__author__ = 'MY'
__version__ = '0.0.1'
__last_modified__ = '18 Feb 2021'

__DEBUG__ = False

from typing import List

_csv_header = ['file-path', 'sha-1', 'error', 'size']

item_list = []
item_count = 0  # not sure why I cannot get the length of item_list
file_list = []
done_file_list = []
file_list_big = []  # for files bigger than file_size_hash_skip
file_list_big_no_hash = []  # for files bigger than file_size_no_hash_skip
directory_list = []
symlink_list = []
symlink_to_list = []
link_to_list = []
mount_point_list = []


class Config:
    # default
    scan_location = r'.\test files'
    report = r'.\hash-report.csv'
    # really big files do not hash (1 GByte)
    # file_size_hash_skip = (1024 ** 3)
    file_size_hash_skip = (1024 ** 1)


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

    parser.add_argument('-report_location',
                        default=config.report,
                        required=False,
                        help=report_location_help)

    args = parser.parse_args()
    if __DEBUG__:
        print(str(args))
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
    # just a single file
    if scan_location.is_file():
        print(f'scan_location is a file: {str(scan_location)}')
        file_list.append(pathlib.Path(scan_location))
        return file_list
    else:
        print(f'scan_location is a folder: {pathlib.Path(scan_location)}')

    if pathlib.Path(scan_location).is_absolute():
        print(f'File location to hash: {pathlib.Path(scan_location)}')
        scan_location = pathlib.Path(scan_location)
    else:
        scan_location = pathlib.Path(scan_location).resolve()
        print(f'File (relative) location to hash: {scan_location}')

    if not pathlib.Path(scan_location).exists():
        print(f'Error: get_file_list: Location to hash is not found: {scan_location}')
        exit(1)

    # item_list = scan_location.glob(filter)
    try:
        item_list = scan_location.rglob('*')
    except Exception as e:
        print(f'Warning: get_file_list: rglob: {e}')
        pass

    global item_count

    for item in item_list:
        item_count = item_count + 1
        try:
            # lots of other files system information may be gathered at this point if needed
            if item.is_file():
                file_list.append(item)

        except Exception as e:
            print(f'Warning: get_file_list: {e}')

    return file_list


def save_dict_as_csv(data_list: List[dict], file: pathlib):
    """
    Save the **data_list** to a csv **file**
    :param data_list: list of dict with data to write to a csv file
    :param file: output csv file
    :return:
    """
    try:
        output_file = open(file, 'w+', encoding='utf-8')
    except Exception as e:
        print(f'Error: print_dict_as_csv: Output file open failure: {e}')
        return 1

    csv_writer = csv.DictWriter(output_file, fieldnames=_csv_header, quoting=csv.QUOTE_ALL, lineterminator='\n')
    csv_writer.writeheader()
    print(f'length of list: {len(data_list)}')
    try:
        for data in data_list:
            csv_writer.writerow(data)
            print(data)
    except Exception as e:
        print(f'Error: file_hash: print_dict: {e} to file: {file}')
    output_file.close()
    print(f'CSV output file: {output_file.name}')


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

    for file in file_list:
        result_dict = {_csv_header[0]: str(file)}
        file_size = get_file_size(file)
        if file_size < config.file_size_hash_skip:
            try:
                result_dict[_csv_header[1]] = get_sha1_hash(file)
            except Exception as e:
                result_dict[_csv_header[2]] = e
        else:
            result_dict[_csv_header[2]] = f'big-file-skipped > {config.file_size_hash_skip} bytes'
        result_dict[_csv_header[3]] = file_size

        print(f'd: {result_dict}')
        result_list.append(result_dict)

    save_dict_as_csv(result_list, report)


if __name__ == "__main__":
    config = Config
    args = parse_args(argparse.ArgumentParser(description='Hash files.', prog='hash-file'), config)

    if args.scan_location is not None:
        config.scan_location = args.scan_location

    if args.report_location is not None:
        config.report_location = args.report_location

    main(config.scan_location, config.report_location)
