---
# Core Classification
protocol: Datachain - ELC for Bridge - Ethereum
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58949
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/datachain-elc-for-bridge-ethereum/254fdabd-0bdb-4969-8716-9bb29562c5d6/index.html
source_link: https://certificate.quantstamp.com/full/datachain-elc-for-bridge-ethereum/254fdabd-0bdb-4969-8716-9bb29562c5d6/index.html
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
  - Jennifer Wu
  - Mustafa Hasan
  - Rabib Islam
---

## Vulnerability Title

Missing Validation for Finalized Header in Light Client

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> > For epochs earlier than DENEB_FORK_EPOCH , execution.blob_gas_used and execution.excess_blob_gas are both 0 . Our light client implementation does not process the full execution header, so we consider this validation unnecessary. For epochs earlier than CAPELLA_FORK_EPOCH , execution is an empty ExecutionPayloadHeader , and execution_branch is an empty ExecutionBranch . In our light client, the execution payload and its proof are mandatory for the update. Therefore, for epochs before capella (i.e., bellatrix), the relayer must construct an update including both `execution` and `execution_branch` and provide it to the light client.

**File(s) affected:**`light-client-verifier\src\updates.rs`

**Description:** The function `is_valid_light_client_finalized_header()` is missing essential validation checks for finalized headers introduced in the Deneb (EIP-4844) and Capella upgrades. These checks ensure that:

*   For epochs earlier than `DENEB_FORK_EPOCH`, `execution.blob_gas_used` and `execution.excess_blob_gas` are both `0`.
*   For epochs earlier than `CAPELLA_FORK_EPOCH`, `execution` is an empty `ExecutionPayloadHeader`, and `execution_branch` is an empty `ExecutionBranch`.

These validations are specified in the [Deneb upgrade to the Sync Protocol](https://github.com/ethereum/consensus-specs/blob/dev/specs/deneb/light-client/sync-protocol.md#modified-is_valid_light_client_header). Without these validations, the function may incorrectly validate headers that are non-compliant with the protocol rules for these upgrades.

**Recommendation:** Add the missing validation checks for Deneb and Capella conditions to ensure finalized headers comply with the protocol's fork-specific rules.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Datachain - ELC for Bridge - Ethereum |
| Report Date | N/A |
| Finders | Jennifer Wu, Mustafa Hasan, Rabib Islam |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/datachain-elc-for-bridge-ethereum/254fdabd-0bdb-4969-8716-9bb29562c5d6/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/datachain-elc-for-bridge-ethereum/254fdabd-0bdb-4969-8716-9bb29562c5d6/index.html

### Keywords for Search

`vulnerability`

