---
# Core Classification
protocol: Stakedotlink Stakingproxy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45294
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-01-20-cyfrin-stakedotlink-stakingproxy-v2.0.md
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
  - 0kage
---

## Vulnerability Title

Storage collision risk in UUPS upgradeable `StakingProxy` due to missing storage gap

### Overview

See description below for full details.

### Original Finding Content

**Description:** `StakingProxy` contract inherits from `UUPSUpgradeable` and `OwnableUpgradeable` but does not implement storage gaps to protect against storage collisions during upgrades.

`StakingProxy` is intended to be used by third parties/DAOs. It is possible that this contract gets inherited by external contracts with their own storage variables. In such a scenario, adding new storage variables to `StakingProxy` during an upgrade can shift storage slots and cause serious storage collision risks.


`StakingProxy.sol`
```solidity
contract StakingProxy is UUPSUpgradeable, OwnableUpgradeable {
    // address of asset token
    IERC20Upgradeable public token;
    // address of liquid staking token
    IStakingPool public lst;
    // address of priority pool
    IPriorityPool public priorityPool;
    // address of withdrawal pool
    IWithdrawalPool public withdrawalPool;
    // address of SDL pool
    ISDLPool public sdlPool;
    // address authorized to deposit/withdraw asset tokens
    address public staker; // ---> @audit missing storage slots
}
```

**Impact:** Potential storage collision can corrupt data and cause contract to malfunction.

**Recommended Mitigation:** Consider adding a storage gap at the end of the contract to reserve slots for future inherited contract variable. A slot size of 50 is the [OpenZeppelin's recommended pattern](https://docs.openzeppelin.com/contracts/3.x/upgradeable#:~:text=Storage%20Gaps,with%20existing%20deployments.) for upgradeable contracts.

**Stake.link:**
Acknowledged.

**Cyfrin:** Acknowledged.

\clearpage

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Stakedotlink Stakingproxy |
| Report Date | N/A |
| Finders | 0kage |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-01-20-cyfrin-stakedotlink-stakingproxy-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

