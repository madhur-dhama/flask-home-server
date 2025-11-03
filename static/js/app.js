// Simple File Browser JS
const form = document.getElementById('uploadForm');
const fileInput = document.getElementById('fileInput');
const progressContainer = document.getElementById('progressContainer');
const progressBar = document.getElementById('progressBar');
const progressLabel = document.getElementById('progressLabel');
const progressPercent = document.getElementById('progressPercent');
const progressTime = document.getElementById('progressTime');

let uploadStart = null;

// Auto-upload on file selection
fileInput.onchange = () => {
  if (fileInput.files.length) uploadFiles();
};

// Upload function
function uploadFiles() {
  const files = fileInput.files;
  if (!files.length) return;

  const formData = new FormData(form);
  progressContainer.classList.add('show');
  fileInput.disabled = true;
  uploadStart = Date.now();

  const xhr = new XMLHttpRequest();

  xhr.upload.onprogress = e => {
    if (!e.lengthComputable) return;
    
    const pct = Math.round((e.loaded / e.total) * 100);
    progressBar.style.width = pct + '%';
    progressPercent.textContent = pct + '%';
    progressLabel.textContent = files.length === 1 ? files[0].name : `${files.length} files`;
    
    const elapsed = (Date.now() - uploadStart) / 1000;
    if (elapsed > 1) {
      const speed = e.loaded / elapsed;
      const timeLeft = (e.total - e.loaded) / speed;
      progressTime.textContent = formatTime(timeLeft) + ' left';
    }
  };

  xhr.onload = () => {
    if (xhr.status === 200) {
      progressLabel.textContent = '✓ Complete!';
      progressBar.style.width = '100%';
      progressPercent.textContent = '100%';
      progressTime.textContent = 'Done!';
      setTimeout(() => location.reload(), 800);
    } else if (xhr.status === 507) {
      // Storage full - only error we show to user
      alert('❌ Storage full');
      resetForm();
    } else {
      // Other errors - just reset, check server logs
      resetForm();
    }
  };

  xhr.onerror = () => resetForm();

  xhr.open('POST', '/upload');
  xhr.send(formData);
}

// Prevent manual form submission
form.onsubmit = e => e.preventDefault();

// Delete file
function deleteFile(filepath, filename) {
  if (!confirm(`Delete "${filename}"?\n\nThis cannot be undone.`)) return;
  
  fetch('/delete/' + filepath, { method: 'POST' })
    .finally(() => location.reload());  // Always reload, errors logged on server
}

// Utils
function formatTime(s) {
  if (s < 60) return Math.round(s) + 's';
  if (s < 3600) return `${Math.floor(s/60)}m ${Math.round(s%60)}s`;
  return `${Math.floor(s/3600)}h ${Math.floor((s%3600)/60)}m`;
}

function resetForm() {
  progressContainer.classList.remove('show');
  fileInput.disabled = false;
  fileInput.value = '';
  progressBar.style.width = '0';
  progressPercent.textContent = '0%';
  progressTime.textContent = 'Calculating...';
}