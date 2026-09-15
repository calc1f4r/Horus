---
# Core Classification
protocol: Tessera
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43292
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-12-tessera
source_link: https://code4rena.com/reports/2022-12-tessera
github_link: https://github.com/code-423n4/2022-12-tessera-findings/issues/40

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
  - cross_chain
  - synthetics
  - privacy

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Trust
---

## Vulnerability Title

[M-07] Loss of ETH for proposer when it is a contract that doesn't have fallback function.

### Overview


A function called `sendEthOrWeth()` is causing issues in the OptimisticListingSeaport code. This function is used in three different places and is supposed to send either ETH or WETH to a specified address. However, there is a problem with the implementation of this function that could result in the loss of funds for users. If the receiving address is a contract that does not have a fallback function, the transfer will fail and the WETH tokens will be stuck in the contract. This could lead to financial losses for users who interact with the OptimisticListingSeaport using proposals. To mitigate this issue, the developers are advised to enforce that the receiving address is an EOA or to take in a recipient address for ETH transfers. The severity of this issue is debated among the judges, but it is agreed that it could potentially cause financial losses for users. 

### Original Finding Content


`sendEthOrWeth()` is used in several locations in OptimisticListingSeaport:

1.  rejectProposal - sent to proposer
2.  rejectActive - sent to proposer
3.  cash - sent to msg.sender

This is the implementation of sendEthOrWeth:

    function _attemptETHTransfer(address _to, uint256 _value) internal returns (bool success) {
        // Here increase the gas limit a reasonable amount above the default, and try
        // to send ETH to the recipient.
        // NOTE: This might allow the recipient to attempt a limited reentrancy attack.
        (success, ) = _to.call{value: _value, gas: 30000}("");
    }
    /// @notice Sends eth or weth to an address
    /// @param _to Address to send to
    /// @param _value Amount to send
    function _sendEthOrWeth(address _to, uint256 _value) internal {
        if (!_attemptETHTransfer(_to, _value)) {
            WETH(WETH_ADDRESS).deposit{value: _value}();
            WETH(WETH_ADDRESS).transfer(_to, _value);
        }
    }

The issue is that the receive could be a contract that does not have a fallback function. In this scenario, \_attemptETHTransfer will fail and WETH would be transferred to the contract. It is likely that it bricks those funds for the contract as there is no reason it would support interaction with WETH tokens.

It can be reasonably assumed that developers will develop contracts which will interact with OptimisticListingSeaport using proposals. They are not warned and are likely to suffer losses.

### Impact

Loss of ETH for proposer when it is a contract that doesn't have fallback function.

### Recommended Mitigation Steps

Either enforce that proposer is an EOA or take in a recipient address for ETH transfers.

**[HickupHH3 (judge) commented](https://github.com/code-423n4/2022-12-tessera-findings/issues/40#issuecomment-1378996495):**
 > The argument here is about the contract being able to handle ETH but not WETH. If the ETH transfer fails (eg. gas used exceeds the 30k sent), then funds would be stuck.
> 
> On the fence regarding severity here.

**[stevennevins (Tessera) confirmed, but disagreed with severity and commented](https://github.com/code-423n4/2022-12-tessera-findings/issues/40#issuecomment-1381978554):**
 > I actually more agree with this being an issue:
> > The argument here is about the contract being able to handle ETH but not WETH. If the ETH transfer fails (eg. gas used exceeds the 30k sent), then funds would be stuck.
> 
> But it's not clear to me that is what was originally highlighted in the description of the issue.

**[HickupHH3 (judge) commented](https://github.com/code-423n4/2022-12-tessera-findings/issues/40#issuecomment-1382004749):**
 > Yeah it's not fully clear because the premise is the contract not having a fallback function, but the intended effect of not being able to handle WETH is.
> > It is likely that it bricks those funds for the contract as there is no reason it would support interaction with WETH tokens.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Tessera |
| Report Date | N/A |
| Finders | Trust |

### Source Links

- **Source**: https://code4rena.com/reports/2022-12-tessera
- **GitHub**: https://github.com/code-423n4/2022-12-tessera-findings/issues/40
- **Contest**: https://code4rena.com/reports/2022-12-tessera

### Keywords for Search

`vulnerability`

