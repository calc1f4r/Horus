---
# Core Classification
protocol: Kinetiq
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58556
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2025-04-kinetiq
source_link: https://code4rena.com/reports/2025-04-kinetiq
github_link: https://code4rena.com/audits/2025-04-kinetiq/submissions/F-18

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
finders_count: 22
finders:
  - zhaojohnson
  - falconhoof
  - adamIdarrha
  - holydevoti0n
  - givn
---

## Vulnerability Title

[M-01] Incorrect Balance Check in Validator Redelegation Process May Block Legitimate Rebalancing Operations

### Overview


The `processValidatorRedelegation` function in the StakingManager contract has an incorrect balance check that could prevent rebalancing operations from being executed. This is because the function checks the wrong balance, causing legitimate rebalancing operations to fail. To fix this, the incorrect balance check should be removed from the function. This bug could lead to operational disruptions and reduced protocol performance.

### Original Finding Content



<https://github.com/code-423n4/2025-04-kinetiq/blob/7f29c917c09341672e73be2f7917edf920ea2adb/src/StakingManager.sol# L365>

### Finding description and impact

The `processValidatorRedelegation` function in the StakingManager contract contains an incorrect balance check that could prevent legitimate rebalancing operations from being executed. The function checks the HyperEVM balance of the StakingManager contract, but the funds being redelegated exist on HyperCore, not on the HyperEVM.

According to the documentation, HYPE staking on Hyperliquid happens within HyperCore. The rebalancing process is designed to delegate/undelegate funds between validators and staking balance on HyperCore without those funds ever leaving the HyperCore environment. However, the current implementation incorrectly checks the StakingManager balance that is on HyperEVM.

When the ValidatorManager’s `closeRebalanceRequests` function is called, it calculates the total amount to be redelegated and then calls `processValidatorRedelegation` on the StakingManager:
```

function closeRebalanceRequests(
    address stakingManager,
    address[] calldata validators
) external whenNotPaused nonReentrant onlyRole(MANAGER_ROLE) {
    // ...
    uint256 totalAmount = 0;
    for (uint256 i = 0; i < validators.length; ) {
        // ...
        totalAmount += request.amount;
        // ...
    }
    // Trigger redelegation through StakingManager if there's an amount to delegate
    if (totalAmount > 0) {
        IStakingManager(stakingManager).processValidatorRedelegation(totalAmount);
    }
}
```

In the StakingManager’s `processValidatorRedelegation` function, there’s an incorrect balance check:
```

function processValidatorRedelegation(uint256 amount) external nonReentrant whenNotPaused {
    require(msg.sender == address(validatorManager), "Only ValidatorManager");
    require(amount > 0, "Invalid amount");
@>    require(address(this).balance >= amount, "Insufficient balance");

    _distributeStake(amount, OperationType.RebalanceDeposit);
}
```

This incorrect balance check could cause legitimate rebalancing operations to fail if the StakingManager doesn’t have sufficient HYPE balance, even though the HyperCore balance is adequate for the redelegation. This would prevent the protocol from properly rebalancing funds between validators, which could lead to operational disruptions and reduced protocol performance.

### Recommended Mitigation Steps

Remove the incorrect balance check from the `processValidatorRedelegation` function:
```

function processValidatorRedelegation(uint256 amount) external nonReentrant whenNotPaused {
    require(msg.sender == address(validatorManager), "Only ValidatorManager");
    require(amount > 0, "Invalid amount");
-   require(address(this).balance >= amount, "Insufficient balance");

    _distributeStake(amount, OperationType.RebalanceDeposit);
}
```

**Kinetiq confirmed**

---



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Kinetiq |
| Report Date | N/A |
| Finders | zhaojohnson, falconhoof, adamIdarrha, holydevoti0n, givn, DemoreX, Infect3d, marchev, KupiaSec, LSHFGJ, zzebra83, dobrevaleri, VAD37, FalseGenius, komronkh, 0xpiken, yaioxy, Ragnarok, 0xG0P1, rouhsamad, Atharv, vangrim |

### Source Links

- **Source**: https://code4rena.com/reports/2025-04-kinetiq
- **GitHub**: https://code4rena.com/audits/2025-04-kinetiq/submissions/F-18
- **Contest**: https://code4rena.com/reports/2025-04-kinetiq

### Keywords for Search

`vulnerability`

