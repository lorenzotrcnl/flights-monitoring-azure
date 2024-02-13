> [!NOTE]  
> All the steps reported in this file must be executed inside the azure-cli container:
``` sh
> docker exec -it azure-cli bin/bash
```

## Resource group
If you want to change the name of the resources or other parameters, you can do it by modifying the `architecture/main.bicep` file.

> [!NOTE]  
> Make sure that all the required fields in the main.bicep file have been filled in (e.g., *var administratorLoginPassword*).

Proceed then to create the resource group and the resources:
``` sh
> cd home
> az login
> az group create --name <NAME> --location <LOCATION>
> az deployment group create --resource-group <NAME> --template-file main.bicep
```

Check the newly created resource by heading into the [Azure Portal](portal.azure.com/#home).

`From there you must manually create the Azure Stream Analytics resource.`

## Environment secrets

As access keys and connection strings are required, it is necessary to add or modify the following files:
* `.env`, inside `architecture/agents`. The file should contain:
    * **COSMOS_CONNECTION_STR**='primary connection string of CosmosDB resource'
* `local.settings.json`, inside `architecture/functions/cosmosTrigger`. The file should contain:
``` json
{
  "IsEncrypted": false,
  "Values": {
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AzureWebJobsFeatureFlags": "EnableWorkerIndexing",
    "AzureWebJobsStorage": "CONNECTION STRING OF THE STORAGE ACCOUNT",
    "CosmosDBConnection": "CONNECTION STRING OF COSMOSDB RESOURCE",
    "EventHubConnection": "CONNECTION STRING OF EVENTHUB RESOURCE"
  }
}
```

The latter file is required to correctly deploy the trigger function in the cloud. 
The function has been created following [this steps](https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-cli-python?tabs=linux,bash,azure-cli&pivots=python-mode-decorators) and lives inside ``architecture/functions/cosmosTrigger``.

To deploy it into Azure to effectively make it work you must push the function using:
``` sh
> cd home/functions/cosmosTrigger
> func azure functionapp publish <FUNCTION_APP_RESOURCE_NAME> --publish-local-settings
```

## Setup PostgreSQL

When deploying resources, the required tables are not automatically created. Therefore, it is necessary to proceed via the CLI.

``` sh
> psql --host=<POSTGRESQL_RESOURCE_URL> --port=5432 --username=<ADMINISTATOR_LOGIN> --dbname=<DB_NAME>
You will be prompted to enter the password
```

I provide just one example of table creation, which should reflect the same name in the output of queries in Azure Stream Analytics (see the next step).
``` sql
> CREATE TABLE coords (
    icao24bit VARCHAR(50),
    latitude VARCHAR(50),
    longitude VARCHAR(50),
    ts TIMESTAMP
);
```


## Setup ASA
Head over into the [Azure Portal](portal.azure.com/#home) and access the Azure Stream Analytics resource. 

Click on Query and from there fill the following field:
* Input (EventHub): it should find automatically the eventhub resource and related connection parameters
* Output (PostgreSQL)
    1. Alias **queryCoords**; In the *Table* field insert the relative table previously created
    2. Alias **queryNFlights**; //
    3. Alias **queryFTable**; // 

In the query editor insert:

``` sql
/*
coords
*/

SELECT DISTINCT "icao_24bit"
    "icao_24bit",
    "latitude",
    "longitude",
    "ts"
INTO queryCoords
FROM
    [flights-eventhub]
ORDER BY
    "fr_id",
    "ts" DESC;


/*
current n flights
*/

SELECT DISTINCT "fr_id"
    "fr_id",
    "ts"
INTO queryNFlights
FROM
    [flights-eventhub]
ORDER BY
    "fr_id",
    "ts" DESC;


/*
flights table
*/
SELECT DISTINCT "registration"
    "registration",
    "origin_airport_iata",
    "destination_airport_iata",
    "ts"
INTO queryFTable
FROM
    [flights-eventhub]
WHERE "origin_airport_iata" != ""
ORDER BY
    "ts" DESC;
```