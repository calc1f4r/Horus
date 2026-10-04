---
# Core Classification
protocol: Hyperdrive June 2023
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35870
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-June-2023.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-June-2023.pdf
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Saw-Mon and Natalie
  - Christoph Michel
  - Deivitto
  - M4rio.eth
---

## Vulnerability Title

Not using safe version of ERC20 transfer / transferFrom / approve can lead to wrong scenarios

### Overview


This bug report discusses an issue with certain tokens (such as ZRX) not properly reverting transactions when a transfer fails. This requires additional checks in the code and can make certain tokens incompatible. The report suggests using a safeTransferFrom function and a SafeApprove library to improve compatibility with these tokens.

### Original Finding Content

## Severity: Medium Risk

## Context
- HyperdriveFactory.sol#L205
- ERC4626Hyperdrive.sol#L115
- BondWrapper.sol#L148
- BondWrapper.sol#L183
- HyperdriveFactory.sol#L205
- AaveHyperdrive.sol#L63
- DsrHyperdrive.sol#L70
- ERC4626Hyperdrive.sol#L68
- ERC4626Hyperdrive.sol#L86
- StethHyperdrive.sol#L96
- ERC4626Hyperdrive.sol#L51
- DsrHyperdrive.sol#L52
- AaveHyperdrive.sol#L45
- HyperdriveFactory.sol#L210

## Description
Some tokens (like ZRX) do not revert the transaction when the `transfer` / `transferFrom` fails and return false, which requires us to check the return value after calling the `transfer` / `transferFrom` function. While the code checks for the return value in all other instances of `transfer` and `transferFrom`:

- HyperdriveFactory.sol#L205

Additionally, note that some ERC20 tokens don't have any return value, for example USDT, BNB, OMG. This will make the expected return value to fail if these tokens are used on the `if (!success) revert` pattern, which is the predominant case in the code, making these tokens not compatible as base tokens. 

Assuming `aToken` is set to the correct address, the `aToken` case can avoid the check as it's known to revert on fail transfer, and therefore is not included in the context files.

The AaveHyperdrive contract sets ERC20 approvals by calling `token.approve(operator, amount)`. This comes with several issues:

1. `ERC20.approve` returns a success boolean that is not checked. Some tokens don't revert and return false instead.
2. Non-standard tokens like USDT return no data at all, but the `IERC20.approve` interface expects the call to return data and attempts to decode it into a boolean. The approval calls will fail for USDT.
3. Non-standard tokens like USDT require approvals to be reset to zero first before being able to set them to a different non-zero value again.

**Approve instances:**
- ERC4626Hyperdrive.sol#L51
- DsrHyperdrive.sol#L52
- AaveHyperdrive.sol#L45
- HyperdriveFactory.sol#L210

## Recommendation
Use some `safeTransferFrom` from OZ or Solady to add better compatibility with more tokens and handle return values where missing boolean check. Also, consider using a SafeApprove library to set ERC20 approvals (note that the mentioned Solady library has a `SafeTransferLib.safeApprove` function, but it does not set approvals to zero first, which is required for point 3). The OpenZeppelin library has a `forceApprove` function for this case.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Hyperdrive June 2023 |
| Report Date | N/A |
| Finders | Saw-Mon and Natalie, Christoph Michel, Deivitto, M4rio.eth |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-June-2023.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-June-2023.pdf

### Keywords for Search

`vulnerability`

