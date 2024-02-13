import azure.functions as func
import datetime
import json
import logging

app = func.FunctionApp()

@app.function_name(name="CosmosDBTrigger")
@app.cosmos_db_trigger(arg_name="dbevent", 
                       container_name="flights",
                       database_name="flights-cosmos-db", 
                       connection="CosmosDBConnection",
                       lease_container_name="leases", 
                       create_lease_container_if_not_exists="true")
@app.event_hub_output(arg_name="hubevent",
                      event_hub_name="flights-eventhub",
                      connection="EventHubConnection")
def cdbTrigger(dbevent: func.DocumentList, hubevent: func.Out[str]):
    logging.info('Python CosmosDB triggered.')
    body = dbevent[0]
    if body is not None:
        hubevent.set(body.to_json())
    else:
        logging.info('dbevent body is none')