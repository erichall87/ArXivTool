# ArXivTool

This is a project which currently (Apr 25) will scrape ArXiv 
emails from Gmail (`ScrapeEmails.py`) and parse the emails into 
a json corpus of recent ArXiv papers. Another script (`AbstractAnalysis.py`)
does some basic Latent Semantic Analysis (LSA) to embed the abstracts
into a lower dimensional space.

##Obtaining OAuth2 Credentials for Gmail API

In order to use the `ScrapeEmails.py` you will need the proper credentials to use the Google API. To do this, follow
the following instructions

- Navigate to (https://console.developers.google.com/project)
- Create a new project, named ArXiv Tool. 
- Enter Arxiv Tool project, go to the credentials page 
- "Create Credentials" and choose OAuth2 client ID.
- Choose other for type of application and call the type "Python Project" or something like that, and hit create.
- A pop-up displaying your credentials will be shown, hit OK
- These credentials will now show up on your credentials page, hit the download button and put into the main folder of this project
- Rename credentials file as "client_secret.json"
- The first time you run `ScrapeEmails.py` you will be prompted to log-in to your Gmail account, but should be set after that
- Be careful not to include sensitive information into your github repo. The `.gitignore` file is set up to ignore the .credentials folder that is made in `ScrapeEmails.py` and the client_secret.json, but other files could be pushed to your repo
- In order to use the Google API you will need to first run this command `pip install --upgrade google-api-python-client`

##Using `ScrapeEmail.py`






