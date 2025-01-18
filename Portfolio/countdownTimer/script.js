// Get references to the HTML elements where we'll display the countdown
let daysSpan = document.querySelector('.day-display-scripted');
let hoursSpan = document.querySelector('.hours-display-scripted');
let minutesSpan = document.querySelector('.minutes-display-scripted');
let secondsSpan = document.querySelector('.seconds-display-scripted');

// Initialize countdownDate to null. This will hold the timestamp of the date we're counting down to.
let countdownDate = null;

// Get a reference to the input box where the user will enter the date
let inputBox = document.getElementById('inputTime'); 

// Add an event listener to the input box that updates countdownDate whenever the user changes the input
inputBox.addEventListener('change', function() {
    // Convert the user's input to a timestamp and store it in countdownDate
    countdownDate = new Date(inputBox.value).getTime();
});

// Set an interval that updates the countdown every second
let x = setInterval(function() {
    // If the user has entered a date, calculate and display the countdown
    if (countdownDate) {
        // Get the current date and time as a timestamp
        let now = new Date().getTime();

        // Calculate the difference between the countdown date and the current date
        let distance = countdownDate - now;

        // Calculate the remaining days, hours, minutes, and seconds
        let days = Math.floor(distance / (1000 * 60 * 60 * 24));
        let hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        let minutes = Math.floor((distance % (1000 * 60 * 60 )) / (1000 * 60));
        let seconds = Math.floor((distance % (1000 * 60 )) / 1000);

        // Display the remaining time in the HTML elements
        daysSpan.innerHTML = days;
        hoursSpan.innerHTML = hours;
        minutesSpan.innerHTML = minutes;
        secondsSpan.innerHTML = seconds;

        // If the countdown is finished, clear the interval and display a message
        if (distance < 0) {
            clearInterval(x);
            document.querySelector('.countdownTimer-display').innerHTML = "Happy New Year!";
        }
    } else {
        // If the user hasn't entered a date, display '00' for the days, hours, minutes, and seconds
        daysSpan.innerHTML = '00';
        hoursSpan.innerHTML = '00';
        minutesSpan.innerHTML = '00';
        secondsSpan.innerHTML = '00';
    }
}, 1000);