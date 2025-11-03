// Simple File Browser JS
const form = document.getElementById('uploadForm');
const fileInput = document.getElementById('fileInput');
const progressContainer = document.getElementById('progressContainer');
const progressBar = document.getElementById('progressBar');
const progressLabel = document.getElementById('progressLabel');
const progressPercent = document.getElementById('progressPercent');

let uploadStart = null;

// Auto-upload on file selection
fileInput.onchange = () => {
  if (fileInput.files.length) uploadFiles();
};

// Upload files
async function uploadFiles() {
  const files = Array.from(fileInput.files);
  if (!files.length) return;

  progressContainer.classList.add('show');
  fileInput.disabled = true;
  uploadStart = Date.now();

  let totalSize = files.reduce((sum, f) => sum + f.size, 0);
  let uploadedSize = 0;

  for (let i = 0; i < files.length; i++) {
    const formData = new FormData();
    formData.append('files', files[i]);
    formData.append('current_path', form.querySelector('[name="current_path"]').value);

    const success = await uploadFile(formData, files[i], uploadedSize, totalSize, i + 1, files.length);
    if (!success) break;
    uploadedSize += files[i].size;
  }

  progressLabel.textContent = 'Complete!';
  progressBar.style.width = '100%';
  progressPercent.textContent = '100%';
  setTimeout(() => location.reload(), 800);
}

// Upload single file
function uploadFile(formData, file, uploaded, total, num, count) {
  return new Promise(resolve => {
    const xhr = new XMLHttpRequest();

    xhr.upload.onprogress = e => {
      if (!e.lengthComputable) return;
      const pct = Math.round(((uploaded + e.loaded) / total) * 100);
      progressBar.style.width = pct + '%';
      progressPercent.textContent = pct + '%';
      progressLabel.textContent = count === 1 ? file.name : `${num}/${count}: ${file.name}`;
    };

    xhr.onload = () => {
      if (xhr.status === 200) {
        resolve(true);
      } else {
        if (xhr.status === 507) alert('Storage full');
        resetForm();
        resolve(false);
      }
    };

    xhr.onerror = () => {
      resetForm();
      resolve(false);
    };

    xhr.open('POST', '/upload');
    xhr.send(formData);
  });
}

// Delete file
function deleteFile(filepath, filename) {
  if (!confirm(`Delete "${filename}"?`)) return;
  fetch('/delete/' + filepath, { method: 'POST' })
    .finally(() => location.reload());
}

// Reset form
function resetForm() {
  progressContainer.classList.remove('show');
  fileInput.disabled = false;
  fileInput.value = '';
  progressBar.style.width = '0';
  progressPercent.textContent = '0%';
}

// Prevent form submission
form.onsubmit = e => e.preventDefault();