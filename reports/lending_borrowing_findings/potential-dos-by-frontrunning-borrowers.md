---
# Core Classification
protocol: Nemeos
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59594
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/nemeos/d98ae938-43ff-44f4-85c8-5852466df646/index.html
source_link: https://certificate.quantstamp.com/full/nemeos/d98ae938-43ff-44f4-85c8-5852466df646/index.html
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
finders_count: 3
finders:
  - Sebastian Banescu
  - Faycal Lalidji
  - Guillermo Escobero
---

## Vulnerability Title

Potential DoS by Frontrunning Borrowers

### Overview


The report discusses a bug found in the `NFTFilter.sol` file, specifically in the `NFTFilter.verifyLoanValidity()` function. The function is responsible for verifying the signature passed by the borrower and returning false if it was not signed by the Nemeos off-chain oracle. However, the function does not have any access control, meaning anyone can call it. This could allow an attacker to listen for `Pool.buyNFT()` transactions, get the signature from the oracle, and call `verifyLoanValidity()`, increasing the nonce of the user. This could cause issues when the legit transaction is executed. The recommendation is to add access control to the function and revert if the signer is not the oracle. The bug has been fixed in two recent updates.

### Original Finding Content

**Update**
Fixed in `cf9ac5d632c0c35c9e8337e501392d2a30d1d098` and `8387199641c1127080b17914b407731a1c4e3533`.

`NFT.verifyLoanValidity()` can only be called by authorized pools.

**File(s) affected:**`NFTFilter.sol`

**Description:**`NFTFilter.verifyLoanValidity()` verifies the signature passed by the borrower and returns false if it was not signed by the Nemeos off-chain oracle. While verifying the signature, it increases an internal mapping that keeps track of all users' nonces.

This is an external function without any access control. Although a valid signature is needed, it does not revert if the signer is not the oracle. Even if it reverted, an attacker could listen for `Pool.buyNFT()` transactions, get the signature from the oracle, and just call `verifyLoanValidity()`. This will increase the nonce of the user, and when the legit transaction executes it will revert.

**Recommendation:** Consider adding access control to the `NFTFilter.verifyLoanValidity()` function, and reverting if the signer is not the oracle.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Nemeos |
| Report Date | N/A |
| Finders | Sebastian Banescu, Faycal Lalidji, Guillermo Escobero |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/nemeos/d98ae938-43ff-44f4-85c8-5852466df646/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/nemeos/d98ae938-43ff-44f4-85c8-5852466df646/index.html

### Keywords for Search

`vulnerability`

