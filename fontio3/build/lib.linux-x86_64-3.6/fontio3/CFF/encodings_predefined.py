#
# encodings_predefined.py
#
# Copyright © 2013-2014 Monotype Imaging Inc. All Rights Reserved.
#

"""
Support for predefined CFF Encodings.
"""

# System imports
import logging

# Other imports
from fontio3.CFF.cffutils import stdStrings
from fontio3.fontdata import mapmeta

# -----------------------------------------------------------------------------

#
# Constants
#

adobeStandardEncoding = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0,
  9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:0, 18:0, 19:0, 20:0,
  21:0, 22:0, 23:0, 24:0, 25:0, 26:0, 27:0, 28:0, 29:0, 30:0, 31:0,
  32:1, 33:2, 34:3, 35:4, 36:5, 37:6, 38:7, 39:8, 40:9, 41:10, 42:11,
  43:12, 44:13, 45:14, 46:15, 47:16, 48:17, 49:18, 50:19, 51:20, 52:21,
  53:22, 54:23, 55:24, 56:25, 57:26, 58:27, 59:28, 60:29, 61:30, 62:31,
  63:32, 64:33, 65:34, 66:35, 67:36, 68:37, 69:38, 70:39, 71:40, 72:41,
  73:42, 74:43, 75:44, 76:45, 77:46, 78:47, 79:48, 80:49, 81:50, 82:51,
  83:52, 84:53, 85:54, 86:55, 87:56, 88:57, 89:58, 90:59, 91:60, 92:61,
  93:62, 94:63, 95:64, 96:65, 97:66, 98:67, 99:68, 100:69, 101:70,
  102:71, 103:72, 104:73, 105:74, 106:75, 107:76, 108:77, 109:78,
  110:79, 111:80, 112:81, 113:82, 114:83, 115:84, 116:85, 117:86,
  118:87, 119:88, 120:89, 121:90, 122:91, 123:92, 124:93, 125:94,
  126:95, 127:0, 128:0, 129:0, 130:0, 131:0, 132:0, 133:0, 134:0, 135:0,
  136:0, 137:0, 138:0, 139:0, 140:0, 141:0, 142:0, 143:0, 144:0, 145:0,
  146:0, 147:0, 148:0, 149:0, 150:0, 151:0, 152:0, 153:0, 154:0, 155:0,
  156:0, 157:0, 158:0, 159:0, 160:0, 161:96, 162:97, 163:98, 164:99,
  165:100, 166:101, 167:102, 168:103, 169:104, 170:105, 171:106,
  172:107, 173:108, 174:109, 175:110, 176:0, 177:111, 178:112, 179:113,
  180:114, 181:0, 182:115, 183:116, 184:117, 185:118, 186:119, 187:120,
  188:121, 189:122, 190:0, 191:123, 192:0, 193:124, 194:125, 195:126,
  196:127, 197:128, 198:129, 199:130, 200:131, 201:0, 202:132, 203:133,
  204:0, 205:134, 206:135, 207:136, 208:137, 209:0, 210:0, 211:0, 212:0,
  213:0, 214:0, 215:0, 216:0, 217:0, 218:0, 219:0, 220:0, 221:0, 222:0,
  223:0, 224:0, 225:138, 226:0, 227:139, 228:0, 229:0, 230:0, 231:0,
  232:140, 233:141, 234:142, 235:143, 236:0, 237:0, 238:0, 239:0, 240:0,
  241:144, 242:0, 243:0, 244:0, 245:145, 246:0, 247:0, 248:146, 249:147,
  250:148, 251:149, 252:0, 253:0, 254:0, 255:0}
  
expertEncoding = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0,
  10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:0, 18:0, 19:0, 20:0,
  21:0, 22:0, 23:0, 24:0, 25:0, 26:0, 27:0, 28:0, 29:0, 30:0, 31:0,
  32:1, 33:229, 34:230, 35:0, 36:231, 37:232, 38:233, 39:234, 40:235,
  41:236, 42:237, 43:238, 44:13, 45:14, 46:15, 47:99, 48:239, 49:240,
  50:241, 51:242, 52:243, 53:244, 54:245, 55:246, 56:247, 57:248, 58:27,
  59:28, 60:249, 61:250, 62:251, 63:252, 64:0, 65:253, 66:254, 67:255,
  68:256, 69:257, 70:0, 71:0, 72:0, 73:258, 74:0, 75:0, 76:259, 77:260,
  78:261, 79:262, 80:0, 81:0, 82:263, 83:264, 84:265, 85:0, 86:266,
  87:109, 88:110, 89:267, 90:268, 91:269, 92:0, 93:270, 94:271, 95:272,
  96:273, 97:274, 98:275, 99:276, 100:277, 101:278, 102:279, 103:280,
  104:281, 105:282, 106:283, 107:284, 108:285, 109:286, 110:287,
  111:288, 112:289, 113:290, 114:291, 115:292, 116:293, 117:294,
  118:295, 119:296, 120:297, 121:298, 122:299, 123:300, 124:301,
  125:302, 126:303, 127:0, 128:0, 129:0, 130:0, 131:0, 132:0, 133:0,
  134:0, 135:0, 136:0, 137:0, 138:0, 139:0, 140:0, 141:0, 142:0, 143:0,
  144:0, 145:0, 146:0, 147:0, 148:0, 149:0, 150:0, 151:0, 152:0, 153:0,
  154:0, 155:0, 156:0, 157:0, 158:0, 159:0, 160:0, 161:304, 162:305,
  163:306, 164:0, 165:0, 166:307, 167:308, 168:309, 169:310, 170:311,
  171:0, 172:312, 173:0, 174:0, 175:313, 176:0, 177:0, 178:314, 179:315,
  180:0, 181:0, 182:316, 183:317, 184:318, 185:0, 186:0, 187:0, 188:158,
  189:155, 190:163, 191:319, 192:320, 193:321, 194:322, 195:323,
  196:324, 197:325, 198:0, 199:0, 200:326, 201:150, 202:164, 203:169,
  204:327, 205:328, 206:329, 207:330, 208:331, 209:332, 210:333,
  211:334, 212:335, 213:336, 214:337, 215:338, 216:339, 217:340,
  218:341, 219:342, 220:343, 221:344, 222:345, 223:346, 224:347,
  225:348, 226:349, 227:350, 228:351, 229:352, 230:353, 231:354,
  232:355, 233:356, 234:357, 235:358, 236:359, 237:360, 238:361,
  239:362, 240:363, 241:364, 242:365, 243:366, 244:367, 245:368,
  246:369, 247:370, 248:371, 249:372, 250:373, 251:374, 252:375,
  253:376, 254:377, 255:378}

# -----------------------------------------------------------------------------

#
# Classes
#

class Predefined(dict, metaclass=mapmeta.FontDataMetaclass):
    """
    Objects representing Predefined encoding.
    """
    
    mapSpec = dict(
        item_renumberdirectvalues = True,
        map_compactremovesfalses = True)    
    
    #
    # Initialization and class methods
    #
    
    @classmethod
    def fromvalidatednumber(cls, n, **kwArgs):
        """
        Like fromwalker(), this method returns a new Predefined Encoding.
        However, it also does extensive validation via the logging module (the
        client should have done a logging.basicConfig call prior to calling this
        method, unless a logger is passed in via the 'logger' keyword argument).
        
        >>> logger = utilities.makeDoctestLogger('test')
        >>> obj = Predefined.fromvalidatednumber(0, logger=logger)
        test.predefined - INFO - Adobe Standard Encoding
        >>> obj[9]
        0
        >>> obj = Predefined.fromvalidatednumber(1, logger=logger)
        test.predefined - INFO - Expert Encoding
        >>> obj[22]
        0
        >>> obj = Predefined.fromvalidatednumber(99, logger=logger)
        test.predefined - ERROR - Unknown predefined encoding designator 99
        """
        
        logger = kwArgs.pop('logger', None)
        
        if logger is None:
            logger = logging.getLogger().getChild('predefined')
        else:
            logger = logger.getChild('predefined')
        
        if n < 0 or n > 1:
            logger.error(('xxxxx', (n,), "Unknown predefined encoding designator %d"))
            return cls({})

        if n == 0:
            logger.info(('xxxxx', (), "Adobe Standard Encoding"))
            enc = adobeStandardEncoding
            
        elif n == 1:
            logger.info(('xxxxx', (), "Expert Encoding"))
            enc = expertEncoding

        return cls(enc)
    
    @classmethod
    def fromnumber(cls, n, **kwArgs):
        """
        Build a Predefined encoding, mapping code:glyphID from the specified Walker.
        
        >>> obj = Predefined.fromnumber(0)
        >>> obj[1]
        0
        >>> obj = Predefined.fromnumber(1)
        >>> obj[99]
        276
        """
        
        if n == 0:
            enc = adobeStandardEncoding
            
        elif n == 1:
            enc = expertEncoding
        
        else:
            raise ValueError("Unknown predefined encoding designator %d " % (n,))

        return cls(enc)
    
    #
    # Public methods
    #
    
    def buildBinary(self, w, **kwArgs):
        """
        Nothing to do here, really.
        """

        pass
        
# -----------------------------------------------------------------------------

#
# Test code
#

if 0:
    def __________________(): pass

if __debug__:
    from fontio3 import utilities
    
    _testingValues = (0, 1, 5)

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    if __debug__:
        _test()

