---
# Core Classification
protocol: Sei EVM
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47378
audit_firm: OtterSec
contest_link: https://www.sei.io/
source_link: https://www.sei.io/
github_link: https://github.com/sei-protocol

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
finders_count: 2
finders:
  - James Wang
  - Naoya Okanami
---

## Vulnerability Title

AnteHandler Skipped In Non-CheckTx Mode

### Overview


The Cosmos AnteHandlers are used to check the validity of transactions and prevent malicious transactions from being executed. However, some of the validators are skipped when not in CheckTx mode, allowing attackers to insert malformed transactions into block proposals. This can lead to incorrect execution of transactions and open up opportunities for denial of service attacks at no cost. To fix this, AnteHandler checks should be performed in both CheckTx and DeliverTx. The issue has been fixed in PR #1474 and #1491.

### Original Finding Content

## Cosmos AnteHandlers

Cosmos AnteHandlers are used to implement basic validity checks against transactions to ensure that malformed and malicious transactions are blocked from execution. Since validators are able to insert arbitrary transactions into a block proposal, AnteHandlers must be run in `DeliverTx` to guarantee correctness.

However, several EVM AnteHandlers are skipped when not in `CheckTx` mode. Thus, if a malicious proposer inserts malformed transactions in block proposals, other validators will incorrectly execute the transaction. For example, fee checks may be bypassed in the following code:

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

Due to the design of the EVM module, errors within fee collection will be treated as an implementation error, and transaction senders will not be charged for gas spent. Combining the above, this opens up an opportunity for attackers to perform denial of service attacks on the Sei chain at zero cost.

## Remediation

Perform AnteHandler checks in both `CheckTx` and `DeliverTx`.

## Patch

Fixed in PR #1474 and PR #1491.

© 2024 Otter Audits LLC. All Rights Reserved. 10/37

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Sei EVM |
| Report Date | N/A |
| Finders | James Wang, Naoya Okanami |

### Source Links

- **Source**: https://www.sei.io/
- **GitHub**: https://github.com/sei-protocol
- **Contest**: https://www.sei.io/

### Keywords for Search

`vulnerability`

