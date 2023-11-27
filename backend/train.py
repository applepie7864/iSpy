from keras.applications import vgg16
from keras.applications.mobilenet import preprocess_input
from keras.layers import Dense, GlobalAveragePooling2D
from keras.models import Model
from keras.preprocessing.image import ImageDataGenerator
import database_interaction

# add final layers for recognition and customizes vgg16 model 
def add_layers(base_model, num_classes):
    """
        :type base_model: VGG16
              num_classes: int
        :rtype: N/A
    """
    model = base_model.output
    model = GlobalAveragePooling2D()(model)
    model = Dense(1024, activation='relu')(model)
    model = Dense(1024, activation='relu')(model)
    model = Dense(512, activation='relu')(model)
    model = Dense(num_classes, activation='softmax')(model)
    return model

# function to train the model
def train():
    """
        :type: N/A
        :rtype: N/A
    """
    # edit for gcs
    num_classes = 2 # get num_ppl
    data_dir = '../test-images'
    
    datagen = ImageDataGenerator(
        preprocessing_function=preprocess_input
    )

    data = datagen.flow_from_directory(
        data_dir,
        target_size = (224, 224),
        color_mode = 'rgb',
        batch_size = 32,
        class_mode = 'categorical',
        shuffle = True
    )
    
    base_model = vgg16.VGG16(
        include_top = False
    )

    custom = add_layers(base_model, num_classes)
    model = Model(inputs = base_model.input, outputs = custom)
    
    index = 0
    for layer in model.layers:
        if index < 19:
            layer.trainable = False
        else:
            layer.trainable = True
    
    model.compile(
        optimizer = 'Adam',
        loss = 'categorical_crossentropy',
        metrics = ['accuracy']
    )
    
    model.fit(
        data,
        batch_size = 1,
        verbose = 1,
        epochs = 20
    )
    
    model.save('./model.h5')
    database_interaction.write_labels(data.class_indices)


if __name__ == '__main__':
    train()