
//Define Global Structures
const WebAPI_MainURL = window.location.href;
const WebAPI_TestURL = window.location.href;
var DebugMode = true;
const WebAPI_Endpoints = {
    Cluster_status:"api/v1/cluster/status",
};


function update_page(data){
    //update the page with the data
    console.log("Updating page with data");
    // THis is called as a callback for the GET request
    // update the Text on the page
    document.getElementById('HEALTH_OK').value = "Not Specified";


}


// 	"cluster_health": "HEALTH_OK",
// 	"cluster_health_color": GREEN,
// 	"nodes_online": "0 Nodes",
// 	"nodes_online_color": RED,
// 	"failover_status": "Failover Ready",
// 	"failover_status_color": GREEN,
// 	"cloud_provider_aws": "0/2 Deployed",
// 	"cloud_provider_aws_color": RED,
// 	"cloud_provider_other": "0/2 Deployed",
// 	"cloud_provider_other_color": RED,
// 	"cloud_provider_azure": "0/2 Deployed",
// 	"cloud_provider_azure_color": RED,
// 	"cloudwatch_operator": "0/2 Deployed",
// 	"cloudwatch_operator_color": RED,
// 	"cloudwatch_dashboard": "0/2 Deployed",
// 	"cloudwatch_dashboard_color": RED,
// 	"cloudwatch_Healthcheck": "0/2 Deployed",
// 	"cloudwatch_Healthcheck_color": RED


//--------------------------------------------------------------------------------------------
function get_cluster_information(Callback){
    //Send Request to get Profile For user
    GetRequest(WebAPI_Endpoints.Cluster_status)
        .then((data) => {
            if (data.cluster_health) {
                console.log("Cluster Information: " + data.cluster_health);
                console.log("Updating page with data");
                // Cluster Health
                //update the Color of the Cluster Health
                document.getElementById('HEALTH_OK').style.color = data.cluster_health_color;
                document.getElementById('HEALTH_OK').innerHTML = data.cluster_health;

                // Nodes Online
                //update the Color of the Nodes Online
                document.getElementById('n__Nodes').style.color = data.nodes_online_color;
                document.getElementById('n__Nodes').innerHTML = data.nodes_online;
                // Failover Status
                //update the Color of the Failover Status
                document.getElementById('Failover_Ready').style.color = data.failover_status_color;
                console.log("Failover Status: " + data.failover_status);
                console.log("Failover Status Color: " + data.failover_status_color);
                document.getElementById('Failover_Ready').innerHTML = data.failover_status;
                //Cloud_Providers
                //AWS
                //update the Color of the AWS
                document.getElementById('n_2_Deployed_ce').style.color = data.cloud_provider_aws_color;
                document.getElementById('n_2_Deployed_ce').innerHTML = data.cloud_provider_aws;
                //Azure
                //update the Color of the Azure
                document.getElementById('n_2_Deployed_cj').style.color = data.cloud_provider_azure_color;
                document.getElementById('n_2_Deployed_cj').innerHTML = data.cloud_provider_azure;
                //Other
                //update the Color of the Other
                document.getElementById('n_2_Deployed_cn').style.color = data.cloud_provider_other_color;
                document.getElementById('n_2_Deployed_cn').innerHTML = data.cloud_provider_other;
                //CloudWatch_Operator
                //update the Color of the CloudWatch_Operator
                document.getElementById('n_2_Deployed').style.color = data.cloudwatch_operator_color;
                document.getElementById('n_2_Deployed').innerHTML = data.cloudwatch_operator;
                //CloudWatch_Dashboard
                //update the Color of the CloudWatch_Dashboard
                document.getElementById('n_2_Deployed_bc').style.color = data.cloudwatch_dashboard_color;
                document.getElementById('n_2_Deployed_bc').innerHTML = data.cloudwatch_dashboard;
                //CloudWatch_Healthcheck
                //update the Color of the CloudWatch_Healthcheck
                document.getElementById('n_1_Deployed').style.color = data.cloudwatch_Healthcheck_color;
                document.getElementById('n_1_Deployed').innerHTML = data.cloudwatch_Healthcheck;
                //All Text Updated
            } else {
                console.log("Error: [GET Failed]");
            }
        })
}
//--------------------------------------------------------------------------------------------
async function POSTRequest(API_Endpoint, JSONData) {
    let URL;
    if(DebugMode){
        URL = WebAPI_TestURL
    }else{
        URL = WebAPI_MainURL
    }
    //Pull most Recent Token From Storage
    let Token = localStorage.getItem('current_token');
    if(!Token){
        console.log("POST Request made With No Token")
    }
    //Send POST Request
    const response = await postData('' + URL + API_Endpoint + '?token=' + Token, JSONData)
        .then((data) => {
            if (data) {
                //Data Pulled successfully
                console.log("LOG: Data POST at endpoint " + API_Endpoint + " Was Successful");
                console.log(data);
                return data;
            } else {
                console.log("LOG: Data POST at endpoint " + API_Endpoint + " Failed");
            }
        });
    return await response;
}
//--------------------------------------------------------------------------------------------
async function postData(url = '', data = {}) {
    // Default options are marked with *
    const response = await fetch(url, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        headers: {
            'Content-Type': 'application/json'
            // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *client
        body: JSON.stringify(data) // body data type must match "Content-Type" header
    });
    return await response.json(); // parses JSON response into native JavaScript objects
}
//--------------------------------------------------------------------------------------------
async function GetRequest(API_Endpoint) {
    let URL;
    if(DebugMode){
        URL = WebAPI_TestURL
    }else{
        URL = WebAPI_MainURL
    }
    //Pull most Recent Token From Storage
    let Token = localStorage.getItem('current_token');
    if(!Token){
        console.log("GET Request made With No Token")
    }
    //Send GET Request
    const response = await getData('' + URL + API_Endpoint + '?token=' + Token)
        .then((data) => {
            if (data) {
                //Data Pulled successfully
                console.log("LOG: Data Get at endpoint " + API_Endpoint + " Was Successful");
                console.log(data);
                return data;
            } else {
                console.log("LOG: Data Get at endpoint " + API_Endpoint + " Failed");
            }
        });
    return await response;
}
//--------------------------------------------------------------------------------------------
async function getData(url = '', data = {}) {
    const response = await fetch(url, {
        method: 'GET', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        headers: {
            // 'Content-Type': 'application/json'
            // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *client
        //  body: JSON.stringify(data) // body data type must match "Content-Type" header
    });
    return await response.json(); // parses JSON response into native JavaScript objects
}
