# Next-Level-Fraud-Detection
Data Exploration Projekt 2020

Locally execute the code:

1. Navigate to the folder containing the dockerfile using a terminal
2. Execute the command "docker build -t de_api".
3. Use the command "docker run -d -p 1213:1213 de_api" to run the container.
4. The endpoints are http:0.0.0.0:1213/post/tx
5. The payload is: {"amount":[float],"type":["PAYMENT","TRANSFER","CASHIN”,”DEBIT”,”CAS HOUT”],”nameOrig” :[nameOrig(ktonr.ausDB)],”nameDest”:[nameDest(ktonr.ausDB)]}
6. Use  http:0.0.0.0:1213/post/model  as  an  endpoint  totrain a new model. This can take some time and willreturn the duration needed to training.
