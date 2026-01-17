---
# Core Classification
protocol: Folks Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61043
audit_firm: Immunefi
contest_link: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2033687%20-%20%5BSmart%20Contract%20-%20Medium%5D%20Loan%20creation%20can%20be%20frontrun%20preventing%20the%20users%20from%20creating%20loans.md
source_link: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2033687%20-%20%5BSmart%20Contract%20-%20Medium%5D%20Loan%20creation%20can%20be%20frontrun%20preventing%20the%20users%20from%20creating%20loans.md
github_link: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2033687%20-%20%5BSmart%20Contract%20-%20Medium%5D%20Loan%20creation%20can%20be%20frontrun%20preventing%20the%20users%20from%20creating%20loans.md

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
finders_count: 1
finders:
  - Kalogerone
---

## Vulnerability Title

Loan creation can be frontrun, preventing the users from creating loans

### Overview


This report is about a bug in a smart contract on the Snowtrace testnet. The bug allows an attacker to prevent users from creating loans by frontrunning their transactions. This is a type of attack called griefing, where the attacker causes damage to the users or the protocol without any profit motive. The bug is caused by the use of a user-selected loanId, which can be easily duplicated by an attacker. The bug is present in the SpokeCommon.sol, SpokeToken.sol, Hub.sol, and LoanManager.sol contracts. The recommendation is to use a counter instead of a user-selected loanId to prevent this type of attack. A proof of concept test is provided to demonstrate the bug. 

### Original Finding Content




Report type: Smart Contract


Target: https://testnet.snowtrace.io/address/0x2cAa1315bd676FbecABFC3195000c642f503f1C9

Impacts:
- Griefing (e.g. no profit motive for an attacker, but damage to the users or the protocol)

## Description
## Brief/Intro

A user who tries to create a loan has to choose the `loanId`. Any user can frontrun this transaction with the same `loanId`, making the initial user's transaction to revert because his selected `loanId` is taken.

## Vulnerability Details

Each loan has a unique `bytes32` identifier named `loanId`. During the loan creation, each user is asked to provide the `loanId` that his loan will have.

```javascript
SpokeCommon.sol

    function createLoan(
        Messages.MessageParams memory params,
        bytes32 accountId,
@>      bytes32 loanId,
        uint16 loanTypeId,
        bytes32 loanName
    ) external payable nonReentrant {
        _doOperation(params, Messages.Action.CreateLoan, accountId, abi.encodePacked(loanId, loanTypeId, loanName));
    }
```

```javascript
SpokeToken.sol

    function createLoanAndDeposit(
        Messages.MessageParams memory params,
        bytes32 accountId,
@>      bytes32 loanId,
        uint256 amount,
        uint16 loanTypeId,
        bytes32 loanName
    ) external payable nonReentrant {
        _doOperation(
            params,
            Messages.Action.CreateLoanAndDeposit,
            accountId,
            amount,
            abi.encodePacked(loanId, poolId, amount, loanTypeId, loanName)
        );
    }
```

This arbitrary `loanId` value is sent through a bridge to the `Hub.sol` contract which in turn calls the `createUserLoan` function is `LoanManager.sol`.

```javascript
Hub.sol

    function _receiveMessage(Messages.MessageReceived memory message) internal override {
        Messages.MessagePayload memory payload = Messages.decodeActionPayload(message.payload);
        .
        .
        .
        } else if (payload.action == Messages.Action.CreateLoan) {
            bytes32 loanId = payload.data.toBytes32(index);
            index += 32;
            uint16 loanTypeId = payload.data.toUint16(index);
            index += 2;
            bytes32 loanName = payload.data.toBytes32(index);

@>          loanManager.createUserLoan(loanId, payload.accountId, loanTypeId, loanName);
        } else if (payload.action == Messages.Action.DeleteLoan) {
            bytes32 loanId = payload.data.toBytes32(index);

            loanManager.deleteUserLoan(loanId, payload.accountId);
        } else if (payload.action == Messages.Action.CreateLoanAndDeposit) {
            bytes32 loanId = payload.data.toBytes32(index);
            index += 32;
            uint8 poolId = payload.data.toUint8(index);
            index += 1;
            uint256 amount = payload.data.toUint256(index);
            index += 32;
            uint16 loanTypeId = payload.data.toUint16(index);
            index += 2;
            bytes32 loanName = payload.data.toBytes32(index);

@>          loanManager.createUserLoan(loanId, payload.accountId, loanTypeId, loanName);
            loanManager.deposit(loanId, payload.accountId, poolId, amount);

            // save token received
            receiveToken = ReceiveToken({poolId: poolId, amount: amount});
        } else if (payload.action == Messages.Action.Deposit) {
        .
        .
        .
```

```javascript
LoanManager.sol

    function createUserLoan(
        bytes32 loanId,
        bytes32 accountId,
        uint16 loanTypeId,
        bytes32 loanName
    ) external override onlyRole(HUB_ROLE) nonReentrant {
        // check loan types exists, is not deprecated and no existing user loan for same loan id
        if (!isLoanTypeCreated(loanTypeId)) revert LoanTypeUnknown(loanTypeId);
        if (isLoanTypeDeprecated(loanTypeId)) revert LoanTypeDeprecated(loanTypeId);
@>      if (isUserLoanActive(loanId)) revert UserLoanAlreadyCreated(loanId);

        // create loan
        UserLoan storage userLoan = _userLoans[loanId];
        userLoan.isActive = true;
        userLoan.accountId = accountId;
        userLoan.loanTypeId = loanTypeId;

        emit CreateUserLoan(loanId, accountId, loanTypeId, loanName);
    }
```

At this point, if there is already a loan with the desired `loanId`, the transaction reverts. Upon a valid loan creation, a new `UserLoan` object is created and `UserLoan.isActive` is set to `true`.

```javascript
    function isUserLoanActive(bytes32 loanId) public view returns (bool) {
        return _userLoans[loanId].isActive;
    }
```

An attacker can take advantage of this and frontrun all the loan creation transactions (on the chains with a public mempool, like the `Ethereum mainnet`) and prevent all the users from creating loans.

## Impact Details

This is a griefing attack which prevents all users from creating loans. Every transaction will fail because the attacker can frontrun it with the same `loanId`.

## References

https://github.com/Folks-Finance/folks-finance-xchain-contracts/blob/main/contracts/spoke/SpokeCommon.sol#L115

https://github.com/Folks-Finance/folks-finance-xchain-contracts/blob/main/contracts/spoke/SpokeToken.sol#L46

https://github.com/Folks-Finance/folks-finance-xchain-contracts/blob/main/contracts/hub/Hub.sol#L186-L210

https://github.com/Folks-Finance/folks-finance-xchain-contracts/blob/main/contracts/hub/LoanManager.sol#L40

https://github.com/Folks-Finance/folks-finance-xchain-contracts/blob/main/contracts/hub/LoanManagerState.sol#L413

## Recommendation

Don't allow for the users to select their desired `loanId`. Use a counter internally and increment it with every loan creation and use it as the `loanId`.

        
## Proof of concept
## Proof of Concept

Let's follow this scenario:

1. Bob tries to create a loan with a random `loanId`
2. Alice (the attacker) sees this transaction in the mempool and frontruns bob transaction with the same `loanId`
3. Alice's transaction goes through
4. Bob's transaction gets reverted
5. Repeat

Paste the following test in the `test/hub/LoanManager.test.ts`:

```javascript
  describe("POCs", () => {
    it("Should test loanId frontrun", async () => {
      const { hub, loanManager } = await loadFixture(deployLoanManagerFixture);
      const { loanTypeId } = await loadFixture(addPoolsFixture);

      const loanId = getRandomBytes(BYTES32_LENGTH);
      const accountId1 = getAccountIdBytes("ACCOUNT_ID");
      const accountId2 = getAccountIdBytes("ACCOUNT_ID2");
      const loanName = getRandomBytes(BYTES32_LENGTH);

      // frontrunning transaction
      const createUserLoan2 = await loanManager.connect(hub).createUserLoan(loanId, accountId2, loanTypeId, loanName);

      // initial transaction
      const createUserLoan = loanManager.connect(hub).createUserLoan(loanId, accountId1, loanTypeId, loanName);

      await expect(createUserLoan)
        .to.be.revertedWithCustomError(loanManager, "UserLoanAlreadyCreated")
        .withArgs(loanId);
    });


  });
```


### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Immunefi |
| Protocol | Folks Finance |
| Report Date | N/A |
| Finders | Kalogerone |

### Source Links

- **Source**: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2033687%20-%20%5BSmart%20Contract%20-%20Medium%5D%20Loan%20creation%20can%20be%20frontrun%20preventing%20the%20users%20from%20creating%20loans.md
- **GitHub**: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2033687%20-%20%5BSmart%20Contract%20-%20Medium%5D%20Loan%20creation%20can%20be%20frontrun%20preventing%20the%20users%20from%20creating%20loans.md
- **Contest**: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2033687%20-%20%5BSmart%20Contract%20-%20Medium%5D%20Loan%20creation%20can%20be%20frontrun%20preventing%20the%20users%20from%20creating%20loans.md

### Keywords for Search

`vulnerability`

