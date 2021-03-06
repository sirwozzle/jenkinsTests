#
# prop_v3.py
#
# Copyright © 2012, 2013 Monotype Imaging Inc. All Rights Reserved.
#

"""
Definitions for version 3 'prop' tables.
"""

# System imports
import collections
import logging
import operator

# Other imports
from fontio3.fontdata import mapmeta
from fontio3.prop import glyphproperties_v3, prop_v2
from fontio3.utilities import lookup

# -----------------------------------------------------------------------------

#
# Private functions
#

def _validate(obj, **kwArgs):
    logger = kwArgs.pop('logger')
    r = True
    
    for glyphIndex in sorted(obj):
        itemLogger = logger.getChild("glyph %d" % (glyphIndex,))
        
        thisGlyphIsOK = obj[glyphIndex].isValid(
          logger = itemLogger,
          glyphIndex = glyphIndex,
          **kwArgs)
        
        r = thisGlyphIsOK and r
    
    return r

# -----------------------------------------------------------------------------

#
# Classes
#

if 0:
    def __________________(): pass

class Prop(dict, metaclass=mapmeta.FontDataMetaclass):
    """
    Objects representing version 3 'prop' tables. These are dicts mapping glyph
    indices to GlyphProperties objects.
    
    >>> GP = Prop.GP
    >>> p1 = GP()
    >>> p2 = GP(floater=True, attachesRight=True)
    >>> d = Prop.fromkeys(range(20), p1)
    >>> d[12] = d[13] = d[14] = p2
    >>> utilities.hexdump(d.binaryString())
           0 | 0003 0000 0001 0000  0008 000C 0003 8080 |................|
          10 | 8080 8080                                |....            |
    
    >>> d = Prop.fromkeys(range(50), p1)
    >>> d[4] = d[42] = d[43] = d[44] = p2
    >>> utilities.hexdump(d.binaryString())
           0 | 0003 0000 0001 0000  0002 0006 0002 000C |................|
          10 | 0001 0000 0004 0004  8080 002C 002A 8080 |...........,.*..|
          20 | FFFF FFFF 0000                           |......          |
    """
    
    #
    # Class definition variables
    #
    
    mapSpec = dict(
        item_followsprotocol = True,
        item_pprintlabelpresort = True,
        item_renumberdirectkeys = True,
        item_usenamerforstr = True,
        map_validatefunc = _validate)
    
    GP = glyphproperties_v3.GlyphProperties
    tableVersion = 0x30000
    
    #
    # Methods
    #
    
    def asVersion2(self, **kwArgs):
        """
        Creates and returns a new version 2 Prop object from self.
        """
        
        f = self.GP.asVersion2  # unbound
        return prop_v2.Prop({k: f(v) for k, v in self.items()})
    
    def buildBinary(self, w, **kwArgs):
        """
        Adds the binary data for the Prop object to the specified LinkedWriter.
        
        >>> GP = Prop.GP
        >>> p1 = GP()
        >>> p2 = GP(floater=True)
        >>> d = Prop.fromkeys(range(20), p1)
        >>> d[12] = d[13] = d[14] = p2
        >>> utilities.hexdump(d.binaryString())
               0 | 0003 0000 0001 0000  0008 000C 0003 8000 |................|
              10 | 8000 8000                                |....            |
        
        >>> d = Prop.fromkeys(range(50), p1)
        >>> d[4] = d[42] = d[43] = d[44] = p2
        >>> utilities.hexdump(d.binaryString())
               0 | 0003 0000 0001 0000  0002 0006 0002 000C |................|
              10 | 0001 0000 0004 0004  8000 002C 002A 8000 |...........,.*..|
              20 | FFFF FFFF 0000                           |......          |
        """
        
        if 'stakeValue' in kwArgs:
            stakeValue = kwArgs.pop('stakeValue')
            w.stakeCurrentWithValue(stakeValue)
        else:
            stakeValue = w.stakeCurrent()
        
        w.add("L", self.tableVersion)
        fan = self.GP.asNumber
        d = {k: fan(gp, glyphIndex=k) for k, gp in self.items()}
        valueToCount = collections.defaultdict(int)
        
        for n in d.values():
            valueToCount[n] += 1
        
        if len(valueToCount) == 1:
            w.add("2H", 0, next(iter(valueToCount)))
            return
        
        freq = sorted(
          valueToCount.items(),
          key = operator.itemgetter(1),
          reverse = True)
        
        default = freq[0][0]
        w.add("2H", 1, default)
        d = {k: n for k, n in d.items() if n != default}
        lookup.Lookup(d).buildBinary(w, sentinelValue=0)
    
    @classmethod
    def fromvalidatedwalker(cls, w, **kwArgs):
        """
        Creates and returns a new Prop object from the specified walker, doing
        source validation. The following keyword arguments are supported:
        
            fontGlyphCount      The number of glyphs in the font. This is
                                required.
            
            logger              A logger to which messages will be posted.
        """
        
        logger = kwArgs.pop('logger', logging.getLogger())
        logger = logger.getChild("prop_v2")
        
        logger.debug((
          'V0001',
          (w.length(),),
          "Walker has %d remaining bytes."))
        
        if w.length() < 8:
            logger.error(('V0004', (), "Insufficient bytes."))
            return None
        
        version, hasLookup, default = w.unpack("L2H")
        
        if version != cls.tableVersion:
            logger.error((
              'V0002',
              (cls.tableVersion, version),
              "Was expecting version 0x%08X, but got 0x%08X instead."))
            
            return None
        
        fgc = kwArgs['fontGlyphCount']
        fvn = cls.GP.fromvalidatednumber
        default = fvn(default, logger=logger)
        
        if default is None:
            return None
        
        r = cls.fromkeys(range(fgc), default)
        
        if hasLookup:
            lk = lookup.Lookup.fromvalidatedwalker(
              w,
              sentinelValue = 0,
              logger = logger)
            
            if lk is None:
                return None
            
            for k, n in lk.items():
                obj = fvn(
                  n,
                  glyphIndex = k,
                  logger = logger.getChild("[%d]" % (k,)))
                
                if obj is None:
                    return None
                
                r[k] = obj
        
        return r
    
    @classmethod
    def fromversion2(cls, v2Obj, **kwArgs):
        """
        Creates and returns a new version 3 Prop object using the data in the
        specified version 2 object.
        """
        
        f = cls.GP.fromversion2
        return cls({k: f(v) for k, v in v2Obj.items()})
    
    @classmethod
    def fromwalker(cls, w, **kwArgs):
        """
        Creates and returns a new Prop object from the data in the specified
        walker. There is one required keyword argument:
        
            fontGlyphCount      The number of glyphs in the font.
        """
        
        version, hasLookup, default = w.unpack("L2H")
        assert version == cls.tableVersion
        fgc = kwArgs['fontGlyphCount']
        fn = cls.GP.fromnumber
        r = cls.fromkeys(range(fgc), fn(default))
        
        if hasLookup:
            lk = lookup.Lookup.fromwalker(w)
            
            for k, n in lk.items():
                r[k] = fn(n, glyphIndex=k)
        
        return r
    
# -----------------------------------------------------------------------------

#
# Test code
#

if 0:
    def __________________(): pass

if __debug__:
    from fontio3 import utilities

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    if __debug__:
        _test()
