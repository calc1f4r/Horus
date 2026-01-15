---
# Core Classification
protocol: BakerFi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49642
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-12-bakerfi-invitational
source_link: https://code4rena.com/reports/2024-12-bakerfi-invitational
github_link: https://code4rena.com/audits/2024-12-bakerfi-invitational/submissions/F-6

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 6
finders:
  - 0xlemon
  - MrPotatoMagic
  - klau5
  - 0xpiken
  - shaflow2
---

## Vulnerability Title

[H-03] `_deployedAmount` not updated on `StrategySupplyBase.undeploy`, preventing performance fees from being collected

### Overview


This bug report is about a function in the `StrategySupplyBase.sol` contract that does not update a variable called `_deployedAmount`. This causes problems when trying to collect performance fees through a function called `rebalance` after a withdrawal has occurred. The proof of concept provided in the report shows that if a withdrawal is made and profits are generated, the contract will still consider it a loss and no fees will be collected. The recommended mitigation is to update the `_deployedAmount` variable in the `StrategySupplyBase.undeploy` function. The team behind the contract has confirmed this issue and has already implemented a solution in their code. The bug has been successfully mitigated and confirmed by external reviewers.

### Original Finding Content



<https://github.com/code-423n4/2024-12-bakerfi/blob/0daf8a0547b6245faed5b6cd3f5daf44d2ea7c9a/contracts/core/strategies/StrategySupplyBase.sol# L110>

### Finding description and impact

`StrategySupplyBase.undeploy` does not update `_deployedAmount`. As a result, if a withdrawal occurs, even if interest is generated, the protocol cannot collect performance fees through `rebalance`.

### Proof of Concept

`StrategySupplyBase.undeploy` does not update `_deployedAmount`. It should subtract the amount of withdrawn asset tokens.
```

function undeploy(uint256 amount) external nonReentrant onlyOwner returns (uint256 undeployedAmount) {
    if (amount == 0) revert ZeroAmount();

    // Get Balance
    uint256 balance = getBalance();
    if (amount > balance) revert InsufficientBalance();

    // Transfer assets back to caller
    uint256 withdrawalValue = _undeploy(amount);

    // Check withdrawal value matches the initial amount
    // Transfer assets to user
    ERC20(_asset).safeTransfer(msg.sender, withdrawalValue);

    balance -= amount;
    emit StrategyUndeploy(msg.sender, withdrawalValue);
    emit StrategyAmountUpdate(balance);

    return amount;
}
```

As a result, if a withdrawal occurs, even if interest is generated, the protocol cannot collect performance fees through `rebalance`. This is because if the withdrawal amount is greater than the interest earned, the Strategy is considered to have a loss and no fee is taken.

* `_deployedAmount`: A
* Interest generated, `getBalance` returns A + profit
* Request to withdraw amount B

  + `_deployedAmount` is still A
  + `getBalance` returns A + profit - B
* During rebalance, `balanceChange` is (A + profit - B) - A

  + That is, if `profit <= B`, the Strategy is considered to have a loss.
```

function harvest() external returns (int256 balanceChange) {
    // Get Balance
    uint256 newBalance = getBalance();

@>  balanceChange = int256(newBalance) - int256(_deployedAmount);

    if (balanceChange > 0) {
        emit StrategyProfit(uint256(balanceChange));
    } else if (balanceChange < 0) {
        emit StrategyLoss(uint256(-balanceChange));
    }
    if (balanceChange != 0) {
        emit StrategyAmountUpdate(newBalance);
    }
    _deployedAmount = newBalance;
}
```

This is PoC. This shows that when harvested after withdrawal, the Strategy is considered to have a loss. This can be executed by adding it to the `StrategySupplyAAVEv3.ts` file.
```

it('PoC - harvest returns loss after undeloy', async () => {
  const { owner, strategySupply, stETH, aave3Pool, otherAccount } = await loadFixture(
    deployStrategySupplyFixture,
  );
  const deployAmount = ethers.parseEther('10');
  await stETH.approve(await strategySupply.getAddress(), deployAmount);
  await strategySupply.deploy(deployAmount);

  //artificial profit
  const profit = ethers.parseEther('1');
  await aave3Pool.mintAtokensArbitrarily(await strategySupply.getAddress(), profit);

  // Undeploy
  const undeployAmount = ethers.parseEther('2');
  await strategySupply.undeploy(undeployAmount);

  await expect(strategySupply.harvest())
    .to.emit(strategySupply, 'StrategyLoss')
    .to.emit(strategySupply, 'StrategyAmountUpdate');
});
```

### Recommended Mitigation Steps

Update `_deployedAmount` by the withdrawal amount in `StrategySupplyBase.undeploy`.

**chefkenji (BakerFi) confirmed**

**[BakerFi mitigated](https://github.com/code-423n4/2025-01-bakerfi-mitigation?tab=readme-ov-file# findings-being-mitigated):**

> [PR-12](https://github.com/baker-fi/bakerfi-contracts/pull/12)

**Status:** Mitigation confirmed. Full details in reports from [shaflow2](https://code4rena.com/evaluate/2025-01-bakerfi-mitigation-review/findings/S-3) and [0xlemon](https://code4rena.com/evaluate/2025-01-bakerfi-mitigation-review/findings/S-41).

---



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | BakerFi |
| Report Date | N/A |
| Finders | 0xlemon, MrPotatoMagic, klau5, 0xpiken, shaflow2, pfapostol |

### Source Links

- **Source**: https://code4rena.com/reports/2024-12-bakerfi-invitational
- **GitHub**: https://code4rena.com/audits/2024-12-bakerfi-invitational/submissions/F-6
- **Contest**: https://code4rena.com/reports/2024-12-bakerfi-invitational

### Keywords for Search

`vulnerability`

