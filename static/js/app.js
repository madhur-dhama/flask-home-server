const form = document.getElementById('uploadForm');
const fileInput = document.getElementById('fileInput');
const progressContainer = document.getElementById('progressContainer');
const progressBar = document.getElementById('progressBar');
const progressLabel = document.getElementById('progressLabel');
const progressPercent = document.getElementById('progressPercent');
const progressTime = document.getElementById('progressTime');
let uploadStart = null;

fileInput.onchange = () => {
  if (fileInput.files.length) uploadFiles();
};
form.onsubmit = e => e.preventDefault();

// UPLOAD FUNCTIONS
async function uploadFiles() {
  const files = Array.from(fileInput.files);
  if (!files.length) return;

  const totalSize = files.reduce((sum, f) => sum + f.size, 0);

  // Storage Check
  const res = await fetch('/storage-check', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ size: totalSize })
  }).then(r => r.json()).catch(() => ({ available: false }));

  if (!res.available) {
    alert('Not enough storage space!');
    fileInput.value = '';
    return;
  }

  // Initialize Progress UI
  progressContainer.classList.add('show');
  fileInput.disabled = true;
  uploadStart = Date.now();

  let uploadedSize = 0;

  // Sequential Upload
  for (let i = 0; i < files.length; i++) {
    const formData = new FormData();
    formData.append('files', files[i]);
    formData.append('current_path', form.querySelector('[name="current_path"]').value);

    const success = await uploadFile(formData, files[i], uploadedSize, totalSize, i + 1, files.length);
    if (!success) break;
    uploadedSize += files[i].size;
  }

  // Completion
  progressLabel.textContent = 'Complete!';
  progressBar.style.width = '100%';
  progressPercent.textContent = '100%';
  progressTime.textContent = 'Done!';
  setTimeout(() => location.reload(), 800);
}

// Upload single file with progress tracking
function uploadFile(formData, file, uploaded, total, num, count) {
  return new Promise(resolve => {
    const xhr = new XMLHttpRequest();

    // Progress Tracking
    xhr.upload.onprogress = e => {
      if (!e.lengthComputable) return;

      const pct = Math.round(((uploaded + e.loaded) / total) * 100);
      progressBar.style.width = pct + '%';
      progressPercent.textContent = pct + '%';
      progressLabel.textContent = count === 1 ? file.name : `${num}/${count}: ${file.name}`;

      // Calculate and display time remaining
      const elapsed = (Date.now() - uploadStart) / 1000;
      if (elapsed > 1) {
        const speed = (uploaded + e.loaded) / elapsed;
        const remaining = (total - uploaded - e.loaded) / speed;
        progressTime.textContent = formatTime(remaining) + ' left';
      }
    };

    // Success Handler
    xhr.onload = () => {
      if (xhr.status === 200) {
        resolve(true);
      } else {
        if (xhr.status === 507) alert('Storage full');
        resetForm();
        resolve(false);
      }
    };

    // Error Handler
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

// Format seconds to readable time
function formatTime(s) {
  if (s < 60) return Math.round(s) + 's';
  if (s < 3600) return Math.floor(s / 60) + 'm ' + Math.round(s % 60) + 's';
  return Math.floor(s / 3600) + 'h ' + Math.floor((s % 3600) / 60) + 'm';
}

// Reset form
function resetForm() {
  progressContainer.classList.remove('show');
  fileInput.disabled = false;
  fileInput.value = '';
  progressBar.style.width = '0';
  progressPercent.textContent = '0%';
  progressTime.textContent = '';
}