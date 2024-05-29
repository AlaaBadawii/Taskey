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