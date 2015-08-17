from PIL import Image, ImageDraw
from wagtail.wagtailimages.image_operations import FillOperation


class CircleOperation(FillOperation):
    def run(self, willow, image):
        super(CircleOperation, self).run(willow, image)

        mask_size = (3 * self.width, 3 * self.height)
        mask = Image.new('L', mask_size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + mask_size, fill=255)
        mask = mask.resize((self.width, self.height), Image.ANTIALIAS)

        willow.putalpha(mask)
        willow.original_format = 'png'
