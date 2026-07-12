rule TrustStability:
    when GraphUpdate
    require TrustStable(3)
    then ACCEPT

rule TrustConsistency:
    when CertificateIssue
    require TrustStable(10)
    then ACCEPT
