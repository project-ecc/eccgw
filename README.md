# eccgw : ECC Message Gateway

The ECC Message Gateway is a simple ECC message handler that expects to receive packets containing UTF-8 text and acts upon the following syntaxes:

- "%routing-tag message" : echo back the message to the sender's routing tag
- "@handle message" : Tweet using a configured Twitter account
- "person@domain message" : Send email using a configured smtp server
- < syntax to be decided > : Send message to Discord server/channel
- "ecc-address routing-tag" with ProtocolID = 255 : Faucet visit

**Note - only email & twitter have been implemented so far**

Currently any `protocolID` and `protocolVersion` can be used.

## Dependencies ##

Twitter support is via Tweepy:

    $ pip3 install tweepy

## Examples ##

Echo example:

    $ ./eccoind sendpacket BMi/dBkqH9SWzb+cuQvsXaKnJWYi24OicSfRo+bzTQ7LvBWRpo6JWzVMO2Mgh7+0+Ocjmws9tNfNkqfpjd2iN3c= 1 1 "%BCg+o696tx1EgU4E6H0j3QOIo+Lp5BL1GgCF84n/5m27mEvOtUENq53lMz3pYs+ghU6k/9yxheWFPwiE3yhWPbw= Hello World"

Tweet example:

    $ ./eccoind sendpacket BMi/dBkqH9SWzb+cuQvsXaKnJWYi24OicSfRo+bzTQ7LvBWRpo6JWzVMO2Mgh7+0+Ocjmws9tNfNkqfpjd2iN3c= 1 1 "@project_ecc This is the first tweet sent by the ECC Message Gateway (eccgw)"

Email example:

    $ ./eccoind sendpacket BMi/dBkqH9SWzb+cuQvsXaKnJWYi24OicSfRo+bzTQ7LvBWRpo6JWzVMO2Mgh7+0+Ocjmws9tNfNkqfpjd2iN3c= 1 1 "fred.bloggs@hotmail.com Hey Fred how is your blog"

Faucet visit example:

    $ ./eccoind sendpacket BMi/dBkqH9SWzb+cuQvsXaKnJWYi24OicSfRo+bzTQ7LvBWRpo6JWzVMO2Mgh7+0+Ocjmws9tNfNkqfpjd2iN3c= 255 1 "EHsAiD5rrtDrsyq1CcMjXGw9va5yjQKQWH BCg+o696tx1EgU4E6H0j3QOIo+Lp5BL1GgCF84n/5m27mEvOtUENq53lMz3pYs+ghU6k/9yxheWFPwiE3yhWPbw="

The routing key of the node running eccgw is obtained:

    $ ./eccoind getroutingpubkey

You can check that a route is available:

    $ ./eccoind haveroute BMi/dBkqH9SWzb+cuQvsXaKnJWYi24OicSfRo+bzTQ7LvBWRpo6JWzVMO2Mgh7+0+Ocjmws9tNfNkqfpjd2iN3c=

Note that the examples above reference an eccgw instance running on eccserver1.ddns.net