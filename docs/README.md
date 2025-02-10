# Formula 1 Qualif-AI
#### V1.0

## Estimate future Formula 1 qualifying results using ML (XGBoost Regression)
![F1_UI](https://github.com/user-attachments/assets/fb577ccd-3e13-45aa-bdf7-cf0aa4185ab6)


## Usage

https://www.f1quali.online/

The user is given a choice between predicting results for a single driver or for all participants in a session. Shown below are the menus for both and example inputs. 

### Driver Prediction
https://github.com/user-attachments/assets/10a2d042-d3bd-470a-aa2a-3d0270f36414



### Session Prediction
https://github.com/user-attachments/assets/84aaae1c-0758-46e2-9646-06f82d8068d2



## Deep-Dive
The entire frontend UI is built using React. GET and POST requests are made to the backend server which runs a custom Python API using the trained model. The model used was an XGBoost Regressor from the open-source xgboost library in Python. I trained an instance of this model on a custom dataset which includes data from the past decade of the sport. 
The relevant data was obtained programatically from theOehrly's fastf1 Python library (https://github.com/theOehrly/Fast-F1). 
