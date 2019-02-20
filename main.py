import config
import img_utils
from api_utils import *
import os, platform


def get_temp_img_path():
    temp_image_path = os.path.dirname(os.path.realpath(__file__))
    if "windows" in platform.platform().lower():
        temp_image_path += '\\'
    else:
        temp_image_path += '/'
    temp_image_path += 'processed_image.jpg'
    return temp_image_path


temp_img_path = get_temp_img_path()
api = InstagramApiFacade(config.login, config.password)

try:
    print("Opening and processing image: {}".format(config.image_path))
    processed_image = img_utils.process_image_from_file(config.image_path)
    print("Saving processed image to temporary file: {}".format(temp_img_path))
    processed_image.save(temp_img_path)
    print("Logging in...")
    api.login_with_retries()
    api.upload_photo(temp_img_path, config.caption)
    print("Removing temporary file: {}".format(temp_img_path))
    os.remove(temp_img_path)
except TooManyLoginAttemptsError:
    print("Operation failed, too many login attempts. ")
except NotLoggedInError:
    print("API session inactive, can't upload image.")
except FileExistsError as err:
    print("File already exists: {}".format(err.filename))
except FileNotFoundError as err:
    print("Couldn't find file: {}".format(err.filename))
except IOError as err:
    print("Couldn't find file: {}".format(err.filename))
except:
    print("Unknown error")
finally:
    api.logout()
