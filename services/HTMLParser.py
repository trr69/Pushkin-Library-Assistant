import re
from bs4 import BeautifulSoup
import json
from typing import List, Dict

class HTMLParser:
    def __init__(self, html_content: str):
        self._html_content = html_content

    def clean_html(self, html_content: str) -> str:
        html_content = re.sub(r'\\[trn]', '', html_content).replace('\\', '')
        soup = BeautifulSoup(html_content, 'html.parser')
        
        for span in soup.find_all('span'):
            span.unwrap()
        
        return str(soup)

    def parse_records_table(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        records = []
        for record in soup.find_all('table', class_='record'):
            record_data = {}
            
            number_cell = record.find('td', class_='number_cell')
            if number_cell:
                record_data['number'] = number_cell.find('div', class_='number').text.strip()
                record_data['code'] = number_cell.find('input', class_='code_checkbox')['value']
            
            cover_cell = record.find('td', class_='cover_cell')
            if cover_cell:
                img_tag = cover_cell.find('img', class_='cover_img')
                record_data['cover_url'] = img_tag['src']
            
            bo_cell = record.find('td', class_='bo_cell')
            if bo_cell:
                bo_div = bo_cell.find('div', class_='bo_div')
                if bo_div:
                    record_data['type'] = bo_div.find(string=' Вид документа').next_element.strip() if bo_div.find(string=' Вид документа') else ''
                    record_data['code'] = bo_div.find(string=' Шифр издания').next_element.strip() if bo_div.find(string=' Шифр издания') else ''
                    record_data['author'] = bo_div.find(string=' Автор(ы)').next_element.strip() if bo_div.find(string=' Автор(ы)') else ''
                    record_data['title'] = bo_div.find(string=' Заглавие').next_element.strip() if bo_div.find(string=' Заглавие') else ''
                    record_data['parallel_title'] = bo_div.find(string=' Параллельн. заглавия').next_element.strip() if bo_div.find(string=' Параллельн. заглавия') else ''
                    record_data['publish_info'] = bo_div.find(string=' Выходные данные').next_element.strip() if bo_div.find(string=' Выходные данные') else ''
                    record_data['pages'] = bo_div.find(string=' Колич.характеристики').next_element.strip() if bo_div.find(string=' Колич.характеристики') else ''
                    record_data['series'] = bo_div.find(string=' Серия:').next_element.strip() if bo_div.find(string=' Серия:') else ''
                    record_data['isbn_price'] = bo_div.find(string=' ISBN,  Цена    ').next_element.strip() if bo_div.find(string=' ISBN,  Цена    ') else ''
            
            records.append(record_data)
        return records

    def start_parsing_data(self) -> List[Dict[str, str]]:
        clean_html_content = self.clean_html(self._html_content)
        soup = BeautifulSoup(clean_html_content, 'html.parser')
        return self.parse_records_table(soup)


def main():
    with open('index.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    parser = HTMLParser(html_content)
    parsed_data = parser.start_parsing_data()
    
    print(json.dumps(parsed_data, ensure_ascii=False, indent=4))

if __name__ == "__main__":
    main()
