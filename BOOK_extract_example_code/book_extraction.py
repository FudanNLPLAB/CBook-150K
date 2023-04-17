import shutil
from bs4 import BeautifulSoup
from urllib.parse import unquote
import os
import warnings
warnings.filterwarnings("ignore")
import zipfile
import mobi
import glob
import PyPDF2

epub_chinese_md5_dir = os.path.join(os.path.realpath(os.path.dirname(os.path.abspath(__file__))),'chinese_book/epub')
mobi_chinese_md5_dir = os.path.join(os.path.realpath(os.path.dirname(os.path.abspath(__file__))),'chinese_book/mobi')
pdf_chinese_md5_dir = os.path.join(os.path.realpath(os.path.dirname(os.path.abspath(__file__))),'chinese_book/pdf')
epub_md5_list = glob.glob( epub_chinese_md5_dir + '/*.{}'.format('epub'))
mobi_md5_list = glob.glob( mobi_chinese_md5_dir + '/*.{}'.format('mobi'))
pdf_md5_list = glob.glob( pdf_chinese_md5_dir + '/*.{}'.format('pdf'))
MIN_WORDS_LIMIT = int(1e3)

for EPUB_MD5 in epub_md5_list:
    # 指定epub文件路径
    book_path = os.path.join(epub_chinese_md5_dir,EPUB_MD5)
    # 使用ZipFile库打开epub文件
    book = zipfile.ZipFile(book_path)
    # 获取书籍的文本数据
    xhtml_data = [string for string in book.namelist() if string.endswith('xhtml') or string.endswith('html') or string.endswith('xml')]
    with open(os.path.join(epub_chinese_md5_dir,'{}.txt'.format(EPUB_MD5)),'w',encoding='utf-8') as fp:
        for k in range(len(xhtml_data)):
            try:
                chapter_file = book.open(unquote(xhtml_data[k]))
                chapter_content = chapter_file.read().decode('utf-8')
                chapter_content = BeautifulSoup(chapter_content, 'html')
                fp.write(chapter_content.get_text().strip())
            except Exception as e:
                print(e)
                continue
        fp.close()
    with open(os.path.join(epub_chinese_md5_dir,'{}.txt'.format(EPUB_MD5)),'r',encoding='utf-8') as fp:
        lines = fp.readlines()
    filtered_lines = []
    total_len = 0
    # 过滤掉单个换行符,格式化
    for line in lines:
        try:
            if line.strip() == '':
                continue
            else:
                filtered_lines.append(line.strip()+'\n')
                total_len += len(line.strip())
        except Exception as e:
            print(e)
            continue
    
    with open(os.path.join(epub_chinese_md5_dir,'{}.txt'.format(EPUB_MD5)),'w',encoding='utf-8') as fp:
        fp.writelines(filtered_lines)
        fp.close()



for MOBI_MD5 in mobi_md5_list:
    book_path = os.path.join(mobi_chinese_md5_dir,MOBI_MD5)
    tempdir, filepath = mobi.extract(book_path)
    with open(filepath,'r',encoding='utf-8') as mobi_fp:
        chapter_content = mobi_fp.read()
    #chapter_content = etree.HTML(chapter_content,parser=etree.HTMLParser(encoding='utf-8'))
    shutil.rmtree(tempdir)

    chapter_content = BeautifulSoup(chapter_content, 'html.parser')
    chapter_content = chapter_content.prettify()
    chapter_content = BeautifulSoup(chapter_content, 'html.parser')
    with open(os.path.join(mobi_chinese_md5_dir,'{}.txt'.format(MOBI_MD5)),'w',encoding='utf-8') as fp:
        fp.write(chapter_content.get_text().strip())
    with open(os.path.join(mobi_chinese_md5_dir,'{}.txt'.format(MOBI_MD5)),'r',encoding='utf-8') as fp:
        lines = fp.readlines()
    filtered_lines = []
    total_len = 0
    # 过滤掉单个换行符,格式化
    for line in lines:
        try:
            if line.strip() == '':
                continue
            else:
                filtered_lines.append(line.strip()+'\n')
                total_len += len(line.strip())
        except Exception as e:
            print(e)
            continue
    with open(os.path.join(mobi_chinese_md5_dir,'{}.txt'.format(MOBI_MD5)),'w',encoding='utf-8') as fp:
        fp.writelines(filtered_lines)
        fp.close()
    


for PDF_MD5 in pdf_md5_list:
    # 保存每页文本信息
    page_info = []
    try:
    # 指定pdf文件路径
        book_path = os.path.join(pdf_chinese_md5_dir,PDF_MD5)
        with open(book_path, 'rb') as pdf_fp:
            pdf_reader = PyPDF2.PdfReader(pdf_fp)
            if pdf_reader.is_encrypted:
                # 如果PDF文档是加密的，则需要提供密码才能继续处理
                pass
            else:
                # 遍历每一页并提取文本信息
                for i in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[i]
                    text = page.extract_text()
                    # 如果提取到的文本信息非空，则认为该PDF文档包含文本信息
                    if text.strip():
                        page_info.append(text.strip()+'\n')
    except Exception as e:
        print(e)
    with open(os.path.join(pdf_chinese_md5_dir,'{}.txt'.format(PDF_MD5)),'w',encoding='utf-8') as fp:
        fp.write(''.join(page_info).strip())
    with open(os.path.join(pdf_chinese_md5_dir,'{}.txt'.format(PDF_MD5)),'r',encoding='utf-8') as fp:
        lines = fp.readlines()
    filtered_lines = []
    # 过滤掉单个换行符,格式化
    for line in lines:
        try:
            if line.strip() == '':
                continue
            else:
                filtered_lines.append(line.strip()+'\n')
                total_len += len(line.strip())
        except Exception as e:
            print(e)
            continue
    
    with open(os.path.join(pdf_chinese_md5_dir,'{}.txt'.format(PDF_MD5)),'w',encoding='utf-8') as fp:
        fp.writelines(filtered_lines)
        fp.close()
