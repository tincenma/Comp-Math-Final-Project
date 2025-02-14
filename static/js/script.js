// Loading the first task at the beginning by default
loadTask('task1')

function loadTask(task) {
    // This function returns html data for the tasks
    fetch(`tasks/${task}.html`)
        .then(response => response.text())
        .then(html => {
            document.getElementById("content").innerHTML = html;  // here it's updating content section in index.html
        })
        .catch(error => console.error("Error loading task:", error));
}