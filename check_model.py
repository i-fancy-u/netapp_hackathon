import joblib

model = joblib.load("storage_model.pkl")
print("Model expects features in this order:")
try:
    print(model.feature_names_in_)
except:
    print("Model does not store feature names. It uses the order given during training.")
