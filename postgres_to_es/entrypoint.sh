#!/bin/sh
if [ "$POSTGRES_DB_NAME" = "postgres" ]
then
    echo "Waiting for Elasticsearch..."

   open=0;
   while [ $open -eq 0 ]
   do
      check_port=`nc -v -w 1 -i 1 es 9200 &> /dev/stdout`
      echo $check_port
      if [[ "$check_port" == *"succeeded"* ]]
      then
        break
      fi
        sleep 1
  done
    echo "Elasticsearch started"
fi

python -m etl