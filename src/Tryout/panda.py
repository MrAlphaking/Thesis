import pandas as pd

# df = pd.read_csv('../../../data/Ground Truth/Mirjam/data_frames_evaluation/data_frames_evaluation/full_df_DBNL_OCR_evaluation.csv', compression='gzip')
df = pd.read_csv('../../../data/Ground Truth/17thcenturynewspapers.csv', compression='gzip')

print(df.to_string())

# print(df.iloc[:10].to_string())

