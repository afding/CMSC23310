import event
import network
import computer
import deliver

def simulate(np, na, tmax, E):
    P, A = [], []
    N = network()
    # To keep labels as ints while separating Proposers and Separators, I use
    # positive ints for Proposers, negative ints for Acceptors.
    for i in range(np):
        P.append(computer(i, "Proposer"))
    for i in range(na):
        P.append(computer(-i, "Acceptor"))
    # Stepping through the ticks
    for i in range(tmax+1):
        if len(N) == 0 and len(E) == 0:
            return
        # Process the event for this tick (if any).
        e = next((x for x in E if x.t == i), None)
        if e is not None:
            E.remove(e)
            for l in e.F:
                c = computer.search(l, P, A)
                c.failed = True
            for l in e.R:
                c = computer.search(l, P, A)
                c.failed = False
            prop_c = computer.search(e.pic, P, A)
            prop_v = e.piv
            if e.pic is not None and e.piv is not None:
                # Message needs a type, src, dst, pid, val, old_pid, old_val).
                m = message("Propose", None, prop_c, None, prop_v, None, None)
                deliver(e.pic, m)
            else:
                m = network.extract(N)
                if m is not None:
                    deliver.deliver(m.dst, m)
