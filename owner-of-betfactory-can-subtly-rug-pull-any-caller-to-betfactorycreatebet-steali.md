---
# Core Classification
protocol: Wannabet
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64639
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md
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
finders_count: 2
finders:
  - Immeas
  - Dacian
---

## Vulnerability Title

Owner of `BetFactory` can subtly rug-pull any caller to `BetFactory::createBet` stealing their tokens

### Overview


The report describes a bug in the `BetFactory` contract that allows the owner to steal tokens from anyone who calls the `createBet` function. This is possible because the owner can set the `BetFactory` contract to use a malicious contract that mimics Aave's `supply` function and transfers tokens to itself. This is because the `Bet::initialize` function gives maximum approval to the pool and then calls the `supply` function on it. To fix this, it is recommended to include `tokenToPool[asset]` in the salt passed to `Clones.cloneDeterministic` in the `createBet` and `predictBetAddress` functions. This will prevent the owner from setting the Aave pool associated with a token to an illegitimate pool. The bug has been fixed in the `WannaBet` contract by including the Aave pool in the salt, but this was later removed after implementing fixes for another issue. The report has been verified by `Cyfrin`.

### Original Finding Content

**Description:** Owner of `BetFactory` can rug-pull any caller to `createBet` stealing their tokens by front-running to call `BetFactory::setPool` with the address of a malicious contract that implements the same interface as Aave `supply` function and just transfers tokens to itself.

This works since `Bet::initialize` gives max approval to the pool then calls the `supply` function on it:
```solidity
// If the pool is set, approve and supply the funds to the pool
if (pool != address(0)) {
    IERC20(initialBet.asset).approve(pool, type(uint256).max);

    _aavePool.supply(
        initialBet.asset,
        initialBet.makerStake,
        address(this),
        0
    );
}
```

**Recommended Mitigation:** In `BetFactory::createBet,predictBetAddress` include `tokenToPool[asset]` in the salt passed to `Clones.cloneDeterministic`. This way if it has changed the new `Bet` contract will be created at a different address which the caller has not approved, the first token transfer in `Bet::initialize` will revert causing the entire transaction to revert.

The recommended fix for I-9 also resolves this issue, since it prevents the owner from setting the Aave pool associated with a token to an illegitimate pool.

**WannaBet:** Initially we fixed this in commit [fbd8016](https://github.com/gskril/wannabet-v2/commit/fbd80169eebe70ce96a0ddbbe61035014ee0b018) by including the aave pool in the salt. But after implementing the fixes for I-9 (pool validation) in commit [70e1565](https://github.com/gskril/wannabet-v2/commit/70e1565b391992b7ea8b11f2cc59195478a69212) we no longer included the pool in the salt since the pool can only be set to a valid one.

**Cyfrin:** Verified.

\clearpage

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Wannabet |
| Report Date | N/A |
| Finders | Immeas, Dacian |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

