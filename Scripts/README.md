# Script

This directory contains the 2 scripts used for the Firmware analysis. In order to simplify the scripts and in turn to speed analysis time, the scripts are seperated into 2 tasks

1. Create a database of only apks with BLE Permissions
2. Analyze Bluetooth APK for labelling.
    * See the `Labels` directory for a full list of the labels we look for. 

The scripts have detailed comments to help with understanding the logic. Regardless, here is a high level overview on how the scripts work.

* `condensed_apk_analyzer.py`
    * Analyzes all apks in the current directory. 
    * Checks each apk for the existence of the following:
        * Nordic DFU Library
        * Nordic Insecure Flag
        * Nordic Insecure Image
        * Nordic Library
        * Nordic Secure Image
    * If a given item in the list above does exist in the current apk, then add that apk's SHA value to the corresponding .txt file which can be found in the `Labels` directory.
    * Note that this script is modular. So if we no longer need to check for a given existence, simply commenting out the corresponding method call will remove it from the analysis. Similarly, if we need to add a new existence, we can simply create a new method to check for that existence given an apk and add it to the list of method calls.

* `script_BLE.py`
    * Pulls an APK from the AndroZoo database using a given SHA value
        * The SHA values are derived from the csv files found in the `csv` directory.
    * If the APK has bluetooth permissions, then it is saved into the `BLE_Perm` database. Otherwise the apk file is deleted.
    * The script uses the `curl` command to pull from the database, and the `axmldec` library to decompile the `AndroidManifest.xml` file.
        * Note that the reason why we only decompile the `AndroidManifest.xml` file is because it takes significantly less time to check as opposed to checking the entire apk.
        * Ensure that both of these libraries are installed and work properly before running this script or it will always fail.

Note that the logic of both these scripts can be combined to make 1 large script that does all of the above, however in my experience this has resulting in very rigid code that is hard to modify and follow later. That being said, these scripts can be run in parallel to each other. Since `condensed_apk_analyzer.py` does not download and takes more time to go through one apk, it can be run in parallel to `script_BLE.py` which can go through apks at a faster pace. Keep in mind however that the amount of time `curl` will take to download an apk file depends on the status of AndroZoo at the time as well as the strength of the user's internet connection. So there may be some cases in which `condensed_apk_analyzer.py` waits for `script_BLE.py` to download more apks to analyze.