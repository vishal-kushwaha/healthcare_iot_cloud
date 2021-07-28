# Healthcare IoT project:
This solution uses [pynamodb](https://github.com/pynamodb/PynamoDB) and [pandas](https://pandas.pydata.org/) to solve the problem statements for this project

## File structure:
* [models](models): model classes for accessing DynamoDB tables
* [attributes](attributes): custom attributes for model classes
* [rules](rules): rule files as json and wrapper class acting as parser
* [screenshots](screenshots): screenshots for first part of problem statement
* [simulator](simulator): code provided for simulating the bedside monitor devices
* [src.py](src.py): code implementation for problem statements
* [main.py](main.py): code to demonstrate the solution
* [stdout.txt](stdout.txt): console output
* [requirements.txt](requirements.txt): requirements file

## Assumptions:
* It is assumed that the queries from table bsm_agg_data and bsm_alerts will be for devices and time range, hence the data is nested in those tables (refer to screenshots below)

## Solution:
1. Generating bsm_data
   
   Use following commands to simulate two devices:
   
   `cd simulator`
   
   `python BedSideMonitor.py -e a1iuxfdjit1v4w-ats.iot.us-east-1.amazonaws.com -r root-CA.crt -c BSM_G101/1507b0a38d-certificate.pem.crt -k BSM_G101/1507b0a38d-private.pem.key -id BSM_G101 -t iot/bsm`

   `python BedSideMonitor.py -e a1iuxfdjit1v4w-ats.iot.us-east-1.amazonaws.com -r root-CA.crt -c BSM_G102/e3e12268ec-certificate.pem.crt -k BSM_G102/e3e12268ec-private.pem.key -id BSM_G102 -t iot/bsm`

   Following screenshots are available in screenshots folder:
   * bsm_data_table.png
     ![bsm data table](screenshots/bsm_data_table.png?raw=true "bsm_data table screenshot")
   * rule.png
     ![rules](screenshots/rule.png?raw=true "rules screenshot")
   * things.png
     ![things](screenshots/things.png?raw=true "things screenshot")
   

2. Problem 2
   1. Create bsm_agg_data table:
      1. Create 'bsm_agg_data 'table programmatically
         
         [src.py#L46](src.py#L46)
      2. model for database actions
         
         [models.bsm_agg_data.BsmAggData class](models/bsm_agg_data.py)
   2. Functionality to aggregate data 
      1. aggregation
         
         [src.py#L12](src.py#L12)
      2. write data to DynamoDB
         
         [src.py#L43](src.py#L43)
   

   Sample entry from bsm_agg_data table
   ![Sample alert entry](screenshots/aggr.png?raw=true "An entry from aggregate table")
      

      It is assumed that the aggregated data will be quered on the basis of deviceid (hash key) and timestamp (sort key).
      Hence, the sensor data for a given device and timestamp is stored as a nested document. For example, plotting all sensory data for a device.
      If needed data for only a given sensor can also be extracted.

      BsmAggData.get(
         'BSM_G101',
         datetime(year=2021, month=6, day=26, hour=5, minute=58),
         attributes_to_get=['deviceid','timestamp' ,'data.Temperature']
         ).serialize()
      
      returns
      
      {
        "data": {
          "M": {
            "Temperature": {
              "M": {
                "avg": {
                  "N": "98.10000000000001"
                },
                "max": {
                  "N": "101.2"
                },
                "min": {
                  "N": "95.4"
                }
              }
            }
          }
        },
        "deviceid": {
          "S": "BSM_G101"
        },
        "timestamp": {
          "S": "2021-06-26 05:58:00"
        }
      }
      
      
3. Problem 3
   1. Create rules config
      1. config rules
         
         [Heart Rate](rules/heart_rate.json)
         
         [SpO2](rules/spo2.json)
         
         [Temperature](rules/temperature.json)
      2. parser
      
         [rules.rule.Rule class](rules/rule.py)
   2. Detect anomaly
      1. assessment for alerts
         
         [src.py#L23](src.py#L23)
      2. create 'bsm_alerts' table programmatically
         
         [src.py#L87](src.py#L87)
      3. Rule check
         
         [src.py#L29](src.py#L29)
      4. write data to DynamoDB
   
         [src.py#L84](src.py#L84)
   

   Sample entry from bsm_alerts table
   ![Sample alert entry](screenshots/alert.png?raw=true "An entry from alert table")


      It is assumed that the alerts data will be quered on the basis of deviceid (hash key) and timestamp (sort key).
      Hence, the alert data for a given device and timestamp is stored as a nested document.
      For example, getting all alerts for a device in given time range.
      If needed data for only a given sensor can also be extracted.
