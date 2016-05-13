

class DataSet:

    def __init__(self):
        self._pages = dict()

    def add(self, page_image, description=None):
        if not description:
            description = page_image.image_file
        self._pages.update({
            description: page_image
        })

    def __str__(self):
        return ", ".join([
            "{DataSet",
            "number of page images: " + str(len(self._pages)),
            "}"])
