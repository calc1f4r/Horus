---
# Core Classification
protocol: Yearn Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28524
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Yearn%20Finance/yveCRV/README.md#1-correct-migration
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
  - MixBytes
---

## Vulnerability Title

Correct migration

### Overview


A bug was identified in the constructor of the yveCRV-vault project on GitHub. The bug is that when migrating the strategy, rights are granted to spend tokens which should be canceled. To fix this bug, it is recommended to add certain lines of code to the prepareMigration() function. This code will cancel the rights to spend tokens when the strategy is migrated. The code includes commands to approve and transfer tokens, and to approve the vault and rewards.

### Original Finding Content

##### Description
In constructor, rights are granted to spend tokens, which should be canceled when migrating the strategy.
- https://github.com/andy8052/yveCRV-vault/blob/6706b9ad45e71ee9014454419f229adfa6409f1d/contracts/Strategy.sol#L171

##### Recommendation
It is recommended to add in function `prepareMigration()`:
```solidity
    IERC20(crv).safeApprove(address(want), 0);
    IERC20(usdc).safeApprove(sushiswap, 0);
    
    IyveCRV(address(want)).claim();
    want.safeTransfer(_newStrategy, want.balanceOf(address(this)));
    
    IERC20(usdc).safeTransfer(_newStrategy, IERC20(usdc).balanceOf(address(this)));
    
    want.safeApprove(vault, 0);
    vault.approve(rewards, 0);
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Yearn Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Yearn%20Finance/yveCRV/README.md#1-correct-migration
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

