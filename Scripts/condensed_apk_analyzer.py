import os
import re
from zipfile import ZipFile
import json
'''
Need to analyze for the following:
    - APKs w/ Secure 
    - APKs w/ Insecure Nordic images.
    - APKs w/ Nordic Library 
    - APKs w/ Nordic DFU Library
    - APKs w/ .setUnsafeExperimentalButtonlessServiceInSecureDfuEnabled(true) library call.

2) For every .apk file in the directory:
    a) Run apktool on the original apk file
    
    b) Check the decoded apk for Secure and Insecure Nordic Images
        i) Open the manifest.json file
        ii) If the string "init_packet_data" is in the manifest.json file, it is Insecure. Otherwise Secure.
        iii) If secure, write sha value to file "Nordic_Secure_Image.txt"
        iv) If insecure, write sha value to file "Nordic_Insecure_Image.txt"
    
    c) Check the decoded apk for a Nordic Library and Nordic DFU Library
        i) Search for the directory "no/nordicsemi/". If so, then Nordic Library exists.
        ii) If library exists, then check inside the directory for the path "nordicsemi/android/dfu". If it exists, then Nordic DFU Library is present.
        iii) If "no/nordicsemi/" library exists write sha value to file "Nordic_Library.txt"
        iv) If DFU library exists, write sha value to file "Nordic_DFU_Library.txt"

    d) Check the decoded apk for insecure dfu flag. 
        i) Go through all the files in the apk that end in .java.
        ii) If the line ".setUnsafeExperimentalButtonlessServiceInSecureDfuEnabled(true)" exists within a java file, then the apk has the insecure flag.
        iii) If flag exists, write sha value to file "Insecure_Nordic_DFU_Flag.txt"
        
    e) Once all of the above have been checked, delete the decoded apk file and move to the next apk in the directory.
'''

# Tries to find Nordic firmware images in the given APK
def NordicImages(decoded_apk, original_apk):
    # Go through all of the files in the decompiled apk.
    for subdir, dirs, files in os.walk(decoded_apk):
        for f in files:
            # Locates potential firmware image and checks its contents.
            if f.endswith(".zip"):
                try:
                    with ZipFile(os.path.join(subdir, f), 'r') as zipObj:
                        listZ = zipObj.namelist()
                        binm = re.compile(r".bin")
                        datm = re.compile(r".dat")
                        if "manifest.json" in listZ and any(
                                binm.search(item) for item in listZ) and any(
                                    datm.search(item) for item in listZ):
                            # If the .zip has a manifest.json, *.bin, and *.dat file, we know it's a Nordic Image.
                            # Now we can extract the firmware image and analyze the manifest.json to determine if it is a secure or insecure image.
                            zipObj.extractall(decoded_apk + "/" +
                                              f.replace(".zip", ""))
                            manifest = open(
                                "./" + decoded_apk + "/" + f.split(".")[0] +
                                "/" + "manifest.json", )
                            data = json.load(manifest)

                            insecure = False
                            for (i, j) in data.items():
                                if "init_packet_data" in str(j):
                                    insecure = True
                                    break
                            manifest.close()

                # If the string "init_packet_data" exists in the .json, then we know it's insecure. Otherwise it's secure.
                    if insecure:
                        Nordic_Insecure_Image_List.write(decoded_apk + "\n")
                        Nordic_Insecure_Image_List.flush()
                        print("Nordic Insecure Image Found")
                    else:
                        Nordic_Secure_Image_List.write(decoded_apk + "\n")
                        Nordic_Secure_Image_List.flush()
                        print("Nordic Secure Image Found")
                except Exception:
                    pass

# Tries to find a Nordic library in the given APK
def NordicLibrary(decoded_apk, original_apk):
    # The library is saved as a subdirectory. Therefore we search all subdirectories for the library.
    for root, dirs, files in os.walk(decoded_apk):
        for d in dirs:
            # The library is always saved as "no/nordicsemi".
            if d.lower() == 'no':
                # If the subdirectory exists then we label the current apk as having the nordic lib.
                if os.path.exists(os.path.join(root, d, 'nordicsemi')):
                    Nordic_Lib_List.write(decoded_apk + "\n")
                    Nordic_Lib_List.flush()
                    print("Nordic Library Found")
                    # Now we check to see if the DFU library exists in the apk.
                    if os.path.exists(os.path.join(root, d, 'nordicsemi/android/dfu')):
                        Nordic_DFU_Lib_List.write(decoded_apk + "\n")
                        Nordic_DFU_Lib_List.flush()
                        print("Nordic DFU Library Found")
                    break

# Tries to find the insecure flag within the java code of the decompiled APK
def NordicInsecureFlag(decoded_apk):
    for root, dirs, files in os.walk(decoded_apk):
        for file in files:
            # Check all the java files in the apk
            if file.endswith(".java"):
                file_path = os.path.join(root, file)
                with open(file_path) as file_java:
                    try:
                        # if the insecure flag exists within any java file, then 
                        if "setUnsafeExperimentalButtonlessServiceInSecureDfuEnabled(true)" in file_java.read():
                            Nordic_Insecure_Flag_List.write(decoded_apk + " " + file_path + "\n")
                            Nordic_Insecure_Flag_List.flush()
                            print("Nordic Insecure Flag Found")
                            break
                    except Exception:
                        break


# Open all of the text files to keep track of our labelling.
Nordic_Insecure_Image_List = open("./Nordic_Insecure_Image_List.txt", "a")
Nordic_Secure_Image_List = open("./Nordic_Secure_Image_List.txt", "a")
Nordic_Lib_List = open("./Nordic_Lib_List.txt", "a")
Nordic_DFU_Lib_List = open("./Nordic_DFU_Lib_List.txt", "a")
Nordic_Insecure_Flag_List = open("./Nordic_Insecure_Flag_List.txt", "a")

# Go through the entire directory and keep track of how many apks have been analyzed. This is to 
# help keep track of how many rows to remove from the .csv file.
directory = [apk for apk in os.listdir('.')]
directory.sort()
counter = 0

# Keep track of a hashset of all the apks that we have checked. We do this because for some reason
# an apk is checked twice. Using a set gives us O(1) lookup time to make sure we don't check the
# same apk.
checked = set()

for apk in directory:
    if apk.endswith(".apk") and apk not in checked:
        checked.add(apk)
        # Print to output so that we can see what the last apk checked was in case of a crash or timeout.
        print("Checking " + str(apk))
        resulting_file = apk.split(".")[0]

        # Use jadx to decompile the apk
        os.system("timeout 2m ~/jadx/bin/jadx " + apk)

        # Run the apk to look for Nordic images, libraries, and insecure flags.
        NordicImages(resulting_file, apk)
        NordicLibrary(resulting_file, apk)
        NordicInsecureFlag(resulting_file)

        # Remove any decompiling objects.
        os.system("rm *.jobf")
        counter += 1
        print("COMPLETED: " + str(counter))

# Close the text files before the end of the script.
Nordic_Secure_Image_List.close()
Nordic_Insecure_Image_List.close()
Nordic_Lib_List.close()
Nordic_DFU_Lib_List.close()
Nordic_Insecure_Flag_List.close()
