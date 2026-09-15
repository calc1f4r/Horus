---
# Core Classification
protocol: NounsDAO
chain: everychain
category: uncategorized
vulnerability_type: usdc

# Attack Vector Details
attack_type: usdc
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5666
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/27
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-nounsdao-judging/issues/37

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.47
financial_impact: medium

# Scoring
quality_score: 2.3333333333333335
rarity_score: 5

# Context Tags
tags:
  - usdc
  - blacklisted

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - cccz
  - bin2chen
  - joestakey
  - Zarf
---

## Vulnerability Title

M-6: If the recipient is added to the USDC blacklist, then cancel() does not work

### Overview


This bug report is about the cancel() function not working if the recipient is added to the USDC blacklist. It was found by Zarf, joestakey, cccz, and bin2chen. When cancel() is called, it sends the vested USDC to the recipient and cancels future payments. However, if the recipient is added to the USDC blacklist, then the payer cannot cancel the payment stream and withdraw future payments. This bug was found through manual review. The recommended solution is to store the number of tokens in variables and have the payer or recipient claim it later.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-11-nounsdao-judging/issues/37 

## Found by 
Zarf, joestakey, cccz, bin2chen

## Summary
cancel() will send the vested USDC to the recipient, if the recipient is added to the USDC blacklist, then cancel() will not work

## Vulnerability Detail
When cancel() is called, it sends the vested USDC to the recipient and cancels future payments.
Consider a scenario where if the payer intends to call cancel() to cancel the payment stream, a malicious recipient can block the address from receiving USDC by adding it to the USDC blacklist (e.g. by doing something malicious with that address, etc.), which prevents the payer from canceling the payment stream and withdrawing future payments 
```solidity
    function cancel() external onlyPayerOrRecipient {
        address payer_ = payer();
        address recipient_ = recipient();
        IERC20 token_ = token();

        uint256 recipientBalance = balanceOf(recipient_);

        // This zeroing is important because without it, it's possible for recipient to obtain additional funds
        // from this contract if anyone (e.g. payer) sends it tokens after cancellation.
        // Thanks to this state update, `balanceOf(recipient_)` will only return zero in future calls.
        remainingBalance = 0;

        if (recipientBalance > 0) token_.safeTransfer(recipient_, recipientBalance);
```
## Impact
A malicious recipient may prevent the payer from canceling the payment stream and withdrawing future payments 
## Code Snippet
https://github.com/sherlock-audit/2022-11-nounsdao/blob/main/src/Stream.sol#L237-L249
## Tool used

Manual Review

## Recommendation
Instead of sending tokens directly to the payer or recipient in cancel(), consider storing the number of tokens in variables and having the payer or recipient claim it later

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 2.3333333333333335/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | NounsDAO |
| Report Date | N/A |
| Finders | cccz, bin2chen, joestakey, Zarf |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-nounsdao-judging/issues/37
- **Contest**: https://app.sherlock.xyz/audits/contests/27

### Keywords for Search

`USDC, Blacklisted`

