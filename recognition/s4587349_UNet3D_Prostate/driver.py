import os
import nibabel as nib
import tensorflow as tf
from tensorflow import keras
import numpy as np

import unet_model as mdl
import support_methods as sm

"""
Sources
"""

"""
All images are 3D MRi's of shape (256, 256, 128) in nibabel format (*.nii.gz).
Data and labels are in numpy arrays, float64.
MRi voxel values vary from 0.0 upwards.
The labels have 6 classes, labelled from 0.0 to 5.0.
"""
dim = (256, 256, 128)
CLASSES = 6


def main():
    """ """
    """ Show reachable GPUs"""
    print(tf.config.list_physical_devices(device_type='GPU'))    #todo remove

    """ 
    Patients had from 1 to 8 MRI scans, a week apart. As scans for a given
    patient are expected to be similar each patients scans have been considered as
    one sample. All up there are 38 patients, and these have been distributed
    between training, validation and testing at 27:7:4 with the number of images
    at 158:35:18.
    """

    """ DATA SOURCES"""

    # """ Data Sources Windows D: """
    X_TRAIN_DIR = 'D:\\prostate\\mr_train'
    X_VALIDATE_DIR = 'D:\\prostate\\mr_validate'
    X_TEST_DIR = 'D:\\prostate\\mr_test'
    # Label sources
    Y_TRAIN_DIR = 'D:\\prostate\\label_train'
    Y_VALIDATE_DIR = 'D:\\prostate\\label_validate'
    Y_TEST_DIR = 'D:\\prostate\\label_test'

    """ Example data and label  """
    img_mr = (nib.load(X_TRAIN_DIR + '\\Case_004_Week0_LFOV.nii.gz')).get_fdata()
    img_label = (nib.load(Y_TRAIN_DIR + '\\Case_004_Week0_SEMANTIC_LFOV.nii.gz')).get_fdata()
    img_label2 = (nib.load(Y_TRAIN_DIR + '\\Case_011_Week7_SEMANTIC_LFOV.nii.gz')).get_fdata()

    """ Full data & label addresses in D: """
    image_train = sorted([os.path.join(os.getcwd(), 'D:\\prostate\\mr_train', x)
                          for x in os.listdir('D:\\prostate\\mr_train')])
    image_validate = sorted([os.path.join(os.getcwd(), 'D:\\prostate\\mr_validate', x)
                             for x in os.listdir('D:\\prostate\\mr_validate')])
    image_test = sorted([os.path.join(os.getcwd(), 'D:\\prostate\\mr_test', x)
                         for x in os.listdir('D:\\prostate\\mr_test')])
    label_train = sorted([os.path.join(os.getcwd(), 'D:\\prostate\\label_train', x)
                          for x in os.listdir('D:\\prostate\\label_train')])
    label_validate = sorted([os.path.join(os.getcwd(), 'D:\\prostate\\label_validate', x)
                             for x in os.listdir('D:\\prostate\\label_validate')])
    label_test = sorted([os.path.join(os.getcwd(), 'D:\\prostate\\label_test', x)
                         for x in os.listdir('D:\\prostate\\label_test')])

    """ Small test set D:"""
    data_small_train = sorted([os.path.join(os.getcwd(), 'D:\\p\\data', x)
                               for x in os.listdir('D:\\p\\data')])
    label_small_train = sorted([os.path.join(os.getcwd(), 'D:\\p\\label', x)
                                for x in os.listdir('D:\\p\\label')])
    data_small_validate = sorted([os.path.join(os.getcwd(), 'D:\\p\\data_validate', x)
                                  for x in os.listdir('D:\\p\\data_validate')])
    label_small_validate = sorted([os.path.join(os.getcwd(), 'D:\\p\\label_validate', x)
                                   for x in os.listdir('D:\\p\\label_validate')])
    data_small_test = sorted([os.path.join(os.getcwd(), 'D:\\p\\data_test', x)
                              for x in os.listdir('D:\\p\\data_test')])
    label_small_test = sorted([os.path.join(os.getcwd(), 'D:\\p\\label_test', x)
                               for x in os.listdir('D:\\p\\label_test')])

    """ Data Sources Windows C: """
    # # Data sources
    # X_TRAIN_DIR = 'C:\\prostate\\mr_train'
    # X_VALIDATE_DIR = 'C:\\prostate\\mr_validate'
    # X_TEST_DIR = 'C:\\prostate\\mr_test'
    # # Label sources
    # Y_TRAIN_DIR = 'C:\\prostate\\label_train'
    # Y_VALIDATE_DIR = 'C:\\prostate\\label_validate'
    # Y_TEST_DIR = 'C:\\prostate\\label_test'

    # """ Full data & label addresses in C: """
    # image_train = sorted([os.path.join(os.getcwd(), 'C:\\prostate\\mr_train', x)
    #                       for x in os.listdir('C:\\prostate\\mr_train')])
    # image_validate = sorted([os.path.join(os.getcwd(), 'C:\\prostate\\mr_validate', x)
    #                          for x in os.listdir('C:\\prostate\\mr_validate')])
    # image_test = sorted([os.path.join(os.getcwd(), 'C:\\prostate\\mr_test', x)
    #                      for x in os.listdir('C:\\prostate\\mr_test')])
    #
    #
    # label_train = sorted([os.path.join(os.getcwd(), 'C:\\prostate\\label_train', x)
    #                       for x in os.listdir('C:\\prostate\\label_train')])
    # label_validate = sorted([os.path.join(os.getcwd(), 'C:\\prostate\\label_validate', x)
    #                          for x in os.listdir('C:\\prostate\\label_validate')])
    # label_test = sorted([os.path.join(os.getcwd(), 'C:\\prostate\\label_test', x)
    #                      for x in os.listdir('C:\\prostate\\label_test')])

    # """ Small test set C:"""
    # data_small_train = sorted([os.path.join(os.getcwd(), 'C:\\p\\data', x)
    #                            for x in os.listdir('C:\\p\\data')])
    # label_small_train = sorted([os.path.join(os.getcwd(), 'C:\\p\\label', x)
    #                             for x in os.listdir('C:\\p\\label')])
    # data_small_validate = sorted([os.path.join(os.getcwd(), 'C:\\p\\data_validate', x)
    #                               for x in os.listdir('C:\\p\\data_validate')])
    # label_small_validate = sorted([os.path.join(os.getcwd(), 'C:\\p\\label_validate', x)
    #                                for x in os.listdir('C:\\p\\label_validate')])
    # data_small_test = sorted([os.path.join(os.getcwd(), 'C:\\p\\data_test', x)
    #                           for x in os.listdir('C:\\p\\data_test')])
    # label_small_test = sorted([os.path.join(os.getcwd(), 'C:\\p\\label_test', x)
    #                            for x in os.listdir('C:\\p\\label_test')])

    """ Data sources Goliath """
    # # Data sources
    # X_TRAIN_DIR = 'prostate/mr_train'
    # X_VALIDATE_DIR = 'prostate/mr_validate'
    # X_TEST_DIR = 'prostate/mr_test'
    # # Label sources
    # Y_TRAIN_DIR = 'prostate?label_train'
    # Y_VALIDATE_DIR = 'prostate/label_validate'
    # Y_TEST_DIR = 'prostate/label_test'
    #
    # """ Full data & label addresses in Goliath """
    # image_train = sorted([os.path.join(os.getcwd(), 'prostate/mr_train', x)
    #                       for x in os.listdir('prostate/mr_train')])
    # image_validate = sorted([os.path.join(os.getcwd(), 'prostate/mr_validate', x)
    #                          for x in os.listdir('prostate/mr_validate')])
    # image_test = sorted([os.path.join(os.getcwd(), 'prostate/mr_test', x)
    #                      for x in os.listdir('prostate/mr_test')])
    # label_train = sorted([os.path.join(os.getcwd(), 'prostate/label_train', x)
    #                       for x in os.listdir('prostate/label_train')])
    # label_validate = sorted([os.path.join(os.getcwd(), 'prostate/label_validate', x)
    #                          for x in os.listdir('prostate/label_validate')])
    # label_test = sorted([os.path.join(os.getcwd(), 'prostate/label_test', x)
    #                      for x in os.listdir('prostate/label_test')])
    #
    # """ Small test set Goliath"""
    # data_small_train = sorted([os.path.join(os.getcwd(), 'p/data', x)
    #                            for x in os.listdir('p/data')])
    # label_small_train = sorted([os.path.join(os.getcwd(), 'p/label', x)
    #                             for x in os.listdir('p/label')])
    # data_small_validate = sorted([os.path.join(os.getcwd(), 'p/data_validate', x)
    #                               for x in os.listdir('p/data_validate')])
    # label_small_validate = sorted([os.path.join(os.getcwd(), 'p/label_validate', x)
    #                                for x in os.listdir('p/label_validate')])
    # data_small_test = sorted([os.path.join(os.getcwd(), 'p/data_test', x)
    #                           for x in os.listdir('p/data_test')])
    # label_small_test = sorted([os.path.join(os.getcwd(), 'p/label_test', x)
    #                            for x in os.listdir('p/label_test')])

    # """ Test generator, try to visualise - small"""
    # training_generator = sm.ProstateSequence(data_small_train,
    #                                          label_small_train, batch_size=1)
    # validation_generator = sm.ProstateSequence(data_small_validate,
    #                                         label_small_validate, batch_size=1)


    """ Test generator, try to visualise - full"""
    training_generator = sm.ProstateSequence(image_train,
                                             label_train, batch_size=1)
    validation_generator = sm.ProstateSequence(image_validate,
                                               label_validate, batch_size=1)
    pred_generator = sm.ProstateSequence(image_test, label_test, batch_size=1, training=False)




    # print(*(n for n in training_generator))  # prints but seems to print series of np.zeros
    # need to visualise

    # """ TESTING SPEED OF TRAINING GENERATOR, ABOUT 1 BATCH/SEC ON THIS SYSTEM
    # 157 SAMPLES TAKES ABOUT 2.5 MIN FOR 1 EPOCH TO PASS SAMPLES TO MODEL ... ON THIS SYSTEM"""
    # xtg = training_generator
    # print(type(xtg))
    # print("xtg ", xtg)
    # print(*(n for n in xtg))










    # """ MODEL """
    # # todo update with BN, Relu
    model = mdl.unet3d(inputsize=(256, 256, 128, 1), kernelSize=3)

    # SMALL 3 SAMPLE MODEL
    # model = mdl.unet3d_small(inputsize= (256,256,128,1), kernelSize=3)  #attempt to run smaller model

    model.compile(optimizer='adam', loss='categorical_crossentropy',
                  metrics=['accuracy'])
    model.summary(print_fn=sm.model_summary_print)  #todo correct
    model.summary()

    with open('model_sum2.txt', 'w') as ff:
        model.summary(print_fn=lambda x: ff.write(x + '\n'))
        # https://newbedev.com/how-to-save-model-summary-to-file-in-keras

    keras.utils.plot_model(model, "unet3d.png", show_shapes=True)

    # WORKING HERE TESTING SUMMARY PLOT
    history = model.fit(training_generator, validation_data=validation_generator, batch_size=1, verbose=2, epochs=3)
    sm.plot_loss(history)
    sm.plot_accuracy(history)
    pred = model.predict(pred_generator)  #todo was model_predict(...)

    # CALCULATE AND PRINT DSC COEF FOR EACH CLASS, AND FOR AVERAGE
    pred_argmax = np.argmax(pred, axis=4)

    # Get an array of test labels -> (18, 256, 256, 128)
    y_true = np.empty((len(label_test), 256, 256, 128))
    for i, id in enumerate(label_test):
        y2 = sm.read_nii(id)
        y_true[i,] = y2
    # calculate & print dsc
    dice = sm.dice_coef_multiclass(y_true, pred_argmax, 6)

    # WORKING HERE 557
    # PRINT SLICES OF y_true and  y_pred
    sm.slices_pred(y_true, "y_true.png")


    # # check prep is working
    # print("prep ", pred.shape) #(18, 256, 256, 128, 6)
    # print(pred)    #  1.01947702e-01 1.02931291e-01]]]]]
    # print(type(pred))  #<class 'numpy.ndarray'>


    #

    # # test print of list of label names which include path
    # print(label_test)

    # todo
    # generator / sequence
    # normalise data, - mean / stdev  - tf.keras.utils.normalize(
    # https://www.tensorflow.org/api_docs/python/tf/keras/utils/normalize
    # https://www.tensorflow.org/api_docs/python/tf/keras/utils/to_categorical
    # sort / shuffle
    # model 3d
    # dsc
    # driver import model and show example
    # model_checkpoint
    # model predict
    # model save / recover
    # plot predicted labels post
    # save wts, load?
    # how to stop trainiang when reach dsc target? callbackz
    # readme
    # augmentation (distortion, slight rotations, horizontal flip
    #   translation (flip?), need to do same to label but siu's does that auto
    #   siu's github library
    #   see augmentation lib in lab sheets
    #   https://github.com/SiyuLiu0329/pyimgaug3d
    # cross validation
    # delete jupyter files from repo
    # save images to add to readme
    # print model.summary() https://stackoverflow.com/questions/45199047/how-to-save-model-summary-to-file-in-keras/45199301
    # todo Issues non -critical
    # 1. Not printing images in subplots, works in jupyter
    # plot image slices & labels, pre - ensure access (try 3d later)
    # slices(img_mr)





    """ Code to investigate data and images """


    # """ PRINT SLICES OF ONE HOT ENCODED LABEL"""
    # ohe = tf.keras.utils.to_categorical(img_label, num_classes = 6)
    # print(img_label.shape, ohe.shape)
    # print(type(img_label), type(img_mr), type(ohe))
    # sm.slices_ohe(ohe)

    # """ PRINT SLICES OF LABEL"""
    # sm.slices(img_label)

    # """ PRINT SLICES OF DATA """
    # sm.slices(img_mr)

    # #Checks dimensions of each image and label against expected.
    # sm.dim_per_directory()

    # # Display raw data and label info
    # sm.data_info()


if __name__ == '__main__':
    main()
