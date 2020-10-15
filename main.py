# General Imports
import pandas as pd
import seaborn as sns
sns.set_style("darkgrid")
import matplotlib.pyplot as plt
import numpy as np

# Sklearn imports. Uncomment as you need, it gets long to run otherwise
from sklearn.metrics import precision_recall_fscore_support,confusion_matrix,accuracy_score  # f1 by default
#from sklearn.naive_bayes import GaussianNB

from sklearn.model_selection import GridSearchCV
# from sklearn.linear_model import Perceptron
# from sklearn.neural_network import MLPClassifier

# Constant alphabet maps
LATIN_ALPHABET = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L',
                  12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W',
                  23: 'X', 24: 'Y', 25: 'Z'}
GREEK_ALPHABET = {0: '\u03C0', 1: '\u03B1', 2: '\u03B2', 3: '\u03C3', 4: '\u03B3', 5: '\u03B4', 6: '\u03BB',
                  7: '\u03C9', 8: '\u03BC', 9: '\u03BE'}

def plot_data(data):
    """ Description

    Parameters
    ----------
    data: tuple of pd.DataFrame
        Tuple containing a tuple of 2 datasets as pd.Dataframe

    Returns
    -------
    """
    df1, df2 = data
    plt.figure(figsize=(12, 8))
    ax = sns.countplot(df1[df1.columns[-1]].map(LATIN_ALPHABET), order=LATIN_ALPHABET.values(), palette='colorblind')
    ax.set(xlabel='Letters', ylabel='Count', title='Count Of Letters In Dataset 1')
    ax.axhline(df1[df1.columns[-1]].shape[0] / 26, color='red', label='Uniform Distribution')
    plt.legend()
    plt.show()
    ax = sns.countplot(df2[df2.columns[-1]].map(GREEK_ALPHABET), order=GREEK_ALPHABET.values(), palette='colorblind')
    ax.set(xlabel='Letters', ylabel='Count', title='Count Of Letters In Dataset 2')
    ax.axhline(df2[df2.columns[-1]].shape[0] / 10, color='red', label='Uniform Distribution')
    plt.legend()
    plt.show()

    

def output_metrics_and_csv(y_pred,y_true,model_name,dataset_id):
    """ Description
    Compute metrics and output predictions of dataset to csv file
    Parameters
    ----------
    y_pred: nd.array
    y_true: nd.array
    model_name: string
    dataset_id: int
        y_pred, y_true: arrays of predicted classes and true classes for a dataset
        model_name: name of model result's being outputted
        dataset_id: id of dataset being outputted (1 or 2)

    Returns
    -------
    """

    # Get metrics TODO Clarify which are pertinent
    accuracy=accuracy_score(y_true,y_pred)
    precision_per_class, recall_per_class, f1_per_class,  support_per_class= precision_recall_fscore_support(y_true, y_pred)
    precision_weighted, recall_weighted, f1_weighted,support_weighted = precision_recall_fscore_support(y_true, y_pred, average='weighted')
    precision_macro, recall_macro, f1_macro,support_macro = precision_recall_fscore_support(y_true, y_pred,average='macro')

    # Prepare Result
    # TODO Confusion matrix is included in output csv? Formatting of metrics in output file?
    conf_mx=confusion_matrix(y_true,y_pred)
    #Output to CSV
    predicted=[np.sum(y_pred==i) for i in range(conf_mx.shape[0])]
    output_acc=zip([round(accuracy,2)],[round(f1_weighted,2)],[round(f1_macro,2)])
    output_pred = zip(np.arange(y_pred.shape[0]), predicted,np.round(precision_per_class,2),np.round(recall_per_class,2),np.round(f1_per_class,2))  # In format (y_instance,prediction)
    df_0=pd.DataFrame(output_acc)
    df_0.to_csv('results/%s-DS%d.csv' % (model_name, dataset_id), index=False, header=[ 'Accuracy','F1_weighted','F1_macro'])    
    df_1=pd.DataFrame(output_pred)
    df_1.to_csv('results/%s-DS%d.csv' % (model_name, dataset_id), index=False, mode='a',header=[ 'Instance','Predicted','Precision','Recall','F1'])
    df_2=pd.DataFrame(conf_mx,columns=np.arange(conf_mx.shape[1]))
    df_2.to_csv('results/%s-DS%d.csv' % (model_name, dataset_id), header=True, mode='a')
   
    return


def GNB(train, val):
    from sklearn.naive_bayes import GaussianNB
    """ Description
    
    Parameters
    ----------
    train: tuple of pd.DataFrame
    val: tuple of pd.DataFrame
    Returns
    -------
    """

    # Unpack datasets
    df1_train, df2_train = train
    df1_val, df2_val = val

    # Define Model
    gnb = GaussianNB()

    # Apply model to dataset1
    X = df1_train[df1_train.columns[:-1]]
    Y = df1_train[df1_train.columns[-1]]
    gnb.fit(X, Y)

    # Get predictions and true labels of dataset1
    y_pred = gnb.predict(np.array(df1_val)[:, :1024])
    y_true = df1_val[df1_val.columns[-1]]

    # Output predictions and metrics of dataset1 to CSV
    output_metrics_and_csv(y_pred, y_true,'GNB',1)


    # Apply model to dataset2
    X = df2_train[df2_train.columns[:-1]]
    Y = df2_train[df2_train.columns[-1]]
    gnb.fit(X, Y)

    # Get predictions and true labels of dataset2
    y_pred = gnb.predict(np.array(df2_val)[:, :1024])
    y_true = df2_val[df2_val.columns[-1]]

    # Output predictions and metrics of dataset2 to CSV
    output_metrics_and_csv(y_pred, y_true,'GNB',2)

    return


def Base_DT(train, val):
    from sklearn.tree import DecisionTreeClassifier
    """ Description

    Parameters
    ----------
    train: tuple of pd.DataFrame
    val: tuple of pd.DataFrame
    Returns
    -------
    """

    # Unpack datasets
    df1_train, df2_train = train
    df1_val, df2_val = val

    # Define Model
    Base_Decision_tree=DecisionTreeClassifier(criterion='entropy')
    # Apply model to dataset1
    X = df1_train[df1_train.columns[:-1]]
    Y = df1_train[df1_train.columns[-1]]
    Base_Decision_tree.fit(X,Y)
    # Get predictions and true labels of dataset1
    y_pred = Base_Decision_tree.predict(np.array(df1_val)[:, :1024])
    y_true = df1_val[df1_val.columns[-1]]
    # Output predictions and metrics of dataset1 to CSV
    output_metrics_and_csv(y_pred, y_true,'Base-DT',1)
    # Apply model to dataset2
    X = df2_train[df2_train.columns[:-1]]
    Y = df2_train[df2_train.columns[-1]]
    Base_Decision_tree.fit(X,Y)
    # Get predictions and true labels of dataset2
    y_pred = Base_Decision_tree.predict(np.array(df2_val)[:, :1024])
    y_true = df2_val[df2_val.columns[-1]]
    # Output predictions and metrics of dataset2 to CSV
    output_metrics_and_csv(y_pred, y_true,'Base-DT',2)


def Best_DT(train, val):
    from sklearn.tree import DecisionTreeClassifier
    """ Description

    Parameters
    ----------
    train: tuple of pd.DataFrame
    val: tuple of pd.DataFrame    Tuple containing a tuple of 2 datasets as pd.Dataframe
    Returns
    -------
    """

    # Unpack datasets
    df1_train, df2_train = train
    df1_val, df2_val = val

    # Define Model
    Best_Decision_tree=DecisionTreeClassifier()
    param_grid={'criterion':['entropy'],'max_depth':[26,27,28],'min_samples_split':[5],'min_impurity_decrease':[0,0.001],'class_weight':[None]}   
     # Apply model to dataset1
    grid_search=GridSearchCV(Best_Decision_tree,param_grid,cv=16,return_train_score=True)
    # Get predictions and true labels of dataset1
    X = df1_train[df1_train.columns[:-1]]
    Y = df1_train[df1_train.columns[-1]]
    grid_search.fit(X,Y)
    final_model=grid_search.best_estimator_
    print(grid_search.best_estimator_)
    y_pred = final_model.predict(np.array(df1_val)[:, :1024])
    y_true = df1_val[df1_val.columns[-1]]
    # Output predictions and metrics of dataset1 to CSV
    output_metrics_and_csv(y_pred, y_true,'Best-DT',1)
    # Apply model to dataset2
    # X = df2_train[df2_train.columns[:-1]]
    # Y = df2_train[df2_train.columns[-1]]
    # param_grid={'criterion':['gini','entropy'],'max_depth':[5,10],'min_samples_split':[2,3,5],'min_impurity_decrease':[0.5,1],'class_weight':[None,'balanced']}   
    # # Apply model to dataset1
    # grid_search=GridSearchCV(Best_Decision_tree,param_grid,cv=10,return_train_score=True)
    # grid_search.fit(X,Y)
    # final_model=grid_search.best_estimator_
    # print(grid_search.best_estimator_)
    # # Get predictions and true labels of dataset2
    # y_pred = final_model.predict(np.array(df2_val)[:, :1024])
    # y_true = df2_val[df2_val.columns[-1]]
    # # Output predictions and metrics of dataset2 to CSV
    # output_metrics_and_csv(y_pred, y_true,'Best-DT',2)

    return


def PER(train, val):
    """ Description

    Parameters
    ----------
    train: tuple of pd.DataFrame
    val: tuple of pd.DataFrame
    Returns
    -------
    """
    from sklearn.linear_model import Perceptron
    # Unpack datasets
    df1_train, df2_train = train
    df1_val, df2_val = val

    # Define Model
    per = Perceptron()
    # Apply model to dataset1
    X = df1_train[df1_train.columns[:-1]]
    y = df1_train[df1_train.columns[-1]]
    per.fit(X,y)
    # Get predictions and true labels of dataset1
    pred = per.predict(np.array(df1_val)[:, :1024])
    true = df1_val[df1_val.columns[-1]]
    # Output predictions and metrics of dataset1 to CSV
    output_metrics_and_csv(pred, true, "Perceptron", 1)
    # Apply model to dataset2
    X = df2_train[df2_train.columns[:-1]]
    y = df2_train[df2_train.columns[-1]]
    per.fit(X,y)
    # Get predictions and true labels of dataset2
    pred = per.predict(np.array(df2_val)[:, :1024])
    true = df2_val[df2_val.columns[-1]]
    # Output predictions and metrics of dataset2 to CSV
    output_metrics_and_csv(pred, true, "Perceptron", 2)
    return


def Base_MLP(train, val):
    """ Description

    Parameters
    ----------
    train: tuple of pd.DataFrame
    val: tuple of pd.DataFrame
    Returns
    -------
    """
    from sklearn.neural_network import MLPClassifier
    # Unpack datasets
    df1_train, df2_train = train
    df1_val, df2_val = val

    # Define Model
    mlp=MLPClassifier(hidden_layer_sizes=(100,),activation="logistic",solver="sgd")
    # Apply model to dataset1
    X = df1_train[df1_train.columns[:-1]]
    y = df1_train[df1_train.columns[-1]]
    mlp.fit(X,y)
    # Get predictions and true labels of dataset1
    pred = mlp.predict(np.array(df1_val)[:, :1024])
    true = df1_val[df1_val.columns[-1]]
    # Output predictions and metrics of dataset1 to CSV
    output_metrics_and_csv(pred, true, "Base-MLP", 1)
    # Apply model to dataset2
    X = df2_train[df2_train.columns[:-1]]
    y = df2_train[df2_train.columns[-1]]
    mlp.fit(X,y)
    # Get predictions and true labels of dataset2
    pred = mlp.predict(np.array(df2_val)[:, :1024])
    true = df2_val[df2_val.columns[-1]]
    # Output predictions and metrics of dataset2 to CSV
    output_metrics_and_csv(pred, true, "Base-MLP", 2)
    return


def Best_MLP(train, val):
    from sklearn.neural_network import MLPClassifier
    """ Description

    Parameters
    ----------
    train: tuple of pd.DataFrame
    val: tuple of pd.DataFrame
    Returns
    -------
    """

    # Unpack datasets
    df1_train, df2_train = train
    df1_val, df2_val = val

    # Define Model
    mlp=MLPClassifier()
    param_grid={'activation':['identity','logistic','tanh','relu'],'hidden_layer_sizes':[(50,30),(20,10,10)],'solver':["adam","sgd"]}   
     # Apply model to dataset1
    grid_search=GridSearchCV(mlp,param_grid,cv=16,return_train_score=True)
    X = df1_train[df1_train.columns[:-1]]
    y = df1_train[df1_train.columns[-1]]
    grid_search.fit(X,y)
    final_model=grid_search.best_estimator_
    print(grid_search.best_estimator_)

    # Get predictions and true labels of dataset1
    pred = final_model.predict(np.array(df1_val)[:, :1024])
    true = df1_val[df1_val.columns[-1]]
    # Output predictions and metrics of dataset1 to CSV
    output_metrics_and_csv(pred, true, "Base-MLP", 1)
    # Apply model to dataset2
    X = df2_train[df2_train.columns[:-1]]
    y = df2_train[df2_train.columns[-1]]
    grid_search.fit(X,y)
    final_model=grid_search.best_estimator_
    print(grid_search.best_estimator_)
    # Get predictions and true labels of dataset2
    pred = final_model.predict(np.array(df2_val)[:, :1024])
    true = df2_val[df2_val.columns[-1]]
    # Output predictions and metrics of dataset2 to CSV
    output_metrics_and_csv(pred, true, "Base-MLP", 2)

    return


def main():
    # Load datasets splits as tuples of each type
    df_train = (pd.read_csv('data/train_1.csv'), pd.read_csv('data/train_2.csv'))
    df_tests_no_label = (pd.read_csv('data/test_no_label_1.csv'), pd.read_csv('data/test_no_label_2.csv'))
    df_tests_with_label = (pd.read_csv('data/test_with_label_1.csv'), pd.read_csv('data/test_with_label_2.csv'))
    df_val = (pd.read_csv('data/val_1.csv'), pd.read_csv('data/val_2.csv'))

    # Plot instance distribution
    #plot_data(df_train)

    # Run models
    # Best_DT(df_train,df_val)
    #GNB(df_train,df_val)
    # PER(df_train, df_val)
    Base_MLP(df_train, df_val)
    # Best_MLP(df_train, df_val)
    return


if __name__ == '__main__':
    main()
