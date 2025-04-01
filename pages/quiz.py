import streamlit as st
import time
import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
import re

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyAt0D0WxtfNVrGSUwmpnsnIQ8o-g9XiN_o")

# Configure Google Gemini API
try:
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error(f"Error configuring Gemini API: {e}")

# Simplified CSS with minimal styling
def apply_custom_css():
    st.markdown("""
    <style>
        /* Simple styling for text elements */
        h1 {
            color: #1E3A8A;
            font-family: 'Georgia', serif;
            font-weight: 700;
            margin-bottom: 10px;
        }
        
        h2, h3 {
            color: #1E3A8A;
            font-family: 'Georgia', serif;
        }
        
        /* Simple styling for important elements */
        
        .quiz-title {
            font-size: 2.5em;
            font-weight: bold;
            color: #2E86C1;
            text-align: center;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
            margin-bottom: 10px;
        }
        .quiz-subtitle {
            font-size: 2.5em;
            font-weight: bold;
            color: #C0C0C0 ;
            text-align: center;
            font-style: italic;
            margin-bottom: 10px;
        }

        
        /* Timer styling */
        .timer {
            font-size: 24px;
            font-weight: bold;
            color: #DC2626;
            display: inline-block;
        }
        
        /* Answer styling */
        .correct-answer {
            color: #059669;
            font-weight: bold;
        }
        
        .incorrect-answer {
            color: #DC2626;
            font-weight: bold;
        }
        
        .explanation {
            background-color: #F5E6C8; /* A parchment-like warm beige */
            color: #3E2723; /* A deep brown for a classic, old-paper feel */
            padding: 15px;
            border-left: 5px solid #8B5E3C; /* A rich brown, giving an aged scroll effect */
            margin-top: 10px;
            border-radius: 6px;
            font-family: 'Merriweather', serif; /* A historical serif font */
            box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1); /* A subtle shadow for depth */
        }

        
        /* Score display */
        .score-display {
            font-size: 28px;
            font-weight: bold;
            text-align: center;
            margin: 20px 0;
            color: #FFD700;
        }
        
        /* Quote styling */
        .quote {
            font-style: italic;
            color: #4B5563;
            text-align: center;
            margin: 20px 0;
        }
    </style>
    """, unsafe_allow_html=True)

# Improved function to fetch quiz questions from Gemini AI
def fetch_questions(search, quiz_level):
    # Debug information
    st.session_state.debug_info = {}
    
    # Create a more specific model instance with proper settings
    generation_config = {
        "temperature": 0.2,  # Lower temperature for more deterministic output
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,  # Ensure we get a complete response
    }
    
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ]
    
    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash-latest",
            generation_config=generation_config,
            safety_settings=safety_settings
        )
    except Exception as e:
        st.error(f"Error initializing Gemini model: {str(e)}")
        return get_sample_questions(search)
    
    # Improved prompt with clearer instructions
    prompt = f"""
    Create a quiz with exactly 10 multiple-choice questions specifically about {search} in world history.
    Difficulty level: {quiz_level}
    
    Each question must have:
    1. A clear question related to {search}
    2. Four options (labeled as A, B, C, D)
    3. One correct answer
    4. A brief explanation of why the answer is correct
    
    Format each question in this exact JSON structure:
    {{
      "question": "What year did the Battle of Hastings take place?",
      "options": ["1066", "1086", "1166", "1186"],
      "answer": "1066",
      "explanation": "The Battle of Hastings took place in 1066 when William, Duke of Normandy defeated King Harold II of England."
    }}
    
    Return ONLY a valid JSON array with 10 questions in the format above. No additional text, no markdown formatting, just the JSON array.
    """

    try:
        st.session_state.loading = True
        
        with st.spinner(f"Generating quiz about {search}..."):
            # Make the API call
            response = model.generate_content(prompt)
            
            if response and response.text:
                # Store the raw response for debugging
                st.session_state.debug_info["raw_response"] = response.text
                
                # Clean the response text
                text = response.text.strip()
                
                # Remove any markdown code block markers
                text = re.sub(r'```(?:json)?', '', text)
                text = text.strip()
                
                # Try to extract JSON from the text
                try:
                    # Find JSON array pattern
                    json_match = re.search(r'\[.*\]', text, re.DOTALL)
                    if json_match:
                        text = json_match.group(0)
                    
                    # Parse the JSON
                    questions_data = json.loads(text)
                    st.session_state.debug_info["parsed_json"] = True
                    
                    # Ensure we have a list of questions
                    if isinstance(questions_data, list):
                        # Validate and format each question
                        valid_questions = []
                        for q in questions_data:
                            if all(key in q for key in ["question", "options", "answer", "explanation"]):
                                # Format options as a), b), c), d)
                                formatted_options = []
                                for i, opt in enumerate(q["options"]):
                                    letter = chr(97 + i)  # a, b, c, d
                                    formatted_options.append(f"{letter}) {opt}")
                                
                                # Find the index of the correct answer in the options
                                try:
                                    answer_index = q["options"].index(q["answer"])
                                    answer_letter = chr(97 + answer_index)
                                except ValueError:
                                    # If the answer isn't in options, use the first option as default
                                    answer_letter = 'a'
                                    st.session_state.debug_info["answer_not_in_options"] = True
                                
                                valid_questions.append({
                                    "question": q["question"],
                                    "options": formatted_options,
                                    "answer": answer_letter,
                                    "explanation": q["explanation"]
                                })
                        
                        if valid_questions:
                            st.session_state.loading = False
                            st.session_state.debug_info["valid_questions_count"] = len(valid_questions)
                            return valid_questions[:10]
                        else:
                            st.session_state.debug_info["no_valid_questions"] = True
                    else:
                        st.session_state.debug_info["not_a_list"] = True
                
                except json.JSONDecodeError as e:
                    st.session_state.debug_info["json_error"] = str(e)
                    # If JSON parsing fails, try to extract questions manually
                    pass
                
                # Fallback: Manual extraction for non-JSON formatted responses
                questions = []
                # Look for patterns like "Question 1:" or "1." or "Question:"
                question_patterns = [
                    r'Question\s*\d+\s*:(.?)(?:Question\s\d+\s*:|$)',
                    r'\d+\.\s*(.?)(?:\d+\.\s|$)',
                    r'Question\s*:(.?)(?:Question\s:|$)'
                ]
                
                for pattern in question_patterns:
                    matches = re.findall(pattern, text, re.DOTALL)
                    if matches:
                        for match in matches:
                            q_text = match.strip()
                            # Extract question, options, answer and explanation
                            question_match = re.search(r'^(.*?)(?:Options:|[aA]\)|\n[aA]\.)', q_text, re.DOTALL)
                            if question_match:
                                question_text = question_match.group(1).strip()
                                
                                # Extract options
                                options = []
                                option_matches = re.findall(r'[a-dA-D][\)\.]?\s*(.*?)(?:[a-dA-D][\)\.]|Answer:|Explanation:|$)', q_text, re.DOTALL)
                                for i, opt in enumerate(option_matches[:4]):  # Limit to 4 options
                                    letter = chr(97 + i)  # a, b, c, d
                                    options.append(f"{letter}) {opt.strip()}")
                                
                                # Extract answer
                                answer_match = re.search(r'Answer\s*:\s*([a-dA-D])', q_text, re.IGNORECASE)
                                answer = answer_match.group(1).lower() if answer_match else "a"
                                
                                # Extract explanation
                                explanation_match = re.search(r'Explanation\s*:(.*?)$', q_text, re.DOTALL)
                                explanation = explanation_match.group(1).strip() if explanation_match else "No explanation provided."
                                
                                if question_text and options:
                                    questions.append({
                                        "question": question_text,
                                        "options": options,
                                        "answer": answer,
                                        "explanation": explanation
                                    })
                
                if questions:
                    st.session_state.loading = False
                    st.session_state.debug_info["manual_extraction_count"] = len(questions)
                    return questions[:10]
                
                # If all parsing attempts fail, log the issue and use sample data
                st.session_state.debug_info["all_parsing_failed"] = True
                st.session_state.loading = False
                
                # Show a more detailed error message
                st.error(f"Could not parse questions from API response. Using sample questions instead. Please try a different topic or difficulty level.")
                return get_sample_questions(search)
            
            st.error("No response from AI model. Using sample questions instead.")
            st.session_state.loading = False
            return get_sample_questions(search)
            
    except Exception as e:
        st.error(f"Error generating questions: {str(e)}")
        st.session_state.debug_info["exception"] = str(e)
        st.session_state.loading = False
        return get_sample_questions(search)

# Sample questions as fallback - dynamically generated based on search term
def get_sample_questions(search_term="World History"):
    # Generic world history questions that can work for most topics
    return [
        {
            "question": f"Which of these events related to {search_term} occurred first?",
            "options": ["a) World War II", "b) World War I", "c) The Cold War", "d) The Gulf War"],
            "answer": "b",
            "explanation": "World War I (1914-1918) occurred before World War II (1939-1945), the Cold War (1947-1991), and the Gulf War (1990-1991)."
        },
        {
            "question": f"Which ancient civilization is most closely associated with {search_term}?",
            "options": ["a) Roman Empire", "b) Ancient Egypt", "c) Mesopotamia", "d) Ancient China"],
            "answer": "c",
            "explanation": "Mesopotamia is often considered the 'cradle of civilization' where the first complex urban societies developed around 4000-3000 BCE."
        },
        {
            "question": "Who was the first Roman Emperor?",
            "options": ["a) Julius Caesar", "b) Augustus", "c) Nero", "d) Constantine"],
            "answer": "b",
            "explanation": "Augustus (born Octavian) became the first Roman Emperor in 27 BCE after defeating Mark Antony and Cleopatra."
        },
        {
            "question": "Which year marked the fall of the Berlin Wall?",
            "options": ["a) 1985", "b) 1989", "c) 1991", "d) 1993"],
            "answer": "b",
            "explanation": "The Berlin Wall fell on November 9, 1989, marking a pivotal moment in the end of the Cold War and leading to German reunification."
        },
        {
            "question": "Which explorer is credited with leading the first expedition to circumnavigate the Earth?",
            "options": ["a) Christopher Columbus", "b) Vasco da Gama", "c) Ferdinand Magellan", "d) James Cook"],
            "answer": "c",
            "explanation": "Ferdinand Magellan led the expedition that first circumnavigated the globe (1519-1522), although Magellan himself was killed in the Philippines and did not complete the journey."
        },
        {
            "question": "The Renaissance period primarily began in which country?",
            "options": ["a) France", "b) England", "c) Italy", "d) Spain"],
            "answer": "c",
            "explanation": "The Renaissance began in Italy in the 14th century before spreading to the rest of Europe, with Florence often considered its birthplace."
        },
        {
            "question": "Which of these ancient wonders still exists today?",
            "options": ["a) Colossus of Rhodes", "b) Hanging Gardens of Babylon", "c) Great Pyramid of Giza", "d) Lighthouse of Alexandria"],
            "answer": "c",
            "explanation": "The Great Pyramid of Giza is the only one of the Seven Wonders of the Ancient World that still exists today, built around 2560 BCE."
        },
        {
            "question": "The Treaty of Versailles was signed at the end of which conflict?",
            "options": ["a) World War I", "b) World War II", "c) The Napoleonic Wars", "d) The Thirty Years' War"],
            "answer": "a",
            "explanation": "The Treaty of Versailles was signed in 1919 at the end of World War I, imposing harsh penalties on Germany."
        },
        {
            "question": "Who wrote 'The Communist Manifesto'?",
            "options": ["a) Vladimir Lenin", "b) Joseph Stalin", "c) Karl Marx and Friedrich Engels", "d) Leon Trotsky"],
            "answer": "c",
            "explanation": "Karl Marx and Friedrich Engels wrote 'The Communist Manifesto' in 1848, which became one of the world's most influential political documents."
        },
        {
            "question": "Which empire was ruled by Genghis Khan?",
            "options": ["a) Ottoman Empire", "b) Mongol Empire", "c) Byzantine Empire", "d) Persian Empire"],
            "answer": "b",
            "explanation": "Genghis Khan founded and ruled the Mongol Empire, which became the largest contiguous land empire in history after his death."
        }
    ]

# Initialize session state variables for quiz
def init_quiz_session_state():
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "questions" not in st.session_state:
        st.session_state.questions = []
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = {}
    if "start_time" not in st.session_state:
        st.session_state.start_time = 0
    if "elapsed_time" not in st.session_state:
        st.session_state.elapsed_time = 0
    if "topic" not in st.session_state:
        st.session_state.topic = ""
    if "difficulty" not in st.session_state:
        st.session_state.difficulty = "Beginner"
    if "loading" not in st.session_state:
        st.session_state.loading = False
    if "debug_info" not in st.session_state:
        st.session_state.debug_info = {}

# Navigation functions
def go_to_quiz():
    if st.session_state.username and st.session_state.topic:
        with st.spinner(f"Generating quiz about {st.session_state.topic}..."):
            st.session_state.questions = fetch_questions(st.session_state.topic, st.session_state.difficulty)
            
        if st.session_state.questions and len(st.session_state.questions) > 0:
            st.session_state.user_answers = {}
            st.session_state.start_time = time.time()
            st.session_state.quiz_state = "quiz"
        else:
            st.error("Failed to generate quiz questions. Please try again.")
    else:
        st.warning("Please enter your name and a topic before starting the quiz.")

def submit_quiz():
    st.session_state.elapsed_time = time.time() - st.session_state.start_time
    st.session_state.quiz_state = "results"

def restart_quiz():
    st.session_state.quiz_state = "welcome"
    st.session_state.user_answers = {}

# Welcome page with simplified design
def show_welcome_page():
    apply_custom_css()
    init_quiz_session_state()
    
    # App title
    st.markdown("<h1 class='quiz-title'>HISTOFACT QUIZ SECTION</h1>", unsafe_allow_html=True)
    st.markdown("<p class='quiz-subtitle'>Test Your Knowledge Here</p>", unsafe_allow_html=True)
    
    # Add a colorful divider
    st.markdown("---")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Use Streamlit's built-in container with custom styling
        with st.container():
            st.subheader("🚀 Ready to challenge your history knowledge?")
            
            # Simplified instructions
            st.write("Pick a historical topic, set your difficulty level, and test your knowledge!")
            
            st.markdown("### Popular Topics:")
            topics_col1, topics_col2 = st.columns(2)
            with topics_col1:
                st.markdown("• Ancient Rome\n• World War II\n• Renaissance")
            with topics_col2:
                st.markdown("• Cold War\n• Ancient Egypt\n• French Revolution")
            
            st.session_state.username = st.text_input("Your Name:", value=st.session_state.username)
            st.session_state.topic = st.text_input("Historical Topic:", value=st.session_state.topic, 
                                                  placeholder="e.g., World War II, Ancient Rome")
            st.session_state.difficulty = st.select_slider(
                "Difficulty Level:",
                options=["Beginner", "Intermediate", "Advanced"],
                value=st.session_state.difficulty
            )
            
            # Use Streamlit's primary button for better visibility
            if st.button("🚀 Start Quiz", type="primary", use_container_width=True):
                go_to_quiz()
    
    with col2:
        # Use Streamlit's built-in container
        with st.container():
            # Use a cheerful image
            st.image("assets/quiz.png", use_container_width=True)
            
            # Add a fun fact
            with st.expander("📚 Did you know?"):
                st.write("The shortest war in history was between Britain and Zanzibar on August 27, 1896. Zanzibar surrendered after just 38 minutes!")

# Quiz page with simplified design
def show_quiz_page():
    apply_custom_css()
    
    # Display header with timer
    elapsed = int(time.time() - st.session_state.start_time)
    minutes, seconds = divmod(elapsed, 60)
    
    # Use Streamlit's native components
    st.title(f"Quiz: {st.session_state.topic}")
    st.write(f"Difficulty: {st.session_state.difficulty}")
    
    # Timer in a colorful container
    with st.container():
        st.markdown(f"<div class='timer'>⏱️ Time: {minutes:02d}:{seconds:02d}</div>", unsafe_allow_html=True)
    
    # Welcome message
    st.info(f"Good luck, *{st.session_state.username}*! Answer all 10 questions below.")
    
    # Add a colorful divider
    st.markdown("---")
    
    # Display questions using Streamlit's native components
    for i, q in enumerate(st.session_state.questions):
        with st.container():
            st.subheader(f"Question {i+1}: {q['question']}")
            
            # Extract just the option letter and text
            options = []
            for opt in q['options']:
                letter = opt[0]  # Get the option letter (a, b, c, d)
                text = opt[3:].strip()  # Get the option text without the letter prefix
                options.append((letter, text))
            
            # Display as radio buttons
            selected = st.radio(
                f"Select your answer:",
                options,
                format_func=lambda x: f"{x[0]}) {x[1]}",
                key=f"q_{i}",
                index=None  # Don't preselect any answer
            )
            
            if selected:
                st.session_state.user_answers[i] = selected[0]  # Store just the letter
            
            # Add a light divider between questions
            if i < len(st.session_state.questions) - 1:
                st.markdown("---")
    
    # Submit button
    st.button("📝 Submit Answers", type="primary", on_click=submit_quiz, use_container_width=True)

# Results page with simplified design
def show_results_page():
    apply_custom_css()
    
    st.title("Your Quiz Results")
    
    # Calculate score
    correct_count = 0
    results = []
    
    for i, q in enumerate(st.session_state.questions):
        user_ans = st.session_state.user_answers.get(i, None)
        correct_ans = q['answer']
        is_correct = user_ans == correct_ans
        
        if is_correct:
            correct_count += 1
            
        results.append({
            "question_num": i + 1,
            "question": q['question'],
            "options": q['options'],
            "user_answer": user_ans,
            "correct_answer": correct_ans,
            "is_correct": is_correct,
            "explanation": q['explanation']
        })
    
    # Display score and time
    minutes, seconds = divmod(int(st.session_state.elapsed_time), 60)
    
    st.markdown(f"""
    <div class='score-display'>
        <h2>{st.session_state.username}, your score: {correct_count}/10</h2>
        <p>Time taken: {minutes:02d}:{seconds:02d}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Performance message with appropriate Streamlit components
    if correct_count >= 8:
        st.success("🏆 Excellent! You're a history expert!")
    elif correct_count >= 6:
        st.info("👍 Good job! You have solid historical knowledge.")
    else:
        st.warning("📚 Keep exploring history! There's more to discover.")
    
    # Add a colorful divider
    st.markdown("---")
    
    # Review answers
    st.subheader("Review Your Answers:")
    
    for result in results:
        with st.expander(f"Question {result['question_num']}: {result['question']}"):
            # Display all options
            for opt in result['options']:
                letter = opt[0]
                is_user_answer = letter == result['user_answer']
                is_correct_answer = letter == result['correct_answer']
                
                if is_user_answer and is_correct_answer:
                    st.markdown(f"<span class='correct-answer'>✓ {opt}</span> (Your answer)", unsafe_allow_html=True)
                elif is_user_answer:
                    st.markdown(f"<span class='incorrect-answer'>✗ {opt}</span> (Your answer)", unsafe_allow_html=True)
                elif is_correct_answer:
                    st.markdown(f"<span class='correct-answer'>{opt}</span> (Correct answer)", unsafe_allow_html=True)
                else:
                    st.markdown(f"{opt}", unsafe_allow_html=True)
            
            # Display explanation for all questions
            st.markdown(f"<div class='explanation'><strong>Explanation:</strong> {result['explanation']}</div>", unsafe_allow_html=True)
    
    # Add a colorful divider
    st.markdown("---")
    
    # Buttons for next actions
    col1, col2 = st.columns(2)
    with col1:
        st.button("🔄 Try Another Topic", type="primary", on_click=restart_quiz, use_container_width=True)
    with col2:
        if st.button("📊 Share Results", use_container_width=True):
            st.success(f"Results shared! (This is a placeholder - actual sharing functionality would be implemented here)")