# Web Services API examples for Python

This repository contains a simple example on how to use IPGPAY Web Services API using python. The example uses
`requests` library to create the HTTP POST requests but you are free to use anything that supports TLS 1.2 or later.

## Quick setup guide

To get started, we suggest you create a Python 3 virtual environment. Once there, execute:

1. `pip install -r requirements.txt`. This will install Django and requests library.

2. Make a copy of the `wsapisite/wsapisite/settings.local.py` and save it as `wsapisite/wsapisite/settings.py`.
If you use this setup on production, make sure you regenerate the secret key in this file.

3. Run migrations. In the wsapisite/ folder, execute `python manage.py migrate`. This will create the tables required
for having session related data in the website. The default setup will install a Sqlite3 database.

4. Set up environment variables.
    `WSAPI_CLIENT_ID` will be the client ID provided by your account manager
    `WSAPI_API_KEY` is the API key provided by your account manager. Keep this one safe.
    `WSAPI_API_HOST` endpoint used by the Web Services API. Generally this will be https://my.ipgpay.com
        
4. Start the server. Execute `python manage.py runserver`. The website will load on http://localhost:8000/

## Notes on using Web Services API.

Note that before you start, you need to add your development IP to the allowed IP list in the IPGPAY Gateway 
configuration.

If your environment variables are set correctly, you should be able to create test orders. You should then be able to
settle any orders you have created if they were of type auth. Any sales or settled auths can then be credited.

All of the other endpoints are working in the same way so implementing new ones should be easy. Feel free to submit
any improvements to this script to your account manager.

## TLDR

You can copy the wsapisite/example/wsapi module to your project and use it. Do note that this is still only an example
on how to use the Web Services API endpoints, not a complete SDK.
