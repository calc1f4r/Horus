---
# Core Classification
protocol: Gondi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35209
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-04-gondi
source_link: https://code4rena.com/reports/2024-04-gondi
github_link: https://github.com/code-423n4/2024-04-gondi-findings/issues/48

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

protocol_categories:
  - nft_lending

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - bin2chen
---

## Vulnerability Title

[H-07] `deployWithdrawalQueue()` need to clear `_queueAccounting[lastQueueIndex]`

### Overview


The report is about a bug in the `deployWithdrawalQueue()` function. The function clears some variables but misses one variable called `_queueAccounting[lastQueueIndex]`. This means that when another function called `queueClaimAll()` is called, it will use the old data from `_queueAccounting[lastQueueIndex]`, which can cause problems. The recommended solution is to add a line of code to clear this variable in the `deployWithdrawalQueue()` function. The bug has been confirmed and mitigated by the developers.

### Original Finding Content


In `deployWithdrawalQueue()`, only clears `_queueOutstandingValues[lastQueueIndex]` and `_outstandingValues`, but doesn't clear `_queueAccounting[lastQueueIndex]`.

```solidity
    function deployWithdrawalQueue() external nonReentrant {
...

        /// @dev We move outstanding values from the pool to the queue that was just deployed.
        _queueOutstandingValues[pendingQueueIndex] = _outstandingValues;
        /// @dev We clear values of the new pending queue.
        delete _queueOutstandingValues[lastQueueIndex];
        delete _outstandingValues;
@>      //@audit miss delete _queueAccounting[lastQueueIndex]

        _updateLoanLastIds();

@>      _pendingQueueIndex = lastQueueIndex;

        // Cannot underflow because the sum of all withdrawals is never larger than totalSupply.
        unchecked {
            totalSupply -= sharesPendingWithdrawal;
        }
    }

```

After this method, anyone calling `queueClaimAll()` will use this stale data `_queueAccounting[lastQueueIndex]`.

`queueClaimAll()` -> `_queueClaimAll(_pendingQueueIndex)`-> `_updatePendingWithdrawalWithQueue(_pendingQueueIndex)`

```solidity
    function _updatePendingWithdrawalWithQueue(
        uint256 _idx,
        uint256 _cachedPendingQueueIndex,
        uint256[] memory _pendingWithdrawal
    ) private returns (uint256[] memory) {
        uint256 totalReceived = getTotalReceived[_idx];
        uint256 totalQueues = getMaxTotalWithdrawalQueues + 1;
        /// @dev Nothing to be returned
        if (totalReceived == 0) {
            return _pendingWithdrawal;
        }
        getTotalReceived[_idx] = 0;

        /// @dev We go from idx to newer queues. Each getTotalReceived is the total
        /// returned from loans for that queue. All future queues/pool also have a piece of it.
        /// X_i: Total received for queue `i`
        /// X_1  = Received * shares_1 / totalShares_1
        /// X_2 = (Received - (X_1)) * shares_2 / totalShares_2 ...
        /// Remainder goes to the pool.
        for (uint256 i; i < totalQueues;) {
            uint256 secondIdx = (_idx + i) % totalQueues;
@>          QueueAccounting memory queueAccounting = _queueAccounting[secondIdx];
            if (queueAccounting.thisQueueFraction == 0) {
                unchecked {
                    ++i;
                }
                continue;
            }
            /// @dev We looped around.
@>          if (secondIdx == _cachedPendingQueueIndex + 1) {
                break;
            }
            uint256 pendingForQueue = totalReceived.mulDivDown(queueAccounting.thisQueueFraction, PRINCIPAL_PRECISION);
            totalReceived -= pendingForQueue;

            _pendingWithdrawal[secondIdx] = pendingForQueue;
            unchecked {
                ++i;
            }
        }
        return _pendingWithdrawal;
    }
```

### Impact

Not clearing `_queueAccounting[lastQueueIndex]` when executing `queueClaimAll()` will use this stale data to distribute `totalReceived`.

### Recommended Mitigation

```diff
    function deployWithdrawalQueue() external nonReentrant {
...

        /// @dev We move outstaning values from the pool to the queue that was just deployed.
        _queueOutstandingValues[pendingQueueIndex] = _outstandingValues;
        /// @dev We clear values of the new pending queue.
        delete _queueOutstandingValues[lastQueueIndex];
+       delete _queueAccounting[lastQueueIndex]
        delete _outstandingValues;


        _updateLoanLastIds();

        _pendingQueueIndex = lastQueueIndex;

        // Cannot underflow because the sum of all withdrawals is never larger than totalSupply.
        unchecked {
            totalSupply -= sharesPendingWithdrawal;
        }
    }
```

### Assessed type

Context

**[0xend (Gondi) confirmed](https://github.com/code-423n4/2024-04-gondi-findings/issues/48#event-12543494424)**

**[Gondi mitigated](https://github.com/code-423n4/2024-05-gondi-mitigation?tab=readme-ov-file#mitigation-of-high--medium-severity-issues):**
> Clear state vars.

**Status:** Mitigation confirmed. Full details in reports from [oakcobalt](https://github.com/code-423n4/2024-05-gondi-mitigation-findings/issues/47), [minhquanym](https://github.com/code-423n4/2024-05-gondi-mitigation-findings/issues/56) and [bin2chen](https://github.com/code-423n4/2024-05-gondi-mitigation-findings/issues/8).

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Gondi |
| Report Date | N/A |
| Finders | bin2chen |

### Source Links

- **Source**: https://code4rena.com/reports/2024-04-gondi
- **GitHub**: https://github.com/code-423n4/2024-04-gondi-findings/issues/48
- **Contest**: https://code4rena.com/reports/2024-04-gondi

### Keywords for Search

`vulnerability`

