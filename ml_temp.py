import joblib


def load_nn_rf():
    import tensorflow as tf
    model1 = tf.keras.models.load_model("C:\\Users\\Hawki\\OneDrive\\Desktop\\models\\lstm_model.h5", compile=False)
    tokenizer1 = joblib.load("C:\\Users\\Hawki\\OneDrive\\Desktop\\models\\tokenizer.pkl")
    label_encoder1 = joblib.load("C:\\Users\\Hawki\\OneDrive\\Desktop\\models\\label_encoder.pkl")
    MAX_LEN = 100

    model2 = tf.keras.models.load_model("C:\\Users\\Hawki\\OneDrive\\Desktop\\models\\tf.h5", compile=False)
    tokenizer2 = joblib.load("C:\\Users\\Hawki\\OneDrive\\Desktop\\models\\tftokenizer.pkl")
    label_encoder2 = joblib.load("C:\\Users\\Hawki\\OneDrive\\Desktop\\models\\tflabel_encoder.pkl")
    return model1, tokenizer1, label_encoder1, MAX_LEN, model2, tokenizer2, label_encoder2


def predict_lstm_class(tokenizer, MAX_LEN, model, label_encoder, text):
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    sequence = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(sequence, maxlen=MAX_LEN)

    prediction = model.predict(padded)
    predicted_index = prediction.argmax(axis=1)[0]

    predicted_label = label_encoder.inverse_transform([predicted_index])[0]
    return predicted_label


def true_or_false(tokenizer, MAX_LEN, model, label_encoder, text):
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    sequence = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(sequence, maxlen=MAX_LEN)

    prediction = model.predict(padded)
    predicted_index = prediction.argmax(axis=1)[0]

    predicted_label = label_encoder.inverse_transform([predicted_index])[0]
    return predicted_label