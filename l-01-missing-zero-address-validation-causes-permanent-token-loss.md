---
# Core Classification
protocol: Colbfinance Usc Offramp
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63346
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/ColbFinance-USC-OffRamp-Security-Review.md
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
  - Shieldify Security
---

## Vulnerability Title

[L-01] Missing Zero Address Validation Causes Permanent Token Loss

### Overview

See description below for full details.

### Original Finding Content


## Severity

Low Risk

## Description

The `PortalCCIP` contract contains a critical vulnerability where tokens can be permanently lost during cross-chain bridging operations. The issue arises from the missing validation of the `destinationAddress` parameter before burning tokens in the `sendDirect()` function.

When a user initiates a bridge transaction via `sendDirect()`, the contract:

- Does NOT validate if `destinationAddress` is `address(0)`
- Burns the tokens on the source chain
- Sends a CCIP message to the destination chain

However, when the CCIP message arrives at the destination chain, `ccipReceive()` performs validation:

```solidity
if (destinationAddress == address(0)) {
    revert InvalidDestinationAddress();
}
```

This causes the transaction to revert on the destination chain AFTER tokens have already been burned on the source chain, resulting in permanent loss of funds with no recovery mechanism.

## Location of Affected Code

File: [contracts/ccip/PortalCCIP.sol#L342-L345](https://github.com/COLB-DEV/SmartContracts/blob/feat/usc-ramps/contracts/ccip/PortalCCIP.sol#L342-L345)

```solidity
function ccipReceive(Client.Any2EVMMessage calldata message) external whenNotPaused {
  // code
  // validate destination address
  if (destinationAddress == address(0)) {
      revert InvalidDestinationAddress();
  }
  // code
}
```

## Impact

Users lose their bridged tokens with no recourse.

## Recommendation

Add `destinationAddress` validation before burning.

## Team Response

Fixed.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Colbfinance Usc Offramp |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/ColbFinance-USC-OffRamp-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

