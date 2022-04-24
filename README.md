# timecoin-blockchain (TIMECOIN)

![Alt Timecoin Logo](https://github.com/Timecoin-Network/timecoin-blockchain/raw/main/timecoin-blockchain-gui/src/assets/img/timecoin_circle.png)

Timecoin (TIMECOIN) is a modern, green cryptocurrency built to be efficient, decentralized, and secure.


## Useful Links

- [Timecoin Website](https://www.timecoincrypto.net/) - Visit the Timecoin Website
- [Timecoin FAQ](https://www.timecoincrypto.net/faq) - Find answers to Frequently Asked Questions
- [Timecoin Calculator](https://chiaforkscalculator.com/) - Estimate out how your Timecoin earnings.
- [Timecoin Blockchain DB](https://www.timecoincrypto.net//blockchain_v1_mainnet.sqlite) - Download the latest Timecoin Blockchain Database


## Social Links
- [Discord](https://discord.gg/wVAd75mJYR) - Join the Timecoin Discord Community
- [Twitter](https://twitter.com/TimecoinCryptoNet) - Follow Timecoin on Twitter


## How to Install

Timecoin Executable are available from our [GitHub Releases Page](https://github.com/Timecoin-Network/timecoin-blockchain/releases). You can also build from source. An example case for Ubuntu source installation is provided below. Please [visit our wiki page](https://github.com/Timecoin-Network/timecoin-blockchain/wiki) for more details, and for source installation on operating systems.

```
# Update, install GIT, clone Timecoin repo

   sudo apt-get update
   sudo apt install git -y
   git clone https://github.com/Timecoin-Network/timecoin-blockchain.git
  
# Install Timecoin Blockchain

   cd timecoin-blockchain
   sh install.sh
   . ./activate
   timecoin init

# Install Timecoin GUI

   sh install-gui.sh
   cd timecoin-blockchain-gui
   npm run electron &
```

If the Timecoin client is unable to find peers automatically, please connect to the following official peers:

- introducer.timecoincrypto.net / Port: 56444
- dns-introducer.timecoincrypto.net / Port: 56444


## How to Stake

1. Query the staking addresses according to your farming plot list:

   ```
   $ timecoin farm summary
   ...
   Staking addresses:
     timecoin1x6jjvepyvjv7395nmtywvx9mknshgy78dsmuu38m0e9grxr080nsltjugr (balance: 0, plots: 27)
   ...
   ```

2. Deposit coins to the staking address:

   ```
   $ timecoin wallet send -t timecoin1x6jjvepyvjv7395nmtywvx9mknshgy78dsmuu38m0e9grxr080nsltjugr -a 1
   ```

   Wait for the transaction get confirmed, query staking balance again:

   ```
   $ timecoin farm summary
   ...
   Staking addresses:
     timecoin1x6jjvepyvjv7395nmtywvx9mknshgy78dsmuu38m0e9grxr080nsltjugr (balance: 1, plots: 27)
   ...
   ```

3. Withdraw coins from the staking address:

   ```
   $ timecoin wallet send_from -s timecoin1x6jjvepyvjv7395nmtywvx9mknshgy78dsmuu38m0e9grxr080nsltjugr -t $RECEIVER
   ```

   Do a transaction to transfer the coins from the staking address to any receive address.

   Make sure to choose the wallet that contains the plot farmer key.
