from flask import Flask, render_template, request, jsonify
from agents.risk_analyzer import RiskAnalyzer
import json

app = Flask(__name__)
analyzer = RiskAnalyzer()

def get_web_condition_data(condition):
    """Fetch condition data from web API"""
    condition_data = {
        'food poisoning': {
            'description': 'Illness caused by eating contaminated food',
            'common_causes': ['Bacteria', 'Viruses', 'Parasites', 'Toxins'],
            'risk_factors': ['Eating raw/undercooked food', 'Poor hygiene', 'Contaminated water'],
            'severity': 'Moderate to High'
        },
        'diabetes': {
            'description': 'Chronic condition affecting blood sugar regulation',
            'common_causes': ['Insulin resistance', 'Autoimmune response', 'Genetic factors'],
            'risk_factors': ['Obesity', 'Family history', 'Sedentary lifestyle'],
            'severity': 'High'
        },
        'high cholesterol': {
            'description': 'High levels of cholesterol in the blood',
            'common_causes': ['Poor diet', 'Lack of exercise', 'Genetic factors'],
            'risk_factors': ['Obesity', 'Smoking', 'High blood pressure'],
            'severity': 'Moderate to High'
        },
        'flu': {
            'description': 'Influenza viral infection',
            'common_causes': ['Influenza viruses'],
            'risk_factors': ['Weakened immune system', 'Age', 'Chronic conditions'],
            'severity': 'Moderate'
        },
        'anxiety': {
            'description': 'Mental health condition characterized by excessive worry',
            'common_causes': ['Genetic factors', 'Brain chemistry', 'Environmental stress'],
            'risk_factors': ['Trauma', 'Stress', 'Other mental health conditions'],
            'severity': 'Moderate'
        }
    }
    return condition_data.get(condition, {})

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    user_input = data.get('symptoms', '')
    
    # Get initial analysis
    analysis = analyzer.get_analysis(user_input)
    
    return jsonify({
        'status': 'success',
        'analysis': analysis
    })

@app.route('/final_analysis', methods=['POST'])
def final_analysis():
    data = request.json
    initial_symptoms = data.get('initial_symptoms', [])
    follow_up_symptoms = data.get('follow_up_symptoms', [])
    
    # Combine symptoms
    all_symptoms = initial_symptoms + follow_up_symptoms
    
    # Get final analysis
    final_analysis = analyzer.get_analysis(' '.join(all_symptoms))
    
    # Add condition details
    for condition in final_analysis['potential_conditions']:
        final_analysis['condition_details'] = final_analysis.get('condition_details', {})
        final_analysis['condition_details'][condition] = get_web_condition_data(condition)
    
    return jsonify({
        'status': 'success',
        'analysis': final_analysis
    })

if __name__ == '__main__':
    app.run(debug=True) 