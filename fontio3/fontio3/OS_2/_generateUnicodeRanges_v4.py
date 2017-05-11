#
# _generateUnicodeRanges_v4.py
#
# Copyright © 2010, 2016 Monotype Imaging Inc. All Rights Reserved.
#

"""
Code that recalculates fontio3.OS_2.unicoderanges._rangeData from the current
Unicode database in the Python unicodedata module. These data are for Version
4 OS/2 tables.

Just run this file and the new _rangeData will be output to stdout.
"""

import unicodedata

from fontio3.utilities import span

rawData = (
    (0, ((0x0000, 0x007F),)),
    (1, ((0x0080, 0x00FF),)),
    (2, ((0x0100, 0x017F),)),
    (3, ((0x0180, 0x024F),)),
    (4, ((0x0250, 0x02AF), (0x1D00, 0x1DBF), (0x1D80, 0x1DBF))),
    (5, ((0x02B0, 0x02FF), (0xA700, 0xA71F))),
    (6, ((0x0300, 0x036F), (0x1DC0, 0x1DFF))),
    (7, ((0x0370, 0x03FF),)),
    (8, ((0x2C80, 0x2CFF),)),
    (9, ((0x0400, 0x052F), (0x2DE0, 0x2DFF), (0xA640, 0xA69F))),
   (10, ((0x0530, 0x058F),)),
   (11, ((0x0590, 0x05FF),)),
   (12, ((0xA500, 0xA63F),)),
   (13, ((0x0600, 0x06FF), (0x0750, 0x077F))),
   (14, ((0x07C0, 0x07FF),)),
   (15, ((0x0900, 0x097F),)),
   (16, ((0x0980, 0x09FF),)),
   (17, ((0x0A00, 0x0A7F),)),
   (18, ((0x0A80, 0x0AFF),)),
   (19, ((0x0B00, 0x0B7F),)),
   (20, ((0x0B80, 0x0BFF),)),
   (21, ((0x0C00, 0x0C7F),)),
   (22, ((0x0C80, 0x0CFF),)),
   (23, ((0x0D00, 0x0D7F),)),
   (24, ((0x0E00, 0x0E7F),)),
   (25, ((0x0E80, 0x0EFF),)),
   (26, ((0x10A0, 0x10FF), (0x2D00, 0x2D2F))),
   (27, ((0x1B00, 0x1B7F),)),
   (28, ((0x1100, 0x11FF),)),
   (29, ((0x1E00, 0x1EFF), (0x2C60, 0x2C7F), (0xA720, 0xA7FF))),
   (30, ((0x1F00, 0x1FFF),)),
   (31, ((0x2000, 0x206F), (0x2E00, 0x2E7F))),
   (32, ((0x2070, 0x209F),)),
   (33, ((0x20A0, 0x20CF),)),
   (34, ((0x20D0, 0x20FF),)),
   (35, ((0x2100, 0x214F),)),
   (36, ((0x2150, 0x218F),)),
   (37, ((0x2190, 0x21FF), (0x27F0, 0x27FF), (0x2900, 0x297F), (0x2B00, 0x2BFF))),
   (38, ((0x2200, 0x22FF), (0x2A00, 0x2AFF), (0x27C0, 0x27EF), (0x2980, 0x29FF))),
   (39, ((0x2300, 0x23FF),)),
   (40, ((0x2400, 0x243F),)),
   (41, ((0x2440, 0x245F),)),
   (42, ((0x2460, 0x24FF),)),
   (43, ((0x2500, 0x257F),)),
   (44, ((0x2580, 0x259F),)),
   (45, ((0x25A0, 0x25FF),)),
   (46, ((0x2600, 0x26FF),)),
   (47, ((0x2700, 0x27BF),)),
   (48, ((0x3000, 0x303F),)),
   (49, ((0x3040, 0x309F),)),
   (50, ((0x30A0, 0x30FF), (0x31F0, 0x31FF))),
   (51, ((0x3100, 0x312F), (0x31A0, 0x31BF))),
   (52, ((0x3130, 0x318F),)),
   (53, ((0xA840, 0xA87F),)),
   (54, ((0x3200, 0x32FF),)),
   (55, ((0x3300, 0x33FF),)),
   (56, ((0xAC00, 0xD7AF),)),
   (57, ((0x10000, 0x10FFFF),)),
   (58, ((0x10900, 0x1091F),)),
   (59, ((0x4E00, 0x9FFF), (0x2E80, 0x2FDF), (0x2FF0, 0x2FFF), (0x3400, 0x4DBF), (0x20000, 0x2A6DF), (0x3190, 0x319F))),
   (60, ((0xE000, 0xF8FF),)),
   (61, ((0x31C0, 0x31EF), (0xF900, 0xFAFF), (0x2F800, 0x2FA1F))),
   (62, ((0xFB00, 0xFB4F),)),
   (63, ((0xFB50, 0xFDFF),)),
   (64, ((0xFE20, 0xFE2F),)),
   (65, ((0xFE10, 0xFE1F), (0xFE30, 0xFE4F))),
   (66, ((0xFE50, 0xFE6F),)),
   (67, ((0xFE70, 0xFEFF),)),
   (68, ((0xFF00, 0xFFEF),)),
   (69, ((0xFFF0, 0xFFFF),)),
   (70, ((0x0F00, 0x0FFF),)),
   (71, ((0x0700, 0x074F),)),
   (72, ((0x0780, 0x07BF),)),
   (73, ((0x0D80, 0x0DFF),)),
   (74, ((0x1000, 0x109F),)),
   (75, ((0x1200, 0x139F), (0x2D80, 0x2DDF))),
   (76, ((0x13A0, 0x13FF),)),
   (77, ((0x1400, 0x167F),)),
   (78, ((0x1680, 0x169F),)),
   (79, ((0x16A0, 0x16FF),)),
   (80, ((0x1780, 0x17FF), (0x19E0, 0x19FF))),
   (81, ((0x1800, 0x18AF),)),
   (82, ((0x2800, 0x28FF),)),
   (83, ((0xA000, 0xA4CF),)),
   (84, ((0x1700, 0x177F),)),
   (85, ((0x10300, 0x1032F),)),
   (86, ((0x10330, 0x1034F),)),
   (87, ((0x10400, 0x1044F),)),
   (88, ((0x1D000, 0x1D24F),)),
   (89, ((0x1D400, 0x1D7FF),)),
   (90, ((0xFF000, 0xFFFFD), (0x100000, 0x10FFFD))),
   (91, ((0xFE00, 0xFE0F), (0xE0100, 0xE01EF))),
   (92, ((0xE0000, 0xE007F),)),
   (93, ((0x1900, 0x194F),)),
   (94, ((0x1950, 0x197F),)),
   (95, ((0x1980, 0x19DF),)),
   (96, ((0x1A00, 0x1A1F),)),
   (97, ((0x2C00, 0x2C5F),)),
   (98, ((0x2D30, 0x2D7F),)),
   (99, ((0x4DC0, 0x4DFF),)),
  (100, ((0xA800, 0xA82F),)),
  (101, ((0x10000, 0x1013F),)),
  (102, ((0x10140, 0x1018F),)),
  (103, ((0x10380, 0x1039F),)),
  (104, ((0x103A0, 0x103DF),)),
  (105, ((0x10450, 0x1047F),)),
  (106, ((0x10480, 0x104AF),)),
  (107, ((0x10800, 0x1083F),)),
  (108, ((0x10A00, 0x10A5F),)),
  (109, ((0x1D300, 0x1D35F),)),
  (110, ((0x12000, 0x1247F),)),
  (111, ((0x1D360, 0x1D37F),)),
  (112, ((0x1B80, 0x1BBF),)),
  (113, ((0x1C00, 0x1C4F),)),
  (114, ((0x1C50, 0x1C7F),)),
  (115, ((0xA880, 0xA8DF),)),
  (116, ((0xA900, 0xA92F),)),
  (117, ((0xA930, 0xA95F),)),
  (118, ((0xAA00, 0xAA5F),)),
  (119, ((0x10190, 0x101CF),)),
  (120, ((0x101D0, 0x101FF),)),
  (121, ((0x10280, 0x102DF), (0x10920, 0x1093F))),
  (122, ((0x1F000, 0x1F09F),)))

def f(n):
    if n <= 0xFFFF:
        return "0x%04X" % (n,)
    else:
        return "0x%06X" % (n,)

class UInfo(object):
    def __init__(self):
        n = unicodedata.name
        s = set()
        
        for i in range(0x110000):
            try:
                if n(chr(i)) is not None:
                    s.add(i)
            
            except ValueError:
                pass
        
        self.allSpans = span.Span(s)
    
    def oSpan(self, key, thisSpan):
        thisSpan.intersectSpan(self.allSpans)
        v = list(thisSpan)
        
        if len(v) == 1:
            print("% 5s: frozenset(range(%s, %s))," % (str(key), f(v[0][0]), f(1 + v[0][1])))
        
        else:
            v.sort()
            s = ', '.join("range(%s, %s)" % (f(t[0]), f(1 + t[1])) for t in v)
            print("% 5s: frozenset(itertools.chain(%s))," % (str(key), s))
    
    def oSpanAsSpan(self, key, thisSpan):
        if key not in frozenset([60, 90]):
            thisSpan.intersectSpan(self.allSpans)
        
        thisSpan.stringOutputInHex = True
        print("% 5s: (None, f('%s'))," % (str(key), str(thisSpan)))
    
    def report(self):
        for key, pairs in rawData:
            thisSpan = span.SpanFromPairs(pairs)
            self.oSpan(key, thisSpan)
    
    def reportAsSpan(self):
        for key, pairs in rawData:
            thisSpan = span.SpanFromPairs(pairs)
            self.oSpanAsSpan(key, thisSpan)

if __name__ == "__main__":
    infoObj = UInfo()
    infoObj.reportAsSpan()