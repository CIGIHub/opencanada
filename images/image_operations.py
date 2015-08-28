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


class CircleWithRingOperation(FillOperation):

    def construct(self, size, *extra):

        self.circle_color = (204, 204, 204, 1)
        self.ring_width = 1

        unprocessed_extra = []
        for extra_part in extra:
            if extra_part.startswith('rgba_'):
                color_parts = extra_part.split('_')
                num_parts = len(color_parts)
                if num_parts == 2:
                    color = int(color_parts[1])
                    self.circle_color = (color, color, color, 1)
                elif num_parts >= 4:
                    if num_parts == 4:
                        alpha = 1
                    else:
                        alpha = int(color_parts[4])
                    red = int(color_parts[1])
                    green = int(color_parts[2])
                    blue = int(color_parts[3])
                    self.circle_color = (red, green, blue, alpha)
            elif extra_part.startswith('w_'):
                self.ring_width = int(extra_part[2:])
            else:
                unprocessed_extra.append(extra)

        super(CircleWithRingOperation, self).construct(size, *unprocessed_extra)

    def run(self, willow, image):
        super(CircleWithRingOperation, self).run(willow, image)
        willow.original_format = 'png'

        ring_width = 3 * self.ring_width
        mask_size = (3 * self.width, 3 * self.height)
        mask = Image.new('L', mask_size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + mask_size, fill=255)
        draw.ellipse((ring_width, ring_width) + (3 * self.width - ring_width, 3 * self.height - ring_width), fill=0)
        mask = mask.resize((self.width, self.height), Image.ANTIALIAS)
        del draw

        willow.draw_bitmap(mask, self.circle_color)

        mask = Image.new('L', mask_size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + mask_size, fill=255)
        mask = mask.resize((self.width, self.height), Image.ANTIALIAS)
        del draw

        willow.putalpha(mask)
