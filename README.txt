********************************************************************
********************************************************************
*
* Alarm prediction project
* Authors:
*      Vladyslav Vitisk - team leader
*      Danyliuk Yevheniia
*      Yefremenko Anastasiia
*      Polishchuk Maksym
*
********************************************************************
********************************************************************

contact e-mail of team leader: vladyslav.vitisk@ukma.edu.ua

*
* BEFORE THE START:
* After cloning project from gitHub insert
* 1. weather dataset into 'data/weather'
* 2. events dataset into 'data/events'
* 3. regions dataset into 'data/regions'
*

*
* REQUIRED PYTHON PACKAGES THAT CAN BE DOWNLOADED USING PIP:
*
*   Pandas
*   bs4
*   nltk
*   jupyter
*   sklearn
*   num2words
*   pickle
*   datetime
*   re
*   requests
*   json
*   flask
*   uwsgi
*


*
* PREPARING MODEL:
*
*   All vectors and ISW dataset is already prepared for future usage.
*   But to rerun all code you have to run prepareBaseDate() method from scrapper.py
*   in main folder that will download all available reports from 24-02-22 to 25-01-23.
*   Then you should run all cells from CreateDataSetOfISW.ipynb, preprocessing_1.ipynb,
*   preprocessing_2.ipynb.
*
*   NEXT CODE IS REQUIRED FOR FURTHER WORK
*
*   To merge datasets run all cells of code from 3_prepare_final_dataset.ipynb
*
*   Then run CreateNewFeatures.ipynb(it's required for visualization and further generated features
*   will be removed in next file, because of problems further modeling and prediction)
*
*   To create models run trainingModel.ipynb
* POSSIBLE PROBLEMS:
*   Merging and training require big amount of Memory, so be sure that you have enough.
*   Also we don't recommend to run "Tuning the hyper-parameters" section, because it requires even more memory
*   so this section of code is not finished, but if you will have enough memory to run cell with this code:
        best_clf = clf.fit(x_train_df, y_train_df)
*   from this section, even if results would be bad, you can contact Vladyslav Vitisk on his e-mail,
*   so we will improve our code.


*
* VISUALISATION:
*
*   After running all required code from PREPARING MODEL section you can run code to some visualisation.
*   Each visualisation have own file in 'visualisation' folder
*




*
* DEPLOYING TO SERVER:
*
*   After preparing server(running all required code from PREPARING MODEL section or moving folder with all models prepared)
*   you have to run GeneratePredictions.py everyHour.
*   For example we run this code on our server on each 59th minute of every hour using corn and this command:

        59 * * * * cd /home/ubuntu/server && . bin/activate && python3 GeneratePredictions.py 2>&1 | logger -t mycmd

*   If you use this command you can check log how it works using next command:

        grep 'mycmd' /var/log/syslog

*   If everything is fine, you can start uwsgi server using next command:

        uwsgi --http 0.0.0.0:8000 --wsgi-file alarm_api.py --callable app --processes 4 --threads 2 --stats 127.0.0.1:9191

*   After starting server you can send requests. Address to send request to get prediction looks like this:

        http://*_ip_address_of_your_server_*:8000/forecast/api/v1

*   To send request you have to set "Content-Type" to "application/json" and send json, that look like that:

        {
            "location": "*REGION_NAME_TO_GET_PREDICTIONS*"
        }

*   If location is "all" - returns json with all regions, else check if there is Region centre with given name
*   and send prediction if exists
*





