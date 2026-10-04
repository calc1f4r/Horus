---
# Core Classification
protocol: Cosmos SDK V3
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47198
audit_firm: OtterSec
contest_link: https://cosmos.network/
source_link: https://cosmos.network/
github_link: https://github.com/cosmos/cosmos-sdk

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
finders_count: 3
finders:
  - James Wang
  - DRA
  - Super Fashi
---

## Vulnerability Title

Potential To Rotate Consensus Key Back To Initial Key

### Overview


This bug report discusses a vulnerability in the code related to rotating the consensus public key for validators. The issue arises from the omission of the initial consensus key from the NewToOldConsKeyMap, which tracks historical rotations of the key. This allows for the possibility of rotating back to the validator's very first key, which defeats the purpose of key rotation for security purposes. Additionally, the code does not validate if the new key conforms to the allowed key types defined by the network's consensus parameters, which may cause issues with the protocol. The suggested fix is to either include the initial key in the NewToOldConsKeyMap or maintain a separate mechanism to track it, and to add a validation step to ensure the new key type matches one of the allowed types. This issue has been resolved in two pull requests.

### Original Finding Content

## Vulnerability Description

The vulnerability arises from the omission of the initial consensus key from the `NewToOldConsKeyMap` in `msg_server::RotateConsPubKey`. `NewToOldConsKeyMap` is utilized to track historical rotations of the consensus public key (`ConsensusPubKey`) for validators. Before rotating to a new public key (`NewPubkey`), the function checks if this new key is already present in `NewToOldConsKeyMap`. If the `NewToOldConsKeyMap` does not include the initial (first) consensus key of a validator, it allows the possibility of rotating back to the validator’s very first consensus key.

```go
func (k msgServer) RotateConsPubKey(ctx context.Context, msg *types.MsgRotateConsPubKey) (res *types.MsgRotateConsPubKeyResponse, err error) {
	// check cons key is already present in the key rotation history.
	rotatedTo, err := k.NewToOldConsKeyMap.Get(ctx, pk.Address())
	if err != nil && !errors.Is(err, collections.ErrNotFound) {
		return nil, err
	}
	if rotatedTo != nil {
		return nil, errorsmod.Wrap(sdkerrors.ErrInvalidAddress, "the new public key is already present in rotation history, please try with a different one")
	}
}
```

Consensus key rotation is designed to enhance security by periodically changing keys. Allowing rotation back to the initial key defeats this purpose, as compromised keys may be utilized again. Additionally, `RotateConsPubKey` does not validate whether the new consensus key conforms to the allowed key types defined by the network’s consensus parameters. Validators may end up with consensus keys of different types, which may not be supported by the protocol.

## Remediation

Update `RotateConsPubKey` to include the initial consensus key in the `NewToOldConsKeyMap` or maintain a separate mechanism to track the initial key separately. Additionally, include a validation step to ensure that the new consensus key type matches one of the allowed key types specified in the consensus parameters.

---

© 2024 Otter Audits LLC. All Rights Reserved. 8/22  
**DRAFT**  
**Cosmos SDK Audit 04 — Vulnerabilities**  
**Patch**  
Resolved in PR #20713 and PR #20714.  
© 2024 Otter Audits LLC. All Rights Reserved. 9/22  
**DRAFT**

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Cosmos SDK V3 |
| Report Date | N/A |
| Finders | James Wang, DRA, Super Fashi |

### Source Links

- **Source**: https://cosmos.network/
- **GitHub**: https://github.com/cosmos/cosmos-sdk
- **Contest**: https://cosmos.network/

### Keywords for Search

`vulnerability`

