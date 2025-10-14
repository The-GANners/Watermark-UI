from PIL import Image
from PIL import ImageDraw, ImageFont  # NEW
from PIL import ImageColor  # NEW
import os
from FreeMark.tools.help import clamp


class WaterMarker:
    """Object for applying a free_mark to images"""
    def __init__(self, watermark_path, overwrite=False):
        self.overwrite = overwrite

        self.watermark_ratio = None
        self.watermark = None
        self.watermark_copy = None
        self.previous_size = None
        self.needs_opacity = None

        self.landscape_scale_factor = 0.15
        self.portrait_scale_factor = 0.30
        self.equal_scale_factor = 0.20
        self.min_scale = 0.5
        self.max_scale = 3

        # Prepare the watermarker
        try:
            if watermark_path:
                self.watermark = Image.open(watermark_path)
                self.watermark_ratio = self.watermark.size[0] / self.watermark.size[1]
            else:
                # Text mode: defer creation until apply_watermark
                self.watermark = None
                self.watermark_ratio = None
        except FileNotFoundError:
            raise FileNotFoundError("Watermark not found, please click the "
                                    "\"Choose watermark\" button")
        except OSError:
            raise OSError("Watermark image is of incompatible type.")

    def clean(self):
        """
        Forget the currently loaded free_mark
        """
        self.watermark_ratio = None
        self.watermark = None

    def apply_watermark(self, input_path, output_path, scale=True,
                        pos="SE", padding=((20, "px"), (5, "px")),
                        opacity=0.5, mode="image", text=None, text_size=32, text_color="#FFFFFF"):
        """
        Apply a free_mark to an image
        :param input_path: path to image on disk as a string
        :param output_path: save destination (path) as a string
        :param scale: Bool, scale free_mark
        :param opacity: free_mark opacity (a value between 0 and 1)
        :param pos: Assumes first char is y (N/S) and second is x (E/W)
        :param padding: padding in format ((x_pad, unit), (y_pad, unit))
        """
        # Don't overwrite existing files unless asked to
        if os.path.isfile(output_path) and not self.overwrite:
            return

        image = Image.open(input_path)

        # NEW: Determine watermark source (image or text)
        if mode == "text" and text:
            # Create a fresh RGBA text watermark
            self.watermark_copy = self.create_text_watermark(text, text_size, text_color, opacity)
            self.needs_opacity = False  # already baked into alpha
        else:
            # Image watermark path flow (existing)
            if scale and \
                    (not self.previous_size or self.previous_size != image.size):
                self.watermark_copy = self.scale_watermark(image)
                if opacity < 1:
                    self.needs_opacity = True
                else:
                    self.needs_opacity = False
            elif not self.watermark_copy:
                self.watermark_copy = self.watermark.copy()
                if opacity < 1:
                    self.needs_opacity = True
                else:
                    self.needs_opacity = False

        self.previous_size = image.size

        # Change free_mark opacity (only for image watermark)
        if self.needs_opacity:
            self.watermark_copy = self.change_opacity(self.watermark_copy, opacity)
            self.needs_opacity = False

        position = self.get_watermark_position(image, self.watermark_copy,
                                               pos=pos, padding=padding)

        try:
            image.paste(self.watermark_copy, box=position,
                        mask=self.watermark_copy)
        except ValueError:
            image.paste(self.watermark_copy, box=position)
        image.save(output_path)

    @staticmethod
    def change_opacity(image, opacity):
        """
        Change opacity of an image.
        :param image: PIL image object.
        :param opacity: Opacity as a factor (number between 0.0 and 1.0)
        :return: Image with new opacity
        """
        assert 0.0 <= opacity <= 1.0, "opacity must be between 0 and 1"
        image = image.convert("RGBA")
        img_data = image.load()
        new_data = []

        width, height = image.size
        for y in range(height):
            for x in range(width):
                if img_data[x, y][3] > 5:
                    new_data.append((img_data[x, y][0],
                                     img_data[x, y][1],
                                     img_data[x, y][2],
                                     int(img_data[x, y][3]*opacity)))
                else:
                    new_data.append(img_data[x, y])

        image.putdata(new_data)
        return image

    def scale_watermark(self, image):
        """
        Get a scaled copy of the currently loaded free_mark,
        tries to scale it to from input image's size and orientation
        :param image: PIL image object that free_mark will be applied to
        :return: scaled copy of currently loaded free_mark as PIL image object
        """
        image_width, image_height = image.size

        # Calculate new free_mark size
        if image_width > image_height:
            # Scales the width of the free_mark based on the width of the image
            # while keeping within min/max values
            new_width = int(clamp(image_width * self.landscape_scale_factor,
                                  self.watermark.size[0] * self.min_scale,
                                  self.watermark.size[0] * self.max_scale))
        # Image is in the portrait position
        elif image_width < image_height:
            new_width = int(clamp(image_width * self.portrait_scale_factor,
                                  self.watermark.size[0] * self.min_scale,
                                  self.watermark.size[0] * self.max_scale))
        # Image is equal sided
        else:
            new_width = int(clamp(image_width * self.equal_scale_factor,
                                  self.watermark.size[0] * self.min_scale,
                                  self.watermark.size[0] * self.max_scale))

        # Determine height from new width and old height/width ratio
        new_height = int(new_width / self.watermark_ratio)

        # Apply it
        return self.watermark.copy().resize((new_width, new_height))

    @staticmethod
    def get_watermark_position(image, watermark, pos="SE",
                               padding=((20, "px"), (5, "px"))):
        """
        Calculate position to place the free_mark
        :param image: image object of image
        :param watermark: image object of free_mark
        :param pos: Assumes first char is y (N/S) and second is x (E/W)
        :param padding: padding in format ((x_pad, unit), (y_pad, unit))
        :return: (x, y) coordinates to place the upper left coordinates
        """
        # Normalize and validate
        assert padding[0][1] and padding[1][1] in ["px", "%"], "unit must be px or %"
        pos = (pos or "SE").upper().strip()

        # Center placement (ignores padding for simplicity)
        if pos in ("C", "CENTER"):
            x = (image.size[0] - watermark.size[0]) // 2
            y = (image.size[1] - watermark.size[1]) // 2
            return x, y

        # Cardinal placement with padding
        assert pos[0] in ['N', 'S'], "first char of pos must be N or S"
        assert pos[1] in ['E', 'W'], "second char of pos must be E or W"

        # Get padding size
        if padding[0][1] == "%":
            padx = int(image.size[0] * (padding[0][0] / 100))
        else:
            padx = padding[0][0]

        if padding[1][1] == "%":
            pady = int(image.size[1] * (padding[1][0] / 100))
        else:
            pady = padding[1][0]

        if pos[0] == "S":
            y = image.size[1] - watermark.size[1] - pady
        else:
            y = pady
        if pos[1] == "E":
            x = image.size[0] - watermark.size[0] - padx
        else:
            # FIX: use horizontal padding for X, not pady
            x = padx
        return x, y

    # NEW: Render text watermark image
    # NEW: Parse color from hex or common color names (with a few aliases)
    @staticmethod
    def _parse_color(color_str, default=(255, 255, 255)):
        if not color_str or not isinstance(color_str, str):
            return default
        s = color_str.strip()
        # Try Pillow's color parser first (supports many English color names and hex)
        try:
            rgb = ImageColor.getrgb(s)
            return rgb if isinstance(rgb, tuple) else default
        except Exception:
            pass
        # Minimal multilingual aliases
        aliases = {
            # English
            'red': '#ff0000', 'green': '#008000', 'blue': '#0000ff', 'yellow': '#ffff00',
            'black': '#000000', 'white': '#ffffff', 'gray': '#808080', 'grey': '#808080',
            # Spanish
            'rojo': '#ff0000', 'verde': '#008000', 'azul': '#0000ff', 'amarillo': '#ffff00',
            'negro': '#000000', 'blanco': '#ffffff', 'gris': '#808080',
            # French
            'rouge': '#ff0000', 'vert': '#008000', 'bleu': '#0000ff', 'jaune': '#ffff00',
            'noir': '#000000', 'blanc': '#ffffff', 'gris': '#808080',
            # German
            'rot': '#ff0000', 'grün': '#008000', 'blau': '#0000ff', 'gelb': '#ffff00',
            'schwarz': '#000000', 'weiß': '#ffffff', 'weiss': '#ffffff', 'grau': '#808080',
        }
        key = s.strip().lower()
        if key in aliases:
            try:
                return ImageColor.getrgb(aliases[key])
            except Exception:
                return default
        # Fallback: parse hex manually (#RRGGBB)
        try:
            h = s.lstrip('#')
            if len(h) == 6:
                r = int(h[0:2], 16)
                g = int(h[2:4], 16)
                b = int(h[4:6], 16)
                return (r, g, b)
        except Exception:
            pass
        return default

    def create_text_watermark(self, text, font_size, color_hex, opacity):
        # Choose font
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except Exception:
            font = ImageFont.load_default()
        # Measure text
        dummy = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
        draw = ImageDraw.Draw(dummy)
        try:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]
        except Exception:
            text_w, text_h = draw.textsize(text, font=font)
        # Create image
        pad = 4
        wm_img = Image.new("RGBA", (text_w + 2 * pad, text_h + 2 * pad), (0, 0, 0, 0))
        draw = ImageDraw.Draw(wm_img)
        base_rgb = self._parse_color(color_hex)  # CHANGED: accept name or hex
        alpha = max(0, min(255, int(255 * opacity)))
        draw.text((pad, pad), text, font=font, fill=(base_rgb[0], base_rgb[1], base_rgb[2], alpha))
        return wm_img

    # NEW: In-memory apply (PIL in, PIL out)
    def apply_watermark_pil(self, pil_image, scale=True,
                            pos="SE", padding=((20, "px"), (5, "px")),
                            opacity=0.5, mode="image", text=None, text_size=32, text_color="#FFFFFF"):
        """
        Apply watermark to a PIL image and return a new PIL image (no file I/O).
        Parameters mirror apply_watermark.
        """
        image = pil_image.convert("RGBA")

        # Build watermark copy (image or text)
        if mode == "text" and text:
            wm = self.create_text_watermark(text, text_size, text_color, opacity)
            needs_opacity = False
        else:
            # Image watermark (follow existing logic)
            if scale and (not self.previous_size or self.previous_size != image.size):
                wm = self.scale_watermark(image)
                needs_opacity = opacity < 1
            else:
                wm = (self.watermark or Image.new("RGBA", (1, 1), (0, 0, 0, 0))).copy()
                needs_opacity = opacity < 1

        self.previous_size = image.size

        if needs_opacity and wm.mode != "RGBA":
            wm = wm.convert("RGBA")
        if needs_opacity:
            wm = self.change_opacity(wm, opacity)

        x, y = self.get_watermark_position(image, wm, pos=pos, padding=padding)

        out = image.copy()
        try:
            out.paste(wm, box=(x, y), mask=wm)
        except ValueError:
            out.paste(wm, box=(x, y))
        return out.convert("RGBA")
