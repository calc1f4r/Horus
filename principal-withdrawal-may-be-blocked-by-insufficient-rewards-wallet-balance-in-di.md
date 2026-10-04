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
solodit_id: 57929
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/DIA/Lumina%20Staking/README.md#5-principal-withdrawal-may-be-blocked-by-insufficient-rewards-wallet-balance-in-diawhitelistedstaking
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 3

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Principal withdrawal may be blocked by insufficient rewards wallet balance in `DIAWhitelistedStaking`

### Overview


This bug report discusses an issue with the `unstake()` and `unstakePrincipal()` functions in the `DIAWhitelistedStaking` contract. These functions require reward payments from an external wallet, but if the wallet does not have enough tokens or has revoked allowances, the entire withdrawal transaction fails. This prevents users from accessing their staked principal, even though it is held within the contract. The recommendation is to separate principal and reward withdrawal logic or implement a try-catch mechanism for reward transfers. The client has added a separate function for unstaking only the principal amount, but it is suggested that this function can be removed as it is similar to an existing function. 

### Original Finding Content

##### Description
The `unstake()` and `unstakePrincipal()` functions in `DIAWhitelistedStaking` require mandatory reward payments from the external `rewardsWallet` before allowing principal withdrawal. When `rewardsWallet` has insufficient token balance or revoked allowances, the `safeTransferFrom()` calls for reward distribution revert, causing the entire withdrawal transaction to fail. This prevents users from accessing their staked principal even though the principal tokens are held within the contract itself. Users can accumulate large rewards over time that exceed the external wallet's capacity, permanently locking access to their own principal funds with no alternative withdrawal path.
<br/>
##### Recommendation
We recommend separating principal and reward withdrawal logic, allowing users to withdraw their principal independently of reward payment status, or implement a try-catch mechanism for reward transfers.

> **Client's Commentary:**
> Client: added separate function for unstakeOnlyPrincipalAmount 
> MixBytes: There are added `requestUnstake` and `requestUnstakeWithoutClaim` functions, which differ from each other only by the `if (currentStore.paidOutReward != totalRewards)` check, which can be omitted as it doesn't update any state variables or affects any logic. `requestUnstake` function can be removed.

---

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 3/5 |
| Audit Firm | MixBytes |
| Protocol | DIA |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/DIA/Lumina%20Staking/README.md#5-principal-withdrawal-may-be-blocked-by-insufficient-rewards-wallet-balance-in-diawhitelistedstaking
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

