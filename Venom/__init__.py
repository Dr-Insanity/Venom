"""
Venom selfbot library
~~~~~~~~~~~~~~~~~~~
Nuking discord servers with nukes the nazis can only dream of
"""
from .embeds import Embed
from .colour import Colour
from .types import TerminalLogType, TerminalSeverities, OccuredEventTypes

EventOccured = TerminalLogType.EventOccured
ExecutedCommmand = TerminalLogType.ExecutedCommmand
Testing = TerminalLogType.Testing

INFO, TEST, WARN, FATAL = TerminalSeverities.INFO, TerminalSeverities.TEST, TerminalSeverities.WARN, TerminalSeverities.FATAL

Color = Colour
__all__ = ['Embed', 'Colour', 'Color', 'ExecutedCommmand', 'EventOccured', 'INFO', 'WARN', 'FATAL', 'TEST', 'OccuredEventTypes']