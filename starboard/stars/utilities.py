from django.conf import settings


def ignore_sources(image, ignore_urls=None):
    if ignore_urls is None:
        ignore_urls = settings.IMG_SRC_IGNORE_STRINGS

    if "data-canonical-src" in image.attrs:
        ignore_image_canonical = any(url in image.attrs["data-canonical-src"] for url in ignore_urls)
    else:
        ignore_image_canonical = False
    ignore_image = "src" not in image.attrs or any(url in image.attrs["src"] for url in ignore_urls)
    return ignore_image or ignore_image_canonical
