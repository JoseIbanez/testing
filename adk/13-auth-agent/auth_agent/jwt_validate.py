import contextvars
from logging import getLogger
import jwt 

from mcp.server.auth.provider import AccessToken, TokenVerifier
jwt_context_var = contextvars.ContextVar[dict | None]("auth_context", default=None)
logger = getLogger(__name__)


def get_jwt_token() -> dict | None:
    """
    Get the JWT token from the current context.

    Returns:
        The JWT token if an authenticated user is available, None otherwise.
    """
    auth_jwt = jwt_context_var.get()
    return auth_jwt




class SimpleTokenVerifier(TokenVerifier):
    """Simple token verifier for demonstration"""

    def __init__(self,auth_server:str):
        super().__init__()
        self.options = {"verify_signature": True, "verify_exp": True, "verify_aud": False}
        self.auth_server = auth_server

    async def verify_token(self, token: str) -> AccessToken | None:
        logger.debug("Verifying token: %s", token)

        if self.options.get("verify_signature", True) and self.auth_server:
            jwks_client = jwt.PyJWKClient(f"{self.auth_server}/.well-known/jwks.json")
            signing_key = jwks_client.get_signing_key_from_jwt(token).key
        else:
            logger.warning("Skipping signature verification as per options.")
            signing_key = None

        decoded = jwt.decode(token, 
                             key=signing_key,
                             options=self.options, 
                             algorithms=["HS256", "RS256"])


        #logger.info(f"Decoded token: {decoded}")
        jwt_context_var.set(decoded)

        resources = [ p for p in decoded.get("permissions", []) if p.startswith("cust:")]

        return AccessToken(token=token, 
                           client_id=decoded.get("user_id") or decoded.get("sub"), 
                           scopes=decoded.get("scope", "").split(" ") + resources,
                           resource=decoded.get("aud"),
                           expires_at=decoded.get("exp"),
                           )



