---
# Core Classification
protocol: Exceed Finance Liquid Staking & Early Purchase
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58774
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/exceed-finance-liquid-staking-early-purchase/cde4c9ed-dfc2-460f-bc2c-780ce622fff7/index.html
source_link: https://certificate.quantstamp.com/full/exceed-finance-liquid-staking-early-purchase/cde4c9ed-dfc2-460f-bc2c-780ce622fff7/index.html
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
  - István Böhm
  - Mustafa Hasan
  - Darren Jensen
---

## Vulnerability Title

Missing/limited Test Suite in Liquid Staking Program

### Overview


The client has acknowledged that there are 40 tests missing from the Liquid Staking Program, and auditors have recommended reviewing these skipped tests for missing coverage and edge cases. The program currently has limited testing, which puts it at risk for serious bugs that could impact its functionality and security. The recommendation is to create a comprehensive test suite that includes various scenarios, verifies state changes and invariants, and may even include fuzz testing. This will help ensure the program's proper functioning and security.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> We have around 40 tests for the Liquid Staking Program, nearly all of the skipped tests are already included in other unit tests that test the whole user flow of the program.

**NOTE** auditors recommend reviewing all skipped tests for missing coverage and edge cases. For example:

*   There are currently no tests for calling the `unseal_program` function. If the unseal function is broken this could cause serious issues with the protocol.
*   There is only one test scenario for `restake_expired_withdraw`. A test could be added to ensure `InvalidWithdrawalWindow` constraint is properly checked.
*   There is only one test scenario for `accept_authority_transfer`. A test could be added to ensure the `InvalidPendingAuthority` constraint is properly checked.

**Description:** The Liquid Staking program appears to have a very limited test suite - there are several unimplemented tests marked with "-" as can be observed in the Test Suite Results section of this report. Contracts that are not extensively tested are at high risk of serious bugs that can impact the protocol's proper functioning and security. While audits can help developers to find bugs, they are not a substitute for thorough unit and integration testing.

**Recommendation:** A test suite should be created, which:

*   Includes unit tests and integration tests with a mainnet fork
*   Includes a variety of test cases, including:
    *   All "happy path" scenarios
    *   Negative test cases
    *   Unexpected or edge cases
    *   All role permissions and access control for protected functions.

*   Verifies the following through assertions:
    *   All state changes
    *   Invariants
    *   Emission of events

*   May include fuzz testing

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Exceed Finance Liquid Staking & Early Purchase |
| Report Date | N/A |
| Finders | István Böhm, Mustafa Hasan, Darren Jensen |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/exceed-finance-liquid-staking-early-purchase/cde4c9ed-dfc2-460f-bc2c-780ce622fff7/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/exceed-finance-liquid-staking-early-purchase/cde4c9ed-dfc2-460f-bc2c-780ce622fff7/index.html

### Keywords for Search

`vulnerability`

