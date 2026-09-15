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
solodit_id: 61065
audit_firm: Immunefi
contest_link: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2033987%20-%20%5BSmart%20Contract%20-%20Medium%5D%20Incorrect%20access%20control%20in%20receiveMessage%20leads%20to%20total%20loss%20of%20funds.md
source_link: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2033987%20-%20%5BSmart%20Contract%20-%20Medium%5D%20Incorrect%20access%20control%20in%20receiveMessage%20leads%20to%20total%20loss%20of%20funds.md
github_link: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2033987%20-%20%5BSmart%20Contract%20-%20Medium%5D%20Incorrect%20access%20control%20in%20receiveMessage%20leads%20to%20total%20loss%20of%20funds.md

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
  - QuantumKid
---

## Vulnerability Title

Incorrect access control in receiveMessage leads to total loss of funds

### Overview


This report is about a bug found in a smart contract on the testnet platform called Snowtrace. The bug allows an attacker to steal funds from the protocol. The bug is caused by a mistake in the code that checks if a user is a valid adapter in the sendMessage function. This mistake allows any arbitrary contract to be considered a valid adapter, which can be used by an attacker to drain the entire protocol. A proof of concept has been provided to demonstrate how the bug can be exploited.

### Original Finding Content




Report type: Smart Contract


Target: https://testnet.snowtrace.io/address/0xa9491a1f4f058832e5742b76eE3f1F1fD7bb6837

Impacts:

* Direct theft of any user funds, whether at-rest or in-motion, other than unclaimed yield

## Description

## Brief/Intro

Due to incorrect adapter access control check in sendMessage function on BridgeRouter contract an attacker can use a malicious contract as adapter to drain the entire funds in the protocol.

## Vulnerability Details

In the receiveMessage to check that whether msg.sender is valid adapter or not first the adapterId is being read from the `adapterToId` mapping as below

```solidity
IBridgeAdapter adapter = IBridgeAdapter(msg.sender);
uint16 adapterId = adapterToId[adapter];
```

Then using that adapterId we check whether that adapterId has a non-zero adapter address in `idToAdapter` mapping as using below function.

```solidity
    function isAdapterInitialized(uint16 adapterId) public view returns (bool) {
        IBridgeAdapter adapter = idToAdapter[adapterId];
        return (address(adapter) != address(0x0));
    }
```

But while adding adapter using below function if zero is used as a valid adapterId any address will be considered as a valid adapter.

```solidity
    function addAdapter(uint16 adapterId, IBridgeAdapter adapter) external onlyRole(MANAGER_ROLE) {
        // check if no existing adapter
        if (isAdapterInitialized(adapterId)) revert AdapterInitialized(adapterId);

        // add adapter
        idToAdapter[adapterId] = adapter;
        adapterToId[adapter] = adapterId;
    }
```

For Example: Let's say 0x1234 is a valid adapter stored at adapterId zero. Then\
`idToAdapter[0] = 0x1234`\
`adapterToId[0x1234] = 0`

Now a malicious contract `0xdead` will also be considered as valid adapter because `adapterToId[0xdead] = 0` and `isAdapterInitialized(0)` will return true as a valid adapter is already initialized with zero as adapterId.

## Impact Details

As any arbitrary contract is considered as a valid adapter. An attacker can use a malicious adapter contract to pass fake messages to drain the entire protocol.

## References

From tests it seems like zero is a valid adapterId

```javascript
  async function addAdapterFixture() {
    const { admin, messager, unusedUsers, bridgeRouter, bridgeRouterAddress } =
      await loadFixture(deployBridgeRouterFixture);

    // deploy and add adapter
    const adapter = await new MockAdapter__factory(admin).deploy(bridgeRouterAddress);
@>  const adapterId = 0;
    const adapterAddress = await adapter.getAddress();
    await bridgeRouter.connect(admin).addAdapter(adapterId, adapterAddress);
  }
```

## Proof of concept

## Proof of Concept

Add this to `add adapter` tests in `/test/bridge/BridgeRouter.test.ts` file.

```javascript
    it("Arbitrary contract will be considered as a valid adapter.", async () => {
      const { bridgeRouter, adapterId, adapterAddress } = await loadFixture(addAdapterFixture);

      // verify adapter was added
      expect(await bridgeRouter.isAdapterInitialized(adapterId)).to.be.true;
      expect(await bridgeRouter.idToAdapter(adapterId)).to.equal(adapterAddress);
      expect(await bridgeRouter.adapterToId(adapterAddress)).to.equal(adapterId);
      // Random address is considered as a valid adapter.
      expect(await bridgeRouter.isAdapterInitialized(await bridgeRouter.adapterToId(getRandomAddress()))).to.be.true;
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
| Finders | QuantumKid |

### Source Links

- **Source**: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2033987%20-%20%5BSmart%20Contract%20-%20Medium%5D%20Incorrect%20access%20control%20in%20receiveMessage%20leads%20to%20total%20loss%20of%20funds.md
- **GitHub**: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2033987%20-%20%5BSmart%20Contract%20-%20Medium%5D%20Incorrect%20access%20control%20in%20receiveMessage%20leads%20to%20total%20loss%20of%20funds.md
- **Contest**: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2033987%20-%20%5BSmart%20Contract%20-%20Medium%5D%20Incorrect%20access%20control%20in%20receiveMessage%20leads%20to%20total%20loss%20of%20funds.md

### Keywords for Search

`vulnerability`

