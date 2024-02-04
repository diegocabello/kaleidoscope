"""
this removes images, captions, and pagenums
"""

from bs4 import BeautifulSoup

input_file = r'c:\users\diego\documents\my stuff\programming stuff\babel\texts\pride and prejudice.html'
output_file = r'c:\users\diego\documents\my stuff\programming stuff\babel\texts\pride and prejudice3.html'

def remove_elements(html_file, output_file, tag, **attrs):
    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    for element in soup.find_all(tag, attrs):
        element.decompose()
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(str(soup))

remove_elements(input_file, output_file, 'img')
remove_elements(input_file, output_file, 'span', class_='pagenum')
remove_elements(input_file, output_file, 'div', class_='caption')