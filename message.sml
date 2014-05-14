structure Message = struct

(* Sometimes, we use a prop to hold just an ID. Hence int option. *)
datatype prop = Prop of int * int option

fun pid(Prop(n, v)) = n
fun value(Prop(n, NONE)) = raise Fail "Calling value on prop with no value." 
  | value(Prop(n, SOME v)) = v
				 
datatype message = Propose of Computer.computer * int | (* No src. *)
		   (* Prepare(src, dst, proposal_id) *)
		   Prepare of Computer.computer * Computer.computer * prop |
		   (* Promise(src, dst, proposal_id, prev_proposal) *)
		   Promise of Computer.computer * Computer.computer * prop * prop |
		   (* Accept(src, dst, proposal) *)
		   Accept of Computer.computer * Computer.computer * prop |
		   (* Accepted(src, dst, proposal) *)
		   Accepted of Computer.computer * Computer.computer * prop |
		   (* Rejected(src, dst, proposal_id) *)
		   Rejected of Computer.computer * Computer.computer * prop

fun src(Propose(_)) = raise Fail "No source for propose message." 
  | src(Prepare(c,_,_)) = c
  | src(Promise(c,_,_,_)) = c
  | src(Accept(c,_,_)) = c
  | src(Accepted(c,_,_)) = c
  | src(Rejected(c,_,_)) = c

fun dst(Propose(c,_)) = c
  | dst(Prepare(_,c,_)) = c
  | dst(Promise(_,c,_,_)) = c
  | dst(Accept(_,c,_)) = c
  | dst(Accepted(_,c,_)) = c
  | dst(Rejected(_,c,_)) = c

fun mprop Propose(_,p) = p
  | mprop Prepare(_,_,p) = p
  | mprop Promise(_,_,p,_) = p
  | mprop Accept(_,_,p) = p
  | mprop Accepted(_,_,p) = p
  | mprop Rejected(_,_,p) = p

fun old_prop Promise(_,_,_,p) = p
  | old_prop _ = raise Fail "No prior proposition for non-Promise message."

end (* struct Message *)
