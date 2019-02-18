from InstagramAPI import InstagramAPI as api
import config
import img_utils
import os


def delete_all_in_feed(api_session):
    print("Removing all posts in feed...")
    for post in api_session.getTotalSelfUserFeed():
        post_id = post['id']
        print("Removing post with id: {}".format(post_id))
        api_session.deleteMedia(post_id)

login_attempts = 0
login_status = False
temp_image_path = "temp.jpg"
session = api(config.login, config.password)
print("Connecting to Instagram API...")

while login_status is False and login_attempts < config.MAX_LOGIN_ATTEMPTS:
    print("Login attempt #{}".format(login_attempts))
    login_status = session.login()
    login_attempts += 1

if login_status is True:
    try:
        base_image = img_utils.Image.open(config.image_path)
        print("Image loaded. Processing...")
        processed_image = img_utils.process_image(base_image)
        print("Saving temporary file {}".format(temp_image_path))
        processed_image.save(temp_image_path)
        print("Attempting to upload photo with caption: \"{}\"".format(config.caption))
        if session.uploadPhoto(temp_image_path, caption=config.caption) is False:
            print("Upload successful!")
        print("Removing temporary file {}".format(temp_image_path))
        os.remove(temp_image_path)
    except FileNotFoundError:
        print("File not found")
    except Exception:
        print("Unexpected error")
else:
    print("Failed to connect to Instagram API")
