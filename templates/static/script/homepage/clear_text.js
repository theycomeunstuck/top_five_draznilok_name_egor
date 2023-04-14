let clearButton = document.getElementById("clear-button");
let area = document.querySelector(".area");

clearButton.addEventListener("click", function() {
  area.innerHTML = "";
  clearTable();
});

function clearTable() {
  fetch('/clear-table', {method: 'POST'})
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error(error));
}
