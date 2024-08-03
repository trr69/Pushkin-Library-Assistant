import requests
import random
import string
from .HTMLParser import HTMLParser

class BaseAPIHandler:
    BASE_URL: str = "http://irbis.pushkinlibrary.kz:8087/jirbis2/components/com_irbis/ajax_provider.php"

    @staticmethod
    def _generate_random_string(length: int = 8) -> str:
        """Generate a random string of letters and digits."""
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    @staticmethod
    def _generate_random_number_string(length: int = 10) -> str:
        """Generate a random string of digits."""
        digits = string.digits
        return ''.join(random.choice(digits) for _ in range(length))

    def _check_response(self, response: requests.Response) -> requests.Response:
        """Check the response status and raise an exception if the request failed."""
        if response.status_code != 200:
            raise Exception(f"Request failed: {response.status_code} {response.text}")
        return response

    def _post_request(self, data: dict) -> requests.Response:
        """Send a POST request with the given data."""
        response = self.session.post(self.BASE_URL, data=data)
        return self._check_response(response)

    def _get_request(self, url: str) -> requests.Response:
        """Send a GET request to the given URL."""
        response = self.session.get(url)
        return self._check_response(response)

class BookSearchHandler(BaseAPIHandler):

    def __init__(self, search_params: dict):
        """Initialize the handler with search parameters and set up the session."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache'
        })
        self.search_params = search_params
        self.client_request_id = self._generate_random_number_string(10)
        self.form_request_id = self._generate_random_number_string(10)

    def _search_request(self) -> requests.Response:
        """Send a search request with the current search parameters."""
        data = {
            'req_static': '0',
            'author': self.search_params.get('author', ''),
            'person': self.search_params.get('person', ''),
            'title': self.search_params.get('title', ''),
            'keywords': self.search_params.get('keywords', ''),
            'keywords_cvalif': self.search_params.get('keywords_cvalif', ''),
            'subject_rubric': self.search_params.get('subject_rubric', ''),
            'year1': self.search_params.get('year1', ''),
            'year2': self.search_params.get('year2', ''),
            'publishing': self.search_params.get('publishing', ''),
            'isbn': self.search_params.get('isbn', ''),
            'document_type': self.search_params.get('document_type', ''),
            'document_form': self.search_params.get('document_form', ''),
            'document_language': self.search_params.get('document_language', ''),
            'task': 'search_broadcast',
            'first_number': '1',
            'req_id_client': self.client_request_id,
            'selected_search_flag': '0'
        }
        return self._post_request(data)

    def _set_selected_databases(self) -> requests.Response:
        """Set the selected databases for the search."""
        url = f"{self.BASE_URL}?task=set_selected_bases&bl_id_array_selected%5B1%5D=1&bl_id_array_selected%5B2%5D=2&bl_id_array_selected%5B3%5D=3&_={self.form_request_id}"
        return self._get_request(url)

    def _set_user_profile(self) -> requests.Response:
        """Set the user profile for the search."""
        url = f"{self.BASE_URL}?task=set_selected_user_profile&rp_elements%5B%5D=document_form&rp_elements%5B%5D=keywords&rp_elements%5B%5D=contents&profile_name=info&_={self.form_request_id}"
        return self._get_request(url)

    def _get_search_results(self) -> requests.Response:
        """Get the search results."""
        url = f"{self.BASE_URL}?task=show_results&req_id_client={self.client_request_id}&first_number=1&recs_outputed=0&reqs_outputed=0&last_output_time=0&finish_flag=last&_={self.form_request_id}"
        return self._get_request(url)

    def execute_search(self) -> None:
        """Execute the full search process."""
        try:
            self._search_request()
            self._set_selected_databases()
            self._set_user_profile()
            self._search_request()
            results = self._get_search_results()
            results_json = results.json()

            htmlParser: HTMLParser = HTMLParser(results_json['recs'])

            results_json['recs'] = htmlParser.start_parsing_data()
            return results_json

        except Exception as e:
            print(f"An error occurred: {e}")
