---
# Core Classification
protocol: Zoro Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61326
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/zoro-protocol/a9a753a4-ad4c-48c1-9d77-527c1951f576/index.html
source_link: https://certificate.quantstamp.com/full/zoro-protocol/a9a753a4-ad4c-48c1-9d77-527c1951f576/index.html
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Shih-Hung Wang
  - Ibrahim Abouzied
  - Hytham Farah
---

## Vulnerability Title

Known Issues in the Compound V2 Protocol

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `5817858d4a26466ebf93e1044da10c7791f5ed36`, `f3e93f55953f41a85e38674486d65b129d76708b`, `f3e93f55953f41a85e38674486d65b129d76708b`, `a6493821126ac10a0f18cb2928410662f455a0b5`, `52ac894c461880ca5773e4bbc1d5d10f417dcadd`, `d4948d06ad7684b5e1eb649bb3538a64b652453e`. The client provided the following explanation:

> Updated the deploy process to ensure that new CTokens are not susceptible to the low liquidity vulnerability. The other risks of Compound V2 forks is considered acceptable protocol behavior.

**File(s) affected:**`contracts/*`

**Description:** The following is a non-exhaustive list of existing or known issues in the Compound V2 codebase:

1.   Empty market vulnerability: An empty market (i.e., cToken with a total supply of 0) is vulnerable to exchange rate manipulation that may lead to loss of funds in other markets managed by the same Comptroller. See [Compound's analysis](https://www.comp.xyz/t/hundred-finance-exploit-and-compound-v2/4266) on the Hundred Finance Incident for more details. This vulnerability can be triggered not only when a market is empty but also when an adversary controls the entire token supply of a market by, e.g., liquidating other users' positions.
2.   Similar to the empty market vulnerability, if the underlying token of a market is compromised, the adversary might be able to drain the funds in other markets by inflating the underlying token balance in the cToken contract (and therefore the return value of `getCash()` and the exchange rate) with a low cost.
3.   Some ERC-20 tokens are incompatible with the Compound V2 codebase and might cause issues when used as an underlying token. For example, tokens with transfer hooks (e.g., ERC-777), double-entry tokens (e.g., TUSD in the past), and tokens allowing balance changes without a transfer (e.g., rebasing tokens).
4.   The `repayBorrowBehalf()` function in the `CEther` and `CErc20` contract allows a user to repay the entire borrow balance of another by specifying the `repayAmount` as `type(uint).max`. This could open an attack vector where the borrower front-runs the repayment transaction and increases the borrow balance, causing the repayer to spend more than expected.
5.   In `CToken.mintFresh()`, the call to `comptroller.mintVerify()` is commented out, and the `comptroller.repayBorrowVerify()` function is never used in the codebase. Therefore, modifications to the `mintVerify()` or `repayBorrowVerify()` functions will not take any effect.
6.   `Comptroller._supportMarket()` calls `isCToken()` on the provided `cToken` parameter but does not validate the return value as `true`. `Comptroller._setPriceOracle()` does not call `isPriceOracle()` on `newOracle` to check that the provided address implements a `PriceOracle`.
7.   The `repayBorrow()`, `repayBorrowBehalf()`, `liquidateBorrow()`, and `mint()` functions in the `CEther` contract do not return a boolean, while the same functions in the `CErc20` contract do. Third-party contracts integrating with the `CEther` contract should be aware of such discrepancies.

**Recommendation:** Consider whether the above-known issues and risks are acceptable. If not, consider implementing code changes or procedures to mitigate the issues. A common mitigation for the empty market vulnerability is to mint a small number of cTokens and burn the tokens or transfer them to a trusted address before setting the collateral factor to non-zero.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Zoro Protocol |
| Report Date | N/A |
| Finders | Shih-Hung Wang, Ibrahim Abouzied, Hytham Farah |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/zoro-protocol/a9a753a4-ad4c-48c1-9d77-527c1951f576/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/zoro-protocol/a9a753a4-ad4c-48c1-9d77-527c1951f576/index.html

### Keywords for Search

`vulnerability`

