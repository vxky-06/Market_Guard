import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler

def preprocess(df):
    """
    Preprocesses the transaction data.

    Args:
        df (pandas.DataFrame): The input DataFrame with transaction data.

    Returns:
        pandas.DataFrame: The processed DataFrame.
        sklearn.compose.ColumnTransformer: The fitted preprocessing pipeline.
    """
    if df is None:
        return None, None

    # Make a copy to avoid modifying the original DataFrame
    df_processed = df.copy()

    # Explicitly convert transaction_amount to float
    if 'transaction_amount' in df_processed.columns:
        df_processed['transaction_amount'] = pd.to_numeric(df_processed['transaction_amount'], errors='coerce')

    # Convert timestamp to a numeric feature (Unix timestamp)
    if 'timestamp' in df_processed.columns:
        df_processed['timestamp'] = pd.to_datetime(df_processed['timestamp'], errors='coerce').astype('int64') // 10**9

    # Identify column types
    numeric_features = df_processed.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = df_processed.select_dtypes(include=['object']).columns.tolist()
    
    # Debug prints
    print('Numeric features:', numeric_features)
    print('Categorical features:', categorical_features)
    print('DataFrame dtypes:', df_processed.dtypes)
    
    # account_id is an identifier, let's remove it from features but NOT from the DataFrame
    if 'account_id' in categorical_features:
        categorical_features.remove('account_id')
    if 'account_id' in numeric_features:
        numeric_features.remove('account_id')

    # Create preprocessing pipelines for numeric and categorical data
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', MinMaxScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    # Set remainder to 'drop' to avoid column mismatch
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ],
        remainder='drop'
    )

    # Fit and transform the data
    processed_data = preprocessor.fit_transform(df_processed)
    print('Processed data shape:', processed_data.shape)
    print('Processed data (first 2 rows):', processed_data[:2])
    print('Fitted categorical transformer:', preprocessor.named_transformers_['cat'])
    if hasattr(preprocessor.named_transformers_['cat'], 'named_steps'):
        print('Fitted onehot encoder:', preprocessor.named_transformers_['cat']['onehot'])
        if hasattr(preprocessor.named_transformers_['cat']['onehot'], 'categories_'):
            print('OneHot categories:', preprocessor.named_transformers_['cat']['onehot'].categories_)
    
    # Get feature names after one-hot encoding
    ohe_feature_names = []
    if categorical_features:
        ohe_feature_names = preprocessor.named_transformers_['cat']['onehot'].get_feature_names_out(categorical_features)
    
    # Combine numeric and one-hot encoded feature names
    all_feature_names = numeric_features + list(ohe_feature_names)
    print('All feature names:', all_feature_names)
    print('Number of feature names:', len(all_feature_names))

    # Create a new DataFrame with the processed data
    df_processed = pd.DataFrame(processed_data, columns=all_feature_names, index=df_processed.index)
    
    return df_processed, preprocessor 