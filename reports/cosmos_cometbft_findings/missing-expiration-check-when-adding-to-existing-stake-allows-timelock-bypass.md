---
# Core Classification
protocol: Sapien - 2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62029
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/sapien-2/9f938662-5bf7-4dc3-8774-3e7a12204cc3/index.html
source_link: https://certificate.quantstamp.com/full/sapien-2/9f938662-5bf7-4dc3-8774-3e7a12204cc3/index.html
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
  - Paul Clemson
  - Julio Aguilar
  - Tim Sigl
---

## Vulnerability Title

Missing Expiration Check when Adding to Existing Stake Allows Timelock Bypass

### Overview


The client has marked a bug as "Fixed" in the `SapienVault.sol` file. The issue was that the `stake()` and `increaseAmount()` functions did not properly validate the lockup period for adding tokens to a stake. This could result in some stakes being immediately unlocked, allowing users to benefit from a higher multiplier while still being able to withdraw their tokens at any time. The recommendation is to check if a user's existing stake has expired before allowing them to add more tokens, or to reset the start time if the stake has expired.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `ffda07756c53963c20a254c11c97f6809d08cfaf`.

**File(s) affected:**`SapienVault.sol`

**Description:** The `stake()` and `increaseAmount()` functions allow users to add tokens to stakes without validation that the initial stake's lockup period has not ended. This can allow for some stakes where the new `weightedStartTime + effectiveLockUpPeriod < block.timestamp` meaning the stake is immediately unlocked. This allows users to benefit from an increased multiplier while being able to unlock their tokens at any time.

**Recommendation:** Consider checking if a user's existing stake has expired before allowing them to add additional tokens via `stake()` or `increaseAmount()` functions. Alternatively, reset the weighted start time to the current timestamp when adding to expired stakes.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Sapien - 2 |
| Report Date | N/A |
| Finders | Paul Clemson, Julio Aguilar, Tim Sigl |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/sapien-2/9f938662-5bf7-4dc3-8774-3e7a12204cc3/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/sapien-2/9f938662-5bf7-4dc3-8774-3e7a12204cc3/index.html

### Keywords for Search

`vulnerability`

