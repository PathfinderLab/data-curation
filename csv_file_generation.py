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

    # 매칭되지 않는 값이 있는지 확인
    if not df['location'].isin(location_dict.keys()).all():
        raise ValueError("Invalid value found in 'location' column")
    if not df['operation'].isin(operation_dict.keys()).all():
        raise ValueError("Invalid value found in 'operation' column")
    if not df['dye'].isin(dye_dict.keys()).all():
        raise ValueError("Invalid value found in 'dye' column")
    
    # patient_num을 1부터 시작하는 고유 번호로 변환 (5자리)
    df['patient_anon'] = df['patient_num'].astype('category').cat.codes + 1
    df['patient_anon'] = df['patient_anon'].apply(lambda x: f"{x:05d}")
    
    # 각 patient_num 그룹 내에서 file_num에 대한 고유 번호 생성 (3자리)
    df['file_anon'] = df.groupby('patient_num').cumcount() + 1
    df['file_anon'] = df['file_anon'].apply(lambda x: f"{x:03d}")
    
    # folder 컬럼 생성
    df['folder'] = 'PIT-01-' + df['location'].map(location_dict) + df['operation'].map(operation_dict) + '-' + df['patient_anon'].astype(str)
    
    # file 컬럼 생성
    df['file'] = df['folder'] + '-' + df['dye'].map(dye_dict) + '-' + df['file_anon'].astype(str) + '.svs'
    
    return df

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--xlsx_path',type=str)
    parser.add_argument('--save_path',type=str)
    args = parser.parse_args()
    xlsx_path = args.xlsx_path
    save_path = args.save_path

    # 데이터 불러오기
    df = pd.read_excel(xlsx_path)

    # 가명화 적용
    df_anonymized = anonymize_dataframe(df)
    df_anonymized = df_anonymized.reset_index().rename(columns={"index": "idx", "patient_num": "src_folder", "file_num": "src_file", "report_gross": "gross", "report": "micro"})
    df_anonymized = df_anonymized[['idx', 'src_folder', 'src_file', 'folder', 'file', 'gross', 'micro']] 
    
    # 데이터 저장
    df_anonymized.to_csv(save_path, index=False)