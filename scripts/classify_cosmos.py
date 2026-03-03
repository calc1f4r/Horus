#!/usr/bin/env python3
"""Multi-classify cosmos reports into fine-grained patterns."""

import os, yaml, re, json, sys
from collections import defaultdict

reports_dir = "reports/cosmos_cometbft_findings"
files = sorted(os.listdir(reports_dir))

# Parse ALL reports 
all_reports = []
for f in files:
    path = os.path.join(reports_dir, f)
    try:
        with open(path, 'r', errors='replace') as fh:
            content = fh.read()
        meta = {}
        if content.startswith('---'):
            end_idx = content.index('---', 3)
            yaml_str = content[3:end_idx]
            meta = yaml.safe_load(yaml_str) or {}
            body = content[end_idx+3:].strip()
        else:
            body = content.strip()
        title_match = re.search(r'## Vulnerability Title\s*\n+(.+)', body)
        title = title_match.group(1).strip() if title_match else f.replace('.md','').replace('-',' ')
        overview_match = re.search(r'### Overview\s*\n+(.*?)(?=\n###|\Z)', body, re.DOTALL)
        overview = overview_match.group(1).strip()[:800] if overview_match else ""
        finding_match = re.search(r'### Original Finding Content\s*\n+(.*?)(?=\n## |\Z)', body, re.DOTALL)
        finding = finding_match.group(1).strip()[:2000] if finding_match else ""
        code_blocks = re.findall(r'```(?:solidity|go|rust|move|javascript|python|typescript|)?\s*\n(.*?)```', body, re.DOTALL)
        
        combined_text = f"{f} {title} {overview} {finding}".lower()
        all_reports.append({
            'file': f, 'title': title, 'overview': overview, 'finding': finding,
            'severity': meta.get('severity', 'unknown'),
            'protocol': meta.get('protocol', 'unknown'),
            'audit_firm': meta.get('audit_firm', 'unknown'),
            'code_blocks': [c.strip() for c in code_blocks if 30 < len(c.strip()) < 3000][:5],
            'combined': combined_text,
        })
    except:
        pass

print(f"Parsed {len(all_reports)} reports")

# Comprehensive patterns dictionary keyed by pattern-id -> keywords
patterns_flat = {
    # STAKING - Core
    'staking-deposit-amount-tracking': ['deposit.*amount', 'stake.*amount', 'staking.*amount', 'deposit.*track', 'total.*staked'],
    'staking-deposit-validation': ['minimum.*stake', 'deposit.*valid', 'stake.*valid', 'stake.*limit', 'max.*stake'],
    'staking-deposit-frontrunning': ['deposit.*frontrun', 'frontrun.*deposit', 'deposit.*before', 'front.*run.*stake'],
    'staking-balance-desync': ['balance.*desync', 'balance.*mismatch', 'staked.*balance.*incorrect', 'balance.*out.*sync', 'accounting.*inconsist'],
    'staking-deposit-queue': ['deposit.*queue', 'pending.*deposit', 'deposit.*delay', 'deposit.*cache'],
    'staking-deposit-inflation': ['first.*deposit', 'share.*inflation', 'inflation.*attack', 'donation.*attack', 'depressing.*share'],
    'staking-incorrect-calculation': ['incorrect.*calculation', 'wrong.*calculation', 'miscalculat', 'math.*error'],
    'staking-invariant-broken': ['invariant.*broken', 'invariant.*violat', 'break.*invariant'],

    # STAKING - Unstaking/Withdrawal
    'unstake-cooldown-bypass': ['cooldown.*bypass', 'bypass.*cooldown', 'unstake.*immediate', 'skip.*cooldown', 'bypass.*lockup'],
    'unstake-withdrawal-dos': ['withdraw.*dos', 'withdraw.*revert', 'withdraw.*fail', 'unable.*withdraw', 'withdraw.*stuck', 'withdraw.*block'],
    'unstake-withdrawal-accounting': ['withdraw.*account', 'withdraw.*amount.*incorrect', 'withdraw.*too.*much', 'over.*withdraw'],
    'unstake-queue-manipulation': ['withdraw.*queue', 'unstake.*queue', 'queue.*manipulat', 'queue.*order'],
    'unstake-before-slash': ['unstake.*before.*slash', 'withdraw.*before.*slash', 'exit.*before.*penalty', 'unstake.*avoid.*slash'],
    'unstake-emergency': ['emergency.*withdraw', 'emergency.*exit', 'force.*withdraw', 'emergency.*unstake'],
    'unstake-pending-not-tracked': ['pending.*unstake', 'pending.*withdraw', 'in.*flight.*withdraw'],
    'unstake-lock-funds': ['fund.*stuck.*unstake', 'cannot.*unstake', 'unstake.*revert', 'unstake.*impossible'],

    # DELEGATION
    'delegation-self-manipulation': ['self.*delegat', 'self-delegation', 'delegator.*reset'],
    'delegation-dos-revert': ['delegat.*dos', 'delegat.*prevent', 'delegat.*revert', 'undelegat.*revert'],
    'delegation-state-inconsistency': ['delegat.*state.*inconsist', 'delegat.*state.*corrupt', 'delegator.*fund.*mismanag', 'mismanagement.*delegat'],
    'delegation-to-inactive': ['delegat.*inactive', 'delegat.*jailed', 'stake.*inactive', 'new.*stake.*inactive'],
    'delegation-frontrunning': ['delegat.*frontrun', 'front.*delegat', 'delegat.*front.*run'],
    'delegation-reward-manipulation': ['delegat.*reward', 'delegator.*reward', 'delegation.*reward.*steal'],
    'delegation-redelegation-error': ['redelegat.*error', 'redelegat.*incorrect', 'redelegat.*track', 'pending.*redelegat'],
    'delegation-unbonding-exploit': ['unbonding.*exploit', 'unbond.*bypass', 'unbonding.*time', 'bonding.*bypass'],

    # VALIDATOR
    'validator-registration-bypass': ['validator.*register.*bypass', 'unrestrict.*validator', 'anyone.*validator', 'unauthorized.*valid'],
    'validator-removal-failure': ['validator.*remov.*fail', 'validator.*cannot.*remov', 'stuck.*validator', 'unremovable.*validator'],
    'validator-set-manipulation': ['validator.*set.*manipul', 'voting.*power.*manipul', 'voting.*power.*incorrect', 'validator.*power'],
    'validator-key-rotation': ['key.*rotat', 'consensus.*key', 'bls.*key.*overwr', 'rotate.*key'],
    'validator-commission-exploit': ['commission.*manipul', 'commission.*rate.*chang', 'commission.*exploit', 'commission.*front'],
    'validator-status-transition': ['validator.*status.*transit', 'inactive.*to.*active', 'jailed.*unjail', 'validator.*state.*desync'],
    'validator-dust-collateral': ['dust.*collateral', 'minimum.*collateral.*bypass', 'dust.*validator', 'validator.*dust'],
    'validator-score-manipulation': ['validator.*score', 'past.*validator.*score', 'validator.*weight', 'argmax.*block.*stake'],
    'validator-operator-mismatch': ['operator.*key.*mismatch', 'node.*id.*reuse', 'operator.*not.*match', 'historical.*node.*id'],
    'validator-can-skip-exit': ['validator.*skip', 'validator.*quickly.*re-register', 'validator.*skip.*exit'],
    'validator-governance-power': ['governance.*power.*validator', 'validator.*governance', 'validator.*govern.*influen'],

    # SLASHING
    'slashing-frontrun-exit': ['frontrun.*slash', 'exit.*before.*slash', 'slash.*frontrun', 'withdraw.*before.*slash', 'frontrun.*penalty'],
    'slashing-cooldown-exploit': ['cooldown.*slash', 'activate.*cooldown.*before.*slash', 'cooldown.*during.*pause', 'evade.*slash.*cooldown'],
    'slashing-delegation-bypass': ['delegat.*slash.*bypass', 'redeleg.*avoid.*slash', 'transfer.*avoid.*slash'],
    'slashing-insufficient-deposit': ['insufficient.*deposit.*slash', 'reduce.*deposit.*before', 'deposit.*below.*slash'],
    'slashing-external-block': ['plugin.*slash.*block', 'external.*contract.*slash', 'slash.*revert.*extern', 'slash.*callback.*revert'],
    'slashing-queued-excluded': ['queued.*withdrawal.*slash', 'pending.*withdrawal.*slash', 'exclude.*slashable', 'withdrawal.*not.*slash'],
    'slashing-unregistered-operator': ['unregist.*slash', 'slash.*unregist', 'operator.*not.*register.*slash'],
    'slashing-amount-incorrect': ['slash.*amount.*incorrect', 'slash.*calculat.*wrong', 'wrong.*slash', 'over.*slash', 'under.*slash'],
    'slashing-share-dilution': ['slash.*share.*dilut', 'slash.*induced.*dilut', 'dilution.*slash'],
    'slashing-balance-update-error': ['slash.*balance.*update', 'balance.*after.*slash', 'slash.*not.*reflect', 'slash.*balance.*incorrect'],
    'slashing-reward-interaction': ['slash.*reward', 'reward.*after.*slash', 'slash.*affect.*reward', 'slash.*reward.*interact'],
    'slashing-pending-operations': ['slash.*pending', 'slash.*queued', 'slash.*in.*progress', 'slash.*during.*withdraw'],
    'slashing-mechanism-abuse': ['slash.*mechanism.*abus', 'exponential.*slash', 'slash.*incentiv', 'slash.*grant.*more.*reward'],
    'slashing-principal-error': ['slash.*principal', 'slash.*staker.*principal', 'exponential.*decay.*slash'],
    'slashing-penalty-system': ['penalty.*system', 'penalty.*delay', 'penalty.*instead.*reduc'],
    'slashing-double-punishment': ['double.*slash', 'slash.*twice', 'double.*jeopardy', 'double.*punish'],
    'slashing-tombstone': ['tombstone.*error', 'tombstone.*miss', 'slash.*tombstone'],

    # REWARDS
    'reward-calculation-incorrect': ['reward.*calculat.*incorrect', 'reward.*amount.*wrong', 'incorrect.*reward.*calculat', 'wrong.*reward'],
    'reward-per-share-error': ['reward.*per.*share', 'reward.*ratio.*error', 'reward.*rate.*incorrect'],
    'reward-accumulation-error': ['reward.*accumulat.*error', 'reward.*accumulator', 'global.*reward.*incorrect'],
    'reward-delayed-balance': ['delayed.*balance.*reward', 'pending.*balance.*reward', 'delayed.*reward'],
    'reward-decimal-mismatch': ['decimal.*mismatch.*reward', 'precision.*reward', 'reward.*precision'],
    'reward-weight-error': ['weight.*reward.*incorrect', 'stake.*weight.*reward', 'weight.*calculat.*incorrect'],
    'reward-historical-loss': ['historical.*reward.*loss', 'past.*reward.*lost', 'reward.*loss.*reuse', 'node.*id.*reuse.*reward'],
    'reward-flashloan-theft': ['flashloan.*reward', 'flash.*loan.*stak', 'borrow.*stake.*exit'],
    'reward-frontrunning': ['frontrun.*reward', 'sandwich.*reward', 'mev.*reward'],
    'reward-orphaned-capture': ['orphan.*reward', 'first.*staker.*reward', 'unassign.*reward', 'captured.*first'],
    'reward-dilution': ['reward.*dilut', 'dilut.*existing.*staker', 'new.*staker.*dilut', 'new.*stake.*dilut'],
    'reward-stuck-locked': ['reward.*stuck', 'reward.*locked', 'reward.*trapped', 'bgt.*reward.*lock'],
    'reward-distribution-dos': ['reward.*distribut.*dos', 'reward.*distribut.*revert', 'reward.*distribut.*fail'],
    'reward-missing-update': ['missing.*reward.*update', 'reward.*not.*accrued', 'reward.*not.*updated', 'reward.*update.*miss'],
    'reward-after-removal': ['reward.*after.*remov', 'claim.*after.*exit', 'reward.*removed.*operator', 'continue.*earn.*after.*remov'],
    'reward-escrow-assignment': ['reward.*escrow', 'incorrect.*escrow', 'escrow.*assign', 'wrong.*escrow'],
    'reward-commission-error': ['commission.*error', 'commission.*calculat', 'dao.*commission', 'commission.*loss'],
    'reward-unclaimed-loss': ['unclaimed.*reward', 'unclaimed.*loss', 'reward.*claim.*miss', 'reward.*not.*claim'],
    'reward-distribution-unfair': ['unfair.*reward', 'uneven.*reward', 'reward.*distribut.*unfair', 'unfair.*distribut'],
    'reward-epoch-timing': ['reward.*epoch', 'reward.*between.*epoch', 'reward.*not.*queue'],
    'reward-gauge-exploit': ['gauge.*reward', 'gauge.*manipul', 'gauge.*exploit', 'gauge.*weight'],
    'reward-vault-interaction': ['reward.*vault.*interact', 'vault.*reward', 'bgt.*station.*reward'],
    'reward-pool-share': ['reward.*pool.*share', 'pool.*reward.*share', 'cutting.*board.*share'],

    # DOS / CHAIN HALT
    'dos-block-production-halt': ['block.*produc.*halt', 'block.*produc.*stop', 'halt.*block', 'stop.*produc'],
    'dos-consensus-halt': ['consensus.*halt', 'consensus.*stuck', 'consensus.*deadlock', 'chain.*halt'],
    'dos-state-machine': ['state.*machine.*halt', 'beginblock.*halt', 'endblock.*halt', 'beginblock.*dos'],
    'dos-unbounded-beginblock': ['unbounded.*beginblock', 'linear.*iteration.*beginblock', 'iteration.*beginblock'],
    'dos-unbounded-endblock': ['unbounded.*endblock', 'endblock.*loop', 'iteration.*endblock'],
    'dos-unbounded-array': ['unbounded.*array', 'unbounded.*size', 'array.*unbounded', 'unbounded.*loop', 'unbounded.*iteration'],
    'dos-gas-limit-exploit': ['gas.*limit.*exploit', 'block.*gas.*limit', 'exceed.*gas', 'gas.*limit.*high'],
    'dos-gas-metering-bypass': ['gas.*meter.*bypass', 'no.*gas.*charg', 'gas.*not.*consum', 'free.*gas'],
    'dos-memory-exhaustion': ['memory.*exhaust', 'memory.*attack', 'oom.*attack', 'memory.*flood'],
    'dos-storage-exhaustion': ['storage.*exhaust', 'storage.*spam', 'state.*bloat', 'payload.*storage'],
    'dos-large-payload': ['large.*payload', 'oversiz.*payload', 'max.*bytes', 'large.*erc20.*name'],
    'dos-function-revert': ['function.*always.*revert', 'function.*will.*revert', 'permanent.*revert', 'will.*always.*revert'],
    'dos-panic-crash': ['panic.*dos', 'crash.*dos', 'nil.*pointer', 'index.*out.*range', 'syncing.*node.*panic'],
    'dos-frontrun-grief': ['frontrun.*dos', 'grief.*frontrun', 'dos.*frontrun', 'grief.*dos', 'block.*stuff'],
    'dos-dust-grief': ['dust.*amount.*dos', 'minimal.*amount.*dos', 'tiny.*deposit.*grief', 'dust.*dos'],
    'dos-external-call-revert': ['external.*call.*revert', 'callback.*revert.*dos', 'hook.*revert.*dos'],
    'dos-deposit-spam': ['spam.*deposit', 'deposit.*spam', 'chain.*halt.*spam'],
    'dos-message-flooding': ['message.*flood', 'message.*spam', 'msg.*flood'],
    'dos-proposal-spam': ['proposal.*spam', 'proposal.*flood', 'governance.*proposal.*dos'],
    'dos-tx-replay': ['tx.*replay.*dos', 'replay.*dos', 'replay.*caus.*revert'],
    'dos-loop-revert': ['loop.*revert', 'iteration.*revert', 'for.*loop.*dos', 'while.*loop.*dos'],

    # FUND SAFETY
    'funds-theft-auth-bypass': ['unauthorized.*withdraw', 'anyone.*withdraw', 'theft.*lack.*auth', 'anyone.*claim'],
    'funds-theft-manipulation': ['manipulat.*steal', 'manipulat.*drain', 'exploit.*drain', 'steal.*fund'],
    'funds-theft-reentrancy': ['reentrancy.*steal', 'reentrant.*drain', 'reentrancy.*theft'],
    'funds-theft-delegatecall': ['delegatecall.*theft', 'delegatecall.*drain', 'delegatecall.*precompile'],
    'funds-theft-replay': ['replay.*theft', 'replay.*steal', 'replay.*drain'],
    'funds-theft-frontrunning': ['frontrun.*steal', 'sandwich.*steal', 'mev.*steal'],
    'funds-theft-surplus': ['surplus.*balance.*theft', 'excess.*balance.*steal', 'surplus.*steal'],
    'funds-lock-permanent': ['permanent.*lock', 'fund.*forever.*lock', 'irrecoverable', 'fund.*stuck.*forever'],
    'funds-lock-conditional': ['fund.*lock.*condition', 'lock.*upon', 'lock.*if.*slash', 'fund.*lock.*event'],
    'funds-insolvency-protocol': ['protocol.*insolven', 'insolven.*protocol', 'protocol.*insolvent'],
    'funds-insolvency-slash': ['insolven.*slash', 'slash.*cause.*insolven', 'slash.*insolven'],
    'funds-insolvency-rebase': ['insolven.*rebase', 'negative.*rebase.*insolven', 'steth.*slash', 'lido.*slash'],
    'funds-bad-debt': ['bad.*debt', 'undercollateral', 'debt.*exceed'],
    'funds-withdrawal-blocked': ['withdrawal.*blocked', 'cannot.*withdraw', 'withdrawal.*prevent', 'withdraw.*impossible'],
    'funds-unsafe-casting-loss': ['unsafe.*cast.*loss', 'fund.*permanent.*lock.*cast', 'truncat.*loss'],
    'funds-race-condition': ['race.*condition.*fund', 'fund.*race', 'fund.*race.*condition'],
    'funds-missing-slippage': ['missing.*slippage', 'no.*slippage', 'slippage.*protect.*miss'],

    # ACCOUNTING
    'accounting-balance-not-updated': ['balance.*not.*updated', 'missing.*balance.*update', 'skip.*balance.*update', 'forget.*update.*balance'],
    'accounting-double-counting': ['double.*count', 'count.*twice', 'duplicate.*account', 'double.*spend'],
    'accounting-tvl-error': ['tvl.*calculat.*error', 'tvl.*incorrect', 'total.*value.*incorrect', 'strategy.*alloc.*track'],
    'accounting-state-corruption': ['state.*corrupt', 'accounting.*corrupt', 'inconsist.*state.*account'],
    'accounting-missing-deduction': ['missing.*deduct', 'not.*subtract', 'forget.*decrement', 'missing.*balance.*deduct'],
    'accounting-cross-module': ['cross.*module.*account', 'module.*balance.*mismatch', 'cross.*module.*fund'],
    'accounting-pending-tracking': ['pending.*amount.*track', 'pending.*track.*miss', 'in.*flight.*amount', 'pending.*not.*account'],
    'accounting-exchange-rate-manipulation': ['exchange.*rate.*manipul', 'share.*price.*manipul', 'rate.*manipulat'],
    'accounting-exchange-rate-stale': ['exchange.*rate.*stale', 'outdated.*exchange.*rate', 'exchange.*rate.*not.*used'],
    'accounting-exchange-rate-error': ['exchange.*rate.*incorrect', 'wrong.*exchange.*rate', 'exchange.*rate.*error'],
    'accounting-share-price-inflation': ['share.*price.*inflat', 'vault.*share.*inflat', 'token.*price.*inflat'],
    'accounting-conversion-rounding': ['conversion.*round', 'round.*conversion', 'share.*round', 'round.*error', 'rounding.*error'],
    'accounting-integer-overflow': ['integer.*overflow', 'overflow.*arithmetic', 'overflow.*calculat', 'overflow.*int'],
    'accounting-integer-underflow': ['integer.*underflow', 'underflow.*subtract', 'potential.*underflow'],
    'accounting-unsafe-casting': ['unsafe.*cast', 'uint256.*uint128', 'downcast.*unsafe', 'truncat.*cast'],
    'accounting-precision-loss': ['precision.*loss', 'precision.*error', 'round.*down.*loss'],
    'accounting-decimal-mismatch': ['decimal.*mismatch', 'different.*decimal', 'decimal.*across.*token'],
    'accounting-negative-value': ['negative.*value.*error', 'negative.*amount', 'negative.*balanc'],
    'accounting-fee-deduction': ['fee.*deduct.*error', 'fee.*not.*deduct', 'fee.*calculat.*incorr'],

    # EVM / PRECOMPILE
    'evm-intrinsic-gas-missing': ['intrinsic.*gas.*miss', 'fail.*charge.*intrinsic', 'intrinsic.*gas.*cost'],
    'evm-gas-refund-error': ['gas.*refund.*incorrect', 'gas.*refund.*block', 'wrong.*gas.*refund'],
    'evm-precompile-gas-hardcode': ['precompile.*gas.*hardcod', 'hardcoded.*gas.*erc20', 'gas.*used.*mismatch'],
    'evm-gas-not-consumed-error': ['gas.*not.*consumed.*fail', 'error.*no.*gas', 'precompile.*fail.*gas'],
    'evm-dirty-state-precompile': ['dirty.*state.*precompile', 'uncommitted.*state', 'state.*before.*precompile'],
    'evm-precompile-panic': ['precompile.*panic', 'precompile.*empty.*calldata', 'stateful.*precompile.*panic'],
    'evm-delegatecall-precompile': ['delegatecall.*precompile', 'delegatecall.*staking', 'precompile.*delegatecall'],
    'evm-bank-balance-sync': ['evm.*bank.*balance', 'bank.*evm.*sync', 'balance.*sync.*evm', 'nibi.*evm.*bank'],
    'evm-nonce-manipulation': ['nonce.*evm', 'nonce.*cosmos.*evm', 'nonce.*contract.*creation'],
    'evm-tx-disguise': ['evm.*tx.*disguis', 'cosmos.*msg.*evm.*disguis', 'regular.*cosmos.*evm'],
    'evm-precompile-outdated': ['precompile.*outdated', 'precompile.*stale', 'total.*supply.*precompile'],
    'evm-gas-mismatch-call': ['gas.*mismatch.*call', 'gas.*used.*mismatch.*call', 'failed.*contract.*call.*gas'],
    'evm-state-revert': ['evm.*state.*revert', 'state.*revert.*evm', 'evm.*transaction.*state'],
    'evm-address-conversion': ['evm.*address.*conver', 'cosmos.*evm.*address', 'eth.*cosmos.*addr'],

    # IBC / BRIDGE
    'ibc-channel-verification': ['ibc.*channel.*verif', 'channel.*open.*ack', 'channel.*handshake.*miss'],
    'ibc-packet-handling': ['ibc.*packet.*handl', 'onrecvpacket.*error', 'packet.*callback.*error'],
    'ibc-version-negotiation': ['ibc.*version.*negotiat', 'channel.*version.*bypass'],
    'ibc-middleware-bypass': ['ibc.*middleware.*bypass', 'middleware.*hook.*bypass', 'l2.*hook.*bypass'],
    'ibc-authentication': ['ibc.*auth', 'onrecvpacket.*auth', 'lack.*auth.*ibc'],
    'ibc-timeout': ['ibc.*timeout', 'timeout.*packet', 'acknowledgement.*timeout'],
    'bridge-replay-attack': ['bridge.*replay', 'cross.*chain.*replay', 'hard.*fork.*replay'],
    'bridge-token-accounting': ['bridge.*token.*account', 'bridge.*balance.*mismatch', 'bridge.*token.*mint'],
    'bridge-relayer-exploit': ['relayer.*manipulat', 'relayer.*avoid.*slash', 'relayer.*fraud', 'relayer.*undisputable'],
    'bridge-freeze-halt': ['bridge.*freeze', 'large.*validator.*set.*bridge', 'bridge.*halt'],
    'bridge-observer-exploit': ['observer.*manipulat', 'observer.*remov.*ballot', 'observer.*halt', 'malicious.*observer'],
    'bridge-denom-handling': ['bridge.*denom', 'erc20.*denom.*bridge', 'freeze.*bridge.*erc20'],
    'bridge-message-validation': ['bridge.*message.*valid', 'bridge.*msg.*check', 'cross.*chain.*message.*valid'],

    # GOVERNANCE
    'governance-voting-power-manipulation': ['voting.*power.*manipul', 'inflat.*voting.*power', 'flash.*vote', 'flashloan.*vote', 'vote.*power.*incorrect'],
    'governance-proposal-exploit': ['proposal.*exploit', 'proposal.*dos', 'malicious.*proposal', 'proposal.*halt.*chain'],
    'governance-quorum-manipulation': ['quorum.*manipul', 'quorum.*lower', 'delegat.*lower.*quorum'],
    'governance-voting-lock': ['vote.*lock.*period', 'voting.*lock', 'vote.*after.*lock.*expir'],
    'governance-ballot-spam': ['ballot.*spam', 'ballot.*creat.*spam', 'limited.*voting.*option'],
    'governance-bribe-manipulation': ['bribe.*reward.*manipul', 'bribe.*manipulat', 'voting.*bribe.*hijack'],
    'governance-offboard-exploit': ['offboard.*exploit', 'offboard.*term', 're-onboard.*term', 'offboard.*bypass'],
    'governance-voting-zero-weight': ['vote.*zero.*weight', 'fully.*slashed.*vote', 'vote.*without.*vote'],
    'governance-parameter-change': ['param.*change.*attack', 'governance.*param.*change', 'malicious.*param'],
    'governance-timelock-bypass': ['timelock.*bypass', 'governance.*timelock', 'bypass.*delay'],

    # CONSENSUS
    'consensus-proposer-dos': ['proposer.*dos', 'block.*proposer.*dos', 'malicious.*proposer', 'proposer.*ddos'],
    'consensus-finality-bypass': ['finality.*bypass', 'forced.*finalization', 'premature.*finality', 'finalization.*bypass'],
    'consensus-reorg': ['reorg.*attack', 'bitcoin.*reorg', 'chain.*reorg', 'consensus.*reorg'],
    'consensus-vote-extension': ['vote.*extension.*vulner', 'inject.*vote.*extension', 'vote.*extension.*validat'],
    'consensus-block-sync': ['block.*sync.*vulner', 'blocksync.*panic', 'syncing.*node'],
    'consensus-non-determinism': ['non.*determinism', 'non-deterministic', 'determinism.*issue'],
    'consensus-proposer-selection': ['proposer.*selection', 'proposer.*algorithm', 'highest.*voting.*power.*update'],
    'consensus-equivocation': ['equivocat', 'double.*sign', 'double.*vote', 'equivocation.*evidence'],
    'consensus-liveness': ['liveness.*attack', 'liveness.*fail', 'consensus.*liveness'],

    # ACCESS CONTROL
    'access-missing-control': ['missing.*access.*control', 'no.*access.*control', 'lack.*access.*control', 'anyone.*can.*call'],
    'access-role-assignment': ['role.*assign.*error', 'missing.*grant.*role', 'role.*not.*grant', 'governance.*role.*missing'],
    'access-antehandler-bypass': ['antehandler.*bypass', 'antehandler.*skip', 'non.*checktx.*antehandler'],
    'access-allowlist-bypass': ['allowlist.*bypass', 'whitelist.*bypass', 'allow.*list.*anyone'],
    'access-cosmwasm-bypass': ['cosmwasm.*auth.*bypass', 'cosmwasm.*contract.*bypass', 'malicious.*cosmwasm'],
    'access-amino-signing': ['amino.*sign.*mismatch', 'legacy.*amino.*sign', 'amino.*bypass'],
    'access-predecessor-misuse': ['predecessor.*id.*misuse', 'signer.*id.*instead', 'account.*id.*misuse'],
    'access-owner-privilege': ['owner.*abus', 'admin.*drain', 'owner.*can.*drain', 'owner.*privilege', 'centralizat.*risk'],
    'access-msg-sender-validation': ['msg.*sender.*valid', 'sender.*not.*check', 'sender.*valid.*miss'],
    'access-module-authority': ['module.*authority', 'authority.*check', 'keeper.*authority'],

    # TIMING / EPOCH  
    'timing-epoch-transition': ['epoch.*transition.*exploit', 'epoch.*boundary.*exploit', 'epoch.*change.*exploit'],
    'timing-epoch-snapshot': ['epoch.*snapshot.*manipul', 'snapshot.*timing', 'cache.*manipulat.*epoch', 'epoch.*cache'],
    'timing-cooldown-bypass': ['cooldown.*bypass', 'lockup.*bypass', 'lock.*period.*bypass', 'bypass.*lock.*period'],
    'timing-timestamp-boundary': ['timestamp.*boundary', 'off.*by.*one.*time', 'expired.*include.*current.*block'],
    'timing-unbonding-change': ['unbonding.*time.*change', 'unbonding.*period.*change', 'change.*unbonding'],
    'timing-epoch-duration-break': ['epoch.*duration.*change', 'epoch.*duration.*break', 'change.*epoch.*break'],
    'timing-expiration-bypass': ['expiration.*bypass', 'expired.*still.*active', 'expiration.*check.*miss'],
    'timing-block-time': ['block.*time.*exploit', 'block.*time.*drift', 'block.*timestamp.*manipul'],
    'timing-race-condition': ['race.*condition', 'time.*of.*check', 'toctou'],

    # VALIDATION
    'validation-zero-check-missing': ['missing.*zero.*check', 'zero.*amount.*miss', 'zero.*address.*miss', 'no.*zero.*valid'],
    'validation-bounds-missing': ['missing.*bounds.*check', 'no.*upper.*limit', 'no.*lower.*limit', 'unbounded.*parameter'],
    'validation-state-check-missing': ['missing.*state.*check', 'no.*state.*valid', 'skip.*state.*verif'],
    'validation-percentage-overflow': ['percentage.*overflow', 'percentage.*higher.*100', 'percentage.*exceed'],
    'validation-address-normalization': ['address.*normalizat', 'canonical.*address', 'address.*lowercase'],
    'validation-duplicate-missing': ['duplicate.*valid.*miss', 'duplicate.*entry', 'no.*duplicate.*check', 'duplicate.*signature'],
    'validation-config-bypass': ['config.*valid.*bypass', 'setparams.*bypass', 'param.*safety.*bypass'],
    'validation-input-general': ['missing.*input.*valid', 'insufficient.*input.*valid', 'improper.*input.*valid'],
    'validation-incorrect-check': ['incorrect.*check', 'wrong.*check', 'check.*incorrect'],
    'validation-logic-error': ['logic.*error', 'logic.*bug', 'inverted.*condition', 'wrong.*condition'],
    'validation-msg-missing': ['missing.*msg.*valid', 'validatebasic.*miss', 'validatebasic.*not.*call'],
    'validation-length-check': ['length.*check.*miss', 'no.*length.*valid', 'size.*not.*check'],

    # TOKEN
    'token-fee-on-transfer': ['fee.*on.*transfer', 'deflationary.*token.*error', 'fee.*transfer.*not.*support'],
    'token-rebasing': ['rebas.*token.*error', 'negative.*rebase', 'rebase.*accounting', 'steth.*rebase'],
    'token-approval-error': ['token.*approv.*error', 'approv.*not.*set', 'allowance.*error'],
    'token-unlimited-mint': ['unlimited.*mint', 'uncontrolled.*mint', 'mint.*without.*limit'],
    'token-burn-error': ['burn.*error', 'burn.*share.*leave.*token', 'burn.*not.*remove', 'lp.*burn.*error'],
    'token-transfer-hook': ['transfer.*hook.*error', 'on.*transfer.*hook', 'before.*send.*hook'],
    'token-nft-handling': ['nft.*lost', 'nft.*stuck', 'nft.*exploit', 'erc721.*error', 'nft.*ownership'],
    'token-decimal-handling': ['token.*decimal.*error', 'decimal.*differ.*handle', 'multi.*token.*decimal'],
    'token-zrc20-bypass': ['zrc20.*bypass', 'zrc20.*pause.*bypass', 'zrc20.*token'],
    'token-supply-tracking': ['token.*supply.*track', 'supply.*mismatch', 'total.*supply.*incorrect'],
    'token-denom-handling': ['denom.*handling', 'coin.*denom', 'denom.*valid', 'invalid.*denom'],

    # VAULT / SHARE
    'vault-share-inflation': ['share.*inflation.*attack', 'vault.*inflation', 'first.*depositor'],
    'vault-share-calculation': ['share.*calculat.*error', 'incorrect.*share.*calculat', 'wrong.*share'],
    'vault-deposit-theft': ['vault.*deposit.*theft', 'front.*deposit.*vault', 'deposit.*steal.*vault'],
    'vault-withdrawal-error': ['vault.*withdrawal.*error', 'vault.*redeem.*error', 'vault.*withdraw.*revert'],
    'vault-tvl-manipulation': ['vault.*tvl.*manipul', 'total.*asset.*manipul'],
    'vault-strategy-loss': ['vault.*strategy.*loss', 'strategy.*incur.*loss', 'active.*pool.*stop'],
    'vault-griefing': ['vault.*grief', 'vault.*dos', 'vault.*brick', 'vault.*lock.*deposit'],
    'vault-insolvency': ['vault.*insolven', 'vault.*insufficient', 'vault.*underfund'],
    'vault-curator-exploit': ['curator.*exploit', 'curator.*bypass', 'curator.*manipul'],

    # ORACLE / PRICE
    'oracle-stale-price': ['stale.*price', 'oracle.*stale', 'outdated.*price'],
    'oracle-price-manipulation': ['price.*manipulat.*oracle', 'oracle.*price.*manipulat', 'twap.*manipul'],
    'oracle-dos': ['oracle.*dos', 'oracle.*block', 'oracle.*spam'],
    'oracle-deviation-exploit': ['price.*deviat', 'lst.*deviat', 'depeg.*exploit', 'swap.*price.*deviat'],
    'oracle-frontrunning': ['oracle.*frontrun', 'price.*update.*frontrun', 'lst.*price.*frontrun'],
    'oracle-missing-stake': ['oracle.*stake.*requir', 'minimum.*oracle.*stake'],
    'oracle-chainlink-specific': ['chainlink.*price.*discrepanc', 'chainlink.*arbitrag'],
    'oracle-wrong-price-usage': ['wrong.*price', 'incorrect.*price.*feed', 'price.*feed.*error'],

    # LIQUIDATION / AUCTION
    'liquidation-threshold-error': ['liquidat.*threshold.*error', 'health.*factor.*incorrect', 'liquidatable.*wrong'],
    'liquidation-frontrunning': ['liquidat.*frontrun', 'frontrun.*liquidat'],
    'liquidation-cascade': ['liquidat.*cascade', 'cascading.*liquidat'],
    'auction-manipulation': ['auction.*manipul', 'auction.*grief', 'auction.*dos', 'bid.*manipulat'],
    'auction-cdp-dust': ['cdp.*dust', 'dust.*position.*cdp', 'tiny.*cdp', 'dust.*cdp'],
    'debt-accounting-error': ['debt.*account.*error', 'debt.*calculat.*incorrect', 'debt.*ceiling'],
    'collateral-ratio-bypass': ['collateral.*ratio.*bypass', 'collateral.*check.*wrong'],
    'lien-exploit': ['lien.*exploit', 'lien.*buyout', 'lien.*position.*delet', 'lien.*stack'],
    'liquidation-bot-dos': ['liquidation.*bot.*dos', 'liquidator.*dos', 'liquidator.*grief'],
    'liquidation-accounting': ['liquidation.*account', 'liquidation.*debt.*account', 'liquidation.*deficit'],

    # LIFECYCLE
    'lifecycle-upgrade-error': ['upgrade.*procedure.*error', 'improper.*upgrade', 'cosmos.*sdk.*upgrade'],
    'lifecycle-migration-failure': ['migration.*data.*loss', 'migration.*failure', 'loadversion.*failure', 'migration.*gas'],
    'lifecycle-init-error': ['initializ.*error', 'double.*init', 'missing.*init'],
    'lifecycle-storage-gap': ['storage.*gap', 'storage.*collision', 'proxy.*storage'],
    'lifecycle-module-registration': ['module.*registrat.*miss', 'message.*type.*registrat', 'amino.*registrat'],
    'lifecycle-genesis-error': ['genesis.*error', 'zero.*height.*genesis', 'genesis.*prepar'],
    'lifecycle-deployment-param': ['deployment.*parameter.*error', 'incorrect.*deploy.*param', 'wrong.*config.*deploy'],
    'lifecycle-state-export': ['state.*export.*error', 'export.*genesis', 'genesis.*export'],
    'lifecycle-version-compat': ['version.*compat', 'incompatible.*version', 'sdk.*version.*mismatch'],

    # SIGNATURE
    'signature-verification-missing': ['missing.*signature.*verif', 'signature.*not.*valid', 'signature.*verif.*miss'],
    'signature-replay': ['signature.*replay', 'cross.*contract.*replay', 'replay.*inflat.*reward'],
    'signature-cross-chain-replay': ['cross.*chain.*replay', 'hard.*fork.*replay', 'chain.*id.*replay'],
    'signature-forgery': ['signature.*forgery', 'forge.*signature', 'tricking.*node.*sign'],
    'signature-duplicate': ['duplicate.*signature', 'duplicate.*validator.*sig'],
    'signature-eip155-missing': ['eip.*155.*miss', 'chain.*id.*valid.*miss'],
    'signature-key-management': ['key.*management.*error', 'private.*key.*arg', 'keyring.*password'],
    'signature-malleability': ['signature.*malleab', 'malleable.*sign', 'low.*s.*check'],

    # REENTRANCY
    'reentrancy-classic': ['classic.*reentrancy', 'reentrancy.*steal', 'safemint.*reentrancy'],
    'reentrancy-cross-contract': ['cross.*contract.*reentrancy', 'cross.*function.*reentrancy'],
    'reentrancy-callback': ['callback.*reentrancy', 'hook.*reentrancy', 'reentrancy.*callback'],
    'reentrancy-read-only': ['read.*only.*reentrancy', 'view.*function.*reentrancy'],

    # MEV / FRONTRUNNING
    'mev-staking-frontrun': ['staking.*frontrun', 'frontrun.*stake.*deposit'],
    'mev-price-update': ['price.*update.*frontrun', 'oracle.*update.*frontrun'],
    'mev-slippage-exploit': ['slippage.*exploit', 'no.*slippage.*protect', 'zero.*slippage', 'missing.*slippage'],
    'mev-sandwich': ['sandwich.*attack', 'sandwich.*staking', 'sandwich.*deposit'],
    'mev-block-stuffing': ['block.*stuff', 'block.*fill.*auction'],
    'mev-arbitrage': ['arbitrag.*exploit', 'rate.*arbitrag', 'stake.*arbitrag', 'price.*discrepanc.*arbitrag'],
    'mev-priority': ['priorit.*manipulat', 'oracle.*message.*priorit', 'gas.*price.*manipul'],
    'mev-jit-liquidity': ['jit.*liquidity', 'just.*in.*time', 'jit.*deposit'],

    # MINIPOOL / NODE OPERATOR
    'minipool-deposit-theft': ['minipool.*deposit.*theft', 'minipool.*hijack', 'hijack.*minipool'],
    'minipool-cancel-error': ['minipool.*cancel.*error', 'cancel.*moratorium', 'minipool.*cancel.*period'],
    'minipool-slash-avoidance': ['minipool.*slash.*avoid', 'node.*operator.*slash.*avoid'],
    'minipool-finalization': ['minipool.*finaliz', 'forced.*finaliz.*minipool', 'minipool.*refund'],
    'minipool-replay': ['minipool.*replay', 'create2.*destroy.*replay'],
    'operator-registration-frontrun': ['operator.*register.*frontrun', 'endpoint.*register.*frontrun'],
    'operator-reward-leak': ['operator.*reward.*leak', 'node.*operator.*reward.*leak'],
    'operator-key-fundable': ['operator.*fundable.*key', 'fundable.*key.*true', 'operator.*has.*fundable'],
    'operator-deregistration': ['operator.*deregist', 'deregist.*operator', 'operator.*exit', 'force.*deregist'],

    # BTC STAKING
    'btc-staking-tx-validation': ['btc.*staking.*tx.*valid', 'coinbase.*transaction.*slash', 'btc.*tx.*valid'],
    'btc-unbonding-handling': ['btc.*unbonding.*handl', 'spending.*unbonding', 'unbonding.*transaction.*spend'],
    'btc-delegation-finality': ['btc.*delegation.*finality', 'babylon.*delegation', 'finality.*provider'],
    'btc-change-output': ['btc.*change.*output', 'unspent.*btc.*change', 'change.*output.*validation'],
    'btc-slashable-stake': ['btc.*slashable', 'unslashable.*btc', 'slashable.*staking.*script'],
    'btc-covenant-signature': ['covenant.*signature.*expired', 'covenant.*expired.*event'],
    'btc-staking-indexer': ['staking.*indexer', 'btc.*indexer.*error', 'indexer.*not.*handle'],
    'btc-timestamp-verification': ['btc.*timestamp', 'bitcoin.*header.*timestamp', 'btc.*block.*time'],

    # MISC INFRASTRUCTURE
    'infra-ssrf': ['ssrf.*attack', 'server.*side.*request'],
    'infra-private-key': ['private.*key.*expos', 'private.*key.*command', 'key.*argument.*command'],
    'infra-tss': ['tss.*manager.*single.*point', 'tss.*node.*frontrun', 'tss.*vulnerab'],
    'infra-keyring': ['keyring.*insecur', 'keyring.*password.*insecur', 'unencrypted.*url.*scheme'],
    'infra-error-handling': ['error.*handl.*miss', 'unhandled.*error', 'silent.*error'],
    'infra-deprecated-usage': ['deprecated.*usage', 'deprecated.*getsigners', 'deprecated.*function'],
    'infra-logging-info-leak': ['log.*sensitive', 'leak.*info.*log', 'information.*leak'],
    'infra-config-exposure': ['config.*expos', 'secret.*expos', 'credential.*expos'],
    'infra-api-abuse': ['api.*abuse', 'rpc.*abuse', 'endpoint.*abuse'],

    # LIQUIDITY / AMM specific to cosmos
    'liquidity-pool-manipulation': ['pool.*manipulat', 'lp.*manipulat', 'amm.*manipulat'],
    'liquidity-imbalance': ['pool.*imbalanc', 'liquidity.*imbalanc', 'skew.*pool'],
    'liquidity-removal-dos': ['remove.*liquidity.*dos', 'liquidity.*remov.*revert'],
    'liquidity-fee-error': ['swap.*fee.*error', 'fee.*tier.*error', 'pool.*fee.*incorrect'],
    'liquidity-concentrated': ['concentrated.*liquidity', 'tick.*error', 'range.*error'],

    # STATE MANAGEMENT cosmos-specific
    'state-store-error': ['store.*error', 'kv.*store', 'iavl.*error', 'state.*store'],
    'state-iterator-error': ['iterator.*error', 'store.*iterator', 'iterator.*close'],
    'state-pruning-error': ['state.*prun.*error', 'pruning.*data.*loss', 'prune.*incorrect'],
    'state-snapshot-error': ['snapshot.*error', 'state.*snapshot', 'snapshot.*corrupt'],
    'state-migration-error': ['state.*migrat.*error', 'store.*migrat', 'data.*migrat'],

    # MODULE-SPECIFIC COSMOS
    'module-bank-error': ['bank.*module.*error', 'bank.*send.*error', 'bank.*keeper'],
    'module-auth-error': ['auth.*module.*error', 'auth.*keeper.*error', 'account.*module'],
    'module-distribution': ['distribution.*module', 'community.*pool', 'fee.*distribution'],
    'module-staking-specific': ['staking.*module.*error', 'staking.*keeper', 'bonded.*pool'],
    'module-slashing-specific': ['slashing.*module', 'slashing.*keeper', 'signing.*info'],
    'module-evidence': ['evidence.*module', 'evidence.*handler', 'evidence.*submit'],
    'module-crisis': ['crisis.*module', 'invariant.*check', 'invariant.*route'],
    'module-capability': ['capability.*module', 'capability.*claim', 'capability.*owner'],

    # HOOKS & CALLBACKS
    'hooks-before-after': ['beforeslash.*hook', 'afterdelegate.*hook', 'hook.*not.*call', 'missing.*hook'],
    'hooks-order-dependency': ['hook.*order.*depend', 'callback.*order', 'hook.*execut.*order'],
    'hooks-revert-propagation': ['hook.*revert.*propagat', 'callback.*revert.*not.*caught', 'hook.*error.*swallow'],
    'hooks-reentrancy-via-hook': ['hook.*reentrancy', 'callback.*reentr', 'before.*send.*reenter'],

    # ABCI LIFECYCLE
    'abci-beginblock-error': ['beginblock.*error', 'beginblocker.*panic', 'beginblock.*logic'],
    'abci-endblock-error': ['endblock.*error', 'endblocker.*panic', 'endblock.*logic'],
    'abci-checktx-bypass': ['checktx.*bypass', 'checktx.*not.*enforc', 'delivertx.*skip.*check'],
    'abci-prepare-process': ['prepareproposal.*error', 'processproposal.*error', 'prepare.*process.*mismatch'],
    'abci-vote-extension-abuse': ['voteextension.*abuse', 'vote.*extension.*inject', 'abci.*vote.*extension'],
    'abci-finalize-block': ['finalizeblock.*error', 'finalize.*block.*return', 'finalize.*block.*state'],
}

# Multi-classify
pattern_groups = defaultdict(list)
report_matched = defaultdict(list)  # report -> list of patterns

for report in all_reports:
    for pattern_name, keywords in patterns_flat.items():
        for kw in keywords:
            if re.search(kw, report['combined']):
                pattern_groups[pattern_name].append(report)
                report_matched[report['file']].append(pattern_name)
                break

unmatched = [r for r in all_reports if r['file'] not in report_matched]

# Summary
active_patterns = {p: r for p, r in pattern_groups.items() if r}
print(f"Parsed {len(all_reports)} reports")
print(f"Active patterns (with reports): {len(active_patterns)}")
print(f"Total report-pattern assignments: {sum(len(v) for v in pattern_groups.values())}")
print(f"Matched reports: {len(report_matched)}/{len(all_reports)}")
print(f"Unmatched reports: {len(unmatched)}")
print(f"\nPattern distribution:")
for p in sorted(active_patterns.keys(), key=lambda x: -len(active_patterns[x])):
    print(f"  {p}: {len(active_patterns[p])}")

# Save classification for use by generator
import json
output = {
    'summary': {
        'total_reports': len(all_reports),
        'active_patterns': len(active_patterns),
        'total_assignments': sum(len(v) for v in pattern_groups.values()),
        'matched_reports': len(report_matched),
        'unmatched_reports': len(unmatched),
    },
    'pattern_counts': {p: len(r) for p, r in sorted(active_patterns.items(), key=lambda x: -len(x[1]))},
    'unmatched_files': [r['file'] for r in unmatched],
}
with open('/tmp/classification_results.json', 'w') as f:
    json.dump(output, f, indent=2)
print(f"\nSaved to /tmp/classification_results.json")
