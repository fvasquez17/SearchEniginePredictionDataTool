# SearchEniginePredictionDataTool
This tool allows user to take keywords off a Google Spreadsheet for data collection and analysis. The tool will take the keywords and run it through Google and Bing APIs to retrieve the search predictions. Then run the predictions through AWS Comprehend API to collect the sentimental analysis. This project also includes an automated script to run daily by itself on a cloud such as EC2 to collect data over long periods of time.
There are two versions of this program "Search Prediction Scraper V1" is the manually GUI and the "PyAutomator" is the code that will schedule the script to run daily as long as the KeyWords.csv has been retrived which can be done in the GUI 
Google Sheet with the keywords should be formatted with only two Columns A->"KeyWord" and B->"Language" you can have as many rows as you want
EXAMPLE SHEETS : https://docs.google.com/spreadsheets/d/1fECOr7nF2cDSM960yI-tZtAC2E3y7HiVUm9lzx68XR8/edit#gid=0
Google Sheet will contain the DOC ID and the gid in the URL to reference 
IMPORTANT in order to run this code all the pip installs have to be done 
\/\/\/\/\/\/\/\/
pip install boto3
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
pip install pandas
pip install --uprade pip
pip install --upgrade google-api-python-client
pip install google
pip install google-cloud-translate==2.0.1
pip install --upgrade google-cloud-translate
pip install xmltodict
pip install schedule
pip install langdetect
https://cloud.google.com/translate/docs/setup
tps://cloud.google.com/docs/authentication/getting-started
https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html(Must Download for AWS sentiment analysis)
https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-creds


@AUTHORS of this Tool
Freddy Vasquez
Srujan Vepuri
Prince Owoborode
Jade Lathbridge
