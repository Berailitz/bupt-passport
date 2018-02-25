"""Login helper logic."""
import logging
import time
import requests
from ..config import LOGIN_MAX_ATTEMPT, LOGIN_WAIT_INTERVEL, HTTP_CLIENT_MAX_RETRIES, HTTP_CLIENT_REFERER, HTTP_CLIENT_TIME_OUT


class HTTPClient:
    """Client for HTTP requests..

    :member session: Attached Requests session.
    """
    def __init__(self, session=None):
        if session:
            self.session = session
        else:
            self.session = requests.Session()

    @staticmethod
    def create_headers(referer='http://my.bupt.edu.cn/index.portal', origin='http://my.bupt.edu.cn/index.portal'):
        """Create http headers with custom `referer` and `origin`.
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Cache-Control': 'max-age=0',
            'Referer': referer,
            'Origin': origin
        }
        return headers

    def post(self, url, data, timeout=HTTP_CLIENT_TIME_OUT, max_retries=HTTP_CLIENT_MAX_RETRIES, referer=HTTP_CLIENT_REFERER, **kw):
        """Post with headers.
        """
        for attempt_counter in range(max_retries):
            try:
                post_response = self.session.post(url, headers=self.create_headers(referer), data=data, timeout=timeout, **kw)
                post_response.encoding = "utf-8"
                return post_response
            except requests.Timeout as identifier:
                logging.warning(f'HTTPClient: ({attempt_counter + 1} / {max_retries}) Failed to POST `{data}` to `{url}`: {identifier}')
                attempt_counter += 1
        raise requests.Timeout(f'HTTPClient: Max POST retries exceeded with url: {url}')

    def get(self, url, timeout=HTTP_CLIENT_TIME_OUT, max_retries=HTTP_CLIENT_MAX_RETRIES, referer=HTTP_CLIENT_REFERER, **kw):
        """Get with headers.
        """
        for attempt_counter in range(max_retries):
            try:
                get_response = self.session.get(url, headers=self.create_headers(referer), timeout=timeout, **kw)
                get_response.encoding = "utf-8"
                return get_response
            except requests.Timeout as identifier:
                logging.warning(f'HTTPClient: ({attempt_counter + 1} / {max_retries}) Failed to GET `{url}`: {identifier}')
                attempt_counter += 1
        raise requests.Timeout(f'HTTPClient: Max GET retries exceeded with url: {url}')

    def refresh_session(self, session=None):
        """Generate a new session or set a new session.

        :param session: New session, defaults to None.
        :type session: Requests.Session, optional.
        """
        self.session = session or requests.Session()
        logging.warning('HTTPClient: session refreshed.')


class LoginHelper(object):
    """Base class for login.
    """
    def __init__(self, http_client=None):
        self.max_attempt = LOGIN_MAX_ATTEMPT
        self.wait_intervel = LOGIN_WAIT_INTERVEL
        self.http_client = http_client

    def init_http_client(self, http_client):
        self.http_client = http_client

    def _login(self):
        """Send login requests.

        :raises NotImplementedError: If this method is not impemented.
        """
        raise NotImplementedError

    def response_checker(self, login_response):
        """Check response from login action, return error description(True)
        for error or `None` for success.

        :param login_response: Response of login request.
        :type login_response: Requests.Response.
        :return: Error message if error occured.
        :rtype: str|None.
        """
        logging.warning('LoginHelper: `response_checker` NOT implemented.')
        return None

    def do_login(self, error_notice=None):
        """Send login requests for :attr:`max_attempt` times, raise last error if failed.

        :param error_notice: Notice to show if failed to log in, defaults to None.
        :type error_notice: str, optional.
        :raises identifier: Error occured.
        :raises PermissionError: Login fails due to unknown error.
        :return: Login response.
        :rtype: requests.Response.
        """
        for login_counter in range(self.max_attempt):
            try:
                login_response = self._login()
                login_result = self.response_checker(login_response)
                if not login_result:
                    logging.info(f'LoginHelper: Result: Success.')
                    return login_response
                else:
                    logging.warning(f'LoginHelper: ({login_counter + 1} / {self.max_attempt}) Error `{login_result}`.')
            except KeyboardInterrupt as identifier:
                logging.warning('LoginHelper: Catch KeyboardInterrupt when logging in.')
                raise identifier
            except Exception as identifier:
                logging.error(f'LoginHelper: ({login_counter + 1} / {self.max_attempt}) Error when logging in: {identifier}')
                if login_counter == self.max_attempt - 1:
                    logging.error(f'LoginHelper: Cannot login: `{error_notice}`.')
                    raise identifier
            finally:
                time.sleep(self.wait_intervel)
        raise PermissionError(f'LoginHelper: Cannot login: `{error_notice}`.')

    def try_login(self, error_notice=None):
        """Try to log in, return response if succeeded, or False if failed.

        :param error_notice: Notice to show if failed to log in, defaults to None.
        :type error_notice: str, optional.
        :raises KeyboardInterrupt: Keyboard interruption.
        :return: Login response.
        :rtype: requests.Response|None.
        """
        try:
            return self.do_login(error_notice=error_notice)
        except KeyboardInterrupt as identifier:
            logging.warning('LoginHelper: Catch KeyboardInterrupt when logging in.')
            raise identifier
        except Exception:
            return False
