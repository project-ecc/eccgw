# ECC Faucet

The ECC Faucet dispenses 1000 ECC to each visitor using a unique full node routing tag (aka routing public key) and ECC address one time only. It is not possible to visit the faucet successfully a second time using the same node or address.

Pending support in wallet apps such as Sapphire, you may visit the ECC Faucet using the following RPC commands. These commands may be issued in any of the following ways:

- eccoind command line RPC interface
- advanced console in Sapphire
- debug console in Lynx

## Prerequisites ##

- eccoind version must be 3.0.0 or greater
- your node needs to have a route to the ECC Gateway Node (eccgw)

eccoind version 3.0.0 requires the following setting in eccoin.conf to enable AODV routing.

    beta=1

## Step 1 - ECC Address ##

Obtain an address from your node's wallet using your preferred method, or the RPC command below:

    getnewaddress

Record the result for later use.

## Step 2 - Node Routing Tag ##

Obtain your node's routing tag using the following RPC command:

    getroutingpubkey

Record the result for later use. It is an 88 character text string ending with an "=".

## Step 3 - Route to ECC Gateway Node ##

Check that your node has an AODV route to the ECC Gateway Node (eccgw) using the following PRC command: 

    haveroute BMi/dBkqH9SWzb+cuQvsXaKnJWYi24OicSfRo+bzTQ7LvBWRpo6JWzVMO2Mgh7+0+Ocjmws9tNfNkqfpjd2iN3c=

Ensure that this command returns the result `true`. If it does not, the final step will not work correctly.

Note that the long character string above is the current routing tag of the ECC Gateway Node.  There is a possibility that this may change in the future, so always check back with the latest documentation. One day there may be an alias system for naming core infrastructure routing tags.

## Step 4 - Visit ECC Faucet ##

To visit the ECC faucet and collect your one time only 1000 ECC, issue the following RPC command:

    sendpacket BMi/dBkqH9SWzb+cuQvsXaKnJWYi24OicSfRo+bzTQ7LvBWRpo6JWzVMO2Mgh7+0+Ocjmws9tNfNkqfpjd2iN3c= 255 1 "<ECC Address> <Node Routing Tag>"

In the command above, replace:

- `<ECC Address>` with the ECC address obtained in step 1
- `<Node Routing Tag>` with the node routing tag obtained in step 2

Follow @eccgw on Twitter to check that your faucet visit was successful. You'll see a tweet similar to [https://twitter.com/eccgw/status/1247519151138066433](https://twitter.com/eccgw/status/1247519151138066433 "Example Tweet")

Good luck !!!

Alternatively, wait for the next release of Sapphire which should have a "Get Free ECC" button which will do all of the above for you at the press of a button.

## Donations ##

If you wish to make a donation to the ECC Faucet, please send to:

    ESLv9BpjsSUxZZYuWmqX9krXbvgGwQP6My

