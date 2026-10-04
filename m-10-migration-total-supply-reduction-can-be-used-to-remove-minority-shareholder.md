---
# Core Classification
protocol: Fractional
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3011
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-07-fractional-v2-contest
source_link: https://code4rena.com/reports/2022-07-fractional
github_link: https://github.com/code-423n4/2022-07-fractional-findings/issues/612

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
  - bridge
  - yield
  - launchpad
  - synthetics

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Lambda  Treasure-Seeker
  - hyh
---

## Vulnerability Title

[M-10] Migration total supply reduction can be used to remove minority shareholders

### Overview


This bug report is regarding the code in the Migration.sol file of the 2022-07-fractional repository on GitHub. The code is used to migrate fractions of a vault. The vulnerability is that if the new total supply is set significantly lower than the current one, minority shareholders can lose their shares due to precision loss. This can go unnoticed as the effect is implementation based.

The code calculates new shares to be transferred for a user as a fraction of their contribution. If a minority shareholder does not pay attention to the total supply reduction, their share can be lost on commit(). This is because the leave() and withdrawContribution() functions require the INACTIVE state for a user to withdraw their contribution.

The recommended mitigation step is to require that the new total supply should be greater than the old one. This can be done by adding the require statement to the code.

### Original Finding Content

_Submitted by hyh, also found by Lambda and Treasure-Seeker_

<https://github.com/code-423n4/2022-07-fractional/blob/8f2697ae727c60c93ea47276f8fa128369abfe51/src/modules/Migration.sol#L469-L472>

<https://github.com/code-423n4/2022-07-fractional/blob/8f2697ae727c60c93ea47276f8fa128369abfe51/src/modules/Migration.sol#L95-L98>

### Vulnerability Details

As new total supply can be arbitrary, setting it significantly lower than current (say to 100 when it was 1e9 before) can be used to remove current minority shareholders, whose shares will end up being zero on a precision loss due to low new total supply value. This can go unnoticed as the effect is implementation based.

During Buyout the remaining shareholders are left with ETH funds based valuation and can sell the shares, but the minority shareholders that did contributed to the Migration, that could have other details favourable to them, may not realize that new shares will be calculated with the numerical truncation as a result of the new total supply introduction.

Setting the severity to Medium as this is a fund loss impact conditional on a user not understanding the particulars of the implementation.

### Proof of Concept

Currently `migrateFractions()` calculates new shares to be transferred for a user as a fraction of her contribution:

<https://github.com/code-423n4/2022-07-fractional/blob/8f2697ae727c60c93ea47276f8fa128369abfe51/src/modules/Migration.sol#L469-L472>

```solidity
        // Calculates share amount of fractions for the new vault based on the new total supply
        uint256 newTotalSupply = IVaultRegistry(registry).totalSupply(newVault);
        uint256 shareAmount = (balanceContributedInEth * newTotalSupply) /
            totalInEth;
```

If Bob the msg.sender is a minority shareholder who contributed to Migration with say some technical enhancements of the Vault, not paying attention to the total supply reduction, his share can be lost on `commit()`:

<https://github.com/code-423n4/2022-07-fractional/blob/8f2697ae727c60c93ea47276f8fa128369abfe51/src/modules/Migration.sol#L209-L210>

```solidity
            // Starts the buyout process
            IBuyout(buyout).start{value: proposal.totalEth}(_vault);
```

As `commit()` starts the Buyout, Bob will not be able to withdraw as both `leave()` and `withdrawContribution()` require INACTIVE state:

<https://github.com/code-423n4/2022-07-fractional/blob/8f2697ae727c60c93ea47276f8fa128369abfe51/src/modules/Migration.sol#L149-L150>

```solidity
        State required = State.INACTIVE;
        if (current != required) revert IBuyout.InvalidState(required, current);
```

If Buyout be successful, Bob's share can be calculated as zero given his small initial share and reduction in the Vault total shares.

For example, if Bob's share together with the ETH funds he provided to Migration were cumulatively less than 1%, and new total supply is 100, he will lose all his contribution on `commit()` as `migrateFractions()` will send him nothing.

### Recommended Mitigation Steps

Consider requiring that the new total supply should be greater than the old one:

<https://github.com/code-423n4/2022-07-fractional/blob/8f2697ae727c60c93ea47276f8fa128369abfe51/src/modules/Migration.sol#L95-L98>

```solidity
        proposal.oldFractionSupply = IVaultRegistry(registry).totalSupply(
            _vault
        );
        proposal.newFractionSupply = _newFractionSupply;
+       require(proposal.newFractionSupply > proposal.oldFractionSupply, ""); // reference version
```

**[stevennevins (Fractional) confirmed](https://github.com/code-423n4/2022-07-fractional-findings/issues/612)** 


**[HardlyDifficult (judge) commented](https://github.com/code-423n4/2022-07-fractional-findings/issues/612#issuecomment-1214463275):**
 > A migration that changes the supply can result in some users losing their expected share of funds. I agree with Medium risk here since the terms are known and the community could aim to reject the migration if they don't agree with these changes.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Fractional |
| Report Date | N/A |
| Finders | Lambda  Treasure-Seeker, hyh |

### Source Links

- **Source**: https://code4rena.com/reports/2022-07-fractional
- **GitHub**: https://github.com/code-423n4/2022-07-fractional-findings/issues/612
- **Contest**: https://code4rena.com/contests/2022-07-fractional-v2-contest

### Keywords for Search

`vulnerability`

