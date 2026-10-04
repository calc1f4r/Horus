---
# Core Classification
protocol: Popcorn
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 22021
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-01-popcorn
source_link: https://code4rena.com/reports/2023-01-popcorn
github_link: https://github.com/code-423n4/2023-01-popcorn-findings/issues/306

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
  - yield
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - joestakey
  - DadeKuma
  - CRYP70
  - 0xTraub
  - Kumpa
---

## Vulnerability Title

[M-24] Accrued perfomance fee calculation takes wrong assumptions for share decimals, leading to loss of shares or hyperinflation

### Overview


This bug report focuses on two files, `AdapterBase.sol` and `Vault.sol` of the project RedVeil (Popcorn). It is related to the fee calculation which is wrong and leads to either a loss of shares for the fee recipient or hyperinflation which makes users' shares worthless.

The calculation is wrong because it assumes that the total supply is always 1e18, which is not always true because the total supply decimals can be greater or lesser than that. In the best case scenario, the fee calculation will always round to zero, thus the fee recipient will never get the deserved accrued fees. In the worst case scenario, the fee recipient will get a highly disproportionate number of shares, leading to hyperinflation.

To mitigate this issue, the fee calculation should be modified so it is divided with the correct denominator, taking into account the share decimals. RedVeil (Popcorn) has confirmed the issue, but disagreed with the severity. The severity has been decreased to Medium by LSDan (judge).

### Original Finding Content


<https://github.com/code-423n4/2023-01-popcorn/blob/main/src/vault/adapter/abstracts/AdapterBase.sol#L529-L542> 

<https://github.com/code-423n4/2023-01-popcorn/blob/main/src/vault/Vault.sol#L447-L460>

### Vulnerability details

This issue applies to both `AdapterBase.sol` and `Vault.sol`. For the sake of simplicity and brevity, this POC will describe just the former.

### Impact

Fee calculation is wrong and it either takes too few or too many shares than what is supposed to be when calculating the `accruedPerformanceFee` and the shares decimals are not `18`.

The former causes a loss of shares that the `FEE_RECIPIENT` should earn, but the latter causes hyperinflation, which makes users' shares worthless.

### Proof of Concept

`accruedPerformanceFee` doesn't take into consideration the shares' decimals, and it supposes that it's always `1e18`.

This is supposed to be a percentage and it's calculated as the following, rounding down.

```solidity
function accruedPerformanceFee() public view returns (uint256) {
    uint256 highWaterMark_ = highWaterMark;
    uint256 shareValue = convertToAssets(1e18);
    uint256 performanceFee_ = performanceFee;

    return
        performanceFee_ > 0 && shareValue > highWaterMark_
            ? performanceFee_.mulDiv(
                (shareValue - highWaterMark_) * totalSupply(),
                1e36,
                Math.Rounding.Down
            )
            : 0;
}
```

This calculation is wrong because the assumption is:

    totalSupply (1e18) * performanceFee_ (1e18) = 1e36

which is not always true because the `totalSupply` decimals can be greater or lesser than that.

Let's see what would happen in this case.

**Best case scenario: `supply decimals < 1e18`**

In this case, the fee calculation will always round to zero, thus the `FEE_RECIPIENT` will never get the deserved accrued fees.

**Worst case scenario: `supply decimals > 1e18`**

The `FEE_RECIPIENT` will get a highly disproportionate number of shares.

This will lead to share hyperinflation, which will also impact the users, making their shares worthless.

### Recommended Mitigation Steps

Modify the fee calculation so it's divided with the correct denominator, that takes into account the share decimals:

```solidity
performanceFee_ > 0 && shareValue > highWaterMark_
? performanceFee_.mulDiv(
    (shareValue - highWaterMark_) * totalSupply(),
    1e18 * (10 ** decimals()),
    Math.Rounding.Down
)
: 0;
``
```

**[RedVeil (Popcorn) confirmed, but disagreed with severity](https://github.com/code-423n4/2023-01-popcorn-findings/issues/306)** 

**[LSDan (judge) decreased severity to Medium](https://github.com/code-423n4/2023-01-popcorn-findings/issues/306)** 


***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Popcorn |
| Report Date | N/A |
| Finders | joestakey, DadeKuma, CRYP70, 0xTraub, Kumpa |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-popcorn
- **GitHub**: https://github.com/code-423n4/2023-01-popcorn-findings/issues/306
- **Contest**: https://code4rena.com/reports/2023-01-popcorn

### Keywords for Search

`vulnerability`

