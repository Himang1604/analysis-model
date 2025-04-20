from typing import Dict, List, Any
import random

class RecommendationAgent:
    def __init__(self):
        """Initialize the recommendation agent with predefined templates and rules."""
        # Define recommendation templates
        self.recommendation_templates = {
            'low': [
                "Based on your symptoms, it seems like a {condition}. Try {recommendation}",
                "Your symptoms suggest {condition}. Consider {recommendation}",
                "It appears you might have {condition}. {recommendation}"
            ],
            'medium': [
                "Given your symptoms, you might have {condition}. {recommendation}",
                "Your symptoms indicate {condition}. Please {recommendation}",
                "Based on the analysis, {condition} is possible. {recommendation}"
            ],
            'high': [
                "Your symptoms suggest {condition}. {recommendation}",
                "Based on the analysis, {condition} is likely. {recommendation}",
                "Your symptoms indicate {condition}. {recommendation}"
            ]
        }
        
        # Define motivational messages
        self.motivational_messages = [
            "Remember to take care of yourself and get plenty of rest.",
            "Your health is important - make sure to follow the recommendations.",
            "Stay positive and focus on your recovery.",
            "Small steps towards better health make a big difference.",
            "You've got this! Take it one day at a time."
        ]
        
        # Define general health tips
        self.health_tips = [
            "Stay hydrated by drinking plenty of water.",
            "Get adequate sleep to help your body recover.",
            "Maintain a balanced diet with plenty of fruits and vegetables.",
            "Practice stress-reduction techniques like deep breathing.",
            "Stay active with light exercise when possible."
        ]
    
    def generate_recommendations(self, conditions: Dict[str, Any], risk_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate health recommendations based on conditions and risk analysis.
        
        Args:
            conditions: Dictionary containing condition information
            risk_analysis: Dictionary containing risk analysis results
            
        Returns:
            Dictionary containing recommendations and motivational messages
        """
        if not conditions['conditions']:
            return {
                'recommendations': [],
                'motivational_message': random.choice(self.motivational_messages),
                'health_tips': random.sample(self.health_tips, 2)
            }
        
        # Get the main condition and its details
        main_condition = conditions['conditions'][0]
        condition_details = conditions.get('details', {})
        
        # Generate specific recommendations
        specific_recommendations = self._generate_specific_recommendations(
            main_condition,
            condition_details,
            risk_analysis['risk_level']
        )
        
        # Generate motivational message
        motivational_message = self._generate_motivational_message(
            risk_analysis['risk_level']
        )
        
        # Select relevant health tips
        health_tips = self._select_health_tips(main_condition)
        
        return {
            'specific_recommendations': specific_recommendations,
            'motivational_message': motivational_message,
            'health_tips': health_tips,
            'risk_level': risk_analysis['risk_level']
        }
    
    def _generate_specific_recommendations(self, condition: str, details: Dict[str, Any], risk_level: str) -> List[str]:
        """Generate specific recommendations based on condition and risk level."""
        template = random.choice(self.recommendation_templates[risk_level])
        recommendations = []
        
        if details:
            recommendation = template.format(
                condition=condition,
                recommendation=details.get('recommendations', 'consult a healthcare provider')
            )
            recommendations.append(recommendation)
        
        return recommendations
    
    def _generate_motivational_message(self, risk_level: str) -> str:
        """Generate an appropriate motivational message based on risk level."""
        if risk_level == 'high':
            return "Please take your symptoms seriously and seek medical attention. " + random.choice(self.motivational_messages)
        elif risk_level == 'medium':
            return "Monitor your symptoms closely and consider consulting a healthcare provider. " + random.choice(self.motivational_messages)
        else:
            return random.choice(self.motivational_messages)
    
    def _select_health_tips(self, condition: str) -> List[str]:
        """Select relevant health tips based on the condition."""
        # This would typically use a more sophisticated selection process
        return random.sample(self.health_tips, 2) 