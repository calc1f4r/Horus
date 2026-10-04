---
# Core Classification
protocol: Omo_2025-01-25
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53347
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Omo-security-review_2025-01-25.md
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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-17] OmoVault first depositor can inflate share price by donating

### Overview


The bug report warns about a high severity bug in the `OmoVault` smart contract. The bug allows malicious users to inflate the share price by donating assets to their registered account, increasing their account holdings. This is because the function `_convertToShares()` uses the total assets, which includes both vault holdings and account holdings, to determine the share price. The report recommends different approaches, such as creating dead shares, to fix this issue.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Low

## Description

`OmoVault` is vulenarable to the _inflation attack_:
The function `_convertToShares()` determines share price using `totalAssets()`, which includes both `vaultHoldings` and `accountHoldings`. A malicious user can inflate share price by donating assets to their own registered account, increasing their `accountHoldings`.

```solidity
    function totalAssets() public view virtual override returns (uint256) {
        uint256 vaultHoldings = _totalAssets;
        uint256 accountHoldings;

        // Sum up values from all registered accounts
        for (uint256 i = 0; i < accountList.length; i++) {
            address account = accountList[i];
            if (registeredAccounts[account]) {
                IDynamicAccount dynamicAcc = IDynamicAccount(account);
                accountHoldings += dynamicAcc.getPositionValue(address(asset));
            }
        }

        return vaultHoldings + accountHoldings;
    }
```

## Recommendations

Different approaches (like creating dead shares) can be found on this thread: [link](https://github.com/OpenZeppelin/openzeppelin-contracts/issues/3706)

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Omo_2025-01-25 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Omo-security-review_2025-01-25.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

