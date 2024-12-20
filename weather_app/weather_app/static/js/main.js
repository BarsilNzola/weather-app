document.addEventListener("DOMContentLoaded", () => {
    console.log("Weather App Loaded");

    // Smooth Scroll for internal links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Weather Report Modal
    const reportButtons = document.querySelectorAll('.report-weather');
    reportButtons.forEach(button => {
        button.addEventListener('click', () => {
            const location = prompt("Enter your location for the weather report:");
            const report = prompt("Describe the weather (e.g., hailstorm, flooding):");
            if (location && report) {
                alert(`Thank you for reporting the weather in ${location}: "${report}".`);
                // In production, send this data to the backend for community sharing
            }
        });
    });

    // Temperature Unit Toggle (Celsius/Fahrenheit)
    const toggleTempButtons = document.querySelectorAll('.toggle-temp');
    toggleTempButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tempElement = document.querySelector('#temperature');
            const currentTemp = parseFloat(tempElement.dataset.temp);
            const isCelsius = tempElement.dataset.unit === 'C';
            let newTemp;

            if (isCelsius) {
                newTemp = (currentTemp * 9/5) + 32; // Convert to Fahrenheit
                tempElement.dataset.unit = 'F';
                button.textContent = 'Switch to Celsius';
            } else {
                newTemp = (currentTemp - 32) * 5/9; // Convert to Celsius
                tempElement.dataset.unit = 'C';
                button.textContent = 'Switch to Fahrenheit';
            }
            tempElement.textContent = `${newTemp.toFixed(1)}° ${tempElement.dataset.unit}`;
        });
    });

    // Animated Weather Icons
    const weatherIcon = document.querySelector('#weather-icon');
    if (weatherIcon) {
        weatherIcon.addEventListener('mouseenter', () => {
            weatherIcon.classList.add('spin-icon');
        });
        weatherIcon.addEventListener('mouseleave', () => {
            weatherIcon.classList.remove('spin-icon');
        });
    }

    // Real-Time Weather Map Interaction
    const mapToggle = document.querySelector('#toggle-map');
    if (mapToggle) {
        mapToggle.addEventListener('click', () => {
            const mapContainer = document.querySelector('#weather-map');
            mapContainer.classList.toggle('hidden');
        });
    }

    // Gamification: Badge Animation on Earned
    const badgeElements = document.querySelectorAll('.badge');
    badgeElements.forEach(badge => {
        badge.addEventListener('mouseover', () => {
            badge.classList.add('pulse-badge');
        });
        badge.addEventListener('mouseout', () => {
            badge.classList.remove('pulse-badge');
        });
    });

    // Alerts for Extreme Weather
    const extremeWeatherAlert = document.querySelector('#extreme-weather-alert');
    if (extremeWeatherAlert) {
        const alertType = extremeWeatherAlert.dataset.alertType; // "storm", "heatwave", etc.
        if (alertType) {
            alert(`⚠️ Extreme Weather Alert: ${alertType.toUpperCase()}!`);
        }
    }
});

// Weather Sentiment Analysis (Dummy Data for Prototype)
function fetchWeatherSentiments() {
    const sentiments = [
        { location: "New York", sentiment: "Hot and sunny vibes from social media!" },
        { location: "Seattle", sentiment: "Cloudy skies, but people seem cozy!" },
        { location: "Miami", sentiment: "High energy about the heat!" },
    ];

    const location = document.querySelector('#location').textContent.trim();
    const sentiment = sentiments.find(s => s.location === location)?.sentiment || "No sentiment data available.";
    alert(`Weather Sentiment Analysis for ${location}: ${sentiment}`);
}

// Trigger sentiment analysis on demand
document.querySelector('#location')?.addEventListener('click', fetchWeatherSentiments);

// Basic Weather Chatbot
const chatbotMessages = document.querySelector('#chatbot-messages');
const chatbotInput = document.querySelector('#chatbot-input');
const chatbotSend = document.querySelector('#chatbot-send');

const chatbotResponses = {
    "hello": "Hi! How can I assist you with the weather today?",
    "rain": "It might rain! Make sure to carry an umbrella.",
    "sunny": "It's sunny! A great day for outdoor activities.",
    "cold": "It's chilly. Don't forget to bundle up!",
    "recommendation": "I suggest staying indoors if it's stormy.",
    "bye": "Goodbye! Stay safe!",
};

chatbotSend.addEventListener('click', () => {
    const userMessage = chatbotInput.value.trim().toLowerCase();
    if (userMessage) {
        const botReply = chatbotResponses[userMessage] || "I'm not sure about that. Can you rephrase?";
        chatbotMessages.innerHTML += `<div class="user-message">${userMessage}</div>`;
        chatbotMessages.innerHTML += `<div class="bot-message">${botReply}</div>`;
        chatbotInput.value = '';
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight; // Scroll to the latest message
    }
});
