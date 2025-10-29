"""PURPOSE: OAuth2 logic for Upwork (authorization code exchange, token refresh).
"""


# PURPOSE: OAuth2 authorization code exchange + token refresh for Upwork.
# Implement the token exchange at:
#   POST https://www.upwork.com/api/auth/v1/oauth2/token

import httpx

async def exchange_code_for_token(client_id: str, client_secret: str, redirect_uri: str, code: str) -> dict:
    # TODO: post to token endpoint and return token payload
    raise NotImplementedError
