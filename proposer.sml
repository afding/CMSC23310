structure Proposer = struct

(* A proposer has a name, failed, state, list of messages in inbox *)
(* True indicates working. *)
datatype proposer = P of string * bool * Message.message list

fun pid P(s, _, _) = s

fun find ps s = List.find (lambda x => (pid x = s)) ps

(* Given a list of proposers and some id, sees if that one is failed. *)
fun isFail(ps : proposer list, pid : string) : bool =
    find ps s
