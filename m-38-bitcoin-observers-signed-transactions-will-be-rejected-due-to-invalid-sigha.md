---
# Core Classification
protocol: ZetaChain Cross-Chain
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58673
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/857
source_link: none
github_link: https://github.com/sherlock-audit/2025-04-zetachain-cross-chain-judging/issues/424

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - g
---

## Vulnerability Title

M-38: Bitcoin Observers' signed transactions will be rejected due to invalid sighashes

### Overview


This bug report is about an issue found in the Bitcoin Observers system. The problem is that the system uses incorrect information when generating the signature for each transaction. This means that when the transaction is broadcast to the Bitcoin network, it will be rejected and users will not be able to withdraw their funds. The cause of the issue is that the system uses empty values instead of the correct previous output's script and amount. No response has been received from the team and the suggested solution is to use the correct values when generating the signature. 

### Original Finding Content


Source: https://github.com/sherlock-audit/2025-04-zetachain-cross-chain-judging/issues/424 

## Found by 
g

### Summary

The Bitcoin Observers use invalid [sighashes](https://github.com/sherlock-audit/2025-04-zetachain-cross-chain/blob/main/node/zetaclient/chains/bitcoin/signer/sign.go#L211) when generating the witness hash for each transaction input. The Bitcoin network will reject all the signed transactions by the Observers.

### Root Cause

In [`SignTx()`](https://github.com/sherlock-audit/2025-04-zetachain-cross-chain/blob/main/node/zetaclient/chains/bitcoin/signer/sign.go#L211), an empty byteslice and zero amount are used when generating the sighashes.

```golang
sigHashes := txscript.NewTxSigHashes(tx, txscript.NewCannedPrevOutputFetcher([]byte{}, 0))
```

The correct input is the previous output's scriptPubKey and amount.

### Internal Pre-conditions

None

### External Pre-conditions

None

### Attack Path

1. The Observers sign the generated Bitcoin transaction with TSS.
2. When the transaction is broadcast, the Bitcoin network rejects it because it fails verification since the sighash it reconstructs using the actual previous outputs' script and amount does not match the sighash created by the Observers.

### Impact

All the withdrawal transactions in the Bitcoin network will fail. Users will be unable to withdraw from the Bitcoin network. 

### PoC

_No response_

### Mitigation

Consider generating the correct sighashes with the below pseudocode. 

```golang
prevOutFetcher := txscript.NewMultiPrevOutFetcher(nil)
for i, input := range tx.TxIn {
	prevOut := selected.UTXOs[i]  // Get the corresponding UTXO
	script, err := hex.DecodeString(prevOut.ScriptPubKey)
	if err != nil {
		return nil, err
	}
	amount := int64(prevOut.Amount * btcutil.SatoshiPerBitcoin)
	prevOutFetcher.AddPrevOut(input.PreviousOutPoint, &wire.TxOut{
		Value:    amount,
		PkScript: script,
	})
}
sigHashes := txscript.NewTxSigHashes(tx, prevOutFetcher)
sigHashes := txscript.NewTxSigHashes(tx, txscript.NewCanned
```




### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | ZetaChain Cross-Chain |
| Report Date | N/A |
| Finders | g |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-04-zetachain-cross-chain-judging/issues/424
- **Contest**: https://app.sherlock.xyz/audits/contests/857

### Keywords for Search

`vulnerability`

