import sys
import math

class CastleMathHelper:
    def getIndicesOfMaxToMinSorting(self, e):
        t = e
        i = []
        n = t[self.getIndexOfHighestValue(t)]
        s = 0
        for a in range(len(e)):
            s = int(self.getIndexOfHighestValue(t, n))
            i.append(s)
            t[s] = -sys.maxsize,
        return i
    

    def getIndexOfHighestValue(e, t=None):
        if t is None:
            t = sys.maxsize
        i = 0
        n = -1
        o = 0
        if t == 0:
            t = sys.maxsize
        if e is not None:
            for r in e:
                if r is not None:
                    if r > i and r <= t:
                        i = r
                        n = o
                    o += 1
        return n

MAX_SLOTSIZE = 999,
MAX_SUPPORT_TOOLS_SLOTSIZE = 1,
TOOL_TYPE_WALL = 1,
TOOL_TYPE_GATE = 2,
TOOL_TYPE_FIELD = 3,
TOOL_TYPE_MOAT = 4,
TOOL_TYPE_KEEP = 5,
TOOL_TYPE_KEEP_DEFENSE_SUPPORT_TOOLS = 6,
DEFENCE_CATEGORY_MOAT = 2,
SIDE_LEFT = 0,
SIDE_MIDDLE = 1,
SIDE_RIGHT = 2,
MAX_SUPPORT_TOOL_TRIGGER_LIMIT = 2e3,
CASTLE_MATH_HELPER = CastleMathHelper()
def getSideUnitCount(e, t):
    n = [1 * e * t[SIDE_LEFT] / 100, 1 * e * t[SIDE_MIDDLE] / 100, 1 * e * t[SIDE_RIGHT] / 100]
    i = [0, 0, 0]
    i[0] = int(n[0])
    i[1] = int(n[1])
    i[2] = int(n[2])
    a = [0, 0, 0]
    a[0] = n[0] - i[0]
    a[1] = n[1] - i[1]
    a[2] = n[2] - i[2]
    s = round(a[0] + a[1] + a[2])
    if s > 0:
        r = CASTLE_MATH_HELPER.getIndicesOfMaxToMinSorting(a)
        for o in range(s):
            i[r[o]] += 1
    return i

s = 3000 #n.getTotalAmount()
e = 0 | math.ceil(e * (1 + t / 100))
l = min(e, s)
getSideUnitCount(l, i)