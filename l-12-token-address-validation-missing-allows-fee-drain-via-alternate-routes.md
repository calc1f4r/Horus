---
# Core Classification
protocol: AgoraStableSwap_2025-06-05
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63862
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/AgoraStableSwap-security-review_2025-06-05.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[L-12] Token address validation missing allows fee drain via alternate routes

### Overview

See description below for full details.

### Original Finding Content


The `removeTokens` function never validates that the supplied `_tokenAddress` matches exactly `token0` or `token1`. In setups where a token can be interacted with through two addresses (for example, a proxy and a secondary entry-point contract), one of those addresses will not match the stored `token0`/`token1` values—even though they control the same underlying balances.

```solidity
File: AgoraStableSwapPairConfiguration.sol
141:     function removeTokens(address _tokenAddress, uint256 _amount) external {
...
152:@>       if (_tokenAddress == _swapStorage.token0 && _amount > _token0Balance - _swapStorage.token0FeesAccumulated) {
153:             revert InsufficientTokens();
154:         }
155:@>       if (_tokenAddress == _swapStorage.token1 && _amount > _token1Balance - _swapStorage.token1FeesAccumulated) {
156:             revert InsufficientTokens();
157:         }
...
159:         // Interactions: transfer tokens from the pair to the token receiver
160:@>       IERC20(_tokenAddress).safeTransfer({ to: _configStorage.tokenReceiverAddress, value: _amount });
```

Consequently, calls using the “alias” address bypass both fee-deduction checks and allow draining the full balance (including fees accumulated).

Recommendations:
Enforce strict token‐address equality:

```solidity
if (_tokenAddress != _swapStorage.token0 && 
    _tokenAddress != _swapStorage.token1) {
    revert InvalidTokenAddress();
}
```





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | AgoraStableSwap_2025-06-05 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/AgoraStableSwap-security-review_2025-06-05.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

