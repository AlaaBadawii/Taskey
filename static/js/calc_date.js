// Get the current date
var currentDate = new Date();

// Get the day number
var dayNumber = currentDate.getDate();

// Update the text of the span element with the day number
document.getElementById('current-date').textContent = dayNumber;