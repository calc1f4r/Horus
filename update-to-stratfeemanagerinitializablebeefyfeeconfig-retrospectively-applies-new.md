---
# Core Classification
protocol: Beefy Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 30952
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md
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
  - carlitox477
---

## Vulnerability Title

Update to `StratFeeManagerInitializable::beefyFeeConfig` retrospectively applies new fees to pending LP rewards yet to be claimed

### Overview


This bug report outlines an issue with the fee configuration in the Beefy protocol. The configuration can be updated while LP rewards are being collected and fees are charged, which can result in the protocol owner being able to change the fees and steal pending LP rewards. This is unfair to protocol users who deposited their liquidity at a different fee level. To mitigate this issue, it is recommended that certain functions be declared virtual and overridden to ensure that pending LP rewards are collected and fees are charged correctly before the fee configuration is updated. Beefy has acknowledged this issue.

### Original Finding Content

**Description:** The fee configuration `StratFeeManagerInitializable::beefyFeeConfig` can be updated via `StratFeeManagerInitializable::setBeefyFeeConfig` [L164-167](https://github.com/beefyfinance/experiments/blob/14a313b76888581b05d42b6f7b6097c79f3e65c6/contracts/protocol/beefy/StratFeeManagerInitializable.sol#L164-L167) while LP rewards are collected and fees charged via `StrategyPassiveManagerUniswap::_harvest` [L306-311](https://github.com/beefyfinance/experiments/blob/14a313b76888581b05d42b6f7b6097c79f3e65c6/contracts/protocol/concliq/uniswap/StrategyPassiveManagerUniswap.sol#L306-L311).

This allows the protocol to enter a state where the fee configuration is updated to for example increase Beefy's protocol fees, then the next time `harvest` is called the higher fees are retrospectively applied to the LP rewards that were pending under the previously lower fee regime.

**Impact:** The protocol owner can retrospectively alter the fee structure to steal pending LP rewards instead of distributing them to protocol users; the retrospective application of fees is unfair on protocol users because those users deposited their liquidity into the protocol and generated LP rewards at the previous fee levels.

**Recommended Mitigation:** 1) `StratFeeManagerInitializable::setBeefyFeeConfig` should be declared virtual
2) `StrategyPassiveManagerUniswap` should override it and before calling the parent function, first call `_claimEarnings` then `_chargeFees`

This ensures that pending LP rewards are collected and have the correct fees charged on them, and only after that has happened is the new fee structure updated.

**Beefy:**
Acknowledged.

\clearpage

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Beefy Finance |
| Report Date | N/A |
| Finders | Dacian, carlitox477 |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

