# recurring-tx-lambda
Example code to schedule Algorand transactions using the Algorand Python SDK in an AWS Lambda execution environment. Keys are stored in AWS Secrets Manager.

`lambda_function.py` is the main AWS Lambda function code. To use, make sure to fill in values for `node_token` and `node_address` and uncomment. Update the name of your secret path and region. Modify the transaction to fit your needs, including changing the sending address.

`function.zip` is a zip file of python dependencies to successfuly run the lambda_function.py code in AWS Lambda. It does _not_ currently include the lambda_function.py as you will need to modify it before adding. You can add new files with `zip -g function.zip <new-file>`.

SHA256: `b2d2b4d96253c58a2a1d613a479b28fc5cb2b39425f770ba679ce0aa7d852ee0  function.zip`

This code is associated with a blog post that contains more step-by-step instructions.

