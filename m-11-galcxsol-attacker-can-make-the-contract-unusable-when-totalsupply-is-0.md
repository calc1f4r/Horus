---
# Core Classification
protocol: Alchemix
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2376
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-05-alchemix-contest
source_link: https://code4rena.com/reports/2022-05-alchemix
github_link: https://github.com/code-423n4/2022-05-alchemix-findings/issues/198

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
  - liquid_staking
  - dexes
  - yield
  - cross_chain
  - rwa

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - TerrierLover
---

## Vulnerability Title

[M-11] [gALCX.sol] Attacker can make the contract unusable when totalSupply is 0

### Overview


This bug report is about a vulnerability in the gALCX contract, which is part of the 2022-05-alchemix project hosted on GitHub. The vulnerability can cause the contract to become unusable when the totalSupply is set to 0 and the balance of the contract is greater than 0. This can happen if the attacker sends the ALCX token directly to the gALCX contract, bypassing the stake function.

When this happens, the bumpExchangeRate function fails, and the stake, unstake, and migrateSource functions do not work as expected. The recommended mitigation step is to add handling when totalSupply is 0 but the balance of the contract is greater than 0.

Static code analysis was used to identify the vulnerability. The proof of concept involves the following steps: deploying the gALCX contract, sending the ALCX token directly to the contract, and then trying to call the stake function.

### Original Finding Content

_Submitted by TerrierLover_

An attacker can make the contract unusable when totalSupply is 0. Specifically,  `bumpExchangeRate` function does not work correctly which results in making `stake`, `unstake` and `migrateSource` functions that do not work as expected.

### Proof of Concept

Here are steps on how the `gALCX` contract can be unusable.

1.  `gALCX` contract is deployed

2.  The attacker sends the `ALCX` token to the deployed `gALCX` contract directly instead of using `stake` function so that the following `balance` variable has value.

[gALCX.sol#L73-L75](https://github.com/code-423n4/2022-05-alchemix/blob/main/contracts-hardhat/gALCX.sol#L73-L75)<br>
    uint balance = alcx.balanceOf(address(this));

    if (balance > 0) {

3.  Since the `ALCX` token is given to the `gALCX` contract directly, `totalSupply == 0` and `alcx.balanceOf(address(this)) > 0` becomes true.

[gALCX.sol#L76](https://github.com/code-423n4/2022-05-alchemix/blob/main/contracts-hardhat/gALCX.sol#L76)<br>

    exchangeRate += (balance * exchangeRatePrecision) / totalSupply;

4.  Non attackers try to call `stake` function, but `bumpExchangeRate` function fails because of `(balance * exchangeRatePrecision) / totalSupply` when totalSupply is 0.

5.  Owner cannot call `migrateSource` function since `bumpExchangeRate` will be in the same situation mentioned in the step4 above

### Recommended Mitigation Steps

Add handling when `totalSupply` is 0 but `alcx.balanceOf(address(this))` is more than 0.

**[0xfoobar (Alchemix) acknowledged and commented](https://github.com/code-423n4/2022-05-alchemix-findings/issues/198#issuecomment-1133996854):**
 > Given that the gALCX deployment has 412 unique tokenholders on mainnet, this series of events is extraordinarily unlikely to occur. But we will keep it in mind for future deployments.

**[0xleastwood (judge) commented](https://github.com/code-423n4/2022-05-alchemix-findings/issues/198#issuecomment-1146895463):**
 > Nice find! Early stakers can DoS new contract deployments, making it impossible for other users to participate in the protocol. As this does not lead to lost funds and is recoverable through redeployment, I believe medium severity to be justified by the warden.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Alchemix |
| Report Date | N/A |
| Finders | TerrierLover |

### Source Links

- **Source**: https://code4rena.com/reports/2022-05-alchemix
- **GitHub**: https://github.com/code-423n4/2022-05-alchemix-findings/issues/198
- **Contest**: https://code4rena.com/contests/2022-05-alchemix-contest

### Keywords for Search

`vulnerability`

