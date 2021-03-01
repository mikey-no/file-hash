import pathlib
from datetime import datetime, timedelta, timezone
from typing import List

import pytest

from app.file_hash import get_sha1_hash, get_file_list, get_file_size, save_dict_as_csv, main, _report_header, \
    get_file_created, get_file_extension, get_file_modified, get_file_name, get_date, get_time


test_files_root = r'C:\Users\a\Documents\vss\python-experiments\test-files'

test_file_list_str = ['C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\kanji-教育漢字',
                      'C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\new 1.txt',
                      'C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\New Microsoft Word Document.docx',
                      'C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\New Text Document (2).txt',
                      'C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\New Text Document.txt',
                      'C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\UTF-16 encoding files-utf16',
                      'C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\永 - Wiktionary.URL',
                      'C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\cam.ac~mgk25\\combining-keycap.txt',
                      'C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\cam.ac~mgk25\\digraphs.txt',
                      'C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\cam.ac~mgk25\\grid-capital.txt',
                      'C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\cam.ac~mgk25\\grid-cyrillic-1.txt',
                      'C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\cam.ac~mgk25\\grid-cyrillic-2.txt',
                      'C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\cam.ac~mgk25\\grid-greek-1.txt',
                      'C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\cam.ac~mgk25\\grid-greek-2.txt',
                      'C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\cam.ac~mgk25\\grid-mixed-1.txt',
                      'C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\cam.ac~mgk25\\grid-mixed-2.txt',
                      'C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\cam.ac~mgk25\\grid-small.txt',
                      'C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\cam.ac~mgk25\\Index of _~mgk25_ucs_examples.html',
                      'C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\cam.ac~mgk25\\ipa-chart.txt',
                      'C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\cam.ac~mgk25\\ipa-english.txt',
                      'C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\cam.ac~mgk25\\luki2.txt',
                      'C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\cam.ac~mgk25\\lyrics-ipa.txt',
                      'C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\cam.ac~mgk25\\postscript-utf-8.txt',
                      'C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\cam.ac~mgk25\\quickbrown.txt',
                      'C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\cam.ac~mgk25\\revelation.txt',
                      'C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\cam.ac~mgk25\\rune-poem.txt',
                      'C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\cam.ac~mgk25\\TeX.txt',
                      'C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\cam.ac~mgk25\\UTF-8-demo.txt',
                      'C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\cam.ac~mgk25\\UTF-8-test.txt',
                      'C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\test-folder\\New Bitmap ImageFFF.bmp',
                      'C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\test-folder\\New Microsoft Excel Worksheet.xlsx',
                      'C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\test-folder\\New Text Document.txt - Shortcut.lnk',
                      'C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\test-folder\\꧇꧑꧑꧇ .txt',
                      'C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\test-folder\\New folder 2\\New Rich Text Document 3 deep.rtf']


class Config:
    # default
    location = r'.\test files'
    report = r'C:\Users\a\Documents\vss\python-experiments\file-hash\hash-report.csv'
    # really big files do not hash (1 GByte)
    # file_size_hash_skip = (1024 ** 3)
    file_size_hash_skip = (1024 ** 3)
    case_label = 'test-case'


def test_create_file(tmpdir):
    p = tmpdir.mkdir("sub").join("hello.txt")
    p.write("content")
    assert p.read() == "content"
    assert len(tmpdir.listdir()) == 1


def test_get_file(tmpdir):
    p = tmpdir.mkdir("sub").join("hello.txt")
    content = 'conticontinet big snake'
    p.write(content)
    assert p.read() == content
    assert len(tmpdir.listdir()) == 1
    assert get_file_size(pathlib.Path(p)) == len(content)


def test_get_file_created(tmpdir):
    now = datetime.now()
    p = tmpdir.mkdir("sub").join("hello.txt")
    content = 'conticontinet big snake'
    p.write(content)
    assert p.read() == content
    assert len(tmpdir.listdir()) == 1
    assert get_file_size(pathlib.Path(p)) == len(content)
    assert get_file_created(pathlib.Path(p)) == now


def test_get_file_created(tmpdir):
    now = datetime.now()
    p = tmpdir.mkdir("sub").join("hello.txt")
    content = 'conticontinet big snake'
    p.write(content)
    assert p.read() == content
    assert len(tmpdir.listdir()) == 1
    assert get_file_size(pathlib.Path(p)) == len(content)
    td = timedelta(milliseconds=300) # give it a generous 300 ms to do this
    response = get_file_modified(pathlib.Path(p))
    if response == now or response <= now + td:
        assert True
    else:
        assert False


def test_get_time():
    date_time_str1 = '2018-06-29 08:15:27.243860'
    date_time_obj1 = datetime.strptime(date_time_str1, '%Y-%m-%d %H:%M:%S.%f')
    date_time_obj1_check = date_time_obj1.strftime("%H:%M:%S%z")
    date_time_str2 = '2021-Feb-28 16:23:56.555666+0400'
    date_time_obj2 = datetime.strptime(date_time_str2, '%Y-%b-%d %H:%M:%S.%f%z')
    date_time_obj2_check = date_time_obj2.strftime("%H:%M:%S%z")
    assert isinstance(date_time_obj1, datetime)
    assert isinstance(date_time_obj2, datetime)
    assert str(get_time(date_time_obj1)) == date_time_obj1_check
    assert str(get_time(date_time_obj2)) == date_time_obj2_check


def test_get_date():
    date_time_str1 = '2018-06-29 08:15:27.243860'
    date_time_obj1 = datetime.strptime(date_time_str1, '%Y-%m-%d %H:%M:%S.%f')
    date_time_obj1_check = date_time_obj1.strftime("%Y-%b-%d")
    date_time_str2 = '2021-Feb-28 16:23:56.555666+0400'
    date_time_obj2 = datetime.strptime(date_time_str2, '%Y-%b-%d %H:%M:%S.%f%z')
    date_time_obj2_check = date_time_obj2.strftime("%Y-%b-%d")
    assert isinstance(date_time_obj1, datetime)
    assert isinstance(date_time_obj2, datetime)
    assert str(get_date(date_time_obj1)) == date_time_obj1_check
    assert str(get_date(date_time_obj2)) == date_time_obj2_check


def test_get_file_extension(tmpdir):
    p = tmpdir.mkdir("sub").join("hello.txt")
    content = 'conticontinet big snake'
    p.write(content)
    assert p.read() == content
    assert len(tmpdir.listdir()) == 1
    assert get_file_size(pathlib.Path(p)) == len(content)
    assert get_file_extension(pathlib.Path(p)) == '.txt'


def test_get_file_name(tmpdir):
    name = u'ᚢᚱ᛫ᛒᛦᚦ᛫ᚪᚾᛗᚩᛞ᛫ᚩᚾᛞ᛫ᚩᚠᛖᚱᚻᛦᚱᚾᛖᛞ'
    p = tmpdir.mkdir("sub").join(name)
    content = 'conticontinet big snake = with unicode stuff in the name'
    p.write(content)
    pl = pathlib.Path(p)
    assert p.read() == content
    assert len(tmpdir.listdir()) == 1
    assert get_file_size(pl) == len(content)
    assert get_file_name(pl) == name


def test_simple_sha1_hash_file(tmpdir):
    p = tmpdir.mkdir("sub").join("hello.txt")
    p.write("content")
    assert p.read() == "content"
    assert len(tmpdir.listdir()) == 1
    result = get_sha1_hash(p)
    assert result == '040F06FD774092478D450774F5BA30C5DA78ACC8'.lower()  # confirmed with 7zip


def test_test_files_exist():
    location = pathlib.Path(test_files_root).resolve()
    assert pathlib.Path(location).exists()


def test_test_file_list():
    location = pathlib.Path(test_files_root).resolve()
    assert pathlib.Path(location).exists()
    result_list = get_file_list(location)
    assert len(result_list) == 34  # test confirmed with os
    # convert result_list to list of strings called result_list_str
    result_list_str: List[str] = []
    for file in result_list:
        f = str(file)
        result_list_str.append(f)

    assert result_list_str == test_file_list_str


def test_get_file_size():
    file = pathlib.Path(
        'C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\cam.ac~mgk25\\grid-cyrillic-1.txt'
    )
    assert get_file_size(file) == 2197  # test confirfmed with os


def test_print_dict_as_csv(tmpdir):
    config = Config
    config.file_size_hash_skip = 1024
    file1 = pathlib.Path(
        'C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\cam.ac~mgk25\\grid-cyrillic-1.txt'
    )
    file2 = pathlib.Path(
        'C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\cam.ac~mgk25\\grid-cyrillic-2.txt'
    )
    report = tmpdir.mkdir("sub").join("test-report.csv")
    report = pathlib.Path(report)
    assert len(tmpdir.listdir()) == 1

    # make a data_dict list to print
    data_list_in = [
        {
            f'{_report_header[0]}': str(file1),
            f'{_report_header[1]}': 'abcdefg',
            f'{_report_header[2]}': 'no error here',
            f'{_report_header[3]}': '9'
        },
        {
            f'{_report_header[0]}': str(file2),
            f'{_report_header[1]}': '1234567890',
            f'{_report_header[2]}': 'no error here or here',
            f'{_report_header[3]}': '10',
        }
    ]

    save_dict_as_csv(data_list=data_list_in, file=report)

    try:
        result_report_file = open(report, 'r', encoding='utf-8')
    except Exception as e:
        print(f'Error: test_file_sha1_hash: test file open failure: {e}')
        return 1
    result_file = result_report_file.read()
    result_report_file.close()
    assert len(result_file) > 1
    ideal_answer = r""""case-label","file-path","sha-1","sha-1-uc","error","size","created","created-time","modified","modified-time","file-name","file-extension"
"C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\grid-cyrillic-1.txt","abcdefg","no error here","9","","","","","","","",""
"C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\grid-cyrillic-2.txt","1234567890","no error here or here","10","","","","","","","",""
"""
    assert ideal_answer == result_file


def test_main(tmpdir):
    config = Config
    config.file_size_hash_skip = 1024
    report = tmpdir.mkdir("sub").join("test-report.csv")
    report = pathlib.Path(report)
    assert len(tmpdir.listdir()) == 1
    main(pathlib.Path(test_files_root), pathlib.Path(report), config)
    result_file = ''
    try:
        result_report_file = open(report, 'r', encoding='utf-8')
        result_file = result_report_file.read()
    except Exception as e:
        print(f'Error: test_file_sha1_hash: test file open failure: {e}')
        return 1
    finally:
        result_report_file.close()
    assert len(result_file) > 100
    assert result_file == r""""case-label","file-path","sha-1","sha-1-uc","error","size","created","created-time","modified","modified-time","file-name","file-extension"
"test-case","C:\Users\a\Documents\vss\python-experiments\test-files\kanji-教育漢字","","","big-file-skipped > 1024 bytes","21864","2020-Oct-14","20:34:47","2020-Oct-14","20:34:47","kanji-教育漢字",""
"test-case","C:\Users\a\Documents\vss\python-experiments\test-files\new 1.txt","","","big-file-skipped > 1024 bytes","735085","2020-Oct-13","21:20:53","2020-Oct-13","21:20:58","new 1.txt",".txt"
"test-case","C:\Users\a\Documents\vss\python-experiments\test-files\New Microsoft Word Document.docx","da39a3ee5e6b4b0d3255bfef95601890afd80709","DA39A3EE5E6B4B0D3255BFEF95601890AFD80709","zero-bytes-file","0","2020-Aug-14","15:55:08","2020-Aug-14","15:55:08","New Microsoft Word Document.docx",".docx"
"test-case","C:\Users\a\Documents\vss\python-experiments\test-files\New Text Document (2).txt","","","big-file-skipped > 1024 bytes","147016","2020-Oct-13","21:18:37","2020-Oct-13","21:19:27","New Text Document (2).txt",".txt"
"test-case","C:\Users\a\Documents\vss\python-experiments\test-files\New Text Document.txt","da39a3ee5e6b4b0d3255bfef95601890afd80709","DA39A3EE5E6B4B0D3255BFEF95601890AFD80709","zero-bytes-file","0","2020-Aug-14","15:55:13","2020-Aug-14","15:55:13","New Text Document.txt",".txt"
"test-case","C:\Users\a\Documents\vss\python-experiments\test-files\UTF-16 encoding files-utf16","5403728097d5bbd5a0c37d4ac88512b3e7a01c8a","5403728097D5BBD5A0C37D4AC88512B3E7A01C8A","","152","2020-Oct-14","10:41:24","2020-Oct-14","10:43:20","UTF-16 encoding files-utf16",""
"test-case","C:\Users\a\Documents\vss\python-experiments\test-files\永 - Wiktionary.URL","c7b81a227cd313feef0b792a252e63ba1fc62d2c","C7B81A227CD313FEEF0B792A252E63BA1FC62D2C","","221","2020-Oct-14","20:27:36","2020-Nov-05","15:21:00","永 - Wiktionary.URL",".URL"
"test-case","C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\combining-keycap.txt","b8de5c46eae0dd85a78a684a9f448265b2610c0d","B8DE5C46EAE0DD85A78A684A9F448265B2610C0D","","564","2020-Oct-14","11:23:30","2020-Oct-14","11:23:30","combining-keycap.txt",".txt"
"test-case","C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\digraphs.txt","aea64a423d298105a47d7a2de5795347efc086c6","AEA64A423D298105A47D7A2DE5795347EFC086C6","","664","2020-Oct-14","11:23:47","2020-Oct-14","11:23:48","digraphs.txt",".txt"
"test-case","C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\grid-capital.txt","","","big-file-skipped > 1024 bytes","2308","2020-Oct-14","11:23:57","2020-Oct-14","11:23:57","grid-capital.txt",".txt"
"test-case","C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\grid-cyrillic-1.txt","","","big-file-skipped > 1024 bytes","2197","2020-Oct-14","11:24:10","2020-Oct-14","11:24:10","grid-cyrillic-1.txt",".txt"
"test-case","C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\grid-cyrillic-2.txt","","","big-file-skipped > 1024 bytes","2248","2020-Oct-14","11:24:40","2020-Oct-14","11:24:41","grid-cyrillic-2.txt",".txt"
"test-case","C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\grid-greek-1.txt","","","big-file-skipped > 1024 bytes","1056","2020-Oct-14","11:25:10","2020-Oct-14","11:25:10","grid-greek-1.txt",".txt"
"test-case","C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\grid-greek-2.txt","","","big-file-skipped > 1024 bytes","1047","2020-Oct-14","11:25:17","2020-Oct-14","11:25:17","grid-greek-2.txt",".txt"
"test-case","C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\grid-mixed-1.txt","","","big-file-skipped > 1024 bytes","5671","2020-Oct-14","11:25:23","2020-Oct-14","11:25:23","grid-mixed-1.txt",".txt"
"test-case","C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\grid-mixed-2.txt","","","big-file-skipped > 1024 bytes","5647","2020-Oct-14","11:25:39","2020-Oct-14","11:25:39","grid-mixed-2.txt",".txt"
"test-case","C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\grid-small.txt","","","big-file-skipped > 1024 bytes","2333","2020-Oct-14","11:25:45","2020-Oct-14","11:25:45","grid-small.txt",".txt"
"test-case","C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\Index of _~mgk25_ucs_examples.html","","","big-file-skipped > 1024 bytes","5143","2020-Oct-14","11:27:54","2020-Oct-14","11:27:55","Index of _~mgk25_ucs_examples.html",".html"
"test-case","C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\ipa-chart.txt","","","big-file-skipped > 1024 bytes","2202","2020-Oct-14","11:25:58","2020-Oct-14","11:26:05","ipa-chart.txt",".txt"
"test-case","C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\ipa-english.txt","","","big-file-skipped > 1024 bytes","1875","2020-Oct-14","11:27:46","2020-Oct-14","11:27:46","ipa-english.txt",".txt"
"test-case","C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\luki2.txt","","","big-file-skipped > 1024 bytes","11829","2020-Oct-14","11:28:08","2020-Oct-14","11:28:09","luki2.txt",".txt"
"test-case","C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\lyrics-ipa.txt","","","big-file-skipped > 1024 bytes","2440","2020-Oct-14","11:28:13","2020-Oct-14","11:28:14","lyrics-ipa.txt",".txt"
"test-case","C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\postscript-utf-8.txt","","","big-file-skipped > 1024 bytes","10149","2020-Oct-14","11:22:41","2020-Oct-14","11:22:41","postscript-utf-8.txt",".txt"
"test-case","C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\quickbrown.txt","","","big-file-skipped > 1024 bytes","4833","2020-Oct-14","11:28:39","2020-Oct-14","11:28:40","quickbrown.txt",".txt"
"test-case","C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\revelation.txt","","","big-file-skipped > 1024 bytes","116240","2020-Oct-14","11:28:46","2020-Oct-14","11:28:47","revelation.txt",".txt"
"test-case","C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\rune-poem.txt","","","big-file-skipped > 1024 bytes","2828","2020-Oct-14","11:28:51","2020-Oct-14","11:28:51","rune-poem.txt",".txt"
"test-case","C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\TeX.txt","","","big-file-skipped > 1024 bytes","4901","2020-Oct-14","11:22:50","2020-Oct-14","11:22:51","TeX.txt",".txt"
"test-case","C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\UTF-8-demo.txt","","","big-file-skipped > 1024 bytes","14058","2020-Oct-14","11:22:59","2020-Oct-14","11:22:59","UTF-8-demo.txt",".txt"
"test-case","C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\UTF-8-test.txt","","","big-file-skipped > 1024 bytes","22781","2020-Oct-14","11:23:21","2020-Oct-14","11:23:21","UTF-8-test.txt",".txt"
"test-case","C:\Users\a\Documents\vss\python-experiments\test-files\test-folder\New Bitmap ImageFFF.bmp","da39a3ee5e6b4b0d3255bfef95601890afd80709","DA39A3EE5E6B4B0D3255BFEF95601890AFD80709","zero-bytes-file","0","2020-Aug-14","16:01:42","2020-Aug-14","16:01:42","New Bitmap ImageFFF.bmp",".bmp"
"test-case","C:\Users\a\Documents\vss\python-experiments\test-files\test-folder\New Microsoft Excel Worksheet.xlsx","","","big-file-skipped > 1024 bytes","5770","2020-Aug-14","15:55:18","2020-Aug-14","15:55:18","New Microsoft Excel Worksheet.xlsx",".xlsx"
"test-case","C:\Users\a\Documents\vss\python-experiments\test-files\test-folder\New Text Document.txt - Shortcut.lnk","","","big-file-skipped > 1024 bytes","2040","2020-Oct-14","19:11:00","2020-Oct-14","19:11:00","New Text Document.txt - Shortcut.lnk",".lnk"
"test-case","C:\Users\a\Documents\vss\python-experiments\test-files\test-folder\꧇꧑꧑꧇ .txt","ea94127443006cf237327df1ac6a055e93de3bd8","EA94127443006CF237327DF1AC6A055E93DE3BD8","","74","2020-Oct-14","11:41:04","2020-Oct-14","11:55:15","꧇꧑꧑꧇ .txt",".txt"
"test-case","C:\Users\a\Documents\vss\python-experiments\test-files\test-folder\New folder 2\New Rich Text Document 3 deep.rtf","2201589aa3ed709b3665e4ff979e10c6ad5137fc","2201589AA3ED709B3665E4FF979E10C6AD5137FC","","7","2020-Aug-14","16:13:25","2020-Aug-14","16:13:25","New Rich Text Document 3 deep.rtf",".rtf"
"""
