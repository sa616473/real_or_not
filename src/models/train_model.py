from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.models import model_from_json


def save_model(model, title=''):
    '''
    This function saves the model into HDF5 format and weights
    into a JSON file
    '''
    model_json = model.to_json()
    with open("../src/models/saved_models/model_{}.json".format(title), "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights("../src/models/saved_models/model_{}.h5".format(title))
    print("Saved model to disk")

def callbacks():
    '''
    Early stopping callbacks
    '''
    callback = EarlyStopping(
    monitor='val_loss', min_delta=0, patience=10, verbose=0, mode='auto',
    baseline=None, restore_best_weights=True)
    return callback