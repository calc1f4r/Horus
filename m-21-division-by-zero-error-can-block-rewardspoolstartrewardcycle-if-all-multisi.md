---
# Core Classification
protocol: GoGoPool
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 8848
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-12-gogopool-contest
source_link: https://code4rena.com/reports/2022-12-gogopool
github_link: https://github.com/code-423n4/2022-12-gogopool-findings/issues/143

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - liquid_staking
  - cdp
  - yield
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 6
finders:
  - __141345__
  - pauliax
  - peakbolt
  - ladboy233
  - unforgiven
---

## Vulnerability Title

[M-21] Division by zero error can block RewardsPool#startRewardCycle if all multisig wallet are disabled

### Overview


This bug report is about an issue in the RewardsPool.sol contract, which is part of the 2022-12-gogopool project. The code in question is located at two lines of code in the RewardsPool.sol contract: line 229 and line 156. 

The vulnerability is a division by zero error that can block the RewardsPool#startRewardCycle function if all multisig wallets are disabled. This can be demonstrated by a proof-of-concept (POC) code. The code attempts to distribute rewards to all multisig wallets evenly, but if there are no enabled wallets, the transaction will revert in a division by zero error and the startRewardsCycle transaction will be blocked.

The recommended mitigation steps are to handle the case when the number of enabled multisig wallets is 0 gracefully, so that the startRewardCycle transaction is not blocked.

### Original Finding Content

## Lines of code

https://github.com/code-423n4/2022-12-gogopool/blob/aec9928d8bdce8a5a4efe45f54c39d4fc7313731/contracts/contract/RewardsPool.sol#L229
https://github.com/code-423n4/2022-12-gogopool/blob/aec9928d8bdce8a5a4efe45f54c39d4fc7313731/contracts/contract/RewardsPool.sol#L156


## Vulnerability details

## Impact

Division by zero error can block RewardsPool#startRewardCycle if all multisig wallet is disabled.

## Proof of Concept

A user needs to call the function startRewardsCycle in RewardsPool.sol

```solidity
/// @notice Public function that will run a GGP rewards cycle if possible
function startRewardsCycle() external {
```

which calls:

```solidity
uint256 multisigClaimContractAllotment = getClaimingContractDistribution("ClaimMultisig");
uint256 nopClaimContractAllotment = getClaimingContractDistribution("ClaimNodeOp");
uint256 daoClaimContractAllotment = getClaimingContractDistribution("ClaimProtocolDAO");
if (daoClaimContractAllotment + nopClaimContractAllotment + multisigClaimContractAllotment > getRewardsCycleTotalAmt()) {
	revert IncorrectRewardsDistribution();
}

TokenGGP ggp = TokenGGP(getContractAddress("TokenGGP"));
Vault vault = Vault(getContractAddress("Vault"));

if (daoClaimContractAllotment > 0) {
	emit ProtocolDAORewardsTransfered(daoClaimContractAllotment);
	vault.transferToken("ClaimProtocolDAO", ggp, daoClaimContractAllotment);
}

if (multisigClaimContractAllotment > 0) {
	emit MultisigRewardsTransfered(multisigClaimContractAllotment);
	distributeMultisigAllotment(multisigClaimContractAllotment, vault, ggp);
}

if (nopClaimContractAllotment > 0) {
	emit ClaimNodeOpRewardsTransfered(nopClaimContractAllotment);
	ClaimNodeOp nopClaim = ClaimNodeOp(getContractAddress("ClaimNodeOp"));
	nopClaim.setRewardsCycleTotal(nopClaimContractAllotment);
	vault.transferToken("ClaimNodeOp", ggp, nopClaimContractAllotment);
}
```

We need to pay speical attention to the code block below:

```solidity
if (multisigClaimContractAllotment > 0) {
	emit MultisigRewardsTransfered(multisigClaimContractAllotment);
	distributeMultisigAllotment(multisigClaimContractAllotment, vault, ggp);
}
```

which calls:

```solidity
/// @notice Distributes GGP to enabled Multisigs
/// @param allotment Total GGP for Multisigs
/// @param vault Vault contract
/// @param ggp TokenGGP contract
function distributeMultisigAllotment(
uint256 allotment,
Vault vault,
TokenGGP ggp
) internal {
MultisigManager mm = MultisigManager(getContractAddress("MultisigManager"));

uint256 enabledCount;
uint256 count = mm.getCount();
address[] memory enabledMultisigs = new address[](count);

// there should never be more than a few multisigs, so a loop should be fine here
for (uint256 i = 0; i < count; i++) {
	(address addr, bool enabled) = mm.getMultisig(i);
	if (enabled) {
		enabledMultisigs[enabledCount] = addr;
		enabledCount++;
	}
}

// Dirty hack to cut unused elements off end of return value (from RP)
// solhint-disable-next-line no-inline-assembly
assembly {
	mstore(enabledMultisigs, enabledCount)
}

uint256 tokensPerMultisig = allotment / enabledCount;
for (uint256 i = 0; i < enabledMultisigs.length; i++) {
	vault.withdrawToken(enabledMultisigs[i], ggp, tokensPerMultisig);
}
}
```

the code distribute the reward to all multisig evenly.

```solidity
uint256 tokensPerMultisig = allotment / enabledCount;
```

However, if the enabledCount is 0, meaning no multisig wallet is enabled, the transactionr revert in division by zero error and revert the startRewardsCycle transaction.

As showns in POC.

In RewardsPool.t.sol,

we change the name from testStartRewardsCycle to testStartRewardsCycle_POC

https://github.com/code-423n4/2022-12-gogopool/blob/aec9928d8bdce8a5a4efe45f54c39d4fc7313731/test/unit/RewardsPool.t.sol#L123

we add the code to disable all multisig wallet. before calling rewardsPool.startRewardsCycle

https://github.com/code-423n4/2022-12-gogopool/blob/aec9928d8bdce8a5a4efe45f54c39d4fc7313731/test/unit/RewardsPool.t.sol#L138

```solidity
// disable all multisg wallet
vm.prank(guardian);
ocyticus.disableAllMultisigs();
```

Then we run the test

```solidity
forge test -vvv --match testStartRewardsCycle_POC
```

the transaction revert in division by zero error, which block the startRewardsCycle

```solidity
    │   ├─ emit MultisigRewardsTransfered(value: 13499352589262561353689)
    │   ├─ [537] Storage::getAddress(0xcda836d09bcf3adcec2f52ddddeceac31738a574d5063511c887064e499593df) [staticcall]
    │   │   └─ ← MultisigManager: [0xA12E9172eB5A8B9054F897cC231Cd7a2751D6D93]
    │   ├─ [1313] MultisigManager::getCount() [staticcall]
    │   │   ├─ [549] Storage::getUint(0x778484468bc504108f077f6bf471293e4138c2d117c6f33607855518cf4bda79) [staticcall]
    │   │   │   └─ ← 1
    │   │   └─ ← 1
    │   ├─ [3050] MultisigManager::getMultisig(0) [staticcall]
    │   │   ├─ [537] Storage::getAddress(0xfebe6f39b65f18e050b53df1d0c8d45b8c5cce333324eb048b67b8ee5f26b7a3) [staticcall]
    │   │   │   └─ ← RialtoSimulator: [0x98D1613BC08756f51f46E841409E61C32f576F2f]
    │   │   ├─ [539] Storage::getBool(0x7ef800e7ca09c0c1063313b56290c06f6bc4bae0e9b7af3899bb7d5ade0403c8) [staticcall]
    │   │   │   └─ ← false
    │   │   └─ ← RialtoSimulator: [0x98D1613BC08756f51f46E841409E61C32f576F2f], false
    │   └─ ← "Division or modulo by 0"
    └─ ← "Division or modulo by 0"

Test result: FAILED. 0 passed; 1 failed; finished in 11.64ms

Failing tests:
Encountered 1 failing test in test/unit/RewardsPool.t.sol:RewardsPoolTest
[FAIL. Reason: Division or modulo by 0] testStartRewardsCycle_POC() (gas: 332890)
```

## Tools Used

Manual Review

## Recommended Mitigation Steps

We recommend the project handle the case when the number of enabled multisig is 0 gracefully to not block the startRewardCycle transaction.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | GoGoPool |
| Report Date | N/A |
| Finders | __141345__, pauliax, peakbolt, ladboy233, unforgiven, rvierdiiev |

### Source Links

- **Source**: https://code4rena.com/reports/2022-12-gogopool
- **GitHub**: https://github.com/code-423n4/2022-12-gogopool-findings/issues/143
- **Contest**: https://code4rena.com/contests/2022-12-gogopool-contest

### Keywords for Search

`vulnerability`

