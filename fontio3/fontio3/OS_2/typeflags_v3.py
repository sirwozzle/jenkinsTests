#
# typeflags_v3.py
#
# Copyright © 2010, 2011 Monotype Imaging Inc. All Rights Reserved.
#

"""
Support for the embedding and subsetting flags in an OS/2 table.
"""

# System imports
import collections
import re

# Other imports
from fontio3.fontdata import maskmeta
from fontio3.OS_2 import typeflags_v2

# -----------------------------------------------------------------------------

#
# Private constants
#

_levelNames = collections.defaultdict(lambda: "Invalid embedding level", {
  0x0000: "Installable Embedding",
  0x0002: "Restricted License Embedding",
  0x0004: "Preview & Print Embedding",
  0x0008: "Editable Embedding"})
  
# -----------------------------------------------------------------------------

#
# Classes
#

class TypeFlags(object, metaclass=maskmeta.FontDataMetaclass):
    """
    >>> TypeFlags.fromnumber(0).pprint()
    Embedding Level: Installable Embedding
    
    >>> TypeFlags.fromnumber(0x0304).pprint()
    Embedding Level: Preview & Print Embedding
    No subsetting
    Bitmap embedding only
    """
    
    #
    # Class definition variables
    #
    
    maskByteLength = 2
    
    maskControls = dict(
        loggername = "fstype",
        validatecode_notsettozero = "E2102")
    
    maskSorted = ('embeddingLevel', 'noSubsetting', 'bitmapEmbeddingOnly')
    
    maskSpec = dict(
        embeddingLevel = dict(
            mask_bitcount = 4,
            mask_enumstringsdict = _levelNames,
            mask_isenum = True,
            mask_label = "Embedding Level",
            mask_rightmostbitindex = 0),
        
        noSubsetting = dict(
            mask_isbool = True,
            mask_label = "No subsetting",
            mask_rightmostbitindex = 8,
            mask_showonlyiftrue = True),
        
        bitmapEmbeddingOnly = dict(
            mask_isbool = True,
            mask_label = "Bitmap embedding only",
            mask_rightmostbitindex = 9,
            mask_showonlyiftrue = True))
    
    #
    # Class constants
    #
    
    _pat2to3 = re.compile(r" \(flags 0x000.\)$")
    
    #
    # Class methods
    #
    
    @classmethod
    def fromversion2(cls, v2Obj, **kwArgs):
        """
        Returns a new version 3 TypeFlags object from the specified
        version 2 TypeFlags object. There is one keyword argument:
        
            deferRecalculation  If True (the default), the fields will be
                                copied but no recalculation is done. The client
                                should do a recalculation, in this case. If
                                False, a recalculated() object will be
                                returned; in this case, the client should be
                                sure to pass in the needed keyword arguments
                                (usually editor and unicodeSpan, and perhaps
                                base1252 and threshold as well).
        """
        
        # Because version 3 TypeFlags object only allow a single bit on in bits
        # 0-3, we convert the enum string to ensure the right bit is set.
        
        s = cls._pat2to3.sub("", v2Obj.embeddingLevel)
        
        r = cls(
          embeddingLevel = s,
          noSubsetting = v2Obj.noSubsetting,
          bitmapEmbeddingOnly = v2Obj.bitmapEmbeddingOnly)
        
        if kwArgs.get('deferRecalculation', True):
            return r
        
        return r.recalculated(**kwArgs)
    
    #
    # Public methods
    #
    
    def asVersion2(self, **kwArgs):
        """
        Returns a version 3 TypeFlags object from the data in self. There
        is one keyword argument:
        
            deferRecalculation  If True (the default), the fields will be
                                copied but no recalculation is done. The client
                                should do a recalculation, in this case. If
                                False, a recalculated() object will be
                                returned; in this case, the client should be
                                sure to pass in the needed keyword arguments
                                (usually editor and unicodeSpan, and perhaps
                                base1252 and threshold as well).
        """
        
        r = typeflags_v2.TypeFlags(
          embeddingLevel = self.embeddingLevel,  # no conversion needed in this direction
          noSubsetting = self.noSubsetting,
          bitmapEmbeddingOnly = self.bitmapEmbeddingOnly)
        
        if kwArgs.get('deferRecalculation', True):
            return r
        
        return r.recalculated(**kwArgs)

# -----------------------------------------------------------------------------

#
# Test code
#

if 0:
    def __________________(): pass

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    if __debug__:
        _test()
