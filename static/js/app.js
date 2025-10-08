// Compact File Browser JS
const form = document.getElementById('uploadForm');
const fileInput = document.getElementById('fileInput');
const uploadBtn = document.getElementById('uploadBtn');
const selectedFile = document.getElementById('selectedFile');
const selectedFileName = document.getElementById('selectedFileName');
const progressContainer = document.getElementById('progressContainer');
const progressBar = document.getElementById('progressBar');
const progressLabel = document.getElementById('progressLabel');
const progressPercent = document.getElementById('progressPercent');
const progressTime = document.getElementById('progressTime');
const deleteModal = document.getElementById('deleteModal');
const deleteText = document.getElementById('deleteText');

let uploadStart = null;
let deleteTarget = null;

// File selection
fileInput.onchange = () => {
  const files = fileInput.files;
  if (!files.length) return;
  
  let size = 0;
  for (let f of files) size += f.size;
  
  selectedFileName.textContent = files.length === 1 
    ? `${files[0].name} (${formatBytes(size)})`
    : `${files.length} files (${formatBytes(size)})`;
  selectedFile.classList.add('show');
};

removeFile.onclick = () => {
  fileInput.value = '';
  selectedFile.classList.remove('show');
};

// Upload
form.onsubmit = e => {
  e.preventDefault();
  const files = fileInput.files;
  if (!files.length) return;

  const max = 15 * 1024 * 1024 * 1024;
  for (let f of files) {
    if (f.size > max) {
      alert(`❌ "${f.name}" is too large! Max 15GB`);
      return;
    }
  }

  const formData = new FormData(form);
  progressContainer.classList.add('active');
  uploadBtn.disabled = true;
  fileInput.disabled = true;
  uploadStart = Date.now();

  const xhr = new XMLHttpRequest();

  xhr.upload.onprogress = e => {
    if (!e.lengthComputable) return;
    
    const pct = Math.round((e.loaded / e.total) * 100);
    progressBar.style.width = pct + '%';
    progressPercent.textContent = pct + '%';
    
    progressLabel.textContent = files.length === 1
      ? `${files[0].name} - ${formatBytes(e.loaded)}/${formatBytes(e.total)}`
      : `${files.length} files - ${formatBytes(e.loaded)}/${formatBytes(e.total)}`;
    
    const elapsed = (Date.now() - uploadStart) / 1000;
    if (elapsed > 1) {
      const timeLeft = (e.total - e.loaded) / (e.loaded / elapsed);
      progressTime.textContent = formatTime(timeLeft) + ' left';
    }
  };

  xhr.onload = () => {
    if (xhr.status === 200 || xhr.status === 302) {
      progressLabel.textContent = '✓ Complete!';
      progressBar.style.width = '100%';
      progressPercent.textContent = '100%';
      progressTime.textContent = 'Done!';
      setTimeout(() => location.reload(), 800);
    } else {
      alert('❌ Upload failed: ' + xhr.statusText);
      resetForm();
    }
  };

  xhr.onerror = () => {
    alert('❌ Upload failed');
    resetForm();
  };

  xhr.open('POST', '/upload');
  xhr.send(formData);
};

// Delete
function confirmDelete(path, isFolder) {
  deleteTarget = path;
  const name = path.split('/').pop();
  deleteText.textContent = isFolder
    ? `Delete folder "${name}" and all contents?`
    : `Delete "${name}"?`;
  deleteModal.classList.add('show');
}

function closeModal() {
  deleteModal.classList.remove('show');
  deleteTarget = null;
}

function executeDelete() {
  if (!deleteTarget) return;
  fetch('/delete/' + encodeURIComponent(deleteTarget), { method: 'POST' })
    .then(r => r.json())
    .then(d => d.success ? location.reload() : alert('❌ ' + d.error))
    .catch(() => alert('❌ Delete failed'));
  closeModal();
}

// Utils
function formatBytes(b) {
  if (!b) return '0 B';
  const k = 1024, s = ['B','KB','MB','GB'];
  const i = Math.floor(Math.log(b) / Math.log(k));
  return (b / Math.pow(k, i)).toFixed(1) + ' ' + s[i];
}

function formatTime(s) {
  if (s < 60) return Math.round(s) + 's';
  if (s < 3600) return `${Math.floor(s/60)}m ${Math.round(s%60)}s`;
  return `${Math.floor(s/3600)}h ${Math.floor((s%3600)/60)}m`;
}

function resetForm() {
  progressContainer.classList.remove('active');
  uploadBtn.disabled = false;
  fileInput.disabled = false;
  fileInput.value = '';
  selectedFile.classList.remove('show');
  progressBar.style.width = '0';
  progressPercent.textContent = '0%';
  progressTime.textContent = 'Calculating...';
}
