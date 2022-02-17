import pickle
import pandas as pd

def split_df(df, perc):
    perc_size = int(len(df.index) * perc)
    lower = df.iloc[:perc_size, :]
    upper = df.iloc[perc_size:, :]
    return lower, upper

def clean_data(filename, train_perc, df_as_numpy=True):
    """
    Open, clean and split database into the training and test sets.
    
    :param      filename:     The filename
    :type       filename:     String
    :param      train_perc:   The percentage size of the training set
    :type       train_perc:   Double
    :param      df_as_numpy:  Whether to return the datasets as Pandas df or as
                              numpy arrays
    :type       df_as_numpy:  bool
    
    :returns:   x_train, y_train, x_test, y_test
    :rtype:     Pandas df or as numpy arrays
    """
    with open(filename, 'rb') as f:
        df = pickle.load(f)

    # Equally distribute the positive and negative samples in the two datasets.
    pos = df[df['malignant'] == 1]
    neg = df[df['malignant'] == 0]

    pos_train, pos_test = split_df(pos, train_perc)
    neg_train, neg_test = split_df(neg, train_perc)
    df_train = pd.concat([pos_train, neg_train])
    df_test = pd.concat([pos_test, neg_test])

    # Drop columns in the two datasets
    x_train = df_train.drop(['malignant'], axis=1)
    x_test = df_test.drop(['malignant'], axis=1)

    # Rename columns from '_0' to mean, et cetera...
    new_col_names = []
    for col_name in x_train.keys():
        if '_0' in col_name:
            new_name = col_name[:-2] + '_mean'
        elif '_1' in col_name:
            new_name = col_name[:-2] + '_std'
        elif '_2' in col_name:
            new_name = col_name[:-2] + '_worst'
        else:
            new_name = col_name
        new_col_names.append(new_name)

    new_names = {o : n for o, n in zip(x_train.keys(), new_col_names)}
    x_train = x_train.rename(new_names, axis='columns')
    x_test = x_test.rename(new_names, axis='columns')

    y_train = df_train['malignant']
    y_test = df_test['malignant']

    if df_as_numpy:
        return x_train.to_numpy(), y_train.to_numpy(), \
            x_test.to_numpy(), y_test.to_numpy()
    else:
        return x_train, y_train, x_test, y_test

def main():
    DATABASE = 'wdbc.pkl'
    TRAIN_PERC = 0.8
    data = clean_data(DATABASE, TRAIN_PERC, df_as_numpy=False)
    x_train, y_train, x_test, y_test = data
    print(x_train.describe().transpose())
    print(y_train.describe().transpose())

if __name__ == '__main__':
    main()
