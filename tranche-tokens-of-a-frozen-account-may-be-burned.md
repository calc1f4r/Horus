---
# Core Classification
protocol: Centrifuge
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35809
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Centrifuge-Spearbit-Security-Review-July-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Centrifuge-Spearbit-Security-Review-July-2024.pdf
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
finders_count: 4
finders:
  - Devtooligan
  - 0xLeastwood
  - Jonatas Martins
  - Gerard Persoon
---

## Vulnerability Title

Tranche tokens of a frozen account may be burned

### Overview

See description below for full details.

### Original Finding Content

## Severity: Low Risk

## Context
- Deployer.sol#L72
- InvestmentManager.sol#L288
- PoolManager.sol#L107
- RestrictionManager.sol#L67

## Description
A user whose account has been frozen can still have their tranche tokens burned. This is inconsistent with the mint function, which prohibits frozen users from minting. As burning can be considered a transfer to the zero address, a frozen account should not be able to perform this action. 

This behavior may violate regulations in some jurisdictions. If an account is frozen for regulatory reasons, burning tokens might be prohibited, similar to how some stablecoins (e.g., USDC) disallow burning of tokens by users on their deny list.

## Recommendation
Call the `_onTransfer` hook in the `Tranche.burn()` function similar to how it is called in `mint()`. This way, if the restriction manager were in place for the tranche, a transaction originating from a frozen user would revert.

```solidity
function burn(address from, uint256 value) public override(ERC20, ITranche) {
    super.burn(from, value);
    _onTransfer(from, address(0), value);
}
```

The function `fulfillRedeemRequest()` will keep working because it burns from escrow and escrow is endorsed, so it will not be blocked by `checkERC20Transfer()`.

## Centrifuge
Fixed in commit `bc1c02e2`.

## Spearbit
Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Centrifuge |
| Report Date | N/A |
| Finders | Devtooligan, 0xLeastwood, Jonatas Martins, Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Centrifuge-Spearbit-Security-Review-July-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Centrifuge-Spearbit-Security-Review-July-2024.pdf

### Keywords for Search

`vulnerability`

