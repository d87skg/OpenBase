rule GraphConsistency:
    when GraphUpdate
    require no Conflict
    then ACCEPT
