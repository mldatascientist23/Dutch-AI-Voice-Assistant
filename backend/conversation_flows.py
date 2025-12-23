import random
from enum import Enum
from typing import Dict, Tuple
from datetime import datetime

class VoiceProfile(str, Enum):
    LIFESTYLE = "lifestyle"
    BUSINESS = "business"

class LifestyleCoachFlow:
    """Friendly & Casual lifestyle coaching check-ins"""
    
    def __init__(self):
        self.conversation_history = []
        self.step = 0
        self.topics = ["stress", "exercise", "sleep", "nutrition", "mood"]
        self.current_topic = None
        
    async def get_greeting(self) -> str:
        greetings = [
            "Hallo! Leuk je te zien. Hoe gaat het vandaag met je?",
            "Hey! Fijn je te spreken. Hoe voel je je vandaag?",
            "Goedemorgen! Ik ben je lifestyle coach. Wat kan ik voor je doen?",
            "Welkom! Ik ben blij je weer te zien. Hoe gaat het?"
        ]
        return random.choice(greetings)
    
    async def get_response(self, user_input: str) -> str:
        """Generate contextual lifestyle coaching response"""
        user_lower = user_input.lower()
        self.conversation_history.append(("user", user_input))
        
        if any(word in user_lower for word in ["stress", "gestrest", "angstig", "zorgen"]):
            self.current_topic = "stress"
            responses = [
                "Dat klinkt lastig. Wat geeft je het meeste stress op dit moment?",
                "Ik snap het. Stress kan echt uitputtend zijn. Kun je me meer vertellen?",
                "Dat begrijp ik. Heb je al iets geprobeerd om dit aan te pakken?",
                "Sorry dat je stress hebt. Wat zou je willen veranderen?"
            ]
            response = random.choice(responses)
        elif any(word in user_lower for word in ["moe", "vermoeid", "uitgeput", "slaperig"]):
            self.current_topic = "sleep"
            responses = [
                "Het klinkt alsof je wat rust nodig hebt. Hoe veel slaap krijg je momenteel?",
                "Vermoeide ben je? Wil je graag wat tips voor beter slapen?",
                "Ik hoor dat je moe bent. Laten we samen aan je slaapschema werken.",
                "Slaperigheid kan veel invloed hebben. Wil je dat bespreken?"
            ]
            response = random.choice(responses)
        elif any(word in user_lower for word in ["goed", "super", "fantastisch", "prima", "prima"]):
            responses = [
                "Dat is geweldig! Waar ben je vandaag trots op?",
                "Echt super om te horen! Wat gaat er goed?",
                "Fijn! Wat is het geheim van je goeie dag?",
                "Prachtig! Ik ben blij voor je!"
            ]
            response = random.choice(responses)
        elif any(word in user_lower for word in ["beweeg", "sport", "gym", "rennen", "yoga", "fitness"]):
            self.current_topic = "exercise"
            responses = [
                "Mooi dat je actief bent! Wat voor beweging doe je graag?",
                "Super! Hoeveel keer per week train je?",
                "Geweldig dat je sport! Hoe voelt dat voor je?",
                "Beweging is goed! Wat hou je het leukst?"
            ]
            response = random.choice(responses)
        else:
            responses = [
                "Dank je dat je dit met me deelt. Wat zou je graag willen veranderen?",
                "Interessant. Hoe lang heb je dit al?",
                "Ik begrijp het. Hoe zou je je voelen als dit beter zou gaan?",
                "Bedankt voor je openheid. Wat kan ik voor je doen?"
            ]
            response = random.choice(responses)
        
        self.conversation_history.append(("assistant", response))
        return response
    
    async def get_closing(self) -> str:
        closings = [
            "Bedankt voor dit gesprek! Je doet het prima. Zullen we volgende week weer praten?",
            "Fijn dat we dit konden bespreken. Hou vol en zorg goed voor jezelf!",
            "Tot ziens! Onthoud: je bent sterker dan je denkt.",
            "Dank je voor je vertrouwen. Tot snel!"
        ]
        return random.choice(closings)

class BusinessCallFlow:
    """Professional & Business-Friendly inbound/outbound service calls"""
    
    def __init__(self):
        self.conversation_history = []
        self.step = 0
        self.customer_name = None
        self.issue_description = None
        
    async def get_greeting(self) -> str:
        greetings = [
            "Goedemorgen, u spreekt met de digitale assistent. Hoe kan ik u van dienst zijn?",
            "Hallo, welkom. Dit is onze automatische assistent. Waarmee kan ik u helpen?",
            "Goed dat u belt. Ik ben hier om u te helpen. Wat is uw vraag?",
            "Hartelijk welkom. Wat kan ik voor u doen vandaag?"
        ]
        return random.choice(greetings)
    
    async def get_response(self, user_input: str) -> str:
        """Generate professional business response"""
        user_lower = user_input.lower()
        self.conversation_history.append(("user", user_input))
        
        if self.step == 0:
            if any(word in user_lower for word in ["mijn naam", "heet", "ben"]):
                self.customer_name = user_input
                self.step = 1
                response = f"Dank u wel. Ik heb opgenoteerd dat u {user_input} bent. Waar kan ik u mee helpen?"
            else:
                response = "Mag ik eerst uw naam vragen alstublieft?"
        elif self.step == 1:
            self.issue_description = user_input
            self.step = 2
            response = f"Dank u voor deze informatie. Ik begrijp dat het gaat om: {user_input}. Wat zou u willen dat wij doen?"
        else:
            if any(word in user_lower for word in ["dank", "bedankt", "fijn", "prima", "goed"]):
                response = "Prima. Wij zullen dit oppakken en u binnenkort contacteren. Bedankt voor het bellen!"
            else:
                response = "Begrepen. Ik zal dit doorgeven aan het juiste team. Nog iets waarmee ik kan helpen?"
        
        self.conversation_history.append(("assistant", response))
        return response
    
    async def get_closing(self) -> str:
        closings = [
            "Dank u voor uw bellen. Wij helpen u snel. Tot ziens!",
            "Bedankt voor uw geduld. Een collega zal u binnenkort contacteren.",
            "Prima, uw zaak is geregistreerd. Wij nemen contact met u op.",
            "Dank u wel. Veel sterkte, en wij spreken snel!"
        ]
        return random.choice(closings)

class ConversationFlowManager:
    """Manager for conversation flows"""
    
    def __init__(self, profile: VoiceProfile = VoiceProfile.LIFESTYLE):
        self.profile = profile
        if profile == VoiceProfile.LIFESTYLE:
            self.flow = LifestyleCoachFlow()
        else:
            self.flow = BusinessCallFlow()
    
    async def start_conversation(self) -> str:
        """Start a new conversation"""
        return await self.flow.get_greeting()
    
    async def respond(self, user_input: str) -> str:
        """Generate response to user input"""
        return await self.flow.get_response(user_input)
    
    async def close_conversation(self) -> str:
        """Close the conversation"""
        return await self.flow.get_closing()
