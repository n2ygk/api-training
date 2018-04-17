### 2018-04-17
* **N.B.** Many things have changed and are not yet corrected here:
  * We no longer use Mulesoft for our API service. This is not yet reflected in the demo apps.
  * Many credentials in the demo apps are probably incorrect.

* use python venv and requirements.txt

* Updates to demo-echo-client-py.ipynb
   * This is the only app that has been partially updated to at least allow us to test OAuth 2.0
   * Make oauth_server more easily configurable
   * Disable SSL validation when using the dev oauth server which is self-signed
   * Replace OAuth 2 demo credentials
