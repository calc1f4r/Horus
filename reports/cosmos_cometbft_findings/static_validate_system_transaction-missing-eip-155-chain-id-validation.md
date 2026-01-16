---
# Core Classification
protocol: Monad
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62896
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Monad-Spearbit-Security-Review-September-2025.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Monad-Spearbit-Security-Review-September-2025.pdf
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
finders_count: 4
finders:
  - Haxatron
  - Dtheo
  - Guido Vranken
  - Rikard Hjort
---

## Vulnerability Title

static_validate_system_transaction missing EIP-155 chain ID validation

### Overview


This report is about a high-risk security vulnerability found in the function `static_validate_system_transaction`. This function is missing chain ID validation, which can allow a malicious block proposer to include an invalid system transaction. This can lead to failed epoch/snapshot changes and break validator set accounting. The recommendation is to validate in monad-bft that the staking syscall has the correct chain ID. This issue has been fixed in commit `aa71c71e`.

### Original Finding Content

## Security Vulnerability Report

## Severity
**High Risk**

## Context
(No context files were provided by the reviewer)

## Description
The function `static_validate_system_transaction` is missing chain ID validation. The only validation for `static_validate_system_transaction` is present in the following code block:

```rust
fn static_validate_system_transaction(
    txn: &Recovered<TxEnvelope>,
) -> Result<(), SystemTransactionError> {
    if !Self::is_system_sender(txn.signer()) {
        return Err(SystemTransactionError::UnexpectedSenderAddress);
    }
    if !txn.tx().is_legacy() {
        return Err(SystemTransactionError::InvalidTxType);
    }
    if txn.tx().gas_price() != Some(0) {
        return Err(SystemTransactionError::NonZeroGasPrice);
    }
    if txn.tx().gas_limit() != 0 {
        return Err(SystemTransactionError::NonZeroGasLimit);
    }
    if !matches!(txn.tx().kind(), TxKind::Call(_)) {
        return Err(SystemTransactionError::InvalidTxKind);
    }
    Ok(())
}
```

This missing validation can allow a malicious block proposer to include an invalid system transaction, which will fail during transaction validation in the execution layer. This can lead to failed epoch/snapshot changes, breaking validator set accounting.

Additional code references include:

### Execute System Transaction
```cpp
Result<Receipt> ExecuteSystemTransaction<rev>::operator()()
{
    // ...
    {
        Transaction tx = tx_;
        tx.gas_limit = 2/quotesingle.ts1000/quotesingle.ts1000; // required to pass intrinsic gas validation check
        BOOST_OUTCOME_TRY(static_validate_transaction<rev>(
            tx,
            std::nullopt /* 0 base fee to pass validation */,
            std::nullopt /* 0 blob fee to pass validation */,
            chain_.get_chain_id(),
            chain_.get_max_code_size(header_.number, header_.timestamp)));
    }
}
```

### Validate Transaction
```cpp
// EIP-155
if (MONAD_LIKELY(tx.sc.chain_id.has_value())) {
    if constexpr (rev < EVMC_SPURIOUS_DRAGON) {
        return TransactionError::TypeNotSupported;
    }
    if (MONAD_UNLIKELY(tx.sc.chain_id.value() != chain_id)) {
        return TransactionError::WrongChainId;
    }
}
```

## Recommendation
Validate in monad-bft that the staking syscall has the correct chain ID.

## Category Labs
Fixed in commit `aa71c71e`.

## Spearbit
Fix verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Monad |
| Report Date | N/A |
| Finders | Haxatron, Dtheo, Guido Vranken, Rikard Hjort |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Monad-Spearbit-Security-Review-September-2025.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Monad-Spearbit-Security-Review-September-2025.pdf

### Keywords for Search

`vulnerability`

