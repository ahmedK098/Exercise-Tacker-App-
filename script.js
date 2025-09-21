async function uploadVideo() {
    const fileInput = document.getElementById('video-upload');
    const statusMessage = document.getElementById('status-message');
    const file = fileInput.files[0];

    // Check if a file was selected
    if (!file) {
        statusMessage.textContent = "Please select a video file to upload.";
        return;
    }

    // Use FormData to prepare the file for sending
    const formData = new FormData();
    formData.append('video', file);

    statusMessage.textContent = "Uploading video...";

    try {
        // Send the file to the backend server
        const response = await fetch('http://localhost:5000/upload', {
            method: 'POST',
            body: formData,
        });

        // Check if the upload was successful
        if (response.ok) {
            statusMessage.textContent = "True";
        } else {
            statusMessage.textContent = "Upload failed. Please try again.";
        }
    } catch (error) {
        // Handle any network or server errors
        console.error('Error:', error);
        statusMessage.textContent = "An error occurred. Check the console for details.";
    }
}