#
# hint_max.py
#
# Copyright © 2014 Monotype Imaging Inc. All Rights Reserved.
#

"""
Support for the MAX opcode.
"""

# Other imports
from fontio3.hints.common import doNotProceedPC
from fontio3.hints.history import op

# -----------------------------------------------------------------------------

#
# Functions
#

def hint_MAX(self, **kwArgs):
    """
    MAX: Maximum, opcode 0x8B
    
    >>> logger = utilities.makeDoctestLogger("MAX_test")
    >>> _popSync, _testingState = _testFuncs()
    >>> h = _testingState(Collection([Triple(1, 13, 2)]), 8, -12, 3)
    >>> h.append(opcode_tt.Opcode_nonpush(nameToOpcodeMap["MAX"]))
    >>> hint_MAX(h, logger=logger)
    >>> len(h.state.stack) == len(h.state.pushHistory)
    True
    >>> h.state.stack[-1]
    3
    >>> h.state.assign('pc', 0)
    >>> hint_MAX(h, logger=logger)
    >>> h.state.stack[-1]
    8
    >>> h.state.assign('pc', 0)
    >>> hint_MAX(h, logger=logger)
    >>> h.state.stack[-1]
    Singles: [8, 9, 11]
    >>> pp.PP().sequence_deep(h.state.pushHistory)
    Result of opcode MAX at index 0 in test, with inputs:
      Extra index 0 in PUSH opcode index 0 in test
      Result of opcode MAX at index 0 in test, with inputs:
        Extra index 1 in PUSH opcode index 0 in test
        Result of opcode MAX at index 0 in test, with inputs:
          Extra index 2 in PUSH opcode index 0 in test
          Extra index 3 in PUSH opcode index 0 in test
    >>> hint_MAX(h, logger=logger)
    MAX_test - CRITICAL - Stack underflow in test (PC 1).
    """
    
    state = self.state
    logger = self._getLogger(**kwArgs)
    t = self._popRemove(state, 'stack', 2, coerceToCollection=True)
    
    if t is None:
        state.assign('pc', doNotProceedPC)
        return
    
    e1, e2 = t
    t = self._popRemove(state, 'pushHistory', 2)
    
    if t is None:
        state.assign('pc', doNotProceedPC)
        return
    
    h1, h2 = t
    n = e1.collectionMax(e2)
    n2 = n.toNumber()
    
    if n2 is not None:
        n = n2
    
    state.append('stack', n)
    
    state.append(
      'pushHistory',
      op.HistoryEntry_op(
        hintsObj = (id(self.ultParent), self.ultParent), 
        hintsPC = state.pc + self.ultDelta,
        opcode = self[state.pc].opcode,
        historyIterable = [h1, h2]))
    
    fatObj = kwArgs.get('fdefArgTracer', None)
    
    if fatObj is not None:
        argIndex1 = fatObj.notePop(None, 'MAX')
        argIndex2 = fatObj.notePop(None, 'MAX')
        
        if (argIndex1 is not None) and (argIndex2 is not None):
            if not isinstance(argIndex1, tuple):
                argIndex1 = (argIndex1,)
            
            if not isinstance(argIndex2, tuple):
                argIndex2 = (argIndex2,)
            
            argIndex = frozenset(argIndex1 + argIndex2)
            
            if len(argIndex) == 1:
                argIndex = next(iter(argIndex))
        
        elif argIndex1 is not None:
            argIndex = argIndex1
        
        elif argIndex2 is not None:
            argIndex = argIndex2
        
        else:
            argIndex = None
        
        fatObj.notePush(argIndex=argIndex)
    
    state.assign('pc', state.pc + 1)

# -----------------------------------------------------------------------------

#
# Test code
#

if 0:
    def __________________(): pass

if __debug__:
    from fontio3 import utilities
    from fontio3.hints import opcode_tt
    from fontio3.hints.common import nameToOpcodeMap
    from fontio3.triple.collection import Collection
    from fontio3.triple.triple import Triple
    from fontio3.utilities import pp
    
    def _testFuncs():
        from fontio3.hints import hints_tt
        return hints_tt._popSync, hints_tt._testingState

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    if __debug__:
        _test()
