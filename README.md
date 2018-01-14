# Jump careers Falcon App

To run the app-

* Install the setup into a virtual environment from the [requirements text file](https://github.com/suki2691/miscellaneous/blob/master/requirements.txt)
* Open a terminal and type `mongod` to ensure that the MongoDB server is active
* Run the file named [mongo_data.py](https://github.com/suki2691/miscellaneous/blob/master/mongo_data.py) to store the data into the database
* Then run the app file - [alt_app.py](https://github.com/suki2691/miscellaneous/blob/master/alt_app.py) by using the following command-
`gunicorn alt_app:app`
* The user input prompt will appear in the terminal. Please enter the first name whose first experience you wish to see
* The results will appear [here](http://127.0.0.1:8000/users)

## Update- 1/13/2018
* The data models for the MongoDB are now defined using MongoEngine
* After running the `gunicorn alt_app:app` in the terminal, the user's first working experience can be obtained by following this format- `http://127.0.0.1:8000/users?firstname=Jarrah`

