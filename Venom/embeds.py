from typing import Union, TYPE_CHECKING
import urllib.parse
if TYPE_CHECKING:
    import venom

class Embed:
    """
    Embed
    ~~~~~~~~~~~~~~~~~~~
    Send an embed. Commonly used in discord bots as UI (User Interface), offering a higher user-friendliness than simple text

    #### Note:
    Embeds for selfbots are LIMITED in several ways compared to the embeds sent by real bots. 
    
    #### Here are some of the major limitations:
    - Embed descriptions are limited to 2000 characters
    - No markdown
    - No footer text
    - No additional fields

    Apologies for these limitations. Perhaps in the future, HTML can grant some of these limitations.
    """
    def __init__(
        self, 
        title: str=None, 
        description: str=None, 
        url: str=None, 
        color: Union[str, "venom.Color"]=None
        ):
        """
        Construct a new Embed
        
        Parameters
        ----------
        [Optional] color: Can be a hex string, like "#FFCC00" or simply venom.Colour or venom.Colour. Call their attributes to return a hex string. For example: venom.Colour.red()
        [Optional] title:
        [Optional] description:
        [Optional] url:
        """
        self.title = title if title is not None else ""
        self.description = description if description is not None else ""
        self.url = url if url is not None else ""
        self.color = color if color is not None else "#000000"
        self._hidephrase = "||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​|| _ _ _ _ _ _"

    def generate_url(self):
        raw_embed = {}
        for k, v in self.__dict__.items():
            if not k.startswith("_"):
                raw_embed[k] = v
        print(raw_embed)
        embed = f"{self._hidephrase}https://discordembeds.vercel.app/embed?" + urllib.parse.urlencode(raw_embed)
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