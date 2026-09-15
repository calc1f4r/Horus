---
# Core Classification
protocol: Allora
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36709
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/454
source_link: none
github_link: https://github.com/sherlock-audit/2024-06-allora-judging/issues/2

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
  - defsec
---

## Vulnerability Title

M-1: Lack of Authentication in OnRecvPacket

### Overview


The report highlights a lack of authentication in the OnRecvPacket function of the Allora chain's IBC middleware. This means that incoming packets are not being properly verified based on the channel ID, which can lead to security vulnerabilities and unauthorized processing of packets. The report suggests modifying the function to include a check for channel ID and sender authentication. The issue has been fixed by the Allora protocol team in a recent PR.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-06-allora-judging/issues/2 

## Found by 
defsec
## Summary

The Axelar sample code acknowledges the importance of authenticating the message based on the channel ID, in addition to verifying the packet sender. However, the Allora chain's implementation does not include any channel ID/sender authentication logic.

## Vulnerability Detail

In the provided code for the Allora chain's IBC middleware (`gmp/middleware.go`), the `OnRecvPacket` function does not perform authentication based on the channel ID when processing incoming packets. This can potentially lead to security vulnerabilities and allow unauthorized or unintended processing of packets.

Comparing it with the Axelar sample code (`gmp_middleware/middleware.go`), there is a commented-out TODO section that mentions the need for channel ID authentication:

```go
// TODO: authenticate the message with channel-id
if data.Sender != AxelarGMPAcc {
    return ack
}
```

## Impact

Without verifying the channel ID, the middleware may process packets from unintended or unauthorized channels. This can result in the execution of malicious or unexpected actions on the receiving chain.

Axelar Sample : https://github.com/axelarnetwork/evm-cosmos-gmp-sample/blob/main/native-integration/sample-middleware/gmp_middleware.go#L114

## Code Snippet

[ibc_middleware.go#L112-L113](https://github.com/sherlock-audit/2024-06-allora/blob/main/allora-chain/x/ibc/gmp/ibc_middleware.go#L112-L113)

```go
// OnRecvPacket implements the IBCMiddleware interface
func (im IBCMiddleware) OnRecvPacket(
	ctx sdk.Context,
	packet channeltypes.Packet,
	relayer sdk.AccAddress,
) ibcexported.Acknowledgement {
	var data transfertypes.FungibleTokenPacketData
	if err := transfertypes.ModuleCdc.UnmarshalJSON(packet.GetData(), &data); err != nil {
		return channeltypes.NewErrorAcknowledgement(fmt.Errorf("cannot unmarshal ICS-20 transfer packet data"))
	}

	var msg Message
	var err error
	err = json.Unmarshal([]byte(data.GetMemo()), &msg)
	if err != nil || len(msg.Payload) == 0 {
		// Not a packet that should be handled by the GMP middleware
		return im.app.OnRecvPacket(ctx, packet, relayer)
	}

	//if !strings.EqualFold(data.Sender, AxelarGMPAcc) {
	//	// Not a packet that should be handled by the GMP middleware
	//	return im.app.OnRecvPacket(ctx, packet, relayer)
	//}

	logger := ctx.Logger().With("handler", "GMP")

	switch msg.Type {
	case TypeGeneralMessage:
		logger.Info("Received TypeGeneralMessage",
			"srcChain", msg.SourceChain,
			"srcAddress", msg.SourceAddress,
			"receiver", data.Receiver,
			"payload", string(msg.Payload),
			"handler", "GMP",
		)
		// let the next layer deal with this
		// the rest of the data fields should be normal
		fallthrough
	case TypeGeneralMessageWithToken:
		logger.Info("Received TypeGeneralMessageWithToken",
			"srcChain", msg.SourceChain,
			"srcAddress", msg.SourceAddress,
			"receiver", data.Receiver,
			"payload", string(msg.Payload),
			"coin", data.Denom,
			"amount", data.Amount,
			"handler", "GMP",
		)
		// we throw out the rest of the msg.Payload fields here, for better or worse
		data.Memo = string(msg.Payload)
		var dataBytes []byte
		if dataBytes, err = transfertypes.ModuleCdc.MarshalJSON(&data); err != nil {
			return channeltypes.NewErrorAcknowledgement(fmt.Errorf("cannot marshal ICS-20 post-processed transfer packet data"))
		}
		packet.Data = dataBytes
		return im.app.OnRecvPacket(ctx, packet, relayer)
	default:
		return channeltypes.NewErrorAcknowledgement(fmt.Errorf("unrecognized mesasge type: %d", msg.Type))
	}
}
```

## Tool used

Manual Review

## Recommendation

Modify the `OnRecvPacket` function to include a check that verifies the authenticity of the packet based on the channel ID/sender.




## Discussion

**sherlock-admin4**

1 comment(s) were left on this issue during the judging contest.

**0xmystery** commented:
> OnRecvPacket doesn't have authentication



**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/allora-network/allora-chain/pull/453

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Allora |
| Report Date | N/A |
| Finders | defsec |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-06-allora-judging/issues/2
- **Contest**: https://app.sherlock.xyz/audits/contests/454

### Keywords for Search

`vulnerability`

