from InstagramAPI import InstagramAPI
from _collections_abc import Iterable
import time


class LoginFailedError(Exception):
    pass


class TooManyLoginAttemptsError(Exception):
    pass


class NotLoggedInError(Exception):
    pass


class InstagramApiFacade:
    MAX_ATTEMPTS = 100
    SECS_BETWEEN_ATTEMPTS = 5

    def __init__(self, login, password):
        self.api_session = InstagramAPI(login, password)

    def login(self):
        self.api_session.login()
        if self.is_logged_in() is False:
            raise LoginFailedError

    def login_with_retries(self, max_attempt_count=None):
        if max_attempt_count is None:
            max_attempt_count = self.MAX_ATTEMPTS

        attempt_count = 1

        while not self.is_logged_in() \
                and attempt_count < max_attempt_count:
            try:
                print("Login attempt [{}/{}]".format(attempt_count, self.MAX_ATTEMPTS))
                self.login()
            except LoginFailedError:
                print("Login attempt failed. Retrying in {} seconds".format(self.SECS_BETWEEN_ATTEMPTS))
                time.sleep(self.SECS_BETWEEN_ATTEMPTS)
                continue

        if self.is_logged_in() is False:
            raise TooManyLoginAttemptsError

    def logout(self):
        if self.is_logged_in():
            self.api_session.logout()

    def is_logged_in(self):
        return self.api_session.isLoggedIn

    def upload_photo(self, file_path, caption):
        if self.is_logged_in():
            print("Uploading {} with caption \"{}\"".format(file_path, caption))
            self.api_session.uploadPhoto(file_path, caption)
        else:
            raise NotLoggedInError

    def delete_post(self, id):
        if isinstance(id, str):
            print("Removing post with id: {}".format(id))
            self.api_session.deleteMedia(id)
        else:
            raise TypeError("Function expects string type")

    def delete_posts(self, ids):
        if isinstance(ids, Iterable) and not isinstance(ids, str):
            for id in ids:
                self.api_session.deleteMedia(id)
        else:
            raise TypeError("Function expects a non-str Iterable")

    def delete_all_posts(self):
        for post in self.api_session.getTotalSelfUserFeed():
            id = post['id']
            self.delete_post(id)

    def get_posts(self):
        return self.api_session.getTotalSelfUserFeed()
