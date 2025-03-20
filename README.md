# PIT Data Curation Code
This code was used for curating the PIT data. The PIT dataset consists of one or more WSIs per patient, along with paired data such as gross reports and micro reports. The code is mainly divided into two tasks: data pseudonymization and data anonymization.

## 1. Pseudonymization of PIT Data
Pseudonymization of the PIT data was performed for the following attributes: organ, hospital, procedure, and modality. An example of this process is [here](#1-pseudonymization):

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

## 2. Anonymization Process
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
0   0        101      101_1             Breast  operation   HE   gross report1     micro report1
1   1        101      101_2             Breast  operation   HE   gross report1     micro report1
2   2        101      101_3             Breast  operation  IHC   gross report1     micro report1
3   3        102      102_1             Breast  operation   HE   gross report2     micro report2
4   4        103      103_1             Breast   Biopsy    IHC   gross report3     micro report3
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
0   0       101      101_1    gross report1     micro report1
1   1       101      101_2    gross report1     micro report1
2   2       101      101_3    gross report1     micro report1
3   3       102      102_1    gross report2     micro report2
4   4       103      103_1    gross report3     micro report3
...

folder                                  file  
0  PIT-01-BROP-00001  PIT-01-BROP-00001-IMH-001.svs  
1  PIT-01-BROP-00001  PIT-01-BROP-00001-IMH-002.svs
2  PIT-01-BROP-00001  PIT-01-BROP-00001-IMI-001.svs
3  PIT-01-BROP-00002  PIT-01-BROP-00002-IMH-001.svs
4  PIT-01-BRBX-00001  PIT-01-BRBX-00001-IMI-001.svs
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
      |    |     |    ├── 101_1.svs
      |    |     |    ├── 101_2.svs
      |    |     |    └── 101_3.svs
      |    |     └── 102
      |    |          └── 102_1.svs
      |    └── PIT1
      |          └── 103
      |               └── 103_1.svs
      └── PIT_anonymized
           ├── PIT0
           └── PIT1
```

#### Anonymization Code Example
```bash
python pit_data_anonymization.py \
    --slide_base /PIT_project/PIT/ \
    --csv_path /PIT_project/PIT/pit_after.csv \
    --anonymized_split /PIT_anonymized/
```

#### Directory Structure Example (after)
```
PIT_project/
      ├── PIT
      |    ├── pit_after.csv
      |    ├── PIT0
      |    └── PIT1
      | 
      └── PIT_anonymized
           ├── PIT0
           |     ├── PIT-01-BROP-00001
           |     |    ├── PIT-01-BROP-00001-IMH-001.svs
           |     |    ├── PIT-01-BROP-00001-IMH-002.svs
           |     |    ├── PIT-01-BROP-00001-IMI-001.svs
           |     |    ├── PIT-01-BROP-00001-TXG.txt
           |     |    └── PIT-01-BROP-00001-TXM.txt
           |     └── PIT-01-BROP-00002
           |          ├── PIT-01-BROP-00002-IMH-001.svs
           |          ├── PIT-01-BROP-00002-TXG.txt
           |          └── PIT-01-BROP-00002-TXM.txt
           └── PIT1
                 └── PIT-01-BRBX-00001
                      ├── PIT-01-BRBX-00001-IMI-001.svs
                      ├── PIT-01-BRBX-00001-TXG.txt
                      └── PIT-01-BRBX-00001-TXM.txt
```
