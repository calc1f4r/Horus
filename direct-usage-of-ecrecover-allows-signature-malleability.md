---
# Core Classification
protocol: Interest Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19434
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/interest-protocol/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/interest-protocol/review.pdf
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
  - Sigma Prime
---

## Vulnerability Title

Direct usage of ecrecover() allows signature malleability

### Overview

See description below for full details.

### Original Finding Content

## Description

The `permit()` and `delegateBySig()` functions call `ecrecover()` directly to verify the given signature. The `ecrecover` precompiled contract allows for malleable (non-unique) signatures and thus is susceptible to replay attacks. Note, although a replay attack on this contract is not possible since each user’s nonce is used only once, rejecting malleable signatures is considered a best practice.

## Recommendations

- Reject malleable signatures (i.e. require the `s` value to be in the lower half order, and the `v` value to be either `27` or `28`).
- Consider using the following OpenZeppelin’s `ECDSA.sol` library that has those checks built in.

## Resolution

The development team has resolved this issue as per commit `8c5cae0`.

## INT-20 Sudden Price Drop Renders Vaults Insolvent

## Asset Lending and Oracle Contracts

**Status:** Closed: See Resolution  
**Rating:** Informational

### Description

Sudden change in the price of an underlying collateral token may render the vault insolvent. Consider a situation where an asset drops in price significantly without liquidations occurring. Some potential scenarios for this might be:

- The price drop is extremely rapid.
- Network delays or downtime make liquidations impossible.
- Oracle downtime or other issues prevent liquidations.
- Gas fees peak so high during a time of extreme volatility that most liquidations are not profitable.

In this situation, if the asset’s LTV and price drop is high enough, it is possible for vaults that have borrowed against that asset to become insolvent.

Consider an asset with a LTV of 75% and a liquidation penalty of 10%. Suppose it has an initial price of $2,000. A user mints a vault and deposits one token in the vault and borrows the full allowance of 1500 USDi.

If the price now drops by 20%, to $1,600, the borrowing allowance will drop to $1,200, allowing liquidation. If we use the formula from page 11 of the protocol’s whitepaper:

```
1500 - (1200/1600) * (1 - 0.1 - 0.75) = 300/1600 * 0.15 = 1.25
```

125% of the vault’s assets can be liquidated to reach solvency: in practice, this means that the entire asset holding of the vault will be liquidated, but it will still not be solvent. There will still be USDi lent out against the vault, and there are no assets to be retrieved by repaying those USDi. Those USDi are also not balanced against USDC in the reserve, as they were not created by a deposit of USDC.

Consider a situation in which this occurs across a large number of vaults, leading to a large number of unbacked USDi which the protocol would have no mechanism to account for. As USDi is no longer matched by other assets, it is likely that there could be a run on USDi, the first stage of which would be emptying the reserve. This would create high interest rates of USDi, but this would not be advantageous to the protocol’s stability as USDi is no longer backed by USDC. Some vault depositors would buy up USDi as the lower prices would allow them to liquidate their vaults cheaply, but this would simply remove the remaining assets from the protocol, ultimately leaving all those still holding USDi with an unbacked token for a protocol with no assets.

### Recommendations

As this issue relates to the design of the protocol and not its Solidity implementation, the testing team raises this issue as informational for the reader to be aware of the behavior outlined above.

### Resolution

This risk was accepted by the project team. No mitigations have been implemented.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Interest Protocol |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/interest-protocol/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/interest-protocol/review.pdf

### Keywords for Search

`vulnerability`

