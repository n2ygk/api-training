
# coding: utf-8

# # An Example Python Client for the demo-echo API
# 
# When using [OAuth 2.0](https://tools.ietf.org/html/rfc6749) (no matter what the flow), the client app (this notebook) gets an *access token* (and optionally some other tokens like *refresh\_token* and even an OpenID Connect *id\_token* which identifies the end user to the client app -- when using the *openid* scope). 
# 
# The only token we are currently concerned with is the **access token**. 
# 
# Once the client app has the access token, it then adds it to the HTTP request that it sends to the Resource Server in one of two ways, either
# 1. in an HTTP header: `Authorization: Bearer <token>` (preferred) or,
# 2. as a query parameter: `https://example.com/resource?access_token=<token>`.
# But not both!
# 
# You can get a valid access token by, for example, using Postman, and then jump down to where the token is added to the Authorization header a few lines below if you want to initially skip over the OAuth 2.0 dancing.
# 
# Let's try out the [oauth2-client](https://github.com/antechrestos/OAuth2Client) Python library. You can install this with:
# ```sh
# pip install oauth2-client
# ```

# In[1]:


import requests
import webbrowser
from oauth2_client.credentials_manager import CredentialManager, ServiceInformation, OAuthError
import json
from pprint import pprint


# # Composing the OAuth 2.0 Authorization Code Request
# 
# The request consists of a few pieces of information: service endpoints, credentials that identify this registered client app, a redirect_uri to be called back to, and a list of scopes that the Resource Server requires for the given resource and method.
# 
# ## Endpoints
# 
# The OAuth 2.0 service endpoints needed for Authorization Code flow are `authorize` and `token`. The particular required URLs for Columbia's PingFederate-based OAuth 2.0 services are show below and can be found in the RAML securitySchemes:
# ```yaml
# #%RAML 1.0 SecurityScheme
# type: OAuth 2.0
# description: |
#   This API supports OAuth 2.0 for authorizing requests using PingFederate.
#   Please note that MuleSoft will not actually implement any OAuth 2.0 scope enforcement
#   as declared with a resource & method's `securedBy` unless you apply an one or more
#   relevant API Manager Policies:
#     - One of the `OAuth 2.0 protected` PingFederate policies.
#     - The `OAuth 2.0 scope enforcement` custom policy.
# describedBy:
#   headers:
#     Authorization?:
#       description: OAuth 2 access token. Use EITHER this or the access_token, not both.
#       type: string
#   queryParameters:
#     access_token?:
#       description: OAuth 2 access token. Use EITHER this or the Authorization header, not both.
#       type: string
#   responses:
#     401:
#       description: Bad or expired token.
#     403:
#       description: Bad OAuth request
# settings:
#   authorizationUri: https://oauth.cc.columbia.edu/as/authorization.oauth2
#   accessTokenUri: https://oauth.cc.columbia.edu/as/token.oauth2
#   authorizationGrants: 
#     - authorization_code
#     - client_credentials
#   scopes: 
#     !include scopes.raml
#  ```
# 
# ## Client Credentials
# 
# The `client_id` and `client_secret` were obtained from **Request API Access** in the AnyPoint API Developer console. These uniquely identify the client app to the Authorization Server (AS).
# 
# <img src="requestAccess.png" width=500>
# 
# ## Redirect URI
# 
# The OAuth 2.0 Authorization Code protocol "returns" data to the requestor by a GET of it's request\_uri with some query parameter which communicate back the code. This is part of the OAuth 2.0 security "magic". Redirect URIs have to be:
# - Registered in advance with the Authorization Server
# - Specified by the client in the "authorize" request
# They must match or the request is denied.
# 
# Redirect URIs for clients are established by AnyPoint API Manager as part of the setup of new client apps along with other settings such as which grant types are allowed for this client and whether it should return a refresh token:
# 
# <img src="requestUris.png" width=450>
# 
# ## Scopes
# 
# The required scopes for a particular endpoint can be found in the API's RAML description. For this example, a GET of the /things endpoint, the RAML shows that scopes of auth-columbia, -google or -facebook and read are required. Let's also add "openid" so that we get an id_token back for this client app to identify who the authorizing user is.
# 
# ```yaml
# /things:
#   displayName: Things
#   description: some things
#   get:
#     securedBy: # allow selection of one of columbia, facebook, or google login. 
#       - oauth_2_0: { scopes: [ auth-columbia, read ] }
#       - oauth_2_0: { scopes: [ auth-google, read ] }
#       - oauth_2_0: { scopes: [ auth-facebook, read ] }
#     responses:
#       200:
#         body:
#           application/json:
#             schema: Thing
#   ...
#   post:
#     securedBy:
#       - oauth_2_0: { scopes: [ auth-columbia, demo-netphone-admin, create ] }
#       - oauth_2_0: { scopes: [ auth-google, create ] }
#       - oauth_2_0: { scopes: [ auth-facebook, create ] }
# ```
# 

# In[2]:


service_information = ServiceInformation(
    authorize_service='https://oauth.cc.columbia.edu/as/authorization.oauth2',
    token_service='https://oauth.cc.columbia.edu/as/token.oauth2',
    client_id='7da405f38cbc4be48fa9bcbc707afa5c',
    client_secret='8d3d402a4A2244aDB2380721CFd8A7CF',
    scopes=['auth-google', 'read', 'openid'],
    skip_ssl_verifications=False)


# In[3]:


manager = CredentialManager(service_information) # initialize the OAuth 2.0 client 


# The redirect\_uri must:
# 1. Match one of the redirect URIs that were registered in AnyPoint API Manager for this client ("External API Tester") w/client\_id and client\_secret, above.
# 2. Actually have a listener on that URI (which the `manager.init_authorize_code_process()` launches for you.

# In[4]:


redirect_uri = 'http://127.0.0.1:5432/oauth2client'


# The Authorization Code flow does a bunch of browser redirects so that the Resource Owner (end user) credentials never flow through the client app itself. As you can see, you must click on the URL which opens another browser tab where the user login flow happens.

# In[5]:


authUrl = manager.init_authorize_code_process(redirect_uri, 'state_test')


# In[6]:


print('Opening this url in your browser: %s'%authUrl)
webbrowser.open_new(authUrl)


# Upon successfully authentication and authorizing in the new tab, you'll see this message: 
# 
# ```Response received ({"state": "state_test", "code": "<random string>"}). Result was transmitted to the original thread. You can close this window.```

# In[7]:


code = manager.wait_and_terminate_authorize_code_process()


# In[8]:


print('code = %s'%code)


# In[9]:


manager.init_with_authorize_code(redirect_uri, code)


# The Authorization code flow gets the code via a the request\_uri callback and then sends the code to the AS which returns back the access token. Since this library overloads the Python requests library, rather than exposing the access token to you, `init_with_authorize_code()` just sticks it straight into the Authorization HTTP header (which can be found in a "private" variable:

# In[10]:


manager._session.headers


# Finally, after this brief amount of basically one-time setup. Now you are read to actually issue the HTTP request to the Resource Server. This part is really easy (`manager.get()` is just `requests.get()` with the headers already set up for you):

# In[11]:



url = "https://columbia-demo-echo.cloudhub.io/v1/api/things"

response = manager.get(url)
print('status %s'%response.status_code)
print(response.headers)


# In[12]:


print(response.text)


# This is a weird API in that it is echoing back information that is not normally shared with the client app, namely, the result of validating the Bearer Token that the client provided. But let's crack open that JSON response just a little anyway. First, let's look at the definition of a Thing object from the RAML:
# ```
# #%RAML 1.0 DataType
# type: object
# properties:
#   authorization:
#     type: string  
#   access_token:
#     type: string
#   user: 
#     type: string
#   tokenContext: 
#     type: string
#   groups: 
#     type: string
#   scopes:
#     type: string
#   client_id:
#     type: string
#   client_name:
#     type: string
#   http_method:
#     type: string
#   http_request_uri:
#     type: string
#   x_forwarded_for:
#     type: string
# example:
#   authorization: Bearer abcdefghi123456
#   access_token: NONE
#   user: fred@columbia.edu
#   tokenContext: foo bar
#   groups: g1 g2demo-echo
#   scopes: a b c
#   client_id: 64575d23b8504c9bb1e9e7ff558c3cd3
#   client_name: another authz demo app
#   http_method: GET
#   http_request_uri: /v1/api/things
#   x_forwarded_for: 123.45.6.7
# ```

# In[13]:


j = json.loads(response.text)
if j and 'tokenContext' in j:
    tc = json.loads(j['tokenContext'])
    if tc and 'expires_in' in tc:
        print("Access token expires in %d minutes."%(tc['expires_in']/60))
    


# Let's try a request where we don't have the correct scope and see what errors look like:

# In[14]:


response = manager.post(url)


# In[15]:


print('status %s'%response.status_code)


# In[16]:


print(response.text)


# # Refresh Tokens
# See the [documentation](https://github.com/antechrestos/OAuth2Client) for how to make use of refresh tokens. If you persist the refresh token, you can continue accessing the resource server without having to bug the user, after the access token expires, by getting a new one.

# In[17]:


print(manager.refresh_token)


# In[18]:


rt = manager.refresh_token
newManager = CredentialManager(service_information)


# In[19]:


newManager.init_with_token(rt)


# In[20]:


print(newManager._session.headers)


# In[21]:


newResponse = newManager.get(url)
print('status %s'%newResponse.status_code)
print(newResponse.headers)
print(newResponse.text)


# In[22]:


print("We've refreshed and now the old access token (%s) is replaced by a new token (%s)"%
    (manager._session.headers['Authorization'][len('Bearer '):],
    newManager._session.headers['Authorization'][len('Bearer '):]))


# In[23]:


resp = manager.get(url)
print('see if the old token still works: %s'%resp.status_code)


# In[32]:


# force an rate limiting error by trying to hit the API more than 10 times in a minute:
for i in range(100):
    resp = manager.get(url)
    if resp.status_code == 200:
        print(i)
    else:
        print('status %s: %s'%(resp.status_code,resp.text))
        break

