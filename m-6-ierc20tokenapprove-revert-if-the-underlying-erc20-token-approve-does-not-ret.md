---
# Core Classification
protocol: Bond Options
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20730
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/99
source_link: none
github_link: https://github.com/sherlock-audit/2023-06-bond-judging/issues/86

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
  - services

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - tsvetanovv
  - Auditwolf
  - pks\_
  - ctf\_sec
---

## Vulnerability Title

M-6: IERC20(token).approve revert if the underlying ERC20 token approve does not return boolean

### Overview


This bug report is about an issue found in the Bond Protocol's Liquidity Mining Options. The issue is that when transferring tokens, the protocol uses safeTransfer and safeTransferFrom when approving the payout token, but does not use safeApprove. This is a problem because some ERC20 tokens, such as USDT, do not return boolean when calling approve, which causes the transaction to revert. This means that USDT or other ERC20 tokens that do not return boolean for approve are not supported as the payout token. The code snippet associated with the bug is available for review. Manual review was used to identify the bug. The recommended solution is to use safeApprove instead of approve. The fix was implemented in a pull request and looks good according to the discussion.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-06-bond-judging/issues/86 

## Found by 
Auditwolf, ctf\_sec, pks\_, tsvetanovv
## Summary

IERC20(token).approve revert if the underlying ERC20 token approve does not return boolean

## Vulnerability Detail

When transferring the token, the protocol use safeTransfer and safeTransferFrom

but when approving the payout token, the safeApprove is not used

for non-standard token such as USDT,

calling approve will revert because the solmate ERC20 enforce the underlying token return a boolean

https://github.com/transmissions11/solmate/blob/bfc9c25865a274a7827fea5abf6e4fb64fc64e6c/src/tokens/ERC20.sol#L68

```solidity
    function approve(address spender, uint256 amount) public virtual returns (bool) {
        allowance[msg.sender][spender] = amount;

        emit Approval(msg.sender, spender, amount);

        return true;
    }
```

while the token such as USDT does not return boolean

https://etherscan.io/address/0xdac17f958d2ee523a2206206994597c13d831ec7#code#L126

## Impact

USDT or other ERC20 token that does not return boolean for approve is not supported as the payout token

## Code Snippet

https://github.com/sherlock-audit/2023-06-bond/blob/fce1809f83728561dc75078d41ead6d60e15d065/options/src/fixed-strike/liquidity-mining/OTLM.sol#L190

https://github.com/sherlock-audit/2023-06-bond/blob/fce1809f83728561dc75078d41ead6d60e15d065/options/src/fixed-strike/liquidity-mining/OTLM.sol#L504

## Tool used

Manual Review

## Recommendation

Use safeApprove instead of approve



## Discussion

**Oighty**

Agree with proposed solution.

**Oighty**

Fix implemented in https://github.com/Bond-Protocol/options/pull/8

**ctf-sec**

Fix looks good!

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Bond Options |
| Report Date | N/A |
| Finders | tsvetanovv, Auditwolf, pks\_, ctf\_sec |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-06-bond-judging/issues/86
- **Contest**: https://app.sherlock.xyz/audits/contests/99

### Keywords for Search

`vulnerability`

