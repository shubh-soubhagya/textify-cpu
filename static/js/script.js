const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const imagePreview = document.getElementById('imagePreview');
const textOutput = document.getElementById('textOutput');
const loading = document.querySelector('.loading');

uploadArea.addEventListener('click', () => fileInput.click());
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = '#4299e1';
    uploadArea.style.backgroundColor = '#ebf8ff';
});

uploadArea.addEventListener('dragleave', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = '#cbd5e0';
    uploadArea.style.backgroundColor = 'white';
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    loading.style.display = 'block';

    const file = e.dataTransfer.files[0];
    handleFile(file);
});

fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    handleFile(file);
});

function handleFile(file) {
    if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = function(e) {
            imagePreview.src = e.target.result;
            imagePreview.style.display = 'block';
            uploadArea.style.display = 'none';
            processImage(file);
        }
        reader.readAsDataURL(file);
    }
}

async function processImage(file) {
    // loading.style.display = 'block';
    const formData = new FormData();
    formData.append('image', file);

    try {
        const response = await fetch('/', {
            method: 'POST',
            body: formData
        });
        const text = await response.text();
        textOutput.textContent = text;
    } catch (error) {
        console.error('Error:', error);
        textOutput.textContent = 'Error processing image. Please try again.';
    } finally {
        loading.style.display = 'none';
    }
}

function copyText() {
    const text = textOutput.textContent;
    navigator.clipboard.writeText(text);
    const notification = document.getElementById('copyNotification');
    notification.style.display = 'block';
    setTimeout(() => {
        notification.style.display = 'none';
    }, 2000);
}

async function downloadText() {
    const format = document.getElementById('formatSelect').value;
    const text = textOutput.textContent;

    const formData = new FormData();
    formData.append('text', text);
    formData.append('format', format);

    try {
        const response = await fetch('/download', {
            method: 'POST',
            body: formData
        });
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `extracted_text.${format}`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    } catch (error) {
        console.error('Error:', error);
    }
}