#
# hint_srp0.py
#
# Copyright © 2014 Monotype Imaging Inc. All Rights Reserved.
#

"""
Support for the SRP0 opcode.
"""

# Other imports
from fontio3.hints.common import doNotProceedPC

# -----------------------------------------------------------------------------

#
# Functions
#

def hint_SRP0(self, **kwArgs):
    """
    SRP0: Set reference point 0, opcode 0x10
    
    >>> logger = utilities.makeDoctestLogger("SRP0_test")
    >>> _popSync, _testingState = _testFuncs()
    >>> h = _testingState(19)
    >>> hint_SRP0(h, logger=logger)
    >>> len(h.state.stack) == len(h.state.pushHistory)
    True
    >>> h.state.graphicsState.referencePoint0
    19
    >>> pp.PP().mapping_deep_smart(h.state.refPtHistory, lambda x: False)
    0: Extra index 0 in PUSH opcode index 0 in test
    1: (no data)
    2: (no data)
    >>> hint_SRP0(h, logger=logger)
    SRP0_test - CRITICAL - Stack underflow in test (PC 1).
    """
    
    state = self.state
    logger = self._getLogger(**kwArgs)
    n = self._popRemove(state, 'stack')
    
    if n is None:
        state.assign('pc', doNotProceedPC)
        return
    
    h = self._popRemove(state, 'pushHistory')
    
    if h is None:
        state.assign('pc', doNotProceedPC)
        return
    
    state.assignDeep('graphicsState', 'referencePoint0', n)
    state.refPtHistory[0] = h
    state.changed('refPtHistory')
    
    if 'fdefEntryStack' in kwArgs:
        # We only note graphicsState effects when a FDEF stack is available
        
        state.statistics.noteGSEffect(
          tuple(kwArgs['fdefEntryStack']),
          state.pc + self.ultDelta)
    
    # Can't check maxima because there is no zone here. This means we rely
    # on the maxima checks in opcodes that use the reference points.
    
    fatObj = kwArgs.get('fdefArgTracer', None)
    
    if fatObj is not None:
        fatObj.notePop('pointIndex', 'SRP0')
    
    state.assign('pc', state.pc + 1)

# -----------------------------------------------------------------------------

#
# Test code
#

if 0:
    def __________________(): pass

if __debug__:
    from fontio3 import utilities
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
