---
# Core Classification
protocol: DIA
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57917
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/DIA/Lumina%20Staking/README.md#5-wdia-prohibits-zero-transfers-which-will-block-rewards-distribution-to-beneficiary-address-if-100-goes-to-principal-unstaker
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

`WDIA` prohibits zero transfers, which will block rewards distribution to beneficiary address if 100% goes to principal unstaker

### Overview


The `DIAExternalStaking` contract has a bug that prevents users from claiming rewards when they have allocated 100% of their rewards to the principal unstaker. This is because the `WDIA` token contract has a check that reverts on zero-amount transfers, causing the entire claim transaction to fail. To fix this, a check should be added to skip the transfer to the beneficiary when the requested unstake reward amount is zero. Additionally, the same check should be performed before transferring the requested unstake principal amount to the principal payout wallet. Consider allowing zero-amount transfers in the `WDIA` token contract, but this may have implications for other parts of the system and should be carefully considered.

### Original Finding Content

##### Description
In the `DIAExternalStaking` contract, the `unstake` function distributes rewards between the principal wallet and beneficiary based on the `principalWalletShareBps` parameter. When `principalWalletShareBps` is set to 10000 (100%), all rewards go to the principal unstaker and `requestedUnstakeRewardAmount` (which goes to the beneficiary) becomes zero.

The issue arises because the `WDIA` token contract implements a check that reverts on zero-amount transfers (`if (wad == 0) revert ZeroTransferAmount();`). When `requestedUnstakeRewardAmount` is zero, the `safeTransferFrom` call to the beneficiary address will revert, causing the entire `claim` transaction to fail.

This prevents users from claiming any rewards when 100% of rewards are allocated to the principal unstaker, effectively locking the rewards and making the staking system unusable for stakes with maximum principal wallet share.
<br/>
##### Recommendation
We recommend adding a check to skip the transfer to beneficiary when the `requestedUnstakeRewardAmount` is zero. The same check should be performed before transferring `requestedUnstakePrincipalAmount` to the `principalPayoutWallet` address to prevent the same issue in case if the transferred amount is zero. Also, consider allowing zero-amount transfers in the `WDIA` token contract by removing the `ZeroTransferAmount` restriction, though this would require careful consideration of the implications for other parts of the system.

> **Client's Commentary:**
> 0 transfer is allowed in WDIA, added amount transfer check to skip transfer if amount is 0

---

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | DIA |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/DIA/Lumina%20Staking/README.md#5-wdia-prohibits-zero-transfers-which-will-block-rewards-distribution-to-beneficiary-address-if-100-goes-to-principal-unstaker
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

