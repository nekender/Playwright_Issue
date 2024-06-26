export START_URL_FILE="union_data.csv"

START=0 
END=2
STEP=1
END=$(expr $END - $STEP)

echo "Starting script execution..."

# Execute Python script
for i in $(seq $START $STEP $END)
do
    python run.py $i $(expr $i + $STEP)
done

echo "Script execution complete."
