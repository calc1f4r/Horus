---
# Core Classification
protocol: Parity
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17185
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/parity.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/parity.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 7
finders:
  - Andy Ying
  - 2018: June 15
  - Jay Little
  - Josselin Feist
  - 2018: Initial report delivered Added Appendix D with retest results Added additional retest results https://docs.google.com/document/d/1M6lrQWHQLqzLnlwlPNcpAq_ulWTpmpﬁ9D_sbnH2S-c/edit# 1/80
---

## Vulnerability Title

"single message" crypto operations lack authentication due to using AES-CTR

### Overview


This bug report is about data validation in the ethstore/src/dir/disk.rs file. It is rated as high difficulty. The encrypt_single_message and decrypt_single_message functions use AES-CTR, which is malleable and could allow attackers to modify encrypted messages without access to the keys. This could be exploited by a malicious user using Wireshark to capture network traffic meant for SecretStore, extract the message, modify certain fields and send the crafted message to gain access to unauthorized functionality. 

The recommendation is to use AES-GCM, an authenticated encryption mode, instead of AES-CTR. This will provide a guarantee of integrity, rather than just confidentiality. It is also suggested to refer to Thomas Ptacek’s Cryptographic Right Answers whenever needed for new code. The references provided are Counter Mode Security: Analysis and Recommendations (Section 2.1) and Evaluation of Some Blockcipher Modes of Operation.

### Original Finding Content

## Data Validation

**Type:** Data Validation  
**Target:** ethstore/src/dir/disk.rs  

**Difficulty:** High  

## Description
In the ECIES module, `encrypt_single_message` and `decrypt_single_message` use AES-CTR. CTR mode is malleable, so under some circumstances, attackers could modify encrypted messages without access to the keys. This could allow attackers to effectively impersonate some party communicating using these facilities.

`decrypt_single_message` is used by the SecretStore server. We did not further investigate the SecretStore server because it is not in-scope for the review. However, a cursory review identified that `decrypt_single_message` decrypts ciphertext received over the network.

## Exploit Scenario
Alice, a malicious user, uses Wireshark to capture network traffic meant for SecretStore. She extracts a message and strategically tampers with it to alter certain critical fields. Alice sends the crafted message to the SecretStore to gain access to unauthorized functionality.

## Recommendation
Use AES-GCM, an authenticated encryption mode. Using an AEAD construction like AES-GCM will provide a guarantee of integrity, rather than just confidentiality. Refer to Thomas Ptacek’s Cryptographic Right Answers whenever needed for new code.

## References
- Counter Mode Security: Analysis and Recommendations (see Section 2.1)  
- Evaluation of Some Blockcipher Modes of Operation  
  [Evaluation Document](https://docs.google.com/document/d/1M6lrQWHQLqzLnlwlPNcpAq_ulWTpmpf9D_sbnH2S-c/edit#)

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Parity |
| Report Date | N/A |
| Finders | Andy Ying, 2018: June 15, Jay Little, Josselin Feist, 2018: Initial report delivered Added Appendix D with retest results Added additional retest results https://docs.google.com/document/d/1M6lrQWHQLqzLnlwlPNcpAq_ulWTpmpﬁ9D_sbnH2S-c/edit# 1/80, 2018: July 6, Changelog February 23 |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/parity.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/parity.pdf

### Keywords for Search

`vulnerability`

