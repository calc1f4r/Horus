---
# Core Classification
protocol: Altr
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60246
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/altr/b6241933-b256-42d2-bb46-acb54a26e560/index.html
source_link: https://certificate.quantstamp.com/full/altr/b6241933-b256-42d2-bb46-acb54a26e560/index.html
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
  - Roman Rohleder
  - Ruben Koch
  - Mostafa Yassin
---

## Vulnerability Title

Inadequate Test Suite

### Overview


This bug report discusses an issue with the test suite for the `Lending` smart contract. The report notes that the tests currently use hardcoded values to compare the output of the contract, rather than testing for functional correctness. This can lead to incorrect results, as seen in the example of the `testGracePeriod()` test. The report recommends replacing the hardcoded value comparisons with checks that ensure the output falls within an expected range, and suggests adding broader tests to cover different loan durations and fee reduction factors.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `fbdf3d0d12ce61b1dc9b0e0783a59eef280432bb`.

While the tests still perform equality checks with magic value constants, the reasoning of these values is now very well documented, as well as now being accompanied by calculations of how these values were derived.

**File(s) affected:**`Lending.sol`

**Description:**[ALT-1](https://certificate.quantstamp.com/full/altr/b6241933-b256-42d2-bb46-acb54a26e560/index.html#findings-qs1) highlighted that the current test suite is inadequately testing the outputs of functions from the smart contract. With closer inspection, rather than testing the functional correctness, most of the tests seem to have been built with the smart contract output in mind, as e.g. they simply compare the smart contract result with hardcoded values.

The test `testGracePeriod()` in `Lending.t.sol` for example can be seen to consider a loan repayment within the grace period with over 300% interest rate as valid, as the `repayGraceFee` is set to `25000`, being interpreted as 250%.

Overall, we deemed the test suite to be slightly minimalistic around some of the features of the protocol too, such as multiple possible loan durations and the application of the fee reduction factor.

**Recommendation:** In the test suite, replace the hardcoded value comparisons with checks that assure that the value lies in an expected range. For example, replace the checks around the borrower's balance changes after a repaid loan is equal to some hardcoded value with a check that assures that the balance change falls in an expected range. ("The borrower paid roughly 11% total for the 10% loan with the 1% percent protocol fee"). These comparison-values should be derived from perhaps simplified math resembling the on-chain calculations.

Furthermore, consider adding broader tests, e.g. around different loan durations with differing APRs and loans that are large enough that the origination fee is reduced multiple times by the `feeReductionFactor`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Altr |
| Report Date | N/A |
| Finders | Roman Rohleder, Ruben Koch, Mostafa Yassin |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/altr/b6241933-b256-42d2-bb46-acb54a26e560/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/altr/b6241933-b256-42d2-bb46-acb54a26e560/index.html

### Keywords for Search

`vulnerability`

