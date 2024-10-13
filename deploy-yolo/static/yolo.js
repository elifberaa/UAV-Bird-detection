const socket = io.connect('http://127.0.0.1:5500'); // Flask-SocketIO sunucusuna bağlan

let allowUpload = false; // Upload permission control
let tempFile = null; // Temporary file storage


function openCaptchaPopup() {
    document.getElementById("captchaPopup").style.display = "block"; // Open modal
    const iframe = document.getElementById("captchaFrame");
    iframe.contentWindow.startCaptcha();
}

function closePopup() {
    window.parent.postMessage('close_captcha', '*'); // Send message to home page
    document.getElementById("captchaPopup").style.display = "none"; // Close popup
    // Clear content
    document.getElementById('grid').innerHTML = '';
    document.getElementById('confirmButton').style.display = 'none';
    document.getElementById('prompt').innerText = '';

}


// Listen to the CAPTCHA result
window.addEventListener('message', function(event) {
    if (event.data === 'captcha_success') {
        document.getElementById("captchaPopup").style.display = "none"; // Close popup
        allowUpload = true; // Grant upload permission

        // Control of incoming events
        if (isDropEvent) {
            // If there is a drop event, perform the upload
            const reader = new FileReader();
            reader.onload = (e) => {
                uploadImage(tempFile, e.target.result); // Use temporary file
                tempFile = null; // Reset temporary file
            };
            reader.readAsDataURL(tempFile); // read file
        } else {
            // If there is a click event, open gallery
            document.getElementById("imageUpload").click();
        }
    } else if (event.data === 'captcha_fail') {
        document.getElementById("captchaPopup").style.display = "none"; // Close popup
    }


});

//Listen to the close_captcha message
window.addEventListener('message', function(event) {
    if (event.data === 'close_captcha') {
        document.getElementById("captchaPopup").style.display = "none"; // Close popup
    }
});


// File upload process
function fileUploadInput(event) {
    const output = document.getElementById('dragDropArea');
    const files = event.target.files;

    if (files.length === 0) {
        alert("Bir dosya seçilmedi.");
        return;
    }

    output.innerHTML = "";

    for (const file of files) {
        if (!file.type.startsWith("image/")) {
            alert("Sadece resim dosyalarını seçebilirsiniz.");
            return;
        }

        // Geçici dosyayı sakla
        tempFile = file;
    }
}

// Drag-and-drop işlevselliği
const dragDropArea = document.getElementById("dragDropArea");

// Drag over olayında stil ekleme
dragDropArea.addEventListener("dragover", (e) => {
    e.preventDefault();  
    dragDropArea.classList.add("dragover"); 
});

// Drag leave olayında stil kaldırma
dragDropArea.addEventListener("dragleave", () => {
    dragDropArea.classList.remove("dragover"); 
});

// Drop olayında dosyayı işleme


let isDropEvent = false; // Check if drop event occurred or not

dragDropArea.addEventListener("drop", (e) => {
    e.preventDefault();
    dragDropArea.classList.remove("dragover");
    e.stopPropagation();

    const files = e.dataTransfer.files;
    if (files.length === 0) {
        alert("Bir dosya seçilmedi.");
        return;
    }

    if (files.length > 1) {
        alert("Bir tane resim seçiniz.");
        return;
    }

    // Keep temporary file and open modal
    tempFile = files[0];
    isDropEvent = true; // Drop incident occurred
    openCaptchaPopup(); // Open modal
});

// Tıklama ile yükleme işlemini başlat
dragDropArea.addEventListener("click", () => {
    isDropEvent = false; // Drop olayı olmadığını belirt
    openCaptchaPopup();
});

// Open modal when file input is clicked
dragDropArea.addEventListener("click", () => {
    openCaptchaPopup();
});

// Resmi yükle
function uploadImage(file, imageData) {
    // Socket.IO ile resmi sunucuya gönder
    socket.emit('upload_image', {
        filename: file.name,
        image: imageData  
    });
}

// Sunucudan gelen yanıtı dinle
socket.on('image_processed', (data) => {
    const output = document.getElementById('dragDropArea');
    const resultImage = document.createElement("img");
    resultImage.src = data.url;
    resultImage.style.display = "block";
    output.innerHTML = ""; 
    output.appendChild(resultImage); // İşlenmiş resmi göster

    const processingTimeElement = document.getElementById('processingTime');
    processingTimeElement.innerText = `İşlem süresi: ${data.processing_time.toFixed(2)} saniye`;
});

// Tespit yoksa mesajı göster
socket.on('no_detection', (data) => {
    const detectionMessage = document.getElementById('detectionMessage');
    detectionMessage.innerText = data.message;
});

// Sunucudan gelen hata mesajını göster
socket.on('error', (data) => {
    alert(data.message);
});

// Dosya yükleme inputu değiştiğinde
document.getElementById("imageUpload").addEventListener("change", (event) => {
    if (allowUpload && tempFile) {
        const reader = new FileReader();
        reader.onload = (e) => {
            uploadImage(tempFile, e.target.result); // Geçici dosyayı yükle
            tempFile = null; // Geçici dosyayı sıfırla
        };
        reader.readAsDataURL(tempFile); // Dosyayı okuyup yükle
    }
});
