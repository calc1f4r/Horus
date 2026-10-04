---
# Core Classification
protocol: Gearbox
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19384
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/gearbox/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/gearbox/review.pdf
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
  - Sigma Prime
---

## Vulnerability Title

Liquidation Avoidance through Rejecting Native Ether Transfers

### Overview


This bug report discusses a vulnerability in Gearbox, a composable DeFi protocol, where borrowers can avoid liquidations by creating a CreditAccount from a contract address that reverts every time it receives native ETH transfers. Malicious borrowers could cause WETHGateway.unwrapWETH() to revert by having the receive() function of a borrowing contract actively revert. The development team recommended removing the option to unwrap WETH when transferring any remaining funds to the borrower. This was implemented in commit fb616cc5 and the issue was mitigated.

### Original Finding Content

## Description
Borrowers can avoid liquidations by creating a CreditAccount from a contract address that reverts every time it receives native ETH transfers. Gearbox is designed as a composable DeFi protocol. Therefore, it is possible to open a CreditAccount from a contract address.

This may create issues when `CreditManager.closeCreditAccount()` attempts to convert `remainingFunds` into native ETH and transfer them to the borrower, when the underlying token is WETH. Malicious borrowers could cause `WETHGateway.unwrapWETH()` to revert by having the `receive()` function of a borrowing contract actively revert. This vulnerability could be exploited to avoid liquidations indefinitely.

## Recommendations
Remove the option to unwrap WETH when transferring any remaining funds to the borrower. This can be implemented under the following adjustment:

```solidity
// transfer remaining funds to borrower [Liquidation case only]
if (remainingFunds > 1) {
    _safeTokenTransfer(
        creditAccount,
        underlyingToken,
        borrower,
        remainingFunds,
        false // convertWETH == false
    );
}
```

## Resolution
The development team mitigated the issue in commit `fb616cc5` by implementing the recommendations above.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Gearbox |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/gearbox/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/gearbox/review.pdf

### Keywords for Search

`vulnerability`

