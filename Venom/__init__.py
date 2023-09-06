import inspect
import urllib.parse

class Embed:
    """An embed"""
    def __init__(self, *, color: int=None, title: str=None, description: str=None, url: str=None):
        self.title = title if title is not None else ""
        self.description = description if description is not None else ""
        self.url = url if url is not None else ""
        self.color = color if color is not None else 0xfff
        self._hidephrase = "||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​|| _ _ _ _ _ _"

    def generate_url(self):
        raw_embed = {}
        for k, v in self.__dict__.items():
            if not k.startswith("_"):
                raw_embed[k] = v
        embed = f"{self._hidephrase}https://appembed.netlify.app/e?" + urllib.parse.urlencode(raw_embed)
        return embed

    def __repr__(self) -> str:
        inner = ', '.join((f'{k}={v!r}' for k, v in self.__dict__.items() if not k.startswith('_')))
        return f'Embed({inner})'

    def __str__(self) -> str:
        """
        Return the url of the embed.

        Returns:
            str: The url of the embed.
        """

        return self.generate_url()

class Color:
    def teal():
        """A factory method that returns a :class:`Colour` with a value of ``0x1ABC9C``."""
        return "#1ABC9C"


    def dark_teal():
        """A factory method that returns a :class:`Colour` with a value of ``0x11806A``."""
        return "#11806A"


    def brand_green():
        """A factory method that returns a :class:`Colour` with a value of ``0x57F287``."""
        return "#57F287"


    def green():
        """A factory method that returns a :class:`Colour` with a value of ``0x2ECC71``."""
        return "#2ECC71"


    def dark_green():
        """A factory method that returns a :class:`Colour` with a value of ``0x1F8B4C``."""
        return "#1F8B4C"


    def blue():
        """A factory method that returns a :class:`Colour` with a value of ``0x3498DB``."""
        return "#3498DB"


    def dark_blue():
        """A factory method that returns a :class:`Colour` with a value of ``0x206694``."""
        return "#206694"


    def purple():
        """A factory method that returns a :class:`Colour` with a value of ``0x9B59B6``."""
        return "#9B59B6"


    def dark_purple():
        """A factory method that returns a :class:`Colour` with a value of ``0x71368A``."""
        return "#71368A"


    def magenta():
        """A factory method that returns a :class:`Colour` with a value of ``0xE91E63``."""
        return "#E91E63"


    def dark_magenta():
        """A factory method that returns a :class:`Colour` with a value of ``0xAD1457``."""
        return "#AD1457"


    def gold():
        """A factory method that returns a :class:`Colour` with a value of ``0xF1C40F``."""
        return "#F1C40F"


    def dark_gold():
        """A factory method that returns a :class:`Colour` with a value of ``0xC27C0E``."""
        return "#C27C0E"


    def orange():
        """A factory method that returns a :class:`Colour` with a value of ``0xE67E22``."""
        return "#E67E22"


    def dark_orange():
        """A factory method that returns a :class:`Colour` with a value of ``0xA84300``."""
        return "#A84300"

    def brand_red():
        """A factory method that returns a :class:`Colour` with a value of ``0xED4245``."""
        return "#ED4245"

    def red():
        """A factory method that returns a :class:`Colour` with a value of ``0xE74C3C``."""
        return "#E74C3C"


    def dark_red():
        """A factory method that returns a :class:`Colour` with a value of ``0x992D22``."""
        return "#992D22"

    def lighter_grey():
        """A factory method that returns a :class:`Colour` with a value of ``0x95A5A6``."""
        return "#95A5A6"

    def dark_grey():
        """A factory method that returns a :class:`Colour` with a value of ``0x607d8b``."""
        return "#607D8B"

    def light_grey():
        """A factory method that returns a :class:`Colour` with a value of ``0x979C9F``."""
        return "#979C9F"

    def darker_grey():
        """A factory method that returns a :class:`Colour` with a value of ``0x546E7A``."""
        return "#546E7A"


    def og_blurple():
        """A factory method that returns a :class:`Colour` with a value of ``0x7289DA``."""
        return "#7289DA"


    def blurple():
        """A factory method that returns a :class:`Colour` with a value of ``0x5865F2``."""
        return "#5865F2"


    def greyple():
        """A factory method that returns a :class:`Colour` with a value of ``0x99AAB5``."""
        return "#99AAB5"


    def dark_theme():
        """A factory method that returns a :class:`Colour` with a value of ``0x313338``.\n\nThis will appear transparent on Discord's dark theme."""
        return "#313338"


    def fuchsia():
        """A factory method that returns a :class:`Colour` with a value of ``0xEB459E``."""
        return "#EB459E"


    def yellow():
        """A factory method that returns a :class:`Colour` with a value of ``0xFEE75C``."""
        return "#FEE75C"


    def dark_embed():
        """A factory method that returns a :class:`Colour` with a value of ``0x2B2D31``."""
        return "#2B2D31"


    def light_embed():
        """A factory method that returns a :class:`Colour` with a value of ``0xEEEFF1``."""
        return "#EEEFF1"