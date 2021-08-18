Alfalfa Database
=================
Usage
-----
1. Store Chr1.txt through Chr8.txt into ./static/DNA
2. Store Alfalfa.db into ./static/sql
3. Run get_max_vcfID.sql and get_min_vcfIDs.sql on Alfalfa.db
4. Edit ./app.py: on Line 264 and 265, replace max_pos and the first 8 values of arr[] by the query results in step 3.
5. Activate vituralenv by running "$ source ./env/bin/activate" on command line at this directory
6. Run ./app.py with the virtual environment, ip address would be printed to console window.
