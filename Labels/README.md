# Labels

This directory holds all of the labels created so far for each apk analyzed. The same apk SHA value can appear in multiple .txt files given they match
all of the requirements to be labelled as such. For example, if `123.apk` has Bluetooth Permission, had a InSecure Nordic Firmware Image, and contains
the Nordic DFU library, than it will appear in the `BLE_Perm_List.txt`, `Nordic_Insecure_Image.txt`, and `Nordic_DFU_Lib_List.txt` files.

* BLE_Perm_List.txt
    * This file contains all of the SHA values which result in an apk that has bluetooth permissions. 
    * The existence of the Bluetooth Permission is done by checking the contents within an apk's `AndroidManifest.xml` file.
    * This file can be used to recreate the Bluetooth Permissions database in case the database itself becomes corrupted or unreachable.
        * To recreate the database, simply go through all of the SHA values in this file and curl them from the AndroZoo database as can be seen in `script_BLE.py`

* Nordic_DFU_Lib_List.txt
    * This file contains all of the SHA values which result in an apk that has the Nordic DFU Library.
    * The existence of the Nordic DFU Library is done by seeing if the directory `no/nordicsemi/android/dfu` is present in an apk file.

* Nordic_Insecure_Flag_List.txt
    * This file contains all of the SHA values which result in an apk that has an insecure DFU flag within its Java code.
    * The existence of the insecure flag is done by seeing if any Java code in the apk contains the call `setUnsafeExperimentalButtonlessServiceInSecureDfuEnabled(true)`.

* Nordic_Insecure_Image_List.txt
    * This file contains all of the SHA values which result in an apk that has an Insecure Nordic Firmware Image.
    * The existence of an insecure nordic firmware image is done by checking the contents of .zip files within an apk. We look for any number of `.bin` and `.dat` files, as well as exactly 1 `.json file`. We check the contents of the `.json` file for the `init_packet_data` key. If the key exists, then the .zip file is an insecure nordic firmware image.

* Nordic_Lib_List.txt
    * This file contains all of the SHA values which result in an apk that has the Nordic Library.
    * The existence of the Nordic Library is done by seeing if the directory `no/nordicsemi/` is present in an apk file.
    * Note that all of the apks in `Nordic_DFU_Lib_List.txt` will also exist in `Nordic_Lib_List.txt`, but not all apks in `Nordic_Lib_List.txt` will exist in `Nordic_DFU_Lib_List.txt`. This is because if the DFU library is present, then the nordic library is also present by nature. However just because the nordic library is present *does not* mean that the DFU library will be present.

* Nordic_Secure_Image_List.txt
    * This file contains all of the SHA values which result in an apk that has a Secure Nordic Firmware Image.
    * The existence of the secure firmware image is done the same way as the insecure firmware image, but if the `init_packet_data` key does not exist in the `.json` file, then we label it as a Secure Firmware Image.

* skipped.txt
    * This file contains all of the SHA values which could not be downloaded or decompiled.
    * The nature of the reason for failure can be vast. For example, if the AndroZoo database ever goes offline for maintainence, then curl will fail. Additionally, if the downloading of the apk file takes too long or is too large, the connection to the database may drop packets or fail. Regardless, of the reason, the failed SHA value is added to this list.
    * Ideally, after the full AndroZoo database is scanned, the SHA values in this list are visited last to complete the analysis.