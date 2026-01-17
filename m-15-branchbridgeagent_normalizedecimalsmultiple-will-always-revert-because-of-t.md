---
# Core Classification
protocol: Maia DAO Ecosystem
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26084
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-05-maia
source_link: https://code4rena.com/reports/2023-05-maia
github_link: https://github.com/code-423n4/2023-05-maia-findings/issues/598

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
  - dexes
  - cross_chain
  - liquidity_manager
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - jasonxiale
---

## Vulnerability Title

[M-15] `BranchBridgeAgent._normalizeDecimalsMultiple` will always revert because of the lack of allocating memory

### Overview


This bug report is about a function `_normalizeDecimalsMultiple` in the code of BranchBridgeAgent. It is found that the function will always revert because `deposits` are never allocated memory. The tools used to find this bug were Visual Studio (VS). The recommended mitigation steps are to add two lines of code to the function that allocate memory for `deposits` and set it to the length of the `_deposits` array. The assessed type of the bug is an Error. The severity of the bug has been decreased to Medium by Trust (judge) and the findings were confirmed by 0xBugsy (Maia). 0xBugsy (Maia) also commented that the findings will not be rectified due to the upcoming migration of this section to Balancer Stable Pools.

### Original Finding Content


### Proof of Concept

[BranchBridgeAgent.\_normalizeDecimalsMultiple](https://github.com/code-423n4/2023-05-maia/blob/54a45beb1428d85999da3f721f923cbf36ee3d35/src/ulysses-omnichain/BranchBridgeAgent.sol#L1349-L1357)'s code is below. Because `deposits` are never allocated memory, the function will always revert.

```solidity
    function _normalizeDecimalsMultiple(uint256[] memory _deposits, address[] memory _tokens)
        internal
        view
        returns (uint256[] memory deposits)
    {
        for (uint256 i = 0; i < _deposits.length; i++) {
            deposits[i] = _normalizeDecimals(_deposits[i], ERC20(_tokens[i]).decimals());
        }
    }
```

### Tools Used

VS

### Recommended Mitigation Steps

```solidity
@@ -1351,7 +1351,9 @@
         view
         returns (uint256[] memory deposits)
     {
-        for (uint256 i = 0; i < _deposits.length; i++) {
+        uint len = _deposits.length;
+        deposits = new uint256[](len);
+        for (uint256 i = 0; i < len; i++) {
             deposits[i] = _normalizeDecimals(_deposits[i], ERC20(_tokens[i]).decimals());
         }
     }

```

### Assessed type

Error

**[Trust (judge) decreased severity to Medium](https://github.com/code-423n4/2023-05-maia-findings/issues/598#issuecomment-1630399431)**

**[0xBugsy (Maia) confirmed](https://github.com/code-423n4/2023-05-maia-findings/issues/598#issuecomment-1632760641)**

**[0xBugsy (Maia) commented](https://github.com/code-423n4/2023-05-maia-findings/issues/598#issuecomment-1655677280):**
 > We recognize the audit's findings on Decimal Conversion for Ulysses AMM. These will not be rectified due to the upcoming migration of this section to Balancer Stable Pools.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Maia DAO Ecosystem |
| Report Date | N/A |
| Finders | jasonxiale |

### Source Links

- **Source**: https://code4rena.com/reports/2023-05-maia
- **GitHub**: https://github.com/code-423n4/2023-05-maia-findings/issues/598
- **Contest**: https://code4rena.com/reports/2023-05-maia

### Keywords for Search

`vulnerability`

