# Next-Level-Fraud-Detection
Data Exploration Projekt 2020

**Projectmembers:**

Anabel Lilja, 
Bjarne Gerdes, 
Raphael Schmidt, 
Georg Schieck

**Motivation and Objective of this project:**

The Objective of this project is to develop and build a machine learning model which can be used to
detect and event prevent fraudulent transactions. Mobile payment methods have taken their place among the
most relevant ways pay in everyday life. At the same time fraudster are motivated to find new ways to overcome the
security measurements established by the financial institutes. PayPal reported a total loss of 1011 Million USD 
in a single year in 2017. Preventing the fraudulent transactions will minimize the loss in monetary value while also
raise the customer satisfaction which is the motivation for developing the above stated machine learning algorithm.

**Locally execute the code:**

1. Navigate to the folder "cd ./project_code/fraud_detector" containing the dockerfile using a terminal
2. Execute the command "docker build -t de_api .".
3. Use the command "docker run -d -p 1213:1213 de_api" to run the container.
4. The endpoints are http://0.0.0.0:1213/post/tx
5. The payload is: {"amount":[float],"type":["PAYMENT","TRANSFER","CASHIN”,”DEBIT”,”CAS HOUT”],”nameOrig” :[nameOrig(ktonr.ausDB)],”nameDest”:[nameDest(ktonr.ausDB)]}
6. Use  http://0.0.0.0:1213/post/model  as  an  endpoint  to train a new model. This can take some time and will return the duration needed to training.

If you want to train a new model, you need at least 18 GB of RAM for the Cross-Validation!

**Use the server-based version:**

Alternatively a version based on a server can be used. If this is the case the endpoints "http://h2655330.stratoserver.net:1213/post/tx" and "http://h2655330.stratoserver.net:1213/post/model" are to be considered. The payload will remain the same as stated above.

**Locally run the website:**

1. Navigate to the folder "cd ./project_code/website" containing the package.json using a terminal.
2. Execute the command "npm install" (node.js needs to be installed)
3. Run the website using the command "npm run dev"

**Accessing the data**

The data can be accessed by:
1. An SQL-Alchemy connection using the file ./project_code/fraud_detector/RequestHandlerData/ORM_Datamodel.py 
2. Online from kaggle.com (https://www.kaggle.com/ntnu-testimon/paysim1)
3. As a backup at https://drive.google.com/file/d/1dND0QN0Rb5JotDAO2AFRrhSQnMNCou_Q/view?usp=sharing

**Notes:**

1. It is recommended to use the website at "http://fraud-detection.schmidt-development.de/".
2. "http://h2655330.stratoserver.net:1213/post/model" will not work on the server because not enough RAM is provided.


