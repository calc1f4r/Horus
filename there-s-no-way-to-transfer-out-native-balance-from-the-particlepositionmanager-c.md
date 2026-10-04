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
solodit_id: 40721
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/83468b34-954f-4650-b16d-7d72c5477780
source_link: https://cdn.cantina.xyz/reports/cantina_competition_particle_feb2024.pdf
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
finders_count: 1
finders:
  - neumo
---

## Vulnerability Title

There 's no way to transfer out native balance from the particlepositionmanager contract 

### Overview


The ParticlePositionManager contract is not able to transfer out or bridge back Blast's native ETH balance, which can get locked until the contract is upgraded. This issue is considered medium priority because the contract is upgradeable. A recommendation is to implement a function that allows the owner to transfer out the native balance. However, it is noted that the Particle contract does not need to hold any native ETH as it is not supported by the uniswap v3 standard. 

### Original Finding Content

## ParticlePositionManager Contract

## Context
(No context files were provided by the reviewer)

## Description
The `ParticlePositionManager` contract is intended to be deployed in the Blast network. Blast allows contracts and EOAs to set their Yield mode. As seen below, the contract configures itself at construction time.

```solidity
contract ParticlePositionManager {
    // ...
    constructor() payable {
        _disableInitializers();
        // Blast.configure();
    }
    // ...
}
```

And the Blast library sets the claim mode and gas mode of the contract as Claimable and the yield mode of both the USDB and WETHB ERC20 rebasing tokens as Claimable:

```solidity
library Blast {
    // ...
    function configure() external {
        IBlast(BLAST).configureClaimableYield();
        IBlast(BLAST).configureClaimableGas();
        IERC20Rebasing(WETHB).configure(YieldMode.CLAIMABLE);
        IERC20Rebasing(USDB).configure(YieldMode.CLAIMABLE);
    }
    // ...
}
```

The owner of the `ParticlePositionManager` contract will have the power of calling the function `claimYieldMaxGas`.

```solidity
function claimYieldMaxGas(
    address recipient,
    uint256 ethToClaim,
    uint256 wethToClaim,
    uint256 usdbToClaim
) external override onlyOwner nonReentrant whenNotPaused returns (uint256 eth, uint256 weth, uint256 usdb, uint256 gas) {
    (eth, weth, usdb, gas) = Blast.claimYieldMaxGas(recipient, address(this), ethToClaim, wethToClaim, usdbToClaim);
    emit ClaimYieldGas(recipient, eth, weth, usdb, gas);
}
```

Which ends up calling `claimYieldMaxGas` in the Blast library:

```solidity
function claimYieldMaxGas(
    address recipient,
    address protocol,
    uint256 ethToClaim,
    uint256 wethToClaim,
    uint256 usdbToClaim
) external returns (uint256 eth, uint256 weth, uint256 usdb, uint256 gas) {
    eth = IBlast(BLAST).claimYield(protocol, recipient, ethToClaim);
    weth = IERC20Rebasing(WETHB).claim(recipient, wethToClaim);
    usdb = IERC20Rebasing(USDB).claim(recipient, usdbToClaim);
    gas = IBlast(BLAST).claimMaxGas(protocol, recipient);
}
```

This way, the owner can collect the yields generated in Blast's native ETH, USDB, and WETHB, as well as the rewards for the gas used by the contract. To generate Blast's native ETH yield, the contract must have a positive balance (at least 1 share), which can happen, for instance, if someone bridges ETH from the mainnet to the Blast at the `ParticlePositionManager` contract address. This positive balance will generate yield, which the owner can claim later.

The issue here is that the contract does not have any mechanism to transfer this Blast's ETH balance out, or bridge it back to the mainnet, meaning it will get locked until the contract is upgraded to allow it. The fact that the contract is upgradeable is what has made me evaluate this issue as medium instead of high.

## Recommendation
The contract could implement a function that would allow the owner to transfer out the native balance. Something like this:

```solidity
function adminTransferETH(address receiver, uint256 amount) external onlyOwner {
    SafeTransferLib.safeTransferETH(receiver, amount);
}
```

## Particle
Acknowledged. As designed, the Particle contract shouldn’t hold any native ETH since Uniswap V3 standard only supports ERC20 tokens. So the Particle contract doesn’t need to set the native ETH yield mode.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Particle |
| Report Date | N/A |
| Finders | neumo |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_particle_feb2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/83468b34-954f-4650-b16d-7d72c5477780

### Keywords for Search

`vulnerability`

