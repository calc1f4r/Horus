---
# Core Classification
protocol: Arbitrum Token Bridge
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61634
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/arbitrum-token-bridge/01aa719e-9903-4c16-9478-ee241338c74e/index.html
source_link: https://certificate.quantstamp.com/full/arbitrum-token-bridge/01aa719e-9903-4c16-9478-ee241338c74e/index.html
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
finders_count: 2
finders:
  - Poming Lee
  - Jan Gorzny
---

## Vulnerability Title

Missing Checks if Address Is Non-Zero

### Overview

See description below for full details.

### Original Finding Content

**Update**
2021-08-03: the admin team considered adding these checks to the contracts are dangerous.

**Description:** There are many functions that do not validate input addresses. A list of them is provided below, but they might not be comprehensive since there are too many of them.

1.   `packages\arb-bridge-peripherals\contracts\tokenbridge\libraries\gateway\ArbitrumMessenger.sol`: `sendTxToL2`, `sendTxToL1`.
2.   `packages\arb-bridge-peripherals\contracts\tokenbridge\libraries\gateway\GatewayRouter.sol`: `_initialize`, `setDefaultGateway`, `outboundTransfer`, `finalizeInboundTransfer`, `inboundExcrowAndCall`, `getOutboundCalldata`.
3.   `packages\arb-bridge-peripherals\contracts\tokenbridge\ethereum\gateway\L1GatewayRouter.sol`: `_initialize`.
4.   `packages\arb-bridge-peripherals\contracts\tokenbridge\libraries\gateway\ArbitrumGateway.sol`: `_initialize`, `outboundTransfer`, `finalizeInboundTransfer`, `inboundExcrowAndCall`.
5.   `packages\arb-bridge-peripherals\contracts\tokenbridge\libraries\gateway\TokenGateway.sol`: `_initialize`, `isRouter`, `isCounterpartGateway`, `calculateL2TokenAddress`, `getOutboundCalldata`, `finalizeInboundTransfer`.
6.   `packages\arb-bridge-peripherals\contracts\tokenbridge\ethereum\gateway\L1ArbitrumGateway.sol`: `_initialize``getExternalCall`, `createOutboundTx`.
7.   `packages\arb-bridge-peripherals\contracts\tokenbridge\ethereum\gateway\L1ArbitrumExtendedGateway.sol`: `transferExitAndCall`, `getExternalCall`.
8.   `packages\arb-bridge-peripherals\contracts\tokenbridge\ethereum\gateway\L1CustomGateway.sol`: `initialize`.
9.   `packages\arb-bridge-peripherals\contracts\tokenbridge\arbitrum\gateway\L2ArbitrumGateway.sol`: `_initialize`, `createOutboundTx`, `getOutboundCalldata`, `outboundTransfer`.
10.   `packages\arb-bridge-peripherals\contracts\tokenbridge\libraries\L2GatewayToken.sol`: `_initialize`.
11.   `packages\arb-bridge-peripherals\contracts\tokenbridge\arbitrum\gateway\L2ERC20Gateway.sol`: `_initialize`, `handleNoContract`.
12.   `packages\arb-bridge-peripherals\contracts\tokenbridge\arbitrum\gateway\L2WethGateway.sol`: `_initialize`, `handleNoContract`, `outBoundEscrowTransfer`, `_calculateL2TokenAddress`.
13.   `packages\arb-bridge-peripherals\contracts\tokenbridge\arbitrum\gateway\L2CustomGateway.sol`: `_initialize`, `handleNoContract`.
14.   `packages\arb-bridge-peripherals\contracts\tokenbridge\libraries\aeWETH.sol`: `_initialize`.

**Recommendation:** Add relevant checks or make sure the checks are done in their caller/callee functions.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Arbitrum Token Bridge |
| Report Date | N/A |
| Finders | Poming Lee, Jan Gorzny |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/arbitrum-token-bridge/01aa719e-9903-4c16-9478-ee241338c74e/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/arbitrum-token-bridge/01aa719e-9903-4c16-9478-ee241338c74e/index.html

### Keywords for Search

`vulnerability`

