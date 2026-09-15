---
# Core Classification
protocol: Infrared Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54064
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/89e5aa01-14ad-48f8-af3d-d1182d4ffefb
source_link: https://cdn.cantina.xyz/reports/cantina_infrared_july2024.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - 0xRajeev
  - Mario Poneder
  - Cryptara
  - phaze
---

## Vulnerability Title

Missing zero address validation in add() can cause issues with validator accounting 

### Overview

See description below for full details.

### Original Finding Content

## InfraredDistributor Contract Issue

## Context
InfraredDistributor.sol#L48-L64

## Description
The `add()` function in the `InfraredDistributor` contract does not validate the provided validator address. This oversight can lead to scenarios where a zero address is added as a validator, which would be incorrectly counted as a valid validator. This can cause issues with validator management, as the `removeValidators()` function will fail due to the validator being set to the zero address, leading to an inability to remove such validators.

## Impact
**Medium**: This can lead to incorrect validator management, potentially affecting the overall functionality of the validator system. Adding zero address validators results in incorrect counts (`numInfraredValidators`) and an inability to remove them (`removeValidators`), causing inconsistencies.

## Likelihood
**Low**: It is unlikely that the Governor mistakenly adds a zero address validator. Governance proposals are assumed to be vetted before execution.

## Proof of Concept
```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.22;

import "forge-std/Test.sol";
import "@core/Infrared.sol";
import "@core/IBGT.sol";
import "@core/InfraredVault.sol";
import "@utils/DataTypes.sol";
import "@utils/ValidatorUtils.sol";
import {IWBERA} from "@berachain/interfaces/IWBERA.sol";
import {ERC1967Proxy} from "@openzeppelin/contracts/proxy/ERC1967/ERC1967Proxy.sol";
import {IBerachainRewardsVaultFactory} from "@berachain/interfaces/IBerachainRewardsVaultFactory.sol";
import {IBeraChef} from "@berachain/interfaces/IBeraChef.sol";
import {BribeCollector} from "@core/BribeCollector.sol";
import {InfraredDistributor} from "@core/InfraredDistributor.sol";
import {Voter} from "@voting/Voter.sol";
import {VotingEscrow} from "@voting/VotingEscrow.sol";
import "@openzeppelin/proxy/Clones.sol";
import "../src/interfaces/IInfrared.sol";
import "@mocks/MockERC20.sol";
import "@mocks/MockWbera.sol";
import "@mocks/MockBerachainRewardsVaultFactory.sol";
import "@mocks/MockBeaconDepositContract.sol";

contract MockBGT is MockERC20 {
    constructor(string memory name, string memory symbol, uint8 decimals) MockERC20(name, symbol, decimals) {}

    mapping(bytes => uint256) _commissions;

    // COMMISSION_MAX check, not over 224 bits
    function setCommission(bytes memory pubkey, uint256 _newCommissions) public {
        _commissions[pubkey] = _newCommissions;
    }

    // (uint32 blockTimestampLast, uint224 rate)
    function commissions(bytes memory pubkey) public view returns (uint32, uint224) {
        return (0, uint224(_commissions[pubkey]));
    }
}

contract POC is Test {
    using Clones for address;

    IBGT public ibgt;
    MockBGT public bgt;
    MockERC20 public ired;
    MockERC20 public wibera;
    MockERC20 public honey;
    MockWbera public mockWbera;
    MockERC20 public mockPool;
    MockBerachainRewardsVaultFactory public rewardsFactory;
    IBeraChef public beraChef;
    BribeCollector public collector;
    InfraredDistributor public distributor;
    Infrared public infrared;
    Voter public voter;
    VotingEscrow public veIRED;
    uint256 public bribeCollectorPayoutAmount = 10 ether;
    address public admin;
    address public keeper;
    address public governance;
    address stakingAsset;
    address public chef = makeAddr("chef"); // TODO: fix with mock chef

    function setupProxy(address implementation) internal returns (address proxy) {
        proxy = address(new ERC1967Proxy(implementation, ""));
    }

    function setUp() public {
        // Mock non transferable token BGT token
        bgt = new MockBGT("BGT", "BGT", 18);
        // Mock contract instantiations
        ibgt = new IBGT(address(bgt));
        ired = new MockERC20("IRED", "IRED", 18);
        wibera = new MockERC20("WIBERA", "WIBERA", 18);
        honey = new MockERC20("HONEY", "HONEY", 18);
        mockWbera = new MockWbera();

        // Set up addresses for roles
        admin = address(0x1337);
        keeper = address(1);
        governance = address(2);

        // TODO: mock contracts
        mockPool = new MockERC20("Mock Asset", "MAS", 18);
        stakingAsset = address(mockPool);

        // deploy a rewards vault for IBGT
        rewardsFactory = new MockBerachainRewardsVaultFactory(address(bgt));

        // initialize Infrared contracts;
        infrared = Infrared(
            setupProxy(
                address(
                    new Infrared(
                        address(ibgt),
                        address(rewardsFactory),
                        address(chef),
                        address(mockWbera),
                        address(honey),
                        address(ired),
                        address(wibera)
                    )
                )
            )
        );

        collector = BribeCollector(
            setupProxy(address(new BribeCollector(address(infrared))))
        );
        
        distributor = InfraredDistributor(
            setupProxy(address(new InfraredDistributor(address(infrared))))
        );

        // IRED voting
        voter = Voter(setupProxy(address(new Voter(address(infrared)))));
        
        veIRED = new VotingEscrow(
            address(this), address(ired), address(voter), address(infrared)
        );

        collector.initialize(admin, address(mockWbera), 10 ether);
        distributor.initialize();
        infrared.initialize(
            address(admin),
            address(collector),
            address(distributor),
            address(voter),
            1 days
        ); // make helper contract the admin
    }

    function test_add_remove_validator_lock() public {
        IInfrared.Validator memory validator = IInfrared.Validator({
            pubkey: "0x1234",
            addr: address(0),
            commission: 0
        });

        IInfrared.Validator[] memory _validators = new IInfrared.Validator[](1);
        _validators[0] = validator;

        vm.startPrank(admin);
        infrared.addValidators(_validators);
        assertEq(infrared.numInfraredValidators(), 1);

        bytes[] memory _pubkeys = new bytes[](1);
        _pubkeys[0] = "0x1234";

        vm.startPrank(admin);
        infrared.removeValidators(_pubkeys);
    }
}
```

### Stack trace
```
[180607] POC::test_add_remove_validator_lock()
[0] VM::startPrank(0x0000000000000000000000000000000000001337)
← [Return]
[158062] ERC1967Proxy::addValidators([Validator({ pubkey: 0x307831323334, addr: 0x0000000000000000000000000000000000000000, commission: 0 })]),→
[153216] Infrared::addValidators([Validator({ pubkey: 0x307831323334, addr: 0x0000000000000000000000000000000000000000, commission: 0 })]) [delegatecall],→
[37130] ERC1967Proxy::add(0x307831323334, 0x0000000000000000000000000000000000000000)
[32308] InfraredDistributor::add(0x307831323334, 0x0000000000000000000000000000000000000000)
[delegatecall],→
emit Added(pubkey: 0x307831323334, validator: 0x0000000000000000000000000000000000000000, amountCumulative: 1),→
← [Stop]
← [Return]
[3111] MockBGT::commissions(0x307831323334) [staticcall]
← [Return] 0, 0
emit ValidatorCommissionUpdated(_sender: 0x0000000000000000000000000000000000001337, _pubkey: 0x307831323334, _current: 0, _new: 0),→
[880] MockBGT::setCommission(0x307831323334, 0)
← [Return]
emit ValidatorsAdded(_sender: 0x0000000000000000000000000000000000001337, _validators: [Validator({
pubkey: 0x307831323334, addr: 0x0000000000000000000000000000000000000000, commission: 0 })]),→
← [Return]
← [Return]
[1487] ERC1967Proxy::numInfraredValidators() [staticcall]
[1180] Infrared::numInfraredValidators() [delegatecall]
← [Return] 1
← [Return] 1
[0] VM::startPrank(0x0000000000000000000000000000000000001337)
← [Return]
[6817] ERC1967Proxy::removeValidators([0x307831323334])
[6485] Infrared::removeValidators([0x307831323334]) [delegatecall]
[1199] ERC1967Proxy::remove(0x307831323334)
[879] InfraredDistributor::remove(0x307831323334) [delegatecall]
← [Revert] ValidatorDoesNotExist()
← [Revert] ValidatorDoesNotExist()
← [Revert] ValidatorDoesNotExist()
← [Revert] ValidatorDoesNotExist()
← [Revert] ValidatorDoesNotExist()
```

## Recommendation
Consider adding a validation check to ensure that the validator address is not zero before adding it. This will prevent zero address validators from being added and ensure consistent and correct validator management.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Infrared Finance |
| Report Date | N/A |
| Finders | 0xRajeev, Mario Poneder, Cryptara, phaze |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_infrared_july2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/89e5aa01-14ad-48f8-af3d-d1182d4ffefb

### Keywords for Search

`vulnerability`

