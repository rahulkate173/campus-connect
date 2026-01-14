document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const previewSection = document.getElementById('previewSection');
    const previewBody = document.getElementById('previewBody');

    // Trigger file browser on click
    dropZone.addEventListener('click', () => fileInput.click());

    // Drag and Drop Effects
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('drag-over');
    });

    dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag-over'));

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('drag-over');
        handleFiles(e.dataTransfer.files[0]);
    });

    fileInput.addEventListener('change', (e) => handleFiles(e.target.files[0]));

    function handleFiles(file) {
        if (!file) return;
        
        // Simulating parsing a CSV/Excel file
        const mockParsedData = [
            { prn: '72014562G', name: 'John Student', sgpa: '8.94', status: 'PASS' },
            { prn: '72014563H', name: 'Sara Khan', sgpa: '7.21', status: 'PASS' },
            { prn: '72014564J', name: 'Mike Ross', sgpa: '4.50', status: 'FAIL' }
        ];

        renderPreview(mockParsedData);
    }

    function renderPreview(data) {
        previewBody.innerHTML = data.map(row => `
            <tr>
                <td>${row.prn}</td>
                <td><strong>${row.name}</strong></td>
                <td>${row.sgpa}</td>
                <td style="color: ${row.status === 'PASS' ? '#059669' : '#dc2626'}; font-weight:700;">${row.status}</td>
                <td><button style="border:none; background:none; color:#94a3b8; cursor:pointer;"><i class="fas fa-times"></i></button></td>
            </tr>
        `).join('');

        previewSection.style.display = 'block';
        document.getElementById('recordCount').innerText = `${data.length} Records Detected`;
    }

    document.getElementById('clearBtn').addEventListener('click', () => {
        previewSection.style.display = 'none';
        fileInput.value = '';
    });
});