//Get a refrence to the container element
const contentContainer = document.getElementById("content-container");

//Function to fetch and inject content
function fetchAndInjectContent(filepath) {
    fetch(filepath)
    .then((response) => response.text())
    .then((htmlContent) =>{
        const contentDiv = document.createElement("div");
        contentDiv.innerHTML = htmlContent;
        contentContainer.appendChild(contentDiv);
    })
    .catch((error) => {
        console.error("Error fetching or injecting content:", error);
    });
}

//Fetch the json file containing file paths
fetch("../../article_path.json")
    .then((response) => response.json())
    .then((data) => {
        const htmlFiles = data.files;

        //Loop through the list of file paths and fetch content
        htmlFiles.forEach((filepath) =>{
            fetchAndInjectContent(filepath);
        })
    })
    .catch((error) => {
        console.error("Error fetchinig JSON file:", error)
    });
