---
# Core Classification
protocol: Meta
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19113
audit_firm: Hans
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hans/2023-07-13-Meta.md
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

Non-accessible function of GMX is used

### Overview


In this bug report, it was identified that the `Helper::harvest` function calls a GMX router’s `compoundForAccount` function, which is only callable by governer. This means that it is impossible to claim rewards from the GMX protocol. The recommendation was to reimplement the harvest mechanism using the correct function of GMX. The Meta Team fixed the issue by moving the code to mUSDManager.sol and adding an interface IGLPRewardsRouter, allowing the function to be called by the address holding the GLP tokens. This was verified by Hans.

### Original Finding Content

**Severity:** High

**Context:** [`Helper.sol#L84-89`](https://github.com/getmetafinance/meta/blob/00bbac1613fa69e4c180ff53515451df4df9f69e/contracts/musd/Helper.sol#L84-89)

**Description:**
`Helper::harvest` calls a GMX router’s `compoundForAccount` function but according to GMX code it’s only callable by governer.

```solidity
function harvest(address _account) external returns (uint256) {
router.compoundForAccount(_account);
gmxRewards.claimForAccount(_account, _account);
glpRewards.claimForAccount(_account, _account);
return native.balanceOf(_account);
}
```

The relevant part on [GMX Router](https://github.com/gmx-io/gmx-contracts/blob/e772060cc46d94fc2679445343f40c65290dede3/contracts/staking/RewardRouterV2.sol#L217 "smartCard-inline") is implemented as below.

```solidity
function compoundForAccount(address _account) external nonReentrant onlyGov {
_compound(_account);
}
```

**Impact**
It is impossible to claim the rewards from the GMX protocol.

**Recommendation:**
Reimplement the harvest mechanism using the correct function of GMX.

**Meta Team:**

Fixed in the latest commit. Harvest function can only be called by the address holding the GLP tokesn. Hence the code has been moved to mUSDManager.sol.

```diff

(commit: 007c1b9183cdb65a500928173608ebff0a5197ef)

+    interface IGLPRewardsRouter {
+        function claimFees() external;
+    }

+    IGLPRewardsRouter public router;


+    function harvest() public {
+        router.claimFees();
+    }

```

**Hans:**
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

`vulnerability`

