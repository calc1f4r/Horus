---
# Core Classification
protocol: Teller Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32388
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/295
source_link: none
github_link: https://github.com/sherlock-audit/2024-04-teller-finance-judging/issues/135

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
  - kennedy1030
  - KupiaSec
  - no
  - 0x73696d616f
  - EgisSecurity
---

## Vulnerability Title

M-11: Incorrect selector in `FlashRolloverLoan_G5::_acceptCommitment()` does not match `SmartCommitmentForwarder::acceptCommitmentWithRecipient()`

### Overview


The bug report discusses an issue in the code of a financial platform called Teller Finance. The problem is that a specific function called `FlashRolloverLoan_G5::_acceptCommitment()` is not working correctly for a type of loan called `LenderCommitmentGroup_Smart`. The issue was found by a group of security researchers and can cause the platform to not function properly for these types of loans. The report includes details on the code causing the problem and the impact it can have. The tool used to identify the issue was manual review using a code editor called Vscode. The recommendation is to fix the code by inserting the correct selector. The platform team has already addressed this issue in their code.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-04-teller-finance-judging/issues/135 

## Found by 
0x73696d616f, 0xadrii, EgisSecurity, KupiaSec, dirtymic, kennedy1030, merlin, no
## Summary

`FlashRolloverLoan_G5::_acceptCommitment()` allows picking the `SmartCommitmentForwarder`, but the selector is incorrect, making it unusable for `LenderCommitmentGroup_Smart`.

## Vulnerability Detail

`FlashRolloverLoan_G5::_acceptCommitment()` accepts the commitment to `SmartCommitmentForwarder` if `_commitmentArgs.smartCommitmentAddress != address(0)`. However, the selector used is `acceptSmartCommitmentWithRecipient()`, which does not match `SmartCommitmentForwarder::acceptCommitmentWithRecipient()`, DoSing the ability to rollover loans for `LenderCommitmentGroup_Smart`.

## Impact

`FlashRolloverLoan_G5` will not work for `LenderCommitmentGroup_Smart` loans.

## Code Snippet

[FlashRolloverLoan_G5::_acceptCommitment()](https://github.com/sherlock-audit/2024-04-teller-finance/blob/main/teller-protocol-v2-audit-2024/packages/contracts/contracts/LenderCommitmentForwarder/extensions/FlashRolloverLoan_G5.sol#L292)
```solidity
function _acceptCommitment(
    address lenderCommitmentForwarder,
    address borrower,
    address principalToken,
    AcceptCommitmentArgs memory _commitmentArgs
)
    internal
    virtual
    returns (uint256 bidId_, uint256 acceptCommitmentAmount_)
{
    uint256 fundsBeforeAcceptCommitment = IERC20Upgradeable(principalToken)
        .balanceOf(address(this));



    if (_commitmentArgs.smartCommitmentAddress != address(0)) {

            bytes memory responseData = address(lenderCommitmentForwarder)
                .functionCall(
                    abi.encodePacked(
                        abi.encodeWithSelector(
                            ISmartCommitmentForwarder
                                .acceptSmartCommitmentWithRecipient
                                .selector,
                            _commitmentArgs.smartCommitmentAddress,
                            _commitmentArgs.principalAmount,
                            _commitmentArgs.collateralAmount,
                            _commitmentArgs.collateralTokenId,
                            _commitmentArgs.collateralTokenAddress,
                            address(this),
                            _commitmentArgs.interestRate,
                            _commitmentArgs.loanDuration
                        ),
                        borrower //cant be msg.sender because of the flash flow
                    )
                );

            (bidId_) = abi.decode(responseData, (uint256));
        ... 
```

## Tool used

Manual Review

Vscode

## Recommendation

Insert the correct selector, `SmartCommitmentForwarder::acceptCommitmentWithRecipient()`.



## Discussion

**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/teller-protocol/teller-protocol-v2-audit-2024/pull/33

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Teller Finance |
| Report Date | N/A |
| Finders | kennedy1030, KupiaSec, no, 0x73696d616f, EgisSecurity, 0xadrii, merlin, dirtymic |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-04-teller-finance-judging/issues/135
- **Contest**: https://app.sherlock.xyz/audits/contests/295

### Keywords for Search

`vulnerability`

