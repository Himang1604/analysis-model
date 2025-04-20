document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const symptomsInput = document.getElementById('symptoms-input');
    const analyzeBtn = document.getElementById('analyze-btn');
    const initialResults = document.getElementById('initial-results');
    const followUp = document.getElementById('follow-up');
    const finalResults = document.getElementById('final-results');
    const finalAnalysisBtn = document.getElementById('final-analysis-btn');
    const newAnalysisBtn = document.getElementById('new-analysis-btn');

    // State
    let currentAnalysis = null;
    let selectedFollowUpSymptoms = [];

    // Event Listeners
    analyzeBtn.addEventListener('click', handleInitialAnalysis);
    finalAnalysisBtn.addEventListener('click', handleFinalAnalysis);
    newAnalysisBtn.addEventListener('click', resetAnalysis);

    // Handle initial analysis
    async function handleInitialAnalysis() {
        const symptoms = symptomsInput.value.trim();
        if (!symptoms) {
            alert('Please enter your symptoms');
            return;
        }

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ symptoms }),
            });

            const data = await response.json();
            if (data.status === 'success') {
                currentAnalysis = data.analysis;
                displayInitialResults(data.analysis);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while analyzing symptoms');
        }
    }

    // Display initial results
    function displayInitialResults(analysis) {
        // Display detected symptoms
        const detectedSymptomsDiv = document.getElementById('detected-symptoms');
        detectedSymptomsDiv.innerHTML = analysis.detected_symptoms
            .map(symptom => `<span class="symptom-tag">${symptom}</span>`)
            .join('');

        // Display potential conditions
        const potentialConditionsDiv = document.getElementById('potential-conditions');
        potentialConditionsDiv.innerHTML = Object.entries(analysis.potential_conditions)
            .map(([condition, score]) => `
                <div class="condition-tag">
                    ${condition} (${(score * 100).toFixed(1)}%)
                </div>
            `)
            .join('');

        // Display follow-up questions
        const followUpQuestionsDiv = document.getElementById('follow-up-questions');
        followUpQuestionsDiv.innerHTML = analysis.follow_up_questions
            .map((question, index) => `
                <div class="question-item" data-index="${index}">
                    <input type="checkbox" id="question-${index}">
                    <label for="question-${index}">${question}</label>
                </div>
            `)
            .join('');

        // Add event listeners to follow-up questions
        document.querySelectorAll('.question-item').forEach(item => {
            item.addEventListener('click', () => {
                const checkbox = item.querySelector('input[type="checkbox"]');
                checkbox.checked = !checkbox.checked;
                updateSelectedSymptoms();
            });
        });

        // Show results and follow-up sections
        initialResults.classList.remove('hidden');
        followUp.classList.remove('hidden');
    }

    // Update selected follow-up symptoms
    function updateSelectedSymptoms() {
        selectedFollowUpSymptoms = Array.from(document.querySelectorAll('.question-item input:checked'))
            .map(checkbox => {
                const index = checkbox.id.split('-')[1];
                return currentAnalysis.follow_up_questions[index];
            });
    }

    // Handle final analysis
    async function handleFinalAnalysis() {
        if (selectedFollowUpSymptoms.length === 0) {
            alert('Please select at least one follow-up symptom');
            return;
        }

        try {
            const response = await fetch('/final_analysis', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    initial_symptoms: currentAnalysis.detected_symptoms,
                    follow_up_symptoms: selectedFollowUpSymptoms,
                }),
            });

            const data = await response.json();
            if (data.status === 'success') {
                displayFinalResults(data.analysis);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while performing final analysis');
        }
    }

    // Display final results
    function displayFinalResults(analysis) {
        // Display all symptoms
        const allSymptomsDiv = document.getElementById('all-symptoms');
        allSymptomsDiv.innerHTML = [...analysis.detected_symptoms, ...selectedFollowUpSymptoms]
            .map(symptom => `<span class="symptom-tag">${symptom}</span>`)
            .join('');

        // Display detailed condition information
        const finalConditionsDiv = document.getElementById('final-conditions');
        finalConditionsDiv.innerHTML = Object.entries(analysis.potential_conditions)
            .map(([condition, score]) => {
                const details = analysis.condition_details[condition] || {};
                return `
                    <div class="condition-card">
                        <h4>${condition.toUpperCase()} (${(score * 100).toFixed(1)}% Risk)</h4>
                        <p><strong>Description:</strong> ${details.description || 'No description available'}</p>
                        <p><strong>Common Causes:</strong> ${(details.common_causes || []).join(', ')}</p>
                        <p><strong>Risk Factors:</strong> ${(details.risk_factors || []).join(', ')}</p>
                        <p><strong>Severity:</strong> ${details.severity || 'Unknown'}</p>
                    </div>
                `;
            })
            .join('');

        // Show final results
        finalResults.classList.remove('hidden');
        followUp.classList.add('hidden');
    }

    // Reset analysis
    function resetAnalysis() {
        symptomsInput.value = '';
        currentAnalysis = null;
        selectedFollowUpSymptoms = [];
        
        // Hide all result sections
        initialResults.classList.add('hidden');
        followUp.classList.add('hidden');
        finalResults.classList.add('hidden');
    }
}); 