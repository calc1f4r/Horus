---
# Core Classification
protocol: Sonic Staking
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43977
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Beethoven-Sonic-Staking-Spearbit-Security-Review-December-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Beethoven-Sonic-Staking-Spearbit-Security-Review-December-2024.pdf
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
  - Tnch
  - R0bert
  - 0xWeiss
  - Gerard Persoon
---

## Vulnerability Title

Missing input validation in SFC and treasury initialization

### Overview

See description below for full details.

### Original Finding Content

## Severity: Low Risk

## Context
- **File Locations**: 
  - SonicStaking.sol#L1
  - SonicStaking.sol#L189
  - SonicStaking.sol#L190

## Description
Missing input validation in SFC and treasury initialization. In fact, it is intended for such variables to be validated, as can be seen in the setter function from the treasury, where it is checked that the address is not set to 0:

```solidity
function setTreasury(address newTreasury) external onlyRole(DEFAULT_ADMIN_ROLE) {
    require(newTreasury != address(0), TreasuryAddressCannotBeZero());
    treasury = newTreasury;
}
```

## Recommendation
The following initialization function should include input validation:

```solidity
function initialize(ISFC _sfc, address _treasury) public initializer {
    __ERC20_init("Beets Staked Sonic", "stS"); //ok
    __ERC20Burnable_init();
    __ERC20Permit_init("Beets Staked Sonic");
    __Ownable_init(msg.sender);
    __UUPSUpgradeable_init();
    __ReentrancyGuard_init();
    _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
    require(_treasury != address(0), TreasuryAddressCannotBeZero());
    require(address(_sfc) != address(0), SFCAddressCannotBeZero());
    SFC = _sfc;
    treasury = _treasury;
}
```

## Resolution
- **Beethoven**: Fixed in PR 45.
- **Spearbit**: Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Sonic Staking |
| Report Date | N/A |
| Finders | Tnch, R0bert, 0xWeiss, Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Beethoven-Sonic-Staking-Spearbit-Security-Review-December-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Beethoven-Sonic-Staking-Spearbit-Security-Review-December-2024.pdf

### Keywords for Search

`vulnerability`

