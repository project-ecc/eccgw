# eccgw : ECC Message Gateway

The ECC Message Gateway is a simple ECC message handler that expects to receive packets containing UTF-8 text and acts upon the following syntaxes:

- "@ message" : echo back the message to the sender
- "@handle message" : Tweet using a configured Twitter account
- "person@domain message" : Send email using a configured smtp server

**Note - only email has been implemented so far**

Currently any `protocolID` and `protocolVersion` can be used.

## Example ##

    $ ./eccoind sendpacket BMi/dBkqH9SWzb+cuQvsXaKnJWYi24OicSfRo+bzTQ7LvBWRpo6JWzVMO2Mgh7+0+Ocjmws9tNfNkqfpjd2iN3c= 1 1 "fred.bloggs@hotmail.com Hey Fred how is your blog"

The routing key of the node running eccgw is obtained:

    $ ./eccoind getroutingpubkey

You can check that a route is available:

    $ ./eccoind haveroute BMi/dBkqH9SWzb+cuQvsXaKnJWYi24OicSfRo+bzTQ7LvBWRpo6JWzVMO2Mgh7+0+Ocjmws9tNfNkqfpjd2iN3c=

Note that the examples above reference an eccgw instance running on eccoinserver1.ddns.net