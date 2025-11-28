const form = document.getElementById('uploadForm');
const fileInput = document.getElementById('fileInput');
const progress = document.getElementById('progressContainer');
const bar = document.getElementById('progressBar');
const pctLabel = document.getElementById('progressPercent');
const nameLabel = document.getElementById('progressLabel');
const timeLabel = document.getElementById('progressTime');

let startTime = 0;

fileInput.onchange = () => fileInput.files.length && uploadFiles();
form.onsubmit = (e) => e.preventDefault();

async function uploadFiles() {
  const files = [...fileInput.files];
  const total = files.reduce((sum, f) => sum + f.size, 0);

  const check = await fetch('/storage-check', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ size: total })
  }).then(r => r.json()).catch(() => ({ available: false }));

  if (!check.available) {
    alert('Upload failed - Storage full');
    fileInput.value = '';
    return;
  }

  startTime = Date.now();
  progress.classList.add('show');
  fileInput.disabled = true;

  let uploaded = 0;

  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    const current_path = form.querySelector('[name="current_path"]').value;
    if (!await uploadSingle(file, current_path, uploaded, total, i + 1, files.length)) {
      reset();
      return;
    }
    uploaded += file.size;
  }

  bar.style.width = pctLabel.textContent = '100%';
  nameLabel.textContent = 'Complete!';
  setTimeout(() => location.reload(), 500);
}

function uploadSingle(file, current_path, uploaded, total, num, count) {
  return new Promise(resolve => {
    const xhr = new XMLHttpRequest();

    xhr.upload.onprogress = (e) => {
      if (!e.lengthComputable) return;
      const pct = Math.round((uploaded + e.loaded) / total * 100);
      bar.style.width = pctLabel.textContent = pct + '%';
      nameLabel.textContent = count === 1 ? file.name : `${num}/${count}: ${file.name}`;
      
      const elapsed = (Date.now() - startTime) / 1000;
      if (elapsed > 1) {
        const speed = (uploaded + e.loaded) / elapsed;
        timeLabel.textContent = formatTime((total - uploaded - e.loaded) / speed) + ' left';
      }
    };

    xhr.onload = () => {
      if (xhr.status === 200) { resolve(true); return; }
      let err = xhr.status;
      try { err = JSON.parse(xhr.responseText).error || err; } catch {}
      alert(`Upload failed - ${err}`);
      resolve(false);
    };

    xhr.onerror = () => { alert('Upload failed - Network error'); resolve(false); };

    xhr.open('POST', '/upload');
    xhr.setRequestHeader('X-Filename', file.name);
    xhr.setRequestHeader('X-Upload-Path', current_path);
    xhr.send(file);
  });
}

function deleteFileAction(e, path, name) {
  e.stopPropagation();
  if (!confirm(`Delete "${name}"?`)) return;
  
  fetch(`/delete/${encodeURIComponent(path)}`, { method: 'POST' })
    .then(r => r.json())
    .then(data => { if (!data.success) alert('Delete failed'); })
    .catch(() => alert('Delete failed'))
    .finally(() => location.reload());
}

function formatTime(s) {
  return s < 60 ? Math.round(s) + 's' :
         s < 3600 ? Math.floor(s / 60) + 'm ' + Math.round(s % 60) + 's' :
         Math.floor(s / 3600) + 'h ' + Math.floor((s % 3600) / 60) + 'm';
}

function reset() {
  progress.classList.remove('show');
  fileInput.disabled = false;
  fileInput.value = '';
  bar.style.width = '0';
  pctLabel.textContent = '0%';
  nameLabel.textContent = '';
  timeLabel.textContent = '';
}