async function startResearch() {
    const topic = document.getElementById('topicInput').value;
    if (!topic) return;

    // Show loading
    document.getElementById('initialState').style.display = 'none';
    document.getElementById('reportResult').style.display = 'none';
    document.getElementById('loadingState').style.display = 'flex';
    document.getElementById('researchBtn').disabled = true;
    document.getElementById('btnText').innerText = 'Processing...';

    try {
        // Hitting the real Python backend connecting to OpenAI!
        const response = await fetch('/api/research', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topic: topic })
        });

        if (!response.ok) {
            throw new Error(`Server returned status: ${response.status}`);
        }

        const report = await response.json();

        // Update UI with real LangChain data
        document.getElementById('resTopic').innerText = report.topic.toUpperCase();
        document.getElementById('resSummary').innerText = report.summary;
        document.getElementById('resDifficulty').innerText = report.difficulty;
        document.getElementById('resNextSteps').innerText = report.next_steps;

        const kpCont = document.getElementById('resKeyPoints');
        kpCont.innerHTML = report.key_points.map(kp => `<div class="list-item"><i class="fas fa-chevron-right"></i> ${kp}</div>`).join('');

        const ucCont = document.getElementById('resUseCases');
        ucCont.innerHTML = report.use_cases.map(uc => `<div class="list-item"><i class="fas fa-check"></i> ${uc}</div>`).join('');

        // Switch screens
        document.getElementById('loadingState').style.display = 'none';
        document.getElementById('reportResult').style.display = 'block';
        document.getElementById('researchBtn').disabled = false;
        document.getElementById('btnText').innerText = 'Execute Research';

    } catch (error) {
        console.error("Research failed:", error);
        alert("🚨 Backend Connection Failed! Make sure you are running the server and have your OPENAI_API_KEY set.");

        // Reset UI
        document.getElementById('loadingState').style.display = 'none';
        document.getElementById('initialState').style.display = 'flex';
        document.getElementById('researchBtn').disabled = false;
        document.getElementById('btnText').innerText = 'Execute Research';
    }
}
