---
# Core Classification
protocol: Superform v2 Periphery
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63087
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Superform-v2-periphery-Spearbit-Security-Review-June-2025.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Superform-v2-periphery-Spearbit-Security-Review-June-2025.pdf
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
finders_count: 5
finders:
  - MiloTruck
  - Christoph Michel
  - Ethan
  - Noah Marconi
  - Ladboy233
---

## Vulnerability Title

Malicious strategist can bypass the slippage protection

### Overview


Bug Summary:

The SuperVaultStrategy contract has a medium risk bug that allows a malicious strategist to disable slippage protection and potentially extract funds. This bug also affects the fulfillRedeemRequests and _processSingleFulfillHookExecution functions. To fix this, the report recommends charging a deposit/collateral from the strategist address and slashing them offline if they execute the transaction maliciously.

### Original Finding Content

## Security Review

## Severity
**Medium Risk**

## Context
`SuperVaultStrategy.sol#L137-L160`

## Description
When hooks are executed in `executeHooks`, this parameter serves as slippage protection:

```solidity
bool usePrevHookAmount = _decodeHookUsePrevHookAmount(hook, hookCalldata);
if (usePrevHookAmount && prevHook != address(0)) {
    vars.outAmount = _getPreviousHookOutAmount(prevHook);
    if (expectedAssetsOrSharesOut == 0) revert ZERO_EXPECTED_VALUE();
    uint256 minExpectedPrevOut = expectedAssetsOrSharesOut * (BPS_PRECISION - _getSlippageTolerance());
    if (vars.outAmount * BPS_PRECISION < minExpectedPrevOut) {
        revert MINIMUM_PREVIOUS_HOOK_OUT_AMOUNT_NOT_MET();
    }
}
```

A malicious strategist can supply arbitrary `args.expectedAssetsOrSharesOut` to disable the slippage protection and frontrun certain hook execution (swap execution) to extract funds. The same issue exists when the strategist executes `fulfillRedeemRequests` and `_processSingleFulfillHookExecution`. A malicious strategist can supply arbitrary `args.expectedAssetsOrSharesOut` to disable the slippage protection to make users receive too few assets.

```solidity
if (vars.outAmount * BPS_PRECISION < expectedAssetOutput * (BPS_PRECISION - _getSlippageTolerance())) {
    revert MINIMUM_OUTPUT_AMOUNT_ASSETS_NOT_MET();
}
```

## Recommendation
Charge deposit/collateral from the strategist address and slash them offline if the strategist does execute the transaction maliciously.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Superform v2 Periphery |
| Report Date | N/A |
| Finders | MiloTruck, Christoph Michel, Ethan, Noah Marconi, Ladboy233 |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Superform-v2-periphery-Spearbit-Security-Review-June-2025.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Superform-v2-periphery-Spearbit-Security-Review-June-2025.pdf

### Keywords for Search

`vulnerability`

