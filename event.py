# F, R, pic should be (list) of labels of computers.
class Event:
    def __init__(self, t, F, R, pic, piv):
        self.t = t
        self.F = F
        self.R = R
        self.pic = pic
        self.piv = piv

    def __repr__(self):
        return "Event(t=%r,F=%r,R=%r,pic=%r,piv=%r)" % (self.t,self.F,self.R,self.pic,self.piv)

    def merge(self, e2):
        self.F = self.F + e2.F
        self.R = self.R + e2.R
        if self.pic is None:
            self.pic = e2.pic
        if self.piv is None:
            self.piv = e2.piv

# Assuming es is arranged in order of time, this should guarantee
# that es has at most one event per time t.
def shrink(es):
    fs = []
    for e in es:
        l = len(fs)-1
        if (not fs) or e.t != fs[l].t:
            # We cannot merge last element of fs with current e.
            # Hence, append current e to f.
            fs.append(e)
        else:
            # We can merge the two!
            fs[l].merge(e)
    return fs
