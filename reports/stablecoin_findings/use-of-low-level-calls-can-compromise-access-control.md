---
# Core Classification
protocol: Wonderland Prophet
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41800
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-05-wonderland-prophet-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-05-wonderland-prophet-securityreview.pdf
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
finders_count: 3
finders:
  - Tjaden Hess
  - Elvis Skoždopolj
  - Nat Chin
---

## Vulnerability Title

Use of low-level calls can compromise access control

### Overview


The report discusses a low-level data validation bug found in the CallbackModule, MultipleCallbacksModule, and CircuitResolverModule contracts. These contracts are used in the overall protocol and have substantial permissions. Malicious users can exploit this bug to steal user funds by calling functions in the AccountingExtension and BondEscalationAccounting contracts, as well as the Oracle contract. The bug can be exploited by setting a specific callback target and data, allowing the malicious user to transfer funds to themselves. The report recommends replacing the arbitrary low-level callbacks with a specific callback interface in the short term and not allowing calls from privileged contracts to user-chosen endpoints in the long term. 

### Original Finding Content

## Difficulty: Low

## Type: Data Validation

## Description
The `CallbackModule`, `MultipleCallbacksModule`, and `CircuitResolverModule` contracts perform low-level calls with user-specified input data and target addresses. These contracts are trusted modules with substantial permissions in the overall protocol. Malicious users can call functions guarded with the `onlyAllowedModule` modifier in the `AccountingExtension` and `BondEscalationAccounting` contracts, potentially stealing user funds. They can also call functions in the `Oracle` contract such as `updateDisputeStatus`, leading to stolen funds or other invalid behavior.

```solidity
/// @inheritdoc ICallbackModule
function finalizeRequest(
    IOracle.Request calldata _request,
    IOracle.Response calldata _response,
    address _finalizer
) external override(Module, ICallbackModule) onlyOracle {
    RequestParameters memory _params = decodeRequestData(_request.finalityModuleData);
    _params.target.call(_params.data);
    emit Callback(_response.requestId, _params.target, _params.data);
    emit RequestFinalized(_response.requestId, _response, _finalizer);
}
```
*Figure 11.1: Unrestricted low-level call in CallbackModule*

## Exploit Scenario
A stablecoin protocol uses the Prophet system to fetch centralized exchange price data via the `HttpRequestModule`. It uses the `BondEscalationModule` for disputes and `MultipleCallbacksModule` for finalization. The protocol pre-fills the `Request` struct with appropriate data but allows end-users to specify a callback target to be notified when the result is finalized.

Mallory, a malicious user, submits a request that includes the address of `BondEscalationModule` as the callback target. She sets the callback data to match an ABI-encoded call to the `pay` function, transferring another user’s bonded funds to herself.

## Recommendations
- **Short term:** Replace the arbitrary low-level callbacks with a specific callback interface.
- **Long term:** Do not allow calls from privileged contracts to user-chosen endpoints.

## Detailed Findings: Prophet Core

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Wonderland Prophet |
| Report Date | N/A |
| Finders | Tjaden Hess, Elvis Skoždopolj, Nat Chin |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2024-05-wonderland-prophet-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2024-05-wonderland-prophet-securityreview.pdf

### Keywords for Search

`vulnerability`

