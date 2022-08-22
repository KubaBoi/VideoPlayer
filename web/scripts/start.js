var debug = false;
var alertTime = 2000;

getAllVideos();

async function getAllVideos() {
    let tbl = document.getElementById("videoTable");
    clearTable(tbl);

    let resp = await callEndpoint("GET", "/video/getAll");
    if (resp.ERROR == null) {
        let shows = resp.SHOWS;
        
        for (const [showName, value] of Object.entries(shows)) {
            
            addHeader(tbl, [{"text": showName}, {"text": "============================"}]);

            for (const [serie, videoArray] of Object.entries(value)) {
                addHeader(tbl, [{"text": serie}]);

                for (let i = 0; i < videoArray.length; i++) {
                    addRow(tbl, [
                        {"text": `<a href="/video.html?video=${videoArray[i].NAME}">${videoArray[i].NAME}</a>`},
                        {"text": `<button onclick="removeVideo('${videoArray[i].NAME}', ${videoArray[i].ID})">Remove</button>`}
                    ]);
                }
            }
        }
    }
}

function removeVideo(name, id) {
    showConfirm("Remove?", `Remove ${name}?`, function() {reallyRemoveVideo(id);});
}

async function reallyRemoveVideo(id) {
    let resp = await callEndpoint("GET", `/video/remove?id=${id}`);
    if (resp.ERROR == null) {
        getAllVideos();
    }
    else {
        console.log(resp);
    }
}