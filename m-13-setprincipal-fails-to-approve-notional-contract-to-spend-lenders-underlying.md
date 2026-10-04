---
# Core Classification
protocol: Illuminate
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3741
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/12
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-illuminate-judging/issues/41

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

protocol_categories:
  - dexes
  - cdp
  - yield
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - rvierdiiev
  - bin2chen
  - neumo
  - minhtrng
  - Holmgren
---

## Vulnerability Title

M-13: setPrincipal fails to approve Notional contract to spend lender's underlying tokens

### Overview


Issue M-13 is a bug in the Marketplace contract of the Sherlock Audit 2022-10-illuminate project. The bug is caused by passing the zero address as underlying to the lender's approve function when trying to add a Notional principal at a later time via setPrincipal. This means that the lender contract is not able to approve the notional contract to spend its underlying tokens. This can be tested with a test added to the Marketplace.t.sol file. The bug has a lesser impact as the admin can fix this issue by approving the notional contract over the underlying token. The recommendation is to change line 238 of the Marketplace contract with a different code snippet. The issue was found by minhtrng, bin2chen, neumo, rvierdiiev, Holmgren and was discussed by pauliax who suggested to escalate for 2 USDC.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-illuminate-judging/issues/41 

## Found by 
minhtrng, bin2chen, neumo, rvierdiiev, Holmgren

## Summary
If the **Notional** principal is not set at Marketplace creation, when trying to add it at a later time via **setPrincipal**, the call will not accomplish that the lender approves the notional contract to spend its underlying tokens,  due to passing the zero address as underlying to the lender's approve function.

## Vulnerability Detail
The vulnerability lies in line 238 of **Marketplace** contract:
https://github.com/sherlock-audit/2022-10-illuminate/blob/main/src/Marketplace.sol#L238
Function **approve** of **Lender** contract expects the address of the underlying contract as the first parameter:
https://github.com/sherlock-audit/2022-10-illuminate/blob/main/src/Lender.sol#L194-L214
As the underlying address passed in in the buggy line above is the zero address, **uToken** is also the zero adress and `Safe.approve(uToken, n, max);` just calls approve on the zero address, which does nothing (not even reverting because there's no contract deployed there). 


## Impact
If there was no way for the lender contract to approve the notional address, I would rate this issue as High, but since there is an admin function `function approve(address[] calldata u, address[] calldata a)`, the admin could fix this issue approving the notional contract over the underlying token, making the impact less severe. But in the meantime **Notional**'s lending would revert due to the lack of approval.

## Code Snippet
The following test, that can be added in the **MarketPlace.t.sol** file, proves this vulnerability:
```solidity
function testIssueSetPrincipalNotional() public {

	address notional = address(token7);

	address[8] memory contracts;
	contracts[0] = address(token0); // Swivel
	contracts[1] = address(token1); // Yield
	contracts[2] = address(token2); // Element
	contracts[3] = address(token3); // Pendle
	contracts[4] = address(token4); // Tempus
	contracts[5] = address(token5); // Sense
	contracts[6] = address(token6); // APWine
	contracts[7] = address(0); // Notional unset at market creation

	mock_erc20.ERC20(underlying).decimalsReturns(10);
	mock_erc20.ERC20 compounding = new mock_erc20.ERC20();
	token6.futureVaultReturns(address(apwfv));
	apwfv.getIBTAddressReturns(address(compounding));

	token3.underlyingYieldTokenReturns(address(compounding));

	mp.createMarket(
		address(underlying),
		maturity,
		contracts,
		'test-token',
		'tt',
		address(elementVault),
		address(apwineRouter)
	);

	// verify approvals
	assertEq(r.approveCalled(), address(compounding));

	// We verify that the notional address approved for address(0) is unset
	(, , address approvedNotional) = l.approveCalled(address(0));
	assertEq(approvedNotional, address(0));
	// and that the approved notional for address(underlying) is unset
	(, , approvedNotional) = l.approveCalled(address(underlying));
	assertEq(approvedNotional, address(0));

	// Then we call setPrincipal for the notional address
	mp.setPrincipal(uint8(MarketPlace.Principals.Notional), address(underlying), maturity, notional);

	// Now we verify that, after the call to setPrincipal, the notional address 
	// approved for address(0) is the Notional address provided in the call
	(, , approvedNotional) = l.approveCalled(address(0));
	assertEq(approvedNotional, notional);
	// and that the approved notional for address(underlying) is still unset
	(, , approvedNotional) = l.approveCalled(address(underlying));
	assertEq(approvedNotional, address(0));
}
```

## Tool used

Forge Tests and manual Review

## Recommendation
Change this line in Marketplace.sol:
https://github.com/sherlock-audit/2022-10-illuminate/blob/main/src/Marketplace.sol#L238
with this:
`ILender(lender).approve(address(u), address(0), address(0), a);`

## Discussion

**pauliax**

Escalate for 2 USDC.
Basically, I have described the same issue in a more generic submission: #233

**sherlock-admin**

 > Escalate for 2 USDC.
> Basically, I have described the same issue in a more generic submission: #233

You've created a valid escalation for 2 USDC!

To remove the escalation from consideration: Delete your comment.
To change the amount you've staked on this escalation: Edit your comment **(do not create a new comment)**.

You may delete or edit your escalation comment anytime before the 48-hour escalation window closes. After that, the escalation becomes final.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Illuminate |
| Report Date | N/A |
| Finders | rvierdiiev, bin2chen, neumo, minhtrng, Holmgren |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-10-illuminate-judging/issues/41
- **Contest**: https://app.sherlock.xyz/audits/contests/12

### Keywords for Search

`vulnerability`

