---
# Core Classification
protocol: Renzo
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33504
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-04-renzo
source_link: https://code4rena.com/reports/2024-04-renzo
github_link: https://github.com/code-423n4/2024-04-renzo-findings/issues/198

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
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 47
finders:
  - bill
  - josephdara
  - mussucal
  - inzinko
  - 0xAadi
---

## Vulnerability Title

[M-09] Deposits will always revert if the amount being deposited is less than the `bufferToFill` value

### Overview


The `deposit` function in the `RestakeManager` contract allows users to deposit ERC20 tokens into the protocol. However, there is a bug where if the deposited amount is less than a certain value, the full amount will be used to fill a withdrawal buffer, leaving the amount value as zero. This causes the function to revert when it tries to approve and call the `deposit` function on the operator delegator. This can happen frequently depending on the set amount for the withdrawal buffer. To fix this issue, the `deposit` function can be modified to only approve and call the `deposit` function on the operator delegator if the deposited amount is greater than zero. The bug has been confirmed and mitigated by the Renzo team.

### Original Finding Content


The [`deposit`](https://github.com/code-423n4/2024-04-renzo/blob/1c7cc4e632564349b204b4b5e5f494c9b0bc631d/contracts/RestakeManager.sol#L491) function in the `RestakeManager` contract enables users to deposit ERC20 whitelisted collateral tokens into the protocol. It first checks the withdrawal buffer and fills it up using some or all of the deposited amount if it is below the buffer target. The remaining amount is then transferred to the operator delegator and deposited into EigenLayer.

The current issue with this implementation is that if the amount deposited is less than `bufferToFill`, the full amount will be used to fill the withdrawal buffer, leaving the amount value as zero.

```solidity
    function deposit(IERC20 _collateralToken, uint256 _amount, uint256 _referralId) public nonReentrant notPaused {
        // Verify collateral token is in the list - call will revert if not found
        uint256 tokenIndex = getCollateralTokenIndex(_collateralToken);
	...

        // Check the withdraw buffer and fill if below buffer target
        uint256 bufferToFill = depositQueue.withdrawQueue().getBufferDeficit(address(_collateralToken));
        if (bufferToFill > 0) {
            bufferToFill = (_amount <= bufferToFill) ? _amount : bufferToFill;
            // update amount to send to the operator Delegator
            _amount -= bufferToFill;

            // safe Approve for depositQueue
            _collateralToken.safeApprove(address(depositQueue), bufferToFill);

            // fill Withdraw Buffer via depositQueue
            depositQueue.fillERC20withdrawBuffer(address(_collateralToken), bufferToFill);
        }

        // Approve the tokens to the operator delegator
        _collateralToken.safeApprove(address(operatorDelegator), _amount);

        // Call deposit on the operator delegator
        operatorDelegator.deposit(_collateralToken, _amount);
        ...
    }
```

Subsequently, the function will approve the zero amount to the operator delegator and call `deposit` on the operator delegator. However, as seen in the `OperatorDelegator` contract's [`deposit`](https://github.com/code-423n4/2024-04-renzo/blob/1c7cc4e632564349b204b4b5e5f494c9b0bc631d/contracts/Delegation/OperatorDelegator.sol#L143) function below, a zero deposit will be reverted.

```solidity
    function deposit(IERC20 token, uint256 tokenAmount)
        external
        nonReentrant
        onlyRestakeManager
        returns (uint256 shares)
    {
        if (address(tokenStrategyMapping[token]) == address(0x0) || tokenAmount == 0) {
            revert InvalidZeroInput();
        }

        // Move the tokens into this contract
        token.safeTransferFrom(msg.sender, address(this), tokenAmount);

        return _deposit(token, tokenAmount);
    }
```

### Impact

Severity: Medium. User deposits will always revert if the amount being deposited is less than the `bufferToFill` value.

Likelihood: High. Depending on the set amount for the withdrawal buffer, this could be a common occurrence.

### Recommendation

To address this issue, the `deposit` function can be modified to only approve the amount to the operator delegator and call `deposit` on the operator delegator if the amount is greater than zero.

```solidity
    function deposit(IERC20 _collateralToken, uint256 _amount, uint256 _referralId) public nonReentrant notPaused {
        // Verify collateral token is in the list - call will revert if not found
        uint256 tokenIndex = getCollateralTokenIndex(_collateralToken);
	...
        // Check the withdraw buffer and fill if below buffer target
        uint256 bufferToFill = depositQueue.withdrawQueue().getBufferDeficit(address(_collateralToken));
        if (bufferToFill > 0) {
            bufferToFill = (_amount <= bufferToFill) ? _amount : bufferToFill;
            // update amount to send to the operator Delegator
            _amount -= bufferToFill;

            // safe Approve for depositQueue
            _collateralToken.safeApprove(address(depositQueue), bufferToFill);

            // fill Withdraw Buffer via depositQueue
            depositQueue.fillERC20withdrawBuffer(address(_collateralToken), bufferToFill);
        }
	if (_amount > 0) { // ADD HERE
            // Transfer the tokens to the operator delegator
            _collateralToken.safeApprove(address(operatorDelegator), _amount);

            // Call deposit on the operator delegator
            operatorDelegator.deposit(_collateralToken, _amount);
        }
        ...
    }
```

**[jatinj615 (Renzo) confirmed](https://github.com/code-423n4/2024-04-renzo-findings/issues/198#event-12916118847)**

**[Renzo mitigated](https://github.com/code-423n4/2024-06-renzo-mitigation?tab=readme-ov-file#scope)**

**Status:** Mitigation confirmed. Full details in reports from [0xCiphky](https://github.com/code-423n4/2024-06-renzo-mitigation-findings/issues/14), [grearlake](https://github.com/code-423n4/2024-06-renzo-mitigation-findings/issues/53), [Fassi\_Security](https://github.com/code-423n4/2024-06-renzo-mitigation-findings/issues/46), [LessDupes](https://github.com/code-423n4/2024-06-renzo-mitigation-findings/issues/31), and [Bauchibred](https://github.com/code-423n4/2024-06-renzo-mitigation-findings/issues/26).



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Renzo |
| Report Date | N/A |
| Finders | bill, josephdara, mussucal, inzinko, 0xAadi, kennedy1030, gesha17, 14si2o\_Flint, Tendency, SBSecurity, fyamf, RamenPeople, BiasedMerc, Neon2835, zzykxx, carrotsmuggler, ZanyBonzy, kinda\_very\_good, KupiaSec, mt030d, MaslarovK, tapir, 0x007, m\_Rassska, underdog, ADM, DanielArmstrong, blutorque, Aamir, 0rpse, Aymen0909, gumgumzum, adam-idarrha, jokr, araj, FastChecker, cu5t0mpeo, Shaheen, xg, baz1ka, b0g0, hunter\_w3b, 0xCiphky, Fassi\_Security, bigtone, lanrebayode77, LessDupes |

### Source Links

- **Source**: https://code4rena.com/reports/2024-04-renzo
- **GitHub**: https://github.com/code-423n4/2024-04-renzo-findings/issues/198
- **Contest**: https://code4rena.com/reports/2024-04-renzo

### Keywords for Search

`vulnerability`

