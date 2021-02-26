import pathlib
from typing import List

from app.file_hash import get_sha1_hash, get_file_list, get_file_size, save_dict_as_csv, main, _report_header

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


def test_create_file(tmpdir):
    p = tmpdir.mkdir("sub").join("hello.txt")
    p.write("content")
    assert p.read() == "content"
    assert len(tmpdir.listdir()) == 1


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
    ideal_answer = r""""file-path","sha-1","error","size"
"C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\grid-cyrillic-1.txt","abcdefg","no error here","9"
"C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\grid-cyrillic-2.txt","1234567890","no error here or here","10"
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
    assert result_file == r""""file-path","sha-1","error","size"
"C:\Users\a\Documents\vss\python-experiments\test-files\kanji-教育漢字","","big-file-skipped > 1024 bytes","21864"
"C:\Users\a\Documents\vss\python-experiments\test-files\new 1.txt","","big-file-skipped > 1024 bytes","735085"
"C:\Users\a\Documents\vss\python-experiments\test-files\New Microsoft Word Document.docx","da39a3ee5e6b4b0d3255bfef95601890afd80709","","0"
"C:\Users\a\Documents\vss\python-experiments\test-files\New Text Document (2).txt","","big-file-skipped > 1024 bytes","147016"
"C:\Users\a\Documents\vss\python-experiments\test-files\New Text Document.txt","da39a3ee5e6b4b0d3255bfef95601890afd80709","","0"
"C:\Users\a\Documents\vss\python-experiments\test-files\UTF-16 encoding files-utf16","5403728097d5bbd5a0c37d4ac88512b3e7a01c8a","","152"
"C:\Users\a\Documents\vss\python-experiments\test-files\永 - Wiktionary.URL","c7b81a227cd313feef0b792a252e63ba1fc62d2c","","221"
"C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\combining-keycap.txt","b8de5c46eae0dd85a78a684a9f448265b2610c0d","","564"
"C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\digraphs.txt","aea64a423d298105a47d7a2de5795347efc086c6","","664"
"C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\grid-capital.txt","","big-file-skipped > 1024 bytes","2308"
"C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\grid-cyrillic-1.txt","","big-file-skipped > 1024 bytes","2197"
"C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\grid-cyrillic-2.txt","","big-file-skipped > 1024 bytes","2248"
"C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\grid-greek-1.txt","","big-file-skipped > 1024 bytes","1056"
"C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\grid-greek-2.txt","","big-file-skipped > 1024 bytes","1047"
"C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\grid-mixed-1.txt","","big-file-skipped > 1024 bytes","5671"
"C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\grid-mixed-2.txt","","big-file-skipped > 1024 bytes","5647"
"C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\grid-small.txt","","big-file-skipped > 1024 bytes","2333"
"C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\Index of _~mgk25_ucs_examples.html","","big-file-skipped > 1024 bytes","5143"
"C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\ipa-chart.txt","","big-file-skipped > 1024 bytes","2202"
"C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\ipa-english.txt","","big-file-skipped > 1024 bytes","1875"
"C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\luki2.txt","","big-file-skipped > 1024 bytes","11829"
"C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\lyrics-ipa.txt","","big-file-skipped > 1024 bytes","2440"
"C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\postscript-utf-8.txt","","big-file-skipped > 1024 bytes","10149"
"C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\quickbrown.txt","","big-file-skipped > 1024 bytes","4833"
"C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\revelation.txt","","big-file-skipped > 1024 bytes","116240"
"C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\rune-poem.txt","","big-file-skipped > 1024 bytes","2828"
"C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\TeX.txt","","big-file-skipped > 1024 bytes","4901"
"C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\UTF-8-demo.txt","","big-file-skipped > 1024 bytes","14058"
"C:\Users\a\Documents\vss\python-experiments\test-files\cam.ac~mgk25\UTF-8-test.txt","","big-file-skipped > 1024 bytes","22781"
"C:\Users\a\Documents\vss\python-experiments\test-files\test-folder\New Bitmap ImageFFF.bmp","da39a3ee5e6b4b0d3255bfef95601890afd80709","","0"
"C:\Users\a\Documents\vss\python-experiments\test-files\test-folder\New Microsoft Excel Worksheet.xlsx","","big-file-skipped > 1024 bytes","5770"
"C:\Users\a\Documents\vss\python-experiments\test-files\test-folder\New Text Document.txt - Shortcut.lnk","","big-file-skipped > 1024 bytes","2040"
"C:\Users\a\Documents\vss\python-experiments\test-files\test-folder\꧇꧑꧑꧇ .txt","ea94127443006cf237327df1ac6a055e93de3bd8","","74"
"C:\Users\a\Documents\vss\python-experiments\test-files\test-folder\New folder 2\New Rich Text Document 3 deep.rtf","2201589aa3ed709b3665e4ff979e10c6ad5137fc","","7"
"""
