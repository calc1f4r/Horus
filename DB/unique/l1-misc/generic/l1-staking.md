---
# Core Classification
protocol: generic
chain: generic
category: l1
vulnerability_type: l1_staking_generic
root_cause_family: see pattern_key

# Pattern Identity
pattern_key: l1-staking-generic | l1 staking generic | varies by finding | see references

# Interaction Scope
interaction_scope: varies
involved_contracts:
  - l1 staking generic

# Attack Vector Details
attack_type: varies
affected_component: l1 staking generic

# Technical Primitives
primitives:
  - aavestrategy
  - able
  - accounted
  - accounts
  - actions
  - admin

# Grep / Hunt-Card Seeds
code_keywords:
  - aavestrategy
  - able
  - accounted
  - accounts
  - actions
  - admin
  - after
  - allocations

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
| [o1] | reports/other-l1_findings/audit-reports-milkyway-2023-12-12-audit-report-milkyway-staking-v1-0-pdf.md | HIGH | Oak Security | Users potentially withdraw incorrect token amounts if the received unstaked tokens are accounted for in the wrong batch |
| [o2] | reports/other-l1_findings/audit-reports-milkyway-2025-05-15-audit-report-milkyway-staking-updates-v1-0-pdf.md | HIGH | Oak Security | Division by zero and incorrect redemption and purchase rates when no liquid stake token in the protocol may lead to transaction failures and loss of f |
| [o3] | reports/other-l1_findings/public-audits-reports-recall-sigma-prime-recall-staking-security-assessment-report-v2-0-pdf.md | HIGH | NCC Group | RSC-01 Bypassing Stake Ownership Checks In unlockedAll Mode Allows Lock Of Funds Asset Staking.sol Status Resolved: See Resolution Rating |
| [o4] | reports/other-l1_findings/public-audits-reports-recall-sigma-prime-recall-staking-security-assessment-report-v2-0-pdf.md | HIGH | NCC Group | Staking Contract Detailed Findings RSC-02 Withdrawal Bypasses Unstaking And Cooldown Asset Staking.sol Status Resolved: See Resolution Rating |
| [o5] | reports/other-l1_findings/public-audits-reports-sushi-bentobox-strategies-staking-contract-review-pdf.md | CRITICAL | NCC Group | Detailed Findings SSBS-01 Reentrancy Vulnerability Allows Draining All Funds Asset StakingContractMainnet.sol Status Resolved: Rating |
| [o6] | reports/other-l1_findings/public-audits-reports-sushi-bentobox-strategies-staking-contract-review-pdf.md | CRITICAL | NCC Group | SSBS-02 Missing Input Validation Allows Subscribing to Non-Existent Incentives Asset StakingContractMainnet.sol Status Resolved: Rating |
| [o7] | reports/other-l1_findings/public-audits-reports-sushi-bentobox-strategies-staking-contract-review-pdf.md | HIGH | NCC Group | Contract Detailed Findings SSBS-03 startTime Incentive Restrictions Can be Bypassed Asset StakingContractMainnet.sol Status Resolved: Rating |
| [o8] | reports/other-l1_findings/public-audits-reports-sushi-bentobox-strategies-staking-contract-review-pdf.md | HIGH | NCC Group | Staking Contract Detailed Findings SSBS-05 Non-standard ERC20 T okens are Not Supported Asset AaveStrategy.sol Status Open Rating |
| [o9] | reports/other-l1_findings/publications-audit-reports-peckshield-audit-report-coin98staking-v1-0-pdf.md | MEDIUM | PeckShield | Status This issue have been fixed as suggested. 3.5 Potential Less Profit From Permissionless unstake() • ID: PVE-005 • |
| [o10] | reports/other-l1_findings/publications-audit-reports-peckshield-audit-report-fegstaking-v1-0-pdf.md | MEDIUM | PeckShield | PeckShield Audit Report #: 2023-154 Public 3   Detailed Results 3.1 Revisited Staking Logic in StakingInterface::stake() • ID: PVE-001 • |
| [o11] | reports/other-l1_findings/publications-audit-reports-peckshield-audit-report-fegstaking-v1-0-pdf.md | MEDIUM | PeckShield | Improper Withdrawal Logic In StakingLogic • ID: PVE-003 • |
| [o12] | reports/other-l1_findings/publications-audit-reports-peckshield-audit-report-onyxstaking-v1-0-pdf.md | MEDIUM | PeckShield | CHNStaking::stake(). Status The issue has been confirmed. 3.4 Trust Issue Of Admin Keys • ID: PVE-004 • |
| [o13] | reports/other-l1_findings/publications-audius-solana-zellic-audit-report-pdf.md | CRITICAL | Zellic | DetailedFindings 3.1 MissingPDAvalidationleadingtomultipletransfers • Target:RewardsManager • Category:CodingMistakes • Likelihood:High • |
| [o14] | reports/other-l1_findings/publications-gammaswap-staking-zellic-audit-report-pdf.md | MEDIUM | Zellic | Cancellation ofisDepositToken still allows rewards to be claimed • Target:RewardTracker • Category:CodingMistakes • Likelihood:Low • |
| [o15] | reports/other-l1_findings/publications-nimbora-zellic-audit-report-pdf.md | HIGH | Zellic | Stray buckets in past withdrawals can block epoch progression |
| [o16] | reports/other-l1_findings/publications-pdt-staking-v2-zellic-audit-report-pdf.md | CRITICAL | Zellic | Reward-token registration is irreversible |
| [o17] | reports/other-l1_findings/publications-pdt-staking-v2-zellic-audit-report-pdf.md | MEDIUM | Zellic | PDT can be set as a reward token and withdrawn by admin |
| [o18] | reports/other-l1_findings/publications-polygon-staking-zellic-audit-report-pdf.md | MEDIUM | Zellic | The rewards quantity is not deducted if the unbond quantity is lesser |
| [o19] | reports/other-l1_findings/publicreports-algorand-smart-contract-audit-yieldly-finance-compound-algorand-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | REWARDS ARE NOT UPDATED AFTER THE STAKE/WITHDRAW PROCESSES |
| [o20] | reports/other-l1_findings/publicreports-l1-audits-koii-network-k2-l1-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | INTEGER OVERFLOW LEADS TO UNFAIR REWARD DISTRIBUTION |
| [o21] | reports/other-l1_findings/publicreports-l1-audits-koii-network-k2-l1-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | HIJACKING STAKE POT ACCOUNTS |
| [o22] | reports/other-l1_findings/publicreports-l1-audits-koii-network-k2-l1-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | SORTING METHOD LEADS TO UNFAIR REWARD DISTRIBUTION |
| [o23] | reports/other-l1_findings/publicreports-l1-audits-koii-network-k2-l1-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | FUNDING AND DELETING INCORRECT STAKE POT ACCOUNTS |
| [o24] | reports/other-l1_findings/publicreports-near-smart-contract-audits-aurora-staking-farm-near-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | HAL03 - MULTIPLE STAKING ACTIONS CAN BE PERFORMED WHILE CONTRACT IS PAUSED |
| [o25] | reports/other-l1_findings/publicreports-solana-program-audit-cropper-finance-farm-solana-program-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | DELEGATE VALIDATION MISSING |
| [o26] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-alluvial-liquid-collective-smart-contract-security-audit-report-halborn-final-update-v2-pdf.md | HIGH | Halborn | DONATE CALL BEFORE DEPOSIT LEADS LOSS OF POSSIBLE REWARDS |
| [o27] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-biconomy-hyphen-v2-smart-contract-security-audit-report-halborn-final-pdf.md | CRITICAL | Halborn | WRONG FEE CALCULATION LEADS LOSS OF REWARD FUNDS |
| [o28] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-coredao-genesis-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | UNDELEGATED COINS ARE NOT CONSIDERED ON THE REWARD DISTRIBUTION |
| [o29] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-degis-scprotection-smart-contract-security-audit-report-halborn-pdf.md | CRITICAL | Halborn | POOL INCOMES ON REPORTER REWARD CAN BE ARBITRARILY INCREASED |
| [o30] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-degis-scprotection-smart-contract-security-audit-report-halborn-pdf.md | HIGH | Halborn | UPDATE REWARDS MAY CAUSE A DENIAL OF SERVICE BETWEEN YEARS |
| [o31] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-degis-scprotection-smart-contract-security-audit-report-halborn-pdf.md | HIGH | Halborn | INVALID REWARD UPDATING MECHANISM |
| [o32] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-floin-floin-smart-contracts-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | REWARD MODIFICATION LEADS TO REWARDS INFLATION |
| [o33] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-gmbl-computer-gmbl-contracts-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | IMPROPER REWARD CALCULATION IN THE HARVEST FUNCTION |
| [o34] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-highstreetmarket-staking-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | UNSTAKE FUNCTION CAN BE LOCKED IF TOTALWEIGHT EQUALS TO ZERO |
| [o35] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-highstreetmarket-staking-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | UPDATEHIGHPERBLOCK IMPACTS NEGATIVELY ALL THE UNCLAIMED REWARDS |
| [o36] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-liquis-evm-contracts-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | CONTROLLED PARAMETER CAN LEAD TO INVALID REWARD CALCULATION |
| [o37] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-moonwell-finance-token-sale-and-comptroller-updates-report-halborn-final-pdf.md | MEDIUM | Halborn | OWNER CAN RESET ALLOCATIONS - DELEGATIONS |
| [o38] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-ocean-protocol-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | DT TOKEN STAKE NOT CALCULATED SUCCESSFULLY |
| [o39] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-orion-liquidity-aggregator-smart-contract-security-assessment-report-halborn-final-pdf.md | HIGH | Halborn | USERS WITH NO ORN STAKED CAN NOT BE LIQUIDATED |
| [o40] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-substance-exchange-exchange-v4-smart-contract-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | INCORRECT TOKEN TRANSFER IN VESTING FUNCTION OF STAKING SMART CONTRACT |
| [o41] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-tenet-vetenet-smart-contract-security-assessment-report-halborn-final-pdf.md | HIGH | Halborn | POTENTIAL DUPLICATE REWARD TOKEN ENTRIES |
| [w42] | reports/other-l1_findings/publications-audit-reports-peckshield-audit-report-altixstaking-v1-0-pdf.md | MEDIUM | Immunefi (warden) | publications-audit-reports-peckshield-audit-report-altixstaking-v1-0 |
| [q43] | reports/other-l1_findings/audit-reports-incrementfi-audit-report-incrementfi-liquid-staking-pdf.md | LOW | Oak Security | Migrate function does not enforce minimum staking amount |
| [q44] | reports/other-l1_findings/audit-reports-incrementfi-audit-report-incrementfi-liquid-staking-pdf.md | LOW | Oak Security | Minimum staking amount and staking cap are not validated against each other |
| [q45] | reports/other-l1_findings/optimism-docs-security-reviews-2026-03-policyenginestaking-cantina-pdf.md | INFO | auditor | Fixed by updating the Spec documentation. Cantina Managed: Fix verified. 3.2.4 ABI/signature mismatch on stake/unstake and stakedAmount width |
| [q46] | reports/other-l1_findings/optimism-docs-security-reviews-2026-03-policyenginestaking-cantina-pdf.md | INFO | auditor | Cantina Managed: Acknowledged. 3.2.9 Beneficiaries can reset a delegating staker's lastUpdate by removing them from the al- lowlist |
| [q47] | reports/other-l1_findings/publications-audit-reports-peckshield-audit-report-airswap-staking-v1-0-pdf.md | INFO | PeckShield | Report #: 2023-100 Public 3   Detailed Results 3.1 Suggested Improvement in Staking::setDuration()/cancelDurationChange() • ID: PVE-001 • |
| [q48] | reports/other-l1_findings/publications-audit-reports-peckshield-audit-report-airswap-staking-v1-0-pdf.md | INFO | PeckShield | This issue has been resolved in the following commit:d0131af. 3.2 Consistent T ransfer Event in Staking::stake()/unstake() • ID: PVE-002 • |
| [q49] | reports/other-l1_findings/publications-audit-reports-peckshield-audit-report-gains-staking-v1-0-pdf.md | LOW | PeckShield | PeckShield Audit Report #: 2004-227 Public 3   Detailed Results 3.1 Suggested Sorted Withdrawal Rules in StakingContract • ID: PVE-001 • |
| [q50] | reports/other-l1_findings/publications-springsui-zellic-audit-report-pdf.md | INFO | Zellic | Active stake withdraw invariant |
| [q51] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-aura-finance-smart-contract-security-audit-report-halborn-final-pdf.md | LOW | Halborn | DUPLICATE ENTRY IN THE VESTING DISTRIBUTION LIST |
| [q52] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-bracket-fi-channels-and-epochchannels-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | IMMUTABLE DEPENDENCIES OF THE EPOCH CHANNELS CONTRACT |
| [q53] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-bware-labs-staking-protocol-smart-contract-security-audit-report-halborn-final-pdf-pdf.md | LOW | Halborn | UNUSABLE STAKING POOL AFTER POOL OWNER UNSTAKE |
| [q54] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-pangolin-allocationvester-smart-contract-security-audit-report-halborn-final-pdf.md | LOW | Halborn | INACCURATE REWARD RATE CALCULATION |
| [q55] | reports/eth-l1-clients_findings/audit-reports-animoca-2025-06-23-audit-report-anichess-ethereum-contracts-v1-2-pdf.md | INFO | Oak Security | Missing event emission to distinguish stake sources (Anichess ethereum contracts v1.2) |
| [q56] | reports/eth-l1-clients_findings/audit-reports-animoca-2025-06-23-audit-report-anichess-ethereum-contracts-v1-2-pdf.md | INFO | Oak Security | Misleading error message (Anichess ethereum contracts v1.2) |
| [q57] | reports/eth-l1-clients_findings/publications-reviews-2025-1-everstake-ethereum-staking-protocol-securityreview-pdf.md | INFO | Trail of Bits | Project uses archived and outdated tools (Everstake ethereum staking protocol) |
| [q58] | reports/eth-l1-clients_findings/publications-reviews-2025-1-everstake-ethereum-staking-protocol-securityreview-pdf.md | INFO | Trail of Bits | Project uses outdated dependencies (Everstake ethereum staking protocol) |
| [q59] | reports/eth-l1-clients_findings/publications-reviews-2025-1-everstake-ethereum-staking-protocol-securityreview-pdf.md | INFO | Trail of Bits | Documentation is out of sync with the code (Everstake ethereum staking protocol) |
| [q60] | reports/eth-l1-clients_findings/publications-reviews-2025-1-everstake-ethereum-staking-protocol-securityreview-pdf.md | INFO | Trail of Bits | Documentation lacks a glossary (Everstake ethereum staking protocol) |
| [q61] | reports/eth-l1-clients_findings/publications-reviews-2025-1-everstake-ethereum-staking-protocol-securityreview-pdf.md | INFO | Trail of Bits | Duplicated code (Everstake ethereum staking protocol) |
| [q62] | reports/eth-l1-clients_findings/publications-reviews-2025-1-everstake-ethereum-staking-protocol-securityreview-pdf.md | INFO | Trail of Bits | Storage variables updated by multiple contracts in the inheritance tree (Everstake ethereum staking protocol) |
| [q63] | reports/eth-l1-clients_findings/publications-reviews-2025-1-everstake-ethereum-staking-protocol-securityreview-pdf.md | INFO | Trail of Bits | _update may fail to update REWARDER_BALANCE_POSITION (Everstake ethereum staking protocol) |
| [q64] | reports/eth-l1-clients_findings/publicreports-solidity-smart-contract-audits-lodestar-finance-staking-smart-contract-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | (HAL-01) esLODE tokens can be drained by calling withdrawEsLODE() function indefinitely (Lodestar Finance esLODE staking) |
| [q65] | reports/eth-l1-clients_findings/publicreports-solidity-smart-contract-audits-lodestar-finance-staking-smart-contract-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | (HAL-02) Voting power can be manipulated by staking, voting, unstaking 10 seconds later and transferring LODE to a new wallet (Lodestar Finance esLODE staking) |
| [q66] | reports/eth-l1-clients_findings/publicreports-solidity-smart-contract-audits-lodestar-finance-staking-smart-contract-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | (HAL-03) Voting power can be stolen by calling votingPower.delegate function (Lodestar Finance esLODE staking) |
| [q67] | reports/eth-l1-clients_findings/publicreports-solidity-smart-contract-audits-lodestar-finance-staking-smart-contract-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | (HAL-04) The one year vesting period for esLODE tokens can be bypassed (Lodestar Finance esLODE staking) |
| [q68] | reports/eth-l1-clients_findings/publicreports-solidity-smart-contract-audits-lodestar-finance-staking-smart-contract-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | (HAL-05) LODE tokens can be permanently stuck in the stakingRestakeLODE functions (Lodestar Finance esLODE staking) |
| [q69] | reports/eth-l1-clients_findings/publicreports-solidity-smart-contract-audits-lodestar-finance-staking-smart-contract-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | (HAL-06) unstakeLODE function may revert as voting power is incorrectly burnt (Lodestar Finance esLODE staking) |
| [q70] | reports/eth-l1-clients_findings/publicreports-solidity-smart-contract-audits-lodestar-finance-staking-smart-contract-security-assessment-report-halborn-final-pdf.md | HIGH | Halborn | (HAL-07) esLODE tokens could get locked permanently in the stakingRewards contract (Lodestar Finance esLODE staking) |
| [q71] | reports/eth-l1-clients_findings/publicreports-solidity-smart-contract-audits-lodestar-finance-staking-smart-contract-security-assessment-report-halborn-final-pdf.md | HIGH | Halborn | (HAL-08) Voting power can be manipulated with a LODE flashloan (Lodestar Finance esLODE staking) |
| [q72] | reports/eth-l1-clients_findings/publicreports-solidity-smart-contract-audits-lodestar-finance-staking-smart-contract-security-assessment-report-halborn-final-pdf.md | HIGH | Halborn | (HAL-09) LODE locking can be bypassed abusing the rewards system (Lodestar Finance esLODE staking) |
| [q73] | reports/eth-l1-clients_findings/publicreports-solidity-smart-contract-audits-lodestar-finance-staking-smart-contract-security-assessment-report-halborn-final-pdf.md | HIGH | Halborn | (HAL-10) Relocking full bonus can be obtained after a 10 seconds lock (Lodestar Finance esLODE staking) |
| [q74] | reports/eth-l1-clients_findings/publicreports-solidity-smart-contract-audits-lodestar-finance-staking-smart-contract-security-assessment-report-halborn-final-pdf.md | HIGH | Halborn | (HAL-11) convertEsLODEToLODE function excessively burns voting power, reverting (Lodestar Finance esLODE staking) |
| [q75] | reports/eth-l1-clients_findings/publicreports-solidity-smart-contract-audits-lodestar-finance-staking-smart-contract-security-assessment-report-halborn-final-pdf.md | HIGH | Halborn | (HAL-12) Stakers may not be able to unstake their LODE tokens due to rounding error (Lodestar Finance esLODE staking) |
| [q76] | reports/eth-l1-clients_findings/publicreports-solidity-smart-contract-audits-lodestar-finance-staking-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | (HAL-13) updateWeeklyRewards function does not guarantee rewards for stakers (Lodestar Finance esLODE staking) |
| [q77] | reports/eth-l1-clients_findings/publicreports-solidity-smart-contract-audits-lodestar-finance-staking-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | (HAL-14) Calling stakingRewards.updateVotingContract function can break the stakingRewards contract (Lodestar Finance esLODE staking) |
| [q78] | reports/eth-l1-clients_findings/publicreports-solidity-smart-contract-audits-lodestar-finance-staking-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | (HAL-15) Possible denial of service by reaching block gas limit when calling convertEsLODEToLODE function (Lodestar Finance esLODE staking) |
| [q79] | reports/eth-l1-clients_findings/publicreports-solidity-smart-contract-audits-lodestar-finance-staking-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | (HAL-16) updateShares is not called in certain cases in the relock function (Lodestar Finance esLODE staking) |
| [q80] | reports/eth-l1-clients_findings/publicreports-solidity-smart-contract-audits-lodestar-finance-staking-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | (HAL-17/18) State variables missing immutable/constant modifier (Lodestar Finance esLODE staking) |
| [q81] | reports/eth-l1-clients_findings/publicreports-solidity-smart-contract-audits-lodestar-finance-staking-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | (HAL-19) Structs do not follow the tight variable packing pattern (Lodestar Finance esLODE staking) |
| [q82] | reports/eth-l1-clients_findings/publicreports-solidity-smart-contract-audits-lodestar-finance-staking-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | (HAL-20) Floating pragma (Lodestar Finance esLODE staking) |
| [q83] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-lybra-finance-v2-smart-contract-security-assessment-report-halborn-final-pdf.md | HIGH | Halborn | (HAL-01) CurvePool.exchangeUnderlying() call could constantly revert in the distributeRewards function (Lybra Finance v2 LSD) |
| [q84] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-lybra-finance-v2-smart-contract-security-assessment-report-halborn-final-pdf.md | HIGH | Halborn | (HAL-02) peUSD.convertToPeUSD() call could cause a denial of service in the distributeRewards function (Lybra Finance v2 LSD) |
| [q85] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-lybra-finance-v2-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | (HAL-03) LybraConfigurator contract assumes that the USDC price will be always pegged to 1 USD (Lybra Finance v2 LSD) |
| [q86] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-lybra-finance-v2-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | (HAL-04) Liquidation calls can be frontrun stealing the reward2Keeper fee (Lybra Finance v2 LSD) |
| [q87] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-lybra-finance-v2-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | (HAL-05) LybraGovernance proposal creation can be DoS'ed (Lybra Finance v2 LSD) |
| [q88] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-lybra-finance-v2-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | (HAL-06) Centralization issue: LybraGovernance deployer has DAO and GOV roles (Lybra Finance v2 LSD) |
| [q89] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-lybra-finance-v2-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | (HAL-07) Missing staleness checks in the Chainlink.latestRoundData() calls (Lybra Finance v2 LSD) |
| [q90] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-lybra-finance-v2-smart-contract-security-assessment-report-halborn-final-pdf.md | LOW | Halborn | (HAL-08) Missing burnEnabled modifier in the peUSDMainnet.convertToEUSD() function (Lybra Finance v2 LSD) |
| [q91] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-lybra-finance-v2-smart-contract-security-assessment-report-halborn-final-pdf.md | LOW | Halborn | (HAL-09) Missing mintEnabled modifier in the peUSDMainnet.convertToPeUSD() function (Lybra Finance v2 LSD) |
| [q92] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-lybra-finance-v2-smart-contract-security-assessment-report-halborn-final-pdf.md | LOW | Halborn | (HAL-10) LybraRETHVault.depositEtherToMint() function calls may revert (Lybra Finance v2 LSD) |
| [q93] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-lybra-finance-v2-smart-contract-security-assessment-report-halborn-final-pdf.md | LOW | Halborn | (HAL-11) Hardcoded dstChainId in stakingRewardsOnArbi contract (Lybra Finance v2 LSD) |
| [q94] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-lybra-finance-v2-smart-contract-security-assessment-report-halborn-final-pdf.md | LOW | Halborn | (HAL-12) Collateral minimum deposit amount can be bypassed (Lybra Finance v2 LSD) |
| [q95] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-lybra-finance-v2-smart-contract-security-assessment-report-halborn-final-pdf.md | LOW | Halborn | (HAL-13) LybraGovernance hardcoded 4 percent quorum (Lybra Finance v2 LSD) |
| [q96] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-lybra-finance-v2-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | (HAL-14) eUSDPriceFeed hardcoded decimals (Lybra Finance v2 LSD) |
| [q97] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-lybra-finance-v2-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | (HAL-15) State variables missing immutable modifier (Lybra Finance v2 LSD) |
| [q98] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-lybra-finance-v2-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | (HAL-16) Lack of a double-step transferOwnership pattern in multiple contracts (Lybra Finance v2 LSD) |
| [q99] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-lybra-finance-v2-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | (HAL-17) Floating pragma (Lybra Finance v2 LSD) |
## L1 Staking Generic

**l1-staking-generic patterns mined from uncited L1 audit reports** - 48 sec-tier findings (13 critical / 15 high / 20 medium) across 33 files from Halborn, NCC Group, Oak Security, PeckShield, Zellic.

### Overview

Titles in the references table are verbatim from source reports. Route to the exact report file for full PoC detail. Validation strength: `unassessed` (evidence rows only).

### Detection Patterns

#### High-Signal Grep Seeds
```
- aavestrategy
- able
- accounted
- accounts
- actions
- admin
- after
- allocations
```

### Vulnerability Description

#### Root Cause

The cited reports describe l1 staking generic paths where a validation, bound, or state-consistency check is missing around attacker-influenced input or an attacker-growable collection. The pattern key for this family is `l1-staking-generic | l1 staking generic | varies by finding | see references`. Every reference row in the table above is a verbatim finding title from the named auditor; consult that report for the exact code location and exploit path.

#### Attack Scenario / Path Variants

**Path A: [Direct input path]**
Path key: `l1-staking-generic | l1 staking generic | varies by finding | see references | user/peer message | direct handler`
1. Attacker submits crafted input (message, tx, packet, or config change) accepted by the entry surface.
2. Missing validation lets the input reach state mutation or an unbounded loop.
3. State corruption, fund misaccounting, or resource exhaustion follows.

**Path B: [Growth-then-trigger path]**
Path key: `l1-staking-generic | l1 staking generic | varies by finding | see references | cheap state growth | later iteration/execution`
1. Attacker cheaply grows a collection (plans, stakes, peers, entries).
2. A later block-time or cleanup path iterates the collection without bounds.
3. Block production exceeds limits or the node exhausts memory (DoS / halt).

### Vulnerable Pattern Examples

**Example 1: Detailed Findings SSBS-01 Reentrancy Vulnerability Allows Draining All Funds Asset StakingContractMainnet.sol Status Res** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Detailed Findings SSBS-01 Reentrancy Vulnerability Allows Draining All Funds Asset StakingContractMainnet.sol Status Resolved: Rating
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Detailed Findings SSBS-01 Reentrancy Vulnerability Allows Draining All Funds Asset StakingContractMa
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 2: SSBS-02 Missing Input Validation Allows Subscribing to Non-Existent Incentives Asset StakingContractMainnet.sol Status R** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// SSBS-02 Missing Input Validation Allows Subscribing to Non-Existent Incentives Asset StakingContractMainnet.sol Status Resolved: Rating
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: SSBS-02 Missing Input Validation Allows Subscribing to Non-Existent Incentives Asset StakingContract
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 3: DetailedFindings 3.1 MissingPDAvalidationleadingtomultipletransfers • Target:RewardsManager • Category:CodingMistakes • ** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// DetailedFindings 3.1 MissingPDAvalidationleadingtomultipletransfers • Target:RewardsManager • Category:CodingMistakes • Likelihood:High •
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: DetailedFindings 3.1 MissingPDAvalidationleadingtomultipletransfers • Target:RewardsManager • Catego
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

`aavestrategy, able, accounted, accounts, actions, admin, after, allocations, allows, amount`

### Related Vulnerabilities

- Sibling entries under the same category folder
