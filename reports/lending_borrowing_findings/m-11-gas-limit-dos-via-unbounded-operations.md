---
# Core Classification
protocol: Union Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3582
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/11
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-union-finance-judging/issues/69

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
  - services
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Ch\_301
  - ctf\_sec
---

## Vulnerability Title

M-11: gas limit DoS via unbounded operations

### Overview


Issue M-11 is a bug found by Ch_301 and ctf_sec in the UserManager.sol and UToken.sol contracts. It is a gas limit DoS via unbounded operations vulnerability that can be exploited in two ways. In the first case, a malicious user can keep vouching Alice with trustAmount set to 0 until the vouchers array reaches its max limit. This prevents normal users from vouching Alice with trustAmount not equal to 0. In the second case, the malicious user can keep vouching Alice with trustAmount set to 0 until the vouchers array reaches late's say 20% of max limit. When Alice invokes borrow() or repayBorrow() on UToken.sol, it calls updateLocked() on UserManager.sol, which has a for loop that can go through the vouchers array, leading to the gas limit DoS. Additionally, the registerMember() function can be used to prevent a user from successfully invoking it.

The impact of this bug is that users can't get any more vouching, borrow(), or repayBorrow(), and no one can successfully invoke registerMember() for a specific user. Dmitriia suggested adding a check for trustAmount equal to 0 as the same can be repeated with dust amounts.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-union-finance-judging/issues/69 

## Found by 
Ch\_301, ctf\_sec

## Summary
Only one attack will lead to two types of vulnerabilities in `UserManager.sol` and `UToken.sol`

## Vulnerability Detail
On `UserManager.sol` ==> `updateTrust()`
Case one:
 malicious users (members) can keep `vouching` Alice with `trustAmount == 0` until his `vouchers` array achieves the max limit (2**256-1)
So when a normal member tries to give `vouching` to Alice with `trustAmount != 0` he will find because the `vouchers` array completely full. 

Case two (which is more realistic ):
 malicious users (members) can keep `vouching` Alice with `trustAmount == 0` until his `vouchers` array achieves late’s say 20% of max limit (2**256-1)
The problem is when Alice invoke `borrow()` or `repayBorrow()` on `UToken.sol`

```solidity
   IUserManager(userManager).updateLocked(msg.sender, uint96(amount + fee), true);
  …
  IUserManager(userManager).updateLocked(borrower, uint96(repayAmount - interest), false);
```
It will call `updateLocked()` on `UserManager.sol`

```solidity
   function updateLocked(
        address borrower,
        uint96 amount,
        bool lock
    ) external onlyMarket {
        uint96 remaining = amount;

        for (uint256 i = 0; i < vouchers[borrower].length; i++) {
 
```
The for loop could go through `vouchers[]` which could be long enough to lead to a "gas limit DoS via unbounded operations" 
And the same thing with `registerMember()`, any user could lose all their fund in this transaction 
```solidity
       function registerMember(address newMember) public virtual whenNotPaused {
        if (stakers[newMember].isMember) revert NoExistingMember();

        uint256 count = 0;
        uint256 vouchersLength = vouchers[newMember].length;

        // Loop through all the vouchers to count how many active vouches there
        // are that are greater than 0. Vouch is the min of stake and trust
        for (uint256 i = 0; i < vouchersLength; i++) {

```



## Impact
1- The user couldn’t  get any more `vouching`
2- The user will be not able to `borrow()` or `repayBorrow()`
3- No one can in invoke`registerMember()` successfully for a specific user 

## Code Snippet
```solidity
   vouchers[borrower].push(Vouch(staker, trustAmount, 0, 0));
```
https://github.com/sherlock-audit/2022-10-union-finance/blob/main/union-v2-contracts/contracts/user/UserManager.sol#L555

```solidity
    for (uint256 i = 0; i < vouchers[borrower].length; i++) {
```
https://github.com/sherlock-audit/2022-10-union-finance/blob/main/union-v2-contracts/contracts/user/UserManager.sol#L807

```solidity
           uint256 vouchersLength = vouchers[newMember].length;

        // Loop through all the vouchers to count how many active vouches there
        // are that are greater than 0. Vouch is the min of stake and trust
        for (uint256 i = 0; i < vouchersLength; i++) {

```
https://github.com/sherlock-audit/2022-10-union-finance/blob/main/union-v2-contracts/contracts/user/UserManager.sol#L637-L641



## Tool used

Manual Review

## Recommendation
Add check for `trustAmount == 0`

## Discussion

**dmitriia**

Some minimal `trustAmount` looks to be needed here as the same can be repeated with dust amounts (say 1 wei, as the attacker pays gas anyway, so financially it will not matter).

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Union Finance |
| Report Date | N/A |
| Finders | Ch\_301, ctf\_sec |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-10-union-finance-judging/issues/69
- **Contest**: https://app.sherlock.xyz/audits/contests/11

### Keywords for Search

`vulnerability`

