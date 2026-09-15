---
# Core Classification
protocol: Telcoin Update
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6672
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/49
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-telcoin-judging/issues/22

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - liquidity_manager
  - payments

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - spyrosonic10
  - 0xGoodess
  - jasonxiale
  - ddimitrov22
  - jonatascm
---

## Vulnerability Title

M-6: FeeBuyback.submit() method may fail if all allowance is not used by referral contract

### Overview


Issue M-6 is a bug in the FeeBuyback.sol contract, which is part of the Telcoin project. The bug was found by jonatascm, jasonxiale, ddimitrov22, 0xGoodess, and spyrosonic10. The bug is that the submit() method may fail if all allowance is not used by the referral contract. This is because the safeApprove() method of the SafeERC20Upgradeable library will revert if the allowance is non-zero. The impact of this bug is that the submit() call will fail until the referral contract uses all allowance. A code snippet and recommendation is provided to fix the issue. The recommendation is to reset the allowance to 0 before non-zero approval. The discussion in the report is about a pull request related to this issue.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-telcoin-judging/issues/22 

## Found by 
jonatascm, jasonxiale, ddimitrov22, 0xGoodess, spyrosonic10

## Summary
Inside `submit()` method of `FeeBuyback.sol`, if token is `_telcoin` then it safeApprove to `_referral` contract.   If `_referral` contract do not use all allowance then `submit()` method will fail in next call. 

## Vulnerability Detail
`SafeApprove()` method of library `SafeERC20Upgradeable` revert in following scenario. 
```solidity
require((value == 0) || (token.allowance(address(this), spender) == 0), 
"SafeERC20: approve from non-zero to non-zero allowance");
```
Submit method is doing `safeApproval` of Telcoin to referral contract.  If referral contract do not use full allowance then subsequent call to submit() method will fails because of `SafeERC20: approve from non-zero to non-zero allowance`.  `FeeBuyback` contract should not trust or assume that referral contract will use all allowance.  If it does not use all allowance in `increaseClaimableBy()` method then submit() method will revert in next call. This vulnerability exists at two places in `submit()` method.  Link given in code snippet section.

## Impact
Submit() call will fail until referral contract do not use all allowance.

## Code Snippet
https://github.com/sherlock-audit/2023-02-telcoin/blob/main/telcoin-audit/contracts/staking/FeeBuyback.sol#L63-L64

https://github.com/sherlock-audit/2023-02-telcoin/blob/main/telcoin-audit/contracts/staking/FeeBuyback.sol#L63-L64

## Tool used

Manual Review

## Recommendation
Reset allowance to 0 before non-zero approval.

```solidity
_telcoin.safeApprove(address(_referral), 0);
_telcoin.safeApprove(address(_referral), _telcoin.balanceOf(address(this)));
```

## Discussion

**amshirif**

https://github.com/telcoin/telcoin-audit/pull/3

**dmitriia**

Looks ok

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Telcoin Update |
| Report Date | N/A |
| Finders | spyrosonic10, 0xGoodess, jasonxiale, ddimitrov22, jonatascm |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-telcoin-judging/issues/22
- **Contest**: https://app.sherlock.xyz/audits/contests/49

### Keywords for Search

`vulnerability`

