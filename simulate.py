import network

def simulate(np, na, tmax, E):
    P, A = [], []
    N = network()
    for i in range(np):
        P.append(computer(i, "Proposer", False))
    for i in range(na):
        P.append(computer(i, "Acceptor", False))
    # Stepping through the ticks
    for i in range(tmax+1):
        if len(N) == 0 and len(E) == 0:
            return
        # Process the event for this tick (if any).
        if next(e for e in E with E.t == i), None) is not None:
            E.remove(e)
            for c in e.F:
                c.failed = true
            for c in e.R:
                c.failed = false
            if e.pic is not None and e.piv is not None:
                # Message needs a type, src, dst, pid, val, old_pid, old_val).
                m = message("Propose", None, e.pic, None, e.piv, None, None)
                deliver(e.pic, m)
            else:
                m = network.extract(N)
                if m is not None:
                    deliver(m.dst, m)

    
