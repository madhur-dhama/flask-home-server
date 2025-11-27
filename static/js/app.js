const form = document.getElementById('uploadForm');
const fileInput = document.getElementById('fileInput');
const progress = document.getElementById('progressContainer');
const bar = document.getElementById('progressBar');
const pctLabel = document.getElementById('progressPercent');
const nameLabel = document.getElementById('progressLabel');
const timeLabel = document.getElementById('progressTime');

let startTime = 0;

fileInput.onchange = () => fileInput.files.length && uploadFiles();
form.onsubmit = e => e.preventDefault();

// Main upload process
async function uploadFiles() {
  const files = [...fileInput.files];
  const total = files.reduce((s, f) => s + f.size, 0);

  // Check if server has space
  const check = await fetch('/storage-check', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ size: total })
  }).then(r => r.json()).catch(() => ({ available: false }));

  if (!check.available) {
    alert('Not enough storage');
    fileInput.value = '';
    return;
  }

  // Show progress UI and disable file input
  startTime = Date.now();
  progress.classList.add('show');
  fileInput.disabled = true;

  let uploaded = 0;

  // Upload each file one by one
  for (let i = 0; i < files.length; i++) {
    const fd = new FormData();
    fd.append('files', files[i]);
    fd.append('current_path', form.querySelector('[name="current_path"]').value);

    const ok = await uploadSingle(fd, files[i], uploaded, total, i + 1, files.length);
    if (!ok) {
      reset();
      return;
    }
    uploaded += files[i].size;
  }

  // All files done - show completion
  bar.style.width = '100%';
  pctLabel.textContent = '100%';
  nameLabel.textContent = 'Complete!';
  timeLabel.textContent = 'Done!';
  setTimeout(() => location.reload(), 500);
}

// Upload one file and track progress
function uploadSingle(fd, file, uploaded, total, num, count) {
  return new Promise(res => {
    const xhr = new XMLHttpRequest();

    // Update progress bar while uploading
    xhr.upload.onprogress = e => {
      if (!e.lengthComputable) return;
      const pct = Math.round((uploaded + e.loaded) / total * 100);

      bar.style.width = pct + '%';
      pctLabel.textContent = pct + '%';
      nameLabel.textContent = count === 1 ? file.name : `${num}/${count}: ${file.name}`;

      // Calculate time remaining
      const elapsed = (Date.now() - startTime) / 1000;
      if (elapsed > 1) {
        const speed = (uploaded + e.loaded) / elapsed;
        const left = (total - uploaded - e.loaded) / speed;
        timeLabel.textContent = formatTime(left) + ' left';
      }
    };

    xhr.onload = () => res(xhr.status === 200);
    xhr.onerror = () => res(false);

    xhr.open('POST', '/upload');
    xhr.send(fd);
  });
}

// Delete file
function deleteFile(path, name) {
  if (!confirm(`Delete "${name}"?`)) return;
  fetch('/delete/' + path, { method: 'POST' }).finally(() => location.reload());
}

// Convert seconds to readable format (45s, 2m 30s, 1h 15m)
function formatTime(s) {
  if (s < 60) return Math.round(s) + 's';
  if (s < 3600) return Math.floor(s / 60) + 'm ' + Math.round(s % 60) + 's';
  return Math.floor(s / 3600) + 'h ' + Math.floor((s % 3600) / 60) + 'm';
}

// Clear progress UI after error or cancel
function reset() {
  progress.classList.remove('show');
  fileInput.disabled = false;
  fileInput.value = '';
  bar.style.width = '0';
  pctLabel.textContent = '0%';
  timeLabel.textContent = '';
}