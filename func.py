import pickle
from numpy import asarray
from xgboost import XGBRegressor

# Load model
model = pickle.load(open('Model/CatBoost.sav', 'rb'))

# Fungsi membuat kolom hasil prediksi Random Forest
def prediksi_adaptive(list_nilai):
    row = list_nilai
    new_data = asarray([row])

    # make a prediction
    yhat = model.predict(new_data)

    if yhat > 100:
        yhat = 100

    return yhat