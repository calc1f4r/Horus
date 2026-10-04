---
# Core Classification
protocol: generic
chain: generic
category: l1
vulnerability_type: l1_access_generic
root_cause_family: see pattern_key

# Pattern Identity
pattern_key: l1-access-generic | l1 access generic | varies by finding | see references

# Interaction Scope
interaction_scope: varies
involved_contracts:
  - l1 access generic

# Attack Vector Details
attack_type: varies
affected_component: l1 access generic

# Technical Primitives
primitives:
  - access
  - accessible
  - account
  - accountid
  - accounts
  - address

# Grep / Hunt-Card Seeds
code_keywords:
  - access
  - accessible
  - account
  - accountid
  - accounts
  - address
  - addresses
  - admin

severity: critical
impact: varies
language: varies
tags:
  - generic
  - l1
  - audit-mined
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [o1] | reports/other-l1_findings/audit-reports-risk-harbor-2022-03-22-audit-report-risk-harbor-v1-0-pdf.md | HIGH | Oak Security | Owner may update default ratio to prevent claims from being made |
| [o2] | reports/other-l1_findings/public-audits-reports-omni-network-sigma-prime-omni-solvernet-security-assessment-report-v2-0-pdf.md | MEDIUM | NCC Group | Possible Theft Of Contract Balance Due T o Lack Of Access Control Asset SolverNetMiddleMan.sol Status Resolved: See Resolution Rating |
| [o3] | reports/other-l1_findings/publications-audit-reports-peckshield-audit-report-aia-bridge-v1-0-pdf.md | MEDIUM | PeckShield | PeckShield Audit Report #: 2023-294 Public 3.4 Trust Issue of Admin Keys • ID: PVE-004 • |
| [o4] | reports/other-l1_findings/publications-audit-reports-peckshield-audit-report-boringdao-1-0-2020-89-pdf.md | CRITICAL | PeckShield | Ownership Takeover • Description: Whether the set owner function is not protected. • Result: Not found • |
| [o5] | reports/other-l1_findings/publications-audit-reports-peckshield-audit-report-coin98staking-v1-0-pdf.md | MEDIUM | PeckShield | Section 3 for details. 11/20 PeckShield Audit Report #: 2021-363 Public 3   Detailed Results 3.1 Trust Issue of Admin Keys • ID: PVE-001 • |
| [o6] | reports/other-l1_findings/publications-audit-reports-peckshield-audit-report-dtravelstaking-v1-0-pdf.md | MEDIUM | PeckShield | Status This issue has been resolved as the team considers it part of the design. 3.2 T rust Issue of Admin Keys • ID: PVE-002 • |
| [o7] | reports/other-l1_findings/publications-audit-reports-peckshield-audit-report-feg-bridge-v1-0-pdf.md | MEDIUM | PeckShield | Status The issue has been fixed by the following commit:32ae91f1. 3.3 Trust Issue of Admin Keys • ID: PVE-003 • |
| [o8] | reports/other-l1_findings/publications-audit-reports-peckshield-audit-report-fegstaking-v1-0-pdf.md | MEDIUM | PeckShield | Status The issue has been fixed by this commit:d56cb0c. 3.6 T rust Issue of Admin Keys • ID: PVE-006 • |
| [o9] | reports/other-l1_findings/publications-audit-reports-peckshield-audit-report-fuelonblast-v1-0-pdf.md | MEDIUM | PeckShield | PeckShield Audit Report #: 2024-102 Public 3.5 T rust Issue Of Admin Keys • ID: PVE-005 • |
| [o10] | reports/other-l1_findings/publications-audit-reports-peckshield-audit-report-luckychipstaking-v1-0-pdf.md | MEDIUM | PeckShield | PeckShield Audit Report #: 2021-386 Public 3.3 T rust Issue of Admin Keys • ID: PVE-003 • |
| [o11] | reports/other-l1_findings/publications-audit-reports-peckshield-audit-report-nearth-masterstaker-v1-0-pdf.md | MEDIUM | PeckShield | The issue has been confirmed by the team. 15/21 PeckShield Audit Report #: 2021-346 Public 3.4 Trust Issue Of Admin Keys • ID: PVE-004 • |
| [o12] | reports/other-l1_findings/publications-audit-reports-peckshield-audit-report-svm-evm-bridge-v1-0-pdf.md | MEDIUM | PeckShield | Status The issue has been confirmed. 3.2 T rust Issue of Admin Keys • ID: PVE-002 • |
| [o13] | reports/other-l1_findings/publications-nimbora-zellic-audit-report-pdf.md | MEDIUM | Zellic | Incorrect role permission in unpause |
| [o14] | reports/other-l1_findings/publications-reviews-2025-04-reserve-solana-dtfs-securityreview-pdf.md | MEDIUM | Trail of Bits | DTF owner key compromise allows manipulation of DAOFeeConfig |
| [o15] | reports/other-l1_findings/publications-reviews-2025-04-reserve-solana-dtfs-securityreview-pdf.md | HIGH | Trail of Bits | Folio owner can rug pull DTF shareholders |
| [o16] | reports/other-l1_findings/publications-reviews-2025-12-near-one-confidential-key-derivation-securityreview-pdf.md | HIGH | Trail of Bits | CKD response handler lacks access controls |
| [o17] | reports/other-l1_findings/publications-reviews-2026-09-cnear-securityreview-pdf.md | HIGH | Trail of Bits | Ownership transfer retains the previous owner's administrative permissions |
| [o18] | reports/other-l1_findings/publications-reviews-2026-09-cnear-securityreview-pdf.md | MEDIUM | Trail of Bits | Frozen or paused accounts can burn their balance via storage_unregister  defeating owner recovery |
| [o19] | reports/other-l1_findings/publicreports-casper-smart-contract-audits-rengo-labs-uniswaap-core-router-casper-smart-contract-security-audit-report-halborn-final-pdf.md | CRITICAL | Halborn | MISSING ACCESS CONTROL AND VULNERABLE LOGICAL DESIGN ALLOWS FOR STEALING TOKENS |
| [o20] | reports/other-l1_findings/publicreports-casper-smart-contract-audits-rengo-labs-uniswaap-core-router-casper-smart-contract-security-audit-report-halborn-final-pdf.md | CRITICAL | Halborn | MISSING ACCESS CONTROL LEADS TO UNAUTHORIZED SETTING TREASURY FEE |
| [o21] | reports/other-l1_findings/publicreports-casper-smart-contract-audits-rengo-labs-uniswaap-core-router-casper-smart-contract-security-audit-report-halborn-final-pdf.md | CRITICAL | Halborn | MISSING ACCESS CONTROL IN SWAP FOR FLASH LOANS |
| [o22] | reports/other-l1_findings/publicreports-cloud-security-moonwell-cloud-security-assesment-report-halborn-final-pdf.md | CRITICAL | Halborn | NETWORK SECURITY - RDS PUBLICLY ACCESSIBLE ENABLED |
| [o23] | reports/other-l1_findings/publicreports-l1-audits-koii-network-k2-l1-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | ANONYMOUS WRITE ACCESS TO TASKS |
| [o24] | reports/other-l1_findings/publicreports-near-smart-contract-audits-aurora-staking-farm-near-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | HAL02 - IMPROPER ROLE-BASED ACCESS CONTROL POLICY |
| [o25] | reports/other-l1_findings/publicreports-near-smart-contract-audits-octopus-network-anchor-near-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | TOKEN PRICE MAINTAINER AS WELL AS RELAYER CAN BE SET TO THE OWNERS ACCOUNTID |
| [o26] | reports/other-l1_findings/publicreports-move-smart-contract-audits-pancakeswap-aptos-dex-move-smart-contract-security-audit-report-halborn-final-pdf.md | CRITICAL | Halborn | FUNCTION TO SET THRESHOLD CAN GET THE MULTISIG WALLETS TOTALLY STUCK |
| [o27] | reports/other-l1_findings/publicreports-node-audits-playground-labs-self-custody-node-security-audit-report-halborn-final-pdf.md | CRITICAL | Halborn | API - AUTHENTICATED INTERNAL USERS CAN CREATE ADMIN USER |
| [o28] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-0x-nodes-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | IMPROPER APPLICATION OF PRINCIPLE OF LEAST PRIVILEGE |
| [o29] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-alluvial-liquid-collective-smart-contract-security-audit-report-halborn-final-update-v2-pdf.md | MEDIUM | Halborn | MALICIOUS OWNER CAN ADD AN OPERATOR WITH SAME ADDRESS |
| [o30] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-alluvial-liquid-collective-smart-contract-security-audit-report-halborn-final-update-v2-pdf.md | MEDIUM | Halborn | SINGLE-STEP OWNERSHIP CHANGE |
| [o31] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-apy-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | PRIVILEGED ADDRESSES CAN BE TRANSFERRED WITHOUT CONFIRMATION |
| [o32] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-bastion-protocol-evm-contracts-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | IMPROPER ROLE-BASED ACCESS CONTROL POLICY |
| [o33] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-bastion-protocol-evm-contracts-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | PRIVILEGED ADDRESS CAN BE TRANSFERRED WITHOUT RECIPIENT'S CONFIRMATION |
| [o34] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-biconomy-gastank-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | MISSING ROLE-BASED ACCESS CONTROL |
| [o35] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-biconomy-liquiditypoolmanager-smart-contract-security-audit-report-halborn-v1-1-pdf.md | HIGH | Halborn | RENOUNCING PAUSER ROLE WHEN CONTRACT IS PAUSED |
| [o36] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-biconomy-transferhandler-smart-contract-security-audit-report-halborn-v1-1-pdf.md | MEDIUM | Halborn | OWNER CAN RENOUNCE OWNERSHIP |
| [o37] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-degis-scprotection-smart-contract-security-audit-report-halborn-pdf.md | MEDIUM | Halborn | OWNER CAN RENOUNCE OWNERSHIP |
| [o38] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-easyfi-farming-smart-contract-security-audit-report-halborn-v1-1-pdf.md | MEDIUM | Halborn | LOCKOUT OWNER ROLE |
| [o39] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-gmbl-computer-gmbl-contracts-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | IMPROPER AUTHORIZATION CHECK IN THE XGMBLS CONVERTTO FUNCTION |
| [o40] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-gmbl-computer-gmbl-contracts-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | LACK OF AUTHORIZATION CHECK IN THE XGMBLS DEALLOCATEFROMUSAGE FUNCTION |
| [o41] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-haqq-social-smart-contract-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | ANONYMOUS ACCESS TO PRIVILEGED FUNCTIONS |
| [o42] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-mochi-smart-contract-security-audit-halborn-v1-1-pdf.md | CRITICAL | Halborn | IMPROPER KEY MANAGEMENT POLICY |
| [o43] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-moonwell-finance-governance-and-timelock-updates-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | OVERPRIVILEGED ROLE ON THE BREAK GLASS GUARDIAN |
| [o44] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-nftfi-bundles-airdrop-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | POSSIBLE LOSS OF OWNERSHIP |
| [o45] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-nftfi-directloanfixedoffer-redeployment-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | POSSIBLE LOSS OF OWNERSHIP |
| [o46] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-oceanprotocol-priority-h2o-system-action-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | AUTHORIZE CAN REMOVE HIMSELF AND ALL OTHER AUTHORIZE ACCOUNT |
| [o47] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-oceanprotocol-priority-h2o-system-action-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | IMPROPER ACCESS CONTROL POLICY |
| [o48] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-pera-finance-smartcontract-halborn-report-v1-1-pdf.md | CRITICAL | Halborn | IMPROPER KEY MANAGEMENT POLICY |
| [o49] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-pera-finance-smartcontract-halborn-report-v1-1-pdf.md | HIGH | Halborn | IMPROPER ROLE-BASED ACCESS CONTROL POLICY |
| [o50] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-planet-finance-smart-contract-security-audit-halborn-v1-1-pdf.md | MEDIUM | Halborn | OWNER CAN RENOUNCE OWNERSHIP |
| [o51] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-polkadex-smartcontract-halborn-report-v1-1-pdf.md | CRITICAL | Halborn | IMPROPER KEY MANAGEMENT POLICY |
| [o52] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-polkadex-smartcontract-halborn-report-v1-1-pdf.md | HIGH | Halborn | IMPROPER ROLE-BASED ACCESS CONTROL POLICY |
| [o53] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-qoda-finance-core-v1-smart-contract-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | UNRESTRICTED ACCESS TO CREATEQUOTE FUNCTION ALLOWS UNAUTHORIZED QUOTE CREATION |
| [o54] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-qoda-finance-core-v1-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | COMPROMISED ADMIN CAN LIQUIDATE USERS |
| [o55] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-seascape-new-staking-saloon-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | ADMIN CAN CHANGE SESSION DETAILS AFTER THE START OF A SESSION |
| [o56] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-seascape-ninja-spin-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | CONTRACT ADMIN CAN REVOKE AND RENOUNCE HIMSELF |
| [o57] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-seascape-riverboat-nft-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | CONTRACT ADMIN CAN REVOKE AND RENOUNCE HIMSELF |
| [o58] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-seascape-riverboat-nft-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | IMPROPER ACCESS CONTROL POLICY |
| [o59] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-stater-lendingdata-smart-contract-audit-report-halborn-v1-1-pdf.md | HIGH | Halborn | OWNER CAN RENOUNCE OWNERSHIP |
| [o60] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-stater-lendingdata-smart-contract-audit-report-halborn-v1-1-pdf.md | HIGH | Halborn | IMPROPER ROLE-BASED ACCESS CONTROL POLICY |
| [o61] | reports/other-l1_findings/publicreports-tezos-smart-contact-audits-tezos-oropocket-smart-contract-final-report-v1-pdf.md | MEDIUM | Halborn | ACCESS CONTROL POLICY |
| [o62] | reports/other-l1_findings/publicreports-web-pentest-seascape-minigames-web-pentest-report-halborn-final-pdf.md | MEDIUM | Halborn | ADMIN PANEL PUBLICLY EXPOSED |
| [o63] | reports/other-l1_findings/publicreports-web-pentest-seascape-nft-marketplace-webapp-pentest-report-halborn-final-pdf.md | MEDIUM | Halborn | HARDCODED PRIVATE KEY IN THE REPOSITORY |
| [q64] | reports/other-l1_findings/audit-reports-asteroid-bridge-2024-06-17-audit-report-asteroid-bridge-v1-0-pdf.md | LOW | Oak Security | Missing validation for public key name identifier |
| [q65] | reports/other-l1_findings/audit-reports-celer-2022-05-14-audit-report-celer-cbridge-flow-v1-0-pdf.md | LOW | Oak Security | Public keys are not validated when updating or resetting signers |
| [q66] | reports/other-l1_findings/audit-reports-celer-2022-05-14-audit-report-celer-cbridge-flow-v1-0-pdf.md | LOW | Oak Security | Duplicate public keys are not removed |
| [q67] | reports/other-l1_findings/audit-reports-incrementfi-audit-report-incrementfi-liquid-staking-pdf.md | LOW | Oak Security | Access nodes are not filtered when approving or setting default node |
| [q68] | reports/other-l1_findings/audit-reports-incrementfi-audit-report-incrementfi-liquid-staking-pdf.md | INFO | Oak Security | Trust dependency on admin keys |
| [q69] | reports/other-l1_findings/audit-reports-incrementfi-audit-report-incrementfi-liquid-staking-pdf.md | INFO | Oak Security | Incorrect event emitted when admin modifies isMigratingPaused configuration |
| [q70] | reports/other-l1_findings/audit-reports-structured-2025-11-25-audit-report-structured-erc20-converter-eth-wrapper-maxbtc-erc20-for-eureka-bridge-v1-0-pdf.md | LOW | Oak Security | The MaxBTCERC20 contract allows for renouncing its ownership |
| [q71] | reports/other-l1_findings/audit-reports-structured-2025-11-25-audit-report-structured-erc20-converter-eth-wrapper-maxbtc-erc20-for-eureka-bridge-v1-0-pdf.md | LOW | Oak Security | Access control flaw in initializer causing ownership and initialization order inconsistency |
| [q72] | reports/other-l1_findings/audit-reports-structured-2025-11-25-audit-report-structured-erc20-converter-eth-wrapper-maxbtc-erc20-for-eureka-bridge-v1-0-pdf.md | INFO | Oak Security | Ownership initialization is performed in the child instead of the base contract initializer |
| [q73] | reports/other-l1_findings/audit-reports-structured-2025-11-25-audit-report-structured-erc20-converter-eth-wrapper-maxbtc-erc20-for-eureka-bridge-v1-0-pdf.md | INFO | Oak Security | Contracts should implement a two-step ownership transfer |
| [q74] | reports/other-l1_findings/audit-reports-structured-2025-11-25-audit-report-structured-erc20-converter-eth-wrapper-maxbtc-erc20-for-eureka-bridge-v1-0-pdf.md | INFO | Oak Security | The current owner proposes a new owner address that is validated and lowercased. 2. The new owner account claims ownership  which applies the configur |
| [q75] | reports/other-l1_findings/optimism-docs-security-reviews-2026-03-policyenginestaking-cantina-pdf.md | INFO | auditor | Spec documentation. Cantina Managed: Fix verified. 3.2.2 Owner transferability conflicts with immutable-owner design intent |
| [q76] | reports/other-l1_findings/optimism-docs-security-reviews-2026-03-policyenginestaking-cantina-pdf.md | INFO | auditor | Cantina Managed: Fix verified. 3.2.7 Consider implementing a two-step ownership transfer pattern |
| [q77] | reports/other-l1_findings/publications-audit-reports-peckshield-audit-report-celer-multibridge-v1-0-pdf.md | LOW | PeckShield | Status This issue has been fixed in the following commit:73001ed. 3.3 (Limited) Trust Of Admin Keys • ID: PVE-003 • |
| [q78] | reports/other-l1_findings/publications-audit-reports-peckshield-audit-report-xterio-staking-v1-0-pdf.md | LOW | PeckShield | Status This issue has been fixed in the following commit:0414d75. 3.2 T rust Issue of Admin Keys • ID: PVE-002 • |
| [q79] | reports/other-l1_findings/publications-reviews-2023-02-solana-token-2022-program-securityreview-pdf.md | LOW | Trail of Bits | Out of bounds access in the get_extension instruction |
| [q80] | reports/other-l1_findings/publications-reviews-2025-11-edera-container-runtime-securityreview-pdf.md | LOW | Trail of Bits | Resource limits can be used to set arbitrary cgroup keys |
| [q81] | reports/other-l1_findings/publications-reviews-2026-01-nearone-nearintentsteesolverregistryandammsolver-securityreview-pdf.md | INFO | Trail of Bits | Lack of two-step process for ownership transfers |
| [q82] | reports/other-l1_findings/publicreports-solana-program-audit-clone-protocol-solana-program-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | ADMINISTRATOR ADDRESS CANNOT BE TRANSFERRED |
| [q83] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-biconomy-forwarder-smart-contract-solidity-audit-report-halborn-final-pdf.md | LOW | Halborn | OWNER CAN RENOUNCE OWNERSHIP |
| [q84] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-bware-labs-staking-protocol-smart-contract-security-audit-report-halborn-final-pdf-pdf.md | LOW | Halborn | NOT ALL ROLES ARE SET UP ON INITIALIZATION |
| [q85] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-egl-eglcontract-smart-contract-security-audit-halborn-v1-1-pdf.md | LOW | Halborn | LACK OF ACCESS CONTROL ON THE MANAGEMENT PARAMETERS |
| [q86] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-egl-genesis-smart-contract-security-audit-halborn-v-1-1-pdf.md | INFO | Halborn | OWNER CAN RENOUNCE OWNERSHIP |
| [q87] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-moonwell-finance-safety-module-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | USE IMMUTABLE KEYWORD FOR GAS OPTIMIZATION |
| [q88] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-mori-finance-mori-protocol-smart-contract-security-assessment-report-halborn-final-pdf.md | LOW | Halborn | ACCESS CONTROL DOES NOT FOLLOW SECURITY BEST PRACTICES |
| [q89] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-sushiswap-miso-smart-contract-report-halborn-v2-pdf.md | INFO | Halborn | MISSING ADDING OPERATOR ROLE AND INTERFACE TO THE DEPLOYED CHILD CONTRACT |
| [q90] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-tidal-finance-smart-contracts-security-audit-halborn-v1-1-pdf.md | LOW | Halborn | MISSING ACCESS CONTROL ON THE TRUSTED FORWARDER FUNCTION |
| [q91] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-tidal-finance-smart-contracts-security-audit-halborn-v1-1-pdf.md | LOW | Halborn | OWNER CAN RENOUNCE OWNERSHIP |
| [q92] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-truffles-nft-invoice-smart-contract-security-assessment-report-halborn-final-pdf.md | LOW | Halborn | LACK OF THE TWO STEP OWNERSHIP TRANSFER PATTERN |
| [q93] | reports/eth-l1-clients_findings/publicauditreports-nm0234-final-ethereum-foundation-holesky-funds-vault-pdf.md | MEDIUM | Nethermind | Certain calls can be forced to revert with an invalid grant (EF Holesky funds vault) |
| [q94] | reports/other-l1_findings/publicauditreports-nm0069-final-polygon-id-pdf.md | LOW | Nethermind | Lack of a two-step process for transferring ownership (PolygonID) |## L1 Access Generic

**l1-access-generic patterns mined from uncited L1 audit reports** - 71 sec-tier findings (11 critical / 15 high / 45 medium) across 56 files from Halborn, NCC Group, Oak Security, PeckShield, Trail of Bits, Zellic.

### Overview

Titles in the references table are verbatim from source reports. Route to the exact report file for full PoC detail. Validation strength: `unassessed` (evidence rows only).

### Detection Patterns

#### High-Signal Grep Seeds
```
- access
- accessible
- account
- accountid
- accounts
- address
- addresses
- admin
```

### Vulnerability Description

#### Root Cause

The cited reports describe l1 access generic paths where a validation, bound, or state-consistency check is missing around attacker-influenced input or an attacker-growable collection. The pattern key for this family is `l1-access-generic | l1 access generic | varies by finding | see references`. Every reference row in the table above is a verbatim finding title from the named auditor; consult that report for the exact code location and exploit path.

#### Attack Scenario / Path Variants

**Path A: [Direct input path]**
Path key: `l1-access-generic | l1 access generic | varies by finding | see references | user/peer message | direct handler`
1. Attacker submits crafted input (message, tx, packet, or config change) accepted by the entry surface.
2. Missing validation lets the input reach state mutation or an unbounded loop.
3. State corruption, fund misaccounting, or resource exhaustion follows.

**Path B: [Growth-then-trigger path]**
Path key: `l1-access-generic | l1 access generic | varies by finding | see references | cheap state growth | later iteration/execution`
1. Attacker cheaply grows a collection (plans, stakes, peers, entries).
2. A later block-time or cleanup path iterates the collection without bounds.
3. Block production exceeds limits or the node exhausts memory (DoS / halt).

### Vulnerable Pattern Examples

**Example 1: Ownership Takeover • Description: Whether the set owner function is not protected. • Result: Not found •** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Ownership Takeover • Description: Whether the set owner function is not protected. • Result: Not found •
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Ownership Takeover • Description: Whether the set owner function is not protected. • Result: Not fou
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 2: MISSING ACCESS CONTROL AND VULNERABLE LOGICAL DESIGN ALLOWS FOR STEALING TOKENS** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// MISSING ACCESS CONTROL AND VULNERABLE LOGICAL DESIGN ALLOWS FOR STEALING TOKENS
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: MISSING ACCESS CONTROL AND VULNERABLE LOGICAL DESIGN ALLOWS FOR STEALING TOKENS
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 3: MISSING ACCESS CONTROL LEADS TO UNAUTHORIZED SETTING TREASURY FEE** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// MISSING ACCESS CONTROL LEADS TO UNAUTHORIZED SETTING TREASURY FEE
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: MISSING ACCESS CONTROL LEADS TO UNAUTHORIZED SETTING TREASURY FEE
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```

### Impact Analysis

#### Technical Impact
- Wrong accounting / reward misallocation / stuck or double-counted funds (fund-loss class rows above)
- State inconsistency after partial failure (see error-handling references)
- Chain halt or node crash from unbounded work (see DoS rows)

#### Business Impact
- User fund loss and withdrawal freezes; validator downtime; consensus/partition risk for client-level bugs.

### Secure Implementation

**Fix 1: [Bound and validate at the entry surface]**
```rust
// ✅ SECURE: explicit bounds + validation before state mutation
fn handler(input: UntrustedInput) -> Result<(), Error> {
    ensure!(input.len() <= T::MaxInput::get(), Error::TooLarge);
    ensure!(is_valid(&input), Error::Invalid);
    state.update_checked(&input)?;
    Ok(())
}
```

**Fix 2: [Aggregate instead of iterate; cap growth]**
```rust
// ✅ SECURE: keep block-time work O(1) and cap attacker growth
fn on_block_end() {
    let aggregate = Aggregates::get();          // maintained incrementally
    distribute(&aggregate);                      // no unbounded iteration
}
fn create_plan(p: Plan) -> Result<(), Error> {
    ensure!(PlansCount::get() < T::MaxPlans::get(), Error::TooManyPlans);
    Ok(())
}
```

### Detection Patterns

#### Contract / Call Graph Signals
```
- Entry surface writes state before validating attacker-controlled fields
- Block-time hooks iterate collections whose size is attacker-influenceable
- Multi-step handlers where a mid-step failure leaves earlier writes committed
- Config setters without role checks or bounds
```

#### Audit Checklist
- [ ] Verify every attacker-reachable input is length/bounds-checked before state writes
- [ ] Verify block-time (end-blocker / on_finalize) iteration is O(1) or capped
- [ ] Verify failure paths roll back partial state mutations
- [ ] Cross-check the cited reports' fix status before re-reporting

### Keywords for Search

`access, accessible, account, accountid, accounts, address, addresses, admin, administrative, administrators`

### Related Vulnerabilities

- Sibling entries under the same category folder
