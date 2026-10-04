---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25843
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-01-astaria
source_link: https://code4rena.com/reports/2023-01-astaria
github_link: https://github.com/code-423n4/2023-01-astaria-findings/issues/133

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
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - rvierdiiev
---

## Vulnerability Title

[M-27] Approved operator of collateral owner can't liquidate lien

### Overview


The bug report is about the `canLiquidate` function in the AstariaRouter.sol code. This function is used to check if it is possible to liquidate a lien. The code shows that the owner of the collateral token can liquidate the lien in any moment. However, approved operators of the owner cannot do this, even though they should be able to. This is because while validating a commitment, it is allowed for the approved operators to request a loan. This means that the owner of the collateral token can approve some operators to work with their debts, so they should also be able to liquidate the loan. The recommended mitigation steps for this bug are to add the ability for approved operators to liquidate lien. SantiagoGregory (Astaria) has confirmed this bug.

### Original Finding Content


If someone wants to liquidate lien then `canLiquidate` function [is called](https://github.com/code-423n4/2023-01-astaria/blob/main/src/AstariaRouter.sol#L625-L627) to check if it's possible.

<https://github.com/code-423n4/2023-01-astaria/blob/main/src/AstariaRouter.sol#L611-L619>

```soldiity
  function canLiquidate(ILienToken.Stack memory stack)
    public
    view
    returns (bool)
  {
    RouterStorage storage s = _loadRouterSlot();
    return (stack.point.end <= block.timestamp ||
      msg.sender == s.COLLATERAL_TOKEN.ownerOf(stack.lien.collateralId));
  }
```

As you can see owner of collateral token can liquidate lien in any moment.<br>
However approved operators of owner can't do that, however they should.

As while validating commitment it's allowed for approved operator [to request a loan](https://github.com/code-423n4/2023-01-astaria/blob/main/src/VaultImplementation.sol#L237-L244).

That means that owner of collateral token can approve some operators to allow them to work with their debts.

So they should be able to liquidate loan as well.

### Tools Used

VsCode

### Recommended Mitigation Steps

Add ability for approved operators to liqiudate lien.

**[SantiagoGregory (Astaria) confirmed](https://github.com/code-423n4/2023-01-astaria-findings/issues/133)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | rvierdiiev |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-astaria
- **GitHub**: https://github.com/code-423n4/2023-01-astaria-findings/issues/133
- **Contest**: https://code4rena.com/reports/2023-01-astaria

### Keywords for Search

`vulnerability`

