---
# Core Classification
protocol: Camp - Re-Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62788
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/camp-re-audit/2a90a14d-4635-462c-905c-0b444e0d8cf8/index.html
source_link: https://certificate.quantstamp.com/full/camp-re-audit/2a90a14d-4635-462c-905c-0b444e0d8cf8/index.html
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
finders_count: 2
finders:
  - Paul Clemson
  - Darren Jensen
---

## Vulnerability Title

Griefing Users Can Cause Deposits to Fail on the Destination Chain Due to Lack of Minimum `_gaslimit` Validation

### Overview


A bug has been reported in the `CampTimelockEscrow.sol` file, where the `bridgeOut()` and `release()` functions do not have a minimum gas validation. This means that a user could specify a very small gas limit, causing the transaction to fail on the destination chain. The recommendation is to add a minimum gas validation to ensure successful bridge transactions.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `ca194fd861d7406c934a01ed91b06205da2f067d`.

Additional fix in: `8e41143cf6839753b027569e24f70a88dffd2388`.

**File(s) affected:**`contracts/CampTimelockEscrow.sol`

**Description:** The `bridgeOut()` and `release()` functions allow the caller to specify a `_gaslimit` argument. This value is the maximum amount of gas units the executor should use on the destination chain when completing the bridge. However, in the case of the `CampTimelockEscrow` contract, there is never any validation that some minimum amount of gas is available on the destination chain to ensure the bridge transaction is successful. Therefore, User A could process User B's deposit via the `release()` function, specifying a very small `_gaslimit`, causing the transaction to fail on the destination chain. This means the affected user would have directly to call the `lzReceive()` function on the target chain's implementation of the Camp OFT contract in order to complete their bridge action successfully.

**Recommendation:** As the `CampTimelockEscrow` contract never attaches any data within its `SendParam` struct, it should be possible to estimate a minimum amount of gas required on the target chain to complete a basic bridge action (`MIN_GAS_LIMIT`) and validate that `_gaslimit >= MIN_GAS_LIMIT`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Camp - Re-Audit |
| Report Date | N/A |
| Finders | Paul Clemson, Darren Jensen |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/camp-re-audit/2a90a14d-4635-462c-905c-0b444e0d8cf8/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/camp-re-audit/2a90a14d-4635-462c-905c-0b444e0d8cf8/index.html

### Keywords for Search

`vulnerability`

