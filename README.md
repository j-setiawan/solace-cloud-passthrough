# solace-cloud-passthrough
Uses a [Solace Cloud API Token](https://console.solace.cloud/) to pass along SEMP requests to your service directly.

Intended to be used with AWS API Gateway using a Lambda as a proxy.

## Creating Lambda ZIP package
1. `pip install --target ./package requests`
1. `cd package`
1. `zip -r9 ${OLDPWD}/function.zip .`
1. `cd $OLDPWD`
1. `zip -g function.zip lambda_function.py`
