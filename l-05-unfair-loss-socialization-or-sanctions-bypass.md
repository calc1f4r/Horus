---
# Core Classification
protocol: USDV_2025-03-06
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57858
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/USDV-security-review_2025-03-06.md
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

[L-05] Unfair loss socialization or sanctions bypass

### Overview

See description below for full details.

### Original Finding Content

Take a look at `ExternalRequestsManager.sol#requestBurn()`

```solidity
function requestBurn(uint256 _issueTokenAmount, address _withdrawalTokenAddress, uint256 _minWithdrawalAmount)
    public
    onlyAllowedProviders
|>   allowedToken(_withdrawalTokenAddress)
    whenNotPaused
{
    // Implementation
}
```

Now would be key to note that the protocol allows users to mint tokens by depositing various supported assets (currently USDC and USDT, _with more potentially added in the future_). However, when burning tokens to reclaim their deposits, users can specify any supported token as their withdrawal token, regardless of what they originally deposited.

This is problematic because it fails to maintain a proper relationship between what users deposit and what they withdraw. For example:

1. User A deposits 1000 USDC to mint protocol tokens.
2. User B deposits 1000 USDT to mint protocol tokens.
3. Both deposits are transferred to the treasury.
4. If USDT experiences a black swan event (depegging, hack, etc.).
5. User A can choose to withdraw USDT instead of their original USDC deposit.

So this design creates a "first to exit" scenario during market stress events, allowing early users to externalize losses to later users. When a supported asset faces a black swan event:

1. Users who deposited the compromised asset can withdraw from other, healthier asset pools.
2. This depletes the treasury of healthy assets.
3. Later users are forced to accept the compromised asset or be unable to withdraw at all.

The problem worsens as more deposit assets are added to the protocol. Instead of each user bearing the risk of their chosen deposit asset, the risk becomes socialized across all users of the protocol (asides the malicious one who intentionally delegates the loss to the other users).

As hinted by the title also, this bug case allows for OFAC sanctioned accounts to bypass their sanctions and still have access to funds, cause, assuming we have a user who initially deposited and minted with USDT and is now blacklisted on USDT, they can withdraw assets from the treasury, and all they need to do is specify `USDC` as their withdrawal token, sidestepping the sanction.

**Recommendation**

Since we already track the original deposit token for each mint request, we should enforce that users can only withdraw the same type of token they initially deposited.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | USDV_2025-03-06 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/USDV-security-review_2025-03-06.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

