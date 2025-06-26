document.addEventListener('DOMContentLoaded', function() {
    // === LOCATION SELECTOR ===
    const locationSelector = document.getElementById("locationSelector");
    const cityCoords = {
        "new-york": { lat: 40.7128, lon: -74.0060 },
        "nagpur": { lat: 21.1458, lon: 79.0882 },
        "mumbai": { lat: 19.0760, lon: 72.8777 },
        "delhi": { lat: 28.6139, lon: 77.2090 },
        "london": { lat: 51.5074, lon: -0.1278 }
    };

    // === REAL-TIME CLOCK ===
    function updateClock() {
        const now = new Date();
        const options = { month: 'long', day: 'numeric', year: 'numeric' };
        const timeOptions = { hour: 'numeric', minute: 'numeric' };
        document.getElementById('current-date').textContent =
            now.toLocaleDateString('en-US', options) + ' • ' +
            now.toLocaleTimeString('en-US', timeOptions);
    }
    updateClock();
    setInterval(updateClock, 60000);

    // === TAB NAVIGATION ===
    const tabs = document.querySelectorAll('.tab');
    const tabContents = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const target = tab.getAttribute('data-tab');
            tabs.forEach(t => t.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            tab.classList.add('active');
            document.getElementById(target).classList.add('active');
        });
    });

    // === QUIZ ===
    const quizOptions = document.querySelectorAll('.quiz-option');
    quizOptions.forEach(option => {
        option.addEventListener('click', function () {
            const parent = this.parentElement;
            parent.querySelectorAll('.quiz-option').forEach(opt => {
                opt.classList.remove('selected');
            });
            this.classList.add('selected');
        });
    });
    document.getElementById('submit-quiz').addEventListener('click', function () {
        const selectedOptions = document.querySelectorAll('.quiz-option.selected');
        if (selectedOptions.length < 3) {
            alert('Please answer all questions before submitting.');
            return;
        }
        let quizScore = 0;
        selectedOptions.forEach(option => {
            quizScore += parseInt(option.getAttribute('data-points'));
        });
        let skinType, skinDescription, skinColor;
        if (quizScore >= 10) {
            skinType = "I"; skinDescription = "Very fair skin, always burns, never tans"; skinColor = "from-pink-200 to-pink-100";
        } else if (quizScore >= 7) {
            skinType = "II"; skinDescription = "Fair skin, burns easily, tans minimally"; skinColor = "from-pink-300 to-pink-100";
        } else if (quizScore >= 5) {
            skinType = "III"; skinDescription = "Medium skin, sometimes burns, gradually tans"; skinColor = "from-yellow-600 to-yellow-400";
        } else if (quizScore >= 3) {
            skinType = "IV"; skinDescription = "Olive skin, rarely burns, tans easily"; skinColor = "from-yellow-800 to-yellow-600";
        } else if (quizScore >= 1) {
            skinType = "V"; skinDescription = "Brown skin, very rarely burns, tans darkly"; skinColor = "from-brown-600 to-brown-400";
        } else {
            skinType = "VI"; skinDescription = "Dark brown or black skin, never burns"; skinColor = "from-gray-900 to-gray-800";
        }
        document.getElementById('quiz-container').classList.add('hidden');
        document.getElementById('quiz-results').classList.remove('hidden');
        const resultCircle = document.querySelector('#quiz-results .rounded-full');
        resultCircle.textContent = skinType;
        resultCircle.className = `w-16 h-16 rounded-full bg-gradient-to-r ${skinColor} mr-4 flex items-center justify-center text-2xl font-bold`;
        document.querySelector('#quiz-results .text-xl').textContent = `Skin Type ${skinType}`;
        document.querySelector('#quiz-results .text-xl + p').textContent = skinDescription;
    });
    document.getElementById('retake-quiz').addEventListener('click', function () {
        document.getElementById('quiz-results').classList.add('hidden');
        document.getElementById('quiz-container').classList.remove('hidden');
        document.querySelectorAll('.quiz-option').forEach(opt => opt.classList.remove('selected'));
    });

    // === REMINDER ===
    document.getElementById('set-reminder').addEventListener('click', function () {
        const firstApp = document.getElementById('first-application').value;
        const interval = document.getElementById('reminder-interval').value;
        const endTime = document.getElementById('end-time').value;
        if (!firstApp || !endTime) {
            alert('Please set both first application time and end time.');
            return;
        }
        document.getElementById('no-reminders').classList.add('hidden');
        document.getElementById('active-reminders').classList.remove('hidden');
        const now = new Date();
        const hours = now.getHours();
        const minutes = now.getMinutes();
        let nextHour = hours + 2;
        if (nextHour > 23) nextHour = 23;
        document.querySelector('#active-reminders .text-sm span').textContent =
            `${nextHour}:${minutes < 10 ? '0' + minutes : minutes}`;
        alert('Reminder set successfully!');
    });

    // === UV FETCH (OpenUV) ===
    locationSelector.addEventListener('change', function () {
        fetchUVForCity(this.value);
    });
    fetchUVForCity(locationSelector.value);  // Initial fetch
    async function fetchUVForCity(city) {
        const { lat, lon } = cityCoords[city];
        try {
            const res = await fetch(`https://api.openuv.io/api/v1/uv?lat=${lat}&lng=${lon}`, {
                headers: { "x-access-token": API_KEY }
            });
            const data = await res.json();
            const uv = data.result.uv;
            const uv_max = data.result.uv_max;
            updateUVDisplay(uv);
            updateChart(simulateForecast(uv, uv_max));
        } catch (err) {
            console.error("OpenUV API error:", err);
        }
    }
    function updateUVDisplay(uv) {
        let uvCategory = "Low", uvPosition = "10%";
        if (uv >= 11) {
            uvCategory = "Extreme"; uvPosition = "95%";
        } else if (uv >= 8) {
            uvCategory = "Very High"; uvPosition = "80%";
        } else if (uv >= 6) {
            uvCategory = "High"; uvPosition = "60%";
        } else if (uv >= 3) {
            uvCategory = "Moderate"; uvPosition = "40%";
        }
        document.getElementById('uv-value').textContent = uv.toFixed(1);
        document.getElementById('uv-category').textContent = uvCategory;
        document.getElementById('uv-indicator').style.left = uvPosition;
    }

    // === DASHBOARD CHART ===
    let uvChart;
    function updateChart(forecast) {
        const labels = forecast.map((f, i) => {
            const date = new Date(f.uv_time);
            return `${date.getHours()}:00`;
        });
        const values = forecast.map(f => f.uv);
        const ctx = document.getElementById("uvChart").getContext("2d");
        if (uvChart) uvChart.destroy();
        uvChart = new Chart(ctx, {
            type: "bar",
            data: {
                labels,
                datasets: [{
                    label: "UV Index Forecast",
                    data: values,
                    backgroundColor: values.map(val =>
                        val < 3 ? "#3EC70B" :
                        val < 6 ? "#FFD24C" :
                        val < 8 ? "#F29F05" :
                        "#F24C3D"
                    )
                }]
            },
            options: {
                scales: {
                    y: { beginAtZero: true, max: 12 }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }
    function simulateForecast(currentUV, maxUV) {
        const forecast = [];
        const now = new Date();
        for (let i = 0; i < 12; i++) {
            const uvSim = Math.max(0, maxUV * Math.sin(Math.PI * (i / 11)));
            forecast.push({ uv_time: new Date(now.getTime() + i * 3600000).toISOString(), uv: uvSim });
        }
        return forecast;
    }
});