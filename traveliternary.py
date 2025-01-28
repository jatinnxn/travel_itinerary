import openai
import streamlit as st

# Set your OpenAI API Key
openai.api_key = "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"

# Step 1: System Prompt for Context
SYSTEM_PROMPT = """
You are an intelligent travel assistant. Your role is to help users create personalized travel itineraries. 
Follow these steps:
1. Ask relevant follow-up questions to gather detailed user input.
2. Refine user inputs to address missing or unclear details.
3. Generate a structured, day-by-day travel itinerary.
Include:
- Attractions and activities aligned with preferences.
- Dining options and local experiences.
- Suggested accommodations and travel tips.
"""

# Step 2: Function to Refine Inputs
def refine_inputs(user_responses):
    questions = """
    Based on the user's inputs, generate clarifying questions for:
    - Location
    - Duration
    - Budget
    - Interests (e.g., adventure, relaxation, food, culture)
    - Accommodation preferences (luxury, budget, etc.)
    - Any specific requirements (e.g., dietary restrictions, accessibility).
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_responses},
            {"role": "assistant", "content": questions},
        ],
    )
    return response["choices"][0]["message"]["content"]

# Step 3: Function to Generate Itinerary
def generate_itinerary(location, duration, budget, interests, accommodation, additional_notes):
    itinerary_prompt = f"""
    Create a travel itinerary for:
    - Location: {location}
    - Duration: {duration} days
    - Budget: {budget}
    - Interests: {interests}
    - Accommodation Preferences: {accommodation}
    - Additional Notes: {additional_notes}

    Provide a detailed day-by-day itinerary with:
    - Morning, afternoon, and evening activities.
    - Dining recommendations.
    - Suggestions for accommodation.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": itinerary_prompt},
        ],
    )
    return response["choices"][0]["message"]["content"]

# Step 4: Streamlit UI for User Interaction
st.title("🌍 Travel Itinerary Generator ✈️")
st.write("Let me help you plan the perfect trip! Answer a few questions to get started.")

# Collect initial user inputs
with st.form("Travel Planner"):
    location = st.text_input("Where are you planning to travel?", placeholder="E.g., Paris, Bali, Tokyo")
    duration = st.slider("How many days will your trip last?", min_value=1, max_value=30, value=5)
    budget = st.selectbox("What's your budget?", ["Low", "Moderate", "High"])
    interests = st.text_area("What are your interests? (E.g., culture, adventure, relaxation, food)")
    accommodation = st.selectbox("Preferred accommodation type:", ["Luxury", "Budget", "Mid-range", "Unique stays"])
    additional_notes = st.text_area("Any specific requirements or preferences?", placeholder="E.g., dietary restrictions, mobility concerns")
    submitted = st.form_submit_button("Generate Itinerary")

if submitted:
    if location and duration and budget and interests and accommodation:
        with st.spinner("Planning your trip..."):
            # Step 5: Refine Inputs (if needed)
            user_input_summary = f"""
            Location: {location}
            Duration: {duration} days
            Budget: {budget}
            Interests: {interests}
            Accommodation: {accommodation}
            Additional Notes: {additional_notes}
            """
            clarifications = refine_inputs(user_input_summary)
            st.write("### 🔎 Clarification Questions:")
            st.write(clarifications)

            # Step 6: Generate Itinerary
            itinerary = generate_itinerary(location, duration, budget, interests, accommodation, additional_notes)
            st.write("### 📝 Your Personalized Itinerary:")
            st.write(itinerary)
    else:
        st.warning("Please fill out all fields to generate your itinerary!")