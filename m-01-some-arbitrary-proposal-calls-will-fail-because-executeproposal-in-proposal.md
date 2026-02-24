---
# Core Classification
protocol: Party Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29547
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-10-party
source_link: https://code4rena.com/reports/2023-10-party
github_link: https://github.com/code-423n4/2023-10-party-findings/issues/475

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
  - Vagner
  - Arz
  - HChang26
---

## Vulnerability Title

[M-01] Some arbitrary proposal calls will fail because `executeProposal()` in `ProposalExecutionEngine` is not payable

### Overview


The `executeProposal()` function in `ProposalExecutionEngine.sol` is used to execute different types of proposals, including `ArbitraryCallsProposal`, which should be able to send ether from the Party's balance or the forwarded ETH attached to the call `msg.value`. However, the function is not marked as payable, causing all calls that use `msg.value` to fail. This means that the Party is unable to execute these types of proposals, which can be important. The recommended mitigation step is to make the `executeProposal()` function payable.

### Original Finding Content


The `executeProposal()` function in `ProposalExecutionEngine.sol` is used to execute different types of proposal call. One of this type is `ArbitraryCallsProposal` and this type should be able to send ether from the Party's balance or the forwarded ETH attached to the call `msg.value`. However, the problem is that the `executeProposal()` function is not marked as payable and all calls that are sending ether and using `msg.value` will fail because of that.

Note: Even though this function is delegate-called from `PartyGovernance.sol::execute()`, which is payable the `msg.value`, it is still preserved when `delegatecall` is used and the function called needs to be payable.

### Impact

All proposal calls that are using attached ether will fail and Party wont be able to execute these types of proposals, which can be important.

### Proof of Concept

<https://github.com/code-423n4/2023-10-party/blob/b23c65d62a20921c709582b0b76b387f2bb9ebb5/contracts/proposals/ProposalExecutionEngine.sol#L146-L148>

```solidity
146:   function executeProposal(
147:     ExecuteProposalParams memory params
148:   ) external onlyDelegateCall returns (bytes memory nextProgressData) { 
```

As you can see, the `executeProposal()` function is not payable; however, later it then calls `_executeArbitraryCalls()`:

<https://github.com/code-423n4/2023-10-party/blob/b23c65d62a20921c709582b0b76b387f2bb9ebb5/contracts/proposals/ArbitraryCallsProposal.sol#L72-L74>

```solidity
72:  // If we're not allowing arbitrary calls to spend the Party's ETH, only
73:  // allow forwarded ETH attached to the call to be spent.
74:  uint256 ethAvailable = allowArbCallsToSpendPartyEth ? address(this).balance : msg.value;
```

As you can see and as the comment suggests, the call should be able to use the forwarded ether attached to the call and `ethAvailable` is then used in `_executeSingleArbitraryCall()`. However, because the function is not payable, the call will revert.

### Recommended Mitigation Steps

Make the `executeProposal()` function payable.

### Assessed type

Payable

**[KingNFT (lookout) commented](https://github.com/code-423n4/2023-10-party-findings/issues/475#issuecomment-1806831773):**
 > Seems right, EVM source code:
> ```golang
> File: core\vm\contract.go
> 134: func (c *Contract) AsDelegate() *Contract {
> 135: 	// NOTE: caller must, at all times be a contract. It should never happen
> 136: 	// that caller is something other than a Contract.
> 137: 	parent := c.caller.(*Contract)
> 138: 	c.CallerAddress = parent.CallerAddress
> 139: 	c.value = parent.value
> 140: 
> 141: 	return c
> 142: }
> ```

**[arr00 (Party) confirmed](https://github.com/code-423n4/2023-10-party-findings/issues/475#issuecomment-1811162360)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Party Protocol |
| Report Date | N/A |
| Finders | Vagner, Arz, HChang26 |

### Source Links

- **Source**: https://code4rena.com/reports/2023-10-party
- **GitHub**: https://github.com/code-423n4/2023-10-party-findings/issues/475
- **Contest**: https://code4rena.com/reports/2023-10-party

### Keywords for Search

`vulnerability`

