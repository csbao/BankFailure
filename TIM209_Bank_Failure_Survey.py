#!/usr/bin/env python

import TIM209_Feature_Engineering as fe
from sklearn import svm
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
import nltk
import random
# from sklearn.metrics import confusion_matrix


def divide_into_training_test(list_of_list, label):
    i = 0
    X_training_data = []
    X_test_data = []
    y_training_labels = []
    y_test_labels = []
    for li in list_of_list:
        if (i % 5 == 0):
            X_test_data.append(li)
            y_test_labels.append(label)
        else:
            X_training_data.append(li)
            y_training_labels.append(label)
        i += 1

    return X_training_data, y_training_labels, X_test_data, y_test_labels


def support_vector_machine(X_training_data, y_training_labels, kernel, C, gamma):
    return svm.SVC(kernel= kernel, gamma=gamma, C=C).fit(X_training_data, y_training_labels)


def gradient_booster(X_training_data, y_training_labels, n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0):
     return GradientBoostingClassifier(n_estimators=n_estimators, learning_rate=learning_rate,
                                       max_depth=max_depth, random_state=random_state).fit(X_training_data,
                                                                                           y_training_labels)

def perceptron(X_training_data, y_training_labels, solver='sgd', alpha=1e-6, hidden_layer_sizes=(5,2), random_state=1):
    return MLPClassifier(solver=solver, alpha=alpha, hidden_layer_sizes=hidden_layer_sizes,
                         random_state=random_state, max_iter=2000).fit(X_training_data, y_training_labels)

if __name__ == '__main__':
    failed_file = "failed_banks_1col_space_delimited.txt"
    failed_files = ["failed_banks_col1_space_delimited.txt",
    "failed_banks_col2_space_delimited.txt",
    "failed_banks_col3_space_delimited.txt",
    "failed_banks_col4_space_delimited.txt"]
    failed_list = []
    for f in failed_files:
        temp_list = fe.store_txt_file_as_list(f)
        failed_list = failed_list + temp_list
    ########
    # failed_list = fe.store_txt_file_as_list(failed_file)
    # active_file = "active_banks_AI_space_delimited.txt"
    #########
    print ("Length of failed_list = ", len(failed_list))

    active_file = "active_banks_allBut1516_space_delimited.txt"

    active_list = fe.store_txt_file_as_list(active_file)
    failed_feature_list_of_list = []
    active_feature_list_of_list = []

    failed_feature_list_of_list = fe.feature_engineering(failed_list)
    active_feature_list_of_list = fe.feature_engineering(active_list)
    print(len(failed_feature_list_of_list))
    print(len(active_feature_list_of_list))

    X_training_data = []
    X_test_data = []
    y_training_labels = []
    y_test_labels = []
    X_training_data, y_training_labels, X_test_data, y_test_labels = \
        divide_into_training_test(failed_feature_list_of_list, "Failed")
    print(len(X_training_data))
    temp_X_training_data = []
    temp_X_test_data = []
    temp_y_training_labels = []
    temp_y_test_labels = []
    num_failed = len(failed_feature_list_of_list)
    ratio = 4
    temp_X_training_data, temp_y_training_labels, temp_X_test_data, temp_y_test_labels = \
        divide_into_training_test(random.sample(active_feature_list_of_list, num_failed * ratio), "Active")
    #########
    # temp_X_training_data, temp_y_training_labels, temp_X_test_data, temp_y_test_labels = \
    #     divide_into_training_test(active_feature_list_of_list, "Active")
    #########
    X_training_data = X_training_data + temp_X_training_data

    print(len(temp_X_training_data))
    print(len(X_training_data))
    X_test_data = X_test_data + temp_X_test_data
    y_training_labels = y_training_labels + temp_y_training_labels
    y_test_labels = y_test_labels + temp_y_test_labels
    #
    kernel = 'rbf'  # SVM kernel, (Gaussian) Radial Basis Function (RBF) Kernel.
    C = 10.0        # SVM regularization parameter, Cost/penalty.
    gamma = 1.0     # SVM, area surrounding the decision boundary.
    classifier = support_vector_machine(X_training_data=X_training_data, y_training_labels=y_training_labels,
                                        kernel=kernel, C=C, gamma=gamma)
    # classifier = perceptron(X_training_data=X_training_data, y_training_labels=y_training_labels)
    # classifier = gradient_booster(X_training_data=X_training_data, y_training_labels=y_training_labels)
    # print(type(classifier))
    acc = classifier.score(X_test_data, y_test_labels)
    print ("Number of y_test_labels = ", len(y_test_labels))
    print("Accuracy = % .4f\n" % acc)
    # print(classifier.feature_importances_)

    pred_labels = classifier.predict(X_test_data)
    predicted_labels = []
    for label in pred_labels:
        predicted_labels.append(label)

    print("Number of predicted_labels =", len(predicted_labels))
    # print(y_test_labels)

    print("Confusion Matrix: ")
    # print(confusion_matrix(y_test_labels, predicted_labels), "\n")
    confusion_matrix = nltk.ConfusionMatrix(y_test_labels, predicted_labels)

    print(confusion_matrix)