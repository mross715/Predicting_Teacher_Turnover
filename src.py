
def na_transformer(df):
    '''
    Changes values to 0 for columns that have 
    'Not Applicable' or 'Insufficient Data' preventing them from becoming numerical.
    '''
    for col in obj_to_num:
        df.loc[(df[col] == 'Not Applicable'), col] = 0
        df.loc[(df[col] == 'Insufficient Data'), col] = 0
    return df


def to_float_transformer(df):
    '''
    Ensure all 'Score' columns are float, and all int64 are also float.
    '''
    for col in obj_to_num:
        df[col] = df[col].astype('float64')
    for col in [df.select_dtypes('int64').columns]:
        df[col] = df[col].astype('float64')
    return df



def print_cv_scores(pipe, X, y):
    '''
    Runs cross_validate on given feature and binary target arrays using given pipeline, 
    printing the scoring results for both training and cross_val.
    '''
    scoring = ['accuracy','recall']
    # we pass in pipe to cross validate along with a feature list.
    results = cross_validate(pipe, X, 
                                   y, 
                                   return_train_score=True, scoring=scoring)
    
    print(results['train_accuracy'])
    print('Training Accuracy', results['train_accuracy'].mean())
    print('##############')
    print(results['test_accuracy'])
    print('Cross_Val Accuracy', results['test_accuracy'].mean())
    print('##############')
    print('Training Recall:', results['train_recall'].mean())
    print('Cross_Val Recall:', results['test_recall'].mean())


    
def create_importance_dataframe(pca):
    '''
    Take the PCA model and generate a dataframe that shows the 
    importance of features that contributed to each of the Principal Components. 
    '''
    # Change pcs components ndarray to a dataframe
    importance_df  = pd.DataFrame(pca.components_)
    # Assign columns and use absolute value
    importance_df.columns  = ohe_feature_names
    importance_df =importance_df.apply(np.abs)
    # Transpose
    importance_df=importance_df.transpose()
    # Get number of PCs
    num_pcs = importance_df.shape[1]
    # Generate the new column names and rename
    new_columns = [f'PC{i}' for i in range(1, num_pcs + 1)]
    importance_df.columns  = new_columns

    # Return importance df
    return importance_df

