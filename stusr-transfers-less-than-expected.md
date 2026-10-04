---
# Core Classification
protocol: Resolv
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33571
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Resolv/README.md#3-stusr-transfers-less-than-expected
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
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

StUSR Transfers Less Than Expected

### Overview


The bug report discusses an issue with the StUSR token when it is being transferred. Due to a rounding error, the sender may receive fewer shares than expected, resulting in a potential loss of funds. This could be exploited by hackers to attack other protocols that use StUSR as collateral. The report recommends documenting this issue and possibly switching to a different ERC-4626 vault implementation to avoid further problems.

### Original Finding Content

##### Description
* https://github.com/resolv-im/resolv-contracts/blob/a36e73c4be0b5f233de6bfc8d2c276136bf67573/contracts/ERC20RebasingUpgradeable.sol#L135

StUSR, when transferring, converts the underlying amount into shares with a rounding error in favor of the sender (i.e., downwards). This error can be significant if the exchange rate between shares and the underlying asset is inflated. Specifically, for some positive underlying amounts, the number of shares will be zero. In such cases, the `transfer()` function will be executed successfully, but the balances of the recipient and the sender will remain unchanged. A hacker could exploit this issue to attack third-party protocols, for example, if a lending protocol integrates StUSD as collateral.

A similar problem affects `transferFrom()`: the transferred allowance will be fully consumed even if the recipient receives zero shares (and consequently, zero underlying assets).

##### Recommendation
We recommend documenting this nuance, mentioning that during transfers using either `transfer()` or `transferFrom()`, the user may receive fewer funds than specified in the arguments, and the allowance will still be consumed. A more radical solution would be to abandon the rebasing token in favor of a regular ERC-4626 vault from OpenZeppelin's standard implementation.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Resolv |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Resolv/README.md#3-stusr-transfers-less-than-expected
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

