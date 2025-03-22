import pandas as pd
import argparse

def anonymize_dataframe(df):
    location_dict = {
        'Breast': 'BR', 'Large intestine': 'LI', 'Esophagous': 'ES', 'Skin, bone and soft tissue': 'SB',
        'Head and neck': 'HN', 'Hepatobiliary system and pancreas': 'HP', 'Female genital organ': 'FG',
        'Male genital organ': 'MG', 'Chest': 'CH', 'Urinary system': 'US', 'Lymphoreticular system': 'LR',
        'Small intestine': 'SM', 'CNS': 'CS', 'Pleura & peritoneum': 'MS', 'Others': 'MS'
    }
    
    operation_dict = {
        'operation': 'OP',
        'biopsy': 'BX'
    }
    
    dye_dict = {
        'HE': 'IMH',
        'IHC': 'IMI',
        'SS': 'IMS'
    }
    
    # Check if there are any unmatched values
    if not df['location'].isin(location_dict.keys()).all():
        raise ValueError("Invalid value found in 'location' column")
    if not df['operation'].isin(operation_dict.keys()).all():
        raise ValueError("Invalid value found in 'operation' column")
    if not df['dye'].isin(dye_dict.keys()).all():
        raise ValueError("Invalid value found in 'dye' column")
    
    # Generate folder name
    df['folder_prefix'] = 'PIT-01-' + df['location'].map(location_dict) + df['operation'].map(operation_dict)
    
    # Convert patient_num to a unique identifier starting from 1 for each folder_prefix (5 digits)
    df['patient_anon'] = df.groupby('folder_prefix')['patient_num'].transform(lambda x: x.factorize()[0] + 1)
    df['patient_anon'] = df['patient_anon'].apply(lambda x: f"{x:05d}")
    
    df['folder'] = df['folder_prefix'] + '-' + df['patient_anon']
    
    # Generate file name
    df['file_prefix'] = df['folder'] + '-' + df['dye'].map(dye_dict) + '-'
    
    # Convert file_num to a unique identifier starting from 1 for each file_prefix (3 digits)
    df['file_anon'] = df.groupby('file_prefix')['file_num'].transform(lambda x: x.factorize()[0] + 1)
    df['file_anon'] = df['file_anon'].apply(lambda x: f"{x:03d}")
    
    df['file'] = df['file_prefix'] + df['file_anon'] + '.svs'
    
    return df

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--xlsx_path',type=str)
    parser.add_argument('--save_path',type=str)
    args = parser.parse_args()
    xlsx_path = args.xlsx_path
    save_path = args.save_path

    # Load excel file 
    df = pd.read_excel(xlsx_path)

    # Generate anonymized dataframe
    df_anonymized = anonymize_dataframe(df)
    df_anonymized = df_anonymized.reset_index().rename(columns={"index": "idx", "patient_num": "src_folder", "file_num": "src_file", "report_gross": "gross", "report": "micro"})
    df_anonymized = df_anonymized[['idx', 'src_folder', 'src_file', 'folder', 'file', 'gross', 'micro']] 
    
    # Save csv file
    df_anonymized.to_csv(save_path, index=False)