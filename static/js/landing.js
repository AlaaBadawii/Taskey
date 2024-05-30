document.addEventListener('DOMContentLoaded', (event) => {
    const video = document.getElementById('myVideo');

    // Function to play video when in view and reset when out of view
    const handleIntersection = (entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                video.play().catch(error => {
                    console.log('Video play was prevented:', error);
                });
            } else {
                video.pause();
                video.currentTime = 0; // Reset the video to the beginning
            }
        });
    };

    // Create intersection observer
    const observer = new IntersectionObserver(handleIntersection, {
        threshold: 0.5 // Adjust this value as needed
    });

    // Start observing the video element
    observer.observe(video);
});