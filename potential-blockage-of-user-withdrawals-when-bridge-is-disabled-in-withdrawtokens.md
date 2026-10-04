---
# Core Classification
protocol: ArkProject: NFT Bridge
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 38509
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/clz2gpi0o000ps6nj8stws2bd
source_link: none
github_link: https://github.com/Cyfrin/2024-07-ark-project

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
finders_count: 6
finders:
  - yVuchev
  - bladesec
  - n3smaro
  - Drynooo
  - agent3bood
---

## Vulnerability Title

Potential Blockage of User Withdrawals When Bridge is Disabled in `withdrawTokens`

### Overview


The `withdrawTokens` function in the `Starklane` bridge contract may prevent users from withdrawing their tokens if the bridge is disabled. This can happen even if the users have already received their tokens from Layer 2. This could result in users being unable to access their assets, causing frustration and distrust. To fix this issue, the logic should be adjusted to allow withdrawals even when the bridge is disabled.

### Original Finding Content

## Summary
In the `withdrawTokens` function of the `Starklane` bridge contract, the contract checks if the bridge is enabled before allowing users to withdraw their tokens. If the bridge is disabled, the function reverts with a `BridgeNotEnabledError`. This behavior can inadvertently prevent users from withdrawing their tokens, leaving them unable to reclaim their assets from Layer 2 (L2) even when they should be able to do so.
## Vulnerability Details
The `withdrawTokens` function contains the following check:
```Solidity
if (!_enabled) {
    revert BridgeNotEnabledError();
}
```
This conditional logic ensures that the function will revert if the bridge is disabled. While it makes sense to prevent new deposits or other operations when the bridge is disabled, this logic also prevents users from withdrawing tokens that they have already received from Layer 2 (L2). This creates a scenario where users could be unfairly blocked from accessing their assets, especially during times when the bridge is disabled for maintenance, upgrades, or other reasons unrelated to withdrawals.


## Impact
- User Funds Locked: If the bridge is disabled, users may be blocked from withdrawing their tokens, potentially locking their assets on the contract without any means to reclaim them. This could lead to frustration and distrust among users.
- Operational Risk: If the bridge is disabled for an extended period, users' funds may remain inaccessible, posing a risk to the integrity of the system. Users may be unable to move their tokens between L1 and L2, disrupting the utility of the bridge.

## Tools Used
Manual Code Review
## Recommendations
To avoid blocking users from withdrawing their tokens when the bridge is disabled, the logic should be adjusted to ensure that withdrawals can still be processed regardless of the bridge's enabled/disabled state. This can be achieved by isolating the `_enabled` check to operations like deposits or other non-withdrawal functions.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | ArkProject: NFT Bridge |
| Report Date | N/A |
| Finders | yVuchev, bladesec, n3smaro, Drynooo, agent3bood, 0xTheBlackPanther |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2024-07-ark-project
- **Contest**: https://codehawks.cyfrin.io/c/clz2gpi0o000ps6nj8stws2bd

### Keywords for Search

`vulnerability`

