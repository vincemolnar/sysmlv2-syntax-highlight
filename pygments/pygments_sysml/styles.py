"""
    pygments_sysml.styles
    ~~~~~~~~~~~~~~~~~~~~~

    A style reproducing the Eclipse editor of the SysML v2 Pilot
    Implementation. The Pilot uses the default colours of Xtext
    (DefaultHighlightingConfiguration) and shows numbers in the default text
    style (KerMLHighlightingConfiguration). Regular comments, which the lexers
    of this package classify as String, and symbols are plain, as in the
    Pilot: only quoted strings get the string colour.

    :license: MIT, see LICENSE for details.
"""

from pygments.style import Style
from pygments.token import Comment, Keyword, String

__all__ = ['SysMLPilotStyle']


class SysMLPilotStyle(Style):
    """
    The colours of the SysML v2 Pilot Implementation's Eclipse editor.
    """

    name = 'sysml-pilot'
    background_color = '#ffffff'

    styles = {
        Keyword: 'bold #7f0055',
        Comment: '#3f7f5f',
        String.Double: '#2a00ff',
        String.Escape: '#2a00ff',
    }
