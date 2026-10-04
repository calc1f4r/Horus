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
solodit_id: 60906
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

`AbstractVault` May Not Have Enough Funds for Lenders to Remove Liquidity

### Overview


The report discusses potential strategies for incentivizing borrowers to repay their loans in the Archi protocol. The first strategy, which involves liquidating positions after one year, is not effective as borrowers can easily reopen the position. The second strategy, setting the reward percentage for borrowers to 0, is more effective but still cannot force borrowers to repay. The team has also introduced a cooldown period for farmers to reopen a position, but this only works if only whitelisted addresses can borrow. The lack of interest rates and high leverage offered by the protocol increases the risk of insolvency. The recommendation is to scale rewards for lenders and fees for borrowers based on available liquidity to maintain solvency.

### Original Finding Content

**Update**
The team has suggested two potential strategies for incentivizing borrowers to pay back their loans. The first is a mechanism implemented within the code to only allow a position to be open for `1` year after which it may be liquidated. However, a borrower may easily close the position and reopen it within the same transaction using a smart contract. So this first mechanism is ineffective at incentivizing the borrowers to repay their loans. However, this may help in cases where borrowers have lost access to their private keys and thus are not capable of repaying. In this case, the liquidation will happen `365` days after the position has been opened.

The second mechanism mentioned by the team would be to set the reward percentage for the borrowers to `0`. This will result in only the lenders receiving rewards from farmed funds. This strategy will be more effective at incentivizing borrowers to repay their loans. However, the borrowers still cannot be forced to repay their loans.

We note that only allowlisted borrowers can open positions, and the protocol team believes they will act in good faith. However, this is based on trust and cannot be guaranteed.

![Image 62: Alert icon](blob:http://localhost/94c75bd51a0d4e9989cbe9929979ce3d)

**Update**
The issue has been further mitigated by introducing a cooldown period such that farmers cannot reopen the position until two days after the position has been closed. We note that this strategy is only effective so long as only whitelisted addresses can be used to borrow. There should be only one whitelisted address per user.

While this issue cannot be entirely fixed due to the nature of the protocol, the Archi team has done everything they can to mitigate the risk without introducing a direct interest rate on the funds borrowed.

**File(s) affected:**`credit/CreditCaller.sol`

**Description:** Farmers pay no interest on their loans in the conventional sense. Rather, a portion of the claimed rewards is simply directed toward the liquidity providers. This means that farmers, so long as they are able to maintain healthy positions, will be incentivized to borrow all liquidity within the vault and never repay it. `AbstractVault` is not guaranteed to have enough funds to return the underlying token to lenders when they call `removeLiquidity()`.

The risk of insolvency is high considering the lack of interest rates and the offering of loans at 10x leverage. Lending protocols such as AAVE incentivize borrowers to repay their loans by raising interest rates based on the liquidity which has been borrowed.

**Recommendation:** The rewards for lenders and fees for borrowers should scale with the available liquidity to incentivize more lenders to enter the protocol and maintain solvency.

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

