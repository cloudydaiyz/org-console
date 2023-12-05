function logResults(msg) {
    console.log(window.location.pathname);
    document.getElementById("resultsBox").innerText = msg;
}

function updateMembershipLogs() {
    logResults("Requesting membership log update...");
    fetch("http://localhost:5001/updatelogs", {
        mode: "cors"
    }).then((response)=> {
        console.log(response);
        if(!response.ok) {
            throw new Error("Not okay");
        }
        return response.json()
    }).then((data) => {
        console.log(data);
        logResults("Updated membership logs successfully");
    }).catch((error) => {
        console.log(error);
        console.log("Request was not okay");
        logResults("Membership logs update unsuccessful");
    });
}

function sendLeadershipUpdate() {
    logResults("Leadership update isn't implemented yet. ");
}