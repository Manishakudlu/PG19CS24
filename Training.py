@app.route('/load_dataset')
def load_dataset():
    import pandas as pd
    data = pd.read_csv(static_path + "dataset\\career_choices.csv")
    print(data)
    # print(data.shape)
    # print(data.head)
    attributes = data.values[:1000, 0:28]
    labels = data.values[:1000, 28]

    attributes1 = data.values[:900, 0:28]
    labels1 = data.values[:900, 28]
    # print("ATTRIBUTES",attributes)
    # print("LABELS",labels)
    X_train, X_test, y_train, y_test = train_test_split(attributes, labels, test_size=0.2)
    #
    #
    rf = RandomForestClassifier(n_estimators=100)
    rf.fit(attributes1, labels1)
    y_pred_rf = rf.predict(X_test)
    print(y_pred_rf)
    acc = accuracy_score(y_test, y_pred_rf)
    acc_rf = round(acc * 100, 2)
    print("R", acc_rf)

    #
    svm = LinearSVC()
    # svm.fit(X_train,y_train)
    svm.fit(attributes1, labels1)
    y_pred_svm = svm.predict(X_test)
    acc = accuracy_score(y_test, y_pred_svm)
    acc_sv = round(acc * 100, 2)
    print("S", acc_sv)

    #

    dummy = DummyClassifier()
    # svm.fit(X_train,y_train)
    dummy.fit(attributes1, labels1)
    y_pred_dummy = dummy.predict(X_test)
    acc = accuracy_score(y_test, y_pred_dummy)
    acc_dy = round(acc * 100, 2)
    print("d", acc_dy)

    #

    ridg = RidgeClassifier()
    # svm.fit(X_train,y_train)
    ridg.fit(attributes1, labels1)
    y_pred_ridg = ridg.predict(X_test)
    acc = accuracy_score(y_test, y_pred_ridg)
    acc_rg = round(acc * 100, 2)
    print("R", acc_rg)

    import os
    import numpy as np
    import matplotlib.pyplot as plt

    x = ["Random Forest", "SVM", "DummyClassifier", "RidgeClassifier"]
    y = [acc_rf, acc_sv, acc_dy, acc_rg]
    # plt.bar(x, y)
    fig, ax=plt.subplots()
    bar1=ax.bar(x, y)
    ax.set_xticks(x)
    ax.bar_label(bar1)
    ax.legend()

    plt.show()
    # fig, ax = plt.subplots()
    # width = 0.75
    # ind = np.arange(len(y))
    #
    # ax.barh(ind, y, width, color="green")
    #
    # for i, v in enumerate(y):
    #     ax.text(v + 3, i + .25, str(v),
    #             color='blue', fontweight='bold')
    # plt.show()
    # plt.savefig()

    return "ok"

