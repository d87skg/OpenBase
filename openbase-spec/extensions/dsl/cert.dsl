rule CertificateIssuance:
    when CertificateIssue
    require TrustStable(5)
    and no Conflict
    then ACCEPT
