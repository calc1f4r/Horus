---
# Core Classification
protocol: Gacha_2025-01-27
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53306
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Gacha-security-review_2025-01-27.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[L-03] Modulo operator introduces bias during `oddsBPS ratio` selection

### Overview

See description below for full details.

### Original Finding Content

The `GachaTickets::getPayout` function uses `modulo` operation with the `recieved random number` to generate randomness for the lottery draw. But the `pyth documentation` states the following regarding the usage of modulo operation :

> Notice that using the modulo operator can distort the distribution of random numbers if it's not a power of 2. This is negligible for small and medium ranges, but it can be noticeable for large ranges. For example, if you want to generate a random number between 1 and 52, the probability of having a value of 5 is approximately 10^-77 higher than the probability of having a value of 50 which is infinitesimal.

As per the documentation, the probability of having 5 has a drastic difference with the probability of having 50. Hence when the `pool.oddsBPS.pick("pt", entropy)` is called to select an `oddsBPS ratio` randomly, the `oddsBPS ratio` may be skewed towards a particular value due to uneven distribution of selection probabilities. In addition, the `oddsBPS array` range could be large enough to cause the `modulo` operation to be `skewed` towards a particular `oddsBPS ratios`.

Hence this could affect the randomness of the `payout` calculation for the winner.

```solidity
  function pick(
    uint16[] memory self,
    string memory prefix,
    bytes32 entropy
  )
    internal
    pure
    returns (uint16)
  {
    return self[uint256(keccak256(abi.encode(prefix, entropy))) % self.length];
  }
```

Hence when determining the `oddsBPS ratio` randomly, it is recommended to consider using a different method to mitigate the bias caused by `modulo operation`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Gacha_2025-01-27 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Gacha-security-review_2025-01-27.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

