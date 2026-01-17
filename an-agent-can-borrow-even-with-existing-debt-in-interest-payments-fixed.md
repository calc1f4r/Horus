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
solodit_id: 21976
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2023/04/glif-filecoin-infinitypool/
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
finders_count: 2
finders:
  - Chingiz Mardanov
  -  Sergii Kravchenko

---

## Vulnerability Title

An Agent Can Borrow Even With Existing Debt in Interest Payments ✓ Fixed

### Overview


This bug report is about an issue with the ‘borrow’ function of the pool in the InfinityPool.sol file. The issue is that when an Agent calls the borrow function, the current debt status is not checked, and the principal debt increases after borrowing, but the account.epochsPaid remains the same. This causes the pending debt to instantly increase as if the borrowing happened on account.epochsPaid. 

The recommendation is to ensure the debt is paid when borrowing more funds. This was mitigated by adding a limit to the remaining interest debt when borrowing, so an Agent should have an interest debt that is no larger than 1 day.

### Original Finding Content

#### Resolution



[Mitigated](https://github.com/glif-confidential/pools/pull/482) by adding a limit to the remaining interest debt when borrowing. So an agent should have an interest debt that is no larger than 1 day.


#### Description


To borrow funds, an `Agent` has to call the `borrow` function of the pool:


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
Let’s assume that the `Agent` already had some funds borrowed. During this function execution, the current debt status is not checked. The principal debt increases after borrowing, but `account.epochsPaid` remains the same. So the pending debt will instantly increase as if the borrowing happened on `account.epochsPaid`.


#### Recommendation


Ensure the debt is paid when borrowing more funds.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

