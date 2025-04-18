import requests
import random
from datetime import datetime

def handle_message(message: str) -> str:
    message = message.lower()
    
    # Basic greeting with campus-specific welcome
    if "hello" in message:
        greetings = [
            "Hello, welcome to the Columbia University Campus Assistant!",
            "Hi there! I'm your Columbia Lion assistant. How can I help you today?",
            "Welcome to Columbia! I'm here to make your campus experience better."
        ]
        return random.choice(greetings)
    
    # Weather command - core functionality
    elif message.startswith("weather"):
        parts = message.split(' ', 1)
        
        if len(parts) < 2 or not parts[1].strip():
            return "Please provide a city name. Example: 'weather New York'"
        
        city_name = parts[1].strip()
        api_key = "549a93ceb620f958377ac8d6eaa2a93a"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
        
        try:
            response = requests.get(url)
            
            if response.status_code == 200:
                weather_data = response.json()
                
                temperature = weather_data['main']['temp']
                weather_description = weather_data['weather'][0]['description']
                humidity = weather_data['main']['humidity']
                wind_speed = weather_data['wind']['speed']
                city = weather_data['name']
                country = weather_data['sys']['country']
                
                return f"Weather in {city}, {country}:\n" \
                       f"🌡️ Temperature: {temperature}°C\n" \
                       f"🌤️ Conditions: {weather_description}\n" \
                       f"💧 Humidity: {humidity}%\n" \
                       f"💨 Wind Speed: {wind_speed} m/s"
            elif response.status_code == 404:
                return f"City '{city_name}' not found. Please check the spelling and try again."
            else:
                return f"Error fetching weather data. Status code: {response.status_code}"
        except Exception as e:
            return f"An error occurred: {str(e)}"
    
    # Campus weather - focused on Columbia University campus
    elif "campus weather" in message:
        # Automatically get weather for Columbia's location
        try:
            api_key = "549a93ceb620f958377ac8d6eaa2a93a"
            # Columbia University coordinates
            url = f"https://api.openweathermap.org/data/2.5/weather?q=New York&appid={api_key}&units=metric"
            
            response = requests.get(url)
            
            if response.status_code == 200:
                weather_data = response.json()
                temperature = weather_data['main']['temp']
                weather_description = weather_data['weather'][0]['description']
                
                # Campus-specific recommendations based on weather
                if temperature < 5:
                    outfit = "Heavy coat, scarf, gloves, and warm boots recommended for crossing campus."
                    study_spot = "Butler Library's warm reading rooms are perfect today."
                elif temperature < 15:
                    outfit = "A jacket or sweater would be good for walking between buildings."
                    study_spot = "Try the cozy cafe at Lerner Hall for studying."
                else:
                    outfit = "Light clothing is fine, maybe bring a light jacket for evening."
                    study_spot = "Great day to study outdoors at the Low Steps or College Walk!"
                
                # Rain or snow specific advice
                if "rain" in weather_description or "drizzle" in weather_description:
                    outfit += " Don't forget your umbrella!"
                    study_spot = "Stay dry in Avery Library or the Northwest Corner Building."
                elif "snow" in weather_description:
                    outfit += " Watch out for slippery paths on College Walk!"
                    
                return f"📍 Columbia Campus Weather Update:\n" \
                       f"🌡️ Current temperature: {temperature}°C\n" \
                       f"🌤️ Conditions: {weather_description}\n\n" \
                       f"👕 Campus Outfit Tip: {outfit}\n" \
                       f"📚 Study Spot Recommendation: {study_spot}"
            else:
                return "Sorry, I couldn't retrieve the current campus weather data."
        except Exception as e:
            return f"An error occurred with campus weather: {str(e)}"
    
    # Campus events with weather consideration
    elif "events" in message or "activities" in message:
        try:
            api_key = "549a93ceb620f958377ac8d6eaa2a93a"
            url = f"https://api.openweathermap.org/data/2.5/weather?q=New York&appid={api_key}&units=metric"
            
            response = requests.get(url)
            
            # Sample campus events - these would ideally be pulled from a real campus API
            indoor_events = [
                "Philosophy Lecture in Hamilton Hall at 3PM",
                "Student Council Meeting in Lerner 5-6:30PM",
                "Jazz Performance at Miller Theatre 7PM",
                "Graduate Research Symposium in Northwest Corner Building 2-5PM",
                "Film Screening at Dodge Hall 8PM"
            ]
            
            outdoor_events = [
                "Ultimate Frisbee on South Lawn 2-4PM",
                "Environmental Club Tree Planting at Morningside Park 12PM",
                "Outdoor Yoga Session on Low Steps 5PM",
                "Campus Tour for Prospective Students 1PM and 3PM",
                "Student Club Fair on College Walk 11AM-2PM"
            ]
            
            if response.status_code == 200:
                weather_data = response.json()
                temperature = weather_data['main']['temp']
                weather_description = weather_data['weather'][0]['description']
                
                # Weather-based event recommendations
                now = datetime.now()
                date_str = now.strftime("%A, %B %d")
                
                response = f"🗓️ Columbia Events for {date_str}:\n\n"
                
                # Logic for recommending indoor vs outdoor events based on weather
                bad_weather = ("rain" in weather_description or 
                              "snow" in weather_description or 
                              "storm" in weather_description or 
                              temperature < 5 or 
                              temperature > 30)
                
                if bad_weather:
                    response += "Given the current weather conditions, these indoor events might be best:\n"
                    for event in random.sample(indoor_events, 3):
                        response += f"• {event}\n"
                    response += "\nOther events (weather advisory):\n"
                    for event in random.sample(outdoor_events, 2):
                        response += f"• {event} (check for weather cancellations)\n"
                else:
                    response += "With today's nice weather, consider these events:\n"
                    for event in random.sample(outdoor_events, 3):
                        response += f"• {event}\n"
                    response += "\nAlso happening indoors:\n"
                    for event in random.sample(indoor_events, 2):
                        response += f"• {event}\n"
                
                return response
            else:
                # Fallback if weather data can't be retrieved
                response = f"🗓️ Columbia Events Today:\n\n"
                response += "Indoor Events:\n"
                for event in random.sample(indoor_events, 3):
                    response += f"• {event}\n"
                response += "\nOutdoor Events:\n"
                for event in random.sample(outdoor_events, 2):
                    response += f"• {event}\n"
                return response
        except Exception as e:
            return f"An error occurred while fetching events: {str(e)}"
    
    # Dining recommendations based on weather
    elif "food" in message or "dining" in message or "eat" in message:
        try:
            api_key = "549a93ceb620f958377ac8d6eaa2a93a"
            url = f"https://api.openweathermap.org/data/2.5/weather?q=New York&appid={api_key}&units=metric"
            
            response = requests.get(url)
            
            # Columbia dining locations
            dining_options = {
                "cold": [
                    "John Jay Dining Hall - Serving hot soups and comfort food today",
                    "JJ's Place - Their warm mac & cheese is perfect for today",
                    "Joe Coffee at Butler Library - Get a hot chocolate while studying",
                    "Faculty House - Warm indoor seating with a view of campus"
                ],
                "warm": [
                    "The Diana Center Café - Great outdoor seating area",
                    "Joe's Coffee kiosk on College Walk - Quick grab-and-go",
                    "Food trucks on Broadway - Variety of options to enjoy outdoors",
                    "Brownie's Café in Avery Hall - Nice spot with outdoor tables"
                ],
                "rainy": [
                    "Ferris Booth Commons - Spacious indoor dining",
                    "Arts and Sciences Café in Schermerhorn Hall - Stay dry between classes",
                    "Café East in Lerner Hall - Comfortable seating to wait out the rain",
                    "Brad's in the Journalism Building - Cozy atmosphere"
                ]
            }
            
            if response.status_code == 200:
                weather_data = response.json()
                temperature = weather_data['main']['temp']
                weather_description = weather_data['weather'][0]['description']
                
                # Select dining recommendations based on weather
                if "rain" in weather_description or "storm" in weather_description:
                    dining_category = "rainy"
                    weather_note = "Since it's raining, here are some places to stay dry while eating:"
                elif temperature < 10:
                    dining_category = "cold"
                    weather_note = "It's chilly out there! Here are some cozy dining options:"
                else:
                    dining_category = "warm"
                    weather_note = "Nice weather today! Consider these dining options:"
                
                response = f"🍽️ Columbia Dining Recommendations\n\n{weather_note}\n\n"
                for option in random.sample(dining_options[dining_category], 3):
                    response += f"• {option}\n"
                return response
            else:
                # Fallback without weather data
                response = "🍽️ Popular Columbia Dining Options Today:\n\n"
                all_options = dining_options["cold"] + dining_options["warm"]
                for option in random.sample(all_options, 4):
                    response += f"• {option}\n"
                return response
        except Exception as e:
            return f"An error occurred with dining recommendations: {str(e)}"
    
    # Study spots recommendation based on weather
    elif "study" in message or "library" in message:
        try:
            api_key = "549a93ceb620f958377ac8d6eaa2a93a"
            url = f"https://api.openweathermap.org/data/2.5/weather?q=New York&appid={api_key}&units=metric"
            
            response = requests.get(url)
            
            # Columbia study locations with occupancy estimates
            study_spots = {
                "indoor": [
                    "Butler Library - 75% full - Quiet study atmosphere",
                    "Science & Engineering Library - 60% full - Outlets at every table",
                    "Law Library - 40% full - Peaceful environment even for non-law students",
                    "Avery Library - 50% full - Great for architecture and design resources",
                    "Lehman Library - 65% full - Social sciences focused"
                ],
                "outdoor": [
                    "Low Steps - Iconic campus spot with great people watching",
                    "Philosophy Lawn - Peaceful green space near Butler Library",
                    "South Lawn - Spacious area for spreading out with books",
                    "Revson Plaza - Elevated area between buildings with tables",
                    "Furnald Lawn - Shaded area with good WiFi coverage"
                ]
            }
            
            if response.status_code == 200:
                weather_data = response.json()
                temperature = weather_data['main']['temp']
                weather_description = weather_data['weather'][0]['description']
                
                response = "📚 Columbia Study Spot Recommendations:\n\n"
                
                # Weather-based recommendations
                bad_weather = ("rain" in weather_description or 
                              "snow" in weather_description or 
                              temperature < 10 or 
                              temperature > 30)
                
                if bad_weather:
                    response += "Given today's weather, here are indoor study spots:\n"
                    for spot in random.sample(study_spots["indoor"], 4):
                        response += f"• {spot}\n"
                else:
                    # Good weather - recommend both
                    response += "Indoor Study Options:\n"
                    for spot in random.sample(study_spots["indoor"], 2):
                        response += f"• {spot}\n"
                    
                    response += "\nWith today's nice weather, also consider these outdoor spots:\n"
                    for spot in random.sample(study_spots["outdoor"], 2):
                        response += f"• {spot}\n"
                
                current_time = datetime.now().hour
                if 21 <= current_time or current_time <= 5:
                    response += "\n⏰ Late Night Study Tip: Butler and NoCo libraries are open 24/7 with your Columbia ID!"
                
                return response
            else:
                # Fallback without weather data
                response = "📚 Popular Columbia Study Spots:\n\n"
                for spot in random.sample(study_spots["indoor"], 3):
                    response += f"• {spot}\n"
                return response
        except Exception as e:
            return f"An error occurred with study recommendations: {str(e)}"
    
    # Help command
    elif "help" in message:
        return "Columbia University Campus Assistant Commands:\n\n" \
               "• 'weather [city]' - Get weather for any city\n" \
               "• 'campus weather' - Get Columbia campus weather with outfit & study recommendations\n" \
               "• 'events' or 'activities' - Get weather-appropriate campus events\n" \
               "• 'food' or 'dining' - Get weather-based dining recommendations\n" \
               "• 'study' or 'library' - Find the best study spots based on current weather\n" \
               "• 'help' - See this list of commands"
               
    # Default response
    else:
        return "I'm sorry, I didn't understand your message. Type 'help' to see what I can do!"

# Optional testing block:
if __name__ == "__main__":
    user_input = input("Enter a message for the agent: ")
    print(handle_message(user_input))
