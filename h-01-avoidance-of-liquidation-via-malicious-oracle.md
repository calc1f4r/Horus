---
# Core Classification
protocol: Abracadabra Money
chain: everychain
category: oracle
vulnerability_type: oracle

# Attack Vector Details
attack_type: oracle
affected_component: oracle

# Source Information
source: solodit
solodit_id: 2126
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-04-abranft-contest
source_link: https://code4rena.com/reports/2022-04-abranft
github_link: https://github.com/code-423n4/2022-04-abranft-findings/issues/136

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.60
financial_impact: high

# Scoring
quality_score: 3
rarity_score: 1

# Context Tags
tags:
  - oracle

protocol_categories:
  - oracle
  - dexes
  - cdp
  - services
  - synthetics

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - hyh
  - BowTiedWardens
  - gzeon
---

## Vulnerability Title

[H-01] Avoidance of Liquidation Via Malicious Oracle

### Overview


This bug report is about an issue in the code of the NFTPairWithOracle.sol contract. The issue is that when a borrower requests a loan, there is no check that the lender agrees to the used oracle, which means that a borrower can request a loan with a malicious oracle and avoid legitimate liquidation. This can be proven through a proof of concept, where the borrower requests a loan with a malicious oracle, the lender unknowingly accepts the loan, and the bad oracle is set to never return a liquidating rate on the oracle.get call. To liquidate the NFT, the lender would have to whitehat by atomically updating to an honest oracle and calling removeCollateral. There are two proposed mitigations to this issue. The first is to add a condition that requires that the oracle used must be the accepted oracle in the _lend function. The second is to consider only allowing whitelisted oracles, to avoid injection of malicious oracles at the initial loan request stage.

### Original Finding Content

_Submitted by BowTiedWardens, also found by gzeon, and hyh_

Issue: Arbitrary oracles are permitted on construction of loans, and there is no check that the lender agrees to the used oracle.

Consequences: A borrower who requests a loan with a malicious oracle can avoid legitimate liquidation.

### Proof of Concept

*   Borrower requests loan with an malicious oracle
*   Lender accepts loan unknowingly
*   Borrowers's bad oracle is set to never return a liquidating rate on `oracle.get` call.
*   Lender cannot call `removeCollateral` to liquidate the NFT when it should be allowed, as it will fail the check on [L288](https://github.com/code-423n4/2022-04-abranft/blob/5cd4edc3298c05748e952f8a8c93e42f930a78c2/contracts/NFTPairWithOracle.sol#L288)
*   To liquidate the NFT, the lender would have to whitehat along the lines of H-01, by atomically updating to an honest oracle and calling `removeCollateral`.

### Mitigations

*   Add `require(params.oracle == accepted.oracle)` as a condition in `_lend`
*   Consider only allowing whitelisted oracles, to avoid injection of malicious oracles at the initial loan request stage

**[cryptolyndon (AbraNFT) confirmed and commented](https://github.com/code-423n4/2022-04-abranft-findings/issues/136#issuecomment-1119136462):**
 > Oracle not compared to lender agreed value: confirmed, and I think this is the first time I've seen this particular vulnerability pointed out. Not marking the entire issue as a duplicate for that reason.
> 
> Oracle not checked on loan request: Not an issue, first reported in #62.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 3/5 |
| Rarity Score | 1/5 |
| Audit Firm | Code4rena |
| Protocol | Abracadabra Money |
| Report Date | N/A |
| Finders | hyh, BowTiedWardens, gzeon |

### Source Links

- **Source**: https://code4rena.com/reports/2022-04-abranft
- **GitHub**: https://github.com/code-423n4/2022-04-abranft-findings/issues/136
- **Contest**: https://code4rena.com/contests/2022-04-abranft-contest

### Keywords for Search

`Oracle`

