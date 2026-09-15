---
# Core Classification
protocol: Sudoswap LSSVM2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18322
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf
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
finders_count: 5
finders:
  - Gerard Persoon
  - Shodan
  - Rajeev
  - Lucas Goiriz
  - David Chaparro
---

## Vulnerability Title

Missing sanity zero-address checks may lead to undesired behavior or lock of funds

### Overview

See description below for full details.

### Original Finding Content

## Severity: Low Risk

## Context
- `StandardSettings.sol#L38-L42`
- `StandardSettings.sol#L164-L206`
- `LSSVMPairFactory.sol#L82-L98`
- `VeryFastRouter.sol#L48-L50`
- `StandardSettings.sol#L132`
- `Splitter.sol#L34`
- `VeryFastRouter.sol#L210`
- `LSSVMRouter.sol#L597`
- `LSSVMRouter.sol#L362`
- `LSSVMRouter.sol#L232`
- `LSSVMPairFactory.sol#L393`
- `LSSVMPairETH.sol#L114`
- `LSSVMPairETH.sol#L95`
- `LSSVMPairETH.sol#L63`

## Description
Certain logic requires zero-address checks to avoid undesired behavior or lock of funds. For example, in `Splitter.sol#L34` users can permanently lock ETH by mistakenly using `safeTransferETH` with a default/zero-address value.

## Recommendation
Check if an address-type variable is `address(0)` and revert when true with an appropriate error message. In particular, see:
- In `StandardSettings.sol#L38-L42`: consider adding `require(_settingsFeeRecipient != address(0))`.
- In `StandardSettings.sol#L164-L206`: consider adding `require(pairInfo.prevOwner != address(0))`.
- In `LSSVMPairFactory.sol#L82-L98`: consider adding `require(_protocolFeeRecipient != address(0))`.
- In `VeryFastRouter.sol#L48-L50`: consider adding `require(_factory != address(0))`.
- In `StandardSettings.sol#L132`, `Splitter.sol#L34`, `VeryFastRouter.sol#L210`, `LSSVMRouter.sol#L597`, `LSSVMRouter.sol#L362`, `LSSVMRouter.sol#L232`, `LSSVMPairFactory.sol#L393`, `LSSVMPairETH.sol#L114`, `LSSVMPairETH.sol#L95`, `LSSVMPairETH.sol#L63`: consider adding a zero-address check on the caller of `safeTransferETH`.

## Sudorandom Labs
We're going to pass on this since the exploit scope is low impact.

## Spearbit
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Sudoswap LSSVM2 |
| Report Date | N/A |
| Finders | Gerard Persoon, Shodan, Rajeev, Lucas Goiriz, David Chaparro |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

