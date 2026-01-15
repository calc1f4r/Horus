---
# Core Classification
protocol: Archi Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60908
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/archi-finance/abb48b19-672a-4390-bf11-59c485978d61/index.html
source_link: https://certificate.quantstamp.com/full/archi-finance/abb48b19-672a-4390-bf11-59c485978d61/index.html
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Mustafa Hasan
  - Zeeshan Meghji
  - Ibrahim Abouzied
  - Hytham Farah
---

## Vulnerability Title

Credit Tokens Burned From the Wrong Account

### Overview


The team has fixed an issue where credit tokens were not being properly burned when a farmer closed their position. They introduced a new contract, called `CreditTokenStaker`, to handle the minting and burning of credit tokens. They also made an adjustment to the `withdrawFor()` function in the `CollateralReward` contract. The bug was caused by credit tokens being burned in the `CreditCaller` contract instead of being transferred to the farmer. The recommendation is to fix this by burning the credit tokens transferred to the user, not the ones already existing in `CreditCaller`.

### Original Finding Content

**Update**
The team has fixed the issue by introducing the `CreditTokenStaker` contract, which will handle the minting and burning of credit tokens to the correct amount. A corresponding adjustment in the `withdrawFor()` function has also been made in the `CollateralReward` contract.

**File(s) affected:**`credit/CreditCaller.sol`

**Description:** Whenever a farmer opens a position, credit tokens are minted and staked in a rewards contract on their behalf, as shown below:

```
_mintTokenAndApprove(strategy.collateralReward, _collateralMintedAmount);

IAbstractReward(strategy.collateralReward).stakeFor(_recipient, _collateralMintedAmount);
```

When the farmer closes the position through the `repayCredit()` function, these credit tokens are withdrawn from the rewards contract and sent to the farmer. However, rather than burning the tokens which were sent to the farmer, tokens within `CreditCaller` are burned:

```
IAbstractReward(strategy.collateralReward).withdrawFor(_recipient, userBorrowed.collateralMintedAmount);
ICreditToken(creditToken).burn(address(this), userBorrowed.collateralMintedAmount);
```

**Recommendation:** Burn the credit tokens transferred to the user, not credit tokens already existing in `CreditCaller`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Archi Finance |
| Report Date | N/A |
| Finders | Mustafa Hasan, Zeeshan Meghji, Ibrahim Abouzied, Hytham Farah |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/archi-finance/abb48b19-672a-4390-bf11-59c485978d61/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/archi-finance/abb48b19-672a-4390-bf11-59c485978d61/index.html

### Keywords for Search

`vulnerability`

