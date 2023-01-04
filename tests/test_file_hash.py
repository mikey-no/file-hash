import csv
import pathlib
from datetime import datetime, timedelta
from typing import List

import pytest

from app.hash_file import (
    get_file_list,
    get_file_size,
    get_file_extension,
    get_file_modified,
    get_file_name,
    get_date,
    get_time,
    get_sha1_hash,
    main,
    A_KB,
    _csv_report_header_simple_,
    _csv_report_header_,
    get_relative_path,
)

test_files_root = pathlib.Path().cwd().parent.parent / f"test-files/001"

test_file_list_str = [
    "C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\001\\kanji-教育漢字",
    "C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\001\\new 1.txt",
    "C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\001\\New Microsoft Word Document.docx",
    "C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\001\\New Text Document (2).txt",
    "C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\001\\New Text Document.txt",
    "C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\001\\UTF-16 encoding files-utf16",
    "C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\001\\永 - Wiktionary.URL",
    "C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\001\\cam.ac~mgk25\\combining-keycap.txt",
    "C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\001\\cam.ac~mgk25\\digraphs.txt",
    "C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\001\\cam.ac~mgk25\\grid-capital.txt",
    "C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\001\\cam.ac~mgk25\\grid-cyrillic-1.txt",
    "C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\001\\cam.ac~mgk25\\grid-cyrillic-2.txt",
    "C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\001\\cam.ac~mgk25\\grid-greek-1.txt",
    "C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\001\\cam.ac~mgk25\\grid-greek-2.txt",
    "C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\001\\cam.ac~mgk25\\grid-mixed-1.txt",
    "C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\001\\cam.ac~mgk25\\grid-mixed-2.txt",
    "C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\001\\cam.ac~mgk25\\grid-small.txt",
    "C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\001\\cam.ac~mgk25\\Index of _~mgk25_ucs_examples.html",
    "C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\001\\cam.ac~mgk25\\ipa-chart.txt",
    "C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\001\\cam.ac~mgk25\\ipa-english.txt",
    "C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\001\\cam.ac~mgk25\\luki2.txt",
    "C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\001\\cam.ac~mgk25\\lyrics-ipa.txt",
    "C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\001\\cam.ac~mgk25\\postscript-utf-8.txt",
    "C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\001\\cam.ac~mgk25\\quickbrown.txt",
    "C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\001\\cam.ac~mgk25\\revelation.txt",
    "C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\001\\cam.ac~mgk25\\rune-poem.txt",
    "C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\001\\cam.ac~mgk25\\TeX.txt",
    "C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\001\\cam.ac~mgk25\\UTF-8-demo.txt",
    "C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\001\\cam.ac~mgk25\\UTF-8-test.txt",
    "C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\001\\test-folder\\New Bitmap ImageFFF.bmp",
    "C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\001\\test-folder\\New Microsoft Excel Worksheet.xlsx",
    "C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\001\\test-folder\\New Text Document.txt - Shortcut.lnk",
    "C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\001\\test-folder\\꧇꧑꧑꧇ .txt",
    "C:\\Users\\a\\Documents\\vss\\python-experiments\\test-files\\001\\test-folder\\New folder 2\\New Rich Text Document 3 deep.rtf",
]


def test_create_file(tmpdir):
    p = tmpdir.mkdir("sub").join("hello.txt")
    p.write("content")
    assert p.read() == "content"
    assert len(tmpdir.listdir()) == 1


def test_get_file(tmpdir):
    p = tmpdir.mkdir("sub").join("hello.txt")
    content = "conticontinet big snake"
    p.write(content)
    assert p.read() == content
    assert len(tmpdir.listdir()) == 1
    assert get_file_size(pathlib.Path(p)) == len(content)


def test_get_file_created_length(tmpdir):
    p = tmpdir.mkdir("sub").join("hello.txt")
    content = "conticontinet big snake"
    p.write(content)
    assert p.read() == content
    assert len(tmpdir.listdir()) == 1
    assert get_file_size(pathlib.Path(p)) == len(content)


def test_get_file_created(tmpdir):
    now = datetime.now()
    p = tmpdir.mkdir("sub").join("hello.txt")
    content = "conticontinet big snake"
    p.write(content)
    assert p.read() == content
    assert len(tmpdir.listdir()) == 1
    assert get_file_size(pathlib.Path(p)) == len(content)
    td = timedelta(milliseconds=300)  # give it a generous 300 ms to do this
    response = get_file_modified(pathlib.Path(p))
    if response == now or response <= now + td:
        assert True
    else:
        assert False


def test_get_time():
    date_time_str1 = "2018-06-29 08:15:27.243860"
    date_time_obj1 = datetime.strptime(date_time_str1, "%Y-%m-%d %H:%M:%S.%f")
    date_time_obj1_check = date_time_obj1.strftime("%H:%M:%S%z")
    date_time_str2 = "2021-Feb-28 16:23:56.555666+0400"
    date_time_obj2 = datetime.strptime(date_time_str2, "%Y-%b-%d %H:%M:%S.%f%z")
    date_time_obj2_check = date_time_obj2.strftime("%H:%M:%S%z")
    assert isinstance(date_time_obj1, datetime)
    assert isinstance(date_time_obj2, datetime)
    assert str(get_time(date_time_obj1)) == date_time_obj1_check
    assert str(get_time(date_time_obj2)) == date_time_obj2_check


def test_get_date():
    date_time_str1 = "2018-06-29 08:15:27.243860"
    date_time_obj1 = datetime.strptime(date_time_str1, "%Y-%m-%d %H:%M:%S.%f")
    date_time_obj1_check = date_time_obj1.strftime("%Y-%b-%d")
    date_time_str2 = "2021-Feb-28 16:23:56.555666+0400"
    date_time_obj2 = datetime.strptime(date_time_str2, "%Y-%b-%d %H:%M:%S.%f%z")
    date_time_obj2_check = date_time_obj2.strftime("%Y-%b-%d")
    assert isinstance(date_time_obj1, datetime)
    assert isinstance(date_time_obj2, datetime)
    assert str(get_date(date_time_obj1)) == date_time_obj1_check
    assert str(get_date(date_time_obj2)) == date_time_obj2_check


def test_get_file_extension(tmpdir):
    p = tmpdir.mkdir("sub").join("hello.txt")
    content = "continent big snake"
    p.write(content)
    assert p.read() == content
    assert len(tmpdir.listdir()) == 1
    assert get_file_size(pathlib.Path(p)) == len(content)
    assert get_file_extension(pathlib.Path(p)) == ".txt"


# sha-1 values from 7zip
@pytest.mark.parametrize(
    "file,ref_hash",
    [
        (rf"kanji-教育漢字", "01e6e9a522a8e3c28c5d65cfd9ec6a5ce026ada0"),
        (rf"new 1.txt", "3cb40aaa24287e4b20f199665f2badf967663935"),
        (rf"New Text Document (2).txt", "fd35d41bebe60ce3bddf7c3e747e6027a811281d"),
        (rf"UTF-16 encoding files-utf16", "5403728097d5bbd5a0c37d4ac88512b3e7a01c8a"),
        (
                rf"test-folder/New Microsoft Excel Worksheet.xlsx",
                "312122090d3e0ce7b2e9bf1739d82de763049e25",
        ),
        (
                rf"test-folder/New Bitmap ImageFFF.bmp",
                "da39a3ee5e6b4b0d3255bfef95601890afd80709",
        ),
        (
                rf"test-folder/New folder 2/New Rich Text Document 3 deep.rtf",
                "74d80438491c0a5ae9ea667b681c8619889ed549",
        ),
    ],
)
def test_get_sha1_hash(file, ref_hash):
    file = test_files_root / file
    # file =  / file
    assert file.exists()
    test_hash = get_sha1_hash(pathlib.Path(file))
    assert ref_hash.upper() == test_hash.upper()


def test_get_file_name(tmpdir):
    name = "ᚢᚱ᛫ᛒᛦᚦ᛫ᚪᚾᛗᚩᛞ᛫ᚩᚾᛞ᛫ᚩᚠᛖᚱᚻᛦᚱᚾᛖᛞ"
    p = tmpdir.mkdir("sub").join(name)
    content = "conticontinet big snake = with unicode stuff in the name"
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
    assert (
            result == "040F06FD774092478D450774F5BA30C5DA78ACC8".lower()
    )  # confirmed with 7zip


def test_files_exist():
    assert pathlib.Path(test_files_root).exists()


def test_file_list():
    location = pathlib.Path(test_files_root).resolve()
    assert pathlib.Path(location).exists()
    result_list_old = get_file_list(location)
    result_list_new = []
    for file in result_list_old:
        result_list_new.append(file)

    assert len(result_list_new) == 34  # test confirmed with os
    # convert result_list to list of strings called result_list_str
    result_list_str: List[str] = []
    for file in result_list_new:
        f = str(file)
        result_list_str.append(f)

    assert result_list_str == test_file_list_str


def test_get_file_size():
    """TODO: make this test not depend on the test files"""
    file = pathlib.Path(test_files_root) / rf"cam.ac~mgk25\grid-cyrillic-1.txt"
    assert get_file_size(file) == 2197  # test confirmed with os


def test_get_relative_path(tmp_path):
    p1 = tmp_path / "sub" / "hello.txt"
    p2 = tmp_path / "sub" / "sub" / "hello.txt"
    p_as_file = tmp_path / "sub" / "hello.txt"

    result1 = get_relative_path(p1, scan_location=tmp_path)
    result2 = get_relative_path(p2, scan_location=tmp_path)
    result3 = get_relative_path(p_as_file, scan_location=p_as_file)
    # assuming Windows path separator
    assert str(result1) == rf"sub\hello.txt"
    assert str(result2) == rf"sub\sub\hello.txt"
    assert result3 == None

    rf"""

    Exception: 
    'C:\\Users\\a\\AppData\\Local\\Temp\\pytest-of-a\\pytest-396\\test_get_relative_path0\\sub' is not in the subpath of 
    'C:\\Users\\a\\AppData\\Local\\Temp\\pytest-of-a\\pytest-396\\test_get_relative_path0\\sub\\hello.txt' OR one path is relative and the other is absolute. - 
    C:\Users\a\AppData\Local\Temp\pytest-of-a\pytest-396\test_get_relative_path0\sub\hello.txt - 
    C:\Users\a\AppData\Local\Temp\pytest-of-a\pytest-396\test_get_relative_path0\sub\hello.txt

    """


@pytest.mark.parametrize(
    "file_str,scan_location, ref_result",
    [
        ("c:\sub\hello.txt", "c:\sub", "hello.txt"),
        ("sub/sub/hello.txt", "./sub", "sub\\hello.txt"),
        (
                pathlib.Path(
                    test_files_root
                    / rf"vss\python-experiments\test-files\001\cam.ac~mgk25\grid-cyrillic-2.txt"
                ),
                test_files_root,
                "vss\\python-experiments\\test-files\\001\\cam.ac~mgk25\\grid-cyrillic-2.txt",
        ),
        ("sub/sub/hello.txt", "sub/sub/hello.txt", str(None)),
        ("hello.txt", "hello.txt", str(None)),
        ("hello", "hello", str(None)),
        (
                pathlib.Path(test_files_root) / "New Microsoft Word Document.docx",
                test_files_root,
                "New Microsoft Word Document.docx",
        ),
        (
                pathlib.Path(test_files_root) / "sub" / "New Microsoft Word Document.docx",
                test_files_root,
                "sub\\New Microsoft Word Document.docx",
        ),
    ],
)
def test_get_relative_path_parameterised(file_str, scan_location, ref_result, tmp_path):
    if scan_location is None:
        scan_location = tmp_path

    # p = scan_location / pathlib.Path(file_str)
    result = get_relative_path(pathlib.Path(file_str), scan_location=scan_location)

    # assuming Windows path separator
    assert str(result) == ref_result


def test_main_simple_output(tmp_path):
    ref_result = rf"""""case-label","relative-path","sha1","hash-error","size","created","modified","file-name","file-extension"
"case1-mongoose","cam.ac~mgk25\grid-cyrillic-2.txt","0bbd4426d4c7277a4c73c25a7ac921950e35383c","","2248","2022-Apr-18 19:41:33","2020-Oct-14 11:24:41","grid-cyrillic-2.txt",".txt"
"case1-mongoose","cam.ac~mgk25\UTF-8-test.txt","","file size, 22781 > 10240, hash skipped","22781","2022-Apr-18 19:41:33","2020-Oct-14 11:23:21","UTF-8-test.txt",".txt"
"case1-mongoose","New Text Document.txt","da39a3ee5e6b4b0d3255bfef95601890afd80709","file size is 0 bytes","0","2022-Apr-18 19:41:33","2020-Aug-14 15:55:13","New Text Document.txt",".txt"
"case1-mongoose","cam.ac~mgk25\grid-cyrillic-1.txt","f190091536bbbc9f3221cc69d04aecbaca3d818b","","2197","2022-Apr-18 19:41:33","2020-Oct-14 11:24:10","grid-cyrillic-1.txt",".txt"
"case1-mongoose","cam.ac~mgk25\UTF-8-demo.txt","","file size, 14058 > 10240, hash skipped","14058","2022-Apr-18 19:41:33","2020-Oct-14 11:22:59","UTF-8-demo.txt",".txt"
"case1-mongoose","cam.ac~mgk25\ipa-chart.txt","56d1be5fa32d53ce08586420b00fb5a30473df42","","2202","2022-Apr-18 19:41:33","2020-Oct-14 11:26:05","ipa-chart.txt",".txt"
"case1-mongoose","cam.ac~mgk25\grid-capital.txt","c36e46008d994b89bdde3a3dc025c49ffdd7e019","","2308","2022-Apr-18 19:41:33","2020-Oct-14 11:23:57","grid-capital.txt",".txt"
"case1-mongoose","New Text Document (2).txt","","file size, 147016 > 10240, hash skipped","147016","2022-Apr-18 19:41:33","2020-Oct-13 21:19:27","New Text Document (2).txt",".txt"
"case1-mongoose","cam.ac~mgk25\TeX.txt","09f7d7797a45bae9454a6e0bf197db04c68c909a","","4901","2022-Apr-18 19:41:33","2020-Oct-14 11:22:51","TeX.txt",".txt"
"case1-mongoose","cam.ac~mgk25\Index of _~mgk25_ucs_examples.html","9b24aced80b12b07b5e08e7b4c406b7a7c8d1536","","5143","2022-Apr-18 19:41:33","2020-Oct-14 11:27:55","Index of _~mgk25_ucs_examples.html",".html"
"case1-mongoose","test-folder\New folder 2\New Rich Text Document 3 deep.rtf","","file size, 18807 > 10240, hash skipped","18807","2022-Apr-18 19:41:33","2021-May-19 21:31:11","New Rich Text Document 3 deep.rtf",".rtf"
"case1-mongoose","cam.ac~mgk25\digraphs.txt","aea64a423d298105a47d7a2de5795347efc086c6","","664","2022-Apr-18 19:41:33","2020-Oct-14 11:23:48","digraphs.txt",".txt"
"case1-mongoose","cam.ac~mgk25\rune-poem.txt","4125a18fd2e350a523f339def7af3c7639c060fa","","2828","2022-Apr-18 19:41:33","2020-Oct-14 11:28:51","rune-poem.txt",".txt"
"case1-mongoose","cam.ac~mgk25\grid-small.txt","08eb3b0434ff1fd74b7446951f4fb00c9b7821cb","","2333","2022-Apr-18 19:41:33","2020-Oct-14 11:25:45","grid-small.txt",".txt"
"case1-mongoose","cam.ac~mgk25\combining-keycap.txt","b8de5c46eae0dd85a78a684a9f448265b2610c0d","","564","2022-Apr-18 19:41:33","2020-Oct-14 11:23:30","combining-keycap.txt",".txt"
"case1-mongoose","cam.ac~mgk25\revelation.txt","","file size, 116240 > 10240, hash skipped","116240","2022-Apr-18 19:41:33","2020-Oct-14 11:28:47","revelation.txt",".txt"
"case1-mongoose","cam.ac~mgk25\grid-mixed-2.txt","b4bcef4cc28b34163dd98a49c396a2cf62df467c","","5647","2022-Apr-18 19:41:33","2020-Oct-14 11:25:39","grid-mixed-2.txt",".txt"
"case1-mongoose","test-folder\꧇꧑꧑꧇ .txt","ea94127443006cf237327df1ac6a055e93de3bd8","","74","2022-Apr-18 19:41:33","2020-Oct-14 11:55:15","꧇꧑꧑꧇ .txt",".txt"
"case1-mongoose","New Microsoft Word Document.docx","da39a3ee5e6b4b0d3255bfef95601890afd80709","file size is 0 bytes","0","2022-Apr-18 19:41:33","2020-Aug-14 15:55:08","New Microsoft Word Document.docx",".docx"
"case1-mongoose","cam.ac~mgk25\quickbrown.txt","4c76f59076fe6db52d5f5d7e47deea0f172da496","","4833","2022-Apr-18 19:41:33","2020-Oct-14 11:28:40","quickbrown.txt",".txt"
"case1-mongoose","cam.ac~mgk25\grid-mixed-1.txt","250ef3d6a87f44974e996a1873c02f2142295053","","5671","2022-Apr-18 19:41:33","2020-Oct-14 11:25:23","grid-mixed-1.txt",".txt"
"case1-mongoose","test-folder\New Text Document.txt - Shortcut.lnk","481e885df1e94ef627e35d2ac943b255c7447f3f","","2040","2022-Apr-18 19:41:33","2020-Oct-14 19:11:00","New Text Document.txt - Shortcut.lnk",".lnk"
"case1-mongoose","cam.ac~mgk25\ipa-english.txt","9d80225c67ffec7b245ad0411905a29c59bf4ed1","","1875","2022-Apr-18 19:41:33","2020-Oct-14 11:27:46","ipa-english.txt",".txt"
"case1-mongoose","cam.ac~mgk25\postscript-utf-8.txt","5649e6d772857a265c471febc6badd67f612a10f","","10149","2022-Apr-18 19:41:33","2020-Oct-14 11:22:41","postscript-utf-8.txt",".txt"
"case1-mongoose","cam.ac~mgk25\grid-greek-2.txt","a2cfe98d9f09b11bd066dac2d4b5df54b27d5177","","1047","2022-Apr-18 19:41:33","2020-Oct-14 11:25:17","grid-greek-2.txt",".txt"
"case1-mongoose","永 - Wiktionary.URL","c7b81a227cd313feef0b792a252e63ba1fc62d2c","","221","2022-Apr-18 19:41:33","2020-Nov-05 15:21:00","永 - Wiktionary.URL",".URL"
"case1-mongoose","test-folder\New Microsoft Excel Worksheet.xlsx","312122090d3e0ce7b2e9bf1739d82de763049e25","","5770","2022-Apr-18 19:41:33","2020-Aug-14 15:55:18","New Microsoft Excel Worksheet.xlsx",".xlsx"
"case1-mongoose","cam.ac~mgk25\lyrics-ipa.txt","4c35a3e3da348219691477ab6b5750c8fdb1ed40","","2440","2022-Apr-18 19:41:33","2020-Oct-14 11:28:14","lyrics-ipa.txt",".txt"
"case1-mongoose","new 1.txt","","file size, 735085 > 10240, hash skipped","735085","2022-Apr-18 19:41:33","2020-Oct-13 21:20:58","new 1.txt",".txt"
"case1-mongoose","cam.ac~mgk25\grid-greek-1.txt","e5759b9bb72100b9c7e1eb805d62ffbfc2b353d0","","1056","2022-Apr-18 19:41:33","2020-Oct-14 11:25:10","grid-greek-1.txt",".txt"
"case1-mongoose","UTF-16 encoding files-utf16","5403728097d5bbd5a0c37d4ac88512b3e7a01c8a","","152","2022-Apr-18 19:41:33","2020-Oct-14 10:43:20","UTF-16 encoding files-utf16",""
"case1-mongoose","kanji-教育漢字","","file size, 21864 > 10240, hash skipped","21864","2022-Apr-18 19:41:33","2020-Oct-14 20:34:47","kanji-教育漢字",""
"case1-mongoose","test-folder\New Bitmap ImageFFF.bmp","da39a3ee5e6b4b0d3255bfef95601890afd80709","file size is 0 bytes","0","2022-Apr-18 19:41:33","2020-Aug-14 16:01:42","New Bitmap ImageFFF.bmp",".bmp"
"case1-mongoose","cam.ac~mgk25\luki2.txt","","file size, 11829 > 10240, hash skipped","11829","2022-Apr-18 19:41:33","2020-Oct-14 11:28:09","luki2.txt",".txt"
"""
    a_report_file_in = tmp_path / "a_report.csv"
    a_case_label_in = "case1-mongoose"
    a_simple_output = True
    a_max_hash_size = A_KB * 10
    report_file = main(
        pathlib.Path(test_files_root),
        a_report_file_in,
        a_case_label_in,
        simple_output=a_simple_output,
        first_n_files=None,
        cores=2,
        max_hash_size=a_max_hash_size,
    )
    assert report_file.exists
    assert report_file == a_report_file_in
    # need to open this as a csv dict!!
    with open(a_report_file_in, "r", encoding="utf-8") as fin:
        test_data = fin.read()

    # arrange
    # first need to write ref results to a file, so we can use csv.DictReader to read it in as a list[dict]
    ref_result_file = tmp_path / "ref_results.csv"
    with open(ref_result_file, "w", encoding="utf-8") as fout_ref:
        fout_ref.write(ref_result)

    ref_result_list = []
    with open(ref_result_file, "r", encoding="utf-8") as fin_ref:
        fin_ref.readline()  # skip the first line header
        ref_result_dict_reader = csv.DictReader(
            fin_ref,
            fieldnames=_csv_report_header_simple_,
            quoting=csv.QUOTE_ALL,
            lineterminator="\n",
        )

        for row in ref_result_dict_reader:
            ref_result_list.append(row)

    ref_result_list_sorted = sorted(ref_result_list, key=lambda d: d["relative-path"])

    # get the test results sorted in the same way
    result_list = []
    with open(report_file, "r", encoding="utf-8") as fin:
        fin.readline()  # skip the first line header
        result_dict_reader = csv.DictReader(
            fin,
            fieldnames=_csv_report_header_simple_,
            quoting=csv.QUOTE_ALL,
            lineterminator="\n",
        )

        for row in result_dict_reader:
            result_list.append(row)

    result_list_sorted = sorted(result_list, key=lambda d: d["relative-path"])

    assert result_list_sorted == ref_result_list_sorted


def test_main(tmp_path):
    """updated output format but with all the extra fields"""
    ref_result = rf""""case-label","path","sha-1","sha-1-uc","hash-error","size","created","created-time","modified","modified-time","file-name","file-extension"
"case1-mongoose","C:\Users\a\Documents\vss\python-experiments\test-files\001\kanji-教育漢字","","","file size, 21864 > 10240, hash skipped","21864","2022-Apr-18","19:41:33","2020-Oct-14","20:34:47","kanji-教育漢字",""
"case1-mongoose","C:\Users\a\Documents\vss\python-experiments\test-files\001\new 1.txt","","","file size, 735085 > 10240, hash skipped","735085","2022-Apr-18","19:41:33","2020-Oct-13","21:20:58","new 1.txt",".txt"
"case1-mongoose","C:\Users\a\Documents\vss\python-experiments\test-files\001\test-folder\New Bitmap ImageFFF.bmp","da39a3ee5e6b4b0d3255bfef95601890afd80709","DA39A3EE5E6B4B0D3255BFEF95601890AFD80709","file size is 0 bytes","0","2022-Apr-18","19:41:33","2020-Aug-14","16:01:42","New Bitmap ImageFFF.bmp",".bmp"
"case1-mongoose","C:\Users\a\Documents\vss\python-experiments\test-files\001\cam.ac~mgk25\luki2.txt","","","file size, 11829 > 10240, hash skipped","11829","2022-Apr-18","19:41:33","2020-Oct-14","11:28:09","luki2.txt",".txt"
"case1-mongoose","C:\Users\a\Documents\vss\python-experiments\test-files\001\cam.ac~mgk25\grid-cyrillic-2.txt","0bbd4426d4c7277a4c73c25a7ac921950e35383c","0BBD4426D4C7277A4C73C25A7AC921950E35383C","","2248","2022-Apr-18","19:41:33","2020-Oct-14","11:24:41","grid-cyrillic-2.txt",".txt"
"case1-mongoose","C:\Users\a\Documents\vss\python-experiments\test-files\001\cam.ac~mgk25\UTF-8-test.txt","","","file size, 22781 > 10240, hash skipped","22781","2022-Apr-18","19:41:33","2020-Oct-14","11:23:21","UTF-8-test.txt",".txt"
"case1-mongoose","C:\Users\a\Documents\vss\python-experiments\test-files\001\New Text Document.txt","da39a3ee5e6b4b0d3255bfef95601890afd80709","DA39A3EE5E6B4B0D3255BFEF95601890AFD80709","file size is 0 bytes","0","2022-Apr-18","19:41:33","2020-Aug-14","15:55:13","New Text Document.txt",".txt"
"case1-mongoose","C:\Users\a\Documents\vss\python-experiments\test-files\001\cam.ac~mgk25\ipa-english.txt","9d80225c67ffec7b245ad0411905a29c59bf4ed1","9D80225C67FFEC7B245AD0411905A29C59BF4ED1","","1875","2022-Apr-18","19:41:33","2020-Oct-14","11:27:46","ipa-english.txt",".txt"
"case1-mongoose","C:\Users\a\Documents\vss\python-experiments\test-files\001\cam.ac~mgk25\grid-cyrillic-1.txt","f190091536bbbc9f3221cc69d04aecbaca3d818b","F190091536BBBC9F3221CC69D04AECBACA3D818B","","2197","2022-Apr-18","19:41:33","2020-Oct-14","11:24:10","grid-cyrillic-1.txt",".txt"
"case1-mongoose","C:\Users\a\Documents\vss\python-experiments\test-files\001\UTF-16 encoding files-utf16","5403728097d5bbd5a0c37d4ac88512b3e7a01c8a","5403728097D5BBD5A0C37D4AC88512B3E7A01C8A","","152","2022-Apr-18","19:41:33","2020-Oct-14","10:43:20","UTF-16 encoding files-utf16",""
"case1-mongoose","C:\Users\a\Documents\vss\python-experiments\test-files\001\cam.ac~mgk25\UTF-8-demo.txt","","","file size, 14058 > 10240, hash skipped","14058","2022-Apr-18","19:41:33","2020-Oct-14","11:22:59","UTF-8-demo.txt",".txt"
"case1-mongoose","C:\Users\a\Documents\vss\python-experiments\test-files\001\cam.ac~mgk25\ipa-chart.txt","56d1be5fa32d53ce08586420b00fb5a30473df42","56D1BE5FA32D53CE08586420B00FB5A30473DF42","","2202","2022-Apr-18","19:41:33","2020-Oct-14","11:26:05","ipa-chart.txt",".txt"
"case1-mongoose","C:\Users\a\Documents\vss\python-experiments\test-files\001\cam.ac~mgk25\grid-capital.txt","c36e46008d994b89bdde3a3dc025c49ffdd7e019","C36E46008D994B89BDDE3A3DC025C49FFDD7E019","","2308","2022-Apr-18","19:41:33","2020-Oct-14","11:23:57","grid-capital.txt",".txt"
"case1-mongoose","C:\Users\a\Documents\vss\python-experiments\test-files\001\cam.ac~mgk25\TeX.txt","09f7d7797a45bae9454a6e0bf197db04c68c909a","09F7D7797A45BAE9454A6E0BF197DB04C68C909A","","4901","2022-Apr-18","19:41:33","2020-Oct-14","11:22:51","TeX.txt",".txt"
"case1-mongoose","C:\Users\a\Documents\vss\python-experiments\test-files\001\New Text Document (2).txt","","","file size, 147016 > 10240, hash skipped","147016","2022-Apr-18","19:41:33","2020-Oct-13","21:19:27","New Text Document (2).txt",".txt"
"case1-mongoose","C:\Users\a\Documents\vss\python-experiments\test-files\001\cam.ac~mgk25\digraphs.txt","aea64a423d298105a47d7a2de5795347efc086c6","AEA64A423D298105A47D7A2DE5795347EFC086C6","","664","2022-Apr-18","19:41:33","2020-Oct-14","11:23:48","digraphs.txt",".txt"
"case1-mongoose","C:\Users\a\Documents\vss\python-experiments\test-files\001\test-folder\New folder 2\New Rich Text Document 3 deep.rtf","","","file size, 18807 > 10240, hash skipped","18807","2022-Apr-18","19:41:33","2021-May-19","21:31:11","New Rich Text Document 3 deep.rtf",".rtf"
"case1-mongoose","C:\Users\a\Documents\vss\python-experiments\test-files\001\cam.ac~mgk25\rune-poem.txt","4125a18fd2e350a523f339def7af3c7639c060fa","4125A18FD2E350A523F339DEF7AF3C7639C060FA","","2828","2022-Apr-18","19:41:33","2020-Oct-14","11:28:51","rune-poem.txt",".txt"
"case1-mongoose","C:\Users\a\Documents\vss\python-experiments\test-files\001\cam.ac~mgk25\Index of _~mgk25_ucs_examples.html","9b24aced80b12b07b5e08e7b4c406b7a7c8d1536","9B24ACED80B12B07B5E08E7B4C406B7A7C8D1536","","5143","2022-Apr-18","19:41:33","2020-Oct-14","11:27:55","Index of _~mgk25_ucs_examples.html",".html"
"case1-mongoose","C:\Users\a\Documents\vss\python-experiments\test-files\001\cam.ac~mgk25\grid-small.txt","08eb3b0434ff1fd74b7446951f4fb00c9b7821cb","08EB3B0434FF1FD74B7446951F4FB00C9B7821CB","","2333","2022-Apr-18","19:41:33","2020-Oct-14","11:25:45","grid-small.txt",".txt"
"case1-mongoose","C:\Users\a\Documents\vss\python-experiments\test-files\001\cam.ac~mgk25\grid-greek-2.txt","a2cfe98d9f09b11bd066dac2d4b5df54b27d5177","A2CFE98D9F09B11BD066DAC2D4B5DF54B27D5177","","1047","2022-Apr-18","19:41:33","2020-Oct-14","11:25:17","grid-greek-2.txt",".txt"
"case1-mongoose","C:\Users\a\Documents\vss\python-experiments\test-files\001\cam.ac~mgk25\combining-keycap.txt","b8de5c46eae0dd85a78a684a9f448265b2610c0d","B8DE5C46EAE0DD85A78A684A9F448265B2610C0D","","564","2022-Apr-18","19:41:33","2020-Oct-14","11:23:30","combining-keycap.txt",".txt"
"case1-mongoose","C:\Users\a\Documents\vss\python-experiments\test-files\001\cam.ac~mgk25\revelation.txt","","","file size, 116240 > 10240, hash skipped","116240","2022-Apr-18","19:41:33","2020-Oct-14","11:28:47","revelation.txt",".txt"
"case1-mongoose","C:\Users\a\Documents\vss\python-experiments\test-files\001\test-folder\꧇꧑꧑꧇ .txt","ea94127443006cf237327df1ac6a055e93de3bd8","EA94127443006CF237327DF1AC6A055E93DE3BD8","","74","2022-Apr-18","19:41:33","2020-Oct-14","11:55:15","꧇꧑꧑꧇ .txt",".txt"
"case1-mongoose","C:\Users\a\Documents\vss\python-experiments\test-files\001\New Microsoft Word Document.docx","da39a3ee5e6b4b0d3255bfef95601890afd80709","DA39A3EE5E6B4B0D3255BFEF95601890AFD80709","file size is 0 bytes","0","2022-Apr-18","19:41:33","2020-Aug-14","15:55:08","New Microsoft Word Document.docx",".docx"
"case1-mongoose","C:\Users\a\Documents\vss\python-experiments\test-files\001\cam.ac~mgk25\quickbrown.txt","4c76f59076fe6db52d5f5d7e47deea0f172da496","4C76F59076FE6DB52D5F5D7E47DEEA0F172DA496","","4833","2022-Apr-18","19:41:33","2020-Oct-14","11:28:40","quickbrown.txt",".txt"
"case1-mongoose","C:\Users\a\Documents\vss\python-experiments\test-files\001\test-folder\New Text Document.txt - Shortcut.lnk","481e885df1e94ef627e35d2ac943b255c7447f3f","481E885DF1E94EF627E35D2AC943B255C7447F3F","","2040","2022-Apr-18","19:41:33","2020-Oct-14","19:11:00","New Text Document.txt - Shortcut.lnk",".lnk"
"case1-mongoose","C:\Users\a\Documents\vss\python-experiments\test-files\001\永 - Wiktionary.URL","c7b81a227cd313feef0b792a252e63ba1fc62d2c","C7B81A227CD313FEEF0B792A252E63BA1FC62D2C","","221","2022-Apr-18","19:41:33","2020-Nov-05","15:21:00","永 - Wiktionary.URL",".URL"
"case1-mongoose","C:\Users\a\Documents\vss\python-experiments\test-files\001\cam.ac~mgk25\grid-mixed-1.txt","250ef3d6a87f44974e996a1873c02f2142295053","250EF3D6A87F44974E996A1873C02F2142295053","","5671","2022-Apr-18","19:41:33","2020-Oct-14","11:25:23","grid-mixed-1.txt",".txt"
"case1-mongoose","C:\Users\a\Documents\vss\python-experiments\test-files\001\cam.ac~mgk25\postscript-utf-8.txt","5649e6d772857a265c471febc6badd67f612a10f","5649E6D772857A265C471FEBC6BADD67F612A10F","","10149","2022-Apr-18","19:41:33","2020-Oct-14","11:22:41","postscript-utf-8.txt",".txt"
"case1-mongoose","C:\Users\a\Documents\vss\python-experiments\test-files\001\test-folder\New Microsoft Excel Worksheet.xlsx","312122090d3e0ce7b2e9bf1739d82de763049e25","312122090D3E0CE7B2E9BF1739D82DE763049E25","","5770","2022-Apr-18","19:41:33","2020-Aug-14","15:55:18","New Microsoft Excel Worksheet.xlsx",".xlsx"
"case1-mongoose","C:\Users\a\Documents\vss\python-experiments\test-files\001\cam.ac~mgk25\grid-mixed-2.txt","b4bcef4cc28b34163dd98a49c396a2cf62df467c","B4BCEF4CC28B34163DD98A49C396A2CF62DF467C","","5647","2022-Apr-18","19:41:33","2020-Oct-14","11:25:39","grid-mixed-2.txt",".txt"
"case1-mongoose","C:\Users\a\Documents\vss\python-experiments\test-files\001\cam.ac~mgk25\lyrics-ipa.txt","4c35a3e3da348219691477ab6b5750c8fdb1ed40","4C35A3E3DA348219691477AB6B5750C8FDB1ED40","","2440","2022-Apr-18","19:41:33","2020-Oct-14","11:28:14","lyrics-ipa.txt",".txt"
"case1-mongoose","C:\Users\a\Documents\vss\python-experiments\test-files\001\cam.ac~mgk25\grid-greek-1.txt","e5759b9bb72100b9c7e1eb805d62ffbfc2b353d0","E5759B9BB72100B9C7E1EB805D62FFBFC2B353D0","","1056","2022-Apr-18","19:41:33","2020-Oct-14","11:25:10","grid-greek-1.txt",".txt"
"""
    a_report_file_in = tmp_path / "a_report.csv"
    a_case_label_in = "case1-mongoose"
    a_simple_output = False
    a_max_hash_size = A_KB * 10
    report_file = main(
        pathlib.Path(test_files_root),
        a_report_file_in,
        a_case_label_in,
        simple_output=a_simple_output,
        first_n_files=None,
        cores=2,
        max_hash_size=a_max_hash_size,
    )
    assert report_file.exists
    assert report_file == a_report_file_in
    # need to open this as a csv dict!!
    with open(a_report_file_in, "r", encoding="utf-8") as fin:
        test_data = fin.read()

    # arrange
    # first need to write ref results to a file, so we can use csv.DictReader to read it in as a list[dict]
    ref_result_file = tmp_path / "ref_results.csv"
    with open(ref_result_file, "w", encoding="utf-8") as fout_ref:
        fout_ref.write(ref_result)

    ref_result_list = []
    with open(ref_result_file, "r", encoding="utf-8") as fin_ref:
        fin_ref.readline()  # skip the first line header
        ref_result_dict_reader = csv.DictReader(
            fin_ref,
            fieldnames=_csv_report_header_,
            quoting=csv.QUOTE_ALL,
            lineterminator="\n",
        )

        for row in ref_result_dict_reader:
            ref_result_list.append(row)

    ref_result_list_sorted = sorted(ref_result_list, key=lambda d: d["path"])

    # get the test results sorted in the same way
    result_list = []
    with open(report_file, "r", encoding="utf-8") as fin:
        fin.readline()  # skip the first line header
        result_dict_reader = csv.DictReader(
            fin,
            fieldnames=_csv_report_header_,
            quoting=csv.QUOTE_ALL,
            lineterminator="\n",
        )

        for row in result_dict_reader:
            result_list.append(row)

    result_list_sorted = sorted(result_list, key=lambda d: d["path"])

    assert result_list_sorted == ref_result_list_sorted
