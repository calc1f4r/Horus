---
# Core Classification
protocol: Restakefi Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32734
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/restakefi-audit
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Shares Not Burned After Redemption of Underlying Assets

### Overview


The report discusses a bug in the asset withdrawal process of the protocol. The process involves two steps, where depositors first request a withdrawal using a specific function and then redeem their underlying assets using another function. However, due to a flaw in the code, the shares associated with the withdrawal request are not being burned, causing them to remain stuck in the contract. This also affects the conversion of balances to shares and vice versa. The report suggests either burning the shares before removing the request from the list or using a temporary variable to store the value that will later be burned. The bug has been resolved in a recent update.

### Original Finding Content

The asset withdrawal process from the protocol is a two-step procedure. Initially, depositors must request a withdrawal using the [`requestWithdraw`](https://github.com/DigitalMOB2/refi-protocol/blob/dc842fd071f225c9d1ff9ad4677b986970125cf9/contracts/Controller.sol#L140) function, requesting the amount in underlying units. This amount is then converted into shares and, if all balance checks pass, transferred back to the `Controller` contract. The request is subsequently added to the pending list, awaiting processing by the `StrategyManager`. Each request is assigned an ID and includes multiple parameters, such as the request owner and the amount of shares associated with that request.


Once the `StrategyManager` processes the withdrawals, users can redeem their underlying assets using the [`redeemUnderlying`](https://github.com/DigitalMOB2/refi-protocol/blob/dc842fd071f225c9d1ff9ad4677b986970125cf9/contracts/Controller.sol#L179) function, inputting the request ID. The function converts the shares tied to the request into underlying units using the [sharesToBalance](https://github.com/DigitalMOB2/refi-protocol/blob/dc842fd071f225c9d1ff9ad4677b986970125cf9/contracts/Controller.sol#L205) function, and then this amount of underlying is transferred to the user. The request is [removed](https://github.com/DigitalMOB2/refi-protocol/blob/dc842fd071f225c9d1ff9ad4677b986970125cf9/contracts/Controller.sol#L207) from the list of withdrawal requests and the function attempts to burn the shares associated with the request using the [`controlledBurnSharesFrom`](https://github.com/DigitalMOB2/refi-protocol/blob/dc842fd071f225c9d1ff9ad4677b986970125cf9/contracts/Controller.sol#L210) function, specifying the `req.shares` value involved as the burn amount.


However, as this request is [removed from the list](https://github.com/DigitalMOB2/refi-protocol/blob/dc842fd071f225c9d1ff9ad4677b986970125cf9/contracts/Controller.sol#L207) once the underlying assets are transferred to the user, the value of `req.shares` will be zero. Due to this, shares will never be burned and will remain stuck in the `Controller` contract.


Moreover, as all calculations for converting balances to shares (and vice versa) depend on the total supply of shares, the underlying balances will not properly reflect the conversion due to an always-increasing `totalShares` value.


A step-by-step proof-of-concept can be found in [this secret gist](https://gist.github.com/m9800/fa0533ce16d242279cf157758f123426).


Consider either burning the shares before removing the request from the list of withdrawal requests, or using a temporary variable to store the value that will later be burned.


***Update:** Resolved in [pull request #14](https://github.com/DigitalMOB2/refi-protocol/pull/14) at commit [376f4e4](https://github.com/DigitalMOB2/refi-protocol/pull/14/commits/376f4e4528d79411107ae62778d58b2d4af651de).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Restakefi Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/restakefi-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

