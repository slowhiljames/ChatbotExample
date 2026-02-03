from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

def build_model(input_size, output_size):
    model = Sequential()
    model.add(Dense(128, activation='relu', input_shape=(input_size,)))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(output_size, activation='softmax'))

    model.compile(
        loss='sparse_categorical_crossentropy',
        optimizer='adam',
        metrics=['accuracy']
    )
    return model
