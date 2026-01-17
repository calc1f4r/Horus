---
# Core Classification (Required)
protocol: generic
chain: everychain
category: bridge
vulnerability_type: layerzero_integration

# Attack Vector Details (Required)
attack_type: channel_blocking|gas_griefing|message_replay|fund_loss|payload_validation|peer_misconfiguration
affected_component: lzReceive|_lzSend|NonblockingLzApp|OFT|ONFT|sgReceive|lzCompose

# Bridge-Specific Fields
bridge_provider: layerzero
bridge_attack_vector: channel_blocking | minimum_gas | gas_estimation | fee_refund | payload_size | composed_message | peer_config | decimal_mismatch | amount_trimming

# Technical Primitives (Required)
primitives:
  - lzReceive
  - _lzSend
  - NonblockingLzApp
  - LzApp
  - adapterParams
  - gasLimit
  - endpoint
  - trustedRemote
  - StoredPayload
  - OFT
  - ONFT
  - OFTCore
  - OFTAdapter
  - compose
  - lzCompose
  - sgReceive
  - setPeer
  - peers
  - MessagingFee
  - lzTokenFee
  - sharedDecimals
  - normalizeAmount
  - removeDust
  - _creditTill
  - minGasToTransferAndStore
  - executorLzReceiveOption
  - forceResumeReceive
  - retryMessage
  - dstGasForCall
  - quoteLayerZeroFee
  - OFTComposeMsgCodec

# Impact Classification (Required)
severity: high|medium|low
impact: channel_dos|fund_loss|gas_griefing|message_stuck|token_theft|refund_loss
exploitability: 0.80
financial_impact: high

# Context Tags
tags:
  - defi
  - bridge
  - cross_chain
  - omnichain
  - layerzero
  - stargate
  - oft
  - onft

# Version Info
language: solidity
version: all
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Channel Blocking Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Velodrome - Channel Blocked | `reports/bridge_crosschain_findings/h-06-attacker-can-block-layerzero-channel.md` | HIGH | Code4rena |
| Tapioca - Variable Gas Blocking | `reports/bridge_crosschain_findings/h-16-attacker-can-block-layerzero-channel-due-to-variable-gas-cost-of-saving-pay.md` | HIGH | Code4rena |
| Tapioca - Missing Min Gas | `reports/bridge_crosschain_findings/h-17-attacker-can-block-layerzero-channel-due-to-missing-check-of-minimum-gas-pa.md` | HIGH | Code4rena |
| Decent - Min Gas Missing | `reports/bridge_crosschain_findings/h-02-due-to-missing-checks-on-minimum-gas-passed-through-layerzero-executions-ca.md` | HIGH | Code4rena |
| HoneyJar - ONFT Pathway Blocked | `reports/bridge_crosschain_findings/c-01-the-communication-channel-for-honeyjaronft-can-be-blocked.md` | HIGH | Pashov |

### Gas Estimation & Fee Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Holograph - Gas Miscalculation | `reports/bridge_crosschain_findings/h-03-layerzeromodule-miscalculates-gas-risking-loss-of-assets.md` | HIGH | Code4rena |
| Mozaic - Gas Underestimation | `reports/bridge_crosschain_findings/trst-m-10-mozbridge-underestimates-gas-for-sending-of-moz-messages.md` | MEDIUM | Trust Security |
| TapiocaDAO - Missing quoteLayerZeroFee | `reports/bridge_crosschain_findings/m-08-missing-implementation-of-the-quotelayerzerofee-in-stargatelbphelpersol.md` | MEDIUM | Pashov |
| Mozaic - No Native Tokens | `reports/bridge_crosschain_findings/trst-h-3-all-layerzero-requests-will-fail-making-the-contracts-are-unfunctional.md` | HIGH | Trust Security |
| StationX - Incorrect Value Distribution | `reports/bridge_crosschain_findings/h-05-incorrect-value-will-get-sent-to-the-commlayer.md` | HIGH | Pashov |
| Maia DAO - Underpay ExecutionGas | `reports/bridge_crosschain_findings/h-14-user-may-underpay-for-the-remote-call-executiongas-on-the-root-chain.md` | HIGH | Code4rena |
| Maia DAO - MIN_FALLBACK_RESERVE | `reports/bridge_crosschain_findings/h-04-min_fallback_reserve-in-branchbridgeagent-doesnt-consider-the-actual-gas-co.md` | HIGH | Code4rena |

### Fee Refund Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Nexus - No Receive Function | `reports/bridge_crosschain_findings/m-01-layerzero-fee-refunds-cannot-be-processed.md` | MEDIUM | Pashov |
| LayerZeroZROClaim - lzReceive Reverts | `reports/bridge_crosschain_findings/h-02-_lzreceive-reverts-when-there-is-a-fee-refund.md` | HIGH | Pashov |
| Nexus - Refund Misdirected | `reports/bridge_crosschain_findings/m-04-layerzero-fee-refunds-misdirected-to-deposit-contracts.md` | MEDIUM | Pashov |
| StationX - No Refund Mechanism | `reports/bridge_crosschain_findings/h-11-no-refund-nor-retry-mechanism-if-the-cross-chain-transfer-failed.md` | HIGH | Pashov |
| TapiocaDAO - Refund Reverts | `reports/bridge_crosschain_findings/h-23-refund-mechanism-for-failed-cross-chain-messages-will-revert-since-moduled.md` | HIGH | Code4rena |
| Tradable - Excessive Fee Not Returned | `reports/bridge_crosschain_findings/excessive-fee-is-not-refunded-to-the-user.md` | MEDIUM | Zokyo |
| Decent - Failed Refund Wrong Address | `reports/bridge_crosschain_findings/h-03-when-decentbridgeexecutorexecute-fails-funds-will-be-sent-to-a-random-addre.md` | HIGH | Code4rena |

### Payload Size & Address Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| UXD - Large toAddress | `reports/bridge_crosschain_findings/h-2-malicious-user-can-use-an-excessively-large-_toaddress-in-oftcoresendfrom-to.md` | HIGH | Sherlock |

### Composed Message (lzCompose) Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| TempleDAO - Compose Rejected | `reports/bridge_crosschain_findings/configuring-compose-option-will-prevent-users-from-receiving-tgld-on-the-destina.md` | MEDIUM | Cyfrin |
| IDEX - lzCompose No Try-Catch | `reports/bridge_crosschain_findings/tokens-deposit-in-exchangestargatevadapterlzcompose-is.md` | HIGH | Immunefi |
| Canto - Composed Message Theft | `reports/bridge_crosschain_findings/h-02-dual-transaction-nature-of-composed-message-transfer-allows-anyone-to-steal.md` | HIGH | Code4rena |
| Maia DAO - Retry Settlement Theft | `reports/bridge_crosschain_findings/h-11-an-attacker-can-steal-accumulated-awards-from-rootbridgeagent-by-abusing-re.md` | HIGH | Code4rena |

### OFT/ONFT Specific Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Across - Decimal Mismatch | `reports/bridge_crosschain_findings/oft-transfers-revert-if-chains-have-different-local-decimals.md` | MEDIUM | OpenZeppelin |
| Across - ZRO Fee Not Validated | `reports/bridge_crosschain_findings/oft-transfer-might-revert-due-to-non-zero-zro-token-fee-quote.md` | MEDIUM | OpenZeppelin |
| HoneyJar - ONFT Channel Blocked | `reports/bridge_crosschain_findings/c-01-the-communication-channel-for-honeyjaronft-can-be-blocked.md` | HIGH | Pashov |
| LEND - Decimal Mismatch Across Chains | `reports/bridge_crosschain_findings/h-11-users-will-lose-funds-due-to-token-decimal-mismatches-across-chains.md` | HIGH | Sherlock |
| Maia DAO - Decimal Scaling Issues | `reports/bridge_crosschain_findings/h-05-multiple-issues-with-decimal-scaling-will-cause-incorrect-accounting-of-hto.md` | HIGH | Code4rena |
| Synonym - Amount Trimming | `reports/bridge_crosschain_findings/unaccounted-amount-trimming.md` | HIGH | OtterSec |
| Maia DAO - Arbitrary hToken Mint | `reports/bridge_crosschain_findings/h-12-an-attacker-can-mint-an-arbitrary-amount-of-htoken-on-rootchain.md` | HIGH | Code4rena |

### Cross-Chain Payload Theft Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| TapiocaDAO - Token Theft via exerciseOption | `reports/bridge_crosschain_findings/h-11-toft-exerciseoption-can-be-used-to-steal-all-underlying-erc20-tokens.md` | HIGH | Code4rena |
| TapiocaDAO - triggerSendFrom Balance Theft | `reports/bridge_crosschain_findings/h-13-toft-triggersendfrom-can-be-used-to-steal-all-the-balance.md` | HIGH | Code4rena |
| TapiocaDAO - retrieveFromStrategy Manipulation | `reports/bridge_crosschain_findings/h-34-basetoftsol-retrievefromstrategy-can-be-used-to-manipulate-other-users-posi.md` | HIGH | Code4rena |
| Tapioca - Remote Transfer USDO Theft | `reports/bridge_crosschain_findings/h-10-wrong-parameter-in-remote-transfer-makes-it-possible-to-steal-all-usdo-bala.md` | HIGH | Sherlock |
| Tapioca - Cross-Chain Decimal Transformation | `reports/bridge_crosschain_findings/h-7-toftoptionsreceivermodule-miss-cross-chain-transformation-for-deposit-and-lo.md` | HIGH | Sherlock |
| TapiocaDAO - Wrong Debit Address | `reports/bridge_crosschain_findings/h-05-incorrect-address-for-toft-debit.md` | HIGH | Pashov |

### Stargate/sgReceive Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Sushi - sgReceive OOG | `reports/bridge_crosschain_findings/sgreceive-could-run-out-of-gas.md` | HIGH | SigmaPrime |
| Sushi - sgReceive Native Transfer | `reports/bridge_crosschain_findings/sgreceive-could-send-native-tokens-to-a-contract.md` | MEDIUM | SigmaPrime |
| TapiocaDAO - sgReceive Permanent Error | `reports/bridge_crosschain_findings/h-02-stargatelbphelpersgreceive-could-encounter-permanent-error-that-causes-rece.md` | HIGH | Pashov |
| TapiocaDAO - Wrong Destination | `reports/bridge_crosschain_findings/h-01-stargatelbphelperparticipate-will-send-tokens-to-the-wrong-address.md` | HIGH | Pashov |
| TapiocaDAO - Hardcoded dstGasForCall | `reports/bridge_crosschain_findings/h-07-underpayingoverpaying-of-stargate-fee-will-occur-in-stargatelbphelperpartic.md` | HIGH | Pashov |
| Tapioca - ETH Stolen via RouterETH | `reports/bridge_crosschain_findings/h-6-all-eth-can-be-stolen-during-rebalancing-for-mtofts-that-hold-native.md` | HIGH | Sherlock |
| Entangle - Missing Allowance | `reports/bridge_crosschain_findings/broken-stargate-deposit-flow-due-to-missing-allowance.md` | HIGH | Halborn |
| Tradable - Refund Not Returned | `reports/bridge_crosschain_findings/excessive-fee-is-not-refunded-to-the-user.md` | MEDIUM | Zokyo |

### Cross-Chain Payload Validation Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| TapiocaDAO - Token Theft via exerciseOption | `reports/bridge_crosschain_findings/h-11-toft-exerciseoption-can-be-used-to-steal-all-underlying-erc20-tokens.md` | HIGH | Code4rena |
| TapiocaDAO - Wrong Debit Address | `reports/bridge_crosschain_findings/h-05-incorrect-address-for-toft-debit.md` | HIGH | Pashov |
| TapiocaDAO - triggerSendFrom Theft | `reports/bridge_crosschain_findings/h-13-toft-triggersendfrom-can-be-used-to-steal-all-the-balance.md` | HIGH | Code4rena |
| TapiocaDAO - retrieveFromStrategy | `reports/bridge_crosschain_findings/h-34-basetoftsol-retrievefromstrategy-can-be-used-to-manipulate-other-users-posi.md` | HIGH | Code4rena |
| Tapioca - Cross-Chain Transformation | `reports/bridge_crosschain_findings/h-7-toftoptionsreceivermodule-miss-cross-chain-transformation-for-deposit-and-lo.md` | HIGH | Sherlock |
| Tapioca - Remote Transfer USDO Theft | `reports/bridge_crosschain_findings/h-10-wrong-parameter-in-remote-transfer-makes-it-possible-to-steal-all-usdo-bala.md` | HIGH | Sherlock |
| Canto - Composed Message Theft | `reports/bridge_crosschain_findings/h-02-dual-transaction-nature-of-composed-message-transfer-allows-anyone-to-steal.md` | HIGH | Code4rena |

### Gas Limit Calculation Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| NFTMirror - Insufficient Per-Token Gas | `reports/bridge_crosschain_findings/h-02-lzreceive-call-for-releaseoneid-results-in-oog-error.md` | HIGH | Pashov |
| Maia DAO - MIN_FALLBACK_RESERVE | `reports/bridge_crosschain_findings/h-04-min_fallback_reserve-in-branchbridgeagent-doesnt-consider-the-actual-gas-co.md` | HIGH | Code4rena |
| Maia DAO - Underpay ExecutionGas | `reports/bridge_crosschain_findings/h-14-user-may-underpay-for-the-remote-call-executiongas-on-the-root-chain.md` | HIGH | Code4rena |
| Tesseract - Fixed Gas Limit | `reports/bridge_crosschain_findings/fixed-gas-limit-in-single-hop-transfers.md` | MEDIUM | OpenZeppelin |
| Wormhole NTT - Immutable Gas Limit | `reports/bridge_crosschain_findings/immutable-gas-limit-within-wormholetransceiver-can-lead-to-execution-failures-on.md` | MEDIUM | Cyfrin |

### Refund Address Misconfiguration
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Tapioca DAO - Refund Address Wrong | `reports/bridge_crosschain_findings/m-32-layerzero-fee-refund-address-is-not-handled-correctly.md` | MEDIUM | Code4rena |
| Sweep n Flip - Refund Locked | `reports/bridge_crosschain_findings/refundaddress-forwarded-to-layerzero-endpoint-is-incorrect.md` | MEDIUM | Cantina |

### Cross-Chain DAO & Deployment Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| StationX - Fee Receiver Wrong | `reports/bridge_crosschain_findings/c-01-the-layerzero-implementation-contract-is-the-receiver-of-daos-fees-on-cross.md` | HIGH | Pashov |
| StationX - Deployment Blocked | `reports/bridge_crosschain_findings/h-12-adversary-can-block-the-counterpart-deployment-of-cross-chain-daos.md` | HIGH | Pashov |
| ZeroLend - Omnichain Staking Funds Loss | `reports/bridge_crosschain_findings/omnichain-stakers-can-permanently-lose-access-to-their-funds.md` | HIGH | Immunefi |

### OFT/ONFT Fee & Bypass Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Radiant - Bridge Fee Bypass | `reports/bridge_crosschain_findings/rdnt-token-bridge-fee-can-be-bypassed.md` | HIGH | OpenZeppelin |
| Bitcorn - Fee Not Refunded | `reports/bridge_crosschain_findings/wrappedbitcornnativeoftadaptersend-doesnt-refund-excess-sent-for-layerzero-fees.md` | MEDIUM | Cantina |
| Bitcorn - Manipulated SendParam Mint | `reports/bridge_crosschain_findings/manipulated-sendparam-in-swapexactcollateralfordebtandlzsend-function-allows-una.md` | HIGH | Cantina |
| dForce - MintCap Bypass | `reports/bridge_crosschain_findings/mintcap-check-missing-in-cross-chain-transfer.md` | HIGH | MixBytes |

### Cross-Chain Slippage & Rate Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Mozaic - No Slippage Protection | `reports/bridge_crosschain_findings/trst-m-11-no-slippage-protection-for-cross-chain-swaps-in-stargateplugin.md` | MEDIUM | Trust Security |
| Sushi - sgReceive Native Transfer | `reports/bridge_crosschain_findings/sgreceive-could-send-native-tokens-to-a-contract.md` | MEDIUM | SigmaPrime |

### Trust & Remote Configuration Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Venus - Locked Funds in Bridges | `reports/bridge_crosschain_findings/potential-of-locked-funds-in-xvs-bridges.md` | MEDIUM | Quantstamp |
| Venus - Compromised Remote Messages | `reports/bridge_crosschain_findings/xvs-bridges-may-accept-messages-from-compromised-remotes.md` | MEDIUM | Quantstamp |
| OmniX - Optimistic Peer | `reports/bridge_crosschain_findings/potential-loss-of-user-funds-due-to-optimistic-peer-assumption.md` | MEDIUM | Cantina |
| Wormhole NTT - Same Chain Peer | `reports/bridge_crosschain_findings/setting-a-peer-nttmanager-contract-for-the-same-chain-can-cause-loss-of-user-fun.md` | MEDIUM | Cyfrin |

### Cross-Chain Replay Attack Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Shardeum - ChainId Replay | `reports/bridge_crosschain_findings/cross-chain-replay-attacks-are-possible-due-to.md` | HIGH | Immunefi |
| Wormhole - Hard Fork Replay | `reports/bridge_crosschain_findings/cross-chain-transactions-can-be-replayed-when-the-chain-undergoes-a-hard-fork.md` | MEDIUM | Cantina |
| RWA - borrowAsset Replay | `reports/bridge_crosschain_findings/h-01-cross-chain-replay-in-borrowasset-swaptoborrow.md` | HIGH | Kann |
| SKALE - Reentrancy Replay | `reports/bridge_crosschain_findings/h-01-reentrancy-in-messageproxyforschain-leads-to-replay-attacks.md` | HIGH | Code4rena |
| Beanstalk - Migration Replay | `reports/bridge_crosschain_findings/cross-chain-replay-attack-vulnerability-in-beanstalks-l2contractmigrationfacet.md` | MEDIUM | Codehawks |
| Next Generation - Signature Replay | `reports/bridge_crosschain_findings/h-01-cross-chain-signature-replay-attack-due-to-user-supplied-domainseparator-an.md` | HIGH | Code4rena |
| Coinbase - Owner Index Replay | `reports/bridge_crosschain_findings/h-01-remove-owner-calls-can-be-replayed-to-remove-a-different-owner-at-the-same-.md` | HIGH | Code4rena |

### Chain Reorganization & Double Spending
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Aurora FastBridge - Reorg Double Spend | `reports/bridge_crosschain_findings/block-reorg-can-allow-for-double-spending.md` | HIGH | AuditOne |
| Polkaswap - Reorg Handling | `reports/bridge_crosschain_findings/ethereum-bridge-cannot-handle-chain-reorganizations.md` | HIGH | TrailOfBits |
| Era - BridgedToken Double Spend | `reports/bridge_crosschain_findings/double-spending-of-funds-when-bridging-bridgedtoken.md` | MEDIUM | Codehawks |

### Cross-Chain Front-Running & Griefing
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Folks Finance - Loan Front-Running | `reports/bridge_crosschain_findings/front-running-vulnerability-in-cross-chain-loan-creation-process-could-lead-in-f.md` | MEDIUM | Immunefi |
| Folks Finance - Account Creation DoS | `reports/bridge_crosschain_findings/denial-of-service-vulnerability-and-possible-griefing-in-cross-chain-account-cre.md` | MEDIUM | Immunefi |
| Folks Finance - Loan ID Griefing | `reports/bridge_crosschain_findings/attacker-can-create-loan-before-users-tx-is-completed-through-bridge.md` | MEDIUM | Immunefi |
| Camp - Min Gas Griefing | `reports/bridge_crosschain_findings/griefing-users-can-cause-deposits-to-fail-on-the-destination-chain-due-to-lack-o.md` | MEDIUM | Quantstamp |

### Cross-Chain Token Locking & Stuck Funds
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Scroll - ETH Stuck on Bridge | `reports/bridge_crosschain_findings/eth-deposits-can-get-stuck-if-they-are-not-successfully-bridged.md` | HIGH | OpenZeppelin |
| Linea - ERC721 Token Lock | `reports/bridge_crosschain_findings/erc-721-tokens-can-be-locked-on-the-token-bridge.md` | HIGH | OpenZeppelin |
| Mantle - Cap Exceeded Lock | `reports/bridge_crosschain_findings/cross-chain-transfers-exceeding-the-cap-are-temporarily-locked.md` | MEDIUM | MixBytes |
| stake.link - reSDL Lock Theft | `reports/bridge_crosschain_findings/a-user-can-steal-an-already-transfered-and-bridged-resdl-lock-because-of-approva.md` | HIGH | Codehawks |

### Cross-Chain Call Failure & Reverts
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Axelar - Tokens Burned But Call Fails | `reports/bridge_crosschain_findings/h-01-cross-chain-smart-contract-calls-can-revert-but-source-chain-tokens-remain-.md` | HIGH | Code4rena |
| Across - Cost Asymmetry Spam Attack | `reports/bridge_crosschain_findings/exploitation-of-cost-asymmetries-across-chains-to-impose-high-gas-costs-on-refun.md` | HIGH | OpenZeppelin |
| Dhedge - L2Comptroller Message Order | `reports/bridge_crosschain_findings/h-01-user-can-receive-too-few-tokens-when-l2comptroller-is-unpaused.md` | HIGH | ZachObront |

### Bridge Freeze & Denial of Service
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Gravity Bridge - Non-UTF8 Freeze | `reports/bridge_crosschain_findings/h-02-freeze-bridge-via-non-utf8-token-namesymboldenom.md` | HIGH | Code4rena |
| Gravity Bridge - Large ERC20 Freeze | `reports/bridge_crosschain_findings/h-03-freeze-the-bridge-via-large-erc20-namessymbolsdenoms.md` | HIGH | Code4rena |
| Axelar - ITSHub Balance Block | `reports/bridge_crosschain_findings/h-02-can-block-bridge-or-limit-the-bridgeable-amount-by-initializing-the-itshub-.md` | HIGH | Code4rena |

### L2 Sequencer Downtime Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Wormhole NTT - Sequencer Down Access | `reports/bridge_crosschain_findings/access-controlled-functions-cannot-be-called-when-l2-sequencers-are-down.md` | MEDIUM | Cyfrin |

### Cross-Chain State Synchronization Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Autonomint - LayerZero State Overwrite | `reports/bridge_crosschain_findings/h-26-using-layerzero-for-synchronizing-global-states-between-two-chains-may-lead.md` | HIGH | Sherlock |
| Nibiru - EVM Bank Balance Desync | `reports/bridge_crosschain_findings/h-03-unlimited-nibi-could-be-minted-because-evm-and-bank-balance-are-not-synced-.md` | HIGH | Code4rena |
| Axelar - Rebasing Token Balance Tracking | `reports/bridge_crosschain_findings/m-01-axelar-cross-chain-token-transfers-balance-tracking-logic-is-completely-bro.md` | MEDIUM | Code4rena |
| Sweep n Flip - Irrecoverable State | `reports/bridge_crosschain_findings/layerzeroadapterexecutemessages-could-lead-to-irrecoverable-state.md` | HIGH | Cantina |

### Cross-Chain Authentication Bypass Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Derby - Message Authentication Bypass | `reports/bridge_crosschain_findings/h-6-cross-chain-message-authentication-can-be-bypassed-allowing-an-attacker-to-d.md` | HIGH | Sherlock |
| Folks Finance - AdapterId Access Control | `reports/bridge_crosschain_findings/incorrect-access-control-in-receivemessage-leads-to-total-loss-of-funds.md` | MEDIUM | Immunefi |
| Taiko - Cross-Chain Owner msg.sender | `reports/bridge_crosschain_findings/cross-chain-owner-cannot-call-privileged-functions-phase-2.md` | MEDIUM | OpenZeppelin |
| Alongside - Remote Token Theft | `reports/bridge_crosschain_findings/m-02-owner-can-steal-all-funds-locked-in-bridge-by-changing-remote_token-value.md` | MEDIUM | ZachObront |

### Cross-Chain Reentrancy Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| SKALE - Replay via Reentrancy | `reports/bridge_crosschain_findings/h-01-reentrancy-in-messageproxyforschain-leads-to-replay-attacks.md` | HIGH | Code4rena |
| Linea - Token Accounting Corruption | `reports/bridge_crosschain_findings/token-bridge-reentrancy-can-corrupt-token-accounting.md` | HIGH | OpenZeppelin |
| Centrifuge - Adapter Batch Reentrancy | `reports/bridge_crosschain_findings/m-6-malicious-adapters-can-exploit-message-batching-via-adapter-side-reentrancy-.md` | MEDIUM | Sherlock |

### Cross-Chain Signature Replay Attack Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Next Generation - DomainSeparator Replay | `reports/bridge_crosschain_findings/h-01-cross-chain-signature-replay-attack-due-to-user-supplied-domainseparator-an.md` | HIGH | Code4rena |
| Biconomy - Missing ChainId | `reports/bridge_crosschain_findings/m-03-cross-chain-signature-replay-attack.md` | MEDIUM | Code4rena |

### Cross-Chain Slippage Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Astrolab - No Slippage Protection | `reports/bridge_crosschain_findings/astro-22-no-slippage-protection-for-bridgefunds.md` | HIGH | Hexens |
| Toki Bridge - Destination Slippage Broken | `reports/bridge_crosschain_findings/m-01-destination-slippage-protections-broken-by-amount-drift.md` | MEDIUM | Shieldify |

### Cross-Chain Encoding & Hash Collision Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Pheasant Network - abi.encodePacked Hash Collision | `reports/bridge_crosschain_findings/using-abiencodepackedcan-lead-to-hash-collisions.md` | HIGH | Quantstamp |

### Cross-Chain Issuance Cap & Limit Bypass Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Securitize - totalIssuance Cap Inflation | `reports/bridge_crosschain_findings/bridging-dstoken-back-and-forth-between-chains-causes-totalissuance-cap-to-be-re.md` | MEDIUM | Cyfrin |
| Lucid Labs - Bridge Limits Bypass | `reports/bridge_crosschain_findings/bypass-of-bridge-limits-in-burnandbridgemulti-function.md` | HIGH | Halborn |
| Mantle - Cap Exceeded Token Lock | `reports/bridge_crosschain_findings/cross-chain-transfers-exceeding-the-cap-are-temporarily-locked.md` | MEDIUM | MixBytes |

### Arbitrary Cross-Chain Minting Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Maia DAO - Arbitrary hToken Mint | `reports/bridge_crosschain_findings/h-12-an-attacker-can-mint-an-arbitrary-amount-of-htoken-on-rootchain.md` | HIGH | Code4rena |

### Cross-Chain Decimal & Precision Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Connext - Slippage Decimal Mismatch | `reports/bridge_crosschain_findings/_slippagetol-does-not-adjust-for-decimal-differences.md` | MEDIUM | Spearbit |
| Fuel - Decimal Precision Oversight | `reports/bridge_crosschain_findings/fuel1-13-decimal-precision-oversight-in-cross-layer-token-transactions.md` | HIGH | Hexens |

### Cross-Chain Fee Handling Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Synonym - Relayer Fee Discrepancy | `reports/bridge_crosschain_findings/discrepancy-in-handling-relayer-fee.md` | HIGH | OtterSec |
| Tradable - Fee Not Refunded | `reports/bridge_crosschain_findings/excessive-fee-is-not-refunded-to-the-user.md` | MEDIUM | Zokyo |

### Cross-Chain Validator/Relayer Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Chakra - Duplicate Validator Signatures | `reports/bridge_crosschain_findings/h-03-settlementsignatureverifier-is-missing-check-for-duplicate-validator-signat.md` | HIGH | Code4rena |
| SEDA - Validator Consensus Bypass | `reports/bridge_crosschain_findings/h-2-malicious-validators-will-bypass-consensus-threshold-requirements-affecting-.md` | HIGH | Sherlock |
| Across - Relayer Refund Drain | `reports/bridge_crosschain_findings/anyone-can-lock-relayer-refunds-and-contract-can-be-drained.md` | HIGH | OpenZeppelin |

### Cross-Chain Address & Token Mapping Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Chakra - Invalid Token Address | `reports/bridge_crosschain_findings/h-01-invalid-token-address-used-in-chakrasettlementhandlercross_chain_erc20_sett.md` | HIGH | Code4rena |

### External Links
- [LayerZero Documentation](https://layerzero.gitbook.io/docs/)
- [LayerZero V2 Documentation](https://docs.layerzero.network/v2)
- [LayerZero Integration Checklist](https://layerzero.gitbook.io/docs/troubleshooting/layerzero-integration-checklist)
- [NonblockingLzApp Example](https://github.com/LayerZero-Labs/solidity-examples/blob/main/contracts/lzApp/NonblockingLzApp.sol)
- [OFT Standard](https://docs.layerzero.network/v2/developers/evm/oft/quickstart)
- [Stargate Documentation](https://stargateprotocol.gitbook.io/stargate/)

---

# LayerZero Integration Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for LayerZero Cross-Chain Security Audits**

---

## Table of Contents

1. [Channel Blocking Vulnerabilities](#1-channel-blocking-vulnerabilities)
2. [Minimum Gas Validation Vulnerabilities](#2-minimum-gas-validation-vulnerabilities)
3. [Gas Estimation & Fee Calculation](#3-gas-estimation--fee-calculation)
4. [Fee Refund Handling](#4-fee-refund-handling)
5. [Payload Size & Address Validation](#5-payload-size--address-validation)
6. [Composed Message Vulnerabilities](#6-composed-message-vulnerabilities-layerzero-v2)
7. [OFT/ONFT Specific Vulnerabilities](#7-oftonft-specific-vulnerabilities)
8. [Peer & Trust Configuration Vulnerabilities](#8-peer--trust-configuration-vulnerabilities)
9. [Stargate/sgReceive Integration Vulnerabilities](#9-stargatesgreceive-integration-vulnerabilities)
10. [Cross-Chain Payload Validation Vulnerabilities](#10-cross-chain-payload-validation-vulnerabilities)
11. [Insufficient Gas Limit Calculation](#11-insufficient-gas-limit-calculation)

---

## 1. Channel Blocking Vulnerabilities

### Overview

LayerZero's default behavior is **blocking** - when a message fails on the destination chain, the channel between source and destination is blocked until the failed message is successfully retried. This can be exploited by attackers to permanently DoS cross-chain communication.

> **📚 Source Reports for Deep Dive:**
> - `reports/bridge_crosschain_findings/h-06-attacker-can-block-layerzero-channel.md` (Velodrome - Code4rena)
> - `reports/bridge_crosschain_findings/h-16-attacker-can-block-layerzero-channel-due-to-variable-gas-cost-of-saving-pay.md` (Tapioca - Code4rena)
> - `reports/bridge_crosschain_findings/h-17-attacker-can-block-layerzero-channel-due-to-missing-check-of-minimum-gas-pa.md` (Tapioca - Code4rena)

### Vulnerability Description

#### Root Cause

Protocols inherit from `LzApp` without implementing the non-blocking pattern (`NonblockingLzApp`), or they implement it incorrectly. When `lzReceive()` reverts, the message is stored in `storedPayload` and blocks all subsequent messages.

#### Attack Scenario

1. Attacker identifies a cross-chain contract without non-blocking implementation
2. Attacker sends a message designed to revert on destination (insufficient gas, malicious payload)
3. Message fails and is stored in `storedPayload`
4. All subsequent messages from that source chain are blocked
5. Protocol becomes permanently DoS'd unless `forceResumeReceive` is implemented

### Vulnerable Pattern Examples

**Example 1: Missing Non-Blocking Pattern** [HIGH]
> 📖 Reference: `reports/bridge_crosschain_findings/h-06-attacker-can-block-layerzero-channel.md`
```solidity
// ❌ VULNERABLE: Inherits LzApp directly without non-blocking wrapper
contract RedemptionReceiver is LzApp {
    function lzReceive(
        uint16 _srcChainId,
        bytes memory _srcAddress,
        uint64 _nonce,
        bytes memory _payload
    ) external override {
        // Any revert here will block the channel
        _processPayload(_payload);  // If this reverts, channel is blocked
    }
}
```

**Example 2: Gas Draining to Force Blocking** [HIGH]
> 📖 Reference: `reports/bridge_crosschain_findings/h-16-attacker-can-block-layerzero-channel-due-to-variable-gas-cost-of-saving-pay.md`
```solidity
// ❌ VULNERABLE: External calls before NonblockingLzApp catch
contract BaseTOFT is NonblockingLzApp {
    function _nonblockingLzReceive(
        uint16 _srcChainId,
        bytes memory _srcAddress,
        uint64 _nonce,
        bytes memory _payload
    ) internal override {
        // Attacker can pass malicious contract that drains gas
        ISendFrom(rewardToken).sendFrom(...);  // Gas drained here
        
        // Never reaches the non-blocking catch block
        // because gas exhausted in external call
    }
}
```

**Example 3: Missing forceResumeReceive** [HIGH]
```solidity
// ❌ VULNERABLE: No recovery mechanism
contract BridgeReceiver is LzApp {
    // Missing forceResumeReceive implementation
    // If channel gets blocked, no way to unblock it
    
    function lzReceive(...) external override {
        require(msg.sender == address(lzEndpoint), "Invalid endpoint");
        _processMessage(_payload);
    }
}
```

### Impact Analysis

#### Technical Impact
- **Channel DoS**: All messages from affected source chain are blocked
- **Permanent Blocking**: Without `forceResumeReceive`, channel may be permanently blocked
- **State Corruption**: Pending messages cannot be processed

#### Business Impact
- **Protocol Unusable**: Cross-chain functionality completely disabled
- **User Funds Locked**: Tokens in transit may be stuck
- **Trust Loss**: Users lose confidence in protocol's reliability

#### Affected Scenarios
- Protocols without `NonblockingLzApp` implementation
- External calls before non-blocking try-catch
- Missing `forceResumeReceive` implementation
- No gas limit validation on user-supplied parameters

### Secure Implementation

**Fix 1: Use NonblockingLzApp Correctly**
```solidity
// ✅ SECURE: Proper NonblockingLzApp implementation
contract SecureBridgeReceiver is NonblockingLzApp {
    mapping(uint16 => mapping(bytes => mapping(uint64 => bytes32))) public failedMessages;
    
    function _nonblockingLzReceive(
        uint16 _srcChainId,
        bytes memory _srcAddress,
        uint64 _nonce,
        bytes memory _payload
    ) internal override {
        // Wrap in try-catch for additional safety
        try this.processPayload(_srcChainId, _payload) {
            // Success
        } catch {
            // Store failed message for retry
            failedMessages[_srcChainId][_srcAddress][_nonce] = keccak256(_payload);
            emit MessageFailed(_srcChainId, _srcAddress, _nonce, _payload);
        }
    }
    
    function retryMessage(
        uint16 _srcChainId,
        bytes memory _srcAddress,
        uint64 _nonce,
        bytes memory _payload
    ) external {
        bytes32 payloadHash = failedMessages[_srcChainId][_srcAddress][_nonce];
        require(payloadHash != bytes32(0), "No stored message");
        require(keccak256(_payload) == payloadHash, "Invalid payload");
        
        delete failedMessages[_srcChainId][_srcAddress][_nonce];
        this.processPayload(_srcChainId, _payload);
    }
}
```

**Fix 2: Implement forceResumeReceive**
```solidity
// ✅ SECURE: Emergency recovery mechanism
contract SecureLzApp is LzApp {
    function forceResumeReceive(uint16 _srcChainId, bytes calldata _srcAddress) external onlyOwner {
        lzEndpoint.forceResumeReceive(_srcChainId, _srcAddress);
    }
}
```

---

## 2. Minimum Gas Validation Vulnerabilities

### Overview

LayerZero allows senders to specify gas through `adapterParams`. If protocols don't enforce minimum gas requirements, attackers can send messages with insufficient gas that revert on destination, blocking the channel.

> **📚 Source Reports for Deep Dive:**
> - `reports/bridge_crosschain_findings/h-17-attacker-can-block-layerzero-channel-due-to-missing-check-of-minimum-gas-pa.md` (Tapioca - Code4rena)
> - `reports/bridge_crosschain_findings/h-02-due-to-missing-checks-on-minimum-gas-passed-through-layerzero-executions-ca.md` (Decent - Code4rena)

### Vulnerability Description

#### Root Cause

Protocols allow users to specify arbitrary `adapterParams` without validating the gas limit meets minimum requirements for the destination chain operation.

#### Attack Scenario

1. Attacker calls a cross-chain function with minimal gas in `adapterParams`
2. LayerZero relayer delivers message with specified gas
3. Transaction reverts due to out-of-gas before reaching `NonblockingLzApp` catch
4. Message is stored in `storedPayload`, blocking channel

### Vulnerable Pattern Examples

**Example 1: No AdapterParams Validation** [HIGH]
> 📖 Reference: `reports/bridge_crosschain_findings/h-17-attacker-can-block-layerzero-channel-due-to-missing-check-of-minimum-gas-pa.md`
```solidity
// ❌ VULNERABLE: User controls gas amount without validation
function triggerSendFrom(
    address _from,
    uint16 _dstChainId,
    bytes calldata _toAddress,
    uint _amount,
    bytes calldata _adapterParams  // User can pass minimal gas
) external payable {
    _lzSend(
        _dstChainId,
        abi.encode(_from, _toAddress, _amount),
        payable(msg.sender),
        address(0),
        _adapterParams,  // No validation!
        msg.value
    );
}
```

**Example 2: Hardcoded Insufficient Gas** [HIGH]
> 📖 Reference: `reports/bridge_crosschain_findings/h-02-due-to-missing-checks-on-minimum-gas-passed-through-layerzero-executions-ca.md`
```solidity
// ❌ VULNERABLE: Hardcoded gas too low for some operations
contract DecentEthRouter {
    uint256 GAS_FOR_RELAY = 100000;  // May be insufficient
    
    function bridge(..., uint64 _dstGasForCall, ...) public payable {
        uint256 gasAmount = GAS_FOR_RELAY + _dstGasForCall;  // User controls _dstGasForCall
        // No minimum validation on _dstGasForCall
    }
}
```

### Secure Implementation

**Fix 1: Enforce Minimum Gas**
```solidity
// ✅ SECURE: Validate minimum gas per message type
contract SecureLzSender is LzApp {
    mapping(uint16 => uint256) public minDstGasLookup;
    
    function setMinDstGas(uint16 _dstChainId, uint256 _minGas) external onlyOwner {
        minDstGasLookup[_dstChainId] = _minGas;
    }
    
    function _lzSend(
        uint16 _dstChainId,
        bytes memory _payload,
        address payable _refundAddress,
        address _zroPaymentAddress,
        bytes memory _adapterParams,
        uint _nativeFee
    ) internal virtual override {
        uint256 gasLimit = _getGasLimit(_adapterParams);
        require(gasLimit >= minDstGasLookup[_dstChainId], "Gas too low");
        
        super._lzSend(_dstChainId, _payload, _refundAddress, _zroPaymentAddress, _adapterParams, _nativeFee);
    }
    
    function _getGasLimit(bytes memory _adapterParams) internal pure returns (uint256 gasLimit) {
        require(_adapterParams.length >= 34, "Invalid adapterParams");
        assembly {
            gasLimit := mload(add(_adapterParams, 34))
        }
    }
}
```

**Fix 2: Use LayerZero's setMinDstGas**
```solidity
// ✅ SECURE: Use built-in minimum gas configuration
contract SecureOFT is OFT {
    constructor(...) OFT(...) {
        // Set minimum gas for each packet type per chain
        setMinDstGas(ARBITRUM_CHAIN_ID, PT_SEND, 200000);
        setMinDstGas(ARBITRUM_CHAIN_ID, PT_SEND_AND_CALL, 500000);
        setMinDstGas(OPTIMISM_CHAIN_ID, PT_SEND, 200000);
    }
}
```

---

## 3. Gas Estimation & Fee Calculation

### Overview

Incorrect gas estimation for cross-chain messages leads to either overpaying (wasted funds) or underpaying (failed execution, potential fund loss).

> **📚 Source Reports for Deep Dive:**
> - `reports/bridge_crosschain_findings/h-03-layerzeromodule-miscalculates-gas-risking-loss-of-assets.md` (Holograph - Code4rena)
> - `reports/bridge_crosschain_findings/trst-m-10-mozbridge-underestimates-gas-for-sending-of-moz-messages.md` (Mozaic - Trust)
> - `reports/bridge_crosschain_findings/trst-h-3-all-layerzero-requests-will-fail-making-the-contracts-are-unfunctional.md` (Mozaic - Trust)

### Vulnerable Pattern Examples

**Example 1: Using Source Chain Gas Costs for Destination** [HIGH]
> 📖 Reference: `reports/bridge_crosschain_findings/h-03-layerzeromodule-miscalculates-gas-risking-loss-of-assets.md`
```solidity
// ❌ VULNERABLE: Uses source chain gas config for destination
contract LayerZeroModule {
    uint256 private _baseGas;  // Single value for all chains!
    uint256 private _gasPerByte;
    
    function send(..., bytes calldata crossChainPayload) external payable {
        // Wrong: _baseGas and _gasPerByte are for source chain
        lZEndpoint.send{value: msgValue}(
            dstChainId,
            abi.encodePacked(address(this), address(this)),
            crossChainPayload,
            payable(msgSender),
            address(this),
            abi.encodePacked(
                uint16(1),
                uint256(_baseGas() + (crossChainPayload.length * _gasPerByte()))  // Source chain values!
            )
        );
    }
}
```

**Example 2: Incorrect Payload for Fee Estimation** [MEDIUM]
> 📖 Reference: `reports/bridge_crosschain_findings/trst-m-10-mozbridge-underestimates-gas-for-sending-of-moz-messages.md`
```solidity
// ❌ VULNERABLE: Fee estimation uses different payload than actual send
function quoteLayerZeroFee(uint16 _chainId, uint16 _msgType, ...) public view returns (uint256, uint256) {
    bytes memory payload = "";
    if (_msgType == TYPE_REPORT_SNAPSHOT) {
        payload = abi.encode(TYPE_REPORT_SNAPSHOT);  // Wrong! Actual includes Snapshot struct
    }
    // Actual payload is longer, causing underestimation
    return layerZeroEndpoint.estimateFees(_chainId, address(this), payload, ...);
}
```

**Example 3: No Native Token Value Sent** [HIGH]
> 📖 Reference: `reports/bridge_crosschain_findings/trst-h-3-all-layerzero-requests-will-fail-making-the-contracts-are-unfunctional.md`
```solidity
// ❌ VULNERABLE: No value passed for LayerZero fees
function requestSnapshot() external {
    bridge.send(...);  // No msg.value! All LZ calls fail
}
```

### Secure Implementation

**Fix 1: Per-Chain Gas Configuration**
```solidity
// ✅ SECURE: Chain-specific gas configuration
contract SecureLayerZeroModule {
    mapping(uint16 => uint256) public dstChainBaseGas;
    mapping(uint16 => uint256) public dstChainGasPerByte;
    
    function setDstChainGasConfig(
        uint16 _dstChainId,
        uint256 _baseGas,
        uint256 _gasPerByte
    ) external onlyOwner {
        dstChainBaseGas[_dstChainId] = _baseGas;
        dstChainGasPerByte[_dstChainId] = _gasPerByte;
    }
    
    function send(uint16 _dstChainId, bytes calldata _payload) external payable {
        uint256 gasAmount = dstChainBaseGas[_dstChainId] + 
            (_payload.length * dstChainGasPerByte[_dstChainId]);
        // Use destination-specific values
    }
}
```

**Fix 2: Accurate Fee Estimation**
```solidity
// ✅ SECURE: Use actual payload for estimation
function quoteLayerZeroFee(
    uint16 _chainId,
    Snapshot memory _snapshot
) public view returns (uint256 nativeFee) {
    bytes memory actualPayload = abi.encode(TYPE_REPORT_SNAPSHOT, _snapshot);
    (nativeFee,) = layerZeroEndpoint.estimateFees(
        _chainId,
        address(this),
        actualPayload,  // Same as actual send
        false,
        _adapterParams
    );
}
```

---

## 4. Fee Refund Handling

### Overview

LayerZero refunds excess fees to the specified refund address. If contracts cannot receive ETH or the refund address is incorrect, funds are lost or transactions revert.

> **📚 Source Reports for Deep Dive:**
> - `reports/bridge_crosschain_findings/m-01-layerzero-fee-refunds-cannot-be-processed.md` (Nexus - Pashov)
> - `reports/bridge_crosschain_findings/h-02-_lzreceive-reverts-when-there-is-a-fee-refund.md` (LayerZero ZRO Claim - Pashov)
> - `reports/bridge_crosschain_findings/m-04-layerzero-fee-refunds-misdirected-to-deposit-contracts.md` (Nexus - Pashov)

### Vulnerable Pattern Examples

**Example 1: Missing receive() Function** [HIGH]
> 📖 Reference: `reports/bridge_crosschain_findings/h-02-_lzreceive-reverts-when-there-is-a-fee-refund.md`
```solidity
// ❌ VULNERABLE: Contract cannot receive refunds
contract ClaimLocal is OApp {
    // Missing receive() or fallback()!
    
    function _lzReceive(...) internal override {
        IOFT(zroToken).send{value: msg.value}(
            sendParams,
            MessagingFee(msg.value, 0),
            address(this)  // Refund to this contract - will revert!
        );
    }
}
```

**Example 2: Refund to Wrong Address** [MEDIUM]
> 📖 Reference: `reports/bridge_crosschain_findings/m-04-layerzero-fee-refunds-misdirected-to-deposit-contracts.md`
```solidity
// ❌ VULNERABLE: Refunds go to contract, not user
function sendMessage(bytes memory _data, uint32 _destId, uint256 _lzFee) 
    external payable onlyDeposit 
{
    _lzSend(
        _destId,
        _data,
        optionsDestId[_destId],
        MessagingFee(_lzFee, 0),
        payable(msg.sender)  // msg.sender is deposit contract, not user!
    );
}
```

### Secure Implementation

**Fix 1: Add receive() Function**
```solidity
// ✅ SECURE: Contract can receive ETH refunds
contract SecureOApp is OApp {
    receive() external payable {}
    
    function withdrawRefunds() external onlyOwner {
        payable(owner()).transfer(address(this).balance);
    }
}
```

**Fix 2: Pass User as Refund Address**
```solidity
// ✅ SECURE: Refund to actual user
function sendMessage(
    bytes memory _data,
    uint32 _destId,
    uint256 _lzFee,
    address refundAddress  // User address passed explicitly
) external payable onlyDeposit {
    _lzSend(
        _destId,
        _data,
        optionsDestId[_destId],
        MessagingFee(_lzFee, 0),
        payable(refundAddress)  // Correct refund address
    );
}
```

---

## 5. Payload Size & Address Validation

### Overview

LayerZero allows arbitrary payload sizes and address lengths. Malicious users can exploit this to create messages that cannot be processed on destination chains with different gas limits.

> **📚 Source Reports for Deep Dive:**
> - `reports/bridge_crosschain_findings/h-2-malicious-user-can-use-an-excessively-large-_toaddress-in-oftcoresendfrom-to.md` (UXD - Sherlock)

### Vulnerable Pattern Examples

**Example 1: Unbounded toAddress Length** [HIGH]
> 📖 Reference: `reports/bridge_crosschain_findings/h-2-malicious-user-can-use-an-excessively-large-_toaddress-in-oftcoresendfrom-to.md`
```solidity
// ❌ VULNERABLE: No limit on _toAddress length
function sendFrom(
    address _from,
    uint16 _dstChainId,
    bytes calldata _toAddress,  // Can be megabytes!
    uint _amount,
    ...
) public payable virtual override {
    _send(_from, _dstChainId, _toAddress, _amount, ...);
    // Massive _toAddress can cause OOG on destination
}
```

### Secure Implementation

**Fix: Limit Address Length**
```solidity
// ✅ SECURE: Validate address length
function sendFrom(
    address _from,
    uint16 _dstChainId,
    bytes calldata _toAddress,
    uint _amount,
    ...
) public payable virtual override {
    require(_toAddress.length <= 32, "Address too long");  // Max 32 bytes (Solana)
    _send(_from, _dstChainId, _toAddress, _amount, ...);
}
```

---

## 6. Composed Message Vulnerabilities (LayerZero V2)

### Overview

LayerZero V2 introduces composed messages (lzCompose) that enable multi-hop cross-chain transactions. Improper handling of composed messages can lead to fund loss, stuck tokens, or blocked channels.

> **📚 Source Reports for Deep Dive:**
> - `reports/bridge_crosschain_findings/configuring-compose-option-will-prevent-users-from-receiving-tgld-on-the-destina.md` (TempleDAO - Cyfrin)
> - `reports/bridge_crosschain_findings/tokens-deposit-in-exchangestargatevadapterlzcompose-is.md` (IDEX - Immunefi)

### Vulnerability Description

#### Root Cause

Composed messages introduce dual-transaction patterns where the initial receive and subsequent compose execution are separate transactions. Failures in either stage can leave tokens stranded or prevent message completion.

### Vulnerable Pattern Examples

**Example 1: Rejecting Composed Messages** [MEDIUM]
> 📖 Reference: `reports/bridge_crosschain_findings/configuring-compose-option-will-prevent-users-from-receiving-tgld-on-the-destina.md`
```solidity
// ❌ VULNERABLE: Rejects compose when user sends with compose option
contract TempleGold is OFT {
    function _lzReceive(..., bytes calldata _message, ...) internal override {
        // Blocks all messages with compose
        if (_message.isComposed()) { 
            revert CannotCompose();  // User loses tokens!
        }
        // ...
    }
}

// User calls send() with compose option set - tokens are burned on source
// but rejected on destination, leading to fund loss
```

**Example 2: lzCompose Without Try-Catch** [HIGH]
> 📖 Reference: `reports/bridge_crosschain_findings/tokens-deposit-in-exchangestargatevadapterlzcompose-is.md`
```solidity
// ❌ VULNERABLE: No error handling in lzCompose
contract ExchangeStargateV2Adapter {
    function lzCompose(
        address _from,
        bytes32 /* _guid */,
        bytes calldata _message,
        address /* _executor */,
        bytes calldata /* _extraData */
    ) public payable override {
        uint256 amountLD = OFTComposeMsgCodec.amountLD(_message);
        address destinationWallet = abi.decode(OFTComposeMsgCodec.composeMsg(_message), (address));
        
        // No try-catch! If deposits are disabled, tokens are stuck
        IExchange(custodian.exchange()).deposit(amountLD, destinationWallet);
    } 
}
```

**Example 3: Compose Stealing Tokens** [HIGH]
> 📖 Reference: `reports/bridge_crosschain_findings/h-02-dual-transaction-nature-of-composed-message-transfer-allows-anyone-to-stea.md`
```solidity
// ❌ VULNERABLE: Anyone can call lzCompose after tokens arrive
// Due to dual-transaction nature, tokens sit in contract between 
// lzReceive (transfers tokens) and lzCompose (executes logic)
// Attacker can front-run lzCompose to steal tokens
```

### Secure Implementation

**Fix 1: Validate SendParam to Prevent Compose Issues**
```solidity
// ✅ SECURE: Prevent users from sending with compose if not supported
function send(SendParam calldata _sendParam, ...) external payable override {
    // Reject if compose option is set when not supported
    require(_sendParam.composeMsg.length == 0, "Compose not supported");
    super.send(_sendParam, ...);
}
```

**Fix 2: Implement Try-Catch in lzCompose**
```solidity
// ✅ SECURE: Handle compose failures gracefully
function lzCompose(
    address _from,
    bytes32 _guid,
    bytes calldata _message,
    address _executor,
    bytes calldata _extraData
) public payable override {
    uint256 amountLD = OFTComposeMsgCodec.amountLD(_message);
    address destinationWallet = abi.decode(OFTComposeMsgCodec.composeMsg(_message), (address));
    
    try IExchange(custodian.exchange()).deposit(amountLD, destinationWallet) {
        // Success
    } catch {
        // Transfer tokens to destination wallet instead
        IERC20(token).safeTransfer(destinationWallet, amountLD);
        emit ComposeFailed(destinationWallet, amountLD);
    }
}
```

---

## 7. OFT/ONFT Specific Vulnerabilities

### Overview

OFT (Omnichain Fungible Token) and ONFT (Omnichain NFT) standards have specific vulnerabilities related to decimal handling, token minting/burning, and cross-chain state consistency.

> **📚 Source Reports for Deep Dive:**
> - `reports/bridge_crosschain_findings/oft-transfers-revert-if-chains-have-different-local-decimals.md` (Across - OpenZeppelin)
> - `reports/bridge_crosschain_findings/oft-transfer-might-revert-due-to-non-zero-zro-token-fee-quote.md` (Across - OpenZeppelin)
> - `reports/bridge_crosschain_findings/c-01-the-communication-channel-for-honeyjaronft-can-be-blocked.md` (HoneyJar - Pashov)
> - `reports/bridge_crosschain_findings/unaccounted-amount-trimming.md` (Synonym - OtterSec)

### Vulnerable Pattern Examples

**Example 1: Decimal Mismatch Between Chains** [MEDIUM]
> 📖 Reference: `reports/bridge_crosschain_findings/oft-transfers-revert-if-chains-have-different-local-decimals.md`
```solidity
// ❌ VULNERABLE: Doesn't account for different decimals on chains
function _transferViaOFT(..., uint256 _amount, ...) internal {
    // ...
    (uint256 amountSentLD, uint256 amountReceivedLD) = oft.send(...);
    
    // This check fails if decimals differ between chains!
    // amountReceivedLD is in destination chain decimals
    // _amount is in source chain decimals
    require(amountReceivedLD >= _amount, "Insufficient received");
}
```

**Example 2: ZRO Token Fee Not Validated** [MEDIUM]
> 📖 Reference: `reports/bridge_crosschain_findings/oft-transfer-might-revert-due-to-non-zero-zro-token-fee-quote.md`
```solidity
// ❌ VULNERABLE: Doesn't validate lzTokenFee is zero
function _transferViaOFT(...) internal {
    // Quote may return both native and ZRO fees
    MessagingFee memory fee = oft.quoteSend(sendParams, false);
    
    // If lzTokenFee > 0, the messenger might not recognize payment type
    // and could revert trying to collect ZRO tokens
    oft.send{value: fee.nativeFee}(sendParams, fee, refundAddress);
}
```

**Example 3: ONFT Batch Transfer OOG** [HIGH]
> 📖 Reference: `reports/bridge_crosschain_findings/c-01-the-communication-channel-for-honeyjaronft-can-be-blocked.md`
```solidity
// ❌ VULNERABLE: Event building after _creditTill can run out of gas
function _nonblockingLzReceive(..., bytes memory _payload) internal override {
    (address toAddress, TokenPayload[] memory tokens) = _decodeSendNFT(_payload);
    
    // _creditTill checks gas and stores for retry if needed
    uint256 nextIndex = _creditTill(_srcChainId, toAddress, 0, tokens);
    if (nextIndex < tokens.length) {
        bytes32 hashedPayload = keccak256(_payload);
        storedCredits[hashedPayload] = StoredCredit(...);
    }
    
    // BUG: This loop can consume remaining gas and cause revert
    // The revert won't be caught by NonblockingLzApp!
    uint256[] memory tokenIds = new uint256[](tokens.length);
    for (uint256 i = 0; i < tokens.length; i++) {
        tokenIds[i] = tokens[i].tokenId;
    }
    emit ReceiveFromChain(_srcChainId, _srcAddress, toAddress, tokenIds);
}
```

**Example 4: Amount Trimming Not Accounted** [HIGH]
> 📖 Reference: `reports/bridge_crosschain_findings/unaccounted-amount-trimming.md`
```solidity
// ❌ VULNERABLE: Wormhole/LayerZero normalizes to 8 decimals
// Tokens with 18 decimals lose precision (dust)
function bridgeTokens(uint256 amount) external {
    // Amount: 1000000000000000001 (1e18 + 1 wei)
    // After normalization: 1000000000000000000 (1e18)
    // Dust (1 wei) stays in bridge contract
    
    wormholeTokenBridge.transferTokens(..., amount, ...);
    // amount forwarded doesn't match what was deducted from user
}
```

### Secure Implementation

**Fix 1: Handle Decimal Differences**
```solidity
// ✅ SECURE: Account for decimal normalization
function _transferViaOFT(..., uint256 _amount, ...) internal {
    uint8 srcDecimals = IERC20Metadata(token).decimals();
    uint8 sharedDecimals = oft.sharedDecimals();
    
    // Trim dust before comparison
    uint256 normalizedAmount = _removeDust(_amount, srcDecimals, sharedDecimals);
    
    (uint256 amountSentLD, uint256 amountReceivedLD) = oft.send(...);
    require(amountReceivedLD >= normalizedAmount, "Insufficient received");
}
```

**Fix 2: Validate ZRO Fee is Zero**
```solidity
// ✅ SECURE: Assert no ZRO fee when paying in native
function _transferViaOFT(...) internal {
    MessagingFee memory fee = oft.quoteSend(sendParams, false);
    
    // Ensure we're only paying in native tokens
    require(fee.lzTokenFee == 0, "Unexpected ZRO fee");
    
    oft.send{value: fee.nativeFee}(sendParams, fee, refundAddress);
}
```

---

## 8. Peer & Trust Configuration Vulnerabilities

### Overview

LayerZero requires proper peer/trusted remote configuration to ensure messages are only accepted from legitimate counterparts. Misconfigurations can lead to fund loss or unauthorized message injection.

> **📚 Source Reports for Deep Dive:**
> - `reports/bridge_crosschain_findings/potential-loss-of-user-funds-due-to-optimistic-peer-assumption.md` (OmniX - Cantina)
> - `reports/bridge_crosschain_findings/setting-a-peer-nttmanager-contract-for-the-same-chain-can-cause-loss-of-user-fun.md` (Wormhole NTT - Cyfrin)

### Vulnerable Pattern Examples

**Example 1: Optimistic Peer Assumption** [MEDIUM]
> 📖 Reference: `reports/bridge_crosschain_findings/potential-loss-of-user-funds-due-to-optimistic-peer-assumption.md`
```solidity
// ❌ VULNERABLE: Uses sender address if peer not configured
function _getPeer(uint32 _dstEid) internal view returns (bytes32) {
    bytes32 trustedRemote = peers[_dstEid];
    if (trustedRemote == 0) {
        // Falls back to assuming same address on destination
        // If contract doesn't exist there, funds are lost!
        return bytes32(uint256(uint160(address(this))));
    }
    return trustedRemote;
}
```

**Example 2: Same Chain Peer Configuration** [MEDIUM]
> 📖 Reference: `reports/bridge_crosschain_findings/setting-a-peer-nttmanager-contract-for-the-same-chain-can-cause-loss-of-user-fun.md`
```solidity
// ❌ VULNERABLE: Allows setting peer for own chain
function setPeer(uint16 _chainId, bytes32 _peer) external onlyOwner {
    // No validation that _chainId != currentChainId
    peers[_chainId] = _peer;
    // User can accidentally transfer to "same chain" which fails
}
```

### Secure Implementation

**Fix 1: Revert on Unknown Peers**
```solidity
// ✅ SECURE: Don't assume peer exists
function _getPeer(uint32 _dstEid) internal view returns (bytes32) {
    bytes32 trustedRemote = peers[_dstEid];
    require(trustedRemote != bytes32(0), "Peer not configured");
    return trustedRemote;
}
```

**Fix 2: Prevent Same-Chain Peer**
```solidity
// ✅ SECURE: Validate peer chain is different
function setPeer(uint16 _chainId, bytes32 _peer) external onlyOwner {
    require(_chainId != currentChainId, "Cannot set self as peer");
    require(_peer != bytes32(0), "Invalid peer address");
    peers[_chainId] = _peer;
}
```

---

## 9. Stargate/sgReceive Integration Vulnerabilities

### Overview

Stargate is built on LayerZero and has its own integration patterns. The `sgReceive` callback has specific vulnerabilities related to gas handling and token recovery.

> **📚 Source Reports for Deep Dive:**
> - `reports/bridge_crosschain_findings/sgreceive-could-run-out-of-gas.md` (Sushi - SigmaPrime)
> - `reports/bridge_crosschain_findings/h-02-stargatelbphelpersgreceive-could-encounter-permanent-error-that-causes-rece.md` (TapiocaDAO - Pashov)
> - `reports/bridge_crosschain_findings/h-01-stargatelbphelperparticipate-will-send-tokens-to-the-wrong-address.md` (TapiocaDAO - Pashov)
> - `reports/bridge_crosschain_findings/h-07-underpayingoverpaying-of-stargate-fee-will-occur-in-stargatelbphelperpartic.md` (TapiocaDAO - Pashov)

### Vulnerable Pattern Examples

**Example 1: sgReceive OOG Without Fallback** [HIGH]
> 📖 Reference: `reports/bridge_crosschain_findings/sgreceive-could-run-out-of-gas.md`
```solidity
// ❌ VULNERABLE: Complex operations can run out of gas
function sgReceive(
    uint16 _chainId,
    bytes memory _srcAddress,
    uint256 _nonce,
    address _token,
    uint256 amountLD,
    bytes memory payload
) external override {
    (bytes[] memory actions, uint256[] memory values, bytes[] memory datas) = 
        abi.decode(payload, (bytes[], uint256[], bytes[]));
    
    // Try-catch is good but...
    try ISushiXSwap(payable(address(this))).cook(actions, values, datas) {
    } catch (bytes memory) {
        // If OOG happens here, entire transaction reverts!
        // Tokens are left in contract, anyone can steal them
        IERC20(_token).safeTransfer(to, amountLD);
    }
}
```

**Example 2: Permanent Error in sgReceive** [HIGH]
> 📖 Reference: `reports/bridge_crosschain_findings/h-02-stargatelbphelpersgreceive-could-encounter-permanent-error-that-causes-rece.md`
```solidity
// ❌ VULNERABLE: No recovery for permanent errors
contract StargateLbpHelper {
    function sgReceive(...) external {
        // If LBP pool is permanently broken, retryRevert() won't help
        // Tokens stuck forever
    }
    
    function retryRevert(bytes calldata _cachedPayload) external onlyOwner {
        // Can only retry, not extract tokens
    }
}
```

**Example 3: Wrong Destination Address** [HIGH]
> 📖 Reference: `reports/bridge_crosschain_findings/h-01-stargatelbphelperparticipate-will-send-tokens-to-the-wrong-address.md`
```solidity
// ❌ VULNERABLE: Sends to msg.sender instead of destination contract
function participate(StargateData calldata stargateData, ...) external payable {
    router.swap{value: msg.value}(
        stargateData.dstChainId,
        stargateData.srcPoolId,
        stargateData.dstPoolId,
        payable(msg.sender),
        stargateData.amount,
        amountWithSlippage,
        IStargateRouterBase.lzTxObj({dstGasForCall: 0, dstNativeAmount: 0, dstNativeAddr: "0x0"}),
        abi.encodePacked(msg.sender),  // BUG: Should be destination contract!
        abi.encode(lbpData, msg.sender)
    );
}
```

**Example 4: Hardcoded Zero dstGasForCall** [HIGH]
> 📖 Reference: `reports/bridge_crosschain_findings/h-07-underpayingoverpaying-of-stargate-fee-will-occur-in-stargatelbphelperpartic.md`
```solidity
// ❌ VULNERABLE: dstGasForCall = 0 uses default 200k gas
router.swap{value: msg.value}(
    ...
    IStargateRouterBase.lzTxObj({
        dstGasForCall: 0,      // Uses default 200k, may be too little or too much
        dstNativeAmount: 0,
        dstNativeAddr: "0x0"
    }),
    ...
);
```

### Secure Implementation

**Fix 1: Gas-Limited Try-Catch in sgReceive**
```solidity
// ✅ SECURE: Explicit gas limit ensures catch block executes
function sgReceive(..., address _token, uint256 amountLD, bytes memory payload) external {
    uint256 limit = gasleft() - exitGas;  // Reserve gas for catch
    
    try ISushiXSwap(payable(address(this))).cook{gas: limit}(actions, values, datas) {
        // Success
    } catch (bytes memory) {
        // Guaranteed to have gas for this
        IERC20(_token).safeTransfer(to, amountLD);
    }
}
```

**Fix 2: Allow Token Recovery**
```solidity
// ✅ SECURE: Allow stuck token recovery
contract StargateLbpHelper {
    function recoverStuckTokens(
        address token,
        address recipient,
        uint256 amount
    ) external onlyOwner {
        IERC20(token).safeTransfer(recipient, amount);
    }
}
```

---

## 10. Cross-Chain Payload Validation Vulnerabilities

### Overview

Cross-chain messages often contain user-controlled data that must be validated. Insufficient validation can lead to theft of funds or unauthorized actions.

> **📚 Source Reports for Deep Dive:**
> - `reports/bridge_crosschain_findings/h-11-toft-exerciseoption-can-be-used-to-steal-all-underlying-erc20-tokens.md` (TapiocaDAO - Code4rena)
> - `reports/bridge_crosschain_findings/h-05-incorrect-address-for-toft-debit.md` (TapiocaDAO - Pashov)

### Vulnerable Pattern Examples

**Example 1: Unvalidated Token Address in Payload** [HIGH]
> 📖 Reference: `reports/bridge_crosschain_findings/h-11-toft-exerciseoption-can-be-used-to-steal-all-underlying-erc20-tokens.md`
```solidity
// ❌ VULNERABLE: tapSendData.tapOftAddress not validated
function exerciseInternal(
    address from,
    uint256 oTAPTokenID,
    address paymentToken,
    uint256 tapAmount,
    address target,
    ITapiocaOptionsBrokerCrossChain.IExerciseLZSendTapData memory tapSendData,
    ICommonData.IApproval[] memory approvals
) public {
    if (approvals.length > 0) { _callApproval(approvals); }
    
    ITapiocaOptionsBroker(target).exerciseOption(oTAPTokenID, paymentToken, tapAmount);
    
    if (tapSendData.withdrawOnAnotherChain) {
        ISendFrom(tapSendData.tapOftAddress).sendFrom(...);
    } else {
        // ATTACK: tapOftAddress can be the underlying ERC20 token
        // tapAmount can be the entire balance of this contract
        // from can be attacker's address
        IERC20(tapSendData.tapOftAddress).safeTransfer(from, tapAmount);
    }
}
```

**Example 2: Wrong Sender in Debit** [HIGH]
> 📖 Reference: `reports/bridge_crosschain_findings/h-05-incorrect-address-for-toft-debit.md`
```solidity
// ❌ VULNERABLE: Debits from msg.sender instead of 'from'
function sendFrom(
    address from,
    uint16 dstChainId,
    bytes32 to,
    uint256 amount,
    ICommonOFT.LzCallParams memory lzCallParams
) external {
    _checkSender(from);  // Allows whitelisted relayer
    
    ISendFrom(_action.target).sendFrom{value: _action.value}(
        msg.sender,  // BUG: Should be 'from'! 
        dstChainId,
        to,
        amount,
        lzCallParams
    );
    // When msg.sender is relayer, tokens are debited from relayer not user
}
```

### Secure Implementation

**Fix 1: Validate Critical Addresses**
```solidity
// ✅ SECURE: Validate tapOftAddress is the expected token
function exerciseInternal(...) public {
    // Validate the token address is the expected TapOFT
    require(tapSendData.tapOftAddress == address(tapOft), "Invalid tap address");
    
    if (tapSendData.withdrawOnAnotherChain) {
        ISendFrom(tapSendData.tapOftAddress).sendFrom(...);
    } else {
        IERC20(tapSendData.tapOftAddress).safeTransfer(from, tapAmount);
    }
}
```

**Fix 2: Use Correct From Address**
```solidity
// ✅ SECURE: Debit from the correct account
function sendFrom(address from, ...) external {
    _checkSender(from);
    
    ISendFrom(_action.target).sendFrom{value: _action.value}(
        from,  // Correct: use 'from' not msg.sender
        dstChainId,
        to,
        amount,
        lzCallParams
    );
}
```

---

## 11. Insufficient Gas Limit Calculation

### Overview

Gas limits for LayerZero messages must account for all operations on the destination chain. Underestimating gas leads to failed transactions, potentially blocking channels or losing funds.

> **📚 Source Reports for Deep Dive:**
> - `reports/bridge_crosschain_findings/h-02-lzreceive-call-for-releaseoneid-results-in-oog-error.md` (NFTMirror - Pashov)
> - `reports/bridge_crosschain_findings/h-04-min_fallback_reserve-in-branchbridgeagent-doesnt-consider-the-actual-gas-co.md` (Maia DAO - Code4rena)

### Vulnerable Pattern Examples

**Example 1: Insufficient Per-Token Gas** [HIGH]
> 📖 Reference: `reports/bridge_crosschain_findings/h-02-lzreceive-call-for-releaseoneid-results-in-oog-error.md`
```solidity
// ❌ VULNERABLE: 20k gas per token is insufficient for minting
uint128 private constant _BASE_OWNERSHIP_UPDATE_COST = 80_000;
uint128 private constant _INCREMENTAL_OWNERSHIP_UPDATE_COST = 20_000;  // Too low!

function getSendOptions(uint256[] calldata tokenIds) public pure returns (bytes memory) {
    // Minting costs ~46k gas, transferring ~27k gas
    // But only 20k allocated per token!
    uint128 totalGasRequired = _BASE_OWNERSHIP_UPDATE_COST + 
        (_INCREMENTAL_OWNERSHIP_UPDATE_COST * uint128(tokenIds.length));
    
    return OptionsBuilder.newOptions().addExecutorLzReceiveOption(totalGasRequired, 0);
}
```

**Example 2: Not Accounting for AnyCall Overhead** [HIGH]
> 📖 Reference: `reports/bridge_crosschain_findings/h-04-min_fallback_reserve-in-branchbridgeagent-doesnt-consider-the-actual-gas-co.md`
```solidity
// ❌ VULNERABLE: MIN_FALLBACK_RESERVE doesn't cover all overhead
uint256 constant MIN_FALLBACK_RESERVE = 185_000;

// Breakdown:
// - 100_000 for anycall 
// - 85_000 for fallback execution
// Missing: ~110_000 for anyExec method in AnyCall
// Missing: Input data fee

function anyFallback(bytes calldata data) external {
    uint256 initialGas = gasleft();
    // ... execution ...
    uint256 gasLeft = gasleft();
    
    // Underestimates actual cost
    uint256 minExecCost = tx.gasprice * (MIN_FALLBACK_RESERVE + initialGas - gasLeft);
    
    if (minExecCost > getDeposit[_depositNonce].depositedGas) {
        _forceRevert();  // Drains execution budget
    }
}
```

### Secure Implementation

**Fix 1: Realistic Gas Per Operation**
```solidity
// ✅ SECURE: Account for actual operation costs
uint128 private constant _BASE_OWNERSHIP_UPDATE_COST = 100_000;
uint128 private constant _INCREMENTAL_MINT_COST = 50_000;      // Minting cost
uint128 private constant _INCREMENTAL_TRANSFER_COST = 30_000;  // Transfer cost

function getSendOptions(uint256[] calldata tokenIds, bool isMint) public pure returns (bytes memory) {
    uint128 perTokenCost = isMint ? _INCREMENTAL_MINT_COST : _INCREMENTAL_TRANSFER_COST;
    uint128 totalGasRequired = _BASE_OWNERSHIP_UPDATE_COST + 
        (perTokenCost * uint128(tokenIds.length));
    
    // Add buffer for safety
    totalGasRequired = totalGasRequired * 120 / 100;
    
    return OptionsBuilder.newOptions().addExecutorLzReceiveOption(totalGasRequired, 0);
}
```

**Fix 2: Allow User Gas Override**
```solidity
// ✅ SECURE: Let users specify higher gas if needed
function releaseOnEid(
    uint256[] calldata tokenIds,
    uint128 additionalGas  // User can add buffer
) external payable {
    uint128 baseGas = _calculateBaseGas(tokenIds);
    uint128 totalGas = baseGas + additionalGas;
    
    bytes memory options = OptionsBuilder.newOptions()
        .addExecutorLzReceiveOption(totalGas, 0);
    
    _lzSend(..., options, ...);
}
```

---

## Detection Patterns

### Code Patterns to Look For
```
- Pattern 1: Contracts inheriting LzApp without NonblockingLzApp
- Pattern 2: User-controlled adapterParams without gas validation
- Pattern 3: External calls inside _nonblockingLzReceive before try-catch
- Pattern 4: Missing receive() function in contracts receiving refunds
- Pattern 5: Hardcoded gas values that don't account for chain differences
- Pattern 6: Fee estimation using different payload than actual send
- Pattern 7: msg.sender used as refund address in delegated calls
- Pattern 8: No length validation on bytes parameters
- Pattern 9: lzCompose without try-catch for external calls
- Pattern 10: sgReceive without gas-limited try-catch
- Pattern 11: Unvalidated addresses in cross-chain payloads
- Pattern 12: Optimistic peer assumptions (fallback to self address)
- Pattern 13: Allowing peer configuration for same chain
- Pattern 14: Hardcoded dstGasForCall = 0 in Stargate integration
- Pattern 15: Not accounting for decimal trimming in token bridges
- Pattern 16: Rejecting composed messages after tokens are burned
```

### Audit Checklist
- [ ] Check if NonblockingLzApp pattern is correctly implemented
- [ ] Verify minimum gas is enforced for all message types
- [ ] Confirm gas configuration is per-destination-chain
- [ ] Ensure contracts can receive ETH refunds
- [ ] Validate refund addresses are correct (user, not contract)
- [ ] Check payload size limits on user inputs
- [ ] Verify forceResumeReceive is implemented for recovery
- [ ] Test fee estimation matches actual payload
- [ ] Verify lzCompose handles failures gracefully
- [ ] Check sgReceive has gas-limited try-catch
- [ ] Validate all addresses in cross-chain payloads
- [ ] Ensure peers cannot be set for same chain
- [ ] Verify unknown peers cause revert, not fallback
- [ ] Check for decimal trimming/dust handling
- [ ] Validate per-operation gas calculations are sufficient
- [ ] Test composed message scenarios end-to-end

---

## Keywords for Search

`layerzero`, `lzReceive`, `_lzSend`, `NonblockingLzApp`, `LzApp`, `adapterParams`, `StoredPayload`, `forceResumeReceive`, `trustedRemote`, `endpoint`, `channel_blocking`, `gas_griefing`, `OFT`, `ONFT`, `omnichain`, `cross_chain`, `bridge`, `relayer`, `minimum_gas`, `lzCompose`, `composed_message`, `stargate`, `sgReceive`, `fee_refund`, `peer`, `setPeer`, `trustedRemote`, `dstGasForCall`, `sharedDecimals`, `normalizeAmount`, `removeDust`, `OFTCore`, `OFTAdapter`, `MessagingFee`, `lzTokenFee`, `_creditTill`, `minGasToTransferAndStore`, `executorLzReceiveOption`, `retryMessage`, `payload_validation`, `tapOftAddress`, `exerciseOption`

---

## Related Vulnerabilities

- [Stargate Integration Issues](../stargate/stargate-integration-vulnerabilities.md)
- [Cross-Chain General Vulnerabilities](../custom/cross-chain-general-vulnerabilities.md)
- [Wormhole Integration Issues](../wormhole/wormhole-integration-vulnerabilities.md)
- [Hyperlane Integration Issues](../hyperlane/hyperlane-integration-vulnerabilities.md)
