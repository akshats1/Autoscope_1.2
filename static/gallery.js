/*function clicked_img(img) {
    console.log(img.src);

    var top = document.getElementById('top');
    top.src = img.src;
    top.hidden = false;

    if (img.naturalWidth < screen.width * 0.6 && img.naturalHeight < screen.height * 0.6) {
        top.width = img.naturalWidth;
        top.height = img.naturalHeight;
    } else {
        top.width = screen.width * 0.6;
        top.height = img.naturalHeight / img.naturalWidth * top.width;
    }

    document.getElementById('close').hidden = false;
}

function do_close() {
    document.getElementById('top').hidden = true;
    document.getElementById('close').hidden = true;
}

function uploadSelectedFiles() {
    const form = document.getElementById('gallery-form');
    const formData = new FormData(form);

    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/', true);

    xhr.onload = function () {
        if (xhr.status === 200) {
            const results = JSON.parse(xhr.responseText);
            const resultContainer = document.getElementById('upload-results');
            resultContainer.innerHTML = results.join('<br>');
        } else {
            alert('Upload failed!');
        }
    };

    xhr.send(formData);
}*/




function clicked_img(img) {
    console.log(img.src);

    var top = document.getElementById('top');
    top.src = img.src;
    top.hidden = false;

    if (img.naturalWidth < screen.width * 0.6 && img.naturalHeight < screen.height * 0.6) {
        top.width = img.naturalWidth;
        top.height = img.naturalHeight;
    } else {
        top.width = screen.width * 0.6;
        top.height = img.naturalHeight / img.naturalWidth * top.width;
    }

    document.getElementById('close').hidden = false;
}

function do_close() {
    document.getElementById('top').hidden = true;
    document.getElementById('close').hidden = true;
}

function uploadSelectedFiles() {
    const form = document.getElementById('gallery-form');
    const formData = new FormData(form);

    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/gallery', true);

    const waitMessage = document.getElementById('wait-message');
    const resultContainer = document.getElementById('upload-results');

    waitMessage.style.display = 'block';
    resultContainer.innerHTML = '';

    xhr.onload = function () {
        waitMessage.style.display = 'none';
        if (xhr.status === 200) {
            const results = JSON.parse(xhr.responseText);
            resultContainer.innerHTML = results.join('<br>');
        } else {
            resultContainer.innerHTML = 'Upload failed!';
        }
    };

    xhr.send(formData);
}


function deleteSelectedFiles() {
            const form = document.getElementById('gallery-form');
            const formData = new FormData(form);
            fetch('/delete', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                alert(data.join('\\n'));
                location.reload();
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }









