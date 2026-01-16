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
solodit_id: 58650
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/857
source_link: none
github_link: https://github.com/sherlock-audit/2025-04-zetachain-cross-chain-judging/issues/275

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Laksmana
---

## Vulnerability Title

M-15: The withdraw method in the Solana node doesn't increment the nonce when the withdrawal transaction fails

### Overview


The bug report is about a missing "increment nonce" instruction in the "withdraw" method of the Zetachain cross-chain judging system. This can cause the nonce to get stuck when the withdrawal transaction fails. The root cause of this issue is that the "prepareWithdrawTx" and "prepareWithdrawSPLTx" functions in the "signer.go" file do not include the necessary instruction. As a result, the nonce in the Solana program remains unchanged when a withdrawal transaction fails. This can have a negative impact as it prevents the nonce from being updated. To mitigate this issue, it is recommended to ensure that the "withdraw" method on the node includes an "increment nonce" instruction.

### Original Finding Content


Source: https://github.com/sherlock-audit/2025-04-zetachain-cross-chain-judging/issues/275 

## Found by 
Laksmana

### Summary

The missing `increment nonce` in the `withdraw` method can cause the nonce to get stuck when the `withdraw` transaction fails.

### Root Cause

In the [signer.go](https://github.com/sherlock-audit/2025-04-zetachain-cross-chain/blob/main/node/zetaclient/chains/solana/signer/signer.go#L341) file, both the `prepareWithdrawTx` and `prepareWithdrawSPLTx` functions do not include a `nonce increment` instruction.
```go
func (signer *Signer) prepareWithdrawTx(
	ctx context.Context,
	cctx *types.CrossChainTx,
	height uint64,
	logger zerolog.Logger,
) (outboundGetter, error) {
	params := cctx.GetCurrentOutboundParam()
	// compliance check
	cancelTx := compliance.IsCCTXRestricted(cctx)
	if cancelTx {
		compliance.PrintComplianceLog(
			logger,
			signer.Logger().Compliance,
			true,
			signer.Chain().ChainId,
			cctx.Index,
			cctx.InboundParams.Sender,
			params.Receiver,
			"SOL",
		)
	}

	// sign gateway withdraw message by TSS
	msg, err := signer.createAndSignMsgWithdraw(ctx, params, height, cancelTx)
	if err != nil {
		return nil, errors.Wrap(err, "createAndSignMsgWithdraw error")
	}

	return func() (*Outbound, error) {
		// sign the withdraw transaction by relayer key
		inst, err := signer.createWithdrawInstruction(*msg)
		if err != nil {
			return nil, errors.Wrap(err, "error creating withdraw instruction")
		}

		tx, err := signer.signTx(ctx, inst, 0)
		if err != nil {
			return nil, errors.Wrap(err, "error signing withdraw instruction")
		}
		return &Outbound{Tx: tx}, nil
	}, nil
}

func (signer *Signer) prepareWithdrawSPLTx(
	ctx context.Context,
	cctx *types.CrossChainTx,
	height uint64,
	logger zerolog.Logger,
) (outboundGetter, error) {
	params := cctx.GetCurrentOutboundParam()
	// compliance check
	cancelTx := compliance.IsCCTXRestricted(cctx)
	if cancelTx {
		compliance.PrintComplianceLog(
			logger,
			signer.Logger().Compliance,
			true,
			signer.Chain().ChainId,
			cctx.Index,
			cctx.InboundParams.Sender,
			params.Receiver,
			"SPL",
		)
	}

	// get mint details to get decimals
	mint, err := signer.decodeMintAccountDetails(ctx, cctx.InboundParams.Asset)
	if err != nil {
		return nil, errors.Wrap(err, "decodeMintAccountDetails error")
	}

	// sign gateway withdraw spl message by TSS
	msg, err := signer.createAndSignMsgWithdrawSPL(
		ctx,
		params,
		height,
		cctx.InboundParams.Asset,
		mint.Decimals,
		cancelTx,
	)
	if err != nil {
		return nil, errors.Wrap(err, "createAndSignMsgWithdrawSPL error")
	}

	return func() (*Outbound, error) {
		// sign the withdraw transaction by relayer key
		inst, err := signer.createWithdrawSPLInstruction(*msg)
		if err != nil {
			return nil, errors.Wrap(err, "error creating withdraw SPL instruction")
		}

		tx, err := signer.signTx(ctx, inst, 0)
		if err != nil {
			return nil, errors.Wrap(err, "error signing withdraw SPL instruction")
		}

		return &Outbound{Tx: tx}, nil
	}, nil
}

```

As a result, when a withdrawal transaction fails, the nonce in the Solana program remains unchanged.



### Internal Pre-conditions

- 

### External Pre-conditions

The withdraw method transaction on Solana failed.

### Attack Path

- 

### Impact

When a withdrawal transaction on Solana fails, the nonce will remain unchanged.

### PoC

- 

### Mitigation

Ensure `withdraw` method on node include a `increment nonce`



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | ZetaChain Cross-Chain |
| Report Date | N/A |
| Finders | Laksmana |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-04-zetachain-cross-chain-judging/issues/275
- **Contest**: https://app.sherlock.xyz/audits/contests/857

### Keywords for Search

`vulnerability`

