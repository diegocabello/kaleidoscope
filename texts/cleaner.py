"""
this removes images, captions, and pagenums
"""

from bs4 import BeautifulSoup

def remove_images(html_file, output_file):
    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    for img_tag in soup.find_all('img'):
        img_tag.decompose()
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(str(soup))
remove_images('path/to/your/file.html', 'output_file.html')

def remove_pagenum_elements(html_file, output_file):
    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    for span_tag in soup.find_all('span', {'class': 'pagenum'}):
        span_tag.decompose()
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(str(soup))s


def remove_caption(html_file, output_file):
    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    for div_tag in soup.find_all('div', {'class': 'caption'}):
        div_tag.decompose()
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(str(soup))

def remove_caption(html_file, output_file):
    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    for div_tag in soup.find_all('span', {'class': 'caption'}):
        div_tag.decompose()
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(str(soup))

