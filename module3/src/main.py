import pandas as pd
from knn import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
import os

def read_csv(path):
    df = pd.read_csv(path)
    return df

def divide_in_sets(df):
    x = df.iloc[:, :-1].values
    y = df.iloc[:, 10].values
    return x, y

if __name__ == '__main__':
    data_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'data'))
    df_Beijing = read_csv(os.path.join(data_dir, 'Beijing_labeled.csv'))
    df_Chengdu = read_csv(os.path.join(data_dir, 'Chengdu_labeled.csv'))
    df_Guangzhou = read_csv(os.path.join(data_dir, 'Guangzhou_labeled.csv'))
    df_Shanghai = read_csv(os.path.join(data_dir, 'Shanghai_labeled.csv'))
    df_Shenyang = read_csv(os.path.join(data_dir, 'Shenyang_labeled.csv'))

    x_Beijing, y_Beijing = divide_in_sets(df_Beijing)
    x_Chengdu, y_Chengdu = divide_in_sets(df_Chengdu)
    x_Guangzhou, y_Guangzhou = divide_in_sets(df_Guangzhou)
    x_Shanghai, y_Shanghai = divide_in_sets(df_Shanghai)
    x_Shenyang, y_Shenyang = divide_in_sets(df_Shenyang)

    # Training and validating the model on Beijing and Shenyang
    # splitting train set and validation set
    beijing = train_test_split(x_Beijing, y_Beijing, test_size=0.2,
                               random_state=420)
    shenyang = train_test_split(x_Shenyang, y_Shenyang, test_size=0.2,
                                random_state=420)
    x_train_Beijing, x_test_Beijing, y_train_Beijing, y_test_Beijing = beijing
    x_train_Shenyang, x_test_Shenyang, y_train_Shenyang, y_test_Shenyang = shenyang

    x_train = np.concatenate((x_train_Beijing,x_train_Shenyang))
    x_test = np.concatenate((x_test_Beijing,x_test_Shenyang))
    y_train = np.concatenate((y_train_Beijing,y_train_Shenyang))
    y_test = np.concatenate((y_test_Beijing,y_test_Shenyang))

    print('INFO. Identifying the best "n_neighbors" parameter.')
    score_arr = []
    for n in range(3, 50, 2):
        model = KNeighborsClassifier(n_neighbors=n)
        model.fit(x_train, y_train)
        test_preds = model.predict(x_test)
        # Evaluation on Guangzhou and Shanghai
        x_eval = np.concatenate((x_Guangzhou,x_Shanghai))
        y_eval = np.concatenate((y_Guangzhou,y_Shanghai))
        accuracy = model.score(x_eval, y_eval)
        print(f'INFO. n_neighbors={n}, testing accuracy: {accuracy}')
        score_arr.append(accuracy)
    print('INFO. Plotting accuracy versus N neighbors:')
    plt.plot(score_arr)
    plt.xlabel('N Neighbors')
    plt.ylabel('Score')
    plt.savefig('Score.png')
    plt.show()
