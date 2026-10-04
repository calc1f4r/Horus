---
# Core Classification
protocol: Connext NXTP — Noncustodial Xchain Transfer Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13339
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2021/07/connext-nxtp-noncustodial-xchain-transfer-protocol/
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

protocol_categories:
  - services
  - synthetics

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Martin Ortner
  -  Heiko Fisch

  -  David Oz Kashi
---

## Vulnerability Title

FulfillInterpreter - Missing check whether callTo address contains code ✓ Fixed

### Overview

See description below for full details.

### Original Finding Content

#### Resolution



This issue has been fixed.


#### Description


The receiver-side `prepare` checks whether the `callTo` address is either zero or a contract:


**code/packages/contracts/contracts/TransactionManager.sol:L466-L470**



```
// Check that the callTo is a contract
// NOTE: This cannot happen on the sending chain (different chain
// contexts), so a user could mistakenly create a transfer that must be
// cancelled if this is incorrect
require(invariantData.callTo == address(0) || Address.isContract(invariantData.callTo), "#P:031");

```
However, as a contract may `selfdestruct` and the check is not repeated later, there is no guarantee that `callTo` still contains code when the call to this address (assuming it is non-zero) is actually executed in `FulfillInterpreter.execute`:


**code/packages/contracts/contracts/interpreters/FulfillInterpreter.sol:L71-L82**



```
// Try to execute the callData
// the low level call will return `false` if its execution reverts
(bool success, bytes memory returnData) = callTo.call{value: isEther ? amount : 0}(callData);

if (!success) {
  // If it fails, transfer to fallback
  Asset.transferAsset(assetId, fallbackAddress, amount);
  // Decrease allowance
  if (!isEther) {
    Asset.decreaseERC20Allowance(assetId, callTo, amount);
  }
}

```
As a result, if the contract at `callTo` self-destructs between `prepare` and `fulfill` (both on the receiving chain), `success` will be `true`, and the funds will probably be lost to the user.


A user could currently try to avoid this by checking that the contract still exists before calling `fulfill` on the receiving chain, but even then, they might get front-run by `selfdestruct`, and the situation is even worse with a relayer, so this provides no reliable protection.


#### Recommendation


Repeat the `Address.isContract` check on `callTo` before making the external call in `FulfillInterpreter.execute` and send the funds to the `fallbackAddress` if the result is `false`.


It is, perhaps, debatable whether the check in `prepare` should be kept or removed. In principle, if the contract gets deployed between `prepare` and `fulfill`, that is still soon enough. However, if the `callTo` address doesn’t have code at the time of `prepare`, this seems more likely to be a mistake than a “late deployment”. So unless there is a demonstrated use case for “late deployments”, failing in `prepare` (even though it’s receiver-side) might still be the better choice.


#### Remark


It should be noted that an unsuccessful call, i.e., a revert, is the only behavior that is recognized by `FulfillInterpreter.execute` as failure. While it is prevalent to indicate failure by reverting, this doesn’t *have to* be the case; a well-known example is an ERC20 token that indicates a failing transfer by returning `false`.  

A user who wants to utilize this feature has to make sure that the called contract behaves accordingly; if that is not the case, an intermediary contract may be employed, which, for example, reverts for return value `false`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Connext NXTP — Noncustodial Xchain Transfer Protocol |
| Report Date | N/A |
| Finders | Martin Ortner,  Heiko Fisch
,  David Oz Kashi |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2021/07/connext-nxtp-noncustodial-xchain-transfer-protocol/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

