class MemoryVideoCreator {
    constructor() {
        this.selectedPhotos = [];
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        const photoInput = document.getElementById('photoInput');
        const uploadArea = document.getElementById('uploadArea');
        const processBtn = document.getElementById('processBtn');
        const clearBtn = document.getElementById('clearBtn');
        const downloadBtn = document.getElementById('downloadBtn');
        const createAnotherBtn = document.getElementById('createAnotherBtn');

        // File input change event
        photoInput.addEventListener('change', (e) => this.handleFileSelect(e));

        // Drag and drop events
        uploadArea.addEventListener('dragover', (e) => this.handleDragOver(e));
        uploadArea.addEventListener('dragleave', (e) => this.handleDragLeave(e));
        uploadArea.addEventListener('drop', (e) => this.handleDrop(e));

        // Button events
        processBtn.addEventListener('click', () => this.processPhotos());
        clearBtn.addEventListener('click', () => this.clearPhotos());
        downloadBtn.addEventListener('click', () => this.downloadVideo());
        createAnotherBtn.addEventListener('click', () => this.resetApp());
    }

    handleFileSelect(event) {
        const files = Array.from(event.target.files);
        this.addPhotos(files);
    }

    handleDragOver(event) {
        event.preventDefault();
        event.currentTarget.classList.add('dragover');
    }

    handleDragLeave(event) {
        event.currentTarget.classList.remove('dragover');
    }

    handleDrop(event) {
        event.preventDefault();
        event.currentTarget.classList.remove('dragover');
        
        const files = Array.from(event.dataTransfer.files);
        const imageFiles = files.filter(file => file.type.startsWith('image/'));
        this.addPhotos(imageFiles);
    }

    addPhotos(files) {
        files.forEach(file => {
            if (file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    this.selectedPhotos.push({
                        file: file,
                        preview: e.target.result,
                        id: Date.now() + Math.random()
                    });
                    this.updatePhotoPreview();
                };
                reader.readAsDataURL(file);
            }
        });
    }

    updatePhotoPreview() {
        const photoPreview = document.getElementById('photoPreview');
        const photoGrid = document.getElementById('photoGrid');
        
        if (this.selectedPhotos.length > 0) {
            photoPreview.style.display = 'block';
            photoGrid.innerHTML = '';
            
            this.selectedPhotos.forEach(photo => {
                const photoItem = document.createElement('div');
                photoItem.className = 'photo-item';
                photoItem.innerHTML = `
                    <img src="${photo.preview}" alt="Preview">
                    <button class="remove-btn" onclick="app.removePhoto('${photo.id}')">
                        <i class="fas fa-times"></i>
                    </button>
                `;
                photoGrid.appendChild(photoItem);
            });
        } else {
            photoPreview.style.display = 'none';
        }
    }

    removePhoto(photoId) {
        this.selectedPhotos = this.selectedPhotos.filter(photo => photo.id !== photoId);
        this.updatePhotoPreview();
    }

    clearPhotos() {
        this.selectedPhotos = [];
        this.updatePhotoPreview();
        document.getElementById('photoInput').value = '';
    }

    async processPhotos() {
        if (this.selectedPhotos.length === 0) {
            alert('Please select some photos first!');
            return;
        }

        this.showProcessingSection();
        
        try {
            // Create FormData for file upload
            const formData = new FormData();
            this.selectedPhotos.forEach(photo => {
                formData.append('photos', photo.file);
            });

            // Upload photos and get context
            const uploadResponse = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            if (!uploadResponse.ok) {
                throw new Error('Upload failed');
            }

            const uploadData = await uploadResponse.json();
            this.updateProgress(50, 'Generating context...');

            // Generate video
            const videoResponse = await fetch('/generate_video', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    photo_paths: uploadData.photo_paths,
                    context: uploadData.context,
                    video_plan: uploadData.video_plan
                })
            });

            if (!videoResponse.ok) {
                throw new Error('Video generation failed');
            }

            const videoData = await videoResponse.json();
            this.updateProgress(100, 'Video created successfully!');

            // Show results
            setTimeout(() => {
                this.showResults(uploadData.context, videoData.download_url);
            }, 1000);

        } catch (error) {
            console.error('Error processing photos:', error);
            alert('Error processing photos: ' + error.message);
            this.resetApp();
        }
    }

    showProcessingSection() {
        document.getElementById('uploadSection').style.display = 'none';
        document.getElementById('resultsSection').style.display = 'none';
        document.getElementById('processingSection').style.display = 'block';
    }

    updateProgress(percentage, status) {
        const progressFill = document.getElementById('progressFill');
        const statusText = document.getElementById('processingStatus');
        
        progressFill.style.width = percentage + '%';
        statusText.textContent = status;
    }

    showResults(context, downloadUrl) {
        document.getElementById('processingSection').style.display = 'none';
        document.getElementById('resultsSection').style.display = 'block';
        
        // Display context
        const contextText = document.getElementById('contextText');
        contextText.textContent = context.overall_context || 'Context generated successfully!';
        
        // Store download URL
        this.downloadUrl = downloadUrl;
    }

    downloadVideo() {
        if (this.downloadUrl) {
            window.open(this.downloadUrl, '_blank');
        }
    }

    resetApp() {
        this.selectedPhotos = [];
        this.downloadUrl = null;
        
        document.getElementById('uploadSection').style.display = 'block';
        document.getElementById('processingSection').style.display = 'none';
        document.getElementById('resultsSection').style.display = 'none';
        
        this.updatePhotoPreview();
        document.getElementById('photoInput').value = '';
    }
}

// Initialize the app when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.app = new MemoryVideoCreator();
});



