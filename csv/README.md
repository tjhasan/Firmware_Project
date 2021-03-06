# CSV

This directory contains .csv files which contain the SHA values required to download all of the apks from the AndroZoo database. The reason why it is in 4 parts is to allow parallelization of the analysis. We can run the `script_BLE.py` on all 4 parts at the same time using the unix `screen` command. More details about this command and how to use it can be found [here](https://linuxize.com/post/how-to-use-linux-screen/)

Here are the column labels in the order as they appear:

`sha256, sha1, md5, apk_size, dex_size, dex_date, pkg_name, vercode, vt_detection,vt_scan_date, markets`

More details on each of the columns can be found in the [AndroZoo website](https://androzoo.uni.lu/lists)

For the purposes of our analysis, we simply need the first column of each row: `sha256`. This allows us to download that apk using our api key which can be seen in the `script_BLE.py`. 

## Cutting CSV File

There may come times when the script needs to be stopped for some reason. It would be a waste of time to go back through SHA values that we have already analyzed. This is why `script_BLE.py` keeps track of a Counter variable and prints it to the screen. Once the script stops running, use the latest number printed in the following command:

```console
foo@bar:~/csv/$  sed -i '1,[x]d' part_[y]
```

x = The latest number printed to the screen before the script stopped.

y = [1 - 4] indicating which part to modify.
