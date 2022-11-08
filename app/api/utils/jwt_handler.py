def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'result': 'OK',
        'token': token,
        'email': user.email
    }
