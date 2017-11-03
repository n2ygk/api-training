# API Training

Some RESTful API training using [Jupyter](http://jupyter.org) Notebooks.

## Contents

- [demo-clientid-client](#demo-clientid-client)
- [demo-echo-client](#demo-echo-client)
- [demo-jsonapi-client](#demo-jsonapi-client)
- [Installing and running Jupyter on your laptop](#installing-and-running-jupyter-on-your-laptop)
	- [Adding JavaScript (node.js)](#adding-javascript-nodejs)
	- [Adding R](#adding-r)
- [Author](#author)
- [LICENSE](#license)

See [instructions for installing Jupyter](#installing-and-running-jupyter-on-your-laptop) below and then:

## demo-clientid-client

Here are some notebooks that demonstrate using the demo-clientid API and the OAuth 2.0 Client Credentials grant:

- demo-clientid-client-js.ipynb (node.js JavaScript)
  - [notebook file](demo-clientid-client-js.ipynb)
  - [open in local notebook](http://localhost:8888/notebooks/demo-clientid-client-js.ipynb) (must be running `jupyter notebook`)

- demo-clientid-client-jquery.ipynb (node.js jquery)
  - [notebook file](demo-clientid-client-jquery.ipynb)
  - [open in local notebook](http://localhost:8888/notebooks/demo-clientid-client-jquery.ipynb) (must be running `jupyter notebook`)

- demo-clientid-client-jquery.html (in-browser jquery)
  - [HTML file](demo-clientid-client-jquery.html)
  - [open in browser](http://localhost:8888/view/demo-clientid-client-jquery.html) (must be running `jupyter notebook`)

## demo-echo-client

Here's a notebook that demonstrates using the demo-echo API with the Authorization Code grant:

- demo-echo-client-py.ipynb (Python)
  - [notebook file](demo-echo-client-py.ipynb)
  - [open in local notebook](http://localhost:8888/notebooks/demo-echo-client-py.ipynb) (must be running `jupyter notebook`)


## demo-jsonapi-client

This set of notebooks demonstrates the [{json:api}](http://jsonapi.org) RESTful request/response standard.
See https://github.com/n2ygk/mulesoft-demo-jsonapi for a demo server that runs on Mulesoft. This client uses
said deployed server. Credentials for it are in the notebook. Don't worry; it's rate-limited.

- demo-jsonapi-client-py.ipynb (Python)
  - [notebook file](demo-jsonapi-client-py.ipynb)
  - [open in local notebook](http://localhost:8888/notebooks/demo-jsonapi-client-py.ipynb) (must be running `jupyter notebook`)

## Installing and running Jupyter on your laptop

[Installing Jupyter](https://jupyter.org/install.html) gets you a basic Python system:

```
git clone git@github.com:n2ygk/api-training.git
cd api-training
pip3 install jupyter
jupyter notebook
```

Your browser will open a new window with the Jupyter notebook browser.

### Adding JavaScript (node.js)

See https://github.com/n-riesco/ijavascript

For MacOS (need a back-level version of node.js to work with ijavascript):

```
brew install node@6
brew link --force node@6
sudo pip install --upgrade pyzmq jupyter
sudo npm install -g ijavascript
ijsinstall
```

Modules installed with `npm install -g` [do not work](https://github.com/n-riesco/ijavascript/issues/4).
You have to make them local to the home directory of your juptyer server (e.g. this directory)
and the node_modules directory must pre-exist or npm will complain. See [package.json](package.json)
for the list of added modules.

```
mkdir node_modules
npm install
```

### Adding R

This has nothing to do with APIs -- just playing around with Jupyter

See the instructions at https://irkernel.github.io/installation/
```
install.packages(c('repr', 'IRdisplay', 'evaluate', 'crayon', 'pbdZMQ', 'devtools', 'uuid', 'digest'))
devtools::install_github('IRkernel/IRkernel')
IRkernel::installspec(user = FALSE)
```

I've added two examples from the Stats course I took, including the data files they need.

- Stats HW05.R.ipynb (R)
  - [notebook file](Stats%20HW05.R.ipynb)
  - [open in local notebook](http://localhost:8888/notebooks/Stats%20HW05.R.ipynb)
- Stats HW11.R.ipynb (R)
  - [notebook file](Stats%20HW11.R.ipynb)
  - [open in local notebook](http://localhost:8888/notebooks/Stats%20HW11.R.ipynb)

## Author
Alan Crosswell

Copyright (c) 2017 The Trustees of Columbia University in the City of New York

## LICENSE

Licensed under the [Apache License, Version 2.0](LICENSE) (the "License"); you may not use this file
except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied. See the License for the specific language governing
permissions and limitations under the License.
