# CSV merger

This script was created in order to merge csv files with the same structure.

## Usage

To run merger just type the following command:
```bash-script
python csv_merger.py prune in1.csv in2.csv in3.csv
```

As a result new `merged` folder would be created and 2 files in it:
* `in1.csv_in2.csv` - result of merging first two files;
* `in1.csv_in2.csv_in3.csv` - result of merging all three files.

All files must have the same columns (otherwise script won't work).
