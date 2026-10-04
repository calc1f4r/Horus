---
protocol: generic
chain: cosmos
category: access_control
vulnerability_type: authorization_vulnerabilities

attack_type: logical_error|economic_exploit|dos
affected_component: access_control_logic

primitives:
  - missing_control
  - role_assignment
  - antehandler_bypass
  - allowlist_bypass
  - cosmwasm_bypass
  - amino_signing
  - predecessor_misuse
  - owner_privilege
  - msg_sender_validation
  - module_authority

severity: high
impact: fund_loss|dos|state_corruption
exploitability: 0.7
financial_impact: high

tags:
  - cosmos
  - appchain
  - access_control
  - staking
  - defi

language: go|solidity|rust
version: all

# Pattern Identity (Required)
root_cause_family: missing_access_control
pattern_key: missing_access_control | access_control_logic | authorization_vulnerabilities

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: multi_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - AnteHandle
  - Indexers
  - Register
  - RegisterConcrete
  - addValidator
  - allowlist_bypass
  - amino_signing
  - antehandler_bypass
  - balanceOf
  - burnERC20
  - calling
  - closeRebalanceRequests
  - cosmwasm_bypass
  - deposit
  - execute
  - getPriceInEth
  - malicious
  - mint
  - missing_control
  - module_authority
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Access Missing Control
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Front-Running redeem Can Prevent Indexers From Receiving Rew | `reports/cosmos_cometbft_findings/front-running-redeem-can-prevent-indexers-from-receiving-rewards-for-allocations.md` | HIGH | OpenZeppelin |
| [H-01] Lack of access control in `AgentNftV2::addValidator() | `reports/cosmos_cometbft_findings/h-01-lack-of-access-control-in-agentnftv2addvalidator-enables-unauthorized-valid.md` | HIGH | Code4rena |
| [H-02] Arbitrary tokens and data can be bridged to `GnosisTa | `reports/cosmos_cometbft_findings/h-02-arbitrary-tokens-and-data-can-be-bridged-to-gnosistargetdispenserl2-to-mani.md` | HIGH | Code4rena |
| Anyone can overwrite Reputer and Worker info attached to a L | `reports/cosmos_cometbft_findings/h-13-anyone-can-overwrite-reputer-and-worker-info-attached-to-a-libp2pkey.md` | HIGH | Sherlock |
| `LiquidationAccountant.claim()` can be called by anyone caus | `reports/cosmos_cometbft_findings/h-14-liquidationaccountantclaim-can-be-called-by-anyone-causing-vault-insolvency.md` | HIGH | Sherlock |
| Lack of access control in PublicVault.sol#transferWithdrawRe | `reports/cosmos_cometbft_findings/h-26-lack-of-access-control-in-publicvaultsoltransferwithdrawreserve-let-user-ca.md` | HIGH | Sherlock |
| liquidationAccountant can be claimed at any time | `reports/cosmos_cometbft_findings/h-34-liquidationaccountant-can-be-claimed-at-any-time.md` | HIGH | Sherlock |
| _deleteLienPosition can be called by anyone to delete any li | `reports/cosmos_cometbft_findings/h-4-_deletelienposition-can-be-called-by-anyone-to-delete-any-lien-they-wish.md` | HIGH | Sherlock |
| [k1] | reports/cosmos-l1-nodes_findings/audit-reports-astroport-2023-02-14-audit-report-astroport-ibc-v1-0-pdf.md | HIGH | Oak Security | Incorrect permissioning of IbcExecuteProposal execution leads to failure of proposal execution and elevated owner privileges |
| [k2] | reports/cosmos-l1-nodes_findings/audit-reports-astroport-2024-05-22-audit-report-astroport-hub-neutron-migration-v1-0-pdf.md | CRITICAL | Oak Security | Attackers can manipulate the proposal outcome by transferring voting powers |
| [k3] | reports/cosmos-l1-nodes_findings/audit-reports-avail-2026-01-15-audit-report-avail-cosmos-and-backend-changes-v1-0-pdf.md | CRITICAL | Oak Security | Malicious vote extensions can arbitrarily mutate bridge state after late precommit injection |
| [k4] | reports/cosmos-l1-nodes_findings/audit-reports-avail-2026-01-15-audit-report-avail-cosmos-and-backend-changes-v1-0-pdf.md | CRITICAL | Oak Security | ProcessProposal accepts all proposals without validating vote extensions |
| [k5] | reports/cosmos-l1-nodes_findings/audit-reports-avail-2026-01-15-audit-report-avail-cosmos-and-backend-changes-v1-0-pdf.md | HIGH | Oak Security | Fetching vote extension events without timeouts can stall consensus |
| [k6] | reports/cosmos-l1-nodes_findings/audit-reports-avail-2026-01-15-audit-report-avail-cosmos-and-backend-changes-v1-0-pdf.md | HIGH | Oak Security | CreateProtocolFees lacks an authorization check, allowing anyone to set themselves as admin |
| [k7] | reports/cosmos-l1-nodes_findings/audit-reports-axelar-audit-report-axelar-pdf.md | HIGH | Oak Security | Non-unique key for identifying voting topics implementations may lead to lost proposals |
| [k8] | reports/cosmos-l1-nodes_findings/audit-reports-axelar-audit-report-axelar-pdf.md | HIGH | Oak Security | Expired polls can be voted on |
| [k9] | reports/cosmos-l1-nodes_findings/audit-reports-comdex-2022-12-07-audit-report-comdex-v1-0-pdf.md | CRITICAL | Oak Security | Permissionless Rewards module Whitelisting process allows attackers to manipulate the Asset Whitelist and App Vault Whitelist |
| [k10] | reports/cosmos-l1-nodes_findings/audit-reports-comdex-2022-12-07-audit-report-comdex-v1-0-pdf.md | HIGH | Oak Security | HandleUpdateAdminProposal does not properly handle admin update and admin is unchangeable as a result |
| [k11] | reports/cosmos-l1-nodes_findings/audit-reports-comdex-2022-12-07-audit-report-comdex-v1-0-pdf.md | HIGH | Oak Security | Hard-coded admins increase the potential of unauthorized privileged activity |
| [k12] | reports/cosmos-l1-nodes_findings/audit-reports-cosmwasm-2023-10-17-audit-report-wasmd-v1-0-pdf.md | HIGH | Oak Security | Contract admins can bypass code ID instantiation permission when migrating contracts |
| [k13] | reports/cosmos-l1-nodes_findings/audit-reports-croncat-2023-03-14-audit-report-croncat-cosmwasm-v1-0-pdf.md | CRITICAL | Oak Security | Task contract's execute_update_config is permissionless |
| [k14] | reports/cosmos-l1-nodes_findings/audit-reports-injective-2023-01-20-audit-report-injective-v1-0-pdf.md | HIGH | Oak Security | Governance is not able to effectively remove a contract from registry |
| [k15] | reports/cosmos-l1-nodes_findings/audit-reports-interchain-foundation-2022-07-20-audit-report-liquidity-staking-cosmos-sdk-modules-v1-0-pdf.md | HIGH | Oak Security | Withdrawal of tokenized share record rewards is unbounded, owner can be grieved by an attacker |
| [k16] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2022-02-17-audit-report-mars-periphery-v1-0-pdf.md | HIGH | Oak Security | Users are unable to withdraw funds once admin deposited all funds in the Red Bank |
| [k17] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2023-08-01-audit-report-mars-red-bank-updates-v1-0-pdf.md | HIGH | Oak Security | Owner cannot update minimum emission without consequences |
| [k18] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2022-12-07-audit-report-neutron-v1-0-pdf.md | CRITICAL | Oak Security | Proposal's tally returns wrong vote results |
| [k19] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2022-12-07-audit-report-neutron-v1-0-pdf.md | HIGH | Oak Security | Unbounded iteration in EndBlocker when calculating vote power could be used by an attacker to slow down or halt the chain |
| [k20] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2025-03-25-audit-report-neutron-independent-chain-v1-0-pdf.md | HIGH | Oak Security | Validators with significant voting power could censor others to prevent them from receiving rewards |
| [k21] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2026-04-09-audit-report-neutron-auction-and-undelegations-contract-chain-upgrade-phase-2-report-2-pdf.md | CRITICAL | Oak Security | Misconfigured governance module permissions causing consensus-halting panic on deposit burn |
| [k22] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2026-04-09-audit-report-neutron-auction-and-undelegations-contract-chain-upgrade-phase-2-report-2-pdf.md | HIGH | Oak Security | Any CosmWasm contract can add cron schedules, bypassing authorization |
| [k23] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2026-04-09-audit-report-neutron-auction-and-undelegations-contract-chain-upgrade-phase-2-report-2-pdf.md | HIGH | Oak Security | Identical minDeposit and expeditedMinDeposit remove economic distinctions between normal and expedited proposals |
| [k24] | reports/cosmos-l1-nodes_findings/audit-reports-stride-2022-09-26-audit-report-stride-v1-0-pdf.md | HIGH | Oak Security | Hard-coded admins increase the potential of unauthorized privileged activity |
| [k25] | reports/cosmos-l1-nodes_findings/audit-reports-structured-2025-12-24-audit-report-structured-cosmwasm-and-solana-updates-v1-0-pdf.md | HIGH | Oak Security | Permissionless burn enables denom recreation failure and withdrawal DoS |
| [k26] | reports/cosmos-l1-nodes_findings/audit-reports-thorchain-2024-12-16-audit-report-validator-scheduled-standard-cosmos-hard-fork-v1-0-pdf.md | HIGH | Oak Security | Unrestricted proposal creation could lead to Denial of Service |
| [k27] | reports/cosmos-l1-nodes_findings/audit-reports-volta-2024-09-18-audit-report-volta-cosmwasm-v1-0-pdf.md | HIGH | Oak Security | Incorrect vote logic prevents correct proposal processing |
| [k28] | reports/cosmos-l1-nodes_findings/audit-reports-volta-2024-09-18-audit-report-volta-cosmwasm-v1-0-pdf.md | HIGH | Oak Security | Malicious owners or users spamming messages could prevent the admin from executing ProposalType::Configuration proposals |
| [k29] | reports/cosmos-l1-nodes_findings/audits-anoma-2024-02-26-namada-masp-final-report-pdf.md | CRITICAL | Informal Systems | Non-authorized users may render useless an arbitrary number of notes |
| [k30] | reports/cosmos-l1-nodes_findings/audits-anoma-2024-04-30-namada-abci-replay-protection-fee-and-gas-metering-final-report-pdf.md | CRITICAL | Informal Systems | Inconsistent Block Size Limit Handling in Proposal Preparation |
| [k31] | reports/cosmos-l1-nodes_findings/audits-anoma-2024-12-11-namada-governance-pgf-pdf.md | CRITICAL | Informal Systems | Malicious user could prevent honest users from installing valid governance proposals by not increasing the governance counter |
| [k32] | reports/cosmos-l1-nodes_findings/audits-anoma-2024-12-11-namada-governance-pgf-pdf.md | CRITICAL | Informal Systems | A governance proposal may prevent creation of future proposals |
| [k33] | reports/cosmos-l1-nodes_findings/audits-anoma-2024-12-11-namada-governance-pgf-pdf.md | CRITICAL | Informal Systems | Adding an incomplete proposal may cause panic in finalize_block |
| [k34] | reports/cosmos-l1-nodes_findings/audits-anoma-2024-12-11-namada-governance-pgf-pdf.md | CRITICAL | Informal Systems | Proposal type key modification |
| [k35] | reports/cosmos-l1-nodes_findings/audits-anoma-2024-12-11-namada-governance-pgf-pdf.md | CRITICAL | Informal Systems | Proposal funds key modification |
| [k36] | reports/cosmos-l1-nodes_findings/audits-anoma-2024-12-11-namada-governance-pgf-pdf.md | HIGH | Informal Systems | Some checks for governance-vetted updates are justified and beneficial |
| [k37] | reports/cosmos-l1-nodes_findings/audits-neutron-2023-11-05-audit-report-neutron-smart-contracts-overrule-liquidity-migration-pdf.md | MEDIUM | Informal Systems | Overly permissive handling of a pre-proposal error |
| [k38] | reports/cosmos-l1-nodes_findings/celestia-app-docs-audit-informal-systems-v2-pdf.md | HIGH | Informal Systems | Unfair voting result due to non unique version identifier |
| [k39] | reports/cosmos-l1-nodes_findings/cosmos-sdk-docs-audits-group-module-audit-pdf.md | MEDIUM | Zellic | Group admin can manipulate vote outcomes by removing members |
| [k40] | reports/cosmos-l1-nodes_findings/publications-babylon-genesis-chain-zellic-audit-report-pdf.md | CRITICAL | Zellic | Slashed finality provider retaining voting power |
| [k41] | reports/cosmos-l1-nodes_findings/publications-babylon-genesis-chain-zellic-audit-report-pdf.md | CRITICAL | Zellic | Slashed finality provider restoring voting power through pending delegations |
| [k42] | reports/cosmos-l1-nodes_findings/publications-babylon-genesis-chain-zellic-audit-report-pdf.md | MEDIUM | Zellic | Proposal vote extensions' byte limit |
| [k43] | reports/cosmos-l1-nodes_findings/publicreports-cosmos-audits-entangle-blockchain-cosmos-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | END DATE IS NOT CHECKED ON THE PROPOSALS |
| [k44] | reports/cosmos-l1-nodes_findings/publicreports-cosmos-audits-sifchain-sifnode-042-upgrade-security-audit-report-halborn-v1-1-pdf.md | MEDIUM | Halborn | PRIVILEGED ACCOUNT CAN ACCESS PEGGED FUNDS |
| [k45] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-a41-supernova-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | ACCESS CONTROL NOT ENFORCED FOR CREATING PAIRS |
| [k46] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-astroport-fi-amm-protocol-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | PRIVILEGED ADDRESS CAN BE TRANSFERRED WITHOUT CONFIRMATION IN FACTORY |
| [k47] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-astroport-fi-amm-protocol-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | OWNER ADDRESS NOT TRANSFERABLE |
| [k48] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-astroport-fi-astral-assembly-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | LACK OF PROPOSAL SANITIZATION COULD HARM USERS |
| [k49] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-astroport-fi-periphery-contracts-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | PRIVILEGED ADDRESS CAN BE TRANSFERRED WITHOUT CONFIRMATION |
| [k50] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-brokkr-protocol-p1-contracts-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | PRIVILEGED ADDRESS CAN BE TRANSFERRED WITHOUT CONFIRMATION |
| [k51] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-brokkr-protocol-p2-contracts-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | PRIVILEGED ADDRESS CAN BE TRANSFERRED WITHOUT CONFIRMATION |
| [k52] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-brokkr-protocol-p3-contracts-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | PRIVILEGED ADDRESS CAN BE TRANSFERRED WITHOUT CONFIRMATION |
| [k53] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-kryptonite-protocol-cosmwasm-smart-contract-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | NO ACCESS CONTROL IN WITHDRAW FUNCTION |
| [k54] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-kryptonite-protocol-cosmwasm-smart-contract-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | NO ACCESS CONTROL IN REPAYMENT ENTRY POINT |
| [k55] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-nexus-protocol-cosmwasm-smart-contract-security-audit-report-halborn-v1-1-pdf.md | MEDIUM | Halborn | PRIVILEGED ADDRESSES CAN BE TRANSFERRED WITHOUT CONFIRMATION |
| [k56] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-sienna-network-amm-protocol-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | PRIVILEGED ADDRESS CAN BE TRANSFERRED WITHOUT CONFIRMATION |
| [k57] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-sienna-network-rewards-v3-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | INSUFFICIENT ACCESS CONTROL IN MIGRATION FUNCTIONS |
| [k58] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-sienna-network-rewards-v3-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | PRIVILEGED ADDRESS CAN BE TRANSFERRED WITHOUT CONFIRMATION |
| [k59] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-spectrum-protocol-cosmwasm-smart-contract-security-audit-halborn-report-v1-1-pdf.md | MEDIUM | Halborn | PRIVILEGED ADDRESSES CAN BE TRANSFERRED WITHOUT CONFIRMATION |
| [k60] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-valkyrie-protocol-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | COLLUDED STAKERS CAN TRANSFER VKR TOKENS OUTSIDE GOVERNANCE CONTRACT |
| [k61] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-valkyrie-protocol-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | PRIVILEGED ADDRESSES CAN BE TRANSFERRED WITHOUT CONFIRMATION |
| [k62] | reports/cosmos-l1-nodes_findings/audits-anoma-namada-q2-2025-e2e-shielded-transaction-balance-consistency-audit-report-final-pdf.md | MEDIUM | Informal Systems | Inconsistent handling of overflowing transactions between prepare and process proposal |
| [k125] | reports/cosmos-l1-nodes_findings/audits-neutron-2024-03-28-neutron-chain-manager-report-pdf.md | HIGH | auditor | ons for one kind of proposal message, can execute any proposal message (for which it has no permissions) Implementation 3 |
| [q126] | reports/cosmos-l1-nodes_findings/audit-reports-astroport-2023-07-13-audit-report-astroport-concentrated-liquidity-pool-with-injective-orderbook-integration-v1-0-pdf.md | LOW | Oak Security | Incorrect validation of updated administrators may lead to exceeding the MAX_ADMINS limit |
| [q127] | reports/cosmos-l1-nodes_findings/audit-reports-astroport-2023-07-13-audit-report-astroport-concentrated-liquidity-pool-with-injective-orderbook-integration-v1-0-pdf.md | LOW | Oak Security | Inconsistent admin duplicate validation |
| [q128] | reports/cosmos-l1-nodes_findings/audit-reports-osmosis-labs-2023-10-09-audit-report-osmosis-transmuter-v1-0-pdf.md | INFO | Oak Security | Admin transfer procedure can be enhanced |

### Access Role Assignment
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Missing _grantRole for GOVERNANCE_ROLE will prevent calling  | `reports/cosmos_cometbft_findings/missing-_grantrole-for-governance_role-will-prevent-calling-of-onlygovernor-func.md` | HIGH | Spearbit |
| Missing _grantRole for KEEPER_ROLE will prevent calling of c | `reports/cosmos_cometbft_findings/missing-_grantrole-for-keeper_role-will-prevent-calling-of-critical-keeper-funct.md` | HIGH | Spearbit |

### Access Antehandler Bypass
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| AnteHandler Skipped In Non-CheckTx Mode | `reports/cosmos_cometbft_findings/antehandler-skipped-in-non-checktx-mode.md` | HIGH | OtterSec |

### Access Allowlist Bypass
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Staking Before Operator Leads To No swETH Minted | `reports/cosmos_cometbft_findings/staking-before-operator-leads-to-no-sweth-minted.md` | MEDIUM | SigmaPrime |

### Access Cosmwasm Bypass
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Incorrect Access Control via Malicious `CosmWasm` Contract | `reports/cosmos_cometbft_findings/incorrect-access-control-via-malicious-cosmwasm-contract.md` | MEDIUM | Zokyo |

### Access Amino Signing
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [M-04] Incorrect names provided in `RegisterConcrete` calls  | `reports/cosmos_cometbft_findings/m-04-incorrect-names-provided-in-registerconcrete-calls-break-legacyamino-signin.md` | MEDIUM | Code4rena |
| [M-05] Amino legacy signing method broken because of name mi | `reports/cosmos_cometbft_findings/m-05-amino-legacy-signing-method-broken-because-of-name-mismatch.md` | MEDIUM | Code4rena |

### Access Predecessor Misuse
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| USAGE OF SIGNER ACCOUNT ID INSTEAD OF PREDECESSOR ID IN ACCE | `reports/cosmos_cometbft_findings/usage-of-signer-account-id-instead-of-predecessor-id-in-access-control.md` | MEDIUM | Halborn |

### Access Owner Privilege
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| DPoS is vulnerable to signiﬁcant centralization risk | `reports/cosmos_cometbft_findings/dpos-is-vulnerable-to-signiﬁcant-centralization-risk.md` | HIGH | TrailOfBits |
| [H-09] Attackers can force the rewards to be stuck in the co | `reports/cosmos_cometbft_findings/h-09-attackers-can-force-the-rewards-to-be-stuck-in-the-contract-with-malicious-.md` | HIGH | Code4rena |
| Malicious observer can drain Solana bridge by adding failed  | `reports/cosmos_cometbft_findings/h-1-malicious-observer-can-drain-solana-bridge-by-adding-failed-deposit-transact.md` | HIGH | Sherlock |
| [M-02] Admin drains all ERC based user funds using `withdraw | `reports/cosmos_cometbft_findings/m-02-admin-drains-all-erc-based-user-funds-using-withdrawerc20.md` | MEDIUM | Code4rena |
| Malicious or compromised admin of certain LSTs could manipul | `reports/cosmos_cometbft_findings/m-5-malicious-or-compromised-admin-of-certain-lsts-could-manipulate-the-price.md` | MEDIUM | Sherlock |
| Owner is able to withdraw staking token. | `reports/cosmos_cometbft_findings/owner-is-able-to-withdraw-staking-token.md` | HIGH | Zokyo |
| REGISTRY OWNER CAN BE SET AS APPCHAIN OWNER | `reports/cosmos_cometbft_findings/registry-owner-can-be-set-as-appchain-owner.md` | MEDIUM | Halborn |
| REGISTRY OWNER CAN SET ITSELF AS VOTER OPERATOR | `reports/cosmos_cometbft_findings/registry-owner-can-set-itself-as-voter-operator.md` | MEDIUM | Halborn |

### Access Msg Sender Validation
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [M-01] Incorrect Balance Check in Validator Redelegation Pro | `reports/cosmos_cometbft_findings/m-01-incorrect-balance-check-in-validator-redelegation-process-may-block-legitim.md` | MEDIUM | Code4rena |
| Misplaced stake limit validation in stake function of `Locke | `reports/cosmos_cometbft_findings/misplaced-stake-limit-validation-in-stake-function-of-lockedstakingpools-contrac.md` | MEDIUM | Zokyo |

### Access Module Authority
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Strict Token Balance Check in `close_withdrawal_window` Crea | `reports/cosmos_cometbft_findings/strict-token-balance-check-in-close_withdrawal_window-creates-a-denial-of-servic.md` | MEDIUM | Quantstamp |

---

# Authorization Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Authorization Vulnerabilities in Cosmos/AppChain Security Audits**

---

## Table of Contents

1. [Access Missing Control](#1-access-missing-control)
2. [Access Role Assignment](#2-access-role-assignment)
3. [Access Antehandler Bypass](#3-access-antehandler-bypass)
4. [Access Allowlist Bypass](#4-access-allowlist-bypass)
5. [Access Cosmwasm Bypass](#5-access-cosmwasm-bypass)
6. [Access Amino Signing](#6-access-amino-signing)
7. [Access Predecessor Misuse](#7-access-predecessor-misuse)
8. [Access Owner Privilege](#8-access-owner-privilege)
9. [Access Msg Sender Validation](#9-access-msg-sender-validation)
10. [Access Module Authority](#10-access-module-authority)

---

## 1. Access Missing Control [HIGH]

### Overview

Implementation flaw in access missing control logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 17 audit reports with severity distribution: HIGH: 10, MEDIUM: 7.

> **Key Finding**: The `redeem` function in `Escrow.sol` allows Indexers to receive query rewards by submitting a signed Receipt Aggregate Voucher (RAV) and `allocationIDProof`. However, anyone with knowledge of a valid `signedRAV` and `allocationIDProof` can call `redeem` and receive the rewards, regardless of whethe



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of missing_access_control"
- Pattern key: `missing_access_control | access_control_logic | authorization_vulnerabilities`
- Interaction scope: `multi_contract`
- Primary affected component(s): `access_control_logic`
- High-signal code keywords: `AnteHandle`, `Indexers`, `Register`, `RegisterConcrete`, `addValidator`, `allowlist_bypass`, `amino_signing`, `antehandler_bypass`
- Typical sink / impact: `fund_loss|dos|state_corruption`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `called.function -> from.function -> has.function`
- Trust boundary crossed: `callback / external call`
- Shared state or sync assumption: `state consistency across operations`

#### Valid Bug Signals

- Signal 1: State-changing function lacks `onlyOwner`/`onlyRole` modifier
- Signal 2: External function accepts arbitrary address and calls interface methods without registry validation
- Signal 3: Configuration setter is callable by non-owner accounts
- Signal 4: Initialization or migration function is unprotected

#### False Positive Guards

- Not this bug when: Function is `internal`/`private` and only called from access-controlled paths
- Safe if: Function is restricted via `onlyOwner`/`onlyRole`/`require(msg.sender == ...)`
- Requires attacker control of: specific conditions per pattern

### Vulnerability Description

#### Root Cause

Implementation flaw in access missing control logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies access missing control in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to access operations

### Vulnerable Pattern Examples

**Example 1: Front-Running redeem Can Prevent Indexers From Receiving Rewards for Allocations** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/front-running-redeem-can-prevent-indexers-from-receiving-rewards-for-allocations.md`
```
// Vulnerable pattern from The Graph Timeline Aggregation Audit:
The [`redeem`](https://github.com/semiotic-ai/timeline-aggregation-protocol-contracts/blob/d8795c747d44da90f7717b3db9a08698e64a9b2f/src/Escrow.sol#L366) function in `Escrow.sol` enables Indexers to receive query rewards by submitting a signed Receipt Aggregate Voucher (RAV) and `allocationIDProof`. However, anyone who knows the contents of a valid `signedRAV` and `allocationIDProof` can call `redeem` regardless of whether the proof and signed RAV belong to them. This is because `redeem` only che
```

**Example 2: [H-01] Lack of access control in `AgentNftV2::addValidator()` enables unauthoriz** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-01-lack-of-access-control-in-agentnftv2addvalidator-enables-unauthorized-valid.md`
```solidity
// AgentNftV2::mint()
    function mint(
        uint256 virtualId,
        address to,
        string memory newTokenURI,
        address payable theDAO,
        address founder,
        uint8[] memory coreTypes,
        address pool,
        address token
    ) external onlyRole(MINTER_ROLE) returns (uint256) {
        require(virtualId == _nextVirtualId, "Invalid virtualId");
        _nextVirtualId++;
        _mint(to, virtualId);
        _setTokenURI(virtualId, newTokenURI);
        VirtualInfo storage info = virtualInfos[virtualId];
        info.dao = theDAO;
        info.coreTypes = coreTypes;
        info.founder = founder;
        IERC5805 daoToken = GovernorVotes(theDAO).token();
        info.token = token;

VirtualLP storage lp = virtualLPs[virtualId];
        lp.pool = pool;
        lp.veToken = address(daoToken);

_stakingTokenToVirtualId[address(daoToken)] = virtualId;
@>        _addValidator(virtualId, founder);
@>        _initValidatorScore(virtualId, founder);
        return virtualId;
    }
    // AgentNftV2::addValidator()
    // Expected to be called by `AgentVeToken::stake()` function
    function addValidator(uint256 virtualId, address validator) public {
        if (isValidator(virtualId, validator)) {
// ... (truncated)
```

**Example 3: [H-02] Arbitrary tokens and data can be bridged to `GnosisTargetDispenserL2` to ** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-02-arbitrary-tokens-and-data-can-be-bridged-to-gnosistargetdispenserl2-to-mani.md`
```
// Vulnerable pattern from Olas:
The [`GnosisTargetDispenserL2`](https://github.com/code-423n4/2024-05-olas/blob/3ce502ec8b475885b90668e617f3983cea3ae29f/tokenomics/contracts/staking/GnosisTargetDispenserL2.sol) contract receives OLAS tokens and data from L1 to L2 via the Omnibridge, or just data via the AMB. When tokens are bridged, the `onTokenBridged()` callback is invoked on the contract. This callback processes the received tokens and associated data by calling the internal `_receiveMessage()` function.

However, the `onTo
```

**Example 4: Anyone can overwrite Reputer and Worker info attached to a LibP2PKey** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-13-anyone-can-overwrite-reputer-and-worker-info-attached-to-a-libp2pkey.md`
```go
// Registers a new network participant to the network for the first time for worker or reputer
func (ms msgServer) Register(ctx context.Context, msg *types.MsgRegister) (*types.MsgRegisterResponse, error) {
	// ...

	nodeInfo := types.OffchainNode{
		NodeAddress:  msg.Sender,
		LibP2PKey:    msg.LibP2PKey,
		MultiAddress: msg.MultiAddress,
		Owner:        msg.Owner,
		NodeId:       msg.Owner + "|" + msg.LibP2PKey,
	}

	if msg.IsReputer {
		err = ms.k.InsertReputer(ctx, msg.TopicId, msg.Sender, nodeInfo) // @POC: Register node info
		if err != nil {
			return nil, err
		}
	} else {
		//...
	}
}
```

**Example 5: `LiquidationAccountant.claim()` can be called by anyone causing vault insolvency** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-14-liquidationaccountantclaim-can-be-called-by-anyone-causing-vault-insolvency.md`
```
// Vulnerable pattern from Astaria:
Source: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/188
```

**Variant: Access Missing Control - MEDIUM Severity Cases** [MEDIUM]
> Found in 7 reports:
> - `reports/cosmos_cometbft_findings/insufficient-validation-in-avalanchel1middlewareremoveoperator-can-create-perman.md`
> - `reports/cosmos_cometbft_findings/m-04-preventing-balance-updates-by-adding-a-new-validator-in-the-current-block.md`
> - `reports/cosmos_cometbft_findings/m-11-validatorwithdrawalvaultdistributerewards-can-be-called-to-make-operator-sl.md`

**Variant: Access Missing Control in Astaria** [HIGH]
> Protocol-specific variant found in 4 reports:
> - `reports/cosmos_cometbft_findings/h-14-liquidationaccountantclaim-can-be-called-by-anyone-causing-vault-insolvency.md`
> - `reports/cosmos_cometbft_findings/h-26-lack-of-access-control-in-publicvaultsoltransferwithdrawreserve-let-user-ca.md`
> - `reports/cosmos_cometbft_findings/h-34-liquidationaccountant-can-be-claimed-at-any-time.md`

**Variant: Access Missing Control in FrankenDAO** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/m-5-castvote-can-be-called-by-anyone-even-those-without-votes.md`
> - `reports/cosmos_cometbft_findings/m-7-castvote-can-be-called-by-anyone-even-those-without-votes.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in access missing control logic allows exploitation through missing validation, 
func secureAccessMissingControl(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 17 audit reports
- **Severity Distribution**: HIGH: 10, MEDIUM: 7
- **Affected Protocols**: Moonscape, Virtuals Protocol, Astaria, Karak-June, Olas
- **Validation Strength**: Strong (3+ auditors)

---

## 2. Access Role Assignment

### Overview

Implementation flaw in access role assignment logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: HIGH: 2.

> **Key Finding**: This bug report is about a critical issue found in the code for the Infrared protocol. The problem is that the GOVERNANCE_ROLE is not being granted to any privileged address during initialization, which means that certain important functions cannot be called. This affects the functioning of several 

### Vulnerability Description

#### Root Cause

Implementation flaw in access role assignment logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies access role assignment in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to access operations

### Vulnerable Pattern Examples

**Example 1: Missing _grantRole for GOVERNANCE_ROLE will prevent calling of onlyGovernor func** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/missing-_grantrole-for-governance_role-will-prevent-calling-of-onlygovernor-func.md`
```
// Vulnerable pattern from Infrared Contracts:
## Upgrades

**Severity:** Critical Risk  
**Context:** (No context files were provided by the reviewer)  
**Summary:** Missing the granting of role for `GOVERNANCE_ROLE` to any privileged address will prevent calling of onlyGovernor functions including upgrades across InfraredBERA contracts along with Voter and BribeCollector core contracts of Infrared.
```

**Example 2: Missing _grantRole for KEEPER_ROLE will prevent calling of critical Keeper funct** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/missing-_grantrole-for-keeper_role-will-prevent-calling-of-critical-keeper-funct.md`
```
// Vulnerable pattern from Infrared Contracts:
## Severity: High Risk
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in access role assignment logic allows exploitation through missing validation, 
func secureAccessRoleAssignment(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 2 audit reports
- **Severity Distribution**: HIGH: 2
- **Affected Protocols**: Infrared Contracts
- **Validation Strength**: Single auditor

---

## 3. Access Antehandler Bypass

### Overview

Implementation flaw in access antehandler bypass logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: HIGH: 1.

> **Key Finding**: The Cosmos AnteHandlers are used to check the validity of transactions and prevent malicious transactions from being executed. However, some of the validators are skipped when not in CheckTx mode, allowing attackers to insert malformed transactions into block proposals. This can lead to incorrect ex

### Vulnerability Description

#### Root Cause

Implementation flaw in access antehandler bypass logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies access antehandler bypass in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to access operations

### Vulnerable Pattern Examples

**Example 1: AnteHandler Skipped In Non-CheckTx Mode** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/antehandler-skipped-in-non-checktx-mode.md`
```go
// sei-tendermint/internal/mempool/mempool.go
func (fc EVMFeeCheckDecorator) AnteHandle(ctx sdk.Context, tx sdk.Tx, simulate bool, next sdk.AnteHandler) (sdk.Context, error) {
    // Only check fee in CheckTx (similar to normal Sei tx)
    if !ctx.IsCheckTx() || simulate {
        return next(ctx, tx, simulate)
    }
    [...]
    anteCharge := txData.Cost()
    senderEVMAddr := evmtypes.MustGetEVMTransactionMessage(tx).Derived.SenderEVMAddr
    if state.NewDBImpl(ctx, fc.evmKeeper, true).GetBalance(senderEVMAddr).Cmp(anteCharge) < 0 {
        return ctx, sdkerrors.ErrInsufficientFunds
    }
    [...]
}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in access antehandler bypass logic allows exploitation through missing validatio
func secureAccessAntehandlerBypass(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 1 audit reports
- **Severity Distribution**: HIGH: 1
- **Affected Protocols**: Sei EVM
- **Validation Strength**: Single auditor

---

## 4. Access Allowlist Bypass

### Overview

Implementation flaw in access allowlist bypass logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: MEDIUM: 1.

> **Key Finding**: This bug report is about a potential issue with the staking call to a validation node. It is intended for the operator to make the first call and deposit either 1 or 16 ETH (unless they are in the super whitelist). However, there is no validation to check if the first user staking is the operator. T

### Vulnerability Description

#### Root Cause

Implementation flaw in access allowlist bypass logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies access allowlist bypass in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to access operations

### Vulnerable Pattern Examples

**Example 1: Staking Before Operator Leads To No swETH Minted** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/staking-before-operator-leads-to-no-sweth-minted.md`
```
// Vulnerable pattern from Swell:
## Description

The first staking call to a validation node is intended to be done by the operator, in which the operator sends a 1 or 16 ETH deposit (assuming they are not in the super whitelist). However, no validation is done to check if the first user staking is the operator. This means a naive end user, Bob, can stake to a new validation node and their funds will become stuck, misinterpreted as the operator’s deposit.

This is because when an operator makes their initial deposit, it is inte
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in access allowlist bypass logic allows exploitation through missing validation,
func secureAccessAllowlistBypass(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 1 audit reports
- **Severity Distribution**: MEDIUM: 1
- **Affected Protocols**: Swell
- **Validation Strength**: Single auditor

---

## 5. Access Cosmwasm Bypass

### Overview

Implementation flaw in access cosmwasm bypass logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: MEDIUM: 1.

> **Key Finding**: Severity: Medium
Status: Acknowledged
Description: The system has a problem with how it controls access when using a specific type of contract called CosmWasm through a feature called IBC. 
Impact: This could result in unauthorized access to important information, loss of money, or the creation of u

### Vulnerability Description

#### Root Cause

Implementation flaw in access cosmwasm bypass logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies access cosmwasm bypass in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to access operations

### Vulnerable Pattern Examples

**Example 1: Incorrect Access Control via Malicious `CosmWasm` Contract** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/incorrect-access-control-via-malicious-cosmwasm-contract.md`
```
// Vulnerable pattern from Shido:
**Severity**: Medium

**Status**: Acknowledged

**Description**: 

The system is vulnerable to incorrect access control through the deployment and use of a malicious CosmWasm contract via IBC interactions.

**Impact:** 

This could lead to unauthorized access to sensitive data, loss of funds, or unexpected minting of tokens.

**Likelihood:** 

Low to moderate, as it requires the ability to deploy and execute malicious contracts.

**Recommendation**: 

Upgrade github.com/cosmos/ibc-go/v7/modules/
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in access cosmwasm bypass logic allows exploitation through missing validation, 
func secureAccessCosmwasmBypass(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 1 audit reports
- **Severity Distribution**: MEDIUM: 1
- **Affected Protocols**: Shido
- **Validation Strength**: Single auditor

---

## 6. Access Amino Signing

### Overview

Implementation flaw in access amino signing logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: MEDIUM: 2.

> **Key Finding**: The report discusses a bug in the Cosmos SDK v0.50.x upgrade that affects the codec used for Amino JSON serialization. This change has caused inconsistencies between the tags used in the protobuf files and the names registered in the code for various modules, including coinswap, csr, erc20, govshutt

### Vulnerability Description

#### Root Cause

Implementation flaw in access amino signing logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies access amino signing in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to access operations

### Vulnerable Pattern Examples

**Example 1: [M-04] Incorrect names provided in `RegisterConcrete` calls break `LegacyAmino` ** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-04-incorrect-names-provided-in-registerconcrete-calls-break-legacyamino-signin.md`
```
// Vulnerable pattern from Canto:
One of the breaking changes introduced with the Cosmos SDK v0.50.x upgrade is [a change in the codec used for Amino JSON
(de)serialization](https://github.com/cosmos/cosmos-sdk/blob/release/v0.50.x/UPGRADING.md#protobuf). To ensure the
new codec behaves as the abandoned one did, the team added `amino.name` tags to the `message` types defined in the Canto
modules' ".proto" files.

There are however many instances where these tags are inconsistent with the `RegisterConcrete` calls made by the
in-s
```

**Example 2: [M-05] Amino legacy signing method broken because of name mismatch** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-05-amino-legacy-signing-method-broken-because-of-name-mismatch.md`
```go
// This function should be used to register concrete types that will appear in
// interface fields/elements to be encoded/decoded by go-amino.
// Usage:
// `amino.RegisterConcrete(MyStruct1{}, "com.tendermint/MyStruct1", nil)`
func (cdc *Codec) RegisterConcrete(o interface{}, name string, copts *ConcreteOptions) {
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in access amino signing logic allows exploitation through missing validation, in
func secureAccessAminoSigning(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 2 audit reports
- **Severity Distribution**: MEDIUM: 2
- **Affected Protocols**: Canto, Initia
- **Validation Strength**: Single auditor

---

## 7. Access Predecessor Misuse

### Overview

Implementation flaw in access predecessor misuse logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: MEDIUM: 1.

> **Key Finding**: The bug report is about a risky usage of a function called `env::signer_account_id()` in a project called `Octopus Network`. The function is used to check if the caller is the owner of the appchain. However, this can be risky because it can be manipulated by a malicious contract to execute functions

### Vulnerability Description

#### Root Cause

Implementation flaw in access predecessor misuse logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies access predecessor misuse in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to access operations

### Vulnerable Pattern Examples

**Example 1: USAGE OF SIGNER ACCOUNT ID INSTEAD OF PREDECESSOR ID IN ACCESS CONTROL** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/usage-of-signer-account-id-instead-of-predecessor-id-in-access-control.md`
```rust
fn assert_appchain_owner(&self, appchain_id: &AppchainId) {
        let appchain_basedata = self.get_appchain_basedata(appchain_id);
        assert_eq!(
            env::signer_account_id(),
            appchain_basedata.owner().clone(),
            "Function can only be called by appchain owner."
        );
    }
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in access predecessor misuse logic allows exploitation through missing validatio
func secureAccessPredecessorMisuse(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 1 audit reports
- **Severity Distribution**: MEDIUM: 1
- **Affected Protocols**: Octopus Network
- **Validation Strength**: Single auditor

---

## 8. Access Owner Privilege

### Overview

Implementation flaw in access owner privilege logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 11 audit reports with severity distribution: HIGH: 5, MEDIUM: 6.

> **Key Finding**: This bug report discusses a potential issue with VeChain's DPoS system, which could lead to centralization and a concentration of power among a few validators. This is because the validators with the highest stakes have a higher chance of proposing the next block, and can also offer incentives to de

### Vulnerability Description

#### Root Cause

Implementation flaw in access owner privilege logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies access owner privilege in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to access operations

### Vulnerable Pattern Examples

**Example 1: DPoS is vulnerable to signiﬁcant centralization risk** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/dpos-is-vulnerable-to-signiﬁcant-centralization-risk.md`
```
// Vulnerable pattern from Upgrade:
## Diﬃculty: N/A
```

**Example 2: [H-09] Attackers can force the rewards to be stuck in the contract with maliciou** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-09-attackers-can-force-the-rewards-to-be-stuck-in-the-contract-with-malicious-.md`
```
// Vulnerable pattern from MANTRA:
Attackers can fund rewards of LP tokens with tokens created from the `x/tokenfactory` module and abuse the `MsgForceTransfer` message to prevent the contract from successfully distributing rewards. This would also prevent the contract owner from closing the malicious farm. As a result, rewards that are accrued to the users will be stuck in the contract, causing a loss of rewards.

### Proof of Concept

When a user claims pending rewards of their LP tokens, all of their rewards are aggregated tog
```

**Example 3: Malicious observer can drain Solana bridge by adding failed deposit transaction ** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-1-malicious-observer-can-drain-solana-bridge-by-adding-failed-deposit-transact.md`
```
// Vulnerable pattern from ZetaChain Cross-Chain:
Source: https://github.com/sherlock-audit/2025-04-zetachain-cross-chain-judging/issues/58
```

**Example 4: [M-02] Admin drains all ERC based user funds using `withdrawERC20()`** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-02-admin-drains-all-erc-based-user-funds-using-withdrawerc20.md`
```solidity
function burnERC20(
	address _tokenAddress) 
	external {
	require(cudosAccessControls.hasAdminRole(msg.sender), "Recipient is not an admin");
	uint256 totalBalance = IERC20(_tokenAddress).balanceOf(address(0));
	- IERC20(_tokenAddress).safeTransfer(msg.sender , totalBalance);
     +   IERC20(_tokenAddress).safeTransfer(address(0) , totalBalance);
}
```

**Example 5: Malicious or compromised admin of certain LSTs could manipulate the price** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-5-malicious-or-compromised-admin-of-certain-lsts-could-manipulate-the-price.md`
```solidity
File: SwEthEthOracle.sol
26:     function getPriceInEth(address token) external view returns (uint256 price) {
27:         // Prevents incorrect config at root level.
28:         if (token != address(swEth)) revert Errors.InvalidToken(token);
29: 
30:         // Returns in 1e18 precision.
31:         price = swEth.swETHToETHRate();
32:     }
```

**Variant: Access Owner Privilege - MEDIUM Severity Cases** [MEDIUM]
> Found in 6 reports:
> - `reports/cosmos_cometbft_findings/m-02-admin-drains-all-erc-based-user-funds-using-withdrawerc20.md`
> - `reports/cosmos_cometbft_findings/m-5-malicious-or-compromised-admin-of-certain-lsts-could-manipulate-the-price.md`
> - `reports/cosmos_cometbft_findings/registry-owner-can-be-set-as-appchain-owner.md`

**Variant: Access Owner Privilege in Octopus Network** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/registry-owner-can-be-set-as-appchain-owner.md`
> - `reports/cosmos_cometbft_findings/registry-owner-can-set-itself-as-voter-operator.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in access owner privilege logic allows exploitation through missing validation, 
func secureAccessOwnerPrivilege(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 11 audit reports
- **Severity Distribution**: HIGH: 5, MEDIUM: 6
- **Affected Protocols**: Upgrade, Cudos, Octopus Network, ZetaChain Cross-Chain, Radiant Capital
- **Validation Strength**: Strong (3+ auditors)

---

## 9. Access Msg Sender Validation

### Overview

Implementation flaw in access msg sender validation logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: MEDIUM: 2.

> **Key Finding**: The `processValidatorRedelegation` function in the StakingManager contract has an incorrect balance check that could prevent rebalancing operations from being executed. This is because the function checks the wrong balance, causing legitimate rebalancing operations to fail. To fix this, the incorrec

### Vulnerability Description

#### Root Cause

Implementation flaw in access msg sender validation logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies access msg sender validation in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to access operations

### Vulnerable Pattern Examples

**Example 1: [M-01] Incorrect Balance Check in Validator Redelegation Process May Block Legit** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-01-incorrect-balance-check-in-validator-redelegation-process-may-block-legitim.md`
```solidity
function closeRebalanceRequests(
    address stakingManager,
    address[] calldata validators
) external whenNotPaused nonReentrant onlyRole(MANAGER_ROLE) {
    // ...
    uint256 totalAmount = 0;
    for (uint256 i = 0; i < validators.length; ) {
        // ...
        totalAmount += request.amount;
        // ...
    }
    // Trigger redelegation through StakingManager if there's an amount to delegate
    if (totalAmount > 0) {
        IStakingManager(stakingManager).processValidatorRedelegation(totalAmount);
    }
}
```

**Example 2: Misplaced stake limit validation in stake function of `LockedStakingPools` contr** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/misplaced-stake-limit-validation-in-stake-function-of-lockedstakingpools-contrac.md`
```go
if (userStakeIds[poolId][msg.sender].length == 0) {
     if (userStakeIds[poolId][msg.sender].length > 100) revert TooManyStake();
     noUsersStaked[poolId] += 1;
   }
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in access msg sender validation logic allows exploitation through missing valida
func secureAccessMsgSenderValidation(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 2 audit reports
- **Severity Distribution**: MEDIUM: 2
- **Affected Protocols**: Blastoff, Kinetiq
- **Validation Strength**: Moderate (2 auditors)

---

## 10. Access Module Authority

### Overview

Implementation flaw in access module authority logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: MEDIUM: 1.

> **Key Finding**: A bug was found in the `liquid-staking` program. The client has marked it as "Fixed" and provided an explanation. The bug involves a strict balance check that prevents the `window_authority` from closing the ATA if a malicious user transfers a few base tokens directly to the `window_base_token_accou

### Vulnerability Description

#### Root Cause

Implementation flaw in access module authority logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies access module authority in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to access operations

### Vulnerable Pattern Examples

**Example 1: Strict Token Balance Check in `close_withdrawal_window` Creates a Denial of Serv** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/strict-token-balance-check-in-close_withdrawal_window-creates-a-denial-of-servic.md`
```go
require!(
    window_base_token_account.amount == 0,
    StakingError::WindowHasActiveRequests
);
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in access module authority logic allows exploitation through missing validation,
func secureAccessModuleAuthority(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 1 audit reports
- **Severity Distribution**: MEDIUM: 1
- **Affected Protocols**: Exceed Finance Liquid Staking & Early Purchase
- **Validation Strength**: Single auditor

---

## Detection Patterns

### Automated Detection
```
# Access Missing Control
grep -rn 'access|missing|control' --include='*.go' --include='*.sol'
# Access Role Assignment
grep -rn 'access|role|assignment' --include='*.go' --include='*.sol'
# Access Antehandler Bypass
grep -rn 'access|antehandler|bypass' --include='*.go' --include='*.sol'
# Access Allowlist Bypass
grep -rn 'access|allowlist|bypass' --include='*.go' --include='*.sol'
# Access Cosmwasm Bypass
grep -rn 'access|cosmwasm|bypass' --include='*.go' --include='*.sol'
# Access Amino Signing
grep -rn 'access|amino|signing' --include='*.go' --include='*.sol'
# Access Predecessor Misuse
grep -rn 'access|predecessor|misuse' --include='*.go' --include='*.sol'
# Access Owner Privilege
grep -rn 'access|owner|privilege' --include='*.go' --include='*.sol'
# Access Msg Sender Validation
grep -rn 'access|msg|sender|validation' --include='*.go' --include='*.sol'
# Access Module Authority
grep -rn 'access|module|authority' --include='*.go' --include='*.sol'
```

## Keywords

`access`, `access control`, `account`, `accounting`, `adding`, `allocations`, `allowlist`, `amino`, `antehandler`, `appchain`, `arbitrary`, `assignment`, `attackers`, `authority`, `balance`, `because`, `before`, `block`, `break`, `bridge`, `bridged`, `broken`, `bypass`, `calling`, `calls`, `causes`, `centralization`, `check`, `contract`, `control`

### Detection Patterns

#### Code Patterns to Look For
```
- See vulnerable pattern examples above for specific code smells
- Check for missing validation on critical state-changing operations
- Look for assumptions about external component behavior
```

#### Audit Checklist
- [ ] Verify all state-changing functions have appropriate access controls
- [ ] Check for CEI pattern compliance on external calls
- [ ] Validate arithmetic operations for overflow/underflow/precision loss
- [ ] Confirm oracle data freshness and sanity checks

### Keywords for Search

> These keywords enhance vector search retrieval:

`AnteHandle`, `Indexers`, `Register`, `RegisterConcrete`, `access_control`, `addValidator`, `allowlist_bypass`, `amino_signing`, `antehandler_bypass`, `appchain`, `authorization_vulnerabilities`, `balanceOf`, `burnERC20`, `calling`, `closeRebalanceRequests`, `cosmos`, `cosmwasm_bypass`, `defi`, `deposit`, `execute`, `getPriceInEth`, `malicious`, `mint`, `missing_control`, `module_authority`, `msg_sender_validation`, `owner_privilege`, `predecessor_misuse`, `role_assignment`, `staking`
