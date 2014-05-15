class Message:

    def __init__(self, typ, src, dst, pid, val, old_pid, old_val):
        self.typ = typ
        self.src = src
        self.dst = dst
        self.pid = pid
        self.val = val
        self.old_pid = old_pid
        self.old_val = old_val
