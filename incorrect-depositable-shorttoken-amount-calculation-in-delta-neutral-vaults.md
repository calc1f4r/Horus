---
# Core Classification
protocol: SteadeFi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27642
audit_firm: Codehawks
contest_link: https://www.codehawks.com/contests/clo38mm260001la08daw5cbuf
source_link: none
github_link: https://github.com/Cyfrin/2023-10-SteadeFi

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
  - hash
  - pontifex
---

## Vulnerability Title

Incorrect depositable shortToken amount calculation in Delta neutral vaults

### Overview


This bug report is about an incorrect depositable shortToken amount calculation in Delta neutral vaults. The severity of this bug is medium risk. The relevant GitHub link is provided in the report. 

The bug occurs when calculating the maximum possible depositable amount for delta neutral vaults, `_maxTokenBLending` is calculated incorrectly. If a user wants to deposit `v` value to a `l` leveraged delta neutral vault with token weights `a` and `b`, the calculation of required lending amount would be as follows:

Total value to deposit to GMX = lv
Value of tokens to short = lva
Hence this value will be borrowed from the tokenA lending vault
Remaining value to borrow (from tokenB lending vault) = lv - lva - v (deposit value provided by user)
Hence if there is Tb value of tokens in tokenB lending vault, v <= Tb / (l - la - 1)

The impact of this bug is that deposit attempts can revert even when there is enough tokens to lend causing inefficiency, loss of gas for depositors and deviation from the protocol specification. The recommendation to fix the bug is to change the formula to the correct one as provided in the report.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-10-SteadeFi/blob/0f909e2f0917cb9ad02986f631d622376510abec/contracts/strategy/gmx/GMXReader.sol#L264-L270">https://github.com/Cyfrin/2023-10-SteadeFi/blob/0f909e2f0917cb9ad02986f631d622376510abec/contracts/strategy/gmx/GMXReader.sol#L264-L270</a>


## Vulnerability Details
When calculating the maximum possible depositable amount for delta neutral vaults, `_maxTokenBLending` is calculated incorrectly.
```solidity
    if (self.delta == GMXTypes.Delta.Neutral) {
      (uint256 _tokenAWeight, ) = tokenWeights(self);


      uint256 _maxTokenALending = convertToUsdValue(
        self,
        address(self.tokenA),
        self.tokenALendingVault.totalAvailableAsset()
      ) * SAFE_MULTIPLIER
        / (self.leverage * _tokenAWeight / SAFE_MULTIPLIER);


      uint256 _maxTokenBLending = convertToUsdValue(
        self,
        address(self.tokenB),
        self.tokenBLendingVault.totalAvailableAsset()
      ) * SAFE_MULTIPLIER
        / (self.leverage * _tokenAWeight / SAFE_MULTIPLIER)
        - 1e18;
```
https://github.com/Cyfrin/2023-10-SteadeFi/blob/0f909e2f0917cb9ad02986f631d622376510abec/contracts/strategy/gmx/GMXReader.sol#L254-L270

If a user wants to deposit `v` value to a `l` leveraged delta neutral vault with token weights `a` and `b`, the calculation of required lending amount would be as follows:
```
Total value to deposit to GMX = lv
Value of tokens to short = lva
Hence this value will be borrowed from the tokenA lending vault
Remaining value to borrow (from tokenB lending vault) = lv - lva - v (deposit value provided by user)
Hence if there is Tb value of tokens in tokenB lending vault, v <= Tb / (l - la - 1)
``` 

## Impact
Deposit attempts can revert even when there is enough tokens to lend causing inefficiency, loss of gas for depositors and deviation from the protocol specification.

## Recommendations
Change the formula to the correct one.
```diff
diff --git a/contracts/strategy/gmx/GMXReader.sol b/contracts/strategy/gmx/GMXReader.sol
index 73bb111..ae819c4 100644
--- a/contracts/strategy/gmx/GMXReader.sol
+++ b/contracts/strategy/gmx/GMXReader.sol
@@ -266,8 +266,7 @@ library GMXReader {
         address(self.tokenB),
         self.tokenBLendingVault.totalAvailableAsset()
       ) * SAFE_MULTIPLIER
-        / (self.leverage * _tokenAWeight / SAFE_MULTIPLIER)
-        - 1e18;
+        / (self.leverage - (self.leverage *_tokenAWeight / SAFE_MULTIPLIER) - 1e18);
 
       _additionalCapacity = _maxTokenALending > _maxTokenBLending ? _maxTokenBLending : _maxTokenALending;
     }

```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | SteadeFi |
| Report Date | N/A |
| Finders | hash, pontifex |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-10-SteadeFi
- **Contest**: https://www.codehawks.com/contests/clo38mm260001la08daw5cbuf

### Keywords for Search

`vulnerability`

