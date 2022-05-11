import csv
import os
import sys
from xml.dom import minidom
from time import sleep

# 1) Download APK
# 2) Use axmldec to decode apk's .xml file
# 3) Read .xml file for Bluetooth permission. If Bluetooth permission exists:
#     a) Set BLE variable to True
# 4) If no BLE permission is found, delete the .apk file and its .xml
# 5) if BLE permission is found move the apk to "./BLE_Perm/.apk"
# 6) Set BLE var to False

BLE_Perm = "../BLE_Perm/"
Temp = "./Temp/"
Counter = 0
Bluetooth = False

if not os.path.exists(BLE_Perm):
    os.makedirs(BLE_Perm)

if not os.path.exists(Temp):
    os.makedirs(Temp)

# The skipped text file keeps track of apks we need to check again due to some error occurring.
skip = open("./skipped.txt", "a")

# Open the csv file containing all of the apk hashes.
file = open(sys.argv[1])
csv_reader = csv.reader(file)


# Get the hashes from the csv file row by row.
for row in csv_reader:
    sha = row[0]
    apk = sha + ".apk"
    xml = sha + ".xml"
    zip = sha + ".zip"
    print("Downloading file...")

    # Try and download the apk with the current hashfile.
    try:
        sleep(0.5)
        os.system(
            "curl -O --remote-header-name -G -d apikey=["API KEY GOES HERE"] -d sha256="
            + sha + " https://androzoo.uni.lu/api/download")
    except Exception:
        # The curl command doesn't return an exception so we need to check for curl errors later in the code.
        pass
    print("Decoding AndroidManifest.xml...")

    # Copy the .apk file to Temp. This is because the .apk file is converted to .zip and we need to keep a copy of the .apk just in case.
    os.system("cp " + apk + " " + Temp)

    # Convert the .apk file to a .zip file and unzip it.
    os.system("mv " + apk + " " + zip)
    os.system("unzip -q " + zip + " -d " + sha)

    # Decode the .xml file.
    os.system("~/axmldec/axmldec -o " + xml + " -i " + sha + "/AndroidManifest.xml")

    try:
        xmldoc = minidom.parse("./" + xml)
    except Exception:
        # If an exception occurs when trying to parse the .xml, that means that there was a curl error when trying to download.
        # simply remove the files related to it and add it to the skipped text file to check later.
        print("Curl error, skipping...")
        os.system("rm -rf ./" + zip)
        os.system("rm -rf " + Temp + apk)
        skip.write(sha + "\n")
        Counter += 1
        print("COMPLETED: ", Counter)
        continue
    # If the .xml file was successfully compiled then look for the Bluetooth permission.
    try:
        itemlist = xmldoc.getElementsByTagName('uses-permission')
        for s in itemlist:
            if s.attributes[
                    'android:name'].value == "android.permission.BLUETOOTH":
                Bluetooth = True
                print("Bluetooth permission found...")
                break
    except Exception:
        pass

    # If the bluetooth permission doesn't exist then remove all of the related files and go to the next hash value
    if Bluetooth is False:
        print("Permission not found, skipping...")
        os.system("rm -rf "+ Temp + apk)
        os.system("rm -rf ./" + xml)
        os.system("rm -rf ./" + zip)
        os.system("rm -rf ./" + sha)
        Counter += 1
        print("COMPLETED: ", Counter)
        continue
    # Otherwise move the .apk copy from Temp to the BLE_Perm directory. Then delete all of its unneccesary .zip, directory, and .xml files.
    else:
        Bluetooth = False
        print("Sending discovered Bluetooth apk to BLE_Perm Directory")
        os.system("mv " + Temp + apk + " " + BLE_Perm)
        os.system("rm -rf ./" + xml)
        os.system("rm -rf ./" + sha)
        os.system("rm -rf ./" + zip)
    Counter += 1
    print("COMPLETED: ", Counter)
