#
# hint_rtdg.py
#
# Copyright © 2014 Monotype Imaging Inc. All Rights Reserved.
#

"""
Support for the RTDG opcode.
"""

# Other imports
from fontio3.hints.graphicsstate import half26Dot6, quarter26Dot6, zero26Dot6

# -----------------------------------------------------------------------------

#
# Functions
#

def hint_RTDG(self, **kwArgs):
    """
    RTDG: Set round mode to "round to double grid", opcode 0x3D
    
    >>> logger = utilities.makeDoctestLogger("RTDG_test")
    >>> _popSync, _testingState = _testFuncs()
    >>> h = _testingState()
    >>> h.state.graphicsState.roundState
    [Singles: [1.0], Singles: [0.0], Singles: [0.5]]
    >>> hint_RTDG(h, logger=logger)
    >>> h.state.graphicsState.roundState
    [Singles: [0.5], Singles: [0.0], Singles: [0.25]]
    """
    
    state = self.state
    gs = state.graphicsState
    rs = gs.roundState
    need = [half26Dot6, zero26Dot6, quarter26Dot6]
    
    if rs != need:
        rs[:] = need
        gs.changed('roundState')
        state.changed('graphicsState')
    
    if 'fdefEntryStack' in kwArgs:
        # We only note graphicsState effects when a FDEF stack is available
        
        state.statistics.noteGSEffect(
          tuple(kwArgs['fdefEntryStack']),
          state.pc + self.ultDelta)
    
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
