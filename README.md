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

A lot of the code in `ScrapeEmail.py` was taken from the Google API python quickstart tutorial fond [here](https://developers.google.com/gmail/api/quickstart/python#step_3_set_up_the_sample)

The main function takes two arguments, the query format for your email and a saving option. 
The query string should be what you would type into the Gmail search to get ONLY your ArXiv notification emails.
For instance if you have a folder just for these emails name ArXiv, the query would be "label:ArXiv". Another good place to start might be "from:no-reply@arxiv.org". The saving option denotes whether or not you want to save the parsed emails to a json file or not.

##Using `AbstractAnalysis.py`

Given that you have a json of abstracts saved as `FullCorpus.json` in the project folder. You can simply run `AbstractAnalysis.py` to get a 500 dimensional representation of all the abstracts. For now I recommend running this
script from an IDE or IPython environment so you can explore the embeddings and/or use the matrix of distances to find similar abstracts to abstracts of interest.






