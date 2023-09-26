import math
import sys

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


class DefenseConst:
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
    MAX_SUPPORT_TOOL_TRIGGER_LIMIT = 2e3
    CASTLE_MATH_HELPER = CastleMathHelper()
    
    def getSideUnitCount(self, e, t):
        n = [1 * e * t[self.SIDE_LEFT] / 100, 1 * e * t[self.SIDE_MIDDLE] / 100, 1 * e * t[self.SIDE_RIGHT] / 100]
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
            r = self.CASTLE_MATH_HELPER.getIndicesOfMaxToMinSorting(a)
            for o in range(s):
                i[r[o]] += 1
        return i
    
    def calculateCastleDefense(self, e, t, n, i, a):
        s = int(n.getTotalAmount()) # attacking or defending army
        e = int(e * (1 + t / 100)) # t - only used here
        l = min(e, s) # e - only used here
        u = self.getSideUnitCount(l, i)
        c = n.getMeleeCount()
        _ = n.getRangedCount()
        d = [] #[0, 0, 0]
        m = [] #[0, 0, 0]
        p = [] #[0, 0, 0]
        h = [] #[0, 0, 0]
        g = 0
        E = 0
        for f in range(3):
            p[f] = int(u[f] * a[f] / 100)
            h[f] = u[f] - p[f]
            g += p[f]
            E += h[f]
        r = int(g)
        o = int(E)
        if g > c:
            for C in range(3):
                p[C] = 0 if r == 0 else int(c * p[C] / g)
                h[C] = u[C] - p[C]
        elif E > _:
            for T in range(3):
                h[T] = 0 if o == 0 else int(_ * h[T] / E)
                p[T] = u[T] - h[T]
        d = [int(p[S]) for S in range(3)]
        m = [int(h[S]) for S in range(3)]
        y = [p[I] - d[I] for I in range(3)]
        v = [h[A] - m[A] for A in range(3)]
        O = int(y[0] + y[1] + y[2] + .5)
        L = int(v[0] + v[1] + v[2] + .49999)
        b = [d[N] + m[N] == u[N] for N in range(3)]
        R = self.getIndicesOfMaxToMinSorting(y)
        P = 0
        while P < 3 and O > 0:
            D = R[P]
            if not b[D]:
                d[D] += 1
                O -= 1
                b[D] = d[D] + m[D] == u[D]
            P += 1

        R = self.getIndicesOfMaxToMinSorting(v)
        M = 0
        while M < 3 and L > 0:
            D = R[M]
            if not b[D]:
                m[D] += 1
                L -= 1
                b[D] = d[D] + m[D] == u[D]
            M += 1

        B = 2 * n.getUnitTypeCount()
        F = [None] * B
        U = 0
        w = n.getSoldierMeleeDefenseOrder()
        k = 0
        while k < len(w):
            G = w[k]
            x = n.getItemAmount(G)
            V = d[0] + d[1] + d[2]
            W = min(x, V)
            if V > 0 and W > 0:
                K = int(1 * W * d[self.SIDE_LEFT] / V)
                Y = int(1 * W * d[self.SIDE_RIGHT] / V - 1e-4)
                H = W - K - Y
                n.removeItem(G, W)
                F[U] = G
                F[U + 1] = K
                F[U + 2] = G
                F[U + 3] = H
                F[U + 4] = G
                F[U + 5] = Y
                U += 6
                d[self.SIDE_LEFT] -= K
                d[self.SIDE_MIDDLE] -= H
                d[self.SIDE_RIGHT] -= Y
            k += 1

        
    def getIndicesOfMaxToMinSorting(self, e):
        t = [0, 1, 2]
        if e[t[0]] > e[t[1]]:
            if e[t[2]] > e[t[0]]:
                t[0] = 2
                t[1] = 0
                t[2] = 1
            elif e[t[2]] > e[t[1]]:
                t[1] = 2
                t[2] = 1
        elif e[t[1]] > e[t[2]]:
            if e[t[0]] > e[t[2]]:
                t[0] = 1
                t[1] = 0
            else:
                t[0] = 1
                t[1] = 2
                t[2] = 0
        else:
            t[0] = 2
            t[2] = 0
        return t