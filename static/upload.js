function uploadFiles() {
    const files = document.getElementById('file-input').files;
    const progressContainer = document.getElementById('progress-container');
    progressContainer.innerHTML = ''; // Clear previous progress bars

    Array.from(files).forEach(file => {
        const formData = new FormData();
        formData.append('files', file);

        const xhr = new XMLHttpRequest();
        xhr.open('POST','/gallery', true);

        const progressBar = document.createElement('div');
        progressBar.className = 'progress-bar';
        progressBar.innerHTML = `<div class="progress-bar-inner">0%</div>`;
        progressContainer.appendChild(progressBar);

        xhr.upload.onprogress = function (event) {
            if (event.lengthComputable) {
                const percentComplete = (event.loaded / event.total) * 100;
                const innerBar = progressBar.querySelector('.progress-bar-inner');
                innerBar.style.width = percentComplete + '%';
                innerBar.innerText = Math.round(percentComplete) + '%';
            }
        };

        xhr.onload = function () {
            if (xhr.status === 200) {
                alert('Upload complete!');
            } else {
                alert('Upload failed!');
            }
        };

        xhr.send(formData);
    });
}
function mountPendrive() {
    fetch('/mount_pendrive', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
        })
        .catch(error => {
            alert('Error mounting pendrive.');
        });
}

function copySelectedFiles() {
    const selectedFiles = Array.from(document.querySelectorAll('input[name="files"]:checked')).map(input => input.value);
    if (selectedFiles.length === 0) {
        alert('No files selected for copying.');
        return;
    }

    document.getElementById('wait-message').style.display = 'block';

    fetch('/copy_to_pendrive', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ files: selectedFiles })
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('wait-message').style.display = 'none';
            alert(data.message);
        })
        .catch(error => {
            document.getElementById('wait-message').style.display = 'none';
            alert('Error copying files to pendrive.');
        });
}
