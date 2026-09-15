---
# Core Classification
protocol: Slock.it Incubed3
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13965
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2019/09/slock.it-incubed3/
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

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Martin Ortner
  - Shayan Eskandari
---

## Vulnerability Title

NodeRegistry - Multiple nodes can share slightly different RPC URL ✓ Fixed

### Overview


This bug report is about the Node Registry in the IN3-contracts. It describes an attack vector in which a user can register multiple nodes with the same URL, allowing them to increase their chance of being picked to provide proofs. It also mentions how a user can register multiple accounts for the same node, or register nodes with URLs that do not serve IN3-clients in an attempt to DDoS and extort web-site operators. The report also suggests that canonicalizing URLs can help prevent this attack, however it will not completely prevent someone from registering nodes for other end-points or websites. The report recommends that nodes can be removed by an admin in the first year, but not after that, and that rogue owners cannot be prevented from registering random nodes with high weights and minimum deposit, but can still unregister to receive their deposit after messing with the system.

### Original Finding Content

#### Resolution



Same mitigation as [issue 6.4](#noderegistry---url-can-be-arbitrary-dns-resolvable-names-ips-and-even-localhost-or-private-subnets).


#### Description


One of the requirements for Node registration is to have a unique URL which is not already used by a different owner. The uniqueness check is done by hashing the provided `_url` and checking if someone already registered with that hash of `_url`.


However, byte-equality checks (via hashing in this case) to enforce uniqueness will not work for URLs. For example, while the following URLs are not equal and will result in different `urlHashes` they can logically be the same end-point:


* `https://some-server.com/in3-rpc`
* `https://some-server.com:443/in3-rpc`
* `https://some-server.com/in3-rpc/`
* `https://some-server.com/in3-rpc///`
* `https://some-server.com/in3-rpc?something`
* `https://some-server.com/in3-rpc?something&something`
* `https://www.some-server.com/in3-rpc?something` (if www resolves to the same ip)


**code/in3-contracts/contracts/NodeRegistry.sol:L547-L553**



```
bytes32 urlHash = keccak256(bytes(\_url));

// make sure this url and also this owner was not registered before.
// solium-disable-next-line
require(!urlIndex[urlHash].used && signerIndex[\_signer].stage == Stages.NotInUse,
    "a node with the same url or signer is already registered");


```
This leads to the following attack vectors:


* A user signs up multiple nodes that resolve to the same end-point (URL). A minimum deposit of `0.01 ether` is required for each registration. Registering multiple nodes for the same end-point might allow an attacker to increase their chance of being picked to provide proofs. Registering multiple nodes requires unique signer addresses per node.
* Also one node can have multiple accounts, hence one node can have slightly different URL and different accounts as the `signer`s.
* DoS - A user might register nodes for URLs that do not serve in3-clients in an attempt to DDoS e.g. in an attempt to extort web-site operators. This is kind of a reflection attack where nodes will request other nodes from the contract and try to contact them over RPC. Since it is http-rpc it will consume resources on the receiving end.
* DoS - A user might register Nodes with RPC URLs of other nodes, manipulating weights to cause more traffic than the node can actually handle. Nodes will try to communicate with that node. If no proof is requested the node will not even know that someone else signed up other nodes with their RPC URL to cause problems. If they request proof the original signer will return a signed proof and the node will fail due to a signature mismatch. However, *the node cannot be convicted* and therefore forced to lose the deposit as conviction is bound the signer and the block was not signed by the rogue node entry. There will be no way to remove the node from the registry other than the admin functionality.


#### Recommendation


Canonicalize URLs, but that will not completely prevent someone from registering nodes for other end-points or websites. Nodes can be removed by an admin in the first year but not after that. Rogue owners cannot be prevented from registering random nodes with high weights and minimum deposit. They cannot be convicted as they do not serve proofs. Rogue owners can still unregister to receive their deposit after messing with the system.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Slock.it Incubed3 |
| Report Date | N/A |
| Finders | Martin Ortner, Shayan Eskandari |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2019/09/slock.it-incubed3/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

