---
# Core Classification
protocol: LayerZeroZROClaim
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37813
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/LayerZeroZROClaim-security-review.md
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

[C-02] Remote donations are stuck

### Overview


The bug report is about a high severity issue in a function called `withdrawDonation` that allows users to donate on non-Ethereum chains and withdraw their donations on the Ethereum chain. The issue is that the function is assigning the value of `donationAmount` to `address(this).balance`, which includes the fee for the cross-chain transfer. This causes the transfer to fail and the donations to be stuck in the contract. The recommendation is to subtract the fee from the `donationAmount` calculation to ensure the transfer is successful.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** High

## Description

Users interact with `RemoteDonate` to perform donations on non-Ethereum chains. And the donation will be withdrawn remotely to the `donationReceiver` on Ethereum chain via Stargate cross-chain transfer.

Due to the cross-chain transfer, an LZ fee is required to be paid via `msg.value` while transferring the `donationAmount` to Ethereum chain.

The issue is that `donationAmount` is assigned the value of `address(this).balance` , which actually includes the `msg.value` meant for the transfer across chain.

That will cause the `IOFT(stargate).send{ value: msg.value + donationAmountNative }` to fail as it is sending more than `address(this).balance`.

The impact of this is that withdrawals for remote donations will always fail, causing them to be stuck within the contract.

```Solidity
    function withdrawDonation(Currency _currency, uint256 _minAmount) external payable {
        address stargate;
        uint256 donationAmount;
        uint256 donationAmountNative;

        if (_currency == Currency.USDC && stargateUsdc != address(0)) {
            stargate = stargateUsdc;
            donationAmount = tokenUsdc.balanceOf(address(this));
        } else if (_currency == Currency.USDT && stargateUsdt != address(0)) {
            stargate = stargateUsdt;
            donationAmount = tokenUsdt.balanceOf(address(this));
        } else if (_currency == Currency.Native && stargateNative != address(0)) {
            stargate = stargateNative;
        //@audit this would have included the LZ fee (msg.value) as well
>>>         donationAmount = address(this).balance;
            donationAmountNative = donationAmount;
        } else {
            revert UnsupportedCurrency(_currency);
        }//ok

        // sends via taxi
        bytes memory emptyBytes = new bytes(0);
        SendParam memory sendParams = SendParam({
            dstEid: remoteEid, // only send to ethereum
            to: bytes32(uint256(uint160(donationReceiver))),
            amountLD: donationAmount,
            minAmountLD: _minAmount,
            extraOptions: emptyBytes,
            composeMsg: emptyBytes,
            oftCmd: emptyBytes // type taxi
        });//ok

        // combine the msg value in addition to the donation amount
        // in non native currencies this will just be 0
        // solhint-disable-next-line check-send-result

       //@audit this will always fail since it is sending more than address(this).balance
 >>>    IOFT(stargate).send{ value: msg.value + donationAmountNative }(
            sendParams,
            MessagingFee(msg.value, 0),
            msg.sender // refund any excess native to the sender
        );

        emit DonationWithdrawn(_currency, donationReceiver, donationAmount);
    }
```

## Recommendations

Make the following change to calculate the actual donation amount for transfer.

```diff
        } else if (_currency == Currency.Native && stargateNative != address(0)) {
            stargate = stargateNative;
-            donationAmount = address(this).balance;
+            donationAmount = address(this).balance - msg.value;
            donationAmountNative = donationAmount;
        } else {
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | LayerZeroZROClaim |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/LayerZeroZROClaim-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

