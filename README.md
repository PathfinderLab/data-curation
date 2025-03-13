# PIT Data Curation Code
This code was used for curating the PIT data. The PIT dataset consists of one or more WSIs per patient, along with paired data such as gross reports and micro reports. The code is mainly divided into two tasks: data pseudonymization and data anonymization.

## Pseudonymization of PIT Data
Pseudonymization of the PIT data was performed for the following attributes: organ, hospital, procedure, and modality. An example of this process is as here:

| Organ                                  | code |
|--------------------------------------|--------|
| Breast                               | BR     |
| Large intestine                      | LI     |
| Esophagus                            | ES     |
| Skin, bone and soft tissue           | SB     |
| Head and neck                        | HN     |
| Hepatobiliary system and pancreas    | HP     |
| Female genital organ                 | FG     |
| Male genital organ                   | MG     |
| Chest                                | CH     |
| Urinary system                       | US     |
| Lymphoreticular system               | LR     |
| Small intestine                      | SM     |
| CNS                                  | CS     |
| Pleura & peritoneum                  | MS     |
| Others                               | MS     |

| Hospital                                  | code |
|--------------------------------------|--------|
| Korea University Anan Hospital       | 01     |

| Procedure                                  | code |
|--------------------------------------|--------|
| operation                            | OP     |
| biopsy                               | BX     |

| Dye                                  | code |
|--------------------------------------|--------|
| HE                                   | IMH    |
| IHC                                  | IMI    |
| SS                                   | IMS    |

## Anonymization Process
The anonymization process includes the following steps:

- `delete_associated_image(slide_path, 'label')`: Removes personal information labels from WSIs.
- `delete_associated_image(slide_path, 'macro')`: Removes personal information macros from WSIs.
- `replace_description(slide_path, anonymized_name)`: Anonymizes personal information in WSI descriptions.
- Extracts gross reports and micro reports from a given CSV file and generates anonymized files.

## Usage

### 1) Pseudonymization
You can obtain a CSV file containing anonymized information by specifying an XLSX file in the same format as the input example and the destination path for saving the output.

#### Input Example (ex. pit_before.xlsx)
```
   num  patient_num file_num           location operation  dye      gross             micro  \
0   0        101        1               Breast  operation   HE   gross report1     micro report1
1   1        101        2               Breast    biopsy    IHC  gross report2     micro report2
```

#### Pseudonymization Code Example

```bash
python csv_file_generation.py \
    --xlsx_path ./pit_before.xlsx \
    --save_path ./pit_after.csv
```

#### Output Example (ex. pit_after.csv)
```
    idx  src_folder src_file      gross             micro  \
0   0       101        1      gross report1     micro report1
1   1       101        2      gross report2     micro report2
...

folder                                  file  
0  PIT-01-BROP-00001  PIT-01-BROP-00001-IMH001  
1  PIT-01-BRBX-00001  PIT-01-BRBX-00001-IMI002  
...
```

### 2) Anonymization
If the data is prepared in the directory structure shown below, it can be anonymized into the corresponding structure as shown. **Please note that the WSIs files are moved rather than copied**.

#### Directory Structure Example (before)
```
PIT_project/
      ├── PIT
      |    ├── pit_after.csv
      |    ├── PIT0
      |    |     ├── 101
      |    |     |    ├── 1.svs
      |    |     |    └── 2.svs
      |    |     ├── 102
      |    |     |    └── 1.svs
          ...
      ├── PIT_anonymized
      |    ├── PIT0
      |    ├── PIT1
          ...
```

#### Anonymization Code Example
```bash
python pit_data_anonymization.py \
    --slide_path /PIT_project/PIT/ \
    --csv_path /PIT_project/PIT/pit_after.csv \
    --anonymized_split /PIT_anonymized/
```

#### Directory Structure Example (after)
```
PIT_project/
      ├── PIT
      |    ├── PIT0
      |    ├── PIT1
          ...
      ├── PIT_anonymized
      |    ├── PIT0
      |    |     ├── PIT-01-BROP-00001
      |    |     |    ├── PIT-01-BROP-00001-IMH001.svs
      |    |     |    ├── PIT-01-BROP-00001-IMH002.svs
      |    |     |    ├── PIT-01-BROP-00001-TXG.txt
      |    |     |    └── PIT-01-BROP-00001-TXM.txt
      |    |     ├── PIT-01-BROP-00002
      |    |     |    ├── PIT-01-BROP-00002-IMH001.svs
      |    |     |    ├── PIT-01-BROP-00002-TXG.txt
      |    |     |    └── PIT-01-BROP-00002-TXM.txt
          ...
```
