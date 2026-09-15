---
# Core Classification
protocol: Meta
chain: everychain
category: uncategorized
vulnerability_type: missing-logic

# Attack Vector Details
attack_type: missing-logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19117
audit_firm: Hans
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hans/2023-07-13-Meta.md
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
  - missing-logic

protocol_categories:
  - liquid_staking
  - cdp
  - yield

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Hans
---

## Vulnerability Title

On restaking, funds should be unslashed back

### Overview


A Medium severity bug was reported in the MetaManager.sol smart contract. The bug was related to the reStake function, which calculates the `toMint` value as `getReservedForVesting(caller) + getClaimable(caller)`. This value should be "unslashed" using the `lastSlashRate` to be fair. If a user starts unstaking with a 10 day vesting period and then stops after a day, the originally slashed amount should be reimbursed partially. 

The severity of this bug is classified as MEDIUM since it is not an intended mechanism to ensure fairness. To fix the bug, a new logic should be added to reimburse the slashed amounts partially when the user restakes. The Meta team fixed the bug and Hans verified it.

### Original Finding Content

**Severity:** Medium

**Context:** [`MetaManager.sol#L117-L126`](https://github.com/getmetafinance/meta/blob/00bbac1613fa69e4c180ff53515451df4df9f69e/contracts/meta/MetaManager.sol#L117-L126)

**Description:**
In `MetaManager::reStake`, `toMint` is calculated as `getReservedForVesting(caller) + getClaimable(caller)` and it’s essentially the same to `unstakeRate[_user] * (time2fullRedemption[_user] - lastWithdrawTime[_user])`. The problem is that this should be “unslashed” using the `lastSlashRate` to be fair.

For example, a user starts unstaking 100e18 esMETA with 10 days vesting period and after a day he decided to stop unstaking and restake.

In this case, the originally slashed 50e18 esMETA are not fair for him and the protocol should reimburse partial slash.

**Impact**
While this is not a genuine bug, it is more of a recommendation to enhance the protocol's completeness. However, I have classified its severity level as MEDIUM since it is evidently not an intended mechanism to ensure fairness.

**Recommendation:**
Add a new logic to reimburse the slashed amounts partially when the user restakes.

**Meta Team:**

Fixed.

```diff

function reStake() external updateReward(msg.sender) {
address caller = msg.sender;
uint256 toMint = getReservedForVesting(caller) + getClaimable(caller);
+       toMint = (toMint * 100 * Constants.PINT) / (100 - lastSlashRate[caller]);
+       toMint /= Constants.PINT;
if (toMint > 0) {
esMeta.mint(caller, toMint);
unstakeRate[caller] = 0;
time2fullRedemption[caller] = 0;
lastSlashRate[caller] = 0;
}
}
```

**Hans:**
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hans |
| Protocol | Meta |
| Report Date | N/A |
| Finders | Hans |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hans/2023-07-13-Meta.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`Missing-Logic`

