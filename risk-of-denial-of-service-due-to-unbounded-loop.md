---
# Core Classification
protocol: NFTX Protocol v2
chain: everychain
category: dos
vulnerability_type: dos

# Attack Vector Details
attack_type: dos
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18162
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
  - dos

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Jaime Iglesias
  - Evan Sultanik
---

## Vulnerability Title

Risk of denial of service due to unbounded loop

### Overview


This bug report is about a Denial of Service (DoS) vulnerability in the NFTX protocol. When the protocol fees are distributed, the system loops through the list of beneficiaries (known as receivers) to send them the protocol fees they are entitled to. This loop is unbounded and the number of receivers can grow, making the amount of gas consumed also unbounded. This can cause the cost of executing the distribution operation to reach the block gas limit, making users unable to mint, redeem, or swap tokens. 

The NFTX team recommends short-term solutions such as examining the execution cost of the function to determine the safe bounds of the loop and, if possible, consider splitting the distribution operation into multiple calls. In the long-term, they suggest redesigning the fee distribution mechanism to avoid unbounded loops and prevent denials of service. For guidance on redesigning this mechanism, the NFTX team has included an Appendix D.

### Original Finding Content

## Diﬃculty: High

## Type: Denial of Service

### Description
When protocol fees are distributed, the system loops through the list of beneﬁciaries (known internally as receivers) to send them the protocol fees they are entitled to.

```solidity
function distribute(uint256 vaultId) external override virtual nonReentrant {
    require(nftxVaultFactory != address(0));
    address _vault = INFTXVaultFactory(nftxVaultFactory).vault(vaultId);
    uint256 tokenBalance = IERC20Upgradeable(_vault).balanceOf(address(this));
    if (distributionPaused || allocTotal == 0) {
        IERC20Upgradeable(_vault).safeTransfer(treasury, tokenBalance);
        return;
    }
    uint256 length = feeReceivers.length;
    uint256 leftover;
    for (uint256 i; i < length; ++i) {
        FeeReceiver memory _feeReceiver = feeReceivers[i];
        uint256 amountToSend = leftover + ((tokenBalance * _feeReceiver.allocPoint) / allocTotal);
        uint256 currentTokenBalance = IERC20Upgradeable(_vault).balanceOf(address(this));
        amountToSend = amountToSend > currentTokenBalance ? currentTokenBalance : amountToSend;
        bool complete = _sendForReceiver(_feeReceiver, vaultId, _vault, amountToSend);
        if (!complete) {
            uint256 remaining = IERC20Upgradeable(_vault).allowance(address(this), _feeReceiver.receiver);
            IERC20Upgradeable(_vault).safeApprove(_feeReceiver.receiver, 0);
            leftover = remaining;
        } else {
            leftover = 0;
        }
    }
    if (leftover != 0) {
        uint256 currentTokenBalance = IERC20Upgradeable(_vault).balanceOf(address(this));
        IERC20Upgradeable(_vault).safeTransfer(treasury, currentTokenBalance);
    }
}
```

_Figure 7.1: The distribute() function in NFTXSimpleFeeDistributor.sol_

Because this loop is unbounded and the number of receivers can grow, the amount of gas consumed is also unbounded.

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

_Figure 7.2: The _sendForReceiver() function in NFTXSimpleFeeDistributor.sol_

Additionally, if one of the receivers is a contract, code that significantly increases the gas cost of the fee distribution will execute (Figure 7.2).

It is important to note that fees are usually distributed within the context of user transactions (redeeming, minting, etc.), so the total cost of the distribution operation depends on the logic outside of the distribute() function.

### Exploit Scenario
The NFTX team adds a new feature that allows NFTX token holders who stake their tokens to register as receivers and gain a portion of protocol fees; because of that, the number of receivers grows dramatically. Due to the large number of receivers, the distribute() function cannot execute because the cost of executing it has reached the block gas limit. As a result, users are unable to mint, redeem, or swap tokens.

### Recommendations
Short term, examine the execution cost of the function to determine the safe bounds of the loop and, if possible, consider splitting the distribution operation into multiple calls.

Long term, consider redesigning the fee distribution mechanism to avoid unbounded loops and prevent denials of service. See appendix D for guidance on redesigning this mechanism.

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

`DOS`

