---
# Core Classification
protocol: cosmos-sdk
chain: everychain
category: ibc
vulnerability_type: authentication_bypass

# Attack Vector Details
attack_type: cross_chain_attack
affected_component: ibc_middleware

# Technical Primitives
primitives:
  - OnRecvPacket
  - OnChanOpenInit
  - OnChanOpenAck
  - channel_version
  - packet_memo
  - acknowledgement

# Impact Classification
severity: medium_to_high
impact: unauthorized_execution
exploitability: 0.6
financial_impact: high

# Context Tags
tags:
  - cosmos_sdk
  - ibc
  - cross_chain
  - middleware
  - channel_handshake
  - packet_handling
  
language: go
version: all
---

## References
- [m-08-ibc-channel-version-negotiation-bypass-in-ibc-hooks-middleware.md](../../../reports/cosmos_cometbft_findings/m-08-ibc-channel-version-negotiation-bypass-in-ibc-hooks-middleware.md)
- [m-1-lack-of-authentication-in-onrecvpacket.md](../../../reports/cosmos_cometbft_findings/m-1-lack-of-authentication-in-onrecvpacket.md)
- [m-14-logic-bug-in-this-ibc-middleware-code-related-to-packet-handling.md](../../../reports/cosmos_cometbft_findings/m-14-logic-bug-in-this-ibc-middleware-code-related-to-packet-handling.md)
- [h-7-use-of-vulnerable-ibc-go-v840-non-deterministic-json-unmarshalling-can-cause.md](../../../reports/cosmos_cometbft_findings/h-7-use-of-vulnerable-ibc-go-v840-non-deterministic-json-unmarshalling-can-cause.md)
- [absence-of-ibc-channel-verification-in-updateentry-function.md](../../../reports/cosmos_cometbft_findings/absence-of-ibc-channel-verification-in-updateentry-function.md)

## Vulnerability Title

**IBC Middleware Authentication and Packet Handling Vulnerabilities**

### Overview

Cosmos SDK appchains implementing IBC middleware for custom packet handling (e.g., cross-chain message passing, GMP protocols, custom hooks) frequently contain authentication and packet routing vulnerabilities. Missing channel/sender verification in `OnRecvPacket`, incorrect version negotiation in channel handshakes, and flawed packet processing logic can lead to unauthorized cross-chain execution, version mismatches that break interoperability, or chain halts from malformed packets.

### Vulnerability Description

#### Root Cause

The fundamental issues arise from:
1. **Missing sender/channel authentication**: `OnRecvPacket` handlers process packets without verifying the source channel or sender address
2. **Wrong version return**: Channel handshake functions return original version instead of negotiated `finalVersion`
3. **Flawed packet routing logic**: Middleware processes unintended packets due to overly permissive memo parsing
4. **Non-deterministic deserialization**: Vulnerable IBC-Go versions have JSON unmarshalling issues causing consensus splits
5. **Missing channel ID validation**: Entry/configuration updates don't verify channel existence or validity

#### Attack Scenario

**Scenario 1: Unauthenticated Cross-Chain Execution**
1. Attacker opens IBC channel to target chain's GMP middleware
2. Attacker crafts packet with valid memo format containing malicious payload
3. `OnRecvPacket` parses memo, finds valid `Message` structure
4. Middleware executes payload without verifying sender is authorized GMP account
5. Arbitrary cross-chain messages executed on target chain

**Scenario 2: Version Mismatch Breaking Hooks**
1. Chain A opens channel to Chain B using IBC hooks middleware
2. Underlying app negotiates version from `ics20-1` to `ics20-2`
3. Middleware ignores negotiated version, returns original `ics20-1`
4. Channel endpoints have mismatched versions
5. Custom hooks become ineffective, transfers may fail

**Scenario 3: Chain Halt via Malformed Acknowledgement**
1. Attacker has permission to open IBC channel (common in permissionless chains)
2. Attacker sends crafted acknowledgement packet exploiting JSON unmarshalling bug
3. Different validators deserialize differently due to non-determinism
4. Consensus failure, chain halts

#### Vulnerable Pattern Examples

**Example 1: Missing Channel/Sender Authentication** [Approx Severity: MEDIUM]
```go
// ❌ VULNERABLE: No authentication of sender or channel
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
    err := json.Unmarshal([]byte(data.GetMemo()), &msg)
    if err != nil || len(msg.Payload) == 0 {
        return im.app.OnRecvPacket(ctx, packet, relayer)
    }
    
    // Processes packet WITHOUT verifying:
    // - packet.SourceChannel is from authorized counterparty
    // - data.Sender is the authorized GMP account (e.g., AxelarGMPAcc)
    return im.processGMPPacket(ctx, packet, msg) // Attacker can execute arbitrary payloads!
}
```

**Example 2: Wrong Version Returned in Channel Handshake** [Approx Severity: MEDIUM]
```go
// ❌ VULNERABLE: Returns original version, not negotiated finalVersion
func (im IBCMiddleware) OnChanOpenInit(
    ctx sdk.Context,
    order channeltypes.Order,
    connectionHops []string,
    portID string,
    channelID string,
    channelCap *capabilitytypes.Capability,
    counterparty channeltypes.Counterparty,
    version string,
) (string, error) {
    if hook, ok := im.ICS4Middleware.Hooks.(OnChanOpenInitBeforeHooks); ok {
        hook.OnChanOpenInitBeforeHook(ctx, order, connectionHops, portID, channelID, channelCap, counterparty, version)
    }

    // Underlying app may negotiate a DIFFERENT version
    finalVersion, err := im.App.OnChanOpenInit(ctx, order, connectionHops, portID, channelID, channelCap, counterparty, version)

    if hook, ok := im.ICS4Middleware.Hooks.(OnChanOpenInitAfterHooks); ok {
        hook.OnChanOpenInitAfterHook(ctx, order, connectionHops, portID, channelID, channelCap, counterparty, version, finalVersion, err)
    }
    
    return version, err  // ❌ Should return finalVersion, not version!
}
```

**Example 3: Overly Permissive Packet Routing** [Approx Severity: MEDIUM]
```go
// ❌ VULNERABLE: Processes any packet with valid memo structure
func (im IBCMiddleware) OnRecvPacket(
    ctx sdk.Context,
    packet channeltypes.Packet,
    relayer sdk.AccAddress,
) ibcexported.Acknowledgement {
    var data transfertypes.FungibleTokenPacketData
    transfertypes.ModuleCdc.UnmarshalJSON(packet.GetData(), &data)

    var msg Message
    err := json.Unmarshal([]byte(data.GetMemo()), &msg)
    
    // Only checks memo format, not source
    // Commented out sender check shows intended logic was bypassed
    //if !strings.EqualFold(data.Sender, AxelarGMPAcc) {
    //    return im.app.OnRecvPacket(ctx, packet, relayer)
    //}
    
    if err != nil || len(msg.Payload) == 0 {
        return im.app.OnRecvPacket(ctx, packet, relayer)
    }
    
    // Any packet with valid memo format gets processed!
    return im.processMessage(ctx, packet, msg)
}
```

**Example 4: Missing Channel Existence Validation** [Approx Severity: MEDIUM]
```go
// ❌ VULNERABLE: No validation of IBC channel identifiers
func (k msgServer) UpdateEntry(goCtx context.Context, msg *types.MsgUpdateEntry) (*types.MsgUpdateEntryResponse, error) {
    if k.authority != msg.Authority {
        return nil, errors.Wrapf(govtypes.ErrInvalidSigner, "invalid authority")
    }

    ctx := sdk.UnwrapSDKContext(goCtx)
    entry, isFound := k.GetEntry(ctx, msg.BaseDenom)
    if !isFound {
        return nil, errorsmod.Wrap(sdkerrors.ErrKeyNotFound, "entry not set")
    }

    entry = types.Entry{
        IbcChannelId:             msg.IbcChannelId,             // No validation!
        IbcCounterpartyChannelId: msg.IbcCounterpartyChannelId, // No validation!
        IbcCounterpartyChainId:   msg.IbcCounterpartyChainId,   // No validation!
        // ... other fields
    }

    k.SetEntry(ctx, entry)
    return &types.MsgUpdateEntryResponse{}, nil
}
```

### Impact Analysis

#### Technical Impact
- Arbitrary cross-chain message execution
- Channel version mismatches breaking interoperability
- Chain halt from non-deterministic packet processing
- Invalid IBC configuration corrupting system state

#### Business Impact
- Cross-chain asset theft via unauthorized transfers
- Failed interoperability with partner chains
- Network downtime during chain halt
- Loss of trust in cross-chain security

#### Affected Scenarios
- Custom GMP (General Message Passing) implementations
- IBC hooks middleware for wasm/evm execution
- Cross-chain governance or oracle systems
- Token transfer with memo-based routing

### Secure Implementation

**Fix 1: Authenticate Sender and Channel**
```go
// ✅ SECURE: Verify sender and channel before processing
func (im IBCMiddleware) OnRecvPacket(
    ctx sdk.Context,
    packet channeltypes.Packet,
    relayer sdk.AccAddress,
) ibcexported.Acknowledgement {
    var data transfertypes.FungibleTokenPacketData
    if err := transfertypes.ModuleCdc.UnmarshalJSON(packet.GetData(), &data); err != nil {
        return channeltypes.NewErrorAcknowledgement(err)
    }

    var msg Message
    if err := json.Unmarshal([]byte(data.GetMemo()), &msg); err != nil || len(msg.Payload) == 0 {
        return im.app.OnRecvPacket(ctx, packet, relayer)
    }
    
    // Authenticate channel ID
    if packet.DestinationChannel != im.authorizedChannelID {
        return im.app.OnRecvPacket(ctx, packet, relayer)
    }
    
    // Authenticate sender address
    if !strings.EqualFold(data.Sender, im.authorizedGMPAccount) {
        return im.app.OnRecvPacket(ctx, packet, relayer)
    }
    
    return im.processGMPPacket(ctx, packet, msg)
}
```

**Fix 2: Return Negotiated Version**
```go
// ✅ SECURE: Return finalVersion from underlying app
func (im IBCMiddleware) OnChanOpenInit(
    ctx sdk.Context,
    order channeltypes.Order,
    connectionHops []string,
    portID string,
    channelID string,
    channelCap *capabilitytypes.Capability,
    counterparty channeltypes.Counterparty,
    version string,
) (string, error) {
    if hook, ok := im.ICS4Middleware.Hooks.(OnChanOpenInitBeforeHooks); ok {
        hook.OnChanOpenInitBeforeHook(ctx, order, connectionHops, portID, channelID, channelCap, counterparty, version)
    }

    finalVersion, err := im.App.OnChanOpenInit(ctx, order, connectionHops, portID, channelID, channelCap, counterparty, version)
    if err != nil {
        return "", err
    }

    if hook, ok := im.ICS4Middleware.Hooks.(OnChanOpenInitAfterHooks); ok {
        hook.OnChanOpenInitAfterHook(ctx, order, connectionHops, portID, channelID, channelCap, counterparty, version, finalVersion, nil)
    }
    
    return finalVersion, nil  // ✅ Return negotiated version!
}
```

**Fix 3: Validate IBC Channel Identifiers**
```go
// ✅ SECURE: Validate channel existence before using
func (k msgServer) UpdateEntry(goCtx context.Context, msg *types.MsgUpdateEntry) (*types.MsgUpdateEntryResponse, error) {
    ctx := sdk.UnwrapSDKContext(goCtx)
    
    // Validate IBC channel exists and is open
    if msg.IbcChannelId != "" {
        channel, found := k.channelKeeper.GetChannel(ctx, transfertypes.PortID, msg.IbcChannelId)
        if foundryup
git init
forge install OpenZeppelin/openzeppelin-contracts 1inch/token-plugins=1inch/token-plugins@d71d6500e954315871bf9da070a6d9d95ac65015 1inch/solidity-utils=1inch/solidity-utils 1inch/farming=1inch/farming@da9c87962272fdcfcee79be14eb13b27387a677e mangrovedao/mangrove-core morpho-org/morpho-blue foundry-rs/forge-std nomad-xyz/ExcessivelySafeCall 

forge build --skip=Skip --sizes
forge test
 {
            return nil, errors.Wrap(sdkerrors.ErrNotFound, "IBC channel not found")
        }
        if channel.State != channeltypes.OPEN {
            return nil, errors.Wrap(sdkerrors.ErrInvalidRequest, "IBC channel not open")
        }
        // Verify counterparty matches
        if channel.Counterparty.ChannelId != msg.IbcCounterpartyChannelId {
            return nil, errors.Wrap(sdkerrors.ErrInvalidRequest, "counterparty channel mismatch")
        }
    }
    
    // ... proceed with update
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- Pattern 1: `OnRecvPacket` without channel/sender verification
- Pattern 2: `return version, err` instead of `return finalVersion, err`
- Pattern 3: Commented-out authentication checks (TODO/FIXME)
- Pattern 4: `json.Unmarshal` on packet memo without source validation
- Pattern 5: IBC channel ID fields accepted without validation
```

#### Audit Checklist
- [ ] `OnRecvPacket` validates source channel against whitelist
- [ ] `OnRecvPacket` verifies packet sender is authorized account
- [ ] Channel handshake returns negotiated version from underlying app
- [ ] IBC channel configuration updates validate channel existence
- [ ] Using patched IBC-Go version (>= v8.6.1 for ASA-2025-004)
- [ ] No commented-out authentication logic in production code

### Real-World Examples

| Protocol | Audit Firm | Severity | Issue |
|----------|------------|----------|-------|
| Initia | Code4rena | MEDIUM | Version negotiation bypass in IBC hooks |
| Allora | Sherlock | MEDIUM | Missing authentication in OnRecvPacket |
| Allora | Sherlock | MEDIUM | Logic bug in packet handling - unintended processing |
| SEDA | Sherlock | HIGH | Vulnerable IBC-Go v8.4.0 - chain halt |
| Elys | Halborn | MEDIUM | Missing IBC channel verification |

### Keywords for Search

`IBC, OnRecvPacket, OnChanOpenInit, channel_handshake, version_negotiation, packet_authentication, sender_verification, channel_validation, cross_chain, GMP, middleware, IBC_hooks, ICS20, fungible_token_packet, memo_parsing, ASA-2025-004`
