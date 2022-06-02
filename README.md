# Introduction
This is Cone Vault - a smart contract made to augment Cubo's (https://cubo.money) functionality.

In a few words, CUBO is a token which allows users to buy Nodes of different tiers, the more you spend the more you get rewarded.

Many people can't afford top tier Nodes, and that's where Cone Vault comes in. It allows users to join forces and create a Vault to finance a top tier Node - the result, users can get rewarded as the top spenders!

## Set up
>```cd blockchain```

>```pip install requirements.txt```

>```brownie test```

## Troubleshooting
Make sure you have ganache-cli instaleld and that you have exported openssl-legacy-provider
>```export NODE_OPTIONS=--openssl-legacy-provider```

## Deploy to local ganache
>```brownie run scripts/token.py```