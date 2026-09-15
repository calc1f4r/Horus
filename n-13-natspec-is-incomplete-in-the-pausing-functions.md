---
# Core Classification
protocol: Ondo Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 23524
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-01-ondo
source_link: https://code4rena.com/reports/2023-01-ondo
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

protocol_categories:
  - leveraged_farming
  - rwa
  - services
  - cdp
  - liquid_staking

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[N-13] NatSpec is incomplete in the pausing functions

### Overview

See description below for full details.

### Original Finding Content

In the both pause and unpause functions a comment is made, that the purpose of this functions is to pause or unpause the minting functionality. This NatSpec isn't full as it not only applies on the minting, but on the redeeming as well.

```solidity
contracts/cash/CashManager.sol

522:  /**
523:   * @notice Will pause minting functionality of this contract
524:   *
525:   */
526:  function pause() external onlyRole(PAUSER_ADMIN) {
527:    _pause();
528:  }

530:  /**
531:   * @notice Will unpause minting functionality of this contract
532:   */
533:  function unpause() external onlyRole(MANAGER_ADMIN) {
534:    _unpause();
535:  }

662:  function requestRedemption(
663:    uint256 amountCashToRedeem
664:  )
665:    external
666:    override
667:    updateEpoch
668:    nonReentrant
669:    whenNotPaused
670:    checkKYC(msg.sender)
671:  {
```



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Ondo Finance |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-ondo
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2023-01-ondo

### Keywords for Search

`vulnerability`

