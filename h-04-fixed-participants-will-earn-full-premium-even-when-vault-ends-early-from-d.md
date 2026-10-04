---
# Core Classification
protocol: Saffron
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31510
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Saffron-security-review.md
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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[H-04] Fixed participants will earn full premium even when vault ends early from debt settlement

### Overview


The report describes a bug in a code that can allow an admin to steal premium from variable participants in a vault. This happens when the admin settles the debt before the full vault duration, which ends the vault early and allows all participants to withdraw their deposits. However, fixed participants are not required to pay back the partial premium based on the remaining time, allowing them to withdraw both their initial deposits and the full premium even when the vault ended early. This can result in a loss for variable participants, and a malicious admin can exploit this to earn the full premium. The report recommends deducting the premium from the admin's earnings when settling the debt early.

### Original Finding Content

**Severity**

**Impact:** High, premium can be stolen from variable participants

**Likelihood:** Medium, occurs when admin settles debt

**Description**

When `adminSettleDebt()` is called before the full vault duration, it will end the vault early, allowing all participants to withdraw their deposits.

In that scenario, the debt will be settled with a positive staking earnings, to ensure that variable participants can withdraw both earnings and part of the fixed premium based on the early vault end time.

The problem is, fixed participants do not pay back the partial premium based on remaining time (not in vault), allowing them to withdraw both full initial deposits and full fixed premium even when vault ended early. This is due to missing calculation in `vaultEndedWithdraw()` to return the partial premium, as shown below.

So variable participants will incur a loss as they are not paid back the partial premium.

Furthermore, a malicious admin can exploit this and earn the full premium by depositing and withdrawing as a fixed participant.

```Solidity
  function vaultEndedWithdraw(uint256 side) internal {
    ...

    // have to call finalizeVaultEndedWithdrawals first
    require(vaultEndedWithdrawalsFinalized, "WNF");

    if (side == FIXED) {
      require(
        fixedToVaultOngoingWithdrawalRequestIds[msg.sender].requestIds.length == 0 &&
          fixedToVaultNotStartedWithdrawalRequestIds[msg.sender].length == 0,
        "WAR"
      );

      uint256 sendAmount = fixedToPendingWithdrawalAmount[msg.sender];

      // they submitted a withdraw before the vault had ended and the vault ending should have claimed it
      if (sendAmount > 0) {
        delete fixedToPendingWithdrawalAmount[msg.sender];
      } else {
        uint256 bearerBalance = fixedBearerToken.balanceOf(msg.sender);
        require(bearerBalance > 0, "NBT");

        //@audit fixed participants will obtain the full deposit as vaultEndedFixedDepositsFunds
        //        will be equal to fixedETHDepositToken.totalSupply() when debt is settled with positive earnings
        sendAmount = fixedBearerToken.balanceOf(msg.sender).mulDiv(
          vaultEndedFixedDepositsFunds,
          fixedLidoSharesTotalSupply()
        );

        fixedBearerToken.burn(msg.sender, bearerBalance);
        fixedETHDepositToken.burn(msg.sender, fixedETHDepositToken.balanceOf(msg.sender));
        vaultEndedFixedDepositsFunds -= sendAmount;
      }

      sendFunds(sendAmount);

      emit FixedFundsWithdrawn(sendAmount, msg.sender, isStarted(), true);
      return;
    } else {
```

**Recommendations**

When admin settle debt ends the vault early, deduct `vaultEndedFixedDepositsFunds` by the amount of premium to be returned to variable participants as part of `feeEarnings`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Saffron |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Saffron-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

