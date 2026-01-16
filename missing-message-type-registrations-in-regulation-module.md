---
# Core Classification
protocol: AppChain Modules
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52143
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/emoney/appchain-modules
source_link: https://www.halborn.com/audits/emoney/appchain-modules
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
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

Missing Message Type Registrations in Regulation Module

### Overview


Bug report summary: Some message types are missing from the registration in the regulation module, which can cause issues with message handling, serialization, and deserialization. The recommendation is to update the RegisterInterfaces function to include all defined message types and ensure they are properly defined in the types package. The Emoney team has already solved the issue by registering the missing message types.

### Original Finding Content

##### Description

Several message types defined in the regulation module are not properly registered in the RegisterInterfaces function. Specifically, the following message types are missing from the registration:

**- MsgProposeBlock**

**- MsgProposeAdd**

**- MsgVote**

**- MsgProcessVoting**

The current **RegisterInterfaces** function only registers **MsgTransferAuthority**, **MsgAllowAddress**, and **MsgDisallowAddress**. This omission can lead to issues with message handling, serialization, and deserialization within the Cosmos SDK framework.

The existing implementation is as follows:

```
func RegisterInterfaces(registry types.InterfaceRegistry) {

    registry.RegisterImplementations((*sdk.Msg)(nil),

        &MsgTransferAuthority{},

        &MsgAllowAddress{},

        &MsgDisallowAddress{},

    )

    msgservice.RegisterMsgServiceDesc(registry, &_Msg_serviceDesc)

}
```

##### BVSS

[AO:A/AC:L/AX:L/C:C/I:C/A:H/D:N/Y:N/R:N/S:C (10.0)](/bvss?q=AO:A/AC:L/AX:L/C:C/I:C/A:H/D:N/Y:N/R:N/S:C)

##### Recommendation

1. Update the **RegisterInterfaces** function in the types package to include all defined message types:

```
func RegisterInterfaces(registry types.InterfaceRegistry) {

    registry.RegisterImplementations((*sdk.Msg)(nil),

        &MsgTransferAuthority{},

        &MsgAllowAddress{},

        &MsgDisallowAddress{},

        &MsgProposeBlock{},

        &MsgProposeAdd{},

        &MsgVote{},

        &MsgProcessVoting{},

    )

    msgservice.RegisterMsgServiceDesc(registry, &_Msg_serviceDesc)

}
```

2. Ensure that all these message types are properly defined in the types package with their respective structs and methods.

3. If these message types are intended to be used with the **LegacyAmino** codec as well, make sure to register them in the **RegisterLegacyAminoCodec** function:

```
func RegisterLegacyAminoCodec(cdc *codec.LegacyAmino) {

    cdc.RegisterConcrete(&MsgTransferAuthority{}, "regulation/MsgTransferAuthority", nil)

    cdc.RegisterConcrete(&MsgAllowAddress{}, "regulation/MsgAllowAddress", nil)

    cdc.RegisterConcrete(&MsgDisallowAddress{}, "regulation/MsgDisallowAddress", nil)

    cdc.RegisterConcrete(&MsgProposeBlock{}, "regulation/MsgProposeBlock", nil)

    cdc.RegisterConcrete(&MsgProposeAdd{}, "regulation/MsgProposeAdd", nil)

    cdc.RegisterConcrete(&MsgVote{}, "regulation/MsgVote", nil)

    cdc.RegisterConcrete(&MsgProcessVoting{}, "regulation/MsgProcessVoting", nil)

}
```

  
  

### Remediation Plan

**SOLVED :** The **Emoney team** solved the issue by registering message types.

##### Remediation Hash

<https://github.com/EMoney-Network/EMoneyChain/commit/9ab44f53a4e637518daef1318b0b0e76904177ed>

##### References

[EMoney-Network/EMoneyChain/x/regulation/types/codec.go#L10](https://github.com/EMoney-Network/EMoneyChain/blob/872703eaad7051654bf13265516732850afd5aac/x/regulation/types/codec.go#L10)

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | AppChain Modules |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/emoney/appchain-modules
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/emoney/appchain-modules

### Keywords for Search

`vulnerability`

