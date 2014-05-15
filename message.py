def trans_label(l):
    if l is None:
        return "   "
    if l > 0:
        return " P%s" % str(l)
    else:
        return " A%s" % str(-l)

def trans_prop(pid, val):
    if pid is None and val is None:
        return ""
    elif pid is None and val is not None:
        return " v=%s" % str(val)
    elif pid is not None and val is None:
        return " n=%s" % str(pid)
    else:
        return " n=%s v=%s" % (str(pid), str(val))

# To be used only in a PROMISE message.
def trans_prior_prop(pid, val):
    if pid is None and val is None:
        return " (Prior: None)"
    else:
        return " (Prior: n=%s, v=%s)" % (str(pid), str(val))

class Message:

    def __init__(self, typ, src, dst, pid, val, old_pid, old_val):
        self.typ = typ
        self.src = src
        self.dst = dst
        self.pid = pid
        self.val = val
        self.old_pid = old_pid
        self.old_val = old_val

    def __repr__(self):
        return "Message(typ=%r,src=%r,dst=%r,pid=%r,val=%r,old_pid=%r,old_val=%r)" % (self.typ,self.src,self.dst,self.pid,self.val,self.old_pid,self.old_val)

    def __str__(self):
        if self.typ == "PROMISE":
            pp = trans_prior_prop(self.old_pid, self.old_val)
        else:
            pp = ""
        return "%s ->%s  %s%s%s" % (trans_label(self.src),
                                    trans_label(self.dst),
                                    self.typ,
                                    trans_prop(self.pid, self.val),
                                    pp)
