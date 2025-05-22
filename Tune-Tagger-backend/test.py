import tensorflow as tf
# from tf.keras import load_model

model = tf.keras.models.load_model('music_detection_model.keras')

print(model.summary())
