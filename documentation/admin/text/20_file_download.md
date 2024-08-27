
# Download Labled Dataset


Files can be downloaded via the Tweeti API by going to `<your url>/api/tweets/` (e.g. `https://www.example.com/api/tweets/`.


## Forbidden

If you are not logged in or do not have admin rights, you will see a page with a `403 Forbidden` message (see Figure \ref{fig:forbidden}). In that case, you can click the "Log in" button in the top right corner to log in as an admin user.


![Defaul 404 page when a non-admin user tries to open the download page. \label{fig:forbidden}](resources/images/forbidden.png)


## Get Dataset

When you log in as an admin, you can see a JSON file and press the "GET" button to download the labelled dataset, see figure \ref{fig:download}.


![Download page when logged in as an admin, use the "GET" button to downlaod the labelled dataset. \label{fig:download}](resources/images/download.png)

\newpage{}

## API via Script

The Tweeti API is also callable via a script, for example use the following script to download the labelled dataset.

``` Python
import requests
import pandas as pd

auth = HTTPBasicAuth("<user name>", "<user password>")
request = requests.get('https://<your url>/api/tweets/', auth=auth)

demo_df = pd.DataFrame.from_dict(json.loads(request.text))
demo_df.to_csv("some_file_name.csv")
```



\newpage{}
