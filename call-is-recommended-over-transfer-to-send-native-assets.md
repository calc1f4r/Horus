---
# Core Classification
protocol: Eon Delegated Staking
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50414
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/horizen-labs/eon-delegated-staking
source_link: https://www.halborn.com/audits/horizen-labs/eon-delegated-staking
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
  - Halborn
---

## Vulnerability Title

Call is recommended over transfer to send native assets

### Overview


The report discusses an issue where the `DelegatedStaking` contract uses the `transfer()` function to send tokens to delegators. The use of `transfer()` can cause problems, as it imposes a fixed gas limit which may not be enough for complex operations. The recommended solution is to use the `call()` function instead, which allows for a custom gas limit. Additionally, the team should implement reentrancy protection mechanisms in the `claimReward()` function to avoid any potential risks. The issue has been solved by the Horizen Labs team by implementing the recommended solution.

### Original Finding Content

##### Description

The `DelegatedStaking` contract sends Eon tokens to the delegators by making use of the Solidity `transfer()` function:

```
function claimReward(address payable owner) external {
    (uint256 totalToClaim, ClaimData[] memory claimDetails) = calcReward(owner);
    if(totalToClaim == 0) {
        revert NothingToClaim();
    }
    //transfer reward
    owner.transfer(totalToClaim); // <----------------------
    //update last claimed epoch
    lastClaimedEpochForAddress[owner] = claimDetails[claimDetails.length - 1].epochNumber;
    emit Claim(signPublicKey, forgerVrf1, forgerVrf2, owner, claimDetails);
}
```

In Solidity, the `call()` function is often preferred over `transfer()` for sending Ether In Solidity due to some gas limit considerations:

* `transfer`: Imposes a fixed gas limit of 2300 gas. This limit can be too restrictive, especially if the receiving contract is a multisig wallet that executes more complex logic in its `receive()` function. For example, native `transfer()`calls to Gnosis Safe multisigs will always revert with an out-of-gas error in Binance Smart Chain.
* `call`: Allows specifying a custom gas limit, providing more flexibility and ensuring that the receiving contract can perform necessary operations.

It should be noted that using `call` also requires explicit reentrancy protection mechanisms (e.g., using checks-effects-interactions pattern or the `ReentrancyGuard` contract from OpenZeppelin).

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:M/A:N/D:N/Y:M/R:N/S:U (6.3)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:M/A:N/D:N/Y:M/R:N/S:U)

##### Recommendation

Consider using `call()` over `transfer()` to transfer native assets in order to ensure compatibility with any type of multisig wallet. Moreover, use the check-effects-interactions pattern in the `DelegatedStaking.claimReward()` function to avoid any reentrancy risks.

### Remediation Plan

**SOLVED:** The **Horizen Labs team** solved the issue by implementing the recommended solution.

##### Remediation Hash

<https://github.com/HorizenLabs/eon-delegated-staking/pull/4/commits/0c866b6492bc229827460e8c9dae54f5fb725cea>

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Eon Delegated Staking |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/horizen-labs/eon-delegated-staking
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/horizen-labs/eon-delegated-staking

### Keywords for Search

`vulnerability`

