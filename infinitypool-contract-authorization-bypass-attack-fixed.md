---
# Core Classification
protocol: Glif Filecoin InfinityPool
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21971
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2023/04/glif-filecoin-infinitypool/
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
finders_count: 2
finders:
  - Chingiz Mardanov
  -  Sergii Kravchenko

---

## Vulnerability Title

InfinityPool Contract Authorization Bypass Attack ✓ Fixed

### Overview


This bug report is about an attack that could be used to bypass the `subjectIsAgentCaller` modifier to borrow funds from the pool, draining any available liquidity. The attacker could create their own credential and set the Agent ID to `0`, which would allow them to call the `borrow` function with any `msg.sender` and an arbitrary `vc.value` as the parameter. This would allow the attacker to steal all the funds from the pool.

The resolution to this bug is to not allow the `vc.subject` to be zero. This would ensure that only an `Agent` can call the `borrow` function and pass the `subjectIsAgentCaller` modifier. The resolution was addressed by a pull request on GitHub.

### Original Finding Content

#### Resolution



[Addressed](https://github.com/glif-confidential/pools/pull/445) by not allowing the `vc.subject` to be zero.


#### Description


An attacker could create their own credential and set the Agent ID to `0`, which would bypass the `subjectIsAgentCaller` modifier. The attacker could use this attack to borrow funds from the pool, draining any available liquidity. For example, only an `Agent` should be able to borrow funds from the pool and call the `borrow` function:


**src/Pool/InfinityPool.sol:L302-L325**



```
function borrow(VerifiableCredential memory vc) external isOpen subjectIsAgentCaller(vc) {
 // 1e18 => 1 FIL, can't borrow less than 1 FIL
 if (vc.value < WAD) revert InvalidParams();
 // can't borrow more than the pool has
 if (totalBorrowableAssets() < vc.value) revert InsufficientLiquidity();
 Account memory account = \_getAccount(vc.subject);
 // fresh account, set start epoch and epochsPaid to beginning of current window
 if (account.principal == 0) {
 uint256 currentEpoch = block.number;
 account.startEpoch = currentEpoch;
 account.epochsPaid = currentEpoch;
 GetRoute.agentPolice(router).addPoolToList(vc.subject, id);
 }

 account.principal += vc.value;
 account.save(router, vc.subject, id);

 totalBorrowed += vc.value;

 emit Borrow(vc.subject, vc.value);

 // interact - here `msg.sender` must be the Agent bc of the `subjectIsAgentCaller` modifier
 asset.transfer(msg.sender, vc.value);
}

```
The following modifier checks that the caller is an `Agent`:


**src/Pool/InfinityPool.sol:L96-L101**



```
modifier subjectIsAgentCaller(VerifiableCredential memory vc) {
 if (
 GetRoute.agentFactory(router).agents(msg.sender) != vc.subject
 ) revert Unauthorized();
 \_;
}

```
But if the caller is not an `Agent`, the `GetRoute.agentFactory(router).agents(msg.sender)` will return `0`. And if the `vc.subject` is also zero, the check will be successful with any `msg.sender`. The attacker can also pass an arbitrary `vc.value` as the parameter and steal all the funds from the pool.


#### Recommendation


Ensure only an `Agent` can call `borrow` and pass the `subjectIsAgentCaller` modifier.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Glif Filecoin InfinityPool |
| Report Date | N/A |
| Finders | Chingiz Mardanov,  Sergii Kravchenko
 |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2023/04/glif-filecoin-infinitypool/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

