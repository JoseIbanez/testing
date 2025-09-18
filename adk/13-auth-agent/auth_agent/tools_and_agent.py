import os
import json


from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google.adk.auth.auth_schemes import OpenIdConnectWithConfig
from google.adk.auth.auth_credential import AuthCredential, AuthCredentialTypes, OAuth2Auth
from google.adk.auth import AuthConfig
from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import OpenAPIToolset
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools import FunctionTool, ToolContext
from typing import Dict

# --- Authentication Configuration ---
# This section configures how the agent will handle authentication using OpenID Connect (OIDC),
# often layered on top of OAuth 2.0.

AUTH_SERVER_URL=os.environ.get("AUTH_SERVER_URL")
CLIENT_ID=os.environ.get("CLIENT_ID")
CLIENT_SECRET=os.environ.get("CLIENT_SECRET")
SCOPES = ['read:Sites']

# Define the Authentication Scheme using OpenID Connect.
# This object tells the ADK *how* to perform the OIDC/OAuth2 flow.
# It requires details specific to your Identity Provider (IDP), like Google OAuth, Okta, Auth0, etc.
# Note: Replace the example Okta URLs and credentials with your actual IDP details.
# All following fields are required, and available from your IDP.
auth_scheme = OpenIdConnectWithConfig(
    # The URL of the IDP's authorization endpoint where the user is redirected to log in.
    #authorization_endpoint="https://your-endpoint.okta.com/oauth2/v1/authorize",
    authorization_endpoint=f"{AUTH_SERVER_URL}/authorize",
    # The URL of the IDP's token endpoint where the authorization code is exchanged for tokens.
    #token_endpoint="https://your-token-endpoint.okta.com/oauth2/v1/token",
    token_endpoint=f"{AUTH_SERVER_URL}/oauth/token",
    # The scopes (permissions) your application requests from the IDP.
    # 'openid' is standard for OIDC. 'profile' and 'email' request user profile info.
    scopes=SCOPES,
)

# Define the Authentication Credentials for your specific application.
# This object holds the client identifier and secret that your application uses
# to identify itself to the IDP during the OAuth2 flow.
# !! SECURITY WARNING: Avoid hardcoding secrets in production code. !!
# !! Use environment variables or a secret management system instead. !!
auth_credential = AuthCredential(
  auth_type=AuthCredentialTypes.OAUTH2, # .OPEN_ID_CONNECT,
  oauth2=OAuth2Auth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
  )
)


# --- Toolset Configuration from OpenAPI Specification ---
# This section defines a sample set of tools the agent can use, configured with Authentication
# from steps above.
# This sample set of tools use endpoints protected by Okta and requires an OpenID Connect flow
# to acquire end user credentials.

# with open(os.path.join(os.path.dirname(__file__), 'spec.yaml'), 'r') as f:
#     spec_content = f.read()

# userinfo_toolset = OpenAPIToolset(
#    spec_str=None, #spec_content,
#    spec_str_type='yaml',
#    # ** Crucially, associate the authentication scheme and credentials with these tools. **
#    # This tells the ADK that the tools require the defined OIDC/OAuth2 flow.
#    auth_scheme=auth_scheme,
#    auth_credential=auth_credential,
# )

def get_user_info(tool_context: ToolContext) -> dict:
    """
    Provide user information: user_id, email, etc. 
    """
    TOKEN_CACHE_KEY = "my_tool_tokens"
    creds = None


    ### Check Token Cache in State ###
    cached_token_info = tool_context.state.get(TOKEN_CACHE_KEY)
    print(f"DEBUG: Cached token info from state: {cached_token_info}")
    if cached_token_info:
        try:
            creds = Credentials.from_authorized_user_info(cached_token_info, SCOPES)
            print(f"DEBUG: Loaded cached creds from state: {creds}")
            if not creds.valid and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                tool_context.state[TOKEN_CACHE_KEY] = json.loads(creds.to_json()) # Update cache
            elif not creds.valid:
                creds = None # Invalid, needs re-auth
                tool_context.state[TOKEN_CACHE_KEY] = None
        except Exception as e:
            print(f"Error loading/refreshing cached creds: {e}")
            creds = None
            tool_context.state[TOKEN_CACHE_KEY] = None


    if not creds or not creds.valid:
        # Use auth_scheme and auth_credential configured in the tool.
        # exchanged_credential: AuthCredential | None
        exchanged_credential = tool_context.get_auth_response(AuthConfig(
                                            auth_scheme=auth_scheme,
                                            raw_auth_credential=auth_credential,
        ))
 
        # If exchanged_credential is not None, then there is already an exchanged credetial from the auth response. 
        if exchanged_credential:
            # ADK exchanged the access token already for us
            access_token = exchanged_credential.oauth2.access_token
            refresh_token = exchanged_credential.oauth2.refresh_token
            creds = Credentials(
                  token=access_token,
                  refresh_token=refresh_token,
                  token_uri=auth_scheme.flows.authorizationCode.tokenUrl,
                  client_id=auth_credential.oauth2.client_id,
                  client_secret=auth_credential.oauth2.client_secret,
                  scopes=list(auth_scheme.flows.authorizationCode.scopes.keys()),
            )
            print(f"DEBUG: Obtained exchanged credentials: {creds}")
            # Cache the token in session state and call the API, skip to step 5
            tool_context.state[TOKEN_CACHE_KEY] = json.loads(creds.to_json())
            print(f"DEBUG: Cached/updated tokens under key: {TOKEN_CACHE_KEY}")


    if not creds or not creds.valid:
        print("no credentials")
        tool_context.request_credential(AuthConfig(
                      auth_scheme=auth_scheme,
                      raw_auth_credential=auth_credential,
        ))
        return {'pending': True, 'message': 'Awaiting user authentication.'}

    print(f"Using credentials: {creds}")
    name = "unknown"

    result = {"message": f"Hello {name}. This is a response from an authenticated tool."}
    print(result)
    return result

my_tool = FunctionTool(func=get_user_info)


# --- Agent Configuration ---
# Configure and create the main LLM Agent.
root_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='enterprise_assistant',
    instruction='Help user integrate with multiple enterprise systems, including retrieving user information which may require authentication.',
    tools=[my_tool],
    #tools=userinfo_toolset.get_tools(),
)

# --- Ready for Use ---
# The `root_agent` is now configured with tools protected by OIDC/OAuth2 authentication.
# When the agent attempts to use one of these tools, the ADK framework will automatically
# trigger the authentication flow defined by `auth_scheme` and `auth_credential`
# if valid credentials are not already available in the session.
# The subsequent interaction flow would guide the user through the login process and handle
# token exchanging, and automatically attach the exchanged token to the endpoint defined in
# the tool.