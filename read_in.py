import sys
import getopt

import event

def read(fname):
    with open(fname) as f:
        is_init = 0
        es = []
        for line in f:
            if line == "0 END\n":
                break;
            if line[0] == '#' or line.isspace():
                continue;
            if is_init == False:
                np, na, tmax = map((lambda x: int(x)), line.split())
                is_init = True
                continue;
            t, action, aux1, aux2 = line.split()
            t = int(t)
            if action == "PROPOSE":
                # Recall: Proposers have positive int labels
                # and Acceptors have negative int labels.
                e = event.Event(t, [], [], int(aux1), int(aux2))
            elif action == "FAIL":
                if aux1 == "PROPOSER":
                    e = event.Event(t, [int(aux2)], [], None, None)
                else:
                    e = event.Event(t, [-int(aux2)], [], None, None)
            elif action == "RECOVER":
                if aux1 == "PROPOSER":
                    e = event.Event(t, [], [int(aux2)], None, None)
                else:
                    e = event.Event(t, [], [-int(aux2)], None, None)
            else:
                raise ValueError("my_read_in: Invalid Action")
            es.append(e)
        fs = event.shrink(es)
        return (np, na, tmax, fs)

def main(argv=None):
    if argv is None:
        argv = sys.argv
    fname = argv[1]
    es = read(fname)
    for e in es[3]:
        print repr(e)
    
if __name__ == "__main__":
    main()
