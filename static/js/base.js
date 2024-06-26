// Get the current date
const currentDate = new Date();
// Get the day number
const dayNumber = currentDate.getDate();
// Update the text of the span element with the day number
document.getElementById('current-date').textContent = dayNumber;


/**
 * Toggles the display style of the menu.
 * If the menu is currently displayed, it will be hidden.
 * If the menu is currently hidden, it will be displayed.
 */
function toggleMenu() {
    let menu = document.getElementById('menu');
    if (menu.style.display === 'none' || menu.style.display === '') {
        menu.style.display = 'flex';
    } else {
        menu.style.display = 'none';
    }
}

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
