from PIL import Image, ImageDraw
from wagtail.wagtailimages.image_operations import FillOperation
from willow.plugins.pillow import PillowImage


class AlphaOperation(FillOperation):
    def putalpha(self, willow, alpha):
        willow.image.putalpha(alpha)
        # willow.image.save('alpha.png')
        return PillowImage(willow.image)


class DrawBitmapOperation(AlphaOperation):
    def draw_bitmap(self, willow, bitmap, fill):
        draw = ImageDraw.Draw(willow.image)
        draw.bitmap((0, 0), bitmap, fill)
        del draw
        # willow.image.save('bitmap.png')
        return PillowImage(willow.image)


# eg circlecrop-80x80-rgba_255_0_0_1-w_1
class CircleCropOperation(FillOperation):
    def construct(self, size, *extra):
        self.border_color = (204, 204, 204, 1)
        self.border_width = 0

        unprocessed_extra = []
        for extra_part in extra:
            if extra_part.startswith('rgba_'):
                color_parts = extra_part.split('_')
                num_parts = len(color_parts)
                if num_parts == 2:
                    color = int(color_parts[1])
                    self.border_color = (color, color, color, 1)
                elif num_parts >= 4:
                    if num_parts == 4:
                        alpha = 1
                    else:
                        alpha = int(color_parts[4])
                    red = int(color_parts[1])
                    green = int(color_parts[2])
                    blue = int(color_parts[3])
                    self.border_color = (red, green, blue, alpha)
            elif extra_part.startswith('w_'):
                self.border_width = int(extra_part[2:])
            else:
                unprocessed_extra.append(extra)

        super(CircleCropOperation, self).construct(size, *unprocessed_extra)

    def run(self, willow, image, env):
        # Note that `image` here is the database model of the Image, not the actual image
        if image.width < self.width or image.height < self.height:
            # unable to process image at all since the putalpha will fail
            return

        willow = super(CircleCropOperation, self).run(willow, image, env)
        with image.get_willow_image() as willow_image:
            original_format = willow_image.format_name

        pillow_image = willow.image
        # pillow_image.save('filled.{0}'.format(original_format))

        # We can get fancy with transparencies...
        if original_format == 'png':
            mask = self._draw_circular_mask()
            if self.border_width > 0:
                # Add a border...
                border_mask = self._draw_circular_mask(with_border=True)
                draw = ImageDraw.Draw(pillow_image)
                draw.bitmap((0, 0), border_mask, self.border_color)
                del draw
                # pillow_image.save('bitmap.png')
                mask.paste(border_mask, (0, 0), border_mask)
                # mask.save('pasted.png')
            pillow_image.putalpha(mask)
        else:
            mask = self._draw_circular_mask(invert=True)
            pillow_image.paste(mask, (0, 0), mask)
            width, height = pillow_image.size
            if self.border_width > 0:
                draw = ImageDraw.Draw(pillow_image)
                # We need this first ellipse which won't actually be a closed circle since we are using 'outline'...
                _border_color = self.border_color
                if draw.im.mode == 'L':
                    # 'L' implies the image is grayscale so providing (r, g, b[, alpha]) doesn't make any sense as there is one channel; it's expecting an integer
                    _border_color = self.border_color[0]
                draw.ellipse((0, 0) + (width, height), outline=_border_color)
                # Move in 1 pixel and draw another ellipse for each pixel of width
                for i in range(self.border_width):
                    draw.ellipse((i + 1, i + 1) + (width - i - 1, height - i - 1), outline=_border_color)
                del draw
        # pillow_image.save('masked.{0}'.format(original_format))

        return PillowImage(pillow_image)

    def _draw_circular_mask(self, with_border=False, invert=False):
        scale_factor = 3
        base_color = 0
        fill_color = 255
        if invert:
            base_color = 255
            fill_color = 0
        mask_size = (scale_factor * self.width, scale_factor * self.height)
        mask = Image.new('L', mask_size, base_color)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + mask_size, fill=fill_color)
        if with_border:
            border_width = scale_factor * self.border_width
            draw.ellipse((border_width, border_width) + (scale_factor * self.width - border_width, scale_factor * self.height - border_width), fill=base_color)
        del draw
        mask = mask.resize((self.width, self.height), Image.ANTIALIAS)
        # if with_border:
        #     mask.save('circular_mask_with_border.png')
        # else:
        #     mask.save('circular_mask.png')
        return mask


class CircleOperation(AlphaOperation):
    def run(self, willow, image):
        if image.width < self.width or image.height < self.height:
            # unable to process image at all since the putalpha will fail
            return

        willow = super(CircleOperation, self).run(willow, image)

        mask_size = (3 * self.width, 3 * self.height)
        mask = Image.new('L', mask_size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + mask_size, fill=255)
        del draw
        mask = mask.resize((self.width, self.height), Image.ANTIALIAS)

        willow = self.putalpha(willow, mask)
        return willow


class CircleWithRingOperation(DrawBitmapOperation):
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
        if image.width < self.width or image.height < self.height:
            # unable to process image at all since the putalpha will fail
            return

        willow = super(CircleWithRingOperation, self).run(willow, image)

        ring_width = 3 * self.ring_width
        mask_size = (3 * self.width, 3 * self.height)
        mask = Image.new('L', mask_size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + mask_size, fill=255)
        draw.ellipse((ring_width, ring_width) + (3 * self.width - ring_width, 3 * self.height - ring_width), fill=0)
        mask = mask.resize((self.width, self.height), Image.ANTIALIAS)
        # mask.save('circle-ring1.png')
        ring_mask = mask
        del draw

        willow = self.draw_bitmap(willow, ring_mask, self.circle_color)

        mask = Image.new('L', mask_size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + mask_size, fill=255)
        mask = mask.resize((self.width, self.height), Image.ANTIALIAS)
        # mask.save('circle-ring2.png')
        del draw

        mask.paste(ring_mask, (0, 0), ring_mask)
        # mask.save('pasted.png')

        willow = self.putalpha(willow, mask)
        return willow
