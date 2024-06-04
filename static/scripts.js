document.getElementById("showButtonsBtn").addEventListener("click", function() {
    var additionalButtons = document.getElementById("additionalButtons");
    additionalButtons.classList.toggle("hidden");
  });
  
document.addEventListener("contextmenu", (event) => {
         event.preventDefault();
      });
  
  function captureImage() {
    fetch('/capture')
        .then(response => {
            if (response.ok) {
                return response.text();
            }
            throw new Error('Network response was not ok.');
        })
        .then(data => {
            alert(data); // Display the message in a popup
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function captureVideo() {
            fetch('/video_record')
                .then(response => {
                    if (response.ok) {
                        return response.text();
                    }
                    throw new Error('Network response was not ok.');
                })
                .then(data => {
                    alert(data); // Display the message in a popup
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }
function stopVideo() {
            fetch('/stop_record')
                .then(response => {
                    if (response.ok) {
                        return response.text();
                    }
                    throw new Error('Network response was not ok.');
                })
                .then(data => {
                    alert(data); // Display the message in a popup
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }
function sendCommand(endpoint) {
            const steps = document.getElementById('steps').value;
            fetch(`${endpoint}?steps=${steps}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.text();
                })
                .then(data => {
                    alert(data);
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert(`Failed to send command: ${error}`);
                });
        }

 async function calibrate(magnification) 
 {
            const response = await fetch(`/calibrate?magnification=${magnification}`, {
                method: 'POST'
            });
            const result = await response.json();
            document.getElementById('x-coord').innerText = result.x;
            document.getElementById('y-coord').innerText = result.y;
            document.getElementById('z-coord').innerText = result.z;
        }

        async function initialize() {
            const response = await fetch(`/initialize`, {
                method: 'POST'
            });
            const result = await response.json();
            document.getElementById('x-coord').innerText = result.x;
            document.getElementById('y-coord').innerText = result.y;
            document.getElementById('z-coord').innerText = result.z;
        }

async function move(axis, direction) 
{
            const steps = document.getElementById(`steps`).value;
            const response = await fetch(`/move?axis=${axis}&direction=${direction}&steps=${steps}`, {
                method: 'POST'
            });
            const result = await response.json();
            document.getElementById('x-coord').innerText = result.x;
            document.getElementById('y-coord').innerText = result.y;
            document.getElementById('z-coord').innerText = result.z;
        }

