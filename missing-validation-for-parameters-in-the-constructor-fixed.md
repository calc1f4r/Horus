---
# Core Classification
protocol: USDKG
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45446
audit_firm: ConsenSys
contest_link: none
source_link: https://diligence.consensys.io/audits/2025/01/usdkg/
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
finders_count: 0
finders:
---

## Vulnerability Title

Missing Validation for Parameters in the Constructor ✓ Fixed

### Overview


The report states that there is a bug in the `USDKG` contract's constructor function. This bug occurs when the `owner` or `compliance` address parameters are set to zero, which makes the token contract unusable. The bug has been fixed in a commit with code `0d22c5326e21541df0c718db98004d5a475aa2ea` by adding checks to ensure that the addresses are non-zero. The recommendation is to implement this fix in the constructor function.

### Original Finding Content

#### Resolution

Fixed in [commit 0d22c5326e21541df0c718db98004d5a475aa2ea](https://github.com/USDkg/USDkg/commit/0d22c5326e21541df0c718db98004d5a475aa2ea) by introducing 0-checks on the `owner` and `compliance` addresses in the constructor.


#### Description

The constructor function of the `USDKG` contract does not validate that the `owner` and `compliance` address parameters are non-zero. If either address is set to the zero address, the token contract would become unusable.

#### Examples

**contracts/USDKG.sol:L45-L52**

```
constructor (address _owner, address _compliance) {
    owner = _owner;
    compliance = _compliance;
    _totalSupply = 0;
    name = "USDKG";
    symbol = "USDKG";
    decimals = 6;
}

```
#### Recommendation

Add non-zero address validation in the constructor.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | USDKG |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://diligence.consensys.io/audits/2025/01/usdkg/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

