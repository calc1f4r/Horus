---
# Core Classification
protocol: Tapioca
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31063
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/170
source_link: none
github_link: https://github.com/sherlock-audit/2024-02-tapioca-judging/issues/102

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
  - bin2chen
---

## Vulnerability Title

H-9: exerciseOptionsReceiver() Lack of Ownership Check for oTAP, Allowing Anyone to Use oTAPTokenID

### Overview


The report discusses a bug found by bin2chen in the exerciseOptionsReceiver() method of the Tapioca judging contract. This bug allows anyone to use the oTAPTokenID without proper authorization. The vulnerability is caused by the lack of ownership checks for the oTAPTokenID, which can be exploited by front-running the execution of the exerciseOptionsReceiver() function. This can be done by using a signature from the owner of the oTAPTokenID or by obtaining approval for the token. This allows malicious users to gain access to the oTAPTokenID and use it without proper authorization. The report recommends adding a check to ensure that the owner of the oTAPTokenID is the one executing the exerciseOptionsReceiver() function. The protocol team has already fixed this issue in their code. 

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-02-tapioca-judging/issues/102 

## Found by 
bin2chen
## Summary
In `UsdoOptionReceiverModule.exerciseOptionsReceiver()`:
For this method to execute successfully, the `owner` of the `oTAPTokenID` needs to approve it to `address(usdo)`.
Once approved, anyone can front-run execute `exerciseOptionsReceiver()` and utilize this authorization.

## Vulnerability Detail
In `USDO.lzCompose()`, it is possible to specify `_msgType == MSG_TAP_EXERCISE` to execute `USDO.exerciseOptionsReceiver()` across chains.

```solidity
    function exerciseOptionsReceiver(address srcChainSender, bytes memory _data) public payable {
...
            ITapiocaOptionBroker(_options.target).exerciseOption(
@>              _options.oTAPTokenID,
                address(this), //payment token
                _options.tapAmount
            );
            _approve(address(this), address(pearlmit), 0);
            uint256 bAfter = balanceOf(address(this));

            // Refund if less was used.
            if (bBefore > bAfter) {
                uint256 diff = bBefore - bAfter;
                if (diff < _options.paymentTokenAmount) {
                    IERC20(address(this)).safeTransfer(_options.from, _options.paymentTokenAmount - diff);
                }
            }
...
```
For this method to succeed, USDO must first obtain approve for the `oTAPTokenID`.

Example: The owner of `oTAPTokenID` is Alice.
1. alice in A chain execute lzSend(dstEid = B)  with
    - composeMsg = [oTAP.permit(usdo,oTAPTokenID,v,r,s) 2.exerciseOptionsReceiver(oTAPTokenID,_options.from=alice) 3. oTAP.revokePermit(oTAPTokenID)]
2. in chain B USDO.lzCompose() will 
   - execute oTAP.permit(usdo,oTAPTokenID)
   - exerciseOptionsReceiver(srcChainSender=alice,_options.from=alice,oTAPTokenID ) 
   - oTAP.revokePermit(oTAPTokenID)
   
The signature of `oTAP.permit` is public, allowing anyone to use it. 
>Note: if alice call approve(oTAPTokenID,usdo) in chain B  without signature, but The same result

This opens up the possibility for malicious users to front-run use this signature. 
Let's consider an example with Bob:
1. Bob in Chain A uses Alice's signature (v, r, s):
    - `composeMsg = [oTAP.permit(usdo, oTAPTokenID, v, r, s), exerciseOptionsReceiver(oTAPTokenID, _options.from=bob)]`-----> (Note: `_options.from` should be set to Bob.)
2. In Chain B, when executing `USDO.lzCompose(dstEid = B)`, the following actions occur:
    - Execute `oTAP.permit(usdo, oTAPTokenID)`
    - Execute `exerciseOptionsReceiver(srcChainSender=bob, _options.from=bob, oTAPTokenID)`

As a result, Bob gains unconditional access to this `oTAPTokenID`.

It is advisable to check the ownership of `oTAPTokenID` is `_options.from` before executing `ITapiocaOptionBroker(_options.target).exerciseOption()`.

## Impact

The `exerciseOptionsReceiver()` function lacks ownership checks for `oTAP`, allowing anyone to use `oTAPTokenID`.

## Code Snippet
https://github.com/sherlock-audit/2024-02-tapioca/blob/main/Tapioca-bar/contracts/usdo/modules/UsdoOptionReceiverModule.sol#L67
## Tool used

Manual Review

## Recommendation

add check `_options.from` is owner or be approved

```diff
    function exerciseOptionsReceiver(address srcChainSender, bytes memory _data) public payable {

...
            uint256 bBefore = balanceOf(address(this));
+           address oTap = ITapiocaOptionBroker(_options.target).oTAP();
+           address oTapOwner = IERC721(oTap).ownerOf(_options.oTAPTokenID);
+           require(oTapOwner == _options.from
+                         || IERC721(oTap).isApprovedForAll(oTapOwner,_options.from)
+                         || IERC721(oTap).getApproved(_options.oTAPTokenID) == _options.from
+                        ,"invalid");
            ITapiocaOptionBroker(_options.target).exerciseOption(
                _options.oTAPTokenID,
                address(this), //payment token
                _options.tapAmount
            );
            _approve(address(this), address(pearlmit), 0);
            uint256 bAfter = balanceOf(address(this));

            // Refund if less was used.
            if (bBefore > bAfter) {
                uint256 diff = bBefore - bAfter;
                if (diff < _options.paymentTokenAmount) {
                    IERC20(address(this)).safeTransfer(_options.from, _options.paymentTokenAmount - diff);
                }
            }
        }
```



## Discussion

**sherlock-admin4**

The protocol team fixed this issue in PR/commit https://github.com/Tapioca-DAO/Tapioca-bar/pull/360; https://github.com/Tapioca-DAO/TapiocaZ/pull/182.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Tapioca |
| Report Date | N/A |
| Finders | bin2chen |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-02-tapioca-judging/issues/102
- **Contest**: https://app.sherlock.xyz/audits/contests/170

### Keywords for Search

`vulnerability`

