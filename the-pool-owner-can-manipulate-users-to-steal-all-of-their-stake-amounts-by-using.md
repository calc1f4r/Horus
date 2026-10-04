---
# Core Classification
protocol: Goat Tech
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40671
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/404911dd-3a50-4b63-90d4-e0b9164a34a5
source_link: https://cdn.cantina.xyz/reports/cantina_competition_goat_mar2024.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0xRajkumar
---

## Vulnerability Title

The pool owner can manipulate users to steal all of their stake amounts by using code edge case 

### Overview


This bug report discusses a potential issue with the poolConfigCode_ function, which is used to validate that users staking in a pool have the same code as when the transaction was created. However, there is an edge case where different configurations can have the same code, which can be exploited by the pool owner. The report recommends using keccak256 to generate the code instead. The issue has been fixed by the developer.

### Original Finding Content

## Pool Configuration Code Vulnerability

## Context
(No context files were provided by the reviewer)

## Description
`poolConfigCode_` is used to validate that users staking in the pool have the same code as when the transaction was created, and the owner has not changed it. This provides protection that `ownerPercent` and `userPercent` have not changed. However, there is an edge case where different configurations can have the same code. Let's see how the code is generated:

```
ownerPercent_ * LPercentage.DEMI + userPercent_
```

Here, the `DEMI` is 10000. We can actually find two different `ownerPercent` and `userPercent` inputs that have the same code:

- **First example:**
  - `ownerPercent = 1`
  - `userPercent = 0`
  - `code = 1 * 10000 + 0`
  - `code = 10000`

- **Second example:**
  - `ownerPercent = 0`
  - `userPercent = 10000`
  - `code = 0 * 10000 + 10000`
  - `code = 10000`

We can also validate the sum because 1 and 0, and the sum of 0 and 10000, is actually valid:

```solidity
function validatePercent(uint percent_) internal pure {
    // 100% == DEMI == 10000
    require(percent_ <= DEMI, "invalid percent");
}
```

We are assuming two things:
1. The pool owner is actually having bad intentions and wants to take advantage of these edge cases.
2. `inDefaultOnlyMode` is false.

Both are possible.

### Exploitation Strategy
Now let's see how the owner can take advantage of it:
1. First, they will need to create a pool by staking some Geth and earning some `p2UDtoken`.
2. As `inDefaultOnlyMode` is false, they will set `ownerPercent = 1` and `userPercent = 0` to attract users.
3. They will run a bot that will constantly monitor transactions and will frontrun with `configPool` where `ownerPercent = 0` and `userPercent = 10000`.
4. As the code will be the same, user funds will be transferred to `pool.ethDistributor`, and since `p2UDtoken` will have all the supply, they will earn all the Geth. Users will not earn any `p2UDtoken` tokens.

## Recommendation
To generate code, we should use `keccak256`. Check this reference.

## Goat
Fixed

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Goat Tech |
| Report Date | N/A |
| Finders | 0xRajkumar |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_goat_mar2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/404911dd-3a50-4b63-90d4-e0b9164a34a5

### Keywords for Search

`vulnerability`

