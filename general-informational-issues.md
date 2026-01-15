---
# Core Classification
protocol: Cryptex
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52944
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/cc661600-b854-49ec-8d9a-90d164b65f28
source_link: https://cdn.cantina.xyz/reports/cantina_cryptex_february2025.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Anurag Jain
  - StErMi
---

## Vulnerability Title

General informational issues 

### Overview

See description below for full details.

### Original Finding Content

## Context
(No context files were provided by the reviewer)

## Description

## Natspec typos, errors or improvements
- **GovernanceCCIPReceiver.sol#L39-L42:** The `GovernanceCCIPReceiver` constructor natspec is outdated. It's referring to the `BaseGovernanceReceiver` contract and misses the natspec for both the `_router` and `_sender` input parameters.

## Renaming, refactoring and Code improvement
- **GovernanceCCIPRelay.sol#L90:** `GovernanceCCIPRelay.relayMessage` should return the `bytes32` `messageId` returned by the `ccipRouter.ccipSend` call.
- **GovernanceCCIPRelay.sol#L78:** `GovernanceCCIPRelay.setDestinationReceiver` should early return if `_receiver == destinationReceiver` and avoid emitting a useless event.
- **GovernanceCCIPRelay.sol#L13-L23:** Consider declaring the `ccipRouter`, `timelock`, and `destinationChainSelector` state variables in `GovernanceCCIPRelay` as immutable. The contract is not upgradable and has no setter to update them.
- **GovernanceCCIPReceiver.sol#L14-L15:** Consider declaring the `mainnetSender` state variable in `GovernanceCCIPReceiver` as immutable. The contract is not upgradable and has no setter to update it.
- **GovernanceCCIPReceiver.sol#L17-L18:** Consider declaring the `mainnetChainSelector` state variable as constant with the value set to `5009297550715157269`. From our understanding, the source chain will always be mainnet and will never change. We can retrieve the current value used by Chainlink for the Mainnet Chain selector directly from their Ethereum CCIP Documentation.
- Consider switching all the revert statements to the new require pattern which is easier to read and understand: replace all instances of `if (!someGuard) revert ErrorToThrow()` to the form `require(someGuard, ErrorToThrow())`.
- **GovernanceCCIPReceiver.sol#L6:** Remove the imports from the Forge testing library.
- **GovernanceCCIPRelay.sol#L28-L30:** The `MessageRelayed` and `DestinationReceiverUpdated` events are not using the indexed keyword for their inputs. Consider declaring some of their inputs as indexed to be able to filter them off-chain.
- **GovernanceCCIPReceiver.sol#L23:** The `MessageExecuted` is not using the indexed keyword for its inputs. Consider declaring some of the inputs as indexed to be able to filter them off-chain.
- **GovernanceCCIPRelay.sol:** Consider adopting the standard best practices and solidity style guide to make the `GovernanceCCIPRelay` code more clear, easier to read and understand:
  1. Create an `IGovernanceCCIPRelay` interface and make `GovernanceCCIPRelay` inherit from it.
  2. Move all the event and error declarations into the interface.
  3. Move the natspec of the functions into the interface.
  4. Replace the current natspec of the external/public functions with the `/// @inheritdoc IGovernanceCCIPRelay` tag.
- **GovernanceCCIPReceiver.sol:** Consider adopting the standard best practices and solidity style guide to make the `GovernanceCCIPReceiver` code more clear, easier to read and understand:
  1. Create an `IGovernanceCCIPReceiver` interface and make `GovernanceCCIPReceiver` inherit from it.
  2. Move all the event and error declarations into the interface.
  3. Move the natspec of the functions into the interface.
  4. Replace the current natspec of the external/public functions with the `/// @inheritdoc IGovernanceCCIPReceiver` tag.
- **GovernanceCCIPReceiver.sol#L27:** `GovernanceCCIPReceiver` contract defines `MainnetSenderUpdated` event which is not required since `mainnetSender` never changes in contract. Remove the event declaration.
- **CryptexBaseTreasury.sol#L21:** `renounceOwnership` mistakenly mentions network as Arbitrum instead of Base on revert. Change `ArbitrumTreasury` to `BaseTreasury`.

## Recommendations
Cryptex should fix all the suggestions listed in the above section.

## Cryptex
Implemented changes in PR 167. All changes have been implemented except:
- **GovernanceCCIPRelay.sol#L78:** `GovernanceCCIPRelay.setDestinationReceiver` should early return if `_receiver == destinationReceiver` and avoid emitting a useless event. Not implemented as a new function has been added in its place in PR 169.
- **GovernanceCCIPRelay.sol#L28-L30:** The `MessageRelayed` and `DestinationReceiverUpdated` events are not using the indexed keyword for their inputs. Consider declaring some of their inputs as indexed to be able to filter them off-chain. Did not update `DestinationReceiverUpdated` as this event has been changed in PR 169.

## Cantina Managed
Fix verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Cryptex |
| Report Date | N/A |
| Finders | Anurag Jain, StErMi |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_cryptex_february2025.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/cc661600-b854-49ec-8d9a-90d164b65f28

### Keywords for Search

`vulnerability`

