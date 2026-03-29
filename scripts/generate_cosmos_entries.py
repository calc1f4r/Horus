#!/usr/bin/env python3
"""
Generate comprehensive Cosmos/CometBFT Horus entries
from the reports/cosmos_cometbft_findings/ directory.

This script:
1. Reads all 847 reports
2. Extracts titles, overviews, code snippets, severity, protocols
3. Groups by vulnerability pattern
4. Generates rich DB entries following TEMPLATE.md format
"""

import os
import re
import yaml
import sys
from collections import defaultdict
from pathlib import Path

REPORTS_DIR = "reports/cosmos_cometbft_findings"
DB_DIR = "DB/cosmos/app-chain"
REL_REPORTS = "../../../../reports/cosmos_cometbft_findings"

def parse_report(filepath):
    """Parse a report and extract structured data."""
    with open(filepath, 'r', errors='replace') as f:
        content = f.read()
    
    meta = {}
    body = content
    if content.startswith('---'):
        try:
            end_idx = content.index('---', 3)
            yaml_str = content[3:end_idx]
            meta = yaml.safe_load(yaml_str) or {}
            body = content[end_idx+3:].strip()
        except:
            pass
    
    # Extract title
    title_match = re.search(r'## Vulnerability Title\s*\n+(.+)', body)
    title = title_match.group(1).strip() if title_match else os.path.basename(filepath).replace('.md','').replace('-',' ')
    
    # Extract overview
    overview_match = re.search(r'### Overview\s*\n+(.*?)(?=\n###|\Z)', body, re.DOTALL)
    overview = overview_match.group(1).strip() if overview_match else ""
    
    # Extract original finding content
    finding_match = re.search(r'### Original Finding Content\s*\n+(.*?)(?=\n## |\Z)', body, re.DOTALL)
    finding = finding_match.group(1).strip() if finding_match else ""
    
    # Extract code snippets
    code_blocks = re.findall(r'```(?:solidity|go|rust|move|javascript|python|typescript|)?\s*\n(.*?)```', body, re.DOTALL)
    
    return {
        'file': os.path.basename(filepath),
        'title': title,
        'overview': overview,
        'finding': finding[:2000],
        'severity': meta.get('severity', 'unknown'),
        'protocol': meta.get('protocol', 'unknown'),
        'audit_firm': meta.get('audit_firm', 'unknown'),
        'code_blocks': code_blocks[:5],  # Limit to 5 code blocks
        'has_code': len(code_blocks) > 0,
    }


def classify_reports(reports):
    """Classify reports into fine-grained vulnerability pattern groups."""
    
    # Define the entry structure: each entry maps to a DB file
    # with multiple sub-patterns inside
    entries = {
        # ===== STAKING CORE =====
        'staking/stake-deposit-vulnerabilities': {
            'title': 'Stake Deposit and Amount Tracking Vulnerabilities',
            'patterns': {
                'incorrect_stake_amount': ['incorrect.*stake.*amount', 'wrong.*stake', 'stake.*calculat.*incorrect', 'miscalculat.*stake'],
                'duplicate_stake_counting': ['duplicate.*stak', 'double.*count', 'over.*allocat', 'same.*stake.*multiple'],
                'stake_without_payment': ['stake.*without.*pay', 'lock.*stake.*arbitrary', 'free.*stak'],
                'deposit_front_running': ['deposit.*front', 'front.*deposit', 'deposit.*sandwic'],
                'deposit_validation_missing': ['deposit.*valid', 'missing.*deposit.*check', 'no.*deposit.*verif', 'minimum.*stake.*bypass'],
                'stake_balance_desync': ['balance.*desync', 'balance.*mismatch', 'staked.*balance.*incorrect', 'balance.*not.*updated'],
                'first_depositor_attack': ['first.*deposit', 'inflation.*attack', 'share.*inflat'],
                'deposit_queue_manipulation': ['deposit.*queue', 'pending.*deposit', 'deposit.*delay'],
            },
            'keywords': ['stake', 'deposit', 'staking', 'validator', 'amount', 'balance', 'tracking', 'accounting', 'minimum-stake', 'over-allocation', 'double-counting'],
        },
        'staking/unstake-withdrawal-vulnerabilities': {
            'title': 'Unstaking and Withdrawal Processing Vulnerabilities',
            'patterns': {
                'unstake_bypass_cooldown': ['unstake.*immediately', 'bypass.*unstaking', 'skip.*cooldown', 'avoid.*delay', 'cooldown.*bypass'],
                'withdrawal_dos': ['withdrawal.*revert', 'withdrawal.*stuck', 'unable.*withdraw', 'withdraw.*fail', 'withdraw.*block'],
                'withdrawal_amount_error': ['withdraw.*amount.*incorrect', 'withdraw.*too.*much', 'over.*withdraw'],
                'withdrawal_queue_manipulation': ['withdrawal.*queue', 'queue.*manipul', 'withdrawal.*order'],
                'incomplete_withdrawal': ['partial.*withdraw', 'incomplete.*withdraw', 'remaining.*fund'],
                'withdrawal_replay': ['withdraw.*replay', 'double.*withdraw', 'withdraw.*twice'],
                'withdrawal_during_slash': ['withdraw.*slash', 'withdrawal.*before.*slash', 'unstake.*before.*penalty'],
                'emergency_withdrawal_abuse': ['emergency.*withdraw', 'emergency.*exit', 'force.*withdraw'],
            },
            'keywords': ['unstake', 'withdrawal', 'cooldown', 'delay', 'queue', 'exit', 'unbonding', 'unstaking-period', 'withdrawal-request', 'force-exit'],
        },
        'staking/delegation-redelegation-vulnerabilities': {
            'title': 'Delegation and Redelegation Vulnerabilities',
            'patterns': {
                'self_delegation_manipulation': ['self.*delegat', 'self-delegation', 'own.*delegation'],
                'delegation_dos': ['delegat.*dos', 'delegat.*prevent', 'delegat.*block', 'delegat.*revert'],
                'undelegation_bypass': ['undelegat.*bypass', 'undelegat.*immediate', 'force.*undelegat'],
                'redelegation_tracking': ['redelegat.*track', 'redelegat.*account', 'pending.*redelegat'],
                'delegation_reward_theft': ['delegat.*reward.*steal', 'delegat.*reward.*manipul'],
                'delegation_state_inconsistency': ['delegat.*state.*inconsist', 'delegat.*state.*corrupt', 'delegator.*fund.*mismanag'],
                'delegation_to_inactive': ['delegat.*inactive', 'delegat.*jailed', 'stake.*inactive.*validator'],
                'delegation_frontrunning': ['delegat.*frontrun', 'front.*delegat'],
            },
            'keywords': ['delegation', 'redelegate', 'undelegate', 'self-delegation', 'delegator', 'delegate', 'bonding', 'unbonding', 'redelegation-tracking'],
        },
        'staking/validator-management-vulnerabilities': {
            'title': 'Validator Registration and Management Vulnerabilities',
            'patterns': {
                'validator_registration_bypass': ['validator.*register.*bypass', 'unrestrict.*validator.*register', 'anyone.*validator'],
                'validator_removal_failure': ['validator.*remov.*fail', 'validator.*cannot.*remov', 'stuck.*validator'],
                'validator_set_manipulation': ['validator.*set.*manipul', 'validator.*power.*manipul', 'voting.*power.*incorrect'],
                'validator_key_rotation': ['key.*rotat', 'consensus.*key', 'bls.*key'],
                'validator_commission_exploit': ['commission.*manipul', 'commission.*rate.*chang', 'validator.*fee.*exploit'],
                'validator_status_transition': ['validator.*status', 'validator.*state.*transit', 'inactive.*active', 'jailed.*unjail'],
                'validator_dust_collateral': ['dust.*collateral', 'minimum.*collateral', 'validator.*dust'],
                'operator_key_mismatch': ['operator.*key', 'node.*id.*reuse', 'key.*mismatch'],
            },
            'keywords': ['validator', 'registration', 'deregistration', 'commission', 'voting-power', 'validator-set', 'key-rotation', 'jailing', 'unjailing', 'operator'],
        },

        # ===== SLASHING =====
        'staking/slashing-evasion-techniques': {
            'title': 'Advanced Slashing Evasion Techniques',
            'patterns': {
                'frontrun_slash_withdraw': ['frontrun.*slash', 'withdraw.*before.*slash', 'exit.*before.*slash'],
                'cooldown_slash_bypass': ['cooldown.*slash', 'activate.*cooldown.*before.*slash'],
                'delegation_slash_bypass': ['delegat.*slash.*bypass', 'redeleg.*avoid.*slash', 'transfer.*avoid.*slash'],
                'insufficient_deposit_slash': ['insufficient.*deposit.*slash', 'reduce.*deposit.*before.*slash'],
                'plugin_slash_block': ['plugin.*slash.*block', 'external.*contract.*slash.*revert'],
                'queued_withdrawal_slash': ['queued.*withdrawal.*slash', 'pending.*withdrawal.*slash', 'withdrawal.*exclude.*slash'],
                'unregistered_operator_slash': ['unregist.*slash', 'slash.*unregist'],
                'slash_reversal': ['slash.*revers', 'undo.*slash', 'recover.*slash'],
            },
            'keywords': ['slashing-evasion', 'frontrunning-slash', 'bypass-slash', 'cooldown-bypass', 'withdrawal-before-slash', 'penalty-evasion', 'economic-security'],
        },
        'staking/slashing-accounting-errors': {
            'title': 'Slashing Accounting and Calculation Errors',
            'patterns': {
                'slash_amount_miscalculation': ['slash.*amount.*incorrect', 'slash.*calculat.*wrong', 'wrong.*slash.*amount'],
                'slash_share_dilution': ['slash.*share.*dilut', 'slash.*induced.*dilut'],
                'over_slashing': ['over.*slash', 'slash.*more.*than', 'excessive.*slash'],
                'under_slashing': ['under.*slash', 'slash.*less.*than', 'insufficient.*slash'],
                'slash_balance_update': ['slash.*balance.*update', 'balance.*after.*slash', 'slash.*not.*reflect'],
                'slash_reward_interaction': ['slash.*reward', 'reward.*after.*slash', 'slash.*affect.*reward'],
                'slash_pending_operations': ['slash.*pending', 'slash.*queued', 'slash.*in.*progress'],
                'cumulative_slash_error': ['cumulat.*slash', 'multiple.*slash', 'slash.*accumulat'],
            },
            'keywords': ['slashing-calculation', 'over-slashing', 'under-slashing', 'slash-amount', 'share-dilution', 'penalty-calculation', 'slash-accounting'],
        },

        # ===== REWARDS =====
        'rewards/reward-calculation-vulnerabilities': {
            'title': 'Staking Reward Calculation Vulnerabilities',
            'patterns': {
                'reward_amount_incorrect': ['reward.*amount.*incorrect', 'wrong.*reward', 'reward.*calculat.*error'],
                'reward_per_share_error': ['reward.*per.*share', 'reward.*ratio', 'reward.*rate.*incorrect'],
                'accumulated_reward_error': ['accumulat.*reward.*error', 'reward.*accumulator', 'global.*reward.*incorrect'],
                'delayed_balance_reward': ['delayed.*balance.*reward', 'pending.*balance.*reward'],
                'decimal_mismatch_reward': ['decimal.*mismatch.*reward', 'precision.*reward'],
                'btc_delegation_reward': ['btc.*delegation.*reward', 'babylon.*reward'],
                'weight_based_reward_error': ['weight.*reward.*incorrect', 'stake.*weight.*reward'],
                'historical_reward_loss': ['historical.*reward', 'past.*reward.*lost', 'reward.*loss.*reuse'],
            },
            'keywords': ['reward-calculation', 'staking-rewards', 'reward-per-share', 'reward-rate', 'accumulated-rewards', 'reward-distribution', 'decimal-mismatch'],
        },
        'rewards/reward-theft-manipulation': {
            'title': 'Reward Theft and Manipulation Vulnerabilities',
            'patterns': {
                'flashloan_reward_theft': ['flashloan.*reward', 'flash.*loan.*stak', 'borrow.*stake.*reward'],
                'reward_frontrunning': ['frontrun.*reward', 'sandwich.*reward', 'mev.*reward'],
                'orphaned_reward_capture': ['orphan.*reward', 'first.*staker.*reward', 'unassign.*reward'],
                'reward_replay': ['reward.*replay', 'double.*claim.*reward', 'claim.*reward.*twice'],
                'reward_dilution': ['reward.*dilut', 'dilut.*existing.*staker', 'new.*staker.*dilut'],
                'cross_contract_reward': ['cross.*contract.*reward', 'reward.*cross.*contract'],
                'fake_stake_reward': ['fake.*stake.*reward', 'spoof.*stake', 'manipulat.*stake.*reward'],
                'commission_theft': ['commission.*theft', 'commission.*steal', 'operator.*commission.*manipul'],
            },
            'keywords': ['reward-theft', 'flashloan-staking', 'reward-frontrunning', 'orphaned-rewards', 'reward-dilution', 'commission-theft', 'MEV-rewards'],
        },
        'rewards/reward-distribution-failures': {
            'title': 'Reward Distribution and Loss Vulnerabilities',
            'patterns': {
                'reward_stuck_contract': ['reward.*stuck', 'reward.*locked', 'reward.*trapped'],
                'reward_distribution_dos': ['reward.*distribut.*dos', 'reward.*distribut.*revert', 'reward.*distribut.*fail'],
                'missing_reward_update': ['missing.*reward.*update', 'reward.*not.*accrued', 'reward.*not.*updated'],
                'reward_after_removal': ['reward.*after.*remov', 'claim.*after.*exit', 'reward.*removed.*operator'],
                'yield_distribution_error': ['yield.*distribut.*error', 'yield.*alloc.*incorrect'],
                'incentive_misalignment': ['incentiv.*misalign', 'perverse.*incentiv', 'wrong.*incentiv'],
                'reward_escrow_error': ['reward.*escrow', 'incorrect.*escrow', 'escrow.*assign'],
                'reward_checkpoint_error': ['reward.*checkpoint', 'snapshot.*reward', 'reward.*at.*time'],
            },
            'keywords': ['reward-distribution', 'stuck-rewards', 'distribution-failure', 'reward-loss', 'yield-distribution', 'incentive-misalignment', 'reward-escrow'],
        },

        # ===== DOS / CHAIN HALT =====
        'dos/chain-halt-vectors': {
            'title': 'Chain Halt and Block Production DoS Vulnerabilities',
            'patterns': {
                'block_production_halt': ['block.*produc.*halt', 'block.*produc.*stop', 'halt.*block'],
                'consensus_halt': ['consensus.*halt', 'consensus.*stuck', 'consensus.*deadlock'],
                'state_machine_halt': ['state.*machine.*halt', 'abci.*halt', 'beginblock.*halt', 'endblock.*halt'],
                'transaction_processing_halt': ['transaction.*halt', 'tx.*processing.*halt'],
                'validator_induced_halt': ['validator.*halt', 'validator.*crash', 'malicious.*validator.*halt'],
                'evm_chain_halt': ['evm.*chain.*halt', 'evm.*block.*halt', 'blob.*halt'],
                'prototype_pollution_halt': ['prototype.*pollut', 'pollution.*brick', 'javascript.*halt'],
                'data_availability_halt': ['data.*availability', 'da.*race', 'sidecar.*race'],
            },
            'keywords': ['chain-halt', 'block-production', 'consensus-halt', 'state-machine', 'validator-crash', 'DoS', 'liveness-attack', 'block-processing'],
        },
        'dos/unbounded-iteration-dos': {
            'title': 'Unbounded Iteration and Loop-Based DoS Vulnerabilities',
            'patterns': {
                'unbounded_loop_beginblock': ['unbounded.*beginblock', 'linear.*iteration.*beginblock', 'beginblock.*loop'],
                'unbounded_loop_endblock': ['unbounded.*endblock', 'endblock.*loop', 'endblock.*iteration'],
                'unbounded_array_iteration': ['unbounded.*array', 'unbounded.*size', 'array.*unbounded'],
                'unmetered_iteration': ['unmetered.*iteration', 'unmetered.*loop', 'unmetered.*balance', 'gas.*meter.*loop'],
                'reward_plan_iteration': ['reward.*plan.*iteration', 'loop.*reward'],
                'undelegation_iteration': ['undelegation.*iteration', 'loop.*undelegat'],
                'token_transfer_iteration': ['token.*transfer.*iteration', 'loop.*transfer'],
                'state_iteration_dos': ['state.*iteration', 'iterate.*state', 'store.*iteration'],
            },
            'keywords': ['unbounded-iteration', 'loop-DoS', 'linear-iteration', 'gas-exhaustion', 'BeginBlock', 'EndBlock', 'unmetered', 'array-size', 'O(n)-complexity'],
        },
        'dos/gas-resource-exhaustion': {
            'title': 'Gas and Resource Exhaustion DoS Vulnerabilities',
            'patterns': {
                'gas_limit_exploit': ['gas.*limit.*exploit', 'block.*gas.*limit', 'exceed.*gas'],
                'gas_metering_bypass': ['gas.*meter.*bypass', 'no.*gas.*charg', 'gas.*not.*consum', 'free.*gas'],
                'memory_exhaustion': ['memory.*exhaust', 'memory.*attack', 'oom'],
                'storage_exhaustion': ['storage.*exhaust', 'storage.*spam', 'state.*bloat'],
                'large_payload_dos': ['large.*payload', 'oversiz', 'max.*bytes.*exceed'],
                'gas_refund_exploit': ['gas.*refund', 'refund.*exploit', 'gas.*refund.*incorrect'],
                'precompile_gas_exploit': ['precompile.*gas', 'gas.*precompile', 'hardcoded.*gas'],
                'cross_chain_gas_mismatch': ['cross.*chain.*gas', 'gas.*mismatch.*chain', 'different.*gas.*limit'],
            },
            'keywords': ['gas-exhaustion', 'resource-exhaustion', 'DoS', 'gas-limit', 'memory-exhaustion', 'storage-bloat', 'payload-size', 'gas-metering'],
        },
        'dos/denial-of-service-patterns': {
            'title': 'General Denial of Service Attack Patterns',
            'patterns': {
                'function_reversion_dos': ['function.*always.*revert', 'function.*will.*revert', 'permanent.*revert'],
                'panic_crash_dos': ['panic.*dos', 'crash.*dos', 'nil.*pointer', 'index.*out.*range'],
                'frontrun_dos': ['frontrun.*dos', 'grief.*frontrun', 'dos.*frontrun'],
                'dust_amount_dos': ['dust.*amount', 'minimal.*amount.*dos', 'tiny.*deposit.*grief'],
                'reentrancy_dos': ['reentrancy.*dos', 'reentrant.*call.*dos'],
                'external_call_dos': ['external.*call.*dos', 'external.*revert', 'callback.*revert'],
                'permission_dos': ['permission.*dos', 'access.*control.*dos', 'role.*dos'],
                'upgrade_dos': ['upgrade.*dos', 'upgrade.*revert', 'migration.*dos'],
            },
            'keywords': ['denial-of-service', 'DoS', 'revert', 'panic', 'crash', 'griefing', 'frontrun-DoS', 'dust-amount', 'permanent-revert'],
        },

        # ===== FUND SAFETY =====
        'fund-safety/fund-theft-vulnerabilities': {
            'title': 'Direct Fund Theft and Drain Vulnerabilities',
            'patterns': {
                'direct_theft_via_auth': ['unauthorized.*withdraw', 'anyone.*withdraw', 'theft.*lack.*auth'],
                'theft_via_manipulation': ['manipulat.*steal', 'manipulat.*drain', 'exploit.*drain'],
                'theft_via_reentrancy': ['reentrancy.*steal', 'reentrant.*drain'],
                'theft_via_share_price': ['share.*price.*steal', 'exchange.*rate.*theft'],
                'theft_via_delegatecall': ['delegatecall.*theft', 'delegatecall.*drain', 'delegatecall.*precompile'],
                'theft_via_replay': ['replay.*theft', 'replay.*steal'],
                'theft_via_frontrunning': ['frontrun.*theft', 'frontrun.*steal', 'sandwich.*steal'],
                'surplus_balance_theft': ['surplus.*balance.*theft', 'excess.*balance.*steal'],
            },
            'keywords': ['fund-theft', 'drain', 'steal', 'unauthorized-withdrawal', 'reentrancy', 'delegatecall', 'replay-attack', 'frontrunning'],
        },
        'fund-safety/fund-locking-insolvency': {
            'title': 'Fund Locking and Protocol Insolvency Vulnerabilities',
            'patterns': {
                'permanent_fund_lock': ['permanent.*lock', 'fund.*forever', 'irrecoverable', 'fund.*stuck.*forever'],
                'conditional_fund_lock': ['fund.*lock.*condition', 'lock.*if', 'lock.*when', 'lock.*during'],
                'insolvency_slash': ['insolven.*slash', 'protocol.*insolven.*slash'],
                'insolvency_rebase': ['insolven.*rebase', 'negative.*rebase.*insolven'],
                'insolvency_bad_debt': ['bad.*debt', 'undercollatera.*insolven'],
                'withdrawal_blocked': ['withdrawal.*blocked', 'cannot.*withdraw', 'withdrawal.*prevent'],
                'upgrade_fund_lock': ['upgrade.*fund.*lock', 'migration.*fund.*lock'],
                'griefing_fund_lock': ['grief.*fund.*lock', 'grief.*lock', 'dos.*lock.*fund'],
            },
            'keywords': ['fund-locking', 'insolvency', 'bad-debt', 'permanent-lock', 'stuck-funds', 'withdrawal-blocked', 'protocol-insolvency', 'negative-rebase'],
        },

        # ===== ACCOUNTING & MATH =====
        'accounting/balance-tracking-errors': {
            'title': 'Balance and State Tracking Vulnerabilities',
            'patterns': {
                'balance_not_updated': ['balance.*not.*updated', 'missing.*balance.*update', 'skip.*balance.*update'],
                'balance_desynchronization': ['balance.*desync', 'out.*of.*sync', 'balance.*mismatch'],
                'double_counting': ['double.*count', 'count.*twice', 'duplicate.*account'],
                'tvl_calculation_error': ['tvl.*calculat.*error', 'tvl.*incorrect', 'total.*value.*incorrect'],
                'accounting_state_corruption': ['state.*corrupt', 'accounting.*corrupt', 'inconsist.*state'],
                'missing_deduction': ['missing.*deduct', 'not.*subtract', 'forget.*decrement'],
                'cross_module_accounting': ['cross.*module.*account', 'module.*balance.*mismatch'],
                'pending_amount_tracking': ['pending.*amount', 'pending.*track', 'in.*flight.*amount'],
            },
            'keywords': ['balance-tracking', 'state-desynchronization', 'accounting-error', 'double-counting', 'TVL-calculation', 'state-corruption', 'missing-update'],
        },
        'accounting/exchange-rate-vulnerabilities': {
            'title': 'Exchange Rate and Share Price Vulnerabilities',
            'patterns': {
                'exchange_rate_manipulation': ['exchange.*rate.*manipul', 'share.*price.*manipul'],
                'exchange_rate_stale': ['exchange.*rate.*stale', 'outdated.*exchange.*rate', 'stale.*rate'],
                'exchange_rate_calculation_error': ['exchange.*rate.*calculat.*error', 'incorrect.*exchange.*rate', 'wrong.*exchange.*rate'],
                'share_price_inflation': ['share.*price.*inflat', 'token.*price.*inflat', 'vault.*share.*inflat'],
                'conversion_rounding': ['conversion.*round', 'round.*conversion', 'share.*round'],
                'rate_update_missing': ['rate.*update.*miss', 'rate.*not.*update', 'stale.*price'],
                'donation_attack': ['donation.*attack', 'direct.*transfer.*manipul'],
                'rate_during_slash': ['rate.*during.*slash', 'exchange.*rate.*slash', 'share.*value.*slash'],
            },
            'keywords': ['exchange-rate', 'share-price', 'rate-manipulation', 'stale-rate', 'donation-attack', 'share-inflation', 'conversion-rounding', 'rate-update'],
        },
        'accounting/integer-overflow-precision': {
            'title': 'Integer Overflow, Underflow and Precision Loss Vulnerabilities',
            'patterns': {
                'integer_overflow': ['integer.*overflow', 'uint.*overflow', 'overflow.*calculat'],
                'integer_underflow': ['integer.*underflow', 'underflow.*subtract', 'negative.*underflow'],
                'unsafe_casting': ['unsafe.*cast', 'uint256.*uint128', 'downcast', 'truncat'],
                'precision_loss_division': ['precision.*loss.*divisi', 'division.*precision', 'round.*down.*loss'],
                'precision_loss_multiplication': ['precision.*loss.*multipl', 'multiply.*before.*divid'],
                'decimal_mismatch': ['decimal.*mismatch', '18.*decimal', '6.*decimal', 'decimal.*different'],
                'rounding_error_accumulation': ['round.*error.*accumulat', 'cumulative.*round'],
                'fullmath_overflow': ['fullmath', 'intermediate.*overflow', 'mulDiv.*overflow'],
            },
            'keywords': ['integer-overflow', 'underflow', 'precision-loss', 'unsafe-cast', 'rounding-error', 'decimal-mismatch', 'truncation', 'arithmetic-error'],
        },

        # ===== EVM / PRECOMPILE =====
        'evm/evm-gas-handling-vulnerabilities': {
            'title': 'EVM Gas Handling and Metering Vulnerabilities in Cosmos Chains',
            'patterns': {
                'missing_intrinsic_gas': ['intrinsic.*gas.*miss', 'fail.*charge.*intrinsic', 'intrinsic.*gas.*not.*charg'],
                'gas_refund_incorrect': ['gas.*refund.*incorrect', 'wrong.*gas.*refund', 'gas.*refund.*block'],
                'stack_overflow_no_gas': ['stack.*overflow.*gas', 'evm.*stack.*overflow'],
                'precompile_gas_hardcode': ['precompile.*gas.*hardcod', 'hardcoded.*gas.*erc20', 'gas.*used.*mismatch'],
                'gas_not_consumed_on_error': ['gas.*not.*consumed.*fail', 'error.*no.*gas', 'fail.*gas.*free'],
                'cross_vm_gas_mismatch': ['cross.*vm.*gas', 'cosmos.*evm.*gas.*mismatch'],
                'explicit_gas_limit_bypass': ['explicit.*gas.*limit.*bypass', 'dispatcher.*gas'],
                'transaction_gas_vs_block': ['transaction.*gas.*block', 'block.*gas.*transaction'],
            },
            'keywords': ['EVM-gas', 'gas-metering', 'intrinsic-gas', 'gas-refund', 'stack-overflow', 'precompile-gas', 'Cosmos-EVM', 'gas-consumption'],
        },
        'evm/precompile-state-vulnerabilities': {
            'title': 'EVM Precompile and State Management Vulnerabilities',
            'patterns': {
                'dirty_state_precompile': ['dirty.*state.*precompile', 'uncommitted.*state.*precompile', 'state.*before.*precompile'],
                'precompile_panic_dos': ['precompile.*panic', 'precompile.*empty.*calldata', 'stateful.*precompile.*panic'],
                'precompile_delegatecall': ['precompile.*delegatecall', 'delegatecall.*staking', 'delegatecall.*precompile'],
                'precompile_state_rollback': ['precompile.*rollback', 'precompile.*revert.*state'],
                'evm_bank_balance_sync': ['evm.*bank.*balance', 'bank.*evm.*sync', 'balance.*sync.*evm'],
                'cosmos_evm_nonce': ['nonce.*evm', 'nonce.*cosmos', 'nonce.*manipulat'],
                'evm_tx_disguise': ['evm.*tx.*disguis', 'cosmos.*msg.*evm', 'regular.*cosmos.*evm'],
                'precompile_outdated_data': ['precompile.*outdated', 'precompile.*stale.*data', 'total.*supply.*precompile'],
            },
            'keywords': ['precompile', 'dirty-state', 'delegatecall', 'state-sync', 'EVM-Cosmos', 'bank-module', 'nonce-manipulation', 'state-rollback'],
        },

        # ===== IBC / BRIDGE =====
        'ibc/ibc-protocol-vulnerabilities': {
            'title': 'IBC Protocol and Channel Vulnerabilities',
            'patterns': {
                'ibc_channel_verification': ['ibc.*channel.*verif', 'channel.*open.*ack', 'channel.*handshake'],
                'ibc_packet_handling': ['ibc.*packet.*handl', 'onrecvpacket', 'packet.*callback'],
                'ibc_version_negotiation': ['ibc.*version', 'version.*negotiat', 'channel.*version'],
                'ibc_middleware_bypass': ['ibc.*middleware.*bypass', 'middleware.*hook.*bypass', 'l2.*hook.*bypass'],
                'ibc_authentication': ['ibc.*auth', 'onrecvpacket.*auth', 'lack.*auth.*ibc'],
                'ibc_abort_flood': ['abort.*flood', 'deadlock.*abort', 'channel.*flood'],
                'ibc_channel_state': ['channel.*state', 'channel.*close', 'channel.*open'],
                'ibc_timeout_handling': ['ibc.*timeout', 'timeout.*packet', 'acknowledgement.*timeout'],
            },
            'keywords': ['IBC', 'channel', 'packet', 'middleware', 'handshake', 'version-negotiation', 'OnRecvPacket', 'authentication', 'abort', 'timeout'],
        },
        'ibc/cross-chain-bridge-vulnerabilities': {
            'title': 'Cross-Chain Bridge and Relay Vulnerabilities',
            'patterns': {
                'bridge_replay_attack': ['bridge.*replay', 'cross.*chain.*replay', 'hard.*fork.*replay'],
                'bridge_token_accounting': ['bridge.*token.*account', 'bridge.*balance.*mismatch', 'bridge.*token.*mint'],
                'relayer_manipulation': ['relayer.*manipulat', 'relayer.*avoid.*slash', 'relayer.*fraud'],
                'bridge_freeze': ['bridge.*freeze', 'large.*validator.*set.*bridge', 'bridge.*halt'],
                'bridge_message_validation': ['bridge.*message.*valid', 'bridge.*msg.*verif'],
                'relayer_slash': ['relayer.*slash', 'relayer.*stake', 'relayer.*bond'],
                'bridge_denom_handling': ['bridge.*denom', 'erc20.*denom', 'token.*bridge.*error'],
                'observer_manipulation': ['observer.*manipulat', 'observer.*remov', 'observer.*vote'],
            },
            'keywords': ['bridge', 'cross-chain', 'relayer', 'replay-attack', 'token-accounting', 'bridge-freeze', 'message-validation', 'observer'],
        },

        # ===== GOVERNANCE =====
        'governance/governance-voting-vulnerabilities': {
            'title': 'Governance and Voting Manipulation Vulnerabilities',
            'patterns': {
                'voting_power_manipulation': ['voting.*power.*manipul', 'vote.*weight.*manipul', 'inflat.*voting.*power'],
                'flash_vote': ['flash.*vote', 'flashloan.*vote', 'borrow.*vote'],
                'proposal_spam': ['proposal.*spam', 'proposal.*dos', 'ballot.*spam'],
                'quorum_manipulation': ['quorum.*manipul', 'quorum.*lower', 'delegat.*quorum'],
                'voting_after_lock': ['vote.*after.*lock', 'vote.*lock.*period', 'vote.*expir'],
                'proposal_griefing': ['proposal.*grief', 'proposal.*block', 'proposal.*prevent'],
                'dual_governance_exploit': ['dual.*governance', 'governance.*conflictt'],
                'bribe_reward_manipulation': ['bribe.*reward', 'bribe.*manipulat', 'voting.*bribe'],
            },
            'keywords': ['governance', 'voting', 'proposal', 'quorum', 'voting-power', 'flash-vote', 'bribe', 'ballot', 'governance-attack', 'DAO'],
        },

        # ===== CONSENSUS =====
        'consensus/consensus-finality-vulnerabilities': {
            'title': 'Consensus, Finality and Block Production Vulnerabilities',
            'patterns': {
                'proposer_ddos': ['proposer.*ddos', 'block.*proposer.*dos', 'malicious.*proposer'],
                'finality_bypass': ['finality.*bypass', 'forced.*finalization', 'premature.*finality'],
                'reorg_attack': ['reorg.*attack', 'bitcoin.*reorg', 'chain.*reorg'],
                'validator_score_manipulation': ['validator.*score', 'past.*validator.*score'],
                'vote_extension_vulnerability': ['vote.*extension.*vulne', 'inject.*vote.*extension'],
                'block_sync_vulnerability': ['block.*sync', 'blocksync', 'syncing.*node.*panic'],
                'consensus_specification_mismatch': ['consensus.*specification', 'specification.*mismatch', 'implementation.*specification'],
                'non_determinism': ['non.*determinism', 'non-deterministic', 'determinism.*issue'],
            },
            'keywords': ['consensus', 'finality', 'proposer', 'reorg', 'block-sync', 'vote-extension', 'non-determinism', 'CometBFT', 'Tendermint', 'block-production'],
        },

        # ===== ACCESS CONTROL =====
        'access-control/authorization-vulnerabilities': {
            'title': 'Access Control and Authorization Vulnerabilities',
            'patterns': {
                'missing_access_control': ['missing.*access.*control', 'no.*access.*control', 'lack.*access.*control', 'anyone.*call'],
                'role_assignment_error': ['role.*assign.*error', 'missing.*grant.*role', 'role.*not.*grant'],
                'owner_manipulation': ['owner.*manipulat', 'admin.*manipulat', 'owner.*set.*invalid'],
                'antehandler_bypass': ['antehandler.*bypass', 'antehandler.*skip', 'checktx.*bypass'],
                'allowlist_bypass': ['allowlist.*bypass', 'whitelist.*bypass', 'allow.*list.*bypass'],
                'legacy_signing_bypass': ['legacy.*sign', 'amino.*sign', 'amino.*bypass'],
                'predecessor_id_misuse': ['predecessor.*id', 'signer.*id', 'account.*id.*misuse'],
                'cosmwasm_auth_bypass': ['cosmwasm.*auth', 'cosmwasm.*contract.*bypass', 'smart.*contract.*access'],
            },
            'keywords': ['access-control', 'authorization', 'permission', 'role', 'admin', 'antehandler', 'allowlist', 'bypass', 'missing-auth', 'privilege-escalation'],
        },

        # ===== TIMING / EPOCH =====
        'timing/epoch-timing-vulnerabilities': {
            'title': 'Epoch Boundary and Timing Exploitation Vulnerabilities',
            'patterns': {
                'epoch_transition_exploit': ['epoch.*transition.*exploit', 'epoch.*boundary.*exploit', 'epoch.*change.*exploit'],
                'epoch_snapshot_manipulation': ['epoch.*snapshot.*manipul', 'snapshot.*timing', 'cache.*manipulat.*epoch'],
                'cooldown_lock_bypass': ['cooldown.*bypass', 'lockup.*bypass', 'lock.*period.*bypass'],
                'timestamp_boundary_error': ['timestamp.*boundary', 'off.*by.*one.*time', 'timestamp.*inclusiv'],
                'unbonding_time_change': ['unbonding.*time.*change', 'unbonding.*period.*change'],
                'epoch_duration_change': ['epoch.*duration.*change', 'change.*epoch.*duration', 'epoch.*break'],
                'reward_epoch_timing': ['reward.*epoch.*timing', 'reward.*between.*epoch'],
                'expiration_bypass': ['expiratio.*bypass', 'expir.*check.*miss', 'expired.*still.*active'],
            },
            'keywords': ['epoch', 'timing', 'snapshot', 'cooldown', 'lockup', 'unbonding-period', 'timestamp', 'boundary-condition', 'expiration', 'epoch-transition'],
        },

        # ===== VALIDATION =====
        'validation/input-validation-vulnerabilities': {
            'title': 'Missing Input Validation and Parameter Check Vulnerabilities',
            'patterns': {
                'missing_zero_check': ['missing.*zero.*check', 'zero.*amount', 'zero.*address', 'no.*zero.*valid'],
                'missing_bounds_check': ['missing.*bounds', 'no.*upper.*limit', 'no.*lower.*limit', 'unbounded.*parameter'],
                'missing_state_check': ['missing.*state.*check', 'no.*state.*valid', 'skip.*state.*verif'],
                'percentage_overflow': ['percentage.*overflow', 'percentage.*higher.*100', 'invalid.*percentage'],
                'address_validation_missing': ['address.*valid.*miss', 'canonical.*address', 'address.*normalizat'],
                'type_validation_missing': ['type.*valid.*miss', 'wrong.*type', 'invalid.*type'],
                'duplicate_validation_missing': ['duplicate.*valid.*miss', 'duplicate.*entry', 'no.*duplicate.*check'],
                'configuration_validation': ['config.*valid', 'param.*valid', 'invalid.*config', 'setparams.*bypass'],
            },
            'keywords': ['input-validation', 'missing-check', 'zero-check', 'bounds-check', 'parameter-validation', 'address-validation', 'type-check', 'configuration'],
        },

        # ===== TOKEN HANDLING =====
        'token/token-handling-vulnerabilities': {
            'title': 'Token Transfer and Handling Vulnerabilities',
            'patterns': {
                'fee_on_transfer_error': ['fee.*on.*transfer', 'deflationary.*token', 'transfer.*amount.*mismatch'],
                'rebasing_token_error': ['rebas.*token', 'negative.*rebase', 'rebase.*accounting'],
                'token_approval_error': ['token.*approval', 'approv.*not.*set', 'allowance.*error'],
                'mint_unlimited': ['unlimited.*mint', 'mint.*vulner', 'uncontrolled.*mint'],
                'burn_error': ['burn.*error', 'burn.*not.*correct', 'burn.*share.*leave.*token'],
                'token_transfer_hook': ['transfer.*hook', 'on.*transfer', 'before.*transfer.*hook'],
                'nft_handling_error': ['nft.*handl.*error', 'nft.*lost', 'nft.*stuck', 'erc721.*error'],
                'token_decimal_handling': ['token.*decimal', 'decimal.*differ.*token', 'multi.*token.*decimal'],
            },
            'keywords': ['token-handling', 'fee-on-transfer', 'rebasing', 'token-approval', 'unlimited-mint', 'NFT', 'ERC20', 'ERC721', 'decimal-handling'],
        },

        # ===== VAULT / SHARE =====
        'vault/vault-share-vulnerabilities': {
            'title': 'Vault Share Inflation and Accounting Vulnerabilities',
            'patterns': {
                'share_inflation_attack': ['share.*inflat.*attack', 'vault.*inflat', 'first.*depositor.*attack'],
                'share_calculation_error': ['share.*calculat.*error', 'incorrect.*share', 'wrong.*share.*amount'],
                'vault_deposit_theft': ['vault.*deposit.*theft', 'front.*deposit.*vault'],
                'vault_withdrawal_error': ['vault.*withdrawal.*error', 'vault.*redeem.*error'],
                'vault_tvl_manipulation': ['vault.*tvl.*manipul', 'total.*asset.*manipul'],
                'vault_strategy_loss': ['vault.*strategy.*loss', 'strategy.*loss.*active.*pool'],
                'vault_griefing': ['vault.*grief', 'vault.*dos', 'vault.*brick'],
                'multi_vault_interaction': ['multi.*vault', 'vault.*interact', 'superpool'],
            },
            'keywords': ['vault', 'share-inflation', 'first-depositor', 'share-calculation', 'TVL-manipulation', 'vault-griefing', 'ERC4626', 'deposit-theft'],
        },

        # ===== ORACLE / PRICE =====
        'oracle/oracle-price-vulnerabilities': {
            'title': 'Oracle and Price Feed Vulnerabilities in Cosmos Protocols',
            'patterns': {
                'stale_price_data': ['stale.*price', 'oracle.*stale', 'outdated.*price', 'staleness.*check'],
                'price_manipulation_attack': ['price.*manipul', 'price.*oracle.*manipul', 'twap.*manipul'],
                'oracle_dos': ['oracle.*dos', 'oracle.*block', 'oracle.*spam'],
                'price_deviation_exploit': ['price.*deviat', 'lst.*deviat', 'depeg.*exploit'],
                'oracle_frontrunning': ['oracle.*frontrun', 'frontrun.*price.*update', 'price.*update.*frontrun'],
                'multi_oracle_inconsistency': ['multi.*oracle', 'oracle.*inconsist', 'oracle.*disagree'],
                'oracle_stake_requirement': ['oracle.*stake.*requir', 'minimum.*oracle.*stake'],
                'price_feed_reliability': ['price.*feed.*reliab', 'rate.*limit', 'api.*rate'],
            },
            'keywords': ['oracle', 'price-feed', 'stale-price', 'manipulation', 'TWAP', 'deviation', 'frontrunning', 'Chainlink', 'price-oracle', 'staleness'],
        },

        # ===== LIQUIDATION / AUCTION =====
        'liquidation/liquidation-auction-vulnerabilities': {
            'title': 'Liquidation and Auction Mechanism Vulnerabilities',
            'patterns': {
                'liquidation_threshold_error': ['liquidat.*threshold.*error', 'health.*factor.*incorrect', 'liquidatable.*check.*wrong'],
                'liquidation_frontrunning': ['liquidat.*frontrun', 'frontrun.*liquidat'],
                'auction_manipulation': ['auction.*manipul', 'auction.*grief', 'auction.*dos', 'bid.*manipulat'],
                'cdp_dust_position': ['cdp.*dust', 'dust.*position', 'tiny.*cdp'],
                'debt_accounting_error': ['debt.*account.*error', 'debt.*calculat.*incorrect'],
                'collateral_ratio_bypass': ['collateral.*ratio.*bypass', 'collateral.*ratio.*error'],
                'liquidation_cascade': ['liquidat.*cascade', 'cascading.*liquidat'],
                'bad_debt_accumulation': ['bad.*debt.*accumulat', 'bad.*debt.*move', 'bad.*debt.*backstop'],
            },
            'keywords': ['liquidation', 'auction', 'CDP', 'collateral', 'debt', 'health-factor', 'bad-debt', 'liquidation-threshold', 'frontrunning', 'cascade'],
        },

        # ===== UPGRADE / MIGRATION =====
        'lifecycle/upgrade-migration-vulnerabilities': {
            'title': 'Upgrade, Migration and Initialization Vulnerabilities',
            'patterns': {
                'upgrade_procedure_error': ['upgrade.*procedure.*error', 'improper.*upgrade', 'cosmos.*sdk.*upgrade'],
                'migration_data_loss': ['migration.*data.*loss', 'migration.*failure', 'loadversion.*failure'],
                'initialization_error': ['initializ.*error', 'double.*init', 'missing.*init'],
                'storage_gap_error': ['storage.*gap', 'storage.*collision', 'proxy.*storage'],
                'proxy_upgrade_error': ['proxy.*upgrade.*error', 'upgrade.*contract.*error'],
                'deployment_parameter_error': ['deployment.*parameter', 'incorrect.*deploy', 'wrong.*config.*deploy'],
                'module_registration_missing': ['module.*registrat.*miss', 'message.*type.*registrat', 'amino.*registrat'],
                'state_migration_error': ['state.*migrat', 'genesis.*migrat', 'zero.*height.*genesis'],
            },
            'keywords': ['upgrade', 'migration', 'initialization', 'storage-gap', 'proxy', 'deployment', 'module-registration', 'genesis', 'state-migration'],
        },

        # ===== SIGNATURE / REPLAY =====
        'signature/signature-replay-vulnerabilities': {
            'title': 'Signature Verification and Replay Attack Vulnerabilities',
            'patterns': {
                'missing_signature_check': ['missing.*signature.*check', 'no.*signature.*verif', 'signature.*not.*valid'],
                'signature_replay': ['signature.*replay', 'replay.*signature', 'cross.*contract.*replay'],
                'cross_chain_replay': ['cross.*chain.*replay', 'hard.*fork.*replay', 'chain.*id.*replay'],
                'signature_forgery': ['signature.*forgery', 'forge.*signature', 'fake.*signature'],
                'duplicate_signature': ['duplicate.*signature', 'duplicate.*validator.*sig'],
                'nonce_manipulation': ['nonce.*manipul', 'nonce.*contract.*creation'],
                'eip155_missing': ['eip.*155.*miss', 'chain.*id.*valid'],
                'key_management_error': ['key.*management', 'private.*key.*arg', 'keyring.*password', 'insecure.*key'],
            },
            'keywords': ['signature', 'replay-attack', 'cross-chain-replay', 'signature-verification', 'nonce', 'EIP-155', 'chain-ID', 'signature-forgery', 'key-management'],
        },

        # ===== REENTRANCY =====
        'reentrancy/reentrancy-vulnerabilities': {
            'title': 'Reentrancy Vulnerabilities in Cosmos/EVM Hybrid Chains',
            'patterns': {
                'classic_reentrancy': ['classic.*reentrancy', 'reentrancy.*steal', 'safemint.*reentrancy'],
                'cross_contract_reentrancy': ['cross.*contract.*reentrancy', 'external.*call.*reentrancy'],
                'erc777_reentrancy': ['erc777.*reentrancy', 'hook.*reentrancy', 'callback.*reentrancy'],
                'read_only_reentrancy': ['read.*only.*reentrancy', 'view.*function.*reentranc'],
                'effects_before_interactions': ['check.*effect.*interact', 'state.*before.*call'],
                'cross_function_reentrancy': ['cross.*function.*reentrancy'],
                'reentry_check_error': ['reentry.*check.*error', 'reentrancy.*guard.*error', 'concurrent.*init'],
            },
            'keywords': ['reentrancy', 'cross-contract', 'callback', 'safeMint', 'ERC777', 'read-only-reentrancy', 'checks-effects-interactions'],
        },

        # ===== FRONTRUNNING / MEV =====
        'mev/frontrunning-mev-vulnerabilities': {
            'title': 'Frontrunning and MEV Exploitation Vulnerabilities',
            'patterns': {
                'staking_frontrunning': ['stak.*frontrun', 'frontrun.*stak', 'deposit.*frontrun'],
                'price_update_frontrunning': ['price.*update.*frontrun', 'oracle.*frontrun', 'lst.*price.*frontrun'],
                'mev_tvl_exploit': ['mev.*tvl', 'mev.*exploit.*tvl'],
                'sandwich_attack': ['sandwich.*attack', 'sandwich.*staking'],
                'block_stuffing': ['block.*stuff', 'block.*fill'],
                'arbitrage_exploit': ['arbitrag.*exploit', 'rate.*arbitrag'],
                'slippage_exploit': ['slippage.*exploit', 'no.*slippage.*protect'],
                'priority_manipulation': ['priorit.*manipulat', 'gas.*price.*manipul', 'oracle.*messag.*priorit'],
            },
            'keywords': ['frontrunning', 'MEV', 'sandwich-attack', 'arbitrage', 'slippage', 'block-stuffing', 'priority', 'gas-price', 'staking-frontrun'],
        },

        # ===== ABCI LIFECYCLE =====
        'abci/abci-lifecycle-vulnerabilities': {
            'title': 'ABCI Lifecycle and Module Hook Vulnerabilities',
            'patterns': {
                'beginblock_vulnerability': ['beginblock.*vulner', 'beginblock.*error', 'beginblock.*dos'],
                'endblock_vulnerability': ['endblock.*vulner', 'endblock.*error', 'endblock.*dos'],
                'prepareproposal_error': ['prepareproposal.*error', 'prepareproposal.*incorrect'],
                'processproposal_error': ['processproposal.*error', 'processproposal.*accept.*incorrect'],
                'finalizeblock_error': ['finalizeblock.*error', 'finalizeblock.*non.*determinism'],
                'hook_callback_error': ['hook.*callback.*error', 'module.*hook.*error', 'before.*hook.*error'],
                'ante_handler_vulnerability': ['ante.*handler', 'antehandler.*vulner', 'antehandler.*skip'],
                'module_wiring_error': ['module.*wir.*error', 'module.*not.*wired', 'cli.*command.*not.*work'],
            },
            'keywords': ['ABCI', 'BeginBlock', 'EndBlock', 'PrepareProposal', 'ProcessProposal', 'FinalizeBlock', 'AnteHandler', 'module-hook', 'lifecycle'],
        },

        # ===== MINIPOOL / NODE =====
        'operator/minipool-node-vulnerabilities': {
            'title': 'Minipool and Node Operator Management Vulnerabilities',
            'patterns': {
                'minipool_deposit_theft': ['minipool.*deposit.*theft', 'minipool.*hijack', 'minipool.*steal'],
                'minipool_cancel_error': ['minipool.*cancel.*error', 'minipool.*cancel.*moratorium'],
                'node_operator_slash_avoidance': ['node.*operator.*slash.*avoid', 'node.*operator.*avoid', 'minipool.*slash.*avoid'],
                'node_operator_reward_error': ['node.*operator.*reward.*error', 'node.*operator.*reward.*leak'],
                'minipool_finalization': ['minipool.*finaliz', 'forced.*finaliz', 'minipool.*refund'],
                'operator_registration_frontrun': ['operator.*register.*frontrun', 'endpoint.*frontrun'],
                'minipool_replay': ['minipool.*replay', 'create2.*destroy.*replay'],
                'node_operator_can_claim': ['node.*operator.*claim', 'operator.*claim.*without'],
            },
            'keywords': ['minipool', 'node-operator', 'deposit-theft', 'hijacking', 'finalization', 'operator-registration', 'replay', 'reward-leak'],
        },

        # ===== MISCELLANEOUS =====
        'misc/btc-staking-vulnerabilities': {
            'title': 'BTC Staking and Babylon Integration Vulnerabilities',
            'patterns': {
                'btc_staking_tx_validation': ['btc.*staking.*tx', 'staking.*tx.*coinbase', 'btc.*tx.*valid'],
                'btc_unbonding_handling': ['btc.*unbonding', 'unbonding.*transaction', 'spending.*unbonding'],
                'btc_delegation_finality': ['btc.*delegation.*final', 'babylon.*delegation', 'finality.*provider'],
                'btc_change_output': ['btc.*change.*output', 'unspent.*btc', 'change.*output'],
                'btc_slashable_stake': ['btc.*slashable', 'slashable.*stake.*btc', 'unslashable.*btc'],
                'btc_staking_script': ['staking.*script', 'btc.*staking.*script', 'staker.*key.*finality'],
                'btc_covenant_signature': ['covenant.*signature', 'covenant.*expired'],
                'btc_indexer_error': ['staking.*indexer', 'btc.*indexer', 'indexer.*error'],
            },
            'keywords': ['BTC-staking', 'Babylon', 'Bitcoin', 'unbonding', 'finality-provider', 'covenant', 'staking-script', 'UTXO', 'slashable'],
        },
        'misc/security-infrastructure-vulnerabilities': {
            'title': 'Security Infrastructure and Operational Vulnerabilities',
            'patterns': {
                'ssrf_vulnerability': ['ssrf', 'server.*side.*request.*forger'],
                'private_key_exposure': ['private.*key.*expos', 'private.*key.*argument', 'command.*line.*key'],
                'tss_vulnerability': ['tss.*manager', 'tss.*single.*point', 'tss.*node.*reporting'],
                'keyring_insecurity': ['keyring.*insecur', 'keyring.*password', 'unencrypted.*url'],
                'documentation_mismatch': ['documentation.*mismatch', 'documentation.*inconsist', 'code.*documentation.*mismatch'],
                'error_handling_missing': ['error.*handl.*miss', 'unhandled.*error', 'silent.*error'],
                'raptorcast_vulnerability': ['raptorcast', 'broadcast.*redundanc', 'raptorcast.*memory'],
                'shred_overflow': ['shred.*overflow', 'shred.*tile'],
            },
            'keywords': ['SSRF', 'private-key', 'TSS', 'keyring', 'error-handling', 'documentation', 'broadcast', 'operational-security'],
        },
    }
    
    # Classify each report
    entry_reports = defaultdict(lambda: defaultdict(list))
    unclassified = []
    
    for report in reports:
        fname = report['file'].lower()
        title = report['title'].lower()
        overview = report['overview'].lower()
        finding = report.get('finding', '').lower()
        combined = f"{fname} {title} {overview} {finding}"
        
        matched = False
        for entry_key, entry_info in entries.items():
            for pattern_name, keywords in entry_info['patterns'].items():
                for kw in keywords:
                    if re.search(kw, combined):
                        entry_reports[entry_key][pattern_name].append(report)
                        matched = True
                        break
                if matched:
                    break
            if matched:
                break
        
        if not matched:
            unclassified.append(report)
    
    return entries, entry_reports, unclassified


def generate_entry(entry_key, entry_info, pattern_reports, all_entry_reports):
    """Generate a DB entry markdown file content."""
    
    title = entry_info['title']
    keywords = entry_info['keywords']
    patterns = entry_info['patterns']
    
    # Collect all reports for this entry
    all_reports_for_entry = []
    for pattern_name, reports in pattern_reports.items():
        all_reports_for_entry.extend(reports)
    
    # Deduplicate
    seen_files = set()
    unique_reports = []
    for r in all_reports_for_entry:
        if r['file'] not in seen_files:
            seen_files.add(r['file'])
            unique_reports.append(r)
    
    if not unique_reports:
        return None
    
    # Determine severity
    sev_counts = defaultdict(int)
    for r in unique_reports:
        sev_counts[r['severity']] += 1
    
    primary_severity = max(sev_counts, key=sev_counts.get)
    
    # Determine protocols
    protocols = set(r['protocol'] for r in unique_reports if r['protocol'] != 'unknown')
    audit_firms = set(r['audit_firm'] for r in unique_reports if r['audit_firm'] != 'unknown')
    
    # Category from key
    parts = entry_key.split('/')
    category = parts[0]
    
    # Build primitives from pattern names
    primitives = list(patterns.keys())[:15]
    
    # Build references
    references = []
    high_reports = [r for r in unique_reports if r['severity'] == 'high']
    medium_reports = [r for r in unique_reports if r['severity'] == 'medium']
    
    # Take up to 20 references, prioritizing high severity
    ref_reports = high_reports[:12] + medium_reports[:8]
    if len(ref_reports) < 5:
        ref_reports = unique_reports[:20]
    
    for r in ref_reports[:20]:
        references.append(f"- [{r['file']}]({REL_REPORTS}/{r['file']})")
    
    # Build vulnerability patterns section
    pattern_sections = []
    pattern_count = 0
    
    for pattern_name, reports in sorted(pattern_reports.items(), key=lambda x: -len(x[1])):
        if not reports:
            continue
        
        pattern_count += 1
        report_count = len(reports)
        
        # Get severity distribution
        pat_sevs = defaultdict(int)
        for r in reports:
            pat_sevs[r['severity']] += 1
        sev_label = 'HIGH' if pat_sevs.get('high', 0) > pat_sevs.get('medium', 0) else 'MEDIUM'
        
        # Get unique protocols for this pattern
        pat_protocols = set(r['protocol'] for r in reports if r['protocol'] != 'unknown')
        pat_firms = set(r['audit_firm'] for r in reports if r['audit_firm'] != 'unknown')
        
        # Validation strength
        if len(pat_firms) >= 3:
            strength = "Strong"
        elif len(pat_firms) >= 2:
            strength = "Moderate"
        else:
            strength = "Weak"
        
        # Get code examples from reports
        code_examples = []
        for r in reports:
            if r.get('code_blocks'):
                for code in r['code_blocks'][:2]:
                    if len(code.strip()) > 30 and len(code.strip()) < 2000:
                        code_examples.append({
                            'code': code.strip(),
                            'protocol': r['protocol'],
                            'severity': r['severity'],
                            'file': r['file'],
                        })
                        if len(code_examples) >= 3:
                            break
            if len(code_examples) >= 3:
                break
        
        # Build pattern description using report overviews
        descriptions = [r['overview'][:300] for r in reports[:3] if r['overview']]
        pattern_desc = descriptions[0] if descriptions else f"Vulnerability pattern: {pattern_name.replace('_', ' ')}"
        
        human_name = pattern_name.replace('_', ' ').title()
        
        section = f"""
#### Pattern {pattern_count}: {human_name}

**Frequency**: {report_count}/{len(unique_reports)} reports | **Severity**: {sev_label} | **Validation**: {strength} ({len(pat_firms)} auditors)
**Protocols affected**: {', '.join(list(pat_protocols)[:5]) if pat_protocols else 'Multiple'}

{pattern_desc[:400]}
"""
        
        # Add code examples
        for i, ex in enumerate(code_examples[:2]):
            section += f"""
**Example {pattern_count}.{i+1}** [{ex['severity'].upper()}] — {ex['protocol']}
Source: `{ex['file']}`
```solidity
// ❌ VULNERABLE: {human_name}
{ex['code'][:800]}
```
"""
        
        pattern_sections.append(section)
    
    # Build the full entry
    total_reports = len(unique_reports)
    high_count = sev_counts.get('high', 0)
    medium_count = sev_counts.get('medium', 0)
    
    content = f"""---
# Core Classification
protocol: cosmos-sdk
chain: everychain
category: {category}
vulnerability_type: {entry_key.split('/')[-1].replace('-', '_')}

# Attack Vector Details
attack_type: economic_exploit
affected_component: staking_module

# Technical Primitives
primitives:
{chr(10).join(f'  - {p}' for p in primitives)}

# Impact Classification
severity: {primary_severity}
impact: fund_loss
exploitability: 0.7
financial_impact: high

# Context Tags
tags:
  - cosmos_sdk
  - {category.replace('-', '_')}
{chr(10).join(f'  - {kw.replace("-", "_")}' for kw in keywords[:8])}
  
language: go
version: all
---

## References
{chr(10).join(references)}

## Vulnerability Title

**{title}**

### Overview

This entry documents {pattern_count} distinct vulnerability patterns extracted from {total_reports} audit reports ({high_count} HIGH, {medium_count} MEDIUM severity) across {len(protocols)} protocols by {len(audit_firms)} independent audit firms. These patterns represent recurring security issues in Cosmos SDK appchains and related staking/infrastructure protocols, validated through cross-auditor analysis.

### Vulnerability Description

#### Root Cause

These vulnerabilities fundamentally stem from:

1. **Missing state transition guards**: Critical operations lack proper checks for concurrent or conflicting state changes
2. **Incomplete accounting**: Balance, share, or reward tracking fails to account for edge cases (slashing, rebasing, pending operations)
3. **Timing window exploitation**: Race conditions between mempool visibility and transaction execution enable frontrunning attacks
4. **Cross-module inconsistency**: State tracked independently across modules can become desynchronized
5. **Insufficient validation**: Input parameters, state preconditions, or return values not properly validated

#### Attack Scenarios
{''.join(pattern_sections)}

### Impact Analysis

#### Technical Impact
- State corruption across staking/delegation modules
- Incorrect balance tracking leading to fund misallocation
- Protocol liveness degradation or complete halt
- Loss of economic security guarantees

#### Business Impact
- Direct financial loss for stakers/delegators: Documented in {high_count} HIGH severity findings
- Protocol insolvency risk due to accounting errors
- Erosion of trust in validator/operator incentive alignment
- Cascading effects across DeFi protocols built on affected infrastructure

#### Frequency Analysis
- Total reports analyzed: {total_reports}
- HIGH severity: {high_count} ({high_count*100//total_reports}%)
- MEDIUM severity: {medium_count} ({medium_count*100//total_reports}%)
- Unique protocols affected: {len(protocols)}
- Independent audit firms: {len(audit_firms)}
- Patterns with 3+ auditor validation (Strong): {sum(1 for p, rs in pattern_reports.items() if len(set(r['audit_firm'] for r in rs)) >= 3)}

### Detection Patterns

#### Code Patterns to Look For
```
- Missing balance update before/after token transfers
- Unchecked return values from staking/delegation operations
- State reads without freshness validation
- Arithmetic operations without overflow/precision checks
- Missing access control on state-modifying functions
- Linear iterations over unbounded collections
- Race condition windows in multi-step operations
```

#### Audit Checklist
- [ ] Verify all staking state transitions update balances atomically
- [ ] Check that slashing affects all relevant state (pending, queued, active)
- [ ] Ensure withdrawal requests cannot bypass cooldown periods
- [ ] Validate that reward calculations handle all edge cases (zero stake, partial periods)
- [ ] Confirm access control on all administrative and state-modifying functions
- [ ] Test for frontrunning vectors in all two-step operations
- [ ] Verify iteration bounds on all loops processing user-controlled data
- [ ] Check cross-module state consistency after complex operations

### Keywords for Search

> {', '.join(f'`{kw}`' for kw in keywords)}, `cosmos-sdk`, `appchain`, `CometBFT`, `staking-security`, `validator-security`

### Related Vulnerabilities

- Slashing evasion bypass patterns
- Epoch snapshot timing manipulation
- Chain halt DoS vectors
- EVM-Cosmos state synchronization issues
- IBC middleware vulnerabilities
"""
    
    return content, pattern_count


def main():
    print("=" * 80)
    print("COSMOS VULNERABILITY DATABASE ENTRY GENERATOR")
    print("=" * 80)
    
    # Parse all reports
    reports_path = Path(REPORTS_DIR)
    files = sorted(reports_path.glob("*.md"))
    
    print(f"\nParsing {len(files)} reports...")
    reports = []
    for f in files:
        try:
            report = parse_report(str(f))
            reports.append(report)
        except Exception as e:
            pass
    
    print(f"Successfully parsed {len(reports)} reports")
    
    # Classify
    print("\nClassifying reports...")
    entries, entry_reports, unclassified = classify_reports(reports)
    
    print(f"\nClassification results:")
    print(f"  Classified entries: {len(entry_reports)}")
    print(f"  Unclassified reports: {len(unclassified)}")
    
    # Generate entries
    print("\nGenerating DB entries...")
    total_patterns = 0
    generated_files = []
    
    for entry_key, entry_info in entries.items():
        if entry_key not in entry_reports or not entry_reports[entry_key]:
            continue
        
        # Create directory path
        dir_path = os.path.join(DB_DIR, os.path.dirname(entry_key))
        os.makedirs(dir_path, exist_ok=True)
        
        file_path = os.path.join(DB_DIR, f"{entry_key.split('/')[-1]}.md")
        dir_for_file = os.path.join(DB_DIR, os.path.dirname(entry_key))
        os.makedirs(dir_for_file, exist_ok=True)
        
        result = generate_entry(entry_key, entry_info, entry_reports[entry_key], entry_reports)
        
        if result:
            content, pattern_count = result
            
            # Write file
            full_path = os.path.join(DB_DIR, os.path.dirname(entry_key), f"{entry_key.split('/')[-1]}.md")
            with open(full_path, 'w') as f:
                f.write(content)
            
            total_patterns += pattern_count
            generated_files.append((full_path, pattern_count))
            print(f"  ✓ {full_path}: {pattern_count} patterns")
    
    print(f"\n{'='*80}")
    print(f"GENERATION COMPLETE")
    print(f"{'='*80}")
    print(f"Total files generated: {len(generated_files)}")
    print(f"Total patterns indexed: {total_patterns}")
    print(f"Total reports processed: {len(reports)}")
    print(f"Unclassified reports: {len(unclassified)}")
    
    # Print unclassified for manual review
    if unclassified:
        print(f"\nTop unclassified reports:")
        for r in unclassified[:20]:
            print(f"  - [{r['severity']}] {r['title'][:80]}")
    
    return generated_files, total_patterns


if __name__ == "__main__":
    main()
