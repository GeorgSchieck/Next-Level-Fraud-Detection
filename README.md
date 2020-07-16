# Next-Level-Fraud-Detection
Data Exploration Projekt 2020

**Gruppenmitglieder:**

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

1. Navigate to the folder containing the dockerfile using a terminal
2. Execute the command "docker build -t de_api".
3. Use the command "docker run -d -p 1213:1213 de_api" to run the container.
4. The endpoints are http://0.0.0.0:1213/post/tx
5. The payload is: {"amount":[float],"type":["PAYMENT","TRANSFER","CASHIN”,”DEBIT”,”CAS HOUT”],”nameOrig” :[nameOrig(ktonr.ausDB)],”nameDest”:[nameDest(ktonr.ausDB)]}
6. Use  http:0.0.0.0:1213/post/model  as  an  endpoint  to train a new model. This can take some time and will return the duration needed to training.

**Use the server-based version:**

Alternatively a version based on a server can be used. If this is the case the endpoints "http://h2655330.stratoserver.net:1213/post/tx"   and"http://h2655330.stratoserver.net:1213/post/model" are to be considered. The payload will remain the same as stated above.

**Locally run the website:**

1. Navigate to the folder containing the package.json using a terminal.
2. Execute the command "npm install" (node.js needs to be installed)
3. Run the website using the command "npm run dev"

**Notes:**

1. It is recommended to use the website at ""http://fraud-detection.schmidt-development.de/".
2."http://h2655330.stratoserver.net:1213/post/model" will not work on the server because not enough RAM is provided.

