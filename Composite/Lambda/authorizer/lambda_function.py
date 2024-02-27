import jwt

def lambda_handler(event, context):
    token = event['authorizationToken'].split(' ')[1]  # extract the token
    secret_key = "Doritos"
    principalId = 'default_user'

    try:
        # decode the jwt token
        decoded = jwt.decode(token, secret_key, algorithms=["HS384"])
        user_role = decoded.get('role')
        user_id = decoded.get('userId')

        # policies
        policy_document = {
            "Version": "2012-10-17",
            "Statement": []
        }

        arn = event['methodArn']
        region = arn.split(':')[3]
        aws_account_id = arn.split(':')[4]
        api_id = arn.split(':')[5].split('/')[0]
        stage = arn.split(':')[5].split('/')[1]

        if user_role == 'admin':
            # admin: allow access to everything
            policy_document['Statement'].append({
                "Action": "execute-api:Invoke",
                "Effect": "Allow",
                "Resource": "*/*"
            })
        elif user_role in ['guest', 'host']:
            # guest & host: access to everything on their own user_id, can GET their own bookings
            user_resources = [
                f"arn:aws:execute-api:{region}:{aws_account_id}:{api_id}/{stage}/GET/users/{user_id}",
                f"arn:aws:execute-api:{region}:{aws_account_id}:{api_id}/{stage}/PUT/users/{user_id}",
                f"arn:aws:execute-api:{region}:{aws_account_id}:{api_id}/{stage}/POST/users/{user_id}",
                f"arn:aws:execute-api:{region}:{aws_account_id}:{api_id}/{stage}/DELETE/users/{user_id}",
                f"arn:aws:execute-api:{region}:{aws_account_id}:{api_id}/{stage}/GET/properties",
            ]

        else:
            # everyoone, including not-loged in users, can access GET properties
            policy_document['Statement'].append({
                "Action": "execute-api:Invoke",
                "Effect": "Allow",
                "Resource": f"arn:aws:execute-api:{region}:{aws_account_id}:{api_id}/{stage}/GET/properties"
            })

        # build the auth response
        auth_response = {
            "principalId": principalId,
            "policyDocument": policy_document
        }

        return auth_response
    except jwt.ExpiredSignatureError:
        # handle expired token
        return {"message": "Token expired"}
    except jwt.InvalidTokenError:
        # handle invalid token
        return {"message": "Invalid token"}