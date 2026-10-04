---
# Core Classification
protocol: Maia DAO Ecosystem
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26086
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-05-maia
source_link: https://code4rena.com/reports/2023-05-maia
github_link: https://github.com/code-423n4/2023-05-maia-findings/issues/583

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

protocol_categories:
  - dexes
  - cross_chain
  - liquidity_manager
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 7
finders:
  - jasonxiale
  - 1
  - 2
  - Madalad
  - ihtishamsudo
---

## Vulnerability Title

[M-17] Protocol fees can become trapped indefinitely inside the Talos vault contracts

### Overview


This bug report is related to Talos strategy and vault contracts. The function `collectProtocolFees` is used by the owner to receive fees earned by the contract, however, certain ERC20 tokens do not revert on failed transfers and instead return false. This means, that the transfer could fail silently, causing the tokens to be irretrievably trapped in the contract. To prevent this, it is recommended to use OpenZeppelin's SafeERC20 library for ERC20 transfers. The bug has been addressed and the fix is available in the Maia DAO repository.

### Original Finding Content


Talos strategy contracts all inherit logic from `TalosBaseStrategy`, including the function `collectProtocolFees`. This function is used by the owner to receive fees earned by the contract.

Talos vault contracts should be expected to work properly for any token that has a sufficiently liquid Uniswap pool. However, certain ERC20 tokens [do not revert on failed transfers](https://docs.openzeppelin.com/contracts/2.x/api/token/erc20#SafeERC20), and instead return `false`. In `TalosBaseStrategy#collectProtocolFees`, tokens are transferred from the contract to the owner using `transfer`, and the return value is not checked. This means, that the transfer could fail silently; in which case `protocolFees0` and `protocolFees1` would be updated without the tokens leaving the contract. This function is inherited by any Talos vault contract.

This accounting discrepancy causes the tokens to be irretrievably trapped in the contract.

### Proof of Concept

```solidity
    function collectProtocolFees(uint256 amount0, uint256 amount1) external nonReentrant onlyOwner {
        uint256 _protocolFees0 = protocolFees0;
        uint256 _protocolFees1 = protocolFees1;

        if (amount0 > _protocolFees0) {
            revert Token0AmountIsBiggerThanProtocolFees();
        }
        if (amount1 > _protocolFees1) {
            revert Token1AmountIsBiggerThanProtocolFees();
        }
        ERC20 _token0 = token0;
        ERC20 _token1 = token1;
        uint256 balance0 = _token0.balanceOf(address(this));
        uint256 balance1 = _token1.balanceOf(address(this));
        require(balance0 >= amount0 && balance1 >= amount1);
        if (amount0 > 0) _token0.transfer(msg.sender, amount0); // @audit should use `safeTransfer`
        if (amount1 > 0) _token1.transfer(msg.sender, amount1); // @audit should use `safeTransfer`

        protocolFees0 = _protocolFees0 - amount0;
        protocolFees1 = _protocolFees1 - amount1;
        emit RewardPaid(msg.sender, amount0, amount1);
    }
```

<https://github.com/code-423n4/2023-05-maia/blob/main/src/talos/base/TalosBaseStrategy.sol#L394-L415>

### Recommended Mitigation Steps

Use [OpenZeppelin's SafeERC20](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/utils/SafeERC20.sol) library for ERC20 transfers.

### Assessed type

ERC20

**[deadrxsezzz (warden) commented](https://github.com/code-423n4/2023-05-maia-findings/issues/583#issuecomment-1652526255):**
 > Since we are talking about ERC20 transfer, the only reason for an ERC20 transfer to fail would be insufficient balance. However, there is a require statement that checks if the balance is enough. This check makes a silent fail impossible to happen.

**[Trust (judge) commented](https://github.com/code-423n4/2023-05-maia-findings/issues/583#issuecomment-1653263459):**
 > I disagree. ERC20s are free to implement their own logic and the transfer can fail for other reasons, e.g. blacklisted address. Therefore, using `safeTransfer` is a requirement.

**[0xLightt (Maia) confirmed](https://github.com/code-423n4/2023-05-maia-findings/issues/583#issuecomment-1655668642)**

**[0xLightt (Maia) commented](https://github.com/code-423n4/2023-05-maia-findings/issues/583#issuecomment-1709162752):**
 > Addressed [here](https://github.com/Maia-DAO/eco-c4-contest/tree/577-57-504-658-583-730).

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Maia DAO Ecosystem |
| Report Date | N/A |
| Finders | jasonxiale, 1, 2, Madalad, ihtishamsudo |

### Source Links

- **Source**: https://code4rena.com/reports/2023-05-maia
- **GitHub**: https://github.com/code-423n4/2023-05-maia-findings/issues/583
- **Contest**: https://code4rena.com/reports/2023-05-maia

### Keywords for Search

`vulnerability`

