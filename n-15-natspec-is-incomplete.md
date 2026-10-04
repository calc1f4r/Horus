---
# Core Classification
protocol: Debt DAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42962
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-11-debtdao
source_link: https://code4rena.com/reports/2022-11-debtdao
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

protocol_categories:
  - dexes
  - services
  - liquidity_manager
  - payments
  - rwa_lending

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[N-15]  NatSpec is incomplete

### Overview

See description below for full details.

### Original Finding Content


*There are 56 instances of this issue:*
```solidity
File: contracts/modules/credit/EscrowedLine.sol

/// @audit Missing: '@param newLine'
82      /**
83       * see SecuredlLine.rollover
84       * @notice helper function to allow borrower to easily swithc collateral to a new Line after repyment
85       *(@dev priviliegad internal function.
86       * @dev MUST only be callable if line is REPAID
87       * @return - if function successfully executed
88      */
89:     function _rollover(address newLine) internal virtual returns(bool) {

```
https://github.com/debtdao/Line-of-Credit/blob/e8aa08b44f6132a5ed901f8daa231700c5afeb3a/contracts/modules/credit/EscrowedLine.sol#L82-L89

```solidity
File: contracts/modules/credit/LineOfCredit.sol

/// @audit Missing: '@return'
216         @param id - the position id for credit position
217       */
218:      function _accrue(Credit memory credit, bytes32 id) internal returns(Credit memory) {

/// @audit Missing: '@param status_'
415       /**
416         * @notice - updates `status` variable in storage if current status is diferent from existing status.
417         * @dev - privileged internal function. MUST check params and logic flow before calling
418         * @dev - does not save new status if it is the same as current status
419         * @return status - the current status of the line after updating
420        */
421:      function _updateStatus(LineLib.STATUS status_) internal returns(LineLib.STATUS) {

/// @audit Missing: '@return'
433        * @param amount - amount of tokens lender will initially deposit
434       */
435       function _createCredit(
436           address lender,
437           address token,
438           uint256 amount
439       )
440           internal
441:          returns (bytes32 id)

/// @audit Missing: '@param credit'
456     /**
457      * @dev - Reduces `principal` and/or `interestAccrued` on a credit line.
458               Expects checks for conditions of repaying and param sanitizing before calling
459               e.g. early repayment of principal, tokens have actually been paid by borrower, etc.
460      * @dev - privileged internal function. MUST check params and logic flow before calling
461      * @param id - position id with all data pertaining to line
462      * @param amount - amount of Credit Token being repaid on credit line
463      * @return credit - position struct in memory with updated values
464     */
465       function _repay(Credit memory credit, bytes32 id, uint256 amount)
466           internal
467:          returns (Credit memory)

/// @audit Missing: '@param credit'
/// @audit Missing: '@param id'
477       /**
478        * @notice - checks that a credit line is fully repaid and removes it
479        * @dev deletes credit storage. Store any data u might need later in call before _close()
480        * @dev - privileged internal function. MUST check params and logic flow before calling
481        * @return credit - position struct in memory with updated values
482        */
483:      function _close(Credit memory credit, bytes32 id) internal virtual returns (bool) {

```
https://github.com/debtdao/Line-of-Credit/blob/e8aa08b44f6132a5ed901f8daa231700c5afeb3a/contracts/modules/credit/LineOfCredit.sol#L216-L218

```solidity
File: contracts/modules/credit/SecuredLine.sol

/// @audit Missing: '@return'
77       * @param targetToken - token in escrow that will be sold of to repay position
78       */
79    
80      function liquidate(
81        uint256 amount,
82        address targetToken
83      )
84        external
85        whileBorrowing
86:       returns(uint256)

```
https://github.com/debtdao/Line-of-Credit/blob/e8aa08b44f6132a5ed901f8daa231700c5afeb3a/contracts/modules/credit/SecuredLine.sol#L77-L86

```solidity
File: contracts/modules/escrow/Escrow.sol

/// @audit Missing: '@param _line'
69        /**
70        * @notice - Allows current owner to transfer ownership to another address
71        * @dev    - Used if we setup Escrow before Line exists. Line has no way to interface with this function so once transfered `line` is set forever
72        * @return didUpdate - if function successfully executed or not
73        */
74:       function updateLine(address _line) external returns(bool) {

/// @audit Missing: '@return'
98         * @param token - the token to all borrow to deposit as collateral
99         */
100:      function enableCollateral(address token) external returns (bool) {

```
https://github.com/debtdao/Line-of-Credit/blob/e8aa08b44f6132a5ed901f8daa231700c5afeb3a/contracts/modules/escrow/Escrow.sol#L69-L74

```solidity
File: contracts/modules/oracle/Oracle.sol

/// @audit Missing: '@param token'
19        /**
20         * @return price - the latest price in USD to 8 decimals
21         */
22:       function getLatestAnswer(address token) external returns (int) {

```
https://github.com/debtdao/Line-of-Credit/blob/e8aa08b44f6132a5ed901f8daa231700c5afeb3a/contracts/modules/oracle/Oracle.sol#L19-L22

```solidity
File: contracts/modules/spigot/Spigot.sol

/// @audit Missing: '@param token'
57        /**
58    
59         * @notice - Claims revenue tokens from the Spigot (push and pull payments) and escrows them for the Owner withdraw later.
60                   - Calls predefined function in contract settings to claim revenue.
61                   - Automatically sends portion to Treasury and then escrows Owner's share
62                   - There is no conversion or trade of revenue tokens. 
63         * @dev    - Assumes the only side effect of calling claimFunc on revenueContract is we receive new tokens.
64                   - Any other side effects could be dangerous to the Spigot or upstream contracts.
65         * @dev    - callable by anyone
66         * @param revenueContract - Contract with registered settings to claim revenue from
67         * @param data - Transaction data, including function signature, to properly claim revenue on revenueContract
68         * @return claimed -  The amount of revenue tokens claimed from revenueContract and split between `owner` and `treasury`
69        */
70        function claimRevenue(address revenueContract, address token, bytes calldata data)
71            external nonReentrant
72:           returns (uint256 claimed)

/// @audit Missing: '@return'
106        * @param data - tx data, including function signature, to call contract with
107        */
108:      function operate(address revenueContract, bytes calldata data) external returns (bool) {

/// @audit Missing: '@return'
123        * @param setting - Spigot settings for smart contract   
124        */
125:      function addSpigot(address revenueContract, Setting memory setting) external returns (bool) {

/// @audit Missing: '@return'
135        * @param revenueContract - smart contract to transfer ownership of
136        */
137       function removeSpigot(address revenueContract)
138           external
139:          returns (bool)

/// @audit Missing: '@return'
157        * @param newOwner - Address to give control to
158        */
159:      function updateOwner(address newOwner) external returns (bool) {

/// @audit Missing: '@return'
168        * @param newOperator - Address to give control to
169        */
170:      function updateOperator(address newOperator) external returns (bool) {

/// @audit Missing: '@return'
179        * @param newTreasury - Address to divert funds to
180        */
181:      function updateTreasury(address newTreasury) external returns (bool) {

/// @audit Missing: '@return'
192        * @param allowed - true/false whether to allow this function to be called by Operator
193        */
194:       function updateWhitelistedFunction(bytes4 func, bool allowed) external returns (bool) {

/// @audit Missing: '@return'
204        * @param token Revenue token that is being garnished from spigots
205       */
206:      function getEscrowed(address token) external view returns (uint256) {

/// @audit Missing: '@return'
213        * @param func Function to check on whitelist 
214       */
215   
216:      function isWhitelisted(bytes4 func) external view returns(bool) {

```
https://github.com/debtdao/Line-of-Credit/blob/e8aa08b44f6132a5ed901f8daa231700c5afeb3a/contracts/modules/spigot/Spigot.sol#L57-L72

```solidity
File: contracts/utils/CreditLib.sol

/// @audit Missing: '@param id'
/// @audit Missing: '@param amount'
/// @audit Missing: '@param lender'
/// @audit Missing: '@param token'
/// @audit Missing: '@return'
120     /**
121       * see ILineOfCredit._createCredit
122       * @notice called by LineOfCredit._createCredit during every repayment function
123       * @param oracle - interset rate contract used by line that will calculate interest owed
124      */
125     function create(
126         bytes32 id,
127         uint256 amount,
128         address lender,
129         address token,
130         address oracle
131     )
132         external 
133:        returns(ILineOfCredit.Credit memory credit)

/// @audit Missing: '@param id'
/// @audit Missing: '@param amount'
/// @audit Missing: '@return'
163     /**
164       * see ILineOfCredit._repay
165       * @notice called by LineOfCredit._repay during every repayment function
166       * @param credit - The lender position being repaid
167      */
168     function repay(
169       ILineOfCredit.Credit memory credit,
170       bytes32 id,
171       uint256 amount
172     )
173       external
174:      returns (ILineOfCredit.Credit memory)

/// @audit Missing: '@param id'
/// @audit Missing: '@param amount'
/// @audit Missing: '@return'
197     /**
198       * see ILineOfCredit.withdraw
199       * @notice called by LineOfCredit.withdraw during every repayment function
200       * @param credit - The lender position that is being bwithdrawn from
201      */
202     function withdraw(
203       ILineOfCredit.Credit memory credit,
204       bytes32 id,
205       uint256 amount
206     )
207       external
208:      returns (ILineOfCredit.Credit memory)

/// @audit Missing: '@param credit'
/// @audit Missing: '@param id'
/// @audit Missing: '@return'
234     /**
235       * see ILineOfCredit._accrue
236       * @notice called by LineOfCredit._accrue during every repayment function
237       * @param interest - interset rate contract used by line that will calculate interest owed
238      */
239     function accrue(
240       ILineOfCredit.Credit memory credit,
241       bytes32 id,
242       address interest
243     )
244       public
245:      returns (ILineOfCredit.Credit memory)

```
https://github.com/debtdao/Line-of-Credit/blob/e8aa08b44f6132a5ed901f8daa231700c5afeb3a/contracts/utils/CreditLib.sol#L120-L133

```solidity
File: contracts/utils/EscrowLib.sol

/// @audit Missing: '@param self'
28        /**
29         * @notice updates the cratio according to the collateral value vs line value
30         * @dev calls accrue interest on the line contract to update the latest interest payable
31         * @param oracle - address to call for collateral token prices
32         * @return cratio - the updated collateral ratio in 4 decimals
33        */
34:       function _getLatestCollateralRatio(EscrowState storage self, address oracle) public returns (uint256) {

/// @audit Missing: '@param self'
46        /**
47        * @notice - Iterates over all enabled tokens and calculates the USD value of all deposited collateral
48        * @param oracle - address to call for collateral token prices
49        * @return totalCollateralValue - the collateral's USD value in 8 decimals
50        */
51:       function _getCollateralValue(EscrowState storage self, address oracle) public returns (uint256) {

```
https://github.com/debtdao/Line-of-Credit/blob/e8aa08b44f6132a5ed901f8daa231700c5afeb3a/contracts/utils/EscrowLib.sol#L28-L34

```solidity
File: contracts/utils/LineFactoryLib.sol

/// @audit Missing: '@param oracle'
/// @audit Missing: '@param arbiter'
33        /**
34          @notice sets up new line based of config of old line. Old line does not need to have REPAID status for this call to succeed.
35          @dev borrower must call rollover() on `oldLine` with newly created line address
36          @param oldLine  - line to copy config from for new line.
37          @param borrower - borrower address on new line
38          @param ttl      - set total term length of line
39          @return newLine - address of newly deployed line with oldLine config
40         */
41        function rolloverSecuredLine(
42            address payable oldLine,
43            address borrower, 
44            address oracle,
45            address arbiter,
46            uint ttl
47:       ) external returns(address) {

```
https://github.com/debtdao/Line-of-Credit/blob/e8aa08b44f6132a5ed901f8daa231700c5afeb3a/contracts/utils/LineFactoryLib.sol#L33-L47

```solidity
File: contracts/utils/LineLib.sol

/// @audit Missing: '@return'
32         * @param amount - amount of tokens to send
33         */
34        function sendOutTokenOrETH(
35          address token,
36          address receiver,
37          uint256 amount
38        )
39          external
40:         returns (bool)

/// @audit Missing: '@return'
57         * @param amount - amount of tokens to send
58         */
59        function receiveTokenOrETH(
60          address token,
61          address sender,
62          uint256 amount
63        )
64          external
65:         returns (bool)

/// @audit Missing: '@return'
78         * @param token - address of token to check. Denominations.ETH for raw ETH
79        */
80:       function getBalance(address token) external view returns (uint256) {

```
https://github.com/debtdao/Line-of-Credit/blob/e8aa08b44f6132a5ed901f8daa231700c5afeb3a/contracts/utils/LineLib.sol#L32-L40

```solidity
File: contracts/utils/SpigotedLineLib.sol

/// @audit Missing: '@param spigot'
/// @audit Missing: '@param status'
/// @audit Missing: '@param defaultSplit'
163       /**
164        * @notice Changes the revenue split between a Borrower's treasury and the LineOfCredit based on line health, runs with updateOwnerSplit()
165        * @dev    - callable `arbiter` + `borrower`
166        * @param revenueContract - spigot to update
167        * @return whether or not split was updated
168        */
169:      function updateSplit(address spigot, address revenueContract, LineLib.STATUS status, uint8 defaultSplit) external returns (bool) {

/// @audit Missing: '@param spigot'
/// @audit Missing: '@param status'
/// @audit Missing: '@param borrower'
/// @audit Missing: '@param arbiter'
/// @audit Missing: '@param to'
186       /**
187   
188      * @notice -  Transfers ownership of the entire Spigot and its revenuw streams from its then Owner to either 
189                   the Borrower (if a Line of Credit has been been fully repaid) or 
190                   to the Arbiter (if the Line of Credit is liquidatable).
191      * @dev    - callable by anyone 
192      * @return - whether or not Spigot was released
193     */
194:      function releaseSpigot(address spigot, LineLib.STATUS status, address borrower, address arbiter, address to) external returns (bool) {

/// @audit Missing: '@param to'
/// @audit Missing: '@param token'
/// @audit Missing: '@param amount'
/// @audit Missing: '@param status'
/// @audit Missing: '@param borrower'
/// @audit Missing: '@param arbiter'
211     /**
212      * @notice -  Sends any remaining tokens (revenue or credit tokens) in the Spigot to the Borrower after the loan has been repaid.
213                -  In case of a Borrower default (loan status = liquidatable), this is a fallback mechanism to withdraw all the tokens and send them to the Arbiter
214                -  Does not transfer anything if line is healthy
215      * @return - whether or not spigot was released
216     */
217:      function sweep(address to, address token, uint256 amount, LineLib.STATUS status, address borrower, address arbiter) external returns (bool) {

```
https://github.com/debtdao/Line-of-Credit/blob/e8aa08b44f6132a5ed901f8daa231700c5afeb3a/contracts/utils/SpigotedLineLib.sol#L163-L169



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Debt DAO |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-11-debtdao
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2022-11-debtdao

### Keywords for Search

`vulnerability`

