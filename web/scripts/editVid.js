
async function editVideo(butt) {
    let textArea = document.getElementById("editArea");

    if (textArea.style.visibility == "hidden") {
        textArea.style.visibility = "visible";
        butt.innerHTML = "Save";

        textArea.value = `{
    "NAME": "${video.NAME}",
    "SHOW_NAME": "${video.SHOW_NAME}",
    "SERIES": "${video.SERIES}",
    "EPISODE": ${video.EPISODE},
    "DESCRIPTION": "${video.DESCRIPTION}"
}`;
    }
    else {
        textArea.style.visibility = "hidden";
        butt.innerHTML = "Edit";

        data = JSON.parse(textArea.value);
        data.ID = video.ID;
        let resp = await callEndpoint("POST", "/video/update", data);
        if (resp.ERROR == null) {
            getVideoInfo();
        }
        else {
            console.log(resp);
        }
    }
}