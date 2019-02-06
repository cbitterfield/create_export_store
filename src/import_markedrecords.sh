#!/bin/bash
DATABASE="edge"

echo "database: $DATABASE"
echo "File to process:$1"
echo "Tablename: $2"
echo "Username:$3"
DATE="`date '+%Y%m%d-%H%S'`"

HEADER="DROP TABLE if exists ${2} ; CREATE TABLE ${2} like markedrecords_source"

if [ $4 ]; then
	echo "Password is set but not displayed"
fi

if [ $1 ]; then


echo "Step 1: Process XML in file $1"
cp  $1 processs_file_${DATE}.xml
tidy -utf8 -xml -output process_file${DATE}_tidy.xml -f process_file${DATE}_errors.log -i processs_file_${DATE}.xml
cat process_file${DATE}_tidy.xml | sed 's/<metadata>//g' | sed 's/<\/metadata>//g' > process_file${DATE}_nm.xml
RECORDLINES="`grep -n '<\/RECORD>' process_file${DATE}_nm.xml | head -1 | awk -F: ' { print  $1 } '`"
LIST=`head -${RECORDLINES} process_file${DATE}_nm.xml | egrep -o '<[a-zA-Z_]+>' | sed 's/<//g' | sed 's/>//g' | sed 's/RECORD//g' | sed 's/PICTICON_S//g' | uniq `
java -jar ./xml2csv/xml2csv-*.jar --input process_file${DATE}_nm.xml --output /tmp/$2.csv --columns `echo $LIST | sed 's/ /,/g'` --item-name /PICTICON_RECORDS/RECORD

echo "$HEADER $TABLECOMMAND"
mysql --host=localhost --user=$3 --password=$4  -e "$HEADER " $DATABASE



echo "Step 2: Import to MySQL, drop and create table first"
mysqlimport --host=localhost --user=$3 --password=$4  --fields-terminated-by=',' --fields-enclosed-by='"' -f -i -d --ignore-lines=1 edge /tmp/$2.csv
mysql --host=localhost --user=$3 --password=$4  -e "CALL create_num_cast; CALL load_marked_data(); " $DATABASE

else
	echo "$0 filename [File To process] [ tablename ] [ username ] [ password ]"
	echo "Database name is set inside this program"
	echo "This program does not validate input"
fi
