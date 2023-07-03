// Get the timer input elements
const hoursInput = document.getElementById('hs');
const minutesInput = document.getElementById('mins');
const secondsInput = document.getElementById('secs');

// Get the start and stop links
const startLink = document.getElementById('startLink');
const stopLink = document.getElementById('stopLink');

let timerInterval; // variable to hold the interval ID

// Function to start the timer
function startTimer() {
  // Disable the start link
  startLink.disabled = true;

  // Get the target time in milliseconds
  const targetTime = new Date().getTime() + (parseInt(hoursInput.value) * 3600 + parseInt(minutesInput.value) * 60 + parseInt(secondsInput.value)) * 1000;

  // Update the timer every second
  timerInterval = setInterval(() => {
    // Get the current time in milliseconds
    const currentTime = new Date().getTime();

    // Calculate the remaining time in milliseconds
    const remainingTime = targetTime - currentTime;

    if (remainingTime < 0) {
      // If the remaining time is negative, stop the timer and reset the input values
      stopTimer();
      hoursInput.value = '00';
      minutesInput.value = '00';
      secondsInput.value = '00';
      return;
    }

    // Convert the remaining time to hours, minutes, and seconds
    const remainingHours = Math.floor(remainingTime / (60 * 60 * 1000));
    const remainingMinutes = Math.floor((remainingTime % (60 * 60 * 1000)) / (60 * 1000));
    const remainingSeconds = Math.floor((remainingTime % (60 * 1000)) / 1000);

    // Update the input values with the remaining time
    hoursInput.value = padZero(remainingHours);
    minutesInput.value = padZero(remainingMinutes);
    secondsInput.value = padZero(remainingSeconds);
  }, 1000);
}

// Function to stop the timer
function stopTimer() {
  // Clear the interval and enable the start link
  clearInterval(timerInterval);
  startLink.disabled = false;
}

// Function to pad a number with leading zeros
function padZero(number) {
  if (number < 10) {
    return '0' + number;
  } else {
    return number.toString();
  }
}

// Add event listeners to the links
startLink.addEventListener('click', function(event) {
  event.preventDefault();
  startTimer();
});

stopLink.addEventListener('click', function(event) {
  event.preventDefault();
  stopTimer();
});