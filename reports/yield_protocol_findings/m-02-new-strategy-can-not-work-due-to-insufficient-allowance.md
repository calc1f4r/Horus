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
solodit_id: 49648
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-12-bakerfi-invitational
source_link: https://code4rena.com/reports/2024-12-bakerfi-invitational
github_link: https://code4rena.com/audits/2024-12-bakerfi-invitational/submissions/F-4

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
finders_count: 4
finders:
  - shaflow2
  - 0xlemon
  - klau5
  - 0xpiken
---

## Vulnerability Title

[M-02] New strategy can not work due to insufficient allowance

### Overview


This bug report highlights an issue with the `MultiStrategyVault` contract, which is used to manage multiple investment strategies. The problem occurs when a new strategy is added through the `MultiStrategy#addStrategy()` function, which is used to add new strategies to the vault. The issue is that the new strategy is not approved to spend the asset in the vault, which can result in the vault being denied service.

To demonstrate this issue, a proof of concept code is provided in the report. This code can be run to show that the new strategy has zero allowance, meaning it is not approved to spend the asset in the vault. The recommended mitigation steps involve approving the new strategy with a maximum allowance when it is added to the vault. This can be achieved by adding a line of code to the `addStrategy()` function.

The report also mentions that BakerFi has confirmed and mitigated the issue by making the necessary changes to their code. This has been confirmed by two separate reports from independent auditors. 

### Original Finding Content



When a new strategy is added through [`MultiStrategy# addStrategy()`](https://github.com/code-423n4/2024-12-bakerfi/blob/main/contracts/core/MultiStrategy.sol# L107-L112), it was not approved to spend the asset in `MultiStrategyVault`. Any functions that call `newStrategy# deploy()` may revert and result in `MultiStrategyVault` being DoS’ed.

### Proof of Concept

`MultiStrategyVault` is used to manage multiple investment strategies. A new strategy can be added through `MultiStrategy# addStrategy()`:
```

107:    function addStrategy(IStrategy strategy) external onlyRole(VAULT_MANAGER_ROLE) {
108:        if (address(strategy) == address(0)) revert InvalidStrategy();
109:        _strategies.push(strategy);
110:        _weights.push(0);
111:        emit AddStrategy(address(strategy));
112:    }
```

However, the new strategy was not approved to spend the asset in `MultiStrategyVault`, resulting `MultiStrategyVault` being DoS’ed.

Copy below codes to [VaultMultiStrategy.ts](https://github.com/code-423n4/2024-12-bakerfi/blob/main/test/core/vault/VaultMultiStrategy.ts) and run `npm run test`:
```

  it.only('Add Strategy - no allowance', async () => {
    const { vault, usdc, owner, otherAccount } = await loadFixture(deployMultiStrategyVaultFixture);

    //@audit-info deploy a new strategy
    const Strategy = await ethers.getContractFactory('StrategySupplyAAVEv3');
    const strategy = await Strategy.deploy(
      owner.address,
      await usdc.getAddress(),
      otherAccount.address,
    );
    await strategy.waitForDeployment();
    //@audit-info add the new strategy to vault
    await vault.addStrategy(await strategy.getAddress());
    //@audit-info the new strategy has been added
    expect(await vault.strategies()).to.include(await strategy.getAddress());
    expect(await vault.asset()).to.equal(await usdc.getAddress());
    //@audit-info however, the new strategy was not approved to spend asset of vault
    expect(await usdc.allowance(vault.target, strategy.target)).to.equal(0);
  });
```

As we can see, the new strategy has zero allowance.

### Recommended mitigation steps

The new strategy should be approved with max allowance when added:
```

    function addStrategy(IStrategy strategy) external onlyRole(VAULT_MANAGER_ROLE) {
        if (address(strategy) == address(0)) revert InvalidStrategy();
        _strategies.push(strategy);
        _weights.push(0);
+       IERC20(strategy.asset()).approve(address(strategy), type(uint256).max);
        emit AddStrategy(address(strategy));
    }
```

**chefkenji (BakerFi) confirmed**

**[BakerFi mitigated](https://github.com/code-423n4/2025-01-bakerfi-mitigation?tab=readme-ov-file# findings-being-mitigated):**

> [PR-13](https://github.com/baker-fi/bakerfi-contracts/pull/13)

**Status:** Mitigation confirmed. Full details in reports from [0xlemon](https://code4rena.com/evaluate/2025-01-bakerfi-mitigation-review/findings/S-31) and [shaflow2](https://code4rena.com/evaluate/2025-01-bakerfi-mitigation-review/findings/S-7).

---



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | BakerFi |
| Report Date | N/A |
| Finders | shaflow2, 0xlemon, klau5, 0xpiken |

### Source Links

- **Source**: https://code4rena.com/reports/2024-12-bakerfi-invitational
- **GitHub**: https://code4rena.com/audits/2024-12-bakerfi-invitational/submissions/F-4
- **Contest**: https://code4rena.com/reports/2024-12-bakerfi-invitational

### Keywords for Search

`vulnerability`

