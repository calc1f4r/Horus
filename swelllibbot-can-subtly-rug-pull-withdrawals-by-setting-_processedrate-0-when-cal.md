---
# Core Classification
protocol: Swell Barracuda
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31979
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md
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
finders_count: 2
finders:
  - Dacian
  - Carlitox477
---

## Vulnerability Title

`SwellLib.BOT` can subtly rug-pull withdrawals by setting `_processedRate = 0` when calling `swEXIT::processWithdrawals`

### Overview


The bug report describes an issue with the `swEXIT` contract, where the `SwellLib.BOT` can manipulate the exchange rate and withdraw more funds than they are supposed to. This can lead to a "rug-pull" situation where the user's funds are taken without their knowledge. The recommended mitigation is to either always fetch the current rate from `swETH::swETHToETHRate` or only allow the `RepricingOracle` contract to call `swEXIT::processWithdrawals` correctly. The bug has been fixed in recent commits and verified by Cyfrin.

### Original Finding Content

**Description:** When users create a withdrawal request, their `swETH` is [burned](https://github.com/SwellNetwork/v3-contracts-lst/blob/a95ea7942ba895ae84845ab7fec1163d667bee38/contracts/implementations/swEXIT.sol#L202-L205) then the current exchange rate `rateWhenCreated` is [fetched](https://github.com/SwellNetwork/v3-contracts-lst/tree/a95ea7942ba895ae84845ab7fec1163d667bee38/contracts/implementations/swEXIT.sol#L213) from `swETH::swETHToETHRate`:
```solidity
uint256 rateWhenCreated = AccessControlManager.swETH().swETHToETHRate();
```

However `SwellLib.BOT` can [pass an arbitrary value](https://github.com/SwellNetwork/v3-contracts-lst/tree/a95ea7942ba895ae84845ab7fec1163d667bee38/contracts/implementations/swEXIT.sol#L111) for `_processedRate` when calling `swEXIT::processWithdrawals`:
```solidity
function processWithdrawals(
  uint256 _lastTokenIdToProcess,
  uint256 _processedRate
) external override checkRole(SwellLib.BOT) {
```

The [final rate](https://github.com/SwellNetwork/v3-contracts-lst/tree/a95ea7942ba895ae84845ab7fec1163d667bee38/contracts/implementations/swEXIT.sol#L150-L152) used is the lesser of `rateWhenCreated` and `_processedRate`:
```solidity
uint256 finalRate = _processedRate > rateWhenCreated
  ? rateWhenCreated
  : _processedRate;
```

This final rate is [multiplied](https://github.com/SwellNetwork/v3-contracts-lst/tree/a95ea7942ba895ae84845ab7fec1163d667bee38/contracts/implementations/swEXIT.sol#L158) by the requested withdrawal amount to determine the actual amount sent to the user requesting a withdrawal:
```solidity
uint256 requestExitedETH = wrap(amount).mul(wrap(finalRate)).unwrap();
```

Hence `SwellLib.BOT` can subtly rug-pull all withdrawals by setting `_processedRate = 0` when calling `swEXIT::processWithdrawals`.

**Recommended Mitigation:** Two possible mitigations:
1) Change `swEXIT::processWithdrawals` to always fetch the current rate from `swETH::swETHToETHRate`
2) Only allow `swEXIT::processWithdrawals` to be called by the `RepricingOracle` contract which [calls it correctly](https://github.com/SwellNetwork/v3-contracts-lst/tree/a95ea7942ba895ae84845ab7fec1163d667bee38/contracts/implementations/RepricingOracle.sol#L130-L132).

**Swell:** Fixed in commits [c6f8708](https://github.com/SwellNetwork/v3-contracts-lst/commit/c6f870847bdf276aee1bf9aeb1ed71771a2aba04), [64cfbdb](https://github.com/SwellNetwork/v3-contracts-lst/commit/64cfbdbf67e28d84f2a706982e28925ab51fd5e6).

**Cyfrin:**
Verified.

\clearpage

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Swell Barracuda |
| Report Date | N/A |
| Finders | Dacian, Carlitox477 |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

