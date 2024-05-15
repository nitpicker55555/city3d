document.addEventListener("DOMContentLoaded", () => {
    const timeDisplay = document.getElementById("time-display");
    const timeSlider = document.getElementById("time-slider");
    const datePicker = document.getElementById("date-picker");
    const resetButton = document.getElementById("reset-button");

    const updateTime = () => {
        let minutes = timeSlider.value * 10;
        let hours = Math.floor(minutes / 60);
        minutes = minutes % 60;
        let minutesFormatted = minutes === 0 ? '00' : minutes.toString().padStart(2, '0');
        timeDisplay.textContent = `${hours.toString().padStart(2, '0')}:${minutesFormatted}`;

    };
    const resetTime = () => {
        const now = new Date();
        datePicker.value = now.toISOString().split('T')[0];
        const hours = now.getHours();
        const minutes = now.getMinutes();
        const totalMinutes = hours * 60 + minutes;
        timeSlider.value = Math.round(totalMinutes / 10);
        updateTime();
    };
    document.getElementById('mode-button').addEventListener('click', function() {
        this.classList.toggle('blue');
    });
    resetTime();
    timeSlider.addEventListener("input", updateTime);
    resetButton.addEventListener("click", resetTime);
});
