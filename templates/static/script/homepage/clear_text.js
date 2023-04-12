document.addEventListener('DOMContentLoaded', function() {
  const clearButton = document.getElementById('clear-button');
  clearButton.addEventListener('click', function(event) {
    event.preventDefault();
    fetch('/clear-table')
      .then(response => response.text())
      .then(text => {
        const textArea = document.getElementById('text-area');
        textArea.value = '';
      })
      .catch(error => console.log(error));
  });
});