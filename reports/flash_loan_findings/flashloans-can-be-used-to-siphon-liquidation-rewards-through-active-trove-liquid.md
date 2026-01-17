---
# Core Classification
protocol: Ethereum Reserve Dollar (ERD)
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60120
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/ethereum-reserve-dollar-erd/d2c63484-d071-4479-ab8d-d3267f272253/index.html
source_link: https://certificate.quantstamp.com/full/ethereum-reserve-dollar-erd/d2c63484-d071-4479-ab8d-d3267f272253/index.html
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
finders_count: 3
finders:
  - Ibrahim Abouzied
  - Rabib Islam
  - Hytham Farah
---

## Vulnerability Title

Flashloans Can Be Used to Siphon Liquidation Rewards Through Active Trove Liquidation Mechanism

### Overview


The bug report discusses an issue where a liquidator can exploit the system by opening a trove with a flash loan, triggering a liquidation, and then closing the trove in the same transaction. This allows them to receive a portion of the collateral rewards that should go to existing trove holders. The client believes this is normal arbitrage behavior, but the report suggests preventing users from opening and closing a trove in the same block to prevent this exploit.

### Original Finding Content

**Update**
Despite the client's response, we are nonetheless concerned that the form of transaction enabled by this issue negatively impacts trove holders.

Marked as "Acknowledged" by the client. The client provided the following explanation:

> We believe this is normal arbitrage behavior that is allowed.

**File(s) affected:**`BorrowerOperations.sol`, `TroveManagerLiquidations.sol`, `TroveManager.sol`, `CollateralManager.sol`

**Description:** A liquidator can open a trove using a flashloan to deposit a large amount of collateral, increasing the number of rewards per unit staked to which they are entitled. In the same transaction they can trigger a liquidation and receive a portion of the redistributed rewards. They can then close their trove, also within the same transaction.

This attack effectively steals a portion of the collateral rewards that should be going to existing trove holders.

Note that the effectiveness of this attack increases as the size of the liquidation increases and as the amount of the collateral in the system decreases (so that they can more easily get a larger share).

**Exploit Scenario:**

1.   Attacker notices (a) large position(s) that may be liquidated.
2.   Attacker sends a transaction performing the following steps:
    1.   Take out a flash loan in the same collateral type that is being liquidated. 
    2.   Open a trove with the minimum debt and uses as much collateral as possible (this will ensure that his share count is high).
    3.   Liquidate the trove(s) and thereby recieve the redistributed collateral rewards. 
    4.   Close the trove.

**Recommendation:** Though this attack may only be feasible in specific circumstances, it may be beneficial to prevent a user from opening and closing a trove in the same block to prevent this from happening. This can be accomplished by adding `_updateCallerBlock()` to the beginning of `openTrove()` and `_checkSameTx()` to the beginning of `closeTrove()`.

```
function _updateCallerBlock() internal {
    _lastCallerBlock = keccak256(abi.encodePacked(tx.origin, block.number));
}

function _checkSameTx() internal view {
    require(keccak256(abi.encodePacked(tx.origin, block.number)) != _lastCallerBlock, "8");
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Ethereum Reserve Dollar (ERD) |
| Report Date | N/A |
| Finders | Ibrahim Abouzied, Rabib Islam, Hytham Farah |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/ethereum-reserve-dollar-erd/d2c63484-d071-4479-ab8d-d3267f272253/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/ethereum-reserve-dollar-erd/d2c63484-d071-4479-ab8d-d3267f272253/index.html

### Keywords for Search

`vulnerability`

