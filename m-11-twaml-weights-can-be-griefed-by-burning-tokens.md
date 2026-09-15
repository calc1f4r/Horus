---
# Core Classification
protocol: Tapioca DAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32334
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-02-tapioca
source_link: https://code4rena.com/reports/2024-02-tapioca
github_link: https://github.com/code-423n4/2024-02-tapioca-findings/issues/132

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

protocol_categories:
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - carrotsmuggler
---

## Vulnerability Title

[M-11] `twAML` weights can be griefed by burning tokens

### Overview


The report discusses a bug in the `TOLP` and `TOB` contracts where users can affect the `twAML` calculations for an infinite amount of time by burning tokens. This is due to the open burn function in the `OTAP` contract, which allows users to directly burn tokens and prevent the `exitPosition` function from being called in the `TOB` contract. The recommended mitigation step is to disable the open burn function and only allow selected contracts to call it. This bug falls under the category of math and has been confirmed by the team. 

### Original Finding Content


Users can lock their liquidity in the `TOLP` contract and mint `OTAP` tokens in the `TOB` contract. The `TOB` contract has a special mechanism called `twAML` to balance out how much rewards they emit over time.

Basically, if a user commits `OTAP` tokens worth more than a minimum amount of shares, they are eligible to sway the votes:

```solidity
bool hasVotingPower =
    lock.ybShares >= computeMinWeight(pool.totalDeposited + VIRTUAL_TOTAL_AMOUNT, MIN_WEIGHT_FACTOR);
```

This allows them to influence the magnitude, divergence as well as the `twAML` value of this asset id.

```solidity
pool.averageMagnitude = (pool.averageMagnitude + magnitude) / pool.totalParticipants; // compute new average magnitude
    // Compute and save new cumulative
    divergenceForce = lock.lockDuration >= pool.cumulative;
    if (divergenceForce) {
        pool.cumulative += pool.averageMagnitude;
    } else {
        if (pool.cumulative > pool.averageMagnitude) {
            pool.cumulative -= pool.averageMagnitude;
        } else {
            pool.cumulative = 0;
        }
    }

    // Save new weight
    pool.totalDeposited += lock.ybShares;

    twAML[lock.sglAssetID] = pool
```

These values determine how large of a discount the users can get when exercising their options.

Similarly, when users decide to exit their position, or if their lock has expired, either they themselves or other users can kick them out of the `TOB` system and reset the `twAML` values to the values it was before.

```solidity
if (!isSGLInRescueMode && participation.hasVotingPower) {
    TWAMLPool memory pool = twAML[lock.sglAssetID];

    if (participation.divergenceForce) {
    //...
```

So the `twAML` change a single user can cause is limited to their lock duration. However, users also have another option: they can directly burn their `OTAP` token after participating. This is because the `OTAP` contract has an open burn function.

```solidity
function burn(uint256 _tokenId) external {
    if (!_isApprovedOrOwner(msg.sender, _tokenId)) revert NotAuthorized();
    _burn(_tokenId);

    emit Burn(msg.sender, _tokenId, options[_tokenId]);
}
```

Now, these user's contributions to the `twAML` calculations cannot be wiped out after their lock expires. This is because the `exitPosition` function calls `otap.burn` which will fail since the user has already burnt their tokens.

So users can affect the `twAML` calculations for an infinite amount of time by burning tokens. This scenario is specifically prevented in the TOLP contract which has a max lock duration enforced with `MAX_LOCK_DURATION`.

Since users can permanently affect the `twAML` calculations, this is a medium severity issue.

### Proof of Concept

Users can directly burn tokens due to `OTAP`'s open burn function as evident from the linked code. This prevents `exitPosition` being called in the `TOB` contract and thus, never resets the `twAML` values.

### Recommended Mitigation Steps

Disable the open burn function in the `OTAP` contract. Only allows selected contracts such as the `TOB` contract to call it.

### Assessed type

Math

**[0xRektora (Tapioca) confirmed](https://github.com/code-423n4/2024-02-tapioca-findings/issues/132#issuecomment-2016854358)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Tapioca DAO |
| Report Date | N/A |
| Finders | carrotsmuggler |

### Source Links

- **Source**: https://code4rena.com/reports/2024-02-tapioca
- **GitHub**: https://github.com/code-423n4/2024-02-tapioca-findings/issues/132
- **Contest**: https://code4rena.com/reports/2024-02-tapioca

### Keywords for Search

`vulnerability`

