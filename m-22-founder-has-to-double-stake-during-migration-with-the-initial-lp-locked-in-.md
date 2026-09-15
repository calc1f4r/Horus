---
# Core Classification
protocol: Virtuals Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61849
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2025-04-virtuals-protocol
source_link: https://code4rena.com/reports/2025-04-virtuals-protocol
github_link: https://code4rena.com/audits/2025-04-virtuals-protocol/submissions/F-170

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
  - gkrastenov
  - oakcobalt
---

## Vulnerability Title

[M-22] Founder has to double-stake during migration with the initial LP locked in the old `veToken`

### Overview


This bug report discusses a problem with the migration process in the AgentMigrator.sol contract. The issue is that during the migration, founders are facing a double-staking problem where their original LP tokens remain locked in the old AgentVeToken contract while they must provide additional virtual tokens for the migration to the new system. This means that the founders are unable to retrieve their original LP tokens and are required to provide duplicate capital during the migration process. This can have a significant impact as the original LP tokens are locked for 10 years and the value of the locked virtual tokens is also significant. To mitigate this issue, it is recommended to modify the AgentMigrator contract to include a mechanism to unlock LP tokens from the old veToken during migration and to add a privileged function in the AgentVeToken contract for founders to withdraw their locked tokens in case of a migration. A proof of concept has been provided to demonstrate how this issue can occur in practice.

### Original Finding Content



During the migration process implemented in AgentMigrator.sol, founders face a double-staking problem where their original LP tokens remain locked in the old AgentVeToken contract while they must provide additional virtual tokens for the migration to the new system.

### Vulnerabilities

The `AgentMigrator.migrateAgent()` function creates new token, LP, `veToken`, and DAO contracts but fails to provide a mechanism to migrate the founder’s locked tokens from the old `veToken` contract:
```

function migrateAgent(
    uint256 id,
    string memory name,
    string memory symbol,
    bool canStake
) external noReentrant {
    // ...
    // Deploy Agent token & LP
    address token = _createNewAgentToken(name, symbol);
    address lp = IAgentToken(token).liquidityPools()[0];
    IERC20(_assetToken).transferFrom(founder, token, initialAmount);
    IAgentToken(token).addInitialLiquidity(address(this));

    // Deploy AgentVeToken
    address veToken = _createNewAgentVeToken(
        string.concat("Staked ", name),
        string.concat("s", symbol),
        lp,
        founder,
        canStake
    );

    // ...
    _nft.migrateVirtual(id, dao, token, lp, veToken);

    // Stake LP in new veToken
    IERC20(lp).approve(veToken, type(uint256).max);
    IAgentVeToken(veToken).stake(
        IERC20(lp).balanceOf(address(this)),
        founder,
        founder
    );
    // ...
}
```

<https://github.com/code-423n4/2025-04-virtuals-protocol/blob/28e93273daec5a9c73c438e216dde04c084be452/contracts/virtualPersona/AgentMigrator.sol# L107-L131>

Meanwhile, the original LP tokens remain locked in the old `veToken` due to the withdrawal restriction in `AgentVeToken.withdraw()`:
```

function withdraw(uint256 amount) public noReentrant {
    address sender = _msgSender();
    require(balanceOf(sender) >= amount, "Insufficient balance");

    if ((sender == founder) && ((balanceOf(sender) - amount) < initialLock)) {
        require(block.timestamp >= matureAt, "Not mature yet");
    }
    // ...
}
```

<https://github.com/code-423n4/2025-04-virtuals-protocol/blob/28e93273daec5a9c73c438e216dde04c084be452/contracts/virtualPersona/AgentVeToken.sol# L99-L100>

### Impact

* Founders must provide duplicate capital (virtual tokens) during migration, as they cannot retrieve their original LP tokens to retrieve originally deposited virtual tokens in the old uniswap pair.
* Original LP tokens remain locked in obsolete contracts for 10 years. Due to the bonding curve graduation requirements and genesis requirements, the locked virtual token values are significant (roughly 35000 virtual tokens (35000 usd) required to graduate a bonding curve pair).

### Recommended mitigation steps

1. Modify the AgentMigrator contract to include a mechanism to unlock LP tokens from the old `veToken` during migration.
2. Add a privileged function to the AgentVeToken contract that allows the founder to withdraw their locked tokens in case of a migration.

### Proof of Concept

1. Founder deployed initial bonding curve.
2. It requires roughly 35000 virtual tokens (35000 usd) to graduate and deploy agent tokens. At graduation, these are converted to LP tokens and locked in the original veToken, with the founder being unable to withdraw the `initialLock` amount.
3. The protocol team deploys new versions of the Agent contracts and encourages migration.
4. The founder attempts to migrate their Agent using `AgentMigrator.migrateAgent()`.
5. The founder must transfer additional virtual tokens to the new token contract to create new LP (assuming around the same amount of virtual tokens are required).
6. New LP tokens are staked in the new `veToken`, but the original LP tokens (worth `~`35,000 usd) remain locked in the old `veToken`.
7. The founder now has capital locked in two places - the new `veToken` (functional) and the old `veToken` (obsolete).
8. The founder cannot withdraw their original locked LP until after 10 years from the original deployment date.

---



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Virtuals Protocol |
| Report Date | N/A |
| Finders | gkrastenov, oakcobalt |

### Source Links

- **Source**: https://code4rena.com/reports/2025-04-virtuals-protocol
- **GitHub**: https://code4rena.com/audits/2025-04-virtuals-protocol/submissions/F-170
- **Contest**: https://code4rena.com/reports/2025-04-virtuals-protocol

### Keywords for Search

`vulnerability`

