---
# Core Classification
protocol: Hifi Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59631
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/hifi-finance/043e76dd-52dd-49e2-a2fb-619199cab24d/index.html
source_link: https://certificate.quantstamp.com/full/hifi-finance/043e76dd-52dd-49e2-a2fb-619199cab24d/index.html
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
finders_count: 3
finders:
  - Zeeshan Meghji
  - Roman Rohleder
  - Souhail Mssassi
---

## Vulnerability Title

Debt Celing Can Be Exceeded

### Overview


The report discusses a bug found in the `Fintroller` contract, which sets a debt ceiling for every `Bond` added. The `BalanceSheetV2.borrow()` code implies that the total debt is the same as the supply of the corresponding hToken. However, it is possible to surpass the debt ceiling by using the `HToken.depositUnderlying()` function, which mints new hTokens without any checks to ensure that the total supply does not exceed the debt ceiling. The recommendation is to add validation to the `HToken.depositUnderlying()` function to prevent this issue.

### Original Finding Content

**Update**
The Hifi team indicated that the purpose of the debt ceiling is to minimize risk. They have indicated that risk is not increased by minting HTokens in this way, since they are one-to-one with the underlying. From the team:

```
The purpose of the debt ceiling is to mitigate risk, depositing underlying to mint new hTokens does not increase risk because they are minted 1:1.
```

**File(s) affected:**`packages/protocol/contracts/core/fintroller/Fintroller.sol`, `packages/protocol/contracts/core/h-token/HToken.sol`, `packages/protocol/contracts/core/balance-sheet/BalanceSheetV2.sol`

**Description:** The `Fintroller` contract defines a debt `ceiling` for every `Bond` added. The following code within the `BalanceSheetV2.borrow()` implies that the total debt is the supply of the hToken corresponding to the bond:

```
uint256 newTotalSupply = bond.totalSupply() + borrowAmount;
uint256 debtCeiling = fintroller.getDebtCeiling(bond);
if (newTotalSupply > debtCeiling) {
    revert BalanceSheet__DebtCeilingOverflow(newTotalSupply, debtCeiling);
}
```

However, it is possible to increase the supply of the hToken past the debt ceiling by calling the `HToken.depositUnderlying()` function. This function mints new hTokens so long as the equivalent amount of underlying is supplied. There are no checks to ensure that hTokens will not be minted past the debt ceiling.

**Recommendation:** Add validation to the `HToken.depositUnderlying()` function to ensure that the total supply of the hToken remains below the debt ceiling.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Hifi Finance |
| Report Date | N/A |
| Finders | Zeeshan Meghji, Roman Rohleder, Souhail Mssassi |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/hifi-finance/043e76dd-52dd-49e2-a2fb-619199cab24d/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/hifi-finance/043e76dd-52dd-49e2-a2fb-619199cab24d/index.html

### Keywords for Search

`vulnerability`

