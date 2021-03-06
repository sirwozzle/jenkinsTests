#
# hint_mazdelta.py
#
# Copyright © 2014 Monotype Imaging Inc. All Rights Reserved.
#

"""
Support for the MAZDELTA opcode.
"""

# Other imports
from fontio3.hints.common import doNotProceedPC

# -----------------------------------------------------------------------------

#
# Functions
#

def hint_MAZDELTA(self, **kwArgs):
    """
    MAZDELTA: Edge deltas, opcodes 0xA2-0xA4
    
    >>> logger = utilities.makeDoctestLogger("MAZDELTA_test")
    >>> _popSync, _testingState = _testFuncs()
    >>> h = _testingState(100, 100, 2, 8)
    >>> hint_MAZDELTA(h, logger=logger)
    >>> len(h.state.stack) == len(h.state.pushHistory)
    True
    >>> h.state.statistics.maxima.point
    8
    >>> hint_MAZDELTA(h, logger=logger)
    MAZDELTA_test - CRITICAL - Stack underflow in test (PC 1).
    """
    
    state = self.state
    logger = self._getLogger(**kwArgs)
    p = self._popRemove(state, 'stack', coerceToCollection=True)
    
    if p is None:
        state.assign('pc', doNotProceedPC)
        return
    
    history = self._popRemove(state, 'pushHistory')
    
    if history is None:
        state.assign('pc', doNotProceedPC)
        return
    
    count = self._popRemove(state, 'stack')
    
    if count is None:
        state.assign('pc', doNotProceedPC)
        return
    
    count = self._toNumber(count)
    
    if count is None:
        state.assign('pc', doNotProceedPC)
        return
    
    if self._popRemove(state, 'stack', count, **kwArgs) is None:
        state.assign('pc', doNotProceedPC)
        return
    
    if self._popRemove(state, 'pushHistory', count + 1, **kwArgs) is None:
        state.assign('pc', doNotProceedPC)
        return
    
    if self._zoneCheck("MAZDELTA", (0,), logger):
        zp0 = state.graphicsState.zonePointer0
        
        if self._pointCheck(
          "MAZDELTA",
          [(zp0, p, True)],
          logger,
          kwArgs.get('extraInfo', {})):
            
            state.statistics.addHistory('pointMoved', (zp0, p), history)
    
    fatObj = kwArgs.get('fdefArgTracer', None)
    
    if fatObj is not None:
        fatObj.notePop('pointIndex', 'MAZDELTA')
        fatObj.notePop(None, 'MAZDELTA')
        
        for i in range(count):
            fatObj.notePop('deltaArg', 'MAZDELTA')
    
    state.assign('pc', state.pc + 1)

# -----------------------------------------------------------------------------

#
# Test code
#

if 0:
    def __________________(): pass

if __debug__:
    from fontio3 import utilities
    
    def _testFuncs():
        from fontio3.hints import hints_tt
        return hints_tt._popSync, hints_tt._testingState

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    if __debug__:
        _test()
