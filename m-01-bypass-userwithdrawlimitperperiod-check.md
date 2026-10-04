---
# Core Classification
protocol: prePO
chain: everychain
category: uncategorized
vulnerability_type: bypass_limit

# Attack Vector Details
attack_type: bypass_limit
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6063
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-12-prepo-contest
source_link: https://code4rena.com/reports/2022-12-prepo
github_link: https://github.com/code-423n4/2022-12-prepo-findings/issues/49

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
  - bypass_limit

protocol_categories:
  - liquid_staking
  - cdp
  - services
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - csanuragjain
---

## Vulnerability Title

[M-01] Bypass `userWithdrawLimitPerPeriod` check

### Overview


This bug report is related to the WithdrawHook.sol contract located at https://github.com/prepo-io/prepo-monorepo/blob/feat/2022-12-prepo/apps/smart-contracts/core/contracts/WithdrawHook.sol#L70. It is possible for a user to bypass the userWithdrawLimitPerPeriod check by transferring balance to another account.

To demonstrate the bug, assume that userWithdrawLimitPerPeriod is set to 1000. User A has a current deposit of 2000 and wants to withdraw everything instantly. User A calls the withdraw function and takes out the 1000 amount. However, the remaining 1000 amount cannot be withdrawn since userWithdrawLimitPerPeriod is reached. User A can simply transfer his balance to his another account and withdraw from that account. Since the withdraw limit is tied to the account, this new account will be allowed to make a withdrawal, thus bypassing the userWithdrawLimitPerPeriod.

The recommended mitigation step for this bug is to only allow the user to transfer leftover limit. For example, if the user has already utilized limit X, then he should only be able to transfer userWithdrawLimitPerPeriod-X.

### Original Finding Content


User can bypass the `userWithdrawLimitPerPeriod` check by transferring the balance to another account.

### Proof of Concept

1.  Assume `userWithdrawLimitPerPeriod` is set to `1000`
2.  User A has current deposit of amount `2000` and wants to withdraw everything instantly
3.  User A calls the withdraw function and takes out the `1000` amount

<!---->

    function withdraw(uint256 _amount) external override nonReentrant {
        uint256 _baseTokenAmount = (_amount * baseTokenDenominator) / 1e18;
        uint256 _fee = (_baseTokenAmount * withdrawFee) / FEE_DENOMINATOR;
        if (withdrawFee > 0) { require(_fee > 0, "fee = 0"); }
        else { require(_baseTokenAmount > 0, "amount = 0"); }
        _burn(msg.sender, _amount);
        uint256 _baseTokenAmountAfterFee = _baseTokenAmount - _fee;
        if (address(withdrawHook) != address(0)) {
          baseToken.approve(address(withdrawHook), _fee);
          withdrawHook.hook(msg.sender, _baseTokenAmount, _baseTokenAmountAfterFee);
          baseToken.approve(address(withdrawHook), 0);
        }
        baseToken.transfer(msg.sender, _baseTokenAmountAfterFee);
        emit Withdraw(msg.sender, _baseTokenAmountAfterFee, _fee);
      }

4.  Remaining `1000` amount cannot be withdrawn since `userWithdrawLimitPerPeriod` is reached

<!---->

    function hook(
        address _sender,
        uint256 _amountBeforeFee,
        uint256 _amountAfterFee
      ) external override onlyCollateral {
    ...
    require(userToAmountWithdrawnThisPeriod[_sender] + _amountBeforeFee <= userWithdrawLimitPerPeriod, "user withdraw limit exceeded");
    ...
    }

5.  User simply transfers his balance to his other account and withdraw from that account

6.  Since withdraw limit is tied to account, this new account will be allowed to make withdrawal thus bypassing `userWithdrawLimitPerPeriod`

### Recommended Mitigation Steps

User should only be allowed to transfer leftover limit. For example if User already utilized limit X then he should only be able to transfer `userWithdrawLimitPerPeriod-X`.

**[ramenforbreakfast (prePO) confirmed](https://github.com/code-423n4/2022-12-prepo-findings/issues/49)** 

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | prePO |
| Report Date | N/A |
| Finders | csanuragjain |

### Source Links

- **Source**: https://code4rena.com/reports/2022-12-prepo
- **GitHub**: https://github.com/code-423n4/2022-12-prepo-findings/issues/49
- **Contest**: https://code4rena.com/contests/2022-12-prepo-contest

### Keywords for Search

`Bypass limit`

