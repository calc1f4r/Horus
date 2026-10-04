---
# Core Classification
protocol: generic
chain: generic
category: l1
vulnerability_type: l1_contract_generic
root_cause_family: see pattern_key

# Pattern Identity
pattern_key: l1-contract-generic | l1 contract generic | varies by finding | see references

# Interaction Scope
interaction_scope: varies
involved_contracts:
  - l1 contract generic

# Attack Vector Details
attack_type: varies
affected_component: l1 contract generic

# Technical Primitives
primitives:
  - _getselfdelegations
  - aave
  - aavestrategy
  - aavestrategymainnet
  - able
  - absence

# Grep / Hunt-Card Seeds
code_keywords:
  - _getselfdelegations
  - aave
  - aavestrategy
  - aavestrategymainnet
  - able
  - absence
  - account
  - accounting

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
| [o1] | reports/other-l1_findings/audit-reports-milkyway-2023-12-12-audit-report-milkyway-staking-v1-0-pdf.md | HIGH | Oak Security | Repeatedly failed ICS-20 token transfers cannot be recovered |
| [o2] | reports/other-l1_findings/audit-reports-milkyway-2025-05-15-audit-report-milkyway-staking-updates-v1-0-pdf.md | HIGH | Oak Security | Migration will fail due to the incorrect contract version set |
| [o3] | reports/other-l1_findings/audit-reports-risk-harbor-2022-03-22-audit-report-risk-harbor-v1-0-pdf.md | HIGH | Oak Security | Lack of pool status validation in claim function leads to a race between underwriters to withdraw and insurees to claim funds |
| [o4] | reports/other-l1_findings/audit-reports-router-2024-04-30-audit-report-router-asset-bridge-v1-2-pdf.md | CRITICAL | Oak Security | Attackers can profit by depositing different tokens and withdrawing as native tokens |
| [o5] | reports/other-l1_findings/audit-reports-router-2024-04-30-audit-report-router-asset-bridge-v1-2-pdf.md | CRITICAL | Oak Security | Fungible token refunds will fail  causing a loss of funds for users |
| [o6] | reports/other-l1_findings/audit-reports-router-2024-04-30-audit-report-router-asset-bridge-v1-2-pdf.md | HIGH | Oak Security | Unstaking liquidity token fails due to incorrect token parameters |
| [o7] | reports/other-l1_findings/audit-reports-router-2024-04-30-audit-report-router-asset-bridge-v1-2-pdf.md | HIGH | Oak Security | Native token transfers always fail due to improper balance check query |
| [o8] | reports/other-l1_findings/audit-reports-router-2024-04-30-audit-report-router-asset-bridge-v1-2-pdf.md | HIGH | Oak Security | Unintended refund due to TEMP_REVERT_STATE not being cleared and incorrectly calling of revert_inbound_to_src_chain on minting gas tokens |
| [o9] | reports/other-l1_findings/audit-reports-router-2024-04-30-audit-report-router-asset-bridge-v1-2-pdf.md | HIGH | Oak Security | The amount of minted gas tokens can exceed the actual charged fee amount |
| [o10] | reports/other-l1_findings/audit-reports-router-2024-05-29-audit-report-router-evm-and-near-gateway-contracts-and-wasm-bindings-v1-0-pdf.md | CRITICAL | Oak Security | Incorrect isReadCall implementation allows infinite token mints |
| [o11] | reports/other-l1_findings/audit-reports-router-2024-05-29-audit-report-router-evm-and-near-gateway-contracts-and-wasm-bindings-v1-0-pdf.md | CRITICAL | Oak Security | ROUTE tokens are not minted for invalid requests  causing a loss of funds |
| [o12] | reports/other-l1_findings/audit-reports-router-2024-05-29-audit-report-router-evm-and-near-gateway-contracts-and-wasm-bindings-v1-0-pdf.md | HIGH | Oak Security | ASM contract state is committed when token mint fails |
| [o13] | reports/other-l1_findings/audit-reports-router-2024-05-29-audit-report-router-evm-and-near-gateway-contracts-and-wasm-bindings-v1-0-pdf.md | HIGH | Oak Security | Incomplete state rollback for failures in minting the ROUTE token |
| [o14] | reports/other-l1_findings/optimism-docs-security-reviews-2022-05-opnode-trailofbits-pdf.md | HIGH | Trail of Bits | Risk of theft due to reentrancy vulnerability in WithdrawalsRelay Status: Resolved |
| [o15] | reports/other-l1_findings/optimism-docs-security-reviews-2022-05-opnode-trailofbits-pdf.md | HIGH | Trail of Bits | Pre-deployed L1 attributes contract will never be updated Status: Resolved |
| [o16] | reports/other-l1_findings/public-audits-reports-mantle-review-pdf.md | CRITICAL | NCC Group | TSS Nodes Can Act Without Any Deposit Asset packages/contracts/contracts/L1/tss/TssGroupManager.sol Status Resolved: See Resolution Rating |
| [o17] | reports/other-l1_findings/public-audits-reports-mantle-review-pdf.md | HIGH | NCC Group | No Mechanism T o Flag Sequencer Fraud Asset packages/contracts/contracts/da/BVM_EigenDataLayrChain.sol Status Closed: See Resolution Rating |
| [o18] | reports/other-l1_findings/public-audits-reports-mantle-review-pdf.md | HIGH | NCC Group | By Having Insufficient Deposits Asset packages/contracts/contracts/L1/tss/TssStakingSlashing.sol Status Resolved: See Resolution Rating |
| [o19] | reports/other-l1_findings/public-audits-reports-mantle-review-pdf.md | HIGH | NCC Group | Findings MNT-06 Precompiled Contract Not Updated Asset l2geth/contracts/tssreward/contract/tssreward.go Status Closed: See Resolution Rating |
| [o20] | reports/other-l1_findings/public-audits-reports-mantle-review-pdf.md | MEDIUM | NCC Group | Checks Asset tss/ws/server/handler.go  tss/manager/sign.go  datalayr-mantle/common/contracts/utils.go Status Resolved: See Resolution Rating |
| [o21] | reports/other-l1_findings/public-audits-reports-mantle-review-pdf.md | MEDIUM | NCC Group | Are Vulnerable T o Front Running Asset packages/contracts/contracts/L1/tss/TssStakingSlashing.sol Status Resolved: See Resolution Rating |
| [o22] | reports/other-l1_findings/public-audits-reports-omni-network-sigma-prime-omni-avs-and-token-security-assessment-report-v2-1-pdf.md | CRITICAL | NCC Group | Contract Review Detailed Findings OMI-01 Infinite Loop In _getSelfDelegations() Asset OmniAVS.sol Status Resolved: See Resolution Rating |
| [o23] | reports/other-l1_findings/public-audits-reports-omni-network-sigma-prime-omni-evm-redenom-security-assessment-report-v2-0-pdf.md | MEDIUM | auditor | Root And Infrastructure Upgrades Allows For Value Extraction Asset halo/app/upgrades/earhart/upgrade.go Status Closed: See Resolution Rating |
| [o24] | reports/other-l1_findings/public-audits-reports-omni-network-sigma-prime-omni-network-omni-portal-security-assessment-report-v2-1-pdf.md | MEDIUM | NCC Group | Findings OMP-10 Relayers Can Be Griefed With xsubmit() Reentrancy Asset protocol/OmniPortal.sol Status Resolved: See Resolution Rating |
| [o25] | reports/other-l1_findings/public-audits-reports-omni-network-sigma-prime-omni-solvernet-security-assessment-report-v2-0-pdf.md | CRITICAL | NCC Group | Unnecessary Reentrancy Protection In markFilled() Function Allows Fund Theft Asset SolverNetInbox.sol Status Resolved: See Resolution Rating |
| [o26] | reports/other-l1_findings/publications-ebridge-aelf-bridge-zellic-audit-report-pdf.md | CRITICAL | Zellic | Unchecked sender inQueryOracle function leading to potential oracle manip- ulation |
| [o27] | reports/other-l1_findings/publications-ebridge-aelf-bridge-zellic-audit-report-pdf.md | HIGH | Zellic | Bypassable oracle fee via manipulated payment input to QueryOracle |
| [o28] | reports/other-l1_findings/publicreports-financial-pentesting-apy-financial-pentesting-report-halborn-final-pdf.md | HIGH | Halborn | EARLY UNLOCKING OF ORACLE ADAPTER COULD LEAD TO UNFAIR WITHDRAWING |
| [o29] | reports/other-l1_findings/publicreports-financial-pentesting-apy-financial-pentesting-report-halborn-final-pdf.md | MEDIUM | Halborn | INSUFFICIENT PROTECTION FOR ORACLE ADAPTER COULD LEAD TO TVL / PRICE MANIPULATION |
| [o30] | reports/other-l1_findings/publicreports-financial-pentesting-apy-financial-pentesting-report-halborn-final-pdf.md | MEDIUM | Halborn | LACK OF INTERNAL MECHANISMS TO DETECT ABNORMAL VALUES FROM ORACLES |
| [o31] | reports/other-l1_findings/publicreports-financial-pentesting-centaurswap-financial-pentesting-halborn-v1-1-pdf.md | MEDIUM | Halborn | PRICE FEED - ORACLE RISK ASSESSMENT |
| [o32] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-alluvial-liquid-collective-smart-contract-security-audit-report-halborn-final-update-v2-pdf.md | MEDIUM | Halborn | ORACLE SHOULD CHECK UNDERLYING BALANCE INSTEAD OF TOTAL SUPPLY |
| [o33] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-convergence-finance-convergence-protocol-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | ORACLE RESPONSE NOT CHECKED FOR STALE PRICES |
| [o34] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-convergence-finance-convergence-protocol-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | PRICE FEED AGGREGATOR NOT RETURNING ADDITIONAL PARAMETERS |
| [o35] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-easyfi-lending-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | MISUSE OF AN ORACLE |
| [o36] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-floin-floin-smart-contracts-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | FIXED PRICE FOR EUR/USD PAIR CAN AFFECT CROWDSALE TOKEN PRICES |
| [o37] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-lyra-finance-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | SKEW UPDATE COULD CREATE DATA INCONSISTENCIES WITH GWAV ORACLE |
| [o38] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-orion-liquidity-aggregator-smart-contract-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | INCORRECT PRICES ARE FETCHED DURING LIQUIDATION |
| [o39] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-planet-finance-green-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | MISUSE OF AN ORACLE |
| [o40] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-qoda-finance-core-v1-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | DIA ORACLE DOES NOT HAVE PROTECTION FOR ZERO VALUE |
| [o41] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-uranium3o8-launchpad-smart-contract-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | UNHANDLED STALE ORACLE PRICES |
| [o42] | reports/other-l1_findings/public-audits-reports-omni-network-sigma-prime-omni-token-upgrade-frontend-security-assessment-report-v2-0-pdf.md | MEDIUM | auditor | T oken Upgrade Frontend Detailed Findings OTU-01 Incorrect Exchange Rate Quote Asset modal.tsx Status Resolved: See Resolution Rating |
| [o43] | reports/other-l1_findings/public-audits-reports-origin-sigma-prime-origin-protocol-validator-consolidations-security-assessment-report-v2-0-pdf.md | MEDIUM | auditor | Status Resolved:See Resolution Rating |
| [o44] | reports/other-l1_findings/public-audits-reports-origin-sigma-prime-origin-protocol-validator-consolidations-security-assessment-report-v2-0-pdf.md | MEDIUM | auditor | Consolidation Requests Assets contracts/contracts/strategies/NativeStaking/ConsolidationController.sol Status Resolved:See Resolution Rating |
| [o49] | reports/other-l1_findings/publications-evm-depositwithdraw-bridge-zellic-audit-report-pdf.md | MEDIUM | Zellic | Gas griefing during native withdrawal settlement |
| [o50] | reports/other-l1_findings/publications-fuelet-zellic-audit-report-pdf.md | CRITICAL | Zellic | Universal XSS in Fuelet dApp WebView |
| [o51] | reports/other-l1_findings/publications-fuelet-zellic-audit-report-pdf.md | HIGH | Zellic | Origin impersonation via URL username and elision |
| [o52] | reports/other-l1_findings/publications-fuelet-zellic-audit-report-pdf.md | MEDIUM | Zellic | Optimizable PasswordManager check |
| [o53] | reports/other-l1_findings/publications-fuelet-zellic-audit-report-pdf.md | MEDIUM | Zellic | Insecure cloud-backup encryption |
| [o54] | reports/other-l1_findings/publications-layerzero-solana-endpoint-zellic-audit-report-pdf.md | HIGH | Zellic | Arbitary ULN PDAs can be closed |
| [o55] | reports/other-l1_findings/publications-layerzero-solana-endpoint-zellic-audit-report-pdf.md | HIGH | Zellic | OAPP can reassign executor account |
| [o56] | reports/other-l1_findings/publications-layerzero-solana-endpoint-zellic-audit-report-pdf.md | MEDIUM | Zellic | Insufficient remaining_accounts for optional DVNs |
| [o57] | reports/other-l1_findings/publications-mina-token-bridge-zellic-audit-report-pdf.md | HIGH | Zellic | Bypassing daily quota may lead to stuck funds |
| [o58] | reports/other-l1_findings/publications-move-and-sui-security-assessment-zellic-audit-report-pdf.md | CRITICAL | Zellic | Commandresultswithoutthe dropabilitycouldbedropped • Target:ProgrammableTransactions • Category:CodingMistakes • Likelihood:High • |
| [o59] | reports/other-l1_findings/publications-move-and-sui-security-assessment-zellic-audit-report-pdf.md | CRITICAL | Zellic | Zellic 10 MystenLabs 3.2 Incorrectcontrolflowgraphconstruction • Target:CoreMoveVerifier • Category:CodingMistakes • Likelihood:High • |
| [o60] | reports/other-l1_findings/publications-move-and-sui-security-assessment-zellic-audit-report-pdf.md | MEDIUM | Zellic | VecPackand VecUnpackinstructions • Target:TypeSafetyandReferenceSafetyVerifiers • Category:CodingMistakes • Likelihood:Medium • |
| [o61] | reports/other-l1_findings/publications-n1-bridge-zellic-audit-report-pdf.md | HIGH | Zellic | Insufficient block validation |
| [o62] | reports/other-l1_findings/publications-pyth-lazer-solana-zellic-audit-report-pdf.md | CRITICAL | Zellic | Signature bypass |
| [o63] | reports/other-l1_findings/publications-reviews-2023-07-solana-solang-library-securityreview-pdf.md | MEDIUM | Trail of Bits | spl_token incorrectly sets some accounts to writable |
| [o64] | reports/other-l1_findings/publications-reviews-2023-07-solana-solang-library-securityreview-pdf.md | MEDIUM | Trail of Bits | spl_token incorrectly decodes the close_authority field of the token account |
| [o65] | reports/other-l1_findings/publications-reviews-2023-11-solana-solang-code-generation-part-1-securityreview-pdf.md | HIGH | Trail of Bits | Hard-coded number of accounts in SolParameters |
| [o66] | reports/other-l1_findings/publications-reviews-2023-11-solana-solang-code-generation-part-1-securityreview-pdf.md | HIGH | Trail of Bits | Out-of-bounds read in the external_call function |
| [o67] | reports/other-l1_findings/publications-reviews-2023-11-solana-solang-code-generation-part-1-securityreview-pdf.md | HIGH | Trail of Bits | Out-of-bounds write in the external_call function |
| [o68] | reports/other-l1_findings/publications-reviews-2023-11-solana-solang-code-generation-securityreview-pdf.md | HIGH | Trail of Bits | Solang-compiled contracts can have multiple storage accounts |
| [o69] | reports/other-l1_findings/publications-reviews-2023-11-solana-solang-code-generation-securityreview-pdf.md | HIGH | Trail of Bits | An attacker can reinitialize a Solang contract |
| [o70] | reports/other-l1_findings/publications-reviews-2023-11-solana-solang-code-generation-securityreview-pdf.md | MEDIUM | Trail of Bits | Compiler does not verify the developer-specified size for the data account |
| [o71] | reports/other-l1_findings/publications-reviews-2023-11-solana-solang-code-generation-securityreview-pdf.md | HIGH | Trail of Bits | Appending state variables to Solang contracts affects their storage layout |
| [o72] | reports/other-l1_findings/publications-reviews-2023-11-solana-solang-code-generation-securityreview-pdf.md | HIGH | Trail of Bits | Fallback function does not verify the data account's magic value |
| [o73] | reports/other-l1_findings/publications-reviews-2024-02-silencelaboratories-silentshard-securityreview-pdf.md | MEDIUM | Trail of Bits | DKG implementation does not enforce length check of committed polynomials |
| [o74] | reports/other-l1_findings/publications-reviews-2024-02-silencelaboratories-silentshard-securityreview-pdf.md | MEDIUM | Trail of Bits | DKG implementation does not enforce zero-knowledge proof verification |
| [o75] | reports/other-l1_findings/publications-reviews-2024-02-silencelaboratories-silentshard-securityreview-pdf.md | HIGH | Trail of Bits | Communication channels between parties can reuse nonces |
| [o76] | reports/other-l1_findings/publications-reviews-2024-02-silencelaboratories-silentshard-securityreview-pdf.md | MEDIUM | Trail of Bits | Parties may not agree on root chain code after DKG |
| [o77] | reports/other-l1_findings/publications-reviews-2024-02-silencelaboratories-silentshard-securityreview-pdf.md | MEDIUM | Trail of Bits | Inconsistent DSG session ID causes honest parties to denylist each other |
| [o78] | reports/other-l1_findings/publications-reviews-2024-02-silencelaboratories-silentshard-securityreview-pdf.md | MEDIUM | Trail of Bits | Messages from previous signing sessions can be replayed |
| [o79] | reports/other-l1_findings/publications-reviews-2024-02-silencelaboratories-silentshard-securityreview-pdf.md | HIGH | Trail of Bits | Implementation mishandles selective abort attacks |
| [o80] | reports/other-l1_findings/publications-reviews-2024-05-polygonlabs-iden3circuits-securityreview-pdf.md | HIGH | Trail of Bits | Unsafe use of Num2Bits in multiple circuits |
| [o81] | reports/other-l1_findings/publications-reviews-2024-07-taraxa-bridge-smart-contracts-v2-securityreview-pdf.md | HIGH | Trail of Bits | Lack of safeTransfer usage for ERC |
| [o82] | reports/other-l1_findings/publications-reviews-2024-07-taraxa-bridge-smart-contracts-v2-securityreview-pdf.md | HIGH | Trail of Bits | Missing validation allows signatures to be duplicated to finalize any PillarBlock |
| [o83] | reports/other-l1_findings/publications-reviews-2025-01-zetachain-solana-gateway-security-review-pdf.md | HIGH | Trail of Bits | Rent payer account can be drained |
| [o84] | reports/other-l1_findings/publications-reviews-2025-05-near-one-pedpop-securityreview-pdf.md | MEDIUM | Trail of Bits | Generic DKG does not delete temporary secret values |
| [o85] | reports/other-l1_findings/publications-silo-staking-zellic-audit-report-pdf.md | HIGH | Zellic | Calling reconcile before token distribution from unbonding leads to funds stuckinthecontract |
| [o86] | reports/other-l1_findings/publications-suilend-zellic-audit-report-pdf.md | MEDIUM | Zellic | No mechanism for debt write-off |
| [o87] | reports/other-l1_findings/publications-suilend-zellic-audit-report-pdf.md | MEDIUM | Zellic | Rate limiter can be abused |
| [o88] | reports/other-l1_findings/publications-zcash-zakura-zellic-audit-report-pdf.md | HIGH | Zellic | Body tip conflated as header frontier disables watchdog fallback |
| [o89] | reports/other-l1_findings/publications-zcash-zakura-zellic-audit-report-pdf.md | HIGH | Zellic | Repeated reconsiderblock panics the state write thread |
| [o90] | reports/other-l1_findings/publications-zcash-zakura-zellic-audit-report-pdf.md | HIGH | Zellic | Post-NU6.3 coinbase accepts non-empty Orchard actions |
| [o91] | reports/other-l1_findings/publications-zcash-zakura-zellic-audit-report-pdf.md | HIGH | Zellic | Header and body frontier desync can stall catch-up |
| [o92] | reports/other-l1_findings/publications-zcash-zakura-zellic-audit-report-pdf.md | MEDIUM | Zellic | Registry miss globally stalls sync dispatch |
| [o93] | reports/other-l1_findings/publicauditreports-nm0131-final-worldcoin-state-bridge-contracts-upgrade-pdf.md | MEDIUM | Nethermind | Medium Info Best Practices Best Practices 81.8% |
| [o94] | reports/other-l1_findings/publicreports-algorand-smart-contract-audit-yieldly-finance-bridge-algorand-smart-contract-security-audit-halborn-v-1-1-pdf.md | MEDIUM | Halborn | LACK OF THRESHOLD CHECK |
| [o100] | reports/other-l1_findings/publicreports-mobile-pentest-make-casper-mobile-wallet-mobile-app-pentest-report-halborn-final-pdf.md | HIGH | Halborn | WEAK CRYPTOGRAPHY DUE TO CLEARTEXT PINCODE PASSED AS PASSPHRASE TO AES.PBKDF2 FUNCTION |
| [o101] | reports/other-l1_findings/publicreports-mobile-pentest-make-casper-mobile-wallet-mobile-app-pentest-report-halborn-final-pdf.md | HIGH | Halborn | ANDROID - FRIDA HOOKING ALLOWS BYPASS PINCODE ATTEMPTS |
| [o102] | reports/other-l1_findings/publicreports-mobile-pentest-make-casper-mobile-wallet-mobile-app-pentest-report-halborn-final-pdf.md | MEDIUM | Halborn | TAPJACKING |
| [o103] | reports/other-l1_findings/publicreports-move-smart-contract-audits-pancakeswap-aptos-dex-move-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | APPROVED TRANSACTIONS CAN BE INVALIDATED |
| [o104] | reports/other-l1_findings/publicreports-near-smart-contract-audits-metapool-katherine-fundraising-and-bond-market-near-smart-contract-security-audit-report-halborn-final-pdf.md | CRITICAL | Halborn | FUNDS LOCKING DUE TO UNAUTHORIZED BOND MERGING |
| [o105] | reports/other-l1_findings/publicreports-near-smart-contract-audits-metapool-liquid-staking-near-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | DENIAL OF SERVICE CONDITION DUE TO STORAGE BLOATING |
| [o106] | reports/other-l1_findings/publicreports-node-audits-playground-labs-self-custody-node-security-audit-report-halborn-final-pdf.md | CRITICAL | Halborn | API - AUTHENTICATED INTERNAL USERS CAN DELETE ANY OTHER USER |
| [o107] | reports/other-l1_findings/publicreports-node-audits-playground-labs-self-custody-node-security-audit-report-halborn-final-pdf.md | CRITICAL | Halborn | ARCHITECTURE - MISSING INTERNAL MFA CONTROLS |
| [o108] | reports/other-l1_findings/publicreports-node-audits-playground-labs-self-custody-node-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | ARCHITECTURE - MISSING RATE LIMIT |
| [o109] | reports/other-l1_findings/publicreports-node-audits-playground-labs-self-custody-node-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | API - USER ENUMERATION |
| [o110] | reports/other-l1_findings/publicreports-solana-program-audit-cropper-finance-amm-program-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | HARDCODED GOVERNANCE ADDRESSES |
| [o111] | reports/other-l1_findings/publicreports-solana-program-audit-goosefx-swap-program-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | POOLS CANNOT BE SUSPENDED |
| [o112] | reports/other-l1_findings/publicreports-solana-program-audit-goosefx-swap-program-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | OFFSET CURVE TOKEN MISMATCH |
| [o113] | reports/other-l1_findings/publicreports-solana-program-audit-phantasia-sports-nft-store-spa-solana-program-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | ANONYMOUS SELL ORDER CANCELLING |
| [o114] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-0x-nodes-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | MISSING RE-ENTRANCY PROTECTION |
| [o115] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-affine-defi-multiplyr-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | IGNORE EXTERNAL CALL FEE |
| [o116] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-affine-defi-multiplyr-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | POSSIBLE LOSS OF FUNDS |
| [o118] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-apy-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | POSSIBILITY OF MANUAL MINTING / BURNING OF MAPT TOKENS |
| [o119] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-archimedes-finance-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | HAL01 - OUSD BEHAVIOUR CAN LEAD TO UNDERFLOW WHEN OPENING A POSITION |
| [o120] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-bancor-smartcontract-halborn-report-v1-pdf.md | MEDIUM | Halborn | ASSESSMENT SUMMARY & FINDINGS OVERVIEW CRITICAL HIGH MEDIUM LOW 0 0 1 5 SECURITY ANALYSIS RISK LEVEL DEPRECATED PRAGMA VERSION OF SOLC |
| [o121] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-base-protocol-cascade-halborn-report-v1-pdf.md | CRITICAL | Halborn | ASSESSMENT SUMMARY & FINDINGS OVERVIEW CRITICAL HIGH MEDIUM LOW 0 0 0 3 SECURITY ANALYSIS RISK LEVEL Remediation Date RE-ENTRANCY |
| [o122] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-bastion-protocol-evm-contracts-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | MISSING DIVISION BY 0 CHECK |
| [o123] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-beanstalk-smart-contract-security-audit-report-halborn-final-pdf.md | CRITICAL | Halborn | INTERNAL BALANCE TOKENS CAN BE DRAINED THROUGH THE CURVEFACET.EXCHANGEUNDERLYING FUNCTION |
| [o124] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-beanstalk-smart-contract-security-audit-report-halborn-final-pdf.md | CRITICAL | Halborn | USDC OF THE INTERNAL BALANCE CAN BE DRAINED BY ANY USER THROUGH THE FERTILIZERFACET.MINTFERTILIZER FUNCTION |
| [o125] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-beanstalk-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | INCONSISTENT INTERNAL BALANCES WHEN SUPPLYING TRANSFER-ON-FEE OR DEFLATIONARY TOKENS |
| [o126] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-beanstalk-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | UNLIMITED FERTILIZER CAN BE BOUGHT THROUGH THE FERTILIZERFACET.MINTFERTILIZER FUNCTION |
| [o127] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-benqi-smart-contract-security-audit-halborn-v1-1-pdf.md | MEDIUM | Halborn | MISSING PAYMENT AMOUNT CHECK |
| [o128] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-biconomy-cross-chain-messaging-protocol-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | FEE PAYMENT BYPASS |
| [o129] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-biconomy-cross-chain-messaging-protocol-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | USING ARBITRARY TOKENS ALLOW FEE PAYMENT BYPASS |
| [o130] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-biconomy-cross-chain-messaging-protocol-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | UN HANDLED SITUATION ALLOWS TWICE FEE PAYMENT |
| [o131] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-biconomy-gastank-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | CONTRACT UPGRADE/INITIALIZATION DROPS MINIMUM DEPOSIT VALUE TO ZERO |
| [o132] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-biconomy-hyphen-v2-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | DIVISION BY ZERO BLOCKS TRANSFER OF FUNDS |
| [o133] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-biconomy-smart-wallet-contracts-v2-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | VULNERABLE ECDSA LIBRARY |
| [o134] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-biconomy-token-smart-contract-security-audit-report-halborn-v1-1-pdf.md | MEDIUM | Halborn | UNWANTED TOKEN MINTING ON CONTRACT UPGRADE |
| [o135] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-biconomy-token-smart-contract-security-audit-report-halborn-v1-1-pdf.md | MEDIUM | Halborn | POSSIBLE FRONT-RUNNING ON INITIALIZATION |
| [o136] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-biconomy-transferhandler-smart-contract-security-audit-report-halborn-v1-1-pdf.md | MEDIUM | Halborn | USERS CAN MANIPULATE THE TRANSFER FEE |
| [o137] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-bitscrunch-protocol-smart-contract-security-assessment-report-halborn-final-pdf.md | HIGH | Halborn | LOSS OF FUNDS FROM PROTOCOL WHEN SWAPPING STABLECOIN FOR BCUT TOKENS |
| [o138] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-blockswap-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | MAPPING IS NOT DECREASED AFTER A DEPOSIT |
| [o139] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-bubbleswap-concentrated-liquidity-pool-amm-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | ARITHMETIC ERROR CAN RESULT IN LOCKED USER FUNDS |
| [o140] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-bubbleswap-concentrated-liquidity-pool-amm-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | IMPROPER SWAP AMOUNTS HANDLING |
| [o141] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-bubbleswap-concentrated-liquidity-pool-amm-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | UNCONTROLLED FEEGROWTH ERROR WHEN ADDING LIQUIDITY |
| [o142] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-cere-bridge-smart-contract-security-audit-solidity-report-halborn-final-pdf.md | MEDIUM | Halborn | LACK OF MINIMUM THRESHOLD FOR INITIALRELAYERS/RELAYERTHRESHOLD |
| [o146] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-coredao-genesis-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | PROPOSAL CAN BE DEFEATED IF THERE IS NO MEMBER |
| [o147] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-coredao-genesis-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | ISCONTRACT MODIFIER CAN BE BYPASSED THROUGH CONSTRUCTOR |
| [o148] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-coredao-genesis-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | BURN ADDRESS SHOULD BE DEFINED AS DIFFERENT THAN SYSTEM CONTRACTS |
| [o149] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-coredao-genesis-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | MISSING CHECK TO IF THE AGENT IS MSG.SENDER WHEN TRANSFERRING POWER |
| [o150] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-coredao-genesis-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | CANDIDATES ARE NOT LIMITED ON THE REGISTRATION |
| [o151] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-coredao-genesis-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | MISSING ONLY INIT MODIFIER |
| [o152] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-coredao-genesis-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | DUST IS ADDED INTO THE FIRST MINER |
| [o153] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-creditswap-core-contracts-smart-contract-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | INADEQUATE PROPOSAL THRESHOLD SETTING IN CREDITSWAP GOVERNOR CONTRACT |
| [o154] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-creditswap-core-contracts-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | NON-STANDARD TOKENS CAN LEAD TO SILENT FAILURES |
| [o155] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-damfinance-audits-damfinance-lmcv-part-3-smart-contract-security-audit-report-halborn-final-pdf.md | CRITICAL | Halborn | UNLIMITED MINTING BY REUSING FAILED HYPERLANE MESSAGES |
| [o156] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-damfinance-audits-damfinance-lmcv-part-3-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | MISMATCHING DATA LOCATION DURING INHERITANCE |
| [o157] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-damfinance-audits-damfinance-lmcv-part-3-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | DENIAL OF SERVICE USING MINT DELAY |
| [o158] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-damfinance-audits-damfinance-lmcv-part-3-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | INCOMPLETE GUARDIAN IMPLEMENTATION |
| [o159] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-degis-scprotection-smart-contract-security-audit-report-halborn-pdf.md | CRITICAL | Halborn | DEPOSITING TO ANY POOL/TOKEN WITH ANY AMOUNT VIA CONTROLLED POLICY CENTER |
| [o160] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-degis-scprotection-smart-contract-security-audit-report-halborn-pdf.md | CRITICAL | Halborn | INFINITE VOTING BY BYPASSING LOCKING AND RE-CLAIMING LOCKED TOKENS |
| [o161] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-degis-scprotection-smart-contract-security-audit-report-halborn-pdf.md | CRITICAL | Halborn | CODE NOT CHECKING IF TOKEN IS NOT PRESENT |
| [o162] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-degis-scprotection-smart-contract-security-audit-report-halborn-pdf.md | CRITICAL | Halborn | DEPOSITING ON ANY POOL USING ANY TOKEN |
| [o163] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-degis-scprotection-smart-contract-security-audit-report-halborn-pdf.md | CRITICAL | Halborn | AN ATTACKER CAN WITHDRAW NOT OWNED TOKENS AND STEAL FUNDS |
| [o164] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-degis-scprotection-smart-contract-security-audit-report-halborn-pdf.md | CRITICAL | Halborn | UPDATING THE 0 INDEX TOKEN WEIGHT VIA UNREGISTERED TOKENS |
| [o165] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-degis-scprotection-smart-contract-security-audit-report-halborn-pdf.md | CRITICAL | Halborn | PUBLICLY EXPOSED FUNCTIONS |
| [o166] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-degis-scprotection-smart-contract-security-audit-report-halborn-pdf.md | CRITICAL | Halborn | DEPOSITING TO SECONDARY TOKENS DOES CAUSE THE CONTRACT TO LOCK |
| [o167] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-degis-scprotection-smart-contract-security-audit-report-halborn-pdf.md | CRITICAL | Halborn | INVALID VARIABLE VISIBILITY DOES CAUSE CONTRACT DEADLOCK |
| [o168] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-degis-scprotection-smart-contract-security-audit-report-halborn-pdf.md | CRITICAL | Halborn | INVALID EXTERNAL CALL DOES CAUSE CONTRACT DEADLOCK |
| [o169] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-degis-scprotection-smart-contract-security-audit-report-halborn-pdf.md | HIGH | Halborn | BUYING COVER FOR THREE MONTHS IS NEVER COUNTED DURING THE CURRENT MONTH |
| [o170] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-degis-scprotection-smart-contract-security-audit-report-halborn-pdf.md | HIGH | Halborn | MINTING ZERO AMOUNT DEADLOCK IS PRODUCED DURING PAYOUT CLAIMING |
| [o171] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-degis-scprotection-smart-contract-security-audit-report-halborn-pdf.md | HIGH | Halborn | COVER MAY BE UPDATED FOR MONTH'S VALUES OUT OF RANGE |
| [o172] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-degis-scprotection-smart-contract-security-audit-report-halborn-pdf.md | HIGH | Halborn | REPORTING DEADLOCK IF QUORUM NOT REACHED |
| [o173] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-degis-scprotection-smart-contract-security-audit-report-halborn-pdf.md | HIGH | Halborn | INVALID PERCENTAGE RESULTS IN LESS PAYED DEBT |
| [o174] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-degis-scprotection-smart-contract-security-audit-report-halborn-pdf.md | HIGH | Halborn | UNABLE TO CLAIM PAYOUTS |
| [o175] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-degis-scprotection-smart-contract-security-audit-report-halborn-pdf.md | MEDIUM | Halborn | ANYONE CAN DEPLOY COVER RIGHT TOKENS |
| [o176] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-degis-scprotection-smart-contract-security-audit-report-halborn-pdf.md | MEDIUM | Halborn | CRTOKENS MAY BE MINTED/BURNED ARBITRARILY IF POLICY CENTER IS NOT SET |
| [o177] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-degis-scprotection-smart-contract-security-audit-report-halborn-pdf.md | MEDIUM | Halborn | SAFEREWARDTRANSFER SHOULD CHECK BEFORE/AFTER BALANCE |
| [o178] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-easyfi-access-vesting-smart-contract-security-audit-halborn-v1-1-pdf.md | MEDIUM | Halborn | TOKENVESTING CONTRACT OUTDATED |
| [o182] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-fortunafi-tokenized-asset-protocol-tap-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | GRIEFING ATTACK |
| [o183] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-gmbl-computer-gmbl-contracts-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | USERS ARE NOT ABLE TO ALLOCATE CONVERTED TOKENS |
| [o184] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-haqq-social-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | VERIFIER DATA CANNOT BE FULLY DELETED |
| [o185] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-highstreetmarket-producttoken-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | PRODUCTTOKENHIGHBASE CONTRACT IS VULNERABLE TO SANDWICH ATTACKS |
| [o186] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-highstreetmarket-staking-smart-contract-security-audit-report-halborn-final-pdf.md | CRITICAL | Halborn | DENIAL OF SERVICE CAUSED BY NONREENTRANT MODIFIER |
| [o187] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-highstreetmarket-staking-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | SUBVAULTREWARDS ARE NOT UPDATED CORRECTLY WHEN CALLING PROCESSREWARDS |
| [o188] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-ithacaprotocol-io-evm-contracts-smart-contract-security-assessment-report-halborn-final-pdf.md | HIGH | Halborn | UNCLAIMED YIELD IS LOST DURING WITHDRAWALS |
| [o189] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-ithacaprotocol-io-evm-contracts-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | APPROVE IS INCOMPATIBLE WITH NON-STANDARD ERC20 TOKENS |
| [o190] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-ksm-starter-smart-contract-security-audit-report-halborn-v1-1-pdf.md | MEDIUM | Halborn | MISSING RE-ENTRANCY PROTECTION |
| [o191] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-ksm-starter-smart-contract-security-audit-report-halborn-v1-1-pdf.md | MEDIUM | Halborn | UNCHECKED TRANSFER |
| [o192] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-kwikswap-factory-contract-smart-contract-security-audit-halborn-v1-1-pdf.md | MEDIUM | Halborn | UNCHECKED TRANSFER |
| [o193] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-lybra-finance-vault-guardian-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | LATESTROUNDDATA CALL MAY RETURN STALE RESULTS |
| [o198] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-matrixswap-dex-aggregator-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | INCOMPATIBILITY WITH NON-STANDARD ERC20 TOKENS |
| [o199] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-matrixswap-dex-aggregator-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | UNCHECKED TRANSFER |
| [o200] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-metapool-eth-staking-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | MINIMUM DEPOSIT RESTRICTION CAN BE BYPASSED |
| [o201] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-money-mates-smart-contract-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | MISSING SLIPPAGE CONTROL |
| [o202] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-money-mates-smart-contract-security-assessment-report-halborn-final-pdf.md | HIGH | Halborn | REFFEE iS MISSING FROM PAYMENT CHECK |
| [o203] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-money-mates-smart-contract-security-assessment-report-halborn-final-pdf.md | HIGH | Halborn | REFFEE IS NOT DEDUCTED FROM SELLPRICE |
| [o204] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-money-mates-smart-contract-security-assessment-report-halborn-final-pdf.md | HIGH | Halborn | OVERPAYMENT IS NOT TRANSFERRED BACK TO BUYERS |
| [o205] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-money-mates-smart-contract-security-assessment-report-halborn-final-pdf.md | HIGH | Halborn | DENIAL OF SERVICE |
| [o206] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-moonwell-finance-contracts-v2-smart-contract-security-assessment-report-halborn-final-pdf.md | HIGH | Halborn | SILENT FAILURE DURING TOKEN MINTING ON THE ROUTER CONTRACT |
| [o207] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-moonwell-finance-contracts-v2-smart-contract-security-assessment-report-halborn-final-pdf.md | HIGH | Halborn | SILENT FAILURE DURING TOKEN REDEMPTION ON THE ROUTER CONTRACT |
| [o208] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-moonwell-finance-contracts-v2-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | MINT WITH PERMIT CAN BE BROKEN WHEN USING TOKENS THAT DO NOT FOLLOW THE ERC2612 STANDARD |
| [o209] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-moonwell-finance-governance-and-timelock-updates-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | TIMELOCK DELAY IS SET TO ZERO IN THE CONSTRUCTOR |
| [o210] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-moonwell-finance-governance-dynamic-quorum-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | MISSING QUORUM CAP COMPARISON CAN BREAK THE GOVERNANCE |
| [o211] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-moonwell-finance-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | ALLOWING ERC777-KIND TOKENS ON PROTOCOL LEADS RE-ENTRANCY |
| [o212] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-moonwell-finance-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | USE OF DEPRECATED CHAINLINK API |
| [o213] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-moonwell-finance-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | ASSETS MAY LOCKED DOWN ON GOVERNORALPHA CONTRACT |
| [o214] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-moonwell-finance-token-sale-and-comptroller-updates-report-halborn-final-pdf.md | MEDIUM | Halborn | OLD TOKENS ARE NOT RECOVERABLE WHEN THE NEW TOKEN IS SET |
| [o215] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-moonwell-finance-token-sale-and-comptroller-updates-report-halborn-final-pdf.md | MEDIUM | Halborn | EXPIRED TOKENS ARE NOT CONSIDERED IN THE VOTING POWER |
| [o216] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-moonwell-finance-xwell-token-rate-limiting-smart-contract-security-assessment-report-halborn-final-pdf.md | HIGH | Halborn | MISSING ERC20PERMIT INIT CALL IN INITIALIZE FUNCTION OF CONTRACT XWELL |
| [o217] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-nexa-cat-erc-standards-smart-contract-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | UNSAFE HANDLING OF ERC20 TRANSFER RESULTS |
| [o218] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-nexa-cat-erc-standards-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | INCOMPATIBILITY WITH TRANSFER-ON-FEE OR DEFLATIONARY TOKENS |
| [o219] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-nftfi-bundles-airdrop-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | BUNDLES INSIDE IMMUTABLEBUNDLES CONTRACT CAN BE EXTRACTED |
| [o220] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-nftfi-bundles-airdrop-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | MISTAKENLY SENT BUNDLE TOKENS CAN NOT BE RESCUED |
| [o221] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-nftfi-native-punk-wrapper-smart-contract-security-audit-report-halborn-final-pdf.md | CRITICAL | Halborn | AIRDROP RECEIVER FUNCTIONALITY DENIED |
| [o222] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-ocean-protocol-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | MINT ATTACK AFTER NFT TRANSFER |
| [o223] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-ocean-protocol-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | MINT ATTACK WITH WORTHLESS TOKEN |
| [o224] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-ocean-protocol-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | UNCHECKED TRANSFER |
| [o225] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-oceanprotocol-priority-h2o-system-action-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | USE LATESTROUNDDATA INSTEAD OF LATESTANSWER TO RUN MORE VALIDATIONS |
| [o226] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-oceanprotocol-priority-h2o-system-action-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | UNCHECKED TRANSFER |
| [o227] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-oceanprotocol-priority-h2o-system-action-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | MISSING RE-ENTRANCY PROTECTION |
| [o228] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-oh-finance-smart-contract-security-audit-report-halborn-v1-1-pdf.md | MEDIUM | Halborn | USE OF TX.ORIGIN |
| [o232] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-planet-finance-smart-contract-security-audit-halborn-v1-1-pdf.md | MEDIUM | Halborn | TRANSFERRED AMOUNT VERIFICATION MISSING |
| [o233] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-playground-labs-kapital-dao-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | PROPOSAL LACKS MULTIPLE IMPORTANT LOGIC CHECKS |
| [o234] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-polkadex-smartcontract-halborn-report-v1-1-pdf.md | HIGH | Halborn | USE OF SELFDESTRUCT FUNCTION |
| [o235] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-polkadex-smartcontract-halborn-report-v1-1-pdf.md | MEDIUM | Halborn | NO TEST COVERAGE |
| [o236] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-portal-gate-project-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | INCORRECT isERC20 CHECK IN zapInEth FUNCTION CAUSES INACCURATE TOKEN VALIDATION |
| [o237] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-primex-protocol-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | NON-STANDARD ERC20 TOKENS WILL REVERT |
| [o238] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-primex-protocol-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | RELAX STRICT CONDITIONS ON SWAPS WITHOUT DEBT |
| [o239] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-primex-protocol-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | CHAINLINK latestRoundData MIGHT RETURN INCORRECT RESULTS |
| [o247] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-seascape-block-lords-import-export-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | UNUSABLE CONTRACT |
| [o248] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-seascape-mini-miners-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | SIGNATURE NONCES ARE IMPLEMENTED INCORRECTLY |
| [o249] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-seascape-moonscape-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | SIGNATURE NONCES ARE IMPLEMENTED INCORRECTLY |
| [o250] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-seascape-moonscape-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | MISSING SIGNATURE VERIFICATION |
| [o251] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-seascape-moonscape-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | MINTERS CANT BE UNSET |
| [o252] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-seascape-mscp-token-vesting-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | INVESTOR MULTI-WITHDRAW IF ADDED AGAIN |
| [o253] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-seascape-ninja-spin-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | CONTRACT DOES NOT ALLOW MINTING NFT WITH THE ID 0 |
| [o254] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-seneca-senecadefi-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | USE OF APPROVE METHOD TO DIRECTLY APPROVE MAX AMOUNT |
| [o255] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-spherium-hyperswap-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | UNCHECKED TRANSFER |
| [o256] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-substance-exchange-exchange-v1-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | CHAINLINK LATESTROUNDDATA MIGHT BE STALE OR INCORRECT |
| [o257] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-substance-exchange-exchange-v1-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | MISSING CHAINLINK ARBITRUM SEQUENCER HEALTH CHECK |
| [o258] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-substance-exchange-exchange-v4-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | ORDERS CAN GET STUCK IN CANCELLED STATE DUE TO MISSING DEADLINE CHECK |
| [o259] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-substance-exchange-exchange-v4-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | GAS STIPEND IN USERWITHDRAWETH FUNCTION AFFECTING GNOSIS SAFE INTERACTIONS |
| [o260] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-substance-exchange-exchange-v4-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | INCOMPATIBILITY WITH REBASING/DEFLATIONARY/INFLATIONARY TOKENS |
| [o261] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-substance-exchange-exchange-v4-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | NON-STANDARD ERC20 TOKENS WILL REVERT |
| [o262] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-tenet-vetenet-smart-contract-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | OVER-DISTRIBUTION ON KILLED GAUGES |
| [o263] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-tenet-vetenet-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | MISSING VALIDATION IN INITIALIZE FUNCTION |
| [o264] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-uranium3o8-erc20-token-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | INVALID ALLOWANCE CHECK IN BURNBYMINTER |
| [o265] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-uranium3o8-erc20-token-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | DUPLCATE MINTERS ALLOWED |
| [o266] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-uranium3o8-erc20-token-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | CENTRALIZATION RISK: MINTERS CAN BURN FROM ANYONE |
| [o268] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-xfai-dex-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | ADDLIQUIDITYETH MISHANDLES DEPOSIT |
| [o269] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-yieldly-finance-polygon-nft-marketplace-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | UNRESTRICTED TOKEN MINTING |
| [o270] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-zetachain-zetanode-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | HAL01 - RECEIVE FUNCTION IS NOT RESTRICTED TO WETH |
| [o271] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-zetachain-zetanode-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | HAL02 - FEE-ON-TRANSFER DEFLATIONARY TOKENS ARE NOT SUPPORTED |
| [o272] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-zetachain-zetanode-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | HAL03 - ABSENCE OF SAFETRANSFER/SAFETRANSFERFROM IN TOKEN TRANSFERS |
| [o273] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-zetachain-zetanode-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | HAL04 - ZRC20 LACKS RESISTANCE TO ERC20 RACE CONDITION ISSUE |
| [o274] | reports/other-l1_findings/publicreports-web-pentest-dtrade-frontend-pentest-executive-summary-report-halborn-v1-1-pdf.md | MEDIUM | Halborn | ASSESSMENT SUMMARY & FINDINGS OVERVIEW 9 EXECUTIVE OVERVIEW SECURITY ANALYSIS RISK LEVEL REMEDIATION DATE (HAL-01) PROPOSALS GET API DENIAL OF SERVICE |
| [o275] | reports/other-l1_findings/publicreports-web-pentest-haqq-backend-webapp-pentest-report-halborn-final-update-pdf.md | MEDIUM | Halborn | POTENTIAL DENIAL OF SERVICE |
| [o276] | reports/other-l1_findings/publicreports-web-pentest-haqq-backend-webapp-pentest-report-halborn-final-update-pdf.md | MEDIUM | Halborn | LACK OF RATE LIMITING IN API ENDPOINTS |
| [o277] | reports/other-l1_findings/publicreports-web-pentest-haqq-backend-webapp-pentest-report-halborn-final-update-pdf.md | MEDIUM | Halborn | DOCKER COMPOSE ENVIRONMENT VARIABLE MISCONFIGURATION |
| [o278] | reports/other-l1_findings/publicreports-web-pentest-haqq-backend-webapp-pentest-report-halborn-final-update-pdf.md | MEDIUM | Halborn | OUTDATED VERSIONS OF TLS SUPPORTED |
| [o279] | reports/other-l1_findings/publicreports-web-pentest-haqq-backend-webapp-pentest-report-halborn-final-update-pdf.md | MEDIUM | Halborn | CACHEABLE HTTPS RESPONSE |
| [o280] | reports/other-l1_findings/publicreports-web-pentest-hbarsuite-webapp-smartnode-frontend-backend-pentest-report-halborn-final-pdf.md | CRITICAL | Halborn | DENIAL OF SERVICE AFFECTING SMART NODES |
| [o281] | reports/other-l1_findings/publicreports-web-pentest-hbarsuite-webapp-smartnode-frontend-backend-pentest-report-halborn-final-pdf.md | CRITICAL | Halborn | LACK OF NFT CREATION WHEN ADDING LIQUIDITY TO A POOL |
| [o282] | reports/other-l1_findings/publicreports-web-pentest-hbarsuite-webapp-smartnode-frontend-backend-pentest-report-halborn-final-pdf.md | MEDIUM | Halborn | HTML INJECTION |
| [o283] | reports/other-l1_findings/publicreports-web-pentest-playground-labs-kapital-dao-guild-service-browser-extension-pentest-report-halborn-final-pdf.md | HIGH | Halborn | UNCHECKED ORIGIN IN POSTMESSAGE |
| [o284] | reports/other-l1_findings/publicreports-web-pentest-prime-trader-backend-whitebox-webapp-pentest-report-halborn-final-pdf.md | HIGH | Halborn | WEAK JWT TOKEN SECRET |
| [o285] | reports/other-l1_findings/publicreports-web-pentest-prime-trader-backend-whitebox-webapp-pentest-report-halborn-final-pdf.md | HIGH | Halborn | UNAUTHORIZED SPAM VIA TOKENS TRANSFER FUNCTIONALITY |
| [o286] | reports/other-l1_findings/publicreports-web-pentest-prime-trader-backend-whitebox-webapp-pentest-report-halborn-final-pdf.md | MEDIUM | Halborn | UNFILTERED PARAMETERS |
| [o287] | reports/other-l1_findings/publicreports-web-pentest-prime-trader-backend-whitebox-webapp-pentest-report-halborn-final-pdf.md | MEDIUM | Halborn | CLEARTEXT COMMUNICATION ALLOWED |
| [o288] | reports/other-l1_findings/publicreports-web-pentest-prime-trader-backend-whitebox-webapp-pentest-report-halborn-final-pdf.md | MEDIUM | Halborn | INSECURE CREDENTIALS DURING DEPLOYMENT |
| [o289] | reports/other-l1_findings/publicreports-web-pentest-rarimo-snap-app-webapp-pentest-report-halborn-final-pdf.md | MEDIUM | Halborn | POTENTIAL SAVE OF ARBITRARY CREDENTIALS |
| [o290] | reports/other-l1_findings/publicreports-web-pentest-rarimo-snap-app-webapp-pentest-report-halborn-final-pdf.md | MEDIUM | Halborn | POTENTIAL GENERATION OF ARBITRARY PROOFS |
| [o291] | reports/other-l1_findings/publicreports-web-pentest-seascape-minigames-web-pentest-report-halborn-final-pdf.md | CRITICAL | Halborn | WEAK CMS PASSWORD |
| [o292] | reports/other-l1_findings/publicreports-web-pentest-seascape-minigames-web-pentest-report-halborn-final-pdf.md | MEDIUM | Halborn | SENSITIVE INFORMATION DISCLOSURE VIA VERBOSE ERROR MESSAGES |
| [o293] | reports/other-l1_findings/publicreports-web-pentest-seascape-minigames-web-pentest-report-halborn-final-pdf.md | MEDIUM | Halborn | OUTDATED THINKPHP VERSION |
| [o294] | reports/other-l1_findings/publicreports-web-pentest-seascape-minigames-web-pentest-report-halborn-final-pdf.md | MEDIUM | Halborn | USE OF PACKAGES WITH KNOWN VULNERABILITIES |
| [o295] | reports/other-l1_findings/publicreports-web-pentest-seascape-nft-marketplace-webapp-pentest-report-halborn-final-pdf.md | MEDIUM | Halborn | USE OF PACKAGES WITH KNOWN VULNERABILITIES |
| [o296] | reports/other-l1_findings/publicreports-zk-audits-matterlabs-zksync-era-circuits-zero-knowledge-security-audit-report-halborn-final-pdf.md | CRITICAL | Halborn | CIRCUIT NOT PROPERLY WORKING WHEN USING SHARD ID > 0 |
| [q297] | reports/other-l1_findings/audit-reports-asteroid-bridge-2024-06-17-audit-report-asteroid-bridge-v1-0-pdf.md | LOW | Oak Security | Unbounded nested iterations in verify_signature could run out of gas |
| [q298] | reports/other-l1_findings/audit-reports-asteroid-bridge-2024-06-17-audit-report-asteroid-bridge-v1-0-pdf.md | LOW | Oak Security | Disabling tokens can lead to inconsistent contract state |
| [q299] | reports/other-l1_findings/audit-reports-asteroid-bridge-2024-06-17-audit-report-asteroid-bridge-v1-0-pdf.md | LOW | Oak Security | IBC fee excess is accumulated and stuck in the contract |
| [q300] | reports/other-l1_findings/audit-reports-asteroid-bridge-2024-06-17-audit-report-asteroid-bridge-v1-0-pdf.md | LOW | Oak Security | Lack of validation for the IBC channel |
| [q301] | reports/other-l1_findings/audit-reports-asteroid-bridge-2024-06-17-audit-report-asteroid-bridge-v1-0-pdf.md | INFO | Oak Security | "Migrate only if newer" pattern is not followed |
| [q302] | reports/other-l1_findings/audit-reports-asteroid-bridge-2024-06-17-audit-report-asteroid-bridge-v1-0-pdf.md | INFO | Oak Security | Lack of validation when disabling a token may mislead users |
| [q303] | reports/other-l1_findings/audit-reports-asteroid-bridge-2024-06-17-audit-report-asteroid-bridge-v1-0-pdf.md | INFO | Oak Security | Sorting of signatures is inefficient |
| [q304] | reports/other-l1_findings/audit-reports-asteroid-bridge-2024-06-17-audit-report-asteroid-bridge-v1-0-pdf.md | INFO | Oak Security | Miscellaneous comments |
| [q305] | reports/other-l1_findings/audit-reports-celer-2022-05-14-audit-report-celer-cbridge-flow-v1-0-pdf.md | LOW | Oak Security | Unbounded dictionary records might cause denial of service |
| [q306] | reports/other-l1_findings/audit-reports-celer-2022-05-14-audit-report-celer-cbridge-flow-v1-0-pdf.md | LOW | Oak Security | Adding delay transfer should not be allowed when the contract is paused |
| [q307] | reports/other-l1_findings/audit-reports-celer-2022-05-14-audit-report-celer-cbridge-flow-v1-0-pdf.md | LOW | Oak Security | Missing logic validations during struct initialization might cause temporary denial of service |
| [q308] | reports/other-l1_findings/audit-reports-celer-2022-05-14-audit-report-celer-cbridge-flow-v1-0-pdf.md | LOW | Oak Security | Sensitive resources can easily be shared and not revoked |
| [q309] | reports/other-l1_findings/audit-reports-celer-2022-05-14-audit-report-celer-cbridge-flow-v1-0-pdf.md | LOW | Oak Security | Misconfiguration of chain identifier values might lead to replay attack possibility |
| [q310] | reports/other-l1_findings/audit-reports-celer-2022-05-14-audit-report-celer-cbridge-flow-v1-0-pdf.md | LOW | Oak Security | Token receiving capability may not exist  which leads to failure of deposits |
| [q311] | reports/other-l1_findings/audit-reports-celer-2022-05-14-audit-report-celer-cbridge-flow-v1-0-pdf.md | INFO | Oak Security | Delay threshold check should use greater than or equal symbol |
| [q312] | reports/other-l1_findings/audit-reports-helix-bridge-2024-07-04-audit-report-helix-bridge-v1-0-pdf.md | LOW | Oak Security | Transfers can still be initiated when a token is removed |
| [q313] | reports/other-l1_findings/audit-reports-helix-bridge-2024-07-04-audit-report-helix-bridge-v1-0-pdf.md | LOW | Oak Security | Centralization risks |
| [q314] | reports/other-l1_findings/audit-reports-helix-bridge-2024-07-04-audit-report-helix-bridge-v1-0-pdf.md | LOW | Oak Security | Irrecoverable Blast points |
| [q315] | reports/other-l1_findings/audit-reports-helix-bridge-2024-07-04-audit-report-helix-bridge-v1-0-pdf.md | LOW | Oak Security | Anybody can request to withdraw providers liquidity |
| [q316] | reports/other-l1_findings/audit-reports-helix-bridge-2024-07-04-audit-report-helix-bridge-v1-0-pdf.md | LOW | Oak Security | Input validation could be improved |
| [q317] | reports/other-l1_findings/audit-reports-helix-bridge-2024-07-04-audit-report-helix-bridge-v1-0-pdf.md | LOW | Oak Security | Incorrect accounting on fee-on-transfer/deflationary tokens |
| [q318] | reports/other-l1_findings/audit-reports-helix-bridge-2024-07-04-audit-report-helix-bridge-v1-0-pdf.md | INFO | Oak Security | Withdrawing all protocol fees is not possible |
| [q319] | reports/other-l1_findings/audit-reports-helix-bridge-2024-07-04-audit-report-helix-bridge-v1-0-pdf.md | INFO | Oak Security | The contract locks up ETH received |
| [q320] | reports/other-l1_findings/audit-reports-helix-bridge-2024-07-04-audit-report-helix-bridge-v1-0-pdf.md | INFO | Oak Security | Miscellaneous |
| [q321] | reports/other-l1_findings/audit-reports-helix-bridge-2024-07-04-audit-report-helix-xtoken-v1-0-pdf.md | LOW | Oak Security | Undelivered transfers require fee to be refunded |
| [q322] | reports/other-l1_findings/audit-reports-helix-bridge-2024-07-04-audit-report-helix-xtoken-v1-0-pdf.md | LOW | Oak Security | Centralization risks |
| [q323] | reports/other-l1_findings/audit-reports-helix-bridge-2024-07-04-audit-report-helix-xtoken-v1-0-pdf.md | LOW | Oak Security | Input validation could be improved |
| [q324] | reports/other-l1_findings/audit-reports-helix-bridge-2024-07-04-audit-report-helix-xtoken-v1-0-pdf.md | INFO | Oak Security | The contract locks up ETH received |
| [q325] | reports/other-l1_findings/audit-reports-helix-bridge-2024-07-04-audit-report-helix-xtoken-v1-0-pdf.md | INFO | Oak Security | Redundant logic in the updateXToken function when approving xToken |
| [q326] | reports/other-l1_findings/audit-reports-helix-bridge-2024-07-04-audit-report-helix-xtoken-v1-0-pdf.md | INFO | Oak Security | Excessive storage usage in XTokenBacking contract |
| [q327] | reports/other-l1_findings/audit-reports-helix-bridge-2024-07-04-audit-report-helix-xtoken-v1-0-pdf.md | INFO | Oak Security | Transfer state mappings could be streamlined |
| [q328] | reports/other-l1_findings/audit-reports-helix-bridge-2024-07-04-audit-report-helix-xtoken-v1-0-pdf.md | INFO | Oak Security | Miscellaneous |
| [q329] | reports/other-l1_findings/audit-reports-incrementfi-audit-report-incrementfi-liquid-staking-pdf.md | INFO | Oak Security | Supply start index higher than the end index causes collectDelegatorsOnEpochStart to perform empty execution |
| [q330] | reports/other-l1_findings/audit-reports-incrementfi-audit-report-incrementfi-liquid-staking-pdf.md | INFO | Oak Security | initApprovedNodeIDList gas consumption can be reduced |
| [q331] | reports/other-l1_findings/audit-reports-incrementfi-audit-report-incrementfi-liquid-staking-pdf.md | INFO | Oak Security | Distributing tokens to the same node operator yield no difference |
| [q332] | reports/other-l1_findings/audit-reports-incrementfi-audit-report-incrementfi-liquid-staking-pdf.md | INFO | Oak Security | Typographic errors and duplicate comments found in codebase |
| [q333] | reports/other-l1_findings/audit-reports-incrementfi-audit-report-incrementfi-liquid-staking-pdf.md | INFO | Oak Security | Unused events and properties |
| [q334] | reports/other-l1_findings/audit-reports-incrementfi-audit-report-incrementfi-liquid-staking-pdf.md | INFO | Oak Security | Best practices for transactions code |
| [q335] | reports/other-l1_findings/audit-reports-incrementfi-audit-report-incrementfi-liquid-staking-pdf.md | INFO | Oak Security | Error messages are returned with proprietary encoding |
| [q336] | reports/other-l1_findings/audit-reports-structured-2025-11-25-audit-report-structured-erc20-converter-eth-wrapper-maxbtc-erc20-for-eureka-bridge-v1-0-pdf.md | LOW | Oak Security | Centralization concerns |
| [q337] | reports/other-l1_findings/audit-reports-structured-2025-11-25-audit-report-structured-erc20-converter-eth-wrapper-maxbtc-erc20-for-eureka-bridge-v1-0-pdf.md | LOW | Oak Security | Missing minimum output parameter enabling slippage exploitation |
| [q338] | reports/other-l1_findings/audit-reports-structured-2025-11-25-audit-report-structured-erc20-converter-eth-wrapper-maxbtc-erc20-for-eureka-bridge-v1-0-pdf.md | LOW | Oak Security | Missing validation allowing zero exchange rate and identical asset pair configuration |
| [q339] | reports/other-l1_findings/audit-reports-structured-2025-11-25-audit-report-structured-erc20-converter-eth-wrapper-maxbtc-erc20-for-eureka-bridge-v1-0-pdf.md | INFO | Oak Security | No event emission for critical configuration updates |
| [q340] | reports/other-l1_findings/audit-reports-structured-2025-11-25-audit-report-structured-erc20-converter-eth-wrapper-maxbtc-erc20-for-eureka-bridge-v1-0-pdf.md | INFO | Oak Security | IWETH interface transfer signature mismatches WETH9 contract |
| [q341] | reports/other-l1_findings/audit-reports-structured-2025-11-25-audit-report-structured-erc20-converter-eth-wrapper-maxbtc-erc20-for-eureka-bridge-v1-0-pdf.md | INFO | Oak Security | Superfluous recoverEther function because the contract cannot receive ETH |
| [q342] | reports/other-l1_findings/audit-reports-structured-2025-11-25-audit-report-structured-erc20-converter-eth-wrapper-maxbtc-erc20-for-eureka-bridge-v1-0-pdf.md | INFO | Oak Security | Missing zero address validations |
| [q343] | reports/other-l1_findings/audit-reports-structured-2025-11-25-audit-report-structured-erc20-converter-eth-wrapper-maxbtc-erc20-for-eureka-bridge-v1-0-pdf.md | INFO | Oak Security | Miscellaneous comments |
| [q344] | reports/other-l1_findings/optimism-docs-security-reviews-2026-03-policyenginestaking-cantina-pdf.md | LOW | auditor | Findings 3.1 Low Risk 3.1.1 Pause bypass through allowlist mutation |
| [q345] | reports/other-l1_findings/optimism-docs-security-reviews-2026-03-policyenginestaking-cantina-pdf.md | INFO | auditor | Cantina Managed: Fix verified. 4 3.2 Informational 3.2.1 ChangeBeneficiary reverts on same beneficiary despite no-op specification |
| [q346] | reports/other-l1_findings/optimism-docs-security-reviews-2026-03-policyenginestaking-cantina-pdf.md | INFO | auditor | Optimism: Fixed by updating the Spec documentation. Cantina Managed: Fix verified. 3.2.3 Pause behavior mismatch for changeBeneficiary |
| [q347] | reports/other-l1_findings/optimism-docs-security-reviews-2026-03-policyenginestaking-cantina-pdf.md | INFO | auditor | Optimism: Fixed by updating the Spec documentation. 6 Cantina Managed: Fix verified. 3.2.6 Unnecessary lastUpdate reset in _decreasePeData |
| [q348] | reports/other-l1_findings/optimism-docs-security-reviews-2026-03-policyenginestaking-cantina-pdf.md | INFO | auditor | Cantina Managed: Fix verified. 3.2.8 PolicyEngineStaking does not inherit IPolicyEngineStaking |
| [q349] | reports/other-l1_findings/public-audits-reports-near-review-pdf.md | LOW | NCC Group | Compiles Smart Contracts Using An Unsafe Solidity Version Asset hardhat-config.js andtruffle-config.js Status Resolved: See Resolution Rating |
| [q350] | reports/other-l1_findings/publications-audit-reports-peckshield-audit-report-celer-multibridge-v1-0-pdf.md | LOW | PeckShield | Audit Report #: 2023-029 Public 3   Detailed Results 3.1 Suggested Adherence Of Checks-Effects-Interactions Pattern • ID: PVE-001 • |
| [q351] | reports/other-l1_findings/publications-audit-reports-peckshield-audit-report-celer-multibridge-v1-0-pdf.md | INFO | PeckShield | Status This issue has been fixed in the following commit:73001ed. 3.2 Meaningful Events For Important State Changes • ID: PVE-002 • |
| [q352] | reports/other-l1_findings/publications-audit-reports-peckshield-audit-report-convex-frax-staking-v1-0-pdf.md | LOW | PeckShield | PeckShield Audit Report #: 2022-145 Public 3   Detailed Results 3.1 T ype Inconsistency Of IVoteEscrow::locked() • ID: PVE-001 • |
| [q353] | reports/other-l1_findings/publications-audit-reports-peckshield-audit-report-convex-frax-staking-v1-0-pdf.md | LOW | PeckShield | Status The issue has been confirmed by the team. 3.2 Accommodation Of Non-ERC20-Compliant T okens • ID: PVE-002 • |
| [q354] | reports/other-l1_findings/publications-audit-reports-peckshield-audit-report-convex-frax-staking-v1-0-pdf.md | INFO | PeckShield | The issue has been addressed by the following commits:263f096 and cc62dfa. 3.3 Meaningful Events For Important State Changes • ID: PVE-003 • |
| [q355] | reports/other-l1_findings/publications-audit-reports-peckshield-audit-report-convex-frax-staking-v1-0-pdf.md | LOW | PeckShield | PeckShield Audit Report #: 2022-145 Public 3.4 Revisited Reentrancy Protection In Current Implementation • ID: PVE-004 • |
| [q356] | reports/other-l1_findings/publications-audit-reports-peckshield-audit-report-gains-staking-v1-0-pdf.md | LOW | PeckShield | Suggested Immutable Storage State When Assigned Only in Constructor • ID: PVE-002 • |
| [q357] | reports/other-l1_findings/publications-audit-reports-peckshield-audit-report-xterio-staking-v1-0-pdf.md | INFO | PeckShield | PeckShield Audit Report #: 2024-297 Public 3   Detailed Results 3.1 Suggested Immutable States If Only Set at Constructor • ID: PVE-001 • |
| [q358] | reports/other-l1_findings/publications-chainflip-solana-zellic-audit-report-pdf.md | INFO | Zellic | Size calculation for program accounts |
| [q359] | reports/other-l1_findings/publications-chainflip-solana-zellic-audit-report-pdf.md | INFO | Zellic | Potential seed collision |
| [q360] | reports/other-l1_findings/publications-chainflip-solana-zellic-audit-report-pdf.md | INFO | Zellic | The CloseEventAccounts event emitted without validating event account |
| [q361] | reports/other-l1_findings/publications-examplestring-passing-solana-oapp-zellic-audit-report-pdf.md | LOW | Zellic | Initialization can be front-run |
| [q362] | reports/other-l1_findings/publications-examplestring-passing-solana-oapp-zellic-audit-report-pdf.md | LOW | Zellic | Ambiguous state initialization |
| [q363] | reports/other-l1_findings/publications-facet-bridge-zellic-audit-report-pdf.md | INFO | Zellic | Deploy script uses incorrect cast subcommand |
| [q364] | reports/other-l1_findings/publications-gotsui-zellic-audit-report-pdf.md | LOW | Zellic | Zellic 7 MystenLabsLtd. 3 DetailedFindings 3.1 Denialofservice • Target:app/callback/page.tsx • Category:CodingMistakes • Likelihood:High • |
| [q365] | reports/other-l1_findings/publications-reviews-2023-02-solana-token-2022-program-securityreview-pdf.md | INFO | Trail of Bits | Ok returned for malformed extension data |
| [q366] | reports/other-l1_findings/publications-reviews-2023-02-solana-token-2022-program-securityreview-pdf.md | INFO | Trail of Bits | Large extension sizes can cause panics |
| [q367] | reports/other-l1_findings/publications-reviews-2023-02-solana-token-2022-program-securityreview-pdf.md | INFO | Trail of Bits | Unexpected function behavior |
| [q368] | reports/other-l1_findings/publications-reviews-2023-02-solana-token-2022-program-securityreview-pdf.md | INFO | Trail of Bits | Iteration over empty data |
| [q369] | reports/other-l1_findings/publications-reviews-2023-02-solana-token-2022-program-securityreview-pdf.md | LOW | Trail of Bits | Missing check in UpdateMint instruction could result in inoperable mints |
| [q370] | reports/other-l1_findings/publications-reviews-2023-02-solana-token-2022-program-securityreview-pdf.md | INFO | Trail of Bits | Incorrect test data description |
| [q371] | reports/other-l1_findings/publications-reviews-2023-02-solana-token-2022-program-securityreview-pdf.md | INFO | Trail of Bits | The Transfer and TransferWithFee instructions are identical |
| [q372] | reports/other-l1_findings/publications-reviews-2023-02-solana-token-2022-program-securityreview-pdf.md | INFO | Trail of Bits | Instruction susceptible to front-running |
| [q373] | reports/other-l1_findings/publications-reviews-2023-09-solana-solang-parser-semantic-analysis-securityreview-pdf.md | INFO | Trail of Bits | Reliance on deprecated/unmaintained dependencies |
| [q374] | reports/other-l1_findings/publications-reviews-2023-09-solana-solang-parser-semantic-analysis-securityreview-pdf.md | INFO | Trail of Bits | Reliance on outdated dependencies |
| [q375] | reports/other-l1_findings/publications-reviews-2023-09-solana-solang-parser-semantic-analysis-securityreview-pdf.md | INFO | Trail of Bits | Insufficient linter use |
| [q376] | reports/other-l1_findings/publications-reviews-2023-09-solana-solang-parser-semantic-analysis-securityreview-pdf.md | INFO | Trail of Bits | Rational evaluation code always returns errors |
| [q377] | reports/other-l1_findings/publications-reviews-2023-09-solana-solang-parser-semantic-analysis-securityreview-pdf.md | INFO | Trail of Bits | Code duplication |
| [q378] | reports/other-l1_findings/publications-reviews-2023-09-solana-solang-parser-semantic-analysis-securityreview-pdf.md | LOW | Trail of Bits | Risk of arithmetic underflow in lexer |
| [q379] | reports/other-l1_findings/publications-reviews-2023-09-solana-solang-parser-semantic-analysis-securityreview-pdf.md | INFO | Trail of Bits | Excessive use of allow for lalrpop-generated code |
| [q380] | reports/other-l1_findings/publications-reviews-2023-09-solana-solang-parser-semantic-analysis-securityreview-pdf.md | INFO | Trail of Bits | No explicit tests for operator precedence |
| [q381] | reports/other-l1_findings/publications-reviews-2024-04-offchain-l1-l3-teleporter-securityreview-pdf.md | INFO | Trail of Bits | The _setupRole function is deprecated |
| [q382] | reports/other-l1_findings/publications-reviews-2024-04-offchain-l1-l3-teleporter-securityreview-pdf.md | INFO | Trail of Bits | Vacuous unit tests |
| [q383] | reports/other-l1_findings/publications-reviews-2024-04-offchain-l1-l3-teleporter-securityreview-pdf.md | INFO | Trail of Bits | Suggested refactorings to make precedence explicit and simplify code |
| [q384] | reports/other-l1_findings/publications-reviews-2024-04-offchain-l1-l3-teleporter-securityreview-pdf.md | INFO | Trail of Bits | Undocumented struct fields |
| [q385] | reports/other-l1_findings/publications-reviews-2024-04-offchain-l1-l3-teleporter-securityreview-pdf.md | INFO | Trail of Bits | Teleport function should document that contract callers should be able to create retryable tickets |
| [q386] | reports/other-l1_findings/publications-reviews-2025-01-beethovenx-sonicstaking-securityreview-pdf.md | LOW | Trail of Bits | Global pause method will fail if a subcomponent is already paused |
| [q387] | reports/other-l1_findings/publications-reviews-2025-01-beethovenx-sonicstaking-securityreview-pdf.md | INFO | Trail of Bits | Risk of read-only reentrancy via Balancer pools |
| [q388] | reports/other-l1_findings/publications-reviews-2025-01-beethovenx-sonicstaking-securityreview-pdf.md | INFO | Trail of Bits | Credentials are persisted in the GitHub CI workflow |
| [q389] | reports/other-l1_findings/publications-reviews-2025-03-offchain-custom-fee-erc20-bridge-securityreview-pdf.md | INFO | Trail of Bits | An invalid upgrade for non-BoLD rollup is possible |
| [q390] | reports/other-l1_findings/publications-reviews-2025-11-edera-container-runtime-securityreview-pdf.md | INFO | Trail of Bits | CreateRequest and AttachRequest validation is bypassed |
| [q391] | reports/other-l1_findings/publications-reviews-2025-11-edera-container-runtime-securityreview-pdf.md | LOW | Trail of Bits | Styrolite can mount to directories outside a target container |
| [q392] | reports/other-l1_findings/publications-reviews-2025-11-edera-container-runtime-securityreview-pdf.md | LOW | Trail of Bits | Styrolite configuration needlessly passes through the filesystem |
| [q393] | reports/other-l1_findings/publications-reviews-2025-11-edera-container-runtime-securityreview-pdf.md | LOW | Trail of Bits | SSRF vulnerability in OCI image authentication |
| [q394] | reports/other-l1_findings/publications-reviews-2025-11-edera-container-runtime-securityreview-pdf.md | INFO | Trail of Bits | OCI connects to Docker hub mirrors starting with "localhost" using HTTP |
| [q395] | reports/other-l1_findings/publications-reviews-2025-11-edera-container-runtime-securityreview-pdf.md | LOW | Trail of Bits | Two-step directory creation vulnerable to race condition |
| [q396] | reports/other-l1_findings/publications-reviews-2025-11-edera-container-runtime-securityreview-pdf.md | INFO | Trail of Bits | Missing call to destroy_map_task |
| [q397] | reports/other-l1_findings/publications-reviews-2025-11-edera-container-runtime-securityreview-pdf.md | LOW | Trail of Bits | Unchecked return values during grant unmapping |
| [q398] | reports/other-l1_findings/publications-reviews-2025-11-edera-container-runtime-securityreview-pdf.md | INFO | Trail of Bits | map_vf can fail silently |
| [q399] | reports/other-l1_findings/publications-reviews-2025-11-edera-container-runtime-securityreview-pdf.md | LOW | Trail of Bits | Unsanitized string-wise mount path concatenation in zone crate |
| [q400] | reports/other-l1_findings/publications-reviews-2025-11-edera-container-runtime-securityreview-pdf.md | INFO | Trail of Bits | is_edera_runtime_class improperly identifies the runtime class |
| [q401] | reports/other-l1_findings/publications-reviews-2025-11-edera-container-runtime-securityreview-pdf.md | LOW | Trail of Bits | Workload configuration written to temp file |
| [q402] | reports/other-l1_findings/publications-reviews-2026-01-nearone-nearintentsteesolverregistryandammsolver-securityreview-pdf.md | INFO | Trail of Bits | Code duplication |
| [q403] | reports/other-l1_findings/publications-reviews-2026-01-nearone-nearintentsteesolverregistryandammsolver-securityreview-pdf.md | INFO | Trail of Bits | Insufficient test coverage |
| [q404] | reports/other-l1_findings/publications-reviews-2026-01-nearone-nearintentsteesolverregistryandammsolver-securityreview-pdf.md | LOW | Trail of Bits | Race condition in create_liquidity_pool |
| [q405] | reports/other-l1_findings/publications-reviews-zcash2-pdf.md | INFO | Trail of Bits | Inflexible build system |
| [q406] | reports/other-l1_findings/publications-reviews-zcash2-pdf.md | INFO | Trail of Bits | ​ ASAN ​ /​ UBSAN ​ errors and ​ cppcheck ​ errors |
| [q407] | reports/other-l1_findings/publications-reviews-zcash2-pdf.md | INFO | Trail of Bits | Lack of fuzzing |
| [q408] | reports/other-l1_findings/publications-springsui-zellic-audit-report-pdf.md | INFO | Zellic | Overpermissive safety check |
| [q409] | reports/other-l1_findings/publicreports-algorand-smart-contract-audit-yieldly-finance-lottery-algorand-smart-contract-halborn-v1-1-pdf.md | LOW | Halborn | LACK OF MULTISIG PROGRAM |
| [q410] | reports/other-l1_findings/publicreports-algorand-smart-contract-audit-yieldly-finance-lottery-algorand-smart-contract-halborn-v1-1-pdf.md | LOW | Halborn | MISSING PROXY ASSET DEFINITION ON THE FUNCTIONS |
| [q411] | reports/other-l1_findings/publicreports-algorand-smart-contract-audit-yieldly-finance-lottery-algorand-smart-contract-halborn-v1-1-pdf.md | INFO | Halborn | MISSING FREEZE/REVOKE ASSETS DEFINITION |
| [q412] | reports/other-l1_findings/publicreports-algorand-smart-contract-audit-yieldly-finance-lottery-algorand-smart-contract-halborn-v1-1-pdf.md | INFO | Halborn | MULTIPLE PRAGMA DEFINITION |
| [q413] | reports/other-l1_findings/publicreports-algorand-smart-contract-audit-yieldly-finance-lottery-algorand-smart-contract-halborn-v1-1-pdf.md | INFO | Halborn | ALERTHUB SETUP |
| [q414] | reports/other-l1_findings/publicreports-near-smart-contract-audits-staderlabs-nearx-staking-reaudit-near-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | USAGE OF VULNERABLE CRATES |
| [q415] | reports/other-l1_findings/publicreports-solana-program-audit-clone-protocol-solana-program-security-assessment-report-halborn-final-pdf.md | LOW | Halborn | MISCALCULATION DURING LIQUIDITY WITHDRAWAL OF THE COMET |
| [q416] | reports/other-l1_findings/publicreports-solana-program-audit-clone-protocol-solana-program-security-assessment-report-halborn-final-pdf.md | LOW | Halborn | LACK OF AUTHORITY CHECK IN INITIALIZE FUNCTION |
| [q417] | reports/other-l1_findings/publicreports-solana-program-audit-clone-protocol-solana-program-security-assessment-report-halborn-final-pdf.md | LOW | Halborn | MISSING SANITY CHECK TO ENSURE THE DEPOSITORY TOKEN MINT DOES NOT MATCH THE DEPOSITING TOKEN MINT |
| [q418] | reports/other-l1_findings/publicreports-solana-program-audit-clone-protocol-solana-program-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | CHECKED ARITHMETIC MISSING |
| [q419] | reports/other-l1_findings/publicreports-solana-program-audit-clone-protocol-solana-program-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | ORACLE CHECKS MISSING |
| [q420] | reports/other-l1_findings/publicreports-solana-program-audit-clone-protocol-solana-program-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | OVERCOLLATERAL RATIOS CHECK MISSING |
| [q421] | reports/other-l1_findings/publicreports-solana-program-audit-clone-protocol-solana-program-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | POTENTIAL DUPLICATION OF AUTHORITIES |
| [q422] | reports/other-l1_findings/publicreports-solana-program-audit-clone-protocol-solana-program-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | ZERO AMOUNT CHECK MISSING |
| [q423] | reports/other-l1_findings/publicreports-solana-program-audit-clone-protocol-solana-program-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | MISSING CARGO OVERFLOW CHECKS |
| [q424] | reports/other-l1_findings/publicreports-solana-program-audit-clone-protocol-solana-program-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | POSSIBLE RUST PANICS DUE TO UNSAFE UNWRAP USAGE |
| [q425] | reports/other-l1_findings/publicreports-solana-program-audit-debridge-solana-contracts-solana-program-security-audit-report-halborn-pdf.md | LOW | Halborn | USAGE OF VULNERABLE CRATES |
| [q426] | reports/other-l1_findings/publicreports-solana-program-audit-debridge-solana-contracts-solana-program-security-audit-report-halborn-pdf.md | INFO | Halborn | MISSING PROPER ERROR HANDLING |
| [q427] | reports/other-l1_findings/publicreports-solana-program-audit-party-parrot-solana-smart-contract-security-audit-report-halborn-v1-1-pdf.md | LOW | Halborn | OUTDATED DEPENDENCY |
| [q428] | reports/other-l1_findings/publicreports-solana-program-audit-party-parrot-solana-smart-contract-security-audit-report-halborn-v1-1-pdf.md | LOW | Halborn | ARITHMETIC ERRORS |
| [q429] | reports/other-l1_findings/publicreports-solana-program-audit-party-parrot-solana-smart-contract-security-audit-report-halborn-v1-1-pdf.md | INFO | Halborn | UNSAFE RUST CODE USAGE |
| [q430] | reports/other-l1_findings/publicreports-solana-program-audit-party-parrot-solana-smart-contract-security-audit-report-halborn-v1-1-pdf.md | INFO | Halborn | LOW TEST COVERAGE |
| [q431] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-21-co-wrapped-assets-smart-contract-security-assessment-report-halborn-final-pdf.md | LOW | Halborn | CURRENT ALLOWANCE CONFIRMATION CAN BE BYPASSED |
| [q432] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-21-co-wrapped-assets-smart-contract-security-assessment-report-halborn-final-pdf.md | LOW | Halborn | THE AUTHORIZATION MODULE DOES NOT FOLLOW SECURITY BEST PRACTICES |
| [q433] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-21-co-wrapped-assets-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | ALLOWANCE CAN BE MODIFIED WHILE CONTRACT IS PAUSED |
| [q434] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-21-co-wrapped-assets-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | FLOATING PRAGMA |
| [q435] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-apy-finance-governance-token-reward-halborn-report-v1-1-pdf.md | LOW | Halborn | ASSESSMENT SUMMARY & FINDINGS OVERVIEW CRITICAL HIGH MEDIUM LOW 0 0 0 1 SECURITY ANALYSIS RISK LEVEL EXPERIMENTAL FEATURES ENABLED |
| [q436] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-apy-finance-smartcontract-halborn-report-v1-pdf.md | LOW | Halborn | ASSESSMENT SUMMARY & FINDINGS OVERVIEW CRITICAL HIGH MEDIUM LOW 0 0 0 2 SECURITY ANALYSIS RISK LEVEL DEPRECATED PRAGMA VERSION OF SOLC |
| [q437] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-aragon-aragonos-v1-3-0-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | MISSING CHECK |
| [q438] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-aragon-aragonos-v1-3-0-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | MISSING CONTRACT CHECK |
| [q439] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-aura-finance-smart-contract-security-audit-report-halborn-final-pdf.md | LOW | Halborn | LACK OF TRANSFEROWNERSHIP PATTERN |
| [q440] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-aura-finance-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | MISTAKENLY SENT ERC20 TOKENS CAN NOT RESCUED IN THE CONTRACTS |
| [q441] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-aura-finance-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | USING POSTFIX OPERATORS IN LOOPS |
| [q442] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-aura-finance-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | ARRAY.LENGTH USED IN LOOP CONDITIONS |
| [q443] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-aura-finance-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | USING != 0 CONSUMES LESS GAS THAN > 0 IN UNSIGNED INTEGER VALIDATION |
| [q444] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-base-protocol-halborn-report-v2-pdf.md | LOW | Halborn | ASSESSMENT SUMMARY & FINDINGS OVERVIEW CRITICAL HIGH MEDIUM LOW 0 0 0 3 SECURITY ANALYSIS RISK LEVEL USE OF TX.ORIGIN Low AVOID USING NOW |
| [q445] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-biconomy-forwarder-smart-contract-solidity-audit-report-halborn-final-pdf.md | INFO | Halborn | ZERO ADDRESS NOT CHECKED |
| [q446] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-biconomy-forwarder-smart-contract-solidity-audit-report-halborn-final-pdf.md | INFO | Halborn | MISSING EVENTS EMITTING |
| [q447] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-bracket-fi-bracketx-smart-contract-security-audit-report-halborn-final-pdf.md | LOW | Halborn | CLAIMED POLICIES CAN BE TRANSFERED |
| [q448] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-bracket-fi-bracketx-smart-contract-security-audit-report-halborn-final-pdf.md | LOW | Halborn | LACK OF DISABLEINITIALIZERS CALL TO PREVENT UNINITIALIZED CONTRACTS |
| [q449] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-bracket-fi-bracketx-smart-contract-security-audit-report-halborn-final-pdf.md | LOW | Halborn | LACK OF PRICE FEED DECIMALS CHECK |
| [q450] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-bracket-fi-bracketx-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | POSTFIX OPERATORS CONSUME MORE GAS THAN PREFIX OPERATORS |
| [q451] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-bracket-fi-bracketx-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | INCREMENTS CAN BE UNCHECKED IN LOOPS |
| [q452] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-bracket-fi-bracketx-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | MISSING ZERO ADDRESS CHECK |
| [q453] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-bracket-fi-channels-and-epochchannels-smart-contract-security-audit-report-halborn-final-pdf.md | LOW | Halborn | ERC-20 TRANSFER IGNORING RETURN VALUE |
| [q454] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-bracket-fi-channels-and-epochchannels-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | CENTRALIZATION RISK |
| [q455] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-bracket-fi-channels-and-epochchannels-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | HARDCODED STATE VARIABLE |
| [q456] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-bracket-fi-channels-and-epochchannels-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | MISSING ZERO ADDRESS CHECK |
| [q457] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-bracket-fi-channels-and-epochchannels-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | FLOATING PRAGMA |
| [q458] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-bware-labs-staking-protocol-smart-contract-security-audit-report-halborn-final-pdf-pdf.md | INFO | Halborn | USE CUSTOM ERRORS TO SAVE GAS |
| [q459] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-bware-labs-staking-protocol-smart-contract-security-audit-report-halborn-final-pdf-pdf.md | INFO | Halborn | INEFFICIENT CONDITION IN THE FINALIZEPOOL INTERNAL FUNCTION |
| [q460] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-centaurswap-smart-contract-security-audit-halborn-v1-1-pdf.md | LOW | Halborn | INFINITE ALLOWANCE |
| [q461] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-centaurswap-smart-contract-security-audit-halborn-v1-1-pdf.md | LOW | Halborn | INTEGER OVERFLOW |
| [q462] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-centaurswap-smart-contract-security-audit-halborn-v1-1-pdf.md | LOW | Halborn | USE OF BLOCK.TIMESTAMP |
| [q463] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-centaurswap-smart-contract-security-audit-halborn-v1-1-pdf.md | LOW | Halborn | FLOATING PRAGMA AND VERSION MISMATCH |
| [q464] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-centaurswap-smart-contract-security-audit-halborn-v1-1-pdf.md | INFO | Halborn | POSSIBLE MISUSE OF PUBLIC FUNCTIONS |
| [q465] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-centaurswap-smart-contract-security-audit-halborn-v1-1-pdf.md | INFO | Halborn | FUNCTION REDEFINITION |
| [q466] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-centaurswap-smart-contract-security-audit-halborn-v1-1-pdf.md | INFO | Halborn | USER CONTROLLED REQUIRE COMPARISON |
| [q467] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-centaurswap-smart-contract-security-audit-halborn-v1-1-pdf.md | INFO | Halborn | MISSING VARIABLE CHECKS |
| [q468] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-debridge-cross-chain-swap-smart-contract-security-audit-report-halborn-pdf.md | INFO | Halborn | SAME PAIR OF TOKENS CAN BE USED |
| [q469] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-debridge-cross-chain-swap-smart-contract-security-audit-report-halborn-pdf.md | INFO | Halborn | MISSING PAUSEABLE FUNCTIONALITY |
| [q470] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-debridge-cross-chain-swap-smart-contract-security-audit-report-halborn-pdf.md | INFO | Halborn | UNUSED RETURN VALUES |
| [q471] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-debridge-cross-chain-swap-smart-contract-security-audit-report-halborn-pdf.md | INFO | Halborn | COGNITIVE COMPLEXITY OF FUNCTION IS TOO HIGH |
| [q472] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-debridge-cross-chain-swap-smart-contract-security-audit-report-halborn-pdf.md | INFO | Halborn | POSSIBLE MISUSE OF PUBLIC FUNCTIONS |
| [q473] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-easyfi-staking-smart-contract-security-audit-halborn-v1-1-pdf.md | LOW | Halborn | PRAGMA VERSION DEPRECATED |
| [q474] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-easyfi-staking-smart-contract-security-audit-halborn-v1-1-pdf.md | LOW | Halborn | FLOATING PRAGMA |
| [q475] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-easyfi-staking-smart-contract-security-audit-halborn-v1-1-pdf.md | INFO | Halborn | MISSING BOUND CHECK |
| [q476] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-easyfi-staking-smart-contract-security-audit-halborn-v1-1-pdf.md | INFO | Halborn | INTEGER OVERFLOW |
| [q477] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-easyfi-staking-smart-contract-security-audit-halborn-v1-1-pdf.md | INFO | Halborn | NO TEST COVERAGE |
| [q478] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-easyfi-staking-smart-contract-security-audit-halborn-v1-1-pdf.md | INFO | Halborn | DOCUMENTATION |
| [q479] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-egl-eglcontract-smart-contract-security-audit-halborn-v1-1-pdf.md | LOW | Halborn | DIVIDE BEFORE MULTIPLY |
| [q480] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-egl-eglcontract-smart-contract-security-audit-halborn-v1-1-pdf.md | LOW | Halborn | LACK OF MULTIPLE VOTING CHECK |
| [q481] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-egl-eglcontract-smart-contract-security-audit-halborn-v1-1-pdf.md | LOW | Halborn | USE OF BLOCK.TIMESTAMP |
| [q482] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-egl-eglcontract-smart-contract-security-audit-halborn-v1-1-pdf.md | LOW | Halborn | MISSING EVENT HANDLER |
| [q483] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-egl-eglcontract-smart-contract-security-audit-halborn-v1-1-pdf.md | LOW | Halborn | IGNORED RETURN VALUES |
| [q484] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-egl-eglcontract-smart-contract-security-audit-halborn-v1-1-pdf.md | INFO | Halborn | USE OF ASSERT |
| [q485] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-egl-eglcontract-smart-contract-security-audit-halborn-v1-1-pdf.md | INFO | Halborn | MISSING RE-ENTRANCY PROTECTION |
| [q486] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-egl-eglcontract-smart-contract-security-audit-halborn-v1-1-pdf.md | INFO | Halborn | BLOCK TIMESTAMP ALIAS USAGE |
| [q487] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-egl-genesis-smart-contract-security-audit-halborn-v-1-1-pdf.md | LOW | Halborn | FLOATING PRAGMA |
| [q488] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-egl-genesis-smart-contract-security-audit-halborn-v-1-1-pdf.md | LOW | Halborn | MISSING ADDRESS VALIDATION |
| [q489] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-egl-genesis-smart-contract-security-audit-halborn-v-1-1-pdf.md | LOW | Halborn | MISSING CALCULATION ON THE CONTRIBUTORS COUNT |
| [q490] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-egl-genesis-smart-contract-security-audit-halborn-v-1-1-pdf.md | LOW | Halborn | ALLOW WITHDRAW PROGRESS WITHOUT FUNDS |
| [q491] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-egl-genesis-smart-contract-security-audit-halborn-v-1-1-pdf.md | INFO | Halborn | MISSING VALIDATION ON THE FUNCTION |
| [q492] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-egl-genesis-smart-contract-security-audit-halborn-v-1-1-pdf.md | INFO | Halborn | POSSIBLE MISUSE OF PUBLIC FUNCTIONS |
| [q493] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-egl-genesis-smart-contract-security-audit-halborn-v-1-1-pdf.md | INFO | Halborn | BLOCK TIMESTAMP ALIAS USAGE |
| [q494] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-egl-genesis-smart-contract-security-audit-halborn-v-1-1-pdf.md | INFO | Halborn | LACK OF VISIBILITY ON THE MAXTHRESHOLD VARIABLE |
| [q495] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-euler-smart-contract-security-audit-halborn-v-1-1-pdf.md | LOW | Halborn | FLOATING PRAGMA |
| [q496] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-euler-smart-contract-security-audit-halborn-v-1-1-pdf.md | LOW | Halborn | USE OF BLOCK.TIMESTAMP |
| [q497] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-euler-smart-contract-security-audit-halborn-v-1-1-pdf.md | INFO | Halborn | NO STORAGE REFUND WHEN EXITING THE MARKET |
| [q498] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-euler-smart-contract-security-audit-halborn-v-1-1-pdf.md | INFO | Halborn | INVALID CONSTANT VALUE |
| [q499] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-euler-smart-contract-security-audit-halborn-v-1-1-pdf.md | INFO | Halborn | INFINITE ALLOWANCE |
| [q500] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-finance-vote-basicpoolfactory-smart-contract-security-audit-halborn-v1-1-pdf.md | LOW | Halborn | MISSING RE-ENTRANCY PROTECTION |
| [q501] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-finance-vote-basicpoolfactory-smart-contract-security-audit-halborn-v1-1-pdf.md | LOW | Halborn | MISSING ADDRESS VALIDATION |
| [q502] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-finance-vote-basicpoolfactory-smart-contract-security-audit-halborn-v1-1-pdf.md | LOW | Halborn | MISSING EVENT HANDLER |
| [q503] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-finance-vote-basicpoolfactory-smart-contract-security-audit-halborn-v1-1-pdf.md | LOW | Halborn | USE OF BLOCK.TIMESTAMP |
| [q504] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-finance-vote-basicpoolfactory-smart-contract-security-audit-halborn-v1-1-pdf.md | LOW | Halborn | IGNORED RETURN VALUES |
| [q505] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-finance-vote-basicpoolfactory-smart-contract-security-audit-halborn-v1-1-pdf.md | INFO | Halborn | POSSIBLE MISUSE OF PUBLIC FUNCTIONS |
| [q506] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-finance-vote-gatedmerkleidentity-and-incinerator-smart-contract-security-audit-halborn-v1-1-pdf.md | LOW | Halborn | MISSING ADDRESS VALIDATION |
| [q507] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-finance-vote-gatedmerkleidentity-and-incinerator-smart-contract-security-audit-halborn-v1-1-pdf.md | LOW | Halborn | MISSING EVENT HANDLER |
| [q508] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-finance-vote-gatedmerkleidentity-and-incinerator-smart-contract-security-audit-halborn-v1-1-pdf.md | LOW | Halborn | IGNORED RETURN VALUES |
| [q509] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-finance-vote-gatedmerkleidentity-and-incinerator-smart-contract-security-audit-halborn-v1-1-pdf.md | INFO | Halborn | MULTIPLE INCINERATE ON THE WITHDRAW PROGRESS |
| [q510] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-finance-vote-gatedmerkleidentity-and-incinerator-smart-contract-security-audit-halborn-v1-1-pdf.md | INFO | Halborn | MISSING ARRAY ELEMENT CHECK |
| [q511] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-finance-vote-gatedmerkleidentity-and-incinerator-smart-contract-security-audit-halborn-v1-1-pdf.md | INFO | Halborn | FOR LOOP OVER DYNAMIC ARRAY |
| [q512] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-finance-vote-gatedmerkleidentity-and-incinerator-smart-contract-security-audit-halborn-v1-1-pdf.md | INFO | Halborn | POSSIBLE MISUSE OF PUBLIC FUNCTIONS |
| [q513] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-highstreetmarket-nft-pool-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | AMOUNT PARAMETER CAN BE REMOVED |
| [q514] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-highstreetmarket-nft-pool-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | EMERGENCYWITHDRAW FUNCTION DOES NOT PROVIDE ANY UTILITY |
| [q515] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-highstreetmarket-nft-pool-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | SOME FUNCTIONS CAN BE REMOVED |
| [q516] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-highstreetmarket-nft-pool-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | GAS OVER-CONSUMPTION IN LOOPS |
| [q517] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-highstreetmarket-nft-pool-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | UNNECESSARY INITIALIZATION OF UINT256 VARIABLES TO 0 |
| [q518] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-jarvis-aerariummilitare-smart-contract-security-audit-halborn-v1-1-pdf.md | LOW | Halborn | FLOATING PRAGMA |
| [q519] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-jarvis-aerariummilitare-smart-contract-security-audit-halborn-v1-1-pdf.md | INFO | Halborn | PRAGMA VERSION |
| [q520] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-jarvis-aerariummilitare-smart-contract-security-audit-halborn-v1-1-pdf.md | INFO | Halborn | POSSIBLE MISUSE OF PUBLIC FUNCTIONS |
| [q521] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-jarvis-perpetualpoolparty-halborn-audit-pdf.md | INFO | Halborn | ASSESSMENT SUMMARY & FINDINGS OVERVIEW CRITICAL HIGH MEDIUM LOW 0 0 0 2 SECURITY ANALYSIS RISK LEVEL ADDRESS CHECK MISSING Low DIVIDE BEFORE MULTIPLE |
| [q522] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-lid-liftoff-audit-halborn-v1-1-pdf.md | LOW | Halborn | ASSESSMENT SUMMARY & FINDINGS OVERVIEW CRITICAL HIGH MEDIUM LOW 0 0 1 2 SECURITY ANALYSIS RISK LEVEL INTEGER OVERFLOW Medium ADDRESS CHECK MISSING |
| [q523] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-matrixswap-staking-smart-contract-security-audit-report-halborn-final-pdf.md | LOW | Halborn | UNCHECKED TRANSFERS |
| [q524] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-matrixswap-staking-smart-contract-security-audit-report-halborn-final-pdf.md | LOW | Halborn | UNUSED RETURNS |
| [q525] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-matrixswap-staking-smart-contract-security-audit-report-halborn-final-pdf.md | LOW | Halborn | MISSING ZERO ADDRESS CHECKS |
| [q526] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-matrixswap-staking-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | STATE VARIABLES MISSING CONSTANT MODIFIER |
| [q527] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-matrixswap-staking-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | STATE VARIABLE MISSING IMMUTABLE MODIFIER |
| [q528] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-matrixswap-staking-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | POSSIBLE MISUSE OF PUBLIC FUNCTIONS |
| [q529] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-matrixswap-staking-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | INCORRECT ERC20 TOKEN NAME |
| [q530] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-moonwell-finance-safety-module-smart-contract-security-audit-report-halborn-final-pdf.md | LOW | Halborn | MISSING ZERO ADDRESS CHECKS |
| [q531] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-moonwell-finance-safety-module-smart-contract-security-audit-report-halborn-final-pdf.md | LOW | Halborn | MISSING REENTRANCY GUARD |
| [q532] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-moonwell-finance-safety-module-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | USE 1E18 CONSTANT FOR GAS OPTIMIZATION |
| [q533] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-moonwell-finance-safety-module-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | USE ++I INSTEAD OF I++ IN LOOPS FOR GAS OPTIMIZATION |
| [q534] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-mori-finance-mori-protocol-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | MISSING FUNCTION IMPLEMENTATION |
| [q535] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-mori-finance-mori-protocol-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | FLOATING PRAGMA |
| [q536] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-nftfi-eth-nftfi-collection-offer-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | GAS OVER-CONSUMPTION IN LOOPS |
| [q537] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-nftfi-eth-nftfi-collection-offer-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | SOLC 0.8.4 COMPILER VERSION CONTAINS MULTIPLE BUGS |
| [q538] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-oraichain-aivaultorai-audit-halborn-v1-1-pdf.md | LOW | Halborn | ASSESSMENT SUMMARY & FINDINGS OVERVIEW CRITICAL HIGH MEDIUM LOW 0 0 0 3 SECURITY ANALYSIS RISK LEVEL FLOATING PRAGMA Low DIVIDE BEFORE MULTIPLY |
| [q539] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-oraichain-controller-and-vault-audit-halborn-v1-3-pdf.md | LOW | Halborn | ASSESSMENT SUMMARY & FINDINGS OVERVIEW CRITICAL HIGH MEDIUM LOW 0 0 0 3 SECURITY ANALYSIS RISK LEVEL MULTIPLES AND FLOATING Low OUTDATED LIBRARIES |
| [q540] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-oraichain-oracle-audit-halborn-v1-pdf.md | INFO | Halborn | ASSESSMENT SUMMARY & FINDINGS OVERVIEW CRITICAL HIGH MEDIUM LOW 0 0 0 0 SECURITY ANALYSIS RISK LEVEL USE OF INLINE ASSEMBLY |
| [q541] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-pangolin-allocationvester-smart-contract-security-audit-report-halborn-final-pdf.md | LOW | Halborn | FLOATING PRAGMA |
| [q542] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-pangolin-allocationvester-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | MISSING EVENTS EMITTING |
| [q543] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-pangolin-allocationvester-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | MISSING ZERO ADDRESS CHECK |
| [q544] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-pocket-network-wrapped-pocket-smart-contract-security-assessment-report-halborn-final-pdf.md | LOW | Halborn | THE WRAPPEDPOCKET CONTRACT CANNOT BE PAUSED |
| [q545] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-pocket-network-wrapped-pocket-smart-contract-security-assessment-report-halborn-final-pdf.md | LOW | Halborn | ZERO ADDRESS CHECK MISSING |
| [q546] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-pocket-network-wrapped-pocket-smart-contract-security-assessment-report-halborn-final-pdf.md | LOW | Halborn | INVALID CONFIGURATION ALLOWED |
| [q547] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-pocket-network-wrapped-pocket-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | INEFFICTIENT FOR LOOPS |
| [q548] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-polkaswitch-smart-contract-security-audit-halborn-v1-1-pdf.md | LOW | Halborn | FLOATING PRAGMA |
| [q549] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-polkaswitch-smart-contract-security-audit-halborn-v1-1-pdf.md | LOW | Halborn | MISSING RE-ENTRANCY PROTECTION |
| [q550] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-polkaswitch-smart-contract-security-audit-halborn-v1-1-pdf.md | INFO | Halborn | USE OF BLOCK.TIMESTAMP |
| [q551] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-polkaswitch-smart-contract-security-audit-halborn-v1-1-pdf.md | INFO | Halborn | POSSIBLE MISUSE OF PUBLIC FUNCTIONS |
| [q552] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-powertrade-fuel-smartcontract-halborn-report-v1-pdf.md | LOW | Halborn | ASSESSMENT SUMMARY & FINDINGS OVERVIEW CRITICAL HIGH MEDIUM LOW 0 0 0 2 SECURITY ANALYSIS RISK LEVEL EXPERIMENTAL FEATURES ENABLED |
| [q553] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-powertrade-vesting-smartcontract-halborn-report-v1-pdf.md | LOW | Halborn | ASSESSMENT SUMMARY & FINDINGS OVERVIEW CRITICAL HIGH MEDIUM LOW 0 0 0 1 SECURITY ANALYSIS RISK LEVEL DIVIDE BEFORE MULTIPLY Very |
| [q554] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-seascape-nft-multisend-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | UPGRADE TO AT LEAST PRAGMA 0.8.10 |
| [q555] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-seascape-nft-swap-smart-contract-security-audit-report-halborn-final-pdf.md | LOW | Halborn | MISSING REENTRANCY GUARD |
| [q556] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-seascape-nft-swap-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | NFT NUMBER 0 CAN NEVER BE TRADED |
| [q557] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-seascape-nft-swap-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | UPGRADE TO AT LEAST PRAGMA 0.8.10 |
| [q558] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-seascape-nft-swap-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | USING ++I CONSUMES LESS GAS THAN I++ IN LOOPS |
| [q559] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-sifchain-balancer-smart-contract-audit-halborn-v1-pdf.md | INFO | Halborn | ASSESSMENT SUMMARY & FINDINGS OVERVIEW CRITICAL HIGH MEDIUM LOW 0 0 0 0 SECURITY ANALYSIS RISK LEVEL FOR LOOP OVER DYNAMIC ARRAY |
| [q560] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-sifchain-peggy-smart-contracts-audit-halborn-v1-pdf.md | INFO | Halborn | ASSESSMENT SUMMARY & FINDINGS OVERVIEW CRITICAL HIGH MEDIUM LOW 0 0 0 0 SECURITY ANALYSIS RISK LEVEL FOR LOOP OVER DYNAMIC ARRAY |
| [q561] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-spherium-bridge-smart-contract-security-audit-report-halborn-v1-1-pdf.md | LOW | Halborn | IGNORE RETURN VALUES |
| [q562] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-spherium-bridge-smart-contract-security-audit-report-halborn-v1-1-pdf.md | LOW | Halborn | FLOATING PRAGMA |
| [q563] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-spherium-bridge-smart-contract-security-audit-report-halborn-v1-1-pdf.md | INFO | Halborn | PRAGMA VERSION |
| [q564] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-spherium-bridge-smart-contract-security-audit-report-halborn-v1-1-pdf.md | INFO | Halborn | POSSIBLE MISUSE OF PUBLIC FUNCTIONS |
| [q565] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-spherium-bridge-smart-contract-security-audit-report-halborn-v1-1-pdf.md | INFO | Halborn | UNUSED CODE |
| [q566] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-spherium-vesting-smart-contract-security-audit-report-halborn-final-pdf.md | LOW | Halborn | USAGE OF BLOCK-TIMESTAMP |
| [q567] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-spherium-vesting-smart-contract-security-audit-report-halborn-final-pdf.md | LOW | Halborn | FLOATING PRAGMA |
| [q568] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-spherium-vesting-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | MISSING EVENTS EMITTING |
| [q569] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-spherium-vesting-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | POSSIBLE MISUSE OF PUBLIC FUNCTIONS |
| [q570] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-staderlabs-tokenerc20-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | SOLC 0.8.2 COMPILER VERSION CONTAINS MULTIPLE BUGS |
| [q571] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-staging-labs-saferoot-contracts-smart-contract-security-assessment-report-halborn-final-pdf.md | LOW | Halborn | MISSING ZERO ADDRESS CHECKS |
| [q572] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-staging-labs-saferoot-contracts-smart-contract-security-assessment-report-halborn-final-pdf.md | LOW | Halborn | REGISTRY CANNOT BE RE-ENABLED |
| [q573] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-staging-labs-saferoot-contracts-smart-contract-security-assessment-report-halborn-final-pdf.md | LOW | Halborn | REGISTRY CANNOT BE CHANGED |
| [q574] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-staging-labs-saferoot-contracts-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | LACK OF SAFEGUARD DATA VALIDATION |
| [q575] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-staging-labs-saferoot-contracts-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | LACK OF DISABLEINITIALIZERS IN THE IMPLEMENTATION CONTRACT |
| [q576] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-staging-labs-saferoot-contracts-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | ARBITRARY AMOUNT OF SAFEGUARDS CAN BE ADDED |
| [q577] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-staging-labs-saferoot-contracts-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | INCOMPATIBILITY WITH TOKENS NOT FOLLOWING THE STANDARDS |
| [q578] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-staging-labs-saferoot-contracts-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | MULTIPLE SAFEGUARDS CAN BE ADDED TO THE SAME ASSET |
| [q579] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-staging-labs-saferoot-contracts-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | ITERATING OVER A DYNAMIC ARRAY |
| [q580] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-staging-labs-saferoot-contracts-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | MISTAKENLY SENT TOKENS AND ETHER CANNOT BE RECOVERED FROM THE CONTRACTS |
| [q581] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-staging-labs-saferoot-contracts-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | FOR LOOPS CAN BE GAS OPTIMIZED |
| [q582] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-staging-labs-saferoot-contracts-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | UNNECESSARY VALIDATION |
| [q583] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-staging-labs-saferoot-contracts-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | NOT ALL EVM COMPATIBLE CHAIN SUPPORTS SOLIDITY 0.8.20 |
| [q584] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-stater-lending-contracts-smart-contract-security-audit-halborn-v-1-1-pdf.md | LOW | Halborn | USAGE OF BLOCK-TIMESTAMP |
| [q585] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-stater-lending-contracts-smart-contract-security-audit-halborn-v-1-1-pdf.md | INFO | Halborn | FOR LOOP OVER DYNAMIC ARRAY |
| [q586] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-sushiswap-miso-smart-contract-report-halborn-v2-pdf.md | LOW | Halborn | USE OF BLOCK.TIMESTAMP |
| [q587] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-sushiswap-miso-smart-contract-report-halborn-v2-pdf.md | LOW | Halborn | UINT256 OVERFLOW |
| [q588] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-sushiswap-miso-smart-contract-report-halborn-v2-pdf.md | LOW | Halborn | FLOATING PRAGMA |
| [q589] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-sushiswap-miso-smart-contract-report-halborn-v2-pdf.md | LOW | Halborn | UNINITIALIZED VARIABLE |
| [q590] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-sushiswap-miso-smart-contract-report-halborn-v2-pdf.md | LOW | Halborn | IGNORE RETURN VALUES |
| [q591] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-sushiswap-miso-smart-contract-report-halborn-v2-pdf.md | INFO | Halborn | INIT FUNCTION SHOULD BE CALLED |
| [q592] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-sushiswap-miso-smart-contract-report-halborn-v2-pdf.md | INFO | Halborn | POSSIBLE MISUSE OF PUBLIC FUNCTIONS |
| [q593] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-sushiswap-miso-smart-contract-report-halborn-v2-pdf.md | INFO | Halborn | POINTLIST FACTORY DEPRECATION HAS NO EFFECT |
| [q594] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-sushiswap-miso-smart-contract-report-halborn-v2-pdf.md | INFO | Halborn | INDEX OUT OF RANGE MISSING CHECKS |
| [q595] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-sushiswap-miso-smart-contract-report-halborn-v2-pdf.md | INFO | Halborn | SLOT0 NOT USED |
| [q596] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-sushiswap-miso-smart-contract-report-halborn-v2-pdf.md | INFO | Halborn | DISORDERED MATH OPERATIONS |
| [q597] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-sushiswap-miso-smart-contract-report-halborn-v2-pdf.md | INFO | Halborn | INTEGER TRUNCATION |
| [q598] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-sushiswap-miso-smart-contract-report-halborn-v2-pdf.md | INFO | Halborn | MISMATCHED STRUCTS AND INTERFACES |
| [q599] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-sushiswap-miso-smart-contract-report-halborn-v2-pdf.md | INFO | Halborn | MISSING CHECKS |
| [q600] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-syncswap-pool-contracts-smart-contract-security-assessment-report-halborn-final-pdf.md | LOW | Halborn | VARIABLES UPDATED IMPROPERLY IN DURING FEE MINTING |
| [q601] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-syncswap-pool-contracts-smart-contract-security-assessment-report-halborn-final-pdf.md | LOW | Halborn | STATE IS NOT RESET PROPERLY WHEN ALL LIQUIDITY IS WITHDRAWN FROM POOL |
| [q602] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-syncswap-pool-contracts-smart-contract-security-assessment-report-halborn-final-pdf.md | LOW | Halborn | INACCURATE AMPLIFIER COEFFICIENT CALCULATION |
| [q603] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-syncswap-pool-contracts-smart-contract-security-assessment-report-halborn-final-pdf.md | LOW | Halborn | IMPROPER INVARIANT UPDATE IN TWEAKPRICE |
| [q604] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-syncswap-pool-contracts-smart-contract-security-assessment-report-halborn-final-pdf.md | LOW | Halborn | UNNECESSARY DEBUG FUNCTIONS |
| [q605] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-syncswap-pool-contracts-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | LACK OF TEST COVARAGE |
| [q606] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-syncswap-pool-contracts-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | EXTERNAL CALLS |
| [q607] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-thorswap-aggregators-smart-contract-security-audit-report-halborn-final-pdf.md | LOW | Halborn | INITIAL vTHOR SHARE PRICE MANIPULATION EXPOSURE |
| [q608] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-thorswap-aggregators-smart-contract-security-audit-report-halborn-final-pdf.md | LOW | Halborn | MISSING RE-ENTRANCY PROTECTION |
| [q609] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-thorswap-aggregators-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | POSSIBLE MISUSE OF PUBLIC FUNCTIONS |
| [q610] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-tidal-finance-smart-contracts-security-audit-halborn-v1-1-pdf.md | LOW | Halborn | EXPERIMENTAL FEATURES ENABLED |
| [q611] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-tidal-finance-smart-contracts-security-audit-halborn-v1-1-pdf.md | LOW | Halborn | MISSING EVENT HANDLER |
| [q612] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-tidal-finance-smart-contracts-security-audit-halborn-v1-1-pdf.md | LOW | Halborn | FLOATING PRAGMA |
| [q613] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-tidal-finance-smart-contracts-security-audit-halborn-v1-1-pdf.md | INFO | Halborn | INFINITE MINTING |
| [q614] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-tidal-finance-smart-contracts-security-audit-halborn-v1-1-pdf.md | INFO | Halborn | USE OF INLINE ASSEMBLY |
| [q615] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-tidal-finance-smart-contracts-security-audit-halborn-v1-1-pdf.md | INFO | Halborn | MISSING RE-ENTRANCY PROTECTION |
| [q616] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-tidal-finance-smart-contracts-security-audit-halborn-v1-1-pdf.md | INFO | Halborn | BLOCK TIMESTAMP ALIAS USAGE |
| [q617] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-tidal-finance-smart-contracts-security-audit-halborn-v1-1-pdf.md | INFO | Halborn | POSSIBLE MISUSE OF PUBLIC FUNCTIONS |
| [q618] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-tidal-finance-smart-contracts-security-audit-halborn-v1-1-pdf.md | INFO | Halborn | MISSING CONSTANT DEFINITION |
| [q619] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-truffles-nft-invoice-smart-contract-security-assessment-report-halborn-final-pdf.md | LOW | Halborn | MISSING ZERO ADDRESS CHECK |
| [q620] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-truffles-nft-invoice-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | INVOICE TYPE CHECK MISSING |
| [q621] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-truffles-nft-invoice-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | LACK OF REENTRANCYGUARD |
| [q622] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-truffles-nft-invoice-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | REDUNDANT CHECK IN THE REMOVEAUTHORIZED FUNCTION |
| [q623] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-truffles-nft-invoice-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | CONTRACT PAUSE FEATURE MISSING |
| [q624] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-truffles-nft-invoice-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | FLOATING PRAGMA |
| [q625] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-woonkly-nft-protocol-smart-contract-security-audit-report-halborn-final-pdf.md | LOW | Halborn | FUNCTION ERC721WOONKLYNFTREVEALWAVE.CHANGEHIDDENBASEURI MODIFIES THE WRONG STATE VARIABLE |
| [q626] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-woonkly-nft-protocol-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | REVEALWAVE.REVEALDATE IS NOT USED |
| [q627] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-woonkly-nft-protocol-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | UNNEEDED INITIALIZATION OF UINT256 VARIABLES TO 0 |
| [q628] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-woonkly-nft-protocol-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | USING ++I CONSUMES LESS GAS THAN I++ IN LOOPS |
| [q629] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-woonkly-nft-protocol-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | POSSIBLE MISUSE OF PUBLIC FUNCTIONS |
| [q630] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-yieldly-finance-lottery-algorand-smart-contract-halborn-v1-1-pdf.md | LOW | Halborn | LACK OF MULTISIG PROGRAM |
| [q631] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-yieldly-finance-lottery-algorand-smart-contract-halborn-v1-1-pdf.md | LOW | Halborn | MISSING PROXY ASSET DEFINITION ON THE FUNCTIONS |
| [q632] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-yieldly-finance-lottery-algorand-smart-contract-halborn-v1-1-pdf.md | INFO | Halborn | MISSING FREEZE/REVOKE ASSETS DEFINITION |
| [q633] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-yieldly-finance-lottery-algorand-smart-contract-halborn-v1-1-pdf.md | INFO | Halborn | MULTIPLE PRAGMA DEFINITION |
| [q634] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-yieldly-finance-lottery-algorand-smart-contract-halborn-v1-1-pdf.md | INFO | Halborn | ALERTHUB SETUP |
| [q635] | reports/eth-l1-clients_findings/publications-spectral-token-zellic-audit-report-pdf.md | INFO | Zellic | Potential integer underflow in calculateAllocation (SpecToken) |
| [q636] | reports/eth-l1-clients_findings/publications-spectral-token-zellic-audit-report-pdf.md | INFO | Zellic | Centralization risks of the owner (SpecToken) |
| [q637] | reports/eth-l1-clients_findings/publicreports-solidity-smart-contract-audits-nftfi-ethereum-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | Cause-effect checks missing (NFTfi ethereum contracts) |
| [q638] | reports/eth-l1-clients_findings/publications-reviews-2024-06-ethereum-foundation-devcon-auction-raffle-securityreview-pdf.md | LOW | Trail of Bits | Risk of funds becoming trapped if owner key is lost before raffle settlement (EF devcon auction raffle) |
| [q639] | reports/eth-l1-clients_findings/publicauditreports-nm0234-final-ethereum-foundation-holesky-funds-vault-pdf.md | INFO | Nethermind | Manager cooldown period is not consistent (EF Holesky funds vault) |
| [q640] | reports/eth-l1-clients_findings/publicauditreports-nm0234-final-ethereum-foundation-holesky-funds-vault-pdf.md | INFO | Nethermind | Missing zero address checks (EF Holesky funds vault) |
| [q641] | reports/eth-l1-clients_findings/publicauditreports-nm0234-final-ethereum-foundation-holesky-funds-vault-pdf.md | INFO | Nethermind | Other best practice fixes (EF Holesky funds vault) |
| [q642] | reports/eth-l1-clients_findings/public-audits-reports-opsek-review-pdf.md | LOW | auditor | (OPK-01) Mishandled DNS configuration in Windows hardening script (Opsek node hardening scripts) |
| [q643] | reports/eth-l1-clients_findings/public-audits-reports-opsek-review-pdf.md | LOW | auditor | (OPK-02) Inconsistent backup of configuration files on macOS (Opsek node hardening scripts) |
| [q644] | reports/eth-l1-clients_findings/public-audits-reports-opsek-review-pdf.md | LOW | auditor | (OPK-03) Fragile restore functionality in macOS backup script (Opsek node hardening scripts) |
| [q645] | reports/eth-l1-clients_findings/public-audits-reports-opsek-review-pdf.md | LOW | auditor | (OPK-04) Flawed backup behaviour on macOS hardening scripts (Opsek node hardening scripts) |
| [q646] | reports/eth-l1-clients_findings/public-audits-reports-opsek-review-pdf.md | LOW | auditor | (OPK-05) Unnecessary install of brew package manager (Opsek node hardening scripts) |
| [q647] | reports/eth-l1-clients_findings/public-audits-reports-opsek-review-pdf.md | LOW | auditor | (OPK-06) Cron configuration deleted without backup (Opsek node hardening scripts) |
| [q648] | reports/eth-l1-clients_findings/public-audits-reports-opsek-review-pdf.md | LOW | auditor | (OPK-07) Fragile update configuration (Opsek node hardening scripts) |
| [q649] | reports/eth-l1-clients_findings/public-audits-reports-opsek-review-pdf.md | LOW | auditor | (OPK-08) Filesystem remount not persistent (Opsek node hardening scripts) |
| [q650] | reports/eth-l1-clients_findings/public-audits-reports-opsek-review-pdf.md | LOW | auditor | (OPK-09) Root account shell change breaks login (Opsek node hardening scripts) |
| [q651] | reports/eth-l1-clients_findings/public-audits-reports-opsek-review-pdf.md | LOW | auditor | (OPK-10) Flawed firewall configuration (Opsek node hardening scripts) |
| [q652] | reports/eth-l1-clients_findings/public-audits-reports-opsek-review-pdf.md | LOW | auditor | (OPK-11) Flawed SSH port randomisation (Opsek node hardening scripts) |
| [q653] | reports/eth-l1-clients_findings/public-audits-reports-opsek-review-pdf.md | LOW | auditor | (OPK-12) SSH service force started (Opsek node hardening scripts) |
| [q654] | reports/eth-l1-clients_findings/public-audits-reports-opsek-review-pdf.md | LOW | auditor | (OPK-13) Flawed backup behaviour on Linux hardening scripts (Opsek node hardening scripts) |
| [q655] | reports/eth-l1-clients_findings/public-audits-reports-opsek-review-pdf.md | LOW | auditor | (OPK-14) Fragile sudoers file manipulation (Opsek node hardening scripts) |
| [q656] | reports/eth-l1-clients_findings/37582-sc-low-incorrect-hexstring-parsing-leads-to-compilation-error-or-type-confusion.md | LOW | Immunefi (anatomist) | Incorrect HexString parsing leads to compilation error or type confusion (Vyper compiler, Attackathon) |
| [q657] | reports/eth-l1-clients_findings/37583-sc-low-incorrect-for-annotation-parsing.md | LOW | Immunefi (anatomist) | Incorrect for annotation parsing (Vyper compiler, Attackathon) |
| [q658] | reports/eth-l1-clients_findings/37584-sc-insight-nonpayable-not-respected-for-internal-function.md | INFO | Immunefi (anatomist) | Nonpayable not respected for internal function (Vyper compiler, Attackathon) |
| [q659] | reports/eth-l1-clients_findings/37634-sc-low-incorrect-builtin-erc4626-call-signature.md | LOW | Immunefi (anatomist) | Incorrect builtin ERC4626 call signature (Vyper compiler, Attackathon) |
| [q660] | reports/eth-l1-clients_findings/37985-sc-low-incorrectly-eliminate-code-with-side-effect-in-slice-args.md | LOW | Immunefi (anatomist) | Incorrectly eliminate code with side effect in slice args (Vyper compiler, Attackathon) |
| [q661] | reports/eth-l1-clients_findings/38505-sc-low-irnode-multi-evaluation-in-for-list-iter.md | LOW | Immunefi (anatomist) | IRNode multi-evaluation in for list iter (Vyper compiler, Attackathon) |
| [q662] | reports/eth-l1-clients_findings/38530-sc-low-incorrectly-eliminated-code-with-side-effect-in-concat-args.md | LOW | Immunefi (anatomist) | Incorrectly eliminated code with side effect in concat args (Vyper compiler, Attackathon) |
| [q663] | reports/eth-l1-clients_findings/38581-sc-insight-incorrect-unwrap-on-bytes-and-string.md | INFO | Immunefi (anatomist) | Incorrect unwrap on bytes and string (Vyper compiler, Attackathon) |
| [q664] | reports/eth-l1-clients_findings/38693-sc-insight-bytesm-to-bytes-conversion-does-not-match-the-reference-implementation.md | INFO | Immunefi (anatomist) | BytesM to Bytes conversion does not match the reference implementation (Vyper compiler, Attackathon) |
| [q665] | reports/eth-l1-clients_findings/38855-sc-low-evaluation-order-is-not-respected-in-log-function.md | LOW | Immunefi (anatomist) | Evaluation order is not respected in log function (Vyper compiler, Attackathon) |
| [q666] | reports/eth-l1-clients_findings/publicreports-solidity-smart-contract-audits-lodestar-lodestar-finance-smart-contract-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | (HAL-01) Any user can borrow on behalf of another user that approved the Ploopy contract (Lodestar Finance Ploopy lending) |
| [q667] | reports/eth-l1-clients_findings/publicreports-solidity-smart-contract-audits-lodestar-lodestar-finance-smart-contract-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | (HAL-02) cEtherDelegator delegatecalls some cEtherUpgradeable functions incorrectly, always reverting (Lodestar Finance Ploopy lending) |
| [q668] | reports/eth-l1-clients_findings/publicreports-solidity-smart-contract-audits-lodestar-lodestar-finance-smart-contract-security-assessment-report-halborn-final-pdf.md | HIGH | Halborn | (HAL-03) Empty markets are vulnerable to inflation attacks (Lodestar Finance Ploopy lending) |
| [q669] | reports/eth-l1-clients_findings/publicreports-solidity-smart-contract-audits-lodestar-lodestar-finance-smart-contract-security-assessment-report-halborn-final-pdf.md | HIGH | Halborn | (HAL-04) Looping with plvGLP borrows USDC and repays with plvGLP, always reverting (Lodestar Finance Ploopy lending) |
| [q670] | reports/eth-l1-clients_findings/publicreports-solidity-smart-contract-audits-lodestar-lodestar-finance-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | (HAL-05) Ploopy leverage calculation is wrongly implemented (Lodestar Finance Ploopy lending) |
| [q671] | reports/eth-l1-clients_findings/publicreports-solidity-smart-contract-audits-lodestar-lodestar-finance-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | (HAL-06) Sequencer status is not checked for lplvGLP price (Lodestar Finance Ploopy lending) |
| [q672] | reports/eth-l1-clients_findings/publicreports-solidity-smart-contract-audits-lodestar-lodestar-finance-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | (HAL-07) swapThroughUniswap call will always revert as nativeUSDC will always be zero (Lodestar Finance Ploopy lending) |
| [q673] | reports/eth-l1-clients_findings/publicreports-solidity-smart-contract-audits-lodestar-lodestar-finance-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | (HAL-08) Missing initial swap call to convert USDCbridged into USDCnative before minting (Lodestar Finance Ploopy lending) |
| [q674] | reports/eth-l1-clients_findings/publicreports-solidity-smart-contract-audits-lodestar-lodestar-finance-smart-contract-security-assessment-report-halborn-final-pdf.md | LOW | Halborn | (HAL-09) useWalletBalance parameter is not used correctly (Lodestar Finance Ploopy lending) |
| [q675] | reports/eth-l1-clients_findings/publicreports-solidity-smart-contract-audits-lodestar-lodestar-finance-smart-contract-security-assessment-report-halborn-final-pdf.md | LOW | Halborn | (HAL-10) blocksPerYear are not correctly adjusted in the rate models (Lodestar Finance Ploopy lending) |
| [q676] | reports/eth-l1-clients_findings/publicreports-solidity-smart-contract-audits-lodestar-lodestar-finance-smart-contract-security-assessment-report-halborn-final-pdf.md | LOW | Halborn | (HAL-11) mintAndStakeGlp() call does not check for slippage (Lodestar Finance Ploopy lending) |
| [q677] | reports/eth-l1-clients_findings/publicreports-solidity-smart-contract-audits-lodestar-lodestar-finance-smart-contract-security-assessment-report-halborn-final-pdf.md | LOW | Halborn | (HAL-12) latestRoundData call may return stale results (Lodestar Finance Ploopy lending) |
| [q678] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-chromatic-protocol-evm-contracts-smart-contract-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | (HAL-01) Vault flashloan() function can be abused to drain the protocol (Chromatic Protocol) |
| [q679] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-chromatic-protocol-evm-contracts-smart-contract-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | (HAL-02) claimLiquidityBatch() function allows stealing other user's claims (Chromatic Protocol) |
| [q680] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-chromatic-protocol-evm-contracts-smart-contract-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | (HAL-03) withdrawLiquidityBatch() function allows stealing other user's withdrawals (Chromatic Protocol) |
| [q681] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-chromatic-protocol-evm-contracts-smart-contract-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | (HAL-04) removeLiquidityBatch() function allows draining all the CLB tokens in the vault (Chromatic Protocol) |
| [q682] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-chromatic-protocol-evm-contracts-smart-contract-security-assessment-report-halborn-final-pdf.md | HIGH | Halborn | (HAL-05) addLiquidity/openPosition callbacks can be abused to execute flashloans without paying the flashloan fee (Chromatic Protocol) |
| [q683] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-chromatic-protocol-evm-contracts-smart-contract-security-assessment-report-halborn-final-pdf.md | HIGH | Halborn | (HAL-06) Liquidations can be blocked if the settlement token is a token with on-transfer hooks (Chromatic Protocol) |
| [q684] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-chromatic-protocol-evm-contracts-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | (HAL-07) Possible gas griefing in liquidation calls (Chromatic Protocol) |
| [q685] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-chromatic-protocol-evm-contracts-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | (HAL-08) Incompatibility with revert-on-zero-value-transfer tokens (Chromatic Protocol) |
| [q686] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-chromatic-protocol-evm-contracts-smart-contract-security-assessment-report-halborn-final-pdf.md | LOW | Halborn | (HAL-09) Double entry point tokens would break the protocol (Chromatic Protocol) |
| [q687] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-chromatic-protocol-evm-contracts-smart-contract-security-assessment-report-halborn-final-pdf.md | LOW | Halborn | (HAL-10) Maker and market earning distributions calls can be sandwiched (Chromatic Protocol) |
| [q688] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-chromatic-protocol-evm-contracts-smart-contract-security-assessment-report-halborn-final-pdf.md | LOW | Halborn | (HAL-11) Incompatibility with non-standard ERC20 tokens (Chromatic Protocol) |
| [q689] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-chromatic-protocol-evm-contracts-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | (HAL-12) High protocol utilization can block makers from withdrawing their liquidity (Chromatic Protocol) |
| [q690] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-chromatic-protocol-evm-contracts-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | (HAL-13) Maker and market earning distributions could revert if the settlement token swapped is not in any Uniswap pool (Chromatic Protocol) |
| [q691] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-chromatic-protocol-evm-contracts-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | (HAL-14) Market's diamond proxy stores the reentrancyGuard status variable in slot 0 (Chromatic Protocol) |
| [q692] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-chromatic-protocol-evm-contracts-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | (HAL-15) delete keyword is used directly in an EnumerableSet (Chromatic Protocol) |
| [q693] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-chromatic-protocol-evm-contracts-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | (HAL-16) Lack of a double-step transferOwnership pattern (Chromatic Protocol) |
| [q694] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-chromatic-protocol-evm-contracts-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | (HAL-17) Floating pragma (Chromatic Protocol) |
| [q695] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-strike-finance-strike-protocol-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | (HAL-01) Empty markets are vulnerable to inflation attacks (Strike Finance) |
| [q696] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-strike-finance-strike-protocol-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | (HAL-02) Potential reentrancy in borrowFresh function (Strike Finance) |
| [q697] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-strike-finance-strike-protocol-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | (HAL-03) GovernorAlpha2 contract is incompatible with the current Timelock (Strike Finance) |
| [q698] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-strike-finance-strike-protocol-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | (HAL-04) Sequencer status is never checked (Strike Finance) |
| [q699] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-strike-finance-strike-protocol-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | (HAL-05) latestAnswer call may return stale results (Strike Finance) |
| [q700] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-strike-finance-strike-protocol-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | (HAL-06) Earned rewards will be lost if withdrawExpiredLocks() is called before getRewards() (Strike Finance) |
| [q701] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-strike-finance-strike-protocol-smart-contract-security-assessment-report-halborn-final-pdf.md | LOW | Halborn | (HAL-07) StrikeStakingProxy is subject to storage collisions (Strike Finance) |
| [q702] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-strike-finance-strike-protocol-smart-contract-security-assessment-report-halborn-final-pdf.md | LOW | Halborn | (HAL-08) Direct usage of ecrecover allows signature malleability (Strike Finance) |
| [q703] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-strike-finance-strike-protocol-smart-contract-security-assessment-report-halborn-final-pdf.md | LOW | Halborn | (HAL-09) blocksPerYear are not correctly adjusted in the different rate models (Strike Finance) |
| [q704] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-strike-finance-strike-protocol-smart-contract-security-assessment-report-halborn-final-pdf.md | LOW | Halborn | (HAL-10) No limitation on the amount of rewardTokens that can be added to the StrikeStaking contract (Strike Finance) |
| [q705] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-strike-finance-strike-protocol-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | (HAL-11) SimplePriceOracle lacks access control (Strike Finance) |
| [q706] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-strike-finance-strike-protocol-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | (HAL-12) Incorrect implementation of onlyBlacklist and nonBlacklist modifiers (Strike Finance) |
| [q707] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-strike-finance-strike-protocol-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | (HAL-13) Lock parameter can be removed from the StrikeStaking.stake() function (Strike Finance) |
| [q708] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-strike-finance-strike-protocol-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | (HAL-14) Floating pragma (Strike Finance) |
| [q709] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-strike-finance-strike-protocol-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | (HAL-15) Unoptimized loops (Strike Finance) |
| [q710] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-strike-finance-strike-protocol-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | (HAL-16) Missing/incomplete NatSpec comments (Strike Finance) |
| [q711] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-strike-finance-strike-protocol-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | (HAL-17) Wrong comments in the StrikeStaking contract (Strike Finance) |
| [q712] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-proofofplay-pirate-nation-smart-contract-security-audit-report-halborn-final-pdf.md | CRITICAL | Halborn | (HAL-01) Users can start a quest using as input and burning an NFT they do not own (Proof of Play Pirate Nation) |
| [q713] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-proofofplay-pirate-nation-smart-contract-security-audit-report-halborn-final-pdf.md | CRITICAL | Halborn | (HAL-02) Flawed logic causes that navies will never steal pirate's gold (Proof of Play Pirate Nation) |
| [q714] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-proofofplay-pirate-nation-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | (HAL-03) Unsafe cast can allow users to permanently mint gold tokens (Proof of Play Pirate Nation) |
| [q715] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-proofofplay-pirate-nation-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | (HAL-04) Reentrancy in RaffleMintV1.withdrawNonRaffleProceeds (Proof of Play Pirate Nation) |
| [q716] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-proofofplay-pirate-nation-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | (HAL-05) Users can start the same quest multiple times draining the Chainlink VRF subscription (Proof of Play Pirate Nation) |
| [q717] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-proofofplay-pirate-nation-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | (HAL-06) Users can craft using as input an NFT they do not own (Proof of Play Pirate Nation) |
| [q718] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-proofofplay-pirate-nation-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | (HAL-07) craftAmount can be set to zero draining the Chainlink VRF subscription (Proof of Play Pirate Nation) |
| [q719] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-proofofplay-pirate-nation-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | (HAL-08) Crafts cooldown time are always zero (Proof of Play Pirate Nation) |
| [q720] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-proofofplay-pirate-nation-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | (HAL-09) QuestDefinition.maxCompletions can be bypassed by starting the same quest multiple times (Proof of Play Pirate Nation) |
| [q721] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-proofofplay-pirate-nation-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | (HAL-10) Lack of pausable functionality in the LootSystem contract (Proof of Play Pirate Nation) |
| [q722] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-proofofplay-pirate-nation-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | (HAL-11) mintBatch function is not implemented (Proof of Play Pirate Nation) |
| [q723] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-proofofplay-pirate-nation-smart-contract-security-audit-report-halborn-final-pdf.md | LOW | Halborn | (HAL-12) Wrong require statements in GameGlobals contract (Proof of Play Pirate Nation) |
| [q724] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-proofofplay-pirate-nation-smart-contract-security-audit-report-halborn-final-pdf.md | LOW | Halborn | (HAL-13) QuestInput.required value is never checked (Proof of Play Pirate Nation) |
| [q725] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-proofofplay-pirate-nation-smart-contract-security-audit-report-halborn-final-pdf.md | LOW | Halborn | (HAL-14) Lack of disableInitializers call to prevent uninitialized contracts (Proof of Play Pirate Nation) |
| [q726] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-proofofplay-pirate-nation-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | (HAL-15) Users can not unstake NFTs after a call to rescueUnlockNFT or rescueUnlockItem (Proof of Play Pirate Nation) |
| [q727] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-proofofplay-pirate-nation-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | (HAL-16) Dangerous usage of tx.origin (Proof of Play Pirate Nation) |
| [q728] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-proofofplay-pirate-nation-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | (HAL-17/18) State variables missing constant/immutable modifier (Proof of Play Pirate Nation) |
| [q729] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-proofofplay-pirate-nation-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | (HAL-19) Unneeded initialization of uint256 variables to 0 (Proof of Play Pirate Nation) |
| [q730] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-proofofplay-pirate-nation-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | (HAL-20) Using ++i consumes less gas than i++ in loops (Proof of Play Pirate Nation) |
| [q731] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-proofofplay-pirate-nation-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | (HAL-21) Unneeded arrays declaration in finishMintShips function (Proof of Play Pirate Nation) |
| [q732] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-proofofplay-pirate-nation-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | (HAL-22) Missing view function that displays all the tickets owned by a user (Proof of Play Pirate Nation) |
| [q733] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-proofofplay-pirate-nation-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | (HAL-23) Incorrect comment (Proof of Play Pirate Nation) |
| [q734] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-irrigation-protocol-smart-contract-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | (HAL-01) SprinklerUpgradeable contract can be drained through the exchangeToWater function (Irrigation Protocol) |
| [q735] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-irrigation-protocol-smart-contract-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | (HAL-02) Auctions and bids could be stuck permanently if a bid is placed by a blacklisted USDC/USDT user (Irrigation Protocol) |
| [q736] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-irrigation-protocol-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | (HAL-03) Bids can be DoS'ed by placing a very high bid on a very small bidAmount (Irrigation Protocol) |
| [q737] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-irrigation-protocol-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | (HAL-04) latestAnswer call may return stale results (Irrigation Protocol) |
| [q738] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-irrigation-protocol-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | (HAL-05) User could cancel the rest of bids of an auction by doing 200 different bids (Irrigation Protocol) |
| [q739] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-irrigation-protocol-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | (HAL-06) swapETHForWater call can be sandwiched (Irrigation Protocol) |
| [q740] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-irrigation-protocol-smart-contract-security-assessment-report-halborn-final-pdf.md | LOW | Halborn | (HAL-07) autoIrrigateCall will always revert with overflow if called with the full rewardAmount (Irrigation Protocol) |
| [q741] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-irrigation-protocol-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | (HAL-08) Lack of a double-step transferOwnership pattern (Irrigation Protocol) |
| [q742] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-irrigation-protocol-smart-contract-security-assessment-report-halborn-final-pdf.md | INFO | Halborn | (HAL-09) Calling setMiddleAsset would cause the irrigation bonus to always be zero (Irrigation Protocol) |
| [q743] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-bracket-fi-passage-executive-summary-halborn-pdf.md | CRITICAL | Halborn | Executive summary (details redacted): 6 critical, 3 medium, 6 informational; headline: LP token calculation allows stealing user funds, missing nonReentrant on ERC1155 LP mint, improper pointer/counter tracking locks funds (Bracket.fi Passage) |
| [q744] | reports/other-l1_findings/publicreports-algorand-smart-contract-audit-c3-pyteal-executive-summary-report-halborn-pdf.md | HIGH | Halborn | Executive summary: 2 high, 3 medium, 3 low, 10 informational identified in C3 pyTEAL vesting module (details redacted) |
| [q745] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-trust-wallet-barz-executive-summary-halborn-pdf.md | INFO | Halborn | Executive summary (severities unstated): guardian threshold can be bypassed with repetitive data, front-running restriction initialization can lock the wallet, broken unlock functionality, whitelisting/blacklisting impossible in no-guardian condition (Trust Wallet Barz) |
| [q746] | reports/other-l1_findings/publicauditreports-nm0069-final-polygon-id-pdf.md | LOW | Nethermind | Unnecessary space allocation in Proof.siblings (PolygonID) |
| [q747] | reports/other-l1_findings/publicauditreports-nm0113-final-polygonid-pdf.md | MEDIUM | Nethermind | Unable to set version for a revocations (PolygonID) |
| [q748] | reports/other-l1_findings/publicauditreports-nm0113-final-polygonid-pdf.md | LOW | Nethermind | Collision of claims' indices (PolygonID) |
| [q749] | reports/other-l1_findings/publicauditreports-nm0113-final-polygonid-pdf.md | LOW | Nethermind | IdentityBase may return data based on non-published state (PolygonID) |
| [q750] | reports/other-l1_findings/publicauditreports-nm0113-final-polygonid-pdf.md | LOW | Nethermind | IdentityBase may return data not synchronized with StateV2 contract (PolygonID) |
| [q751] | reports/other-l1_findings/publicauditreports-nm0113-final-polygonid-pdf.md | LOW | Nethermind | On-chain ID genesis state cannot follow the specification (PolygonID) |
| [q752] | reports/other-l1_findings/publicauditreports-nm0113-final-polygonid-pdf.md | LOW | Nethermind | State transition security properties differ for ID types (PolygonID) |
| [q753] | reports/other-l1_findings/publicauditreports-nm0113-final-polygonid-pdf.md | LOW | Nethermind | OnChain identities can be left unusable (PolygonID) |
| [q754] | reports/other-l1_findings/publicauditreports-nm0113-final-polygonid-pdf.md | LOW | Nethermind | bytesToAddress(...) casts to incomplete address (PolygonID) |## L1 Contract Generic

**l1-contract-generic patterns mined from uncited L1 audit reports** - 150 sec-tier findings (33 critical / 50 high / 67 medium) across 75 files from Halborn, NCC Group, Oak Security, PeckShield, Trail of Bits, Zellic.

### Overview

Titles in the references table are verbatim from source reports. Route to the exact report file for full PoC detail. Validation strength: `unassessed` (evidence rows only).

### Detection Patterns

#### High-Signal Grep Seeds
```
- _getselfdelegations
- aave
- aavestrategy
- aavestrategymainnet
- able
- absence
- account
- accounting
```

### Vulnerability Description

#### Root Cause

The cited reports describe l1 contract generic paths where a validation, bound, or state-consistency check is missing around attacker-influenced input or an attacker-growable collection. The pattern key for this family is `l1-contract-generic | l1 contract generic | varies by finding | see references`. Every reference row in the table above is a verbatim finding title from the named auditor; consult that report for the exact code location and exploit path.

#### Attack Scenario / Path Variants

**Path A: [Direct input path]**
Path key: `l1-contract-generic | l1 contract generic | varies by finding | see references | user/peer message | direct handler`
1. Attacker submits crafted input (message, tx, packet, or config change) accepted by the entry surface.
2. Missing validation lets the input reach state mutation or an unbounded loop.
3. State corruption, fund misaccounting, or resource exhaustion follows.

**Path B: [Growth-then-trigger path]**
Path key: `l1-contract-generic | l1 contract generic | varies by finding | see references | cheap state growth | later iteration/execution`
1. Attacker cheaply grows a collection (plans, stakes, peers, entries).
2. A later block-time or cleanup path iterates the collection without bounds.
3. Block production exceeds limits or the node exhausts memory (DoS / halt).

### Vulnerable Pattern Examples

**Example 1: Attackers can profit by depositing different tokens and withdrawing as native tokens** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Attackers can profit by depositing different tokens and withdrawing as native tokens
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Attackers can profit by depositing different tokens and withdrawing as native tokens
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 2: Fungible token refunds will fail causing a loss of funds for users** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Fungible token refunds will fail causing a loss of funds for users
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Fungible token refunds will fail causing a loss of funds for users
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 3: Incorrect isReadCall implementation allows infinite token mints** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Incorrect isReadCall implementation allows infinite token mints
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Incorrect isReadCall implementation allows infinite token mints
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

`_getselfdelegations, aave, aavestrategy, aavestrategymainnet, able, absence, account, accounting, accounts, active`

### Related Vulnerabilities

- Sibling entries under the same category folder
