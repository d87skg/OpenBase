rule EvidenceFirst:
    when TrustUpdate
    if exists Evidence BEFORE timestamp
    require TrustStable(5)
    then ACCEPT

rule EvidenceMustBeVerified:
    when TrustUpdate
    if exists VerifiedEvidence
    require no Conflict
    then ACCEPT
