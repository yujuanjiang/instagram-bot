import random
from PIL import ImageOps, ImageFilter, Image


def make_decision(value):
    if value > 100:
        value = 100
    if random.randrange(0, 100) < value:
        return True
    return False

def get_random_hex_color():
    hex_color = "#{:06x}".format(random.randint(0, 0xffffff))
    print("Generated HEX color: {}".format(hex_color))
    return hex_color


def process_image_from_file(path):
    base_image = Image.open(path)
    return process_image(base_image)


def process_image(image):

    if make_decision(85):
        image = ImageOps.grayscale(image)
        image = ImageOps.colorize(image,
                                  get_random_hex_color(),
                                  get_random_hex_color(),
                                  get_random_hex_color())
    # if with_decision(50):
    #     image = ImageOps.flip(image)
    # if with_decision(50):
    #     image = ImageOps.mirror(image)
    if make_decision(50):
        posterize_bits = random.randrange(1, 8)
        image = ImageOps.posterize(image, posterize_bits)
    if make_decision(50):
        threshold = random.randrange(0, 255)
        image = ImageOps.solarize(image, threshold)
    if make_decision(50):
        image = ImageOps.equalize(image)
    if make_decision(50):
        blur_radius = random.randrange(0, 3)
        image = image.filter(ImageFilter.GaussianBlur(blur_radius))

    return image
