
//Define Global Structures
const WebAPI_MainURL = "http://API.loot.agency:28015/";
const WebAPI_TestURL = "http://localhost:28015/";
var DebugMode = true;
const WebAPI_Endpoints = {
    Cluster_status:"api/v1/cluster/status",
};

//--------------------------------------------------------------------------------------------
function get_cluster_information(Callback){
    //Send Request to get Profile For user
    GetRequest(WebAPI_Endpoints.Cluster_status)
        .then((data) => {
            if (data.info) {
                console.log("Cluster Information: " + data.info);
                if(Callback){
                    return Callback();
                }
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
