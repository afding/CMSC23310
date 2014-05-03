signature SIMULATE = sig
    val queue = Network.network * Message.message -> Network.network;
    val extract = Network.network -> Message.message;
    val simulate = raise Fail "TODO: Determine type of simulate"
