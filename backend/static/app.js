document.getElementById('convert-form').addEventListener('submit', async function(e) {
    e.preventDefault();

    const urlInput = document.getElementById('youtube-url');
    const submitBtn = document.getElementById('submit-btn');
    const statusContainer = document.getElementById('status-container');
    const errorContainer = document.getElementById('error-container');
    const errorText = document.getElementById('error-text');

    const videoUrl = urlInput.value.trim();

    if (!videoUrl) return;

    // Reset UI state
    submitBtn.disabled = true;
    urlInput.disabled = true;
    errorContainer.classList.add('hidden');
    statusContainer.classList.remove('hidden');

    try {
        const response = await fetch('/api/convert', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: videoUrl })
        });

        if (!response.ok) {
            let errorMsg = 'Error al convertir el video. Verifica la URL y vuelve a intentarlo.';
            try {
                const errorData = await response.json();
                if (errorData.error) errorMsg = errorData.error;
            } catch (jsonErr) {} // Si no es JSON, usa el error por defecto
            throw new Error(errorMsg);
        }

        // Obtener nombre del archivo del header Content-Disposition si existe
        let filename = 'audio.mp3';
        const contentDisposition = response.headers.get('Content-Disposition');
        if (contentDisposition && contentDisposition.includes('filename=')) {
            const matches = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/.exec(contentDisposition);
            if (matches != null && matches[1]) {
                filename = matches[1].replace(/['"]/g, '');
            }
        }

        const blob = await response.blob();

        // Crear enlace temporal para descargar
        const downloadUrl = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = downloadUrl;
        a.download = filename;
        document.body.appendChild(a);
        a.click();

        // Limpiar
        window.URL.revokeObjectURL(downloadUrl);
        document.body.removeChild(a);

        // Reset input for another download
        urlInput.value = '';

    } catch (error) {
        errorText.textContent = error.message;
        errorContainer.classList.remove('hidden');
    } finally {
        // Restaurar UI state
        submitBtn.disabled = false;
        urlInput.disabled = false;
        statusContainer.classList.add('hidden');
    }
});
