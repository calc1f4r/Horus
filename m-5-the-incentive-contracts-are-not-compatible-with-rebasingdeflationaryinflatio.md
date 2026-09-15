---
# Core Classification
protocol: Boost Account AA Wallet
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41041
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/426
source_link: none
github_link: https://github.com/sherlock-audit/2024-06-boost-aa-wallet-judging/issues/460

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
finders_count: 8
finders:
  - ZanyBonzy
  - 0xdeadbeef
  - ge6a
  - denzi\_
  - 0xNirix
---

## Vulnerability Title

M-5: The incentive contracts are not compatible with rebasing/deflationary/inflationary tokens

### Overview


This bug report discusses an issue with the incentive contracts used in the Boost Protocol. The contracts are not compatible with rebasing, deflationary, or inflationary tokens. This means that the balances in the contracts can become outdated and cause problems for all parties involved. The issue can lead to denial of service when balances are rebased. The report includes code snippets and recommends tracking balances after each transfer to keep the data updated. The bug was found through a manual review by a group of individuals.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-06-boost-aa-wallet-judging/issues/460 

## Found by 
0xNirix, 0xbranded, 0xdeadbeef, Atharv, ZanyBonzy, denzi\_, ge6a, haxagon
## Summary

The protocol wants to work with all kind of tokens including rebasing tokens. From 
[weirdERC20](https://github.com/d-xo/weird-erc20/tree/main) we can read more about Balance Modfications Outisde of Transfers (rebasing/airdrops) section which states

> Some tokens may make arbitrary balance modifications outside of transfers (e.g. Ampleforth style rebasing tokens, Compound style airdrops of governance tokens, mintable/burnable tokens).

> Some smart contract systems cache token balances (e.g. Balancer, Uniswap-V2), and arbitrary modifications to underlying balances can mean that the contract is operating with outdated information.

## Vulnerability Detail

One such example of not supporting in the code is the `ERC20Incentive::clawback()` function

```solidity
function clawback(bytes calldata data_) external override onlyOwner returns (bool) {
        ClawbackPayload memory claim_ = abi.decode(data_, (ClawbackPayload));
        (uint256 amount) = abi.decode(claim_.data, (uint256));

        if (strategy == Strategy.RAFFLE) {
            // Ensure the amount is the full reward and there are no raffle entries, then reset the limit
            if (amount != reward || claims > 0) revert BoostError.ClaimFailed(msg.sender, abi.encode(claim_));
            limit = 0;
        } else {
            // Ensure the amount is a multiple of the reward and reduce the max claims accordingly
            if (amount % reward != 0) revert BoostError.ClaimFailed(msg.sender, abi.encode(claim_));
            limit -= amount / reward;
        }
```

The variable `reward` is being used in these if conditions, reward is set during initialization of the contract. It is either set as the full amount for raffles or the amount of reward per person for pools.

Lets consider the raffle situation for this report.

In the `initialize()` function, suppose that the reward amount in the data is sent as `10e18`, this is set as reward for the raffle after confirming by checking the balance of the contract.

Now suppose after some time the balance has changed due to rebasing. The reward variable is still 10e18 but the actual balance of the contract is different.

In the `clawback()` function, the owner wants to withdraw the full amount of the raffle. If they provide the rebased balance of the contract, the function will revert due to the following if condition

```solidity
if (amount != reward || claims > 0) revert BoostError.ClaimFailed(msg.sender, abi.encode(claim_));
```

If they provide 10e18 as amount which was the original amount and the current balance of the contract is lower then the following line will cause a revert

```solidity
asset.safeTransfer(claim_.target, amount);
```

This is only one instance of an issue, these issues are present in the Incentive contracts which use ERC20s.

Similarly `ERC20Incentive::drawRaffle()` will also not work if the actual balance of the contract has changed to a lower amount.


## Impact

The balances are outdated and will cause hindrances for all parties involved. Denial of Service when the balances rebase. 

## Code Snippet

[ERC20VariableIncentive.sol](https://github.com/sherlock-audit/2024-06-boost-aa-wallet/blob/main/boost-protocol/packages/evm/contracts/incentives/ERC20VariableIncentive.sol)

[ERC20Incentive.sol](https://github.com/sherlock-audit/2024-06-boost-aa-wallet/blob/main/boost-protocol/packages/evm/contracts/incentives/ERC20Incentive.sol#L1-L147)

[CGDAIncentive.sol](https://github.com/sherlock-audit/2024-06-boost-aa-wallet/blob/main/boost-protocol/packages/evm/contracts/incentives/CGDAIncentive.sol)

## Tool used

Manual Review

## Recommendation

Track the balances after each transfer in/out to keep updated data in the contracts.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Boost Account AA Wallet |
| Report Date | N/A |
| Finders | ZanyBonzy, 0xdeadbeef, ge6a, denzi\_, 0xNirix, haxagon, 0xbred, Atharv |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-06-boost-aa-wallet-judging/issues/460
- **Contest**: https://app.sherlock.xyz/audits/contests/426

### Keywords for Search

`vulnerability`

