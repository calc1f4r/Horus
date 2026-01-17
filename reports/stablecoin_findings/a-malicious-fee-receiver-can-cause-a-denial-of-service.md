---
# Core Classification
protocol: NFTX Protocol v2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18163
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/NFTX.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/NFTX.pdf
github_link: none

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
finders_count: 2
finders:
  - Jaime Iglesias
  - Evan Sultanik
---

## Vulnerability Title

A malicious fee receiver can cause a denial of service

### Overview


A bug report has been filed concerning the NFTXSimpleFeeDistributor contract in the NFTX protocol. Whenever a user executes a minting, redeeming, or swapping operation on a vault, a fee is charged to the user and is sent to the NFXTSimpleFeeDistributor contract for distribution. The distribution function loops through all fee receivers and sends them the number of tokens they are entitled to, but if the fee receiver is a contract, a special logic is executed. This allows the receiver to pull all the tokens from the NFXTSimpleFeeDistributor contract, which can cause a denial of service on the vaults calling the function.

The issue is of low difficulty because the addReceiver() function is owner-protected and, as indicated by the NFTX team, the owner is the NFTX DAO. It is assumed that a proposal is created and a certain quorum has to be met for it to be executed.

The exploit scenario is that Eve, a malicious receiver, sets up a smart contract that consumes all the gas forwarded to it when receiveRewards is called. This causes the distribute() function to run out of gas, resulting in a denial of service on the vaults.

To address this issue, short-term recommendations include changing the fee distribution mechanism so that only a token transfer is executed even if the receiver is a contract. Long-term recommendations suggest redesigning the fee distribution mechanism to prevent malicious fee receivers from causing a denial of service on the protocol. Guidance on redesigning this mechanism can be found in appendix D.

### Original Finding Content

## Difficulty: Low

## Type: Access Controls

## Description
Whenever a user executes a minting, redeeming, or swapping operation on a vault, a fee is charged to the user and is sent to the `NFXTSimpleFeeDistributor` contract for distribution. The distribution function loops through all fee receivers and sends them the number of tokens they are entitled to (see figure 7.1).

If the fee receiver is a contract, a special logic is executed; instead of receiving the corresponding number of tokens, the receiver pulls all the tokens from the `NFXTSimpleFeeDistributor` contract.

```solidity
function _sendForReceiver(FeeReceiver memory _receiver, uint256 _vaultId, address _vault, uint256 amountToSend) internal virtual returns (bool) {
    if (_receiver.isContract) {
        IERC20Upgradeable(_vault).safeIncreaseAllowance(_receiver.receiver, amountToSend);
        bytes memory payload = abi.encodeWithSelector(INFTXLPStaking.receiveRewards.selector, _vaultId, amountToSend);
        (bool success, ) = address(_receiver.receiver).call(payload);
        // If the allowance has not been spent, it means we can pass it forward to next.
        return success && IERC20Upgradeable(_vault).allowance(address(this), _receiver.receiver) == 0;
    } else {
        IERC20Upgradeable(_vault).safeTransfer(_receiver.receiver, amountToSend);
        return true;
    }
}
```

*Figure 8.1: The `_sendForReceiver()` function in `NFTXSimpleFeeDistributor.sol`*

In this case, because the receiver contract executes arbitrary logic and receives all of the gas, the receiver contract can spend all of it; as a result, only 1/64 of the original gas forwarded to the receiver contract would remain to continue executing the `distribute()` function (see EIP-150), which may not be enough to complete the execution, leading to a denial of service.

The issue is of high difficulty because the `addReceiver()` function is owner-protected and, as indicated by the NFTX team, the owner is the NFTX DAO. Because the DAO itself was out of scope for this review, we do not know what the process to become a receiver looks like. We assume that a proposal is created and a certain quorum has to be met for it to be executed.

## Exploit Scenario
Eve, a malicious receiver, sets up a smart contract that consumes all the gas forwarded to it when `receiveRewards` is called. As a result, the `distribute()` function runs out of gas, causing a denial of service on the vaults calling the function.

## Recommendations
Short term, change the fee distribution mechanism so that only a token transfer is executed even if the receiver is a contract.

Long term, consider redesigning the fee distribution mechanism to prevent malicious fee receivers from causing a denial of service on the protocol. See appendix D for guidance on redesigning this mechanism.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | NFTX Protocol v2 |
| Report Date | N/A |
| Finders | Jaime Iglesias, Evan Sultanik |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/NFTX.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/NFTX.pdf

### Keywords for Search

`vulnerability`

