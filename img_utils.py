import random
from PIL import ImageOps, ImageFilter, Image


def probability(value):
    if value > 1.0:
        value = 1.0
    if random.randrange(1, 101) / 100.0 <= value:
        return True
    return False


def get_rand_hex_color():
    hex_color = "#{:06x}".format(random.randint(0, 0xffffff))
    print("Generated HEX color: {}".format(hex_color))
    return hex_color


def process_image(image):
    if probability(85):
        image = ImageOps.grayscale(image)
        image = ImageOps.colorize(image,
                                  get_rand_hex_color(),
                                  get_rand_hex_color(),
                                  get_rand_hex_color())
    # if with_probability(50):
    #     image = ImageOps.flip(image)
    # if with_probability(50):
    #     image = ImageOps.mirror(image)
    if probability(0.5):
        posterize_bits = random.randrange(1, 8)
        image = ImageOps.posterize(image, posterize_bits)
    if probability(0.5):
        threshold = random.randrange(0, 255)
        image = ImageOps.solarize(image, threshold)
    if probability(0.5):
        image = ImageOps.equalize(image)
    if probability(0.5):
        blur_radius = random.randrange(0, 3)
        image = image.filter(ImageFilter.GaussianBlur(blur_radius))

    return image
