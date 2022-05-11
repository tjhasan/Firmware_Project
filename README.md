# Firmware Project
This project consists of 3 directories:
* Labels
  * Contains the SHA value labelling so far from the AndroZoo database.
* Scripts
  * Contains the scripts used to interact with the AndroZoo database as well as labelling the apks that came from them. 
* csv
  * Contains the .csv files which contain the sha values that can be used to interact with the AndroZoo database.

Within each directory are more details on its contents. 

## Prerequisites

### Libraries
This list is assuming that you are using Python 3.x

* `jadx`
  * Download the .zip file for the latest release [here](https://github.com/skylot/jadx/releases)
  * Don't download the window zip files, we simply need the binary which can be found in the generic .zip file.

* `axmldec`
  * Follow the instructions described [here](https://github.com/ytsutano/axmldec)


### Directory Structure
Before running any of the scripts, ensure that you have the following directory structure (assuming Unix based system):

```
~
└───BLE_Perm/
│   │   0000.apk
│   │   0001.apk
│   │   0002.apk
│   │   ...
│
└───csv/
│   │   part_1.csv
│   │   part_2.csv
│   │   part_3.csv
│   │   part_4.csv
│ 
└───Labels/
│   │   BLE_Perm_List.txt
│   │   Nordic_DFU_Lib_List.txt
│   │   Nordic_Insecure_Flag_List.txt
│   │   Nordic_Insecure_Image_List.txt
│   │   Nordic_Lib_List.txt
│   │   Nordic_Secure_Image_List.txt
│   │   skipped.txt
│
└───Scripts/
│   │   condensed_apk_analyzer.py
│   │   BLE_Perm.py
|   └───Temp/
│       │   ...
│
└───axmldec/
│   │   ...
│
└───jadx/
    │   ...

```