---
# Core Classification
protocol: Polygon zkEVM
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21371
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/PolygonzkEVM-Protocol/zkEVM-engagement-2-Spearbit-27-March.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/PolygonzkEVM-Protocol/zkEVM-engagement-2-Spearbit-27-March.pdf
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
finders_count: 8
finders:
  - Thibaut Schaeffer
  - Alex Beregszaszi
  - Blockdev
  - Lucas Vella
  - Paweł Bylica
---

## Vulnerability Title

SENDALL zeroes out balance in case receiver equals sender

### Overview


This bug report concerns the SENDALL implementation in zkevm-rom:create-terminate-context.zkasm#L1040. It states that when running SENDALL with the receiver being the same as the executing contract, the sender’s balance is zeroed out without ever checking whether they are the same address. This is not intended behavior, as evidenced by the tests. 

To conﬁrm, the team ran ethereum/tests#1024, requiring a number of changes. These included disabling skipping SELFDESTRUCT tests in the test infrastructure, modifying go-ethereum to activate SENDALL in Berlin, fixing a bug in the gas charge in go-ethereum implementation, and modifying the tests to be run on Berlin. The outcome is that the sendallBasic passes and sendallToSelf fails at generating inputs. 

The recommendation is to not update the balance in the case that the receiver is the same as the executing contract. Polygon-Hermez has fixed the issue in PR #236, added the provided test to run automatically on each ROM change in PR #172, and modified ethereumjs-monorepo to handle sendall to itself properly. Spearbit has acknowledged the issue.

### Original Finding Content

## Severity: Critical Risk

**Context:** `zkevm-rom:create-terminate-context.zkasm#L1040`

**Description:** The `SENDALL` implementation updates the receiver’s balance, then zeroes out the sender’s balance without ever checking whether they are the same address. Running `SENDALL` with the receiver being the same as the executing contract results in balance 0.

As noted in the Ethereum Test Suite, testing of `SENDALL` is not covered. To confirm, we ran `ethereum/tests#1024`, which required a number of changes:

- Disabling skipping `SELFDESTRUCT` tests in test infrastructure at `zkevm-testvectors:gen-inputs.js#L406`
- Modifying go-ethereum to activate `SENDALL` in Berlin
- Fixing a bug in gas charge in go-ethereum implementation (find modified version at internal repository)
- Modifying the tests to be run on Berlin (find modified version at internal repository)

**Outcome** is that `sendallBasic` passes and `sendallToSelf` fails at generating inputs:

**Test name:** `sendallToSelf.json`

```
AssertionError: expected '0' to equal '1000000000000000000 '
    at Context.<anonymous> (/0xPolygonHermez/zkevm-testvectors/tools/ethereum-tests/gen-inputs.js:452:92)
    at process.processTicksAndRejections (node:internal/process/task_queues:95:5) {
    showDiff: true,
    actual: '0',
    expected: '1000000000000000000 ',
    operator: 'strictEqual '
}
```

While `SELFDESTRUCT` uses this edge case for "burning" Ether, the `SENDALL` proposals seem to not want this edge case, as evidenced by the tests.

**Recommendation:** Do not update balance in case the receiver is the same as the executing contract.

## Polygon-Hermez:

- Fixed in PR #236.
- Added provided test to run automatically on each ROM change in PR #172.
- Modified `ethereumjs-monorepo` to handle `sendall` to itself properly.

## Spearbit: Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Polygon zkEVM |
| Report Date | N/A |
| Finders | Thibaut Schaeffer, Alex Beregszaszi, Blockdev, Lucas Vella, Paweł Bylica, Christian Reitwiessner, Andrei Maiboroda, Leo Alt |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/PolygonzkEVM-Protocol/zkEVM-engagement-2-Spearbit-27-March.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/PolygonzkEVM-Protocol/zkEVM-engagement-2-Spearbit-27-March.pdf

### Keywords for Search

`vulnerability`

