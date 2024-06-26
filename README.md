# Giboo Grant Crawler

## Install packages

```
python3 -m venv ./venv
. venv/bin/activate
pip install -r requirements.txt
```

## Input file format (CSV)

Note that _id here is Rank from Won-Yong's file.

```
_id,name,business_name_2,ein,url
1,FIDELITY INVESTMENTS CHARITABLE GIFT FUND,,110303001,https://www.fidelitycharitable.org/
2,BILL & MELINDA GATES FOUNDATION,,562618866,https://www.gatesfoundation.org/
3,LOOKOUT TRUST,,836462138,https://lookout.org/
...

```

## Run crawler

You can make run.sh file.
This file will paginate csv file and run crawler subprocesses to control resource consumption.

```
#!/bin/bash

export MONGO_URL="mongodb://masTerUser:***@giboo-mongodb"
export MONGO_DATABASE="crawler"
export START_URL_FILE="donors_philanthropy_URL.csv"

STEP=4
START=0
END=75000
END=`expr $END - $STEP`


for i in $(seq $START $STEP $END)
do
    python run.py $i `expr $i + $STEP`
done
```

## Aggregate from MongoDB

```
[
  {
    $match:
      {
        timestamp: {
          $gt: ISODate("2022-06-21"),
        },
      },
  },
  
  {  $group:
      {
        _id: {
          rank: "$rank",
          ein: "ein",
          name: "name",
        },
        urls: {
          $push: {
            url: "$url",
            msg: "$msg",
            text: "$text",
          },
        },
      },
  },
  {
    $project:
      {
        _id: 0,
        rank: "$_id.rank",
        name: "$_id.name",
        ein: "$_id.ein",
        urls: 1,
      },
  },
  {
    $sort:
      {
        rank: 1,
      },
  },
]
```


