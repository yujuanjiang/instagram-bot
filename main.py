from InstagramAPI import InstagramAPI as api
import config
import img_utils
import os


def delete_all_in_feed(api_session):
    for post in api_session.getTotalSelfUserFeed():
        api_session.deleteMedia(post['id'])


temp_image_path = "temp.jpg"

base_image = img_utils.Image.open(config.image_path)
processed_image = img_utils.process_image(base_image)
print("Saving temporary file {}".format(temp_image_path))
processed_image.save(temp_image_path)

session = api(config.login, config.password)
print("Connecting to Instagram API...")
if session.login() is True:
    print("Attempting to upload photo with caption: \"{}\"".format(config.caption))
    if session.uploadPhoto(temp_image_path, caption=config.caption) is False:
        print("Upload successful!")

print("Removing temporary file {}".format(temp_image_path))
os.remove(temp_image_path)
