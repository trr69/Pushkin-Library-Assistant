import asyncio
from playwright.async_api import async_playwright, Browser, ElementHandle, TimeoutError
from typing import Dict

class BaseBooksParser:
    """
    Базовый класс для парсера книг с сайта 
    http://irbis.pushkinlibrary.kz:8087/jirbis2/index.php?option=com_irbis&view=irbis&Itemid=351&lang=ru
    """
    SEARCH_PAGE: str = "http://irbis.pushkinlibrary.kz:8087/jirbis2/index.php?option=com_irbis&view=irbis&Itemid=351&lang=ru"
    
    def __init__(self, browser: Browser) -> None:
        self._browser = browser

    async def _get_new_page(self) -> ElementHandle:
        """
        Метод возвращает новую страницу
        """
        try:
            if self._browser:
                return await self._browser.new_page()
            else:
                raise RuntimeError("Браузер не инициализирован")
        except Exception as e:
            print(f"Произошла ошибка при создании новой страницы: {e}")
            return None

class BooksParser(BaseBooksParser):
    """
    Дочерний класс для парсинга книг с сайта
    """
    def __init__(self, browser: Browser) -> None:
        super().__init__(browser)

    async def start_handle(self, data: Dict[str, str]) -> None:
        try:
            async with await self._get_new_page() as page:
                await page.goto(self.SEARCH_PAGE)
                await self._past_and_send_data(data=data, page=page)
                req_count: str = await self._get_req_count(page)
                print(req_count)
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    async def _validate_form(self, data: Dict[str, str]) -> Dict[str, str]:
        validated_data: Dict[str, str] = {}
        fields_to_check = ['author', 'person', 'title', 'keywords']

        for field in fields_to_check:
            if field in data:
                validated_data[field] = data[field]

        if not validated_data:
            return {'error': 'Должно быть заполнено хотя бы 1 поле'}
        
        return validated_data

    async def _past_and_send_data(self, data: Dict[str, str], page: ElementHandle) -> None:
        validated_data: Dict[str, str] = await self._validate_form(data)
        if 'error' in validated_data:
            return
        
        try:
            # Ввод для автора
            author_input_box: ElementHandle = await page.query_selector('input[id="author"]')
            await author_input_box.fill(validated_data.get('author', ''))

            # Ввод для персоналии
            person_input_box: ElementHandle = await page.query_selector('input[id="person"]')
            await person_input_box.fill(validated_data.get('person', ''))

            # Ввод для названия
            title_input_box: ElementHandle = await page.query_selector('input[id="title"]')
            await title_input_box.fill(validated_data.get('title', ''))

            # Ввод для ключевых слов
            keywords_input_box: ElementHandle = await page.query_selector('input[id="keywords"]')
            await keywords_input_box.fill(validated_data.get('keywords', ''))

            # Поиск и нажатие на кнопку поиска
            search_button: ElementHandle = await page.query_selector('input[id="search_button"]')
            await search_button.click()
        except Exception as e:
            print(f"Произошла ошибка во время ввода данных: {e}")

    async def _get_req_count(self, page: ElementHandle) -> str:
        try:
            req_description_cell: ElementHandle = await page.wait_for_selector('td[id="req_description_cell"]')
            return await req_description_cell.text_content()
        except Exception as e:
            raise TimeoutError('Не удалось найти поле req_description_cell в течении заданного времени')

async def main():
    async with async_playwright() as p:
        try:
            browser: Browser = await p.chromium.launch(headless=True)
            bParser: BooksParser = BooksParser(browser=browser)
            await bParser.start_handle({'author': 'Абай', 'person': 'Не'})
        finally:
            await browser.close()

asyncio.run(main())
