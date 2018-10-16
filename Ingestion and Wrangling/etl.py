import requests
import zipfile

# download the Kiva snapshot in csv format to local directory
url = "http://s3.kiva.org/snapshots/kiva_ds_csv.zip"
download = requests.get(url, allow_redirects=True)
open('kiva_ds_csv.zip', 'wb').write(download.content)

# unzip the file to local directory
kiva_csv = zipfile.ZipFile('kiva_ds_csv.zip', 'r')
kiva_csv.extractall()
kiva_csv.close()
