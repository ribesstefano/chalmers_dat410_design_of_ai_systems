import pandas as pd
import knn
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt


def read_csv(path):
    df = pd.read_csv(path)
    return df


def divide_in_sets(df):
    x = df.iloc[:, :-1].values
    y = df.iloc[:, 10].values

    return x, y


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    df_Beijing = read_csv('data/Beijing_labeled.csv')
    df_Chengdu = read_csv('data/Chengdu_labeled.csv')
    df_Guangzhou = read_csv('data/Guangzhou_labeled.csv')
    df_Shanghai = read_csv('data/Shanghai_labeled.csv')
    df_Shenyang = read_csv('data/Shenyang_labeled.csv')

    x_Beijing, y_Beijing = divide_in_sets(df_Beijing)
    x_Chengdu, y_Chengdu = divide_in_sets(df_Chengdu)
    x_Guangzhou, y_Guangzhou = divide_in_sets(df_Guangzhou)
    x_Shanghai, y_Shanghai = divide_in_sets(df_Shanghai)
    x_Shenyang, y_Shenyang = divide_in_sets(df_Shenyang)


    # training and validating the model on Beijing and Shenyang

    # splitting train set and validation set

    x_train_Beijing, x_test_Beijing, y_train_Beijing, y_test_Beijing = train_test_split(x_Beijing, y_Beijing,
                                                                                        test_size=0.2, random_state=420)

    x_train_Shenyang, x_test_Shenyang, y_train_Shenyang, y_test_Shenyang = train_test_split(x_Shenyang, y_Shenyang,
                                                                                            test_size=0.2, random_state=420)

    x_train = np.concatenate((x_train_Beijing,x_train_Shenyang))
    x_test = np.concatenate((x_test_Beijing,x_test_Shenyang))
    y_train = np.concatenate((y_train_Beijing,y_train_Shenyang))
    y_test = np.concatenate((y_test_Beijing,y_test_Shenyang))


    score_arr = []

    for n in range(3, 50, 2):

        model = knn.KNeighborsClassifier(n_neighbors=n)

        model.fit(x_train, y_train)

        test_preds = model.predict(x_test)



        #evaluation on Guangzhou and Shanghai

        x_eval = np.concatenate((x_Guangzhou,x_Shanghai))

        y_eval = np.concatenate((y_Guangzhou,y_Shanghai))

        res = model.score(x_eval, y_eval)

        print(n, res)

        score_arr.append(res)

    plt.plot(score_arr)
    plt.xlabel('N Neighbors')
    plt.ylabel('Score')
    plt.savefig('Score.png')
    plt.show()
