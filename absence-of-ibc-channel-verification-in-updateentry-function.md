---
# Core Classification
protocol: Elys Modules
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51428
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/elys-network/elys-modules
source_link: https://www.halborn.com/audits/elys-network/elys-modules
github_link: none

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
  - Halborn
---

## Vulnerability Title

Absence of IBC Channel Verification in UpdateEntry Function

### Overview


The provided UpdateEntry function in a system managing entries in IBC lacks verification for the correctness and validity of Inter-Blockchain Communication (IBC) channel identifiers. This can potentially lead to unauthorized access or incorrect updates to the system. The recommended solution is for the team to consider validating IBC channels. The issue has been solved by the Elys Network team and the remediation plan can be found at the provided GitHub link.

### Original Finding Content

##### Description

In the provided **UpdateEntry** function, part of a system managing entries in IBC. The function updates an entry with various fields, including **IbcChannelId** and **IbcCounterpartyChannelId**. However, it lacks verification for the correctness and validity of these Inter-Blockchain Communication (IBC) channel identifiers.

  

```
func (k msgServer) UpdateEntry(goCtx context.Context, msg *types.MsgUpdateEntry) (*types.MsgUpdateEntryResponse, error) {
	if k.authority != msg.Authority {
		return nil, errors.Wrapf(govtypes.ErrInvalidSigner, "invalid authority; expected %s, got %s", k.authority, msg.Authority)
	}

	ctx := sdk.UnwrapSDKContext(goCtx)

	// Check if the value exists
	entry, isFound := k.GetEntry(ctx, msg.BaseDenom)
	if !isFound {
		return nil, errorsmod.Wrap(sdkerrors.ErrKeyNotFound, "entry not set")
	}

	// Checks if the the msg authority is the same as the current owner
	if msg.Authority != entry.Authority {
		return nil, errorsmod.Wrap(sdkerrors.ErrUnauthorized, "incorrect owner")
	}

	entry = types.Entry{
		Authority:                msg.Authority,
		BaseDenom:                msg.BaseDenom,
		Decimals:                 msg.Decimals,
		Denom:                    msg.Denom,
		Path:                     msg.Path,
		IbcChannelId:             msg.IbcChannelId,
		IbcCounterpartyChannelId: msg.IbcCounterpartyChannelId,
		DisplayName:              msg.DisplayName,
		DisplaySymbol:            msg.DisplaySymbol,
		Network:                  msg.Network,
		Address:                  msg.Address,
		ExternalSymbol:           msg.ExternalSymbol,
		TransferLimit:            msg.TransferLimit,
		Permissions:              msg.Permissions,
		UnitDenom:                msg.UnitDenom,
		IbcCounterpartyDenom:     msg.IbcCounterpartyDenom,
		IbcCounterpartyChainId:   msg.IbcCounterpartyChainId,
		CommitEnabled:            msg.CommitEnabled,
		WithdrawEnabled:          msg.WithdrawEnabled,
	}

	k.SetEntry(ctx, entry)

	return &types.MsgUpdateEntryResponse{}, nil
}
```

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:M/A:N/D:N/Y:N/R:N/S:C (6.3)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:M/A:N/D:N/Y:N/R:N/S:C)

##### Recommendation

Consider validating IBC channel.

  

Remediation Plan
----------------

**SOLVED:** The **Elys Network team** solved the issue.

##### Remediation Hash

<https://github.com/elys-network/elys/pull/337/commits/537ccb4b7244760b8e774ea509e8d09b124b8514>

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Elys Modules |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/elys-network/elys-modules
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/elys-network/elys-modules

### Keywords for Search

`vulnerability`

