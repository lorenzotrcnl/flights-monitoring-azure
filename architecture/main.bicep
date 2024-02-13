
param location string = resourceGroup().location

var eventHubSku = 'Standard'
var eventHubNamespaceName = 'flights-eventhub-namespace'
var eventHubName = 'flights-eventhub'
module eventhubModule 'modules/eventhub.bicep' = {
  name: 'eventhubModule'
  params: {
    location: location
    eventHubSku: eventHubSku
    eventHubNamespaceName: eventHubNamespaceName
    eventHubName: eventHubName
  }
}

var accountName = 'flights-cosmos-account'
var databaseName = 'flights-cosmos-db'
var containerName = 'flights'
module dbModule 'modules/db.bicep' = {
  name: 'dbModule'
  params: {
    location: location
    accountName: accountName
    databaseName: databaseName
    containerName: containerName
  }
}

var appName = 'flights-functionApp'
var storageAccountName = 'flightsstoragefa'
var storageAccountType = 'Standard_LRS'
module functionModule 'modules/functionapp.bicep' = {
  name: 'functionModule'
  params: {
    appName: appName
    location: location
    storageAccountName: storageAccountName
    storageAccountType: storageAccountType
  }
}


var administratorLoginPassword = ''
var pglocation = 'northeurope'
var administratorLogin = 'flightsadmin'
var serverName = 'flights-postgresql'
module postgresModule 'modules/postgres.bicep' = {
  name: 'postgresModule'
  params: {
    location: pglocation
    administratorLogin: administratorLogin
    administratorLoginPassword: administratorLoginPassword
    serverName: serverName
  }
}
