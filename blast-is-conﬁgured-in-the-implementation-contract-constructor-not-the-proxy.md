---
# Core Classification
protocol: Particle
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40716
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/83468b34-954f-4650-b16d-7d72c5477780
source_link: https://cdn.cantina.xyz/reports/cantina_competition_particle_feb2024.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.80
financial_impact: high

# Scoring
quality_score: 4
rarity_score: 3

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - neumo
  - Sujith Somraaj
  - Jonatas Martins
---

## Vulnerability Title

Blast is conﬁgured in the implementation contract constructor, not the proxy 

### Overview


The ParticlePositionManager contract has a bug where the configuration of the yield and gas modes is not being properly applied. This is due to the fact that the contract is sitting behind a proxy, which means that the configuration in the constructor only affects the implementation and not the proxy. As a result, the balances of certain tokens will not accrue any yield or gas fees. The recommended solution is to move the configuration to the initialize function, which should be called through the proxy contract. This bug has been fixed by moving the configuration to the proxy.

### Original Finding Content

## Context
(No context files were provided by the reviewer)

## Description
The `ParticlePositionManager` contract has a line in the constructor (which is currently commented out to deploy on mainnet, but will be uncommented when it is deployed on Blast) intended to configure the yield and gas modes of the contract as claimable.

## ParticlePositionManager
```solidity
// ...
constructor() payable {
    _disableInitializers();
    // Blast.configure();
}
// ...
```

## Blast (library)
```solidity
// ...
function configure() external {
    IBlast(BLAST).configureClaimableYield();
    IBlast(BLAST).configureClaimableGas();
    IERC20Rebasing(WETHB).configure(YieldMode.CLAIMABLE);
    IERC20Rebasing(USDB).configure(YieldMode.CLAIMABLE);
}
// ...
```

The `ParticlePositionManager` is supposed to be sitting behind a proxy, so configuring yield modes in the constructor only affects the implementation, not the proxy. The balances of Blast ETH, USDB, and WETHB will be accruing yield in the proxy contract, not the implementation. Since the proxy will have disabled yield mode (the default for newly created contracts in Blast), they will accrue zero yield and there’s no way to change the modes in the current codebase.

Regarding gas, the contract accruing gas will be the proxy contract (not the implementation), and since the gas mode will be void (the default mode), and there’s no mechanism in place to change that, it will accrue zero gas fees.

## Recommendation
The configuration of the Blast yield modes should be done in the initialize function, which should be called through the proxy contract.

```solidity
constructor() payable {
    _disableInitializers();
    // Blast.configure();
}
// ...
function initialize(
    uint256 feeFactor,
    uint128 liquidationRewardFactor,
    uint256 loanTerm,
    uint256 treasuryRate,
    address blastAdmin
) external initializer {
    __UUPSUpgradeable_init();
    __Ownable_init();
    __Pausable_init();
    updateFeeFactor(feeFactor);
    updateLiquidationRewardFactor(liquidationRewardFactor);
    updateLoanTerm(loanTerm);
    updateTreasuryRate(treasuryRate);
    updateBlastPointsAdmin(blastAdmin);
    // Blast.configure();
}
```

## Particle
Fixed. We moved it to proxy.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 4/5 |
| Rarity Score | 3/5 |
| Audit Firm | Cantina |
| Protocol | Particle |
| Report Date | N/A |
| Finders | neumo, Sujith Somraaj, Jonatas Martins |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_particle_feb2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/83468b34-954f-4650-b16d-7d72c5477780

### Keywords for Search

`vulnerability`

