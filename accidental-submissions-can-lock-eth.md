---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19484
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/lido/lido/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/lido/lido/review.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Accidental Submissions Can Lock ETH

### Overview

See description below for full details.

### Original Finding Content

## Lido Contract Issues and Recommendations

## Description
The Lido contract’s current fallback function treats any unrecognized function call as a submission attempt. This may result in users accidentally locking their funds if they mistook the Lido contract for something else, or accessed it through an inaccurate interface.

## Recommendations
Consider adding a `require(msg.data.length == 0);` statement to the fallback function, to protect against accidental submissions by people calling non-existent functions.

## Resolution
This was resolved in PR #238.

---

## LID-12 Suboptimal Scrypt Parameterization for DC4BC Encryption Key

## Asset
`dc4bc/airgapped/encryption.go`

## Status
Resolved: See Resolution

## Rating
**Severity:** Low  
**Impact:** Low  
**Likelihood:** Low

## Description
The current scrypt parameterization appears based on the 2017 recommendations for interactive logons. While this is likely quite resistant to dictionary brute-force attacks, with a derivation time on the order of 100ms, a much higher parameterization is advisable given the use-case and highly valuable data. The use-case is for long-term storage of highly valuable info (Eth2 withdrawal keys). As such, performance considerations associated with interactive logon are not a concern, and a longer key derivation delay is acceptable.

## Recommendations
Consider performing a benchmarking test on representative hardware. Tune the scrypt N parameter such that key derivation takes an acceptable amount of time (e.g., 3 seconds).

## Resolution
This issue was sufficiently remediated in PR #74 and PR #105. 

In PR #74, the difficulty parameter N was increased from 2^15 to 2^16. PR #105 changed the long-term storage medium from USB keys containing the encrypted data to a paper wallet (or similar) containing a BIP39 mnemonic. This mnemonic, used as a random seed, can be used to regenerate the relevant keys. As such, the database containing encrypted secrets is needed only for the duration of the ceremony and is recommended to be held ephemerally in memory (or the storage medium destroyed upon completion of the ceremony).

## References
- Described in [scrypt Key Documentation](https://godoc.org/golang.org/x/crypto/scrypt#Key)
- Useful information: 
  - [Golang Issue #22082](https://github.com/golang/go/issues/22082)
  - [Filippo.io on Scrypt Parameters](https://blog.filippo.io/the-scrypt-parameters)

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Lido |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/lido/lido/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/lido/lido/review.pdf

### Keywords for Search

`vulnerability`

