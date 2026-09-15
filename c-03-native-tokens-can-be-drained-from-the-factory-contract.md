---
# Core Classification
protocol: StationX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41384
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/StationX-security-review.md
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

[C-03] Native tokens can be drained from the Factory contract

### Overview


This bug report discusses a vulnerability in the Factory contract that allows an attacker to steal all native tokens. This is a high severity issue as it can result in the loss of valuable assets. The likelihood of this attack is also high as it can be carried out by any user.

The vulnerability lies in the `crossChainBuy()` function, specifically in the calculation of `value: msg.value - fees`. The error allows an attacker to send a LayerZero message with a higher value than intended and receive a refund for the excess amount. This means that the protocol fees, which should remain in the Factory contract until claimed by the protocol owner, can be stolen by the attacker.

The report also mentions that the native tokens deposited are sent to the Safe/DAO, while a fee is sent to the DAO owner. This is done by the Factory contract and can also be exploited by an attacker to create a fake DAO and receive these funds.

To fix this issue, the report recommends correctly calculating the remaining `value` to send to LayerZero, taking into account factors such as the deposit token, deposit amount, owner share, deposit fees, and KYC fees. This will ensure that the correct amount of native tokens is sent to LayerZero and prevent the theft of assets.

### Original Finding Content

## Severity

**Impact:** High. Stolen assets.

**Likelihood:** High. Any user can do it.

## Description

An adversary can perform an attack to steal all native tokens from the Factory contract by exploiting an error in the `crossChainBuy()` function.

Here's a simplified version of the error. It's present on the `value: msg.value - fees` calculation:

```solidity
    function crossChainBuy(...) {
        _buyGovernanceTokenERC20DAO(_daoAddress, _numOfTokensToBuy);

        fees = ((depositFees * platformFeeMultiplier) / 100);
@>      ICommLayer(_commLayer).sendMsg{value: msg.value - fees}(_commLayer, _payload, _extraParams);
    }
```

`sendMsg()` will send a LayerZero message with `value = msg.value - fees` and will refund the excess amount to an address provided by the user inside `_extraParams`.

Let's say that `msg.value = 10 ETH`, `fees = 0.1 ETH` and the LayerZero message requires another 0.1 ETH. So, LayerZero will receive 9.9 ETH and refund the amount not used. The user's final balance would be 9.8 ETH.

Note how the protocol fees stay in the Factory contract. This also happens for DAO deployments. Native token fees will remain in the contract until the protocol owner claims them. These are the tokens that can be stolen.

Notice how in `_buyGovernanceTokenERC20DAO()` (and the ERC721 function) the native tokens deposited are sent to the Safe/DAO, while some fee is sent to the DAO owner:

```solidity
    function _buyGovernanceTokenERC20DAO(...) {
        uint256 ownerShare = (_totalAmount * _daoDetails.ownerFeePerDepositPercent) / (FLOAT_HANDLER_TEN_4);

        if (_daoDetails.depositTokenAddress == NATIVE_TOKEN_ADDRESS) {
            checkDepositFeesSent(_daoAddress, _totalAmount + ownerShare);
@>          payable(_daoDetails.assetsStoredOnGnosis ? _daoDetails.gnosisAddress : _daoAddress).call{
                value: _totalAmount
            }("");

            payable(
                ccDetails[_daoAddress].ownerAddress != address(0)
                    ? ccDetails[_daoAddress].ownerAddress
                    : IERC20DAO(_daoAddress).getERC20DAOdetails().ownerAddress
@>          ).call{value: ownerShare}("");
        }
    }
```

These funds are sent from the Factory because it validates that the `msg.value` provided is enough to cover them all via `checkDepositFeesSent()`.

As an example, let's consider the deposited amount is 9 ETH, and the fees are 0.1 ETH. So 9.1 ETH will be transferred to the DAO/Safe/DAO owner. An adversary can even create a fake DAO to receive this.

Remember that as long as the contract has enough funds, it will also send the previously mentioned `value = msg.value - fees` to LayerZero, and finally refund the excess to the user (in our example 9.8 ETH).

So basically, the Factory contract is supplying the necessary native tokens for cross-chain deposits.

## Recommendations

Calculate the remaining `value` correctly to send to LayerZero, considering if the deposit token is the native one, the deposit amount, the owner share, the deposit fees, and the KYC fees.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | StationX |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/StationX-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

