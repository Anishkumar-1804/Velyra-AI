"""
Angiyam.ai Curriculum Seed Data
Idempotent Seeder for all 7 Genres, Units, and Sessions.
"""
from typing import List, Dict, Any
from sqlalchemy.orm import Session as DBSession
from backend.app.models.genre import Genre
from backend.app.models.unit import Unit
from backend.app.models.session import Session


CURRICULUM_DATA: List[Dict[str, Any]] = [
    # ---------------------------------------------------------
    # GENRE 1: COLLEGE LIFE
    # ---------------------------------------------------------
    {
        "slug": "college-life",
        "title": "College Life",
        "description": "Navigate campus interactions, classroom discussions, faculty meetings, friendships, and career preparation.",
        "icon": "GraduationCap",
        "order_index": 1,
        "units": [
            {
                "slug": "campus-life",
                "title": "Campus Life",
                "description": "Essential conversations across campus, canteen, libraries, and orienting yourself.",
                "order_index": 1,
                "sessions": [
                    {
                        "slug": "introducing-yourself-classmate",
                        "title": "Introducing Yourself to a Classmate",
                        "description": "Break the ice with a new peer in the college corridor or lecture hall.",
                        "difficulty": "Beginner",
                        "cefr_level": "A1",
                        "scenario": "You have just arrived for your first lecture and sit next to another student who is also starting their degree.",
                        "ai_role": "Fellow first-year college student (Kavin)",
                        "user_role": "First-year college student",
                        "learning_objectives": [
                            "Introduce your name and hometown",
                            "State your major or course of study",
                            "Ask a polite question about their background",
                            "Establish a friendly rapport"
                        ],
                        "allowed_topics": ["names", "hometowns", "majors", "classes", "campus locations", "college hobbies"],
                        "forbidden_topics": ["politics", "unrelated trivia", "complex technical theory"],
                        "conversation_stages": [
                            "1. Greeting & Name Exchange",
                            "2. Department / Degree Talk",
                            "3. Hometown / Background Sharing",
                            "4. First Impression of Campus",
                            "5. Friendly Wrap-up Before Class Starts"
                        ],
                        "opening_message": "Hi there! Is anyone sitting here, or can I grab this seat next to you?",
                        "completion_conditions": [
                            "User has exchanged names",
                            "User has mentioned their subject or major",
                            "At least 4 conversational turns completed"
                        ],
                        "suggested_vocabulary": ["major", "hometown", "orientation", "lecture", "department", "commute"],
                        "estimated_duration": 4,
                        "target_turns": 5,
                        "order_index": 1
                    },
                    {
                        "slug": "talking-about-your-course",
                        "title": "Talking About Your Course",
                        "description": "Discuss subjects, syllabus, professors, and expectations with a senior or classmate.",
                        "difficulty": "Elementary",
                        "cefr_level": "A2",
                        "scenario": "You meet a department classmate at the cafeteria to discuss the semester subjects and textbooks.",
                        "ai_role": "Department Classmate (Priya)",
                        "user_role": "College student",
                        "learning_objectives": [
                            "Express opinions about challenging and interesting subjects",
                            "Ask about recommended study materials or reference books",
                            "Discuss semester goals"
                        ],
                        "allowed_topics": ["subjects", "professors", "syllabus", "assignments", "reference books", "credits"],
                        "forbidden_topics": ["off-topic news", "personal financial details"],
                        "conversation_stages": [
                            "1. Greeting at Cafeteria",
                            "2. Discussion of Semester Subjects",
                            "3. Favorite and Difficult Modules",
                            "4. Sharing Study Strategies",
                            "5. Wrap-up and Next Class Reminder"
                        ],
                        "opening_message": "Hey! How are you finding the course syllabus this semester? Some of the engineering mathematics modules look pretty intense!",
                        "completion_conditions": [
                            "User shared their thoughts on at least one subject",
                            "User discussed their preparation plan"
                        ],
                        "suggested_vocabulary": ["syllabus", "credits", "electives", "practical lab", "curriculum", "assignments"],
                        "estimated_duration": 5,
                        "target_turns": 6,
                        "order_index": 2
                    },
                    {
                        "slug": "finding-a-classroom",
                        "title": "Finding a Classroom",
                        "description": "Ask for directions to academic blocks, seminar halls, and lab facilities.",
                        "difficulty": "Beginner",
                        "cefr_level": "A1",
                        "scenario": "You are running slightly late for a lecture in Block C and need to ask a senior student for directions.",
                        "ai_role": "Helpful senior college student (Karthik)",
                        "user_role": "Student looking for room C-304",
                        "learning_objectives": [
                            "Ask polite directional questions",
                            "Understand prepositions of place (next to, opposite, 3rd floor)",
                            "Confirm details before departing"
                        ],
                        "allowed_topics": ["classroom numbers", "academic blocks", "stairs", "elevators", "departments"],
                        "forbidden_topics": ["unrelated topics", "academic grades"],
                        "conversation_stages": [
                            "1. Polite Attention Grab",
                            "2. Stating Target Classroom (C-304)",
                            "3. Understanding Landmarks & Floor Directions",
                            "4. Clarification and Gratitude"
                        ],
                        "opening_message": "Hey, you look a bit lost! Are you looking for a specific lecture hall or department block?",
                        "completion_conditions": [
                            "User asked for the classroom location",
                            "User confirmed the directions",
                            "User thanked the senior"
                        ],
                        "suggested_vocabulary": ["corridor", "adjacent", "staircase", "opposite", "seminar hall", "wing"],
                        "estimated_duration": 3,
                        "target_turns": 4,
                        "order_index": 3
                    },
                    {
                        "slug": "asking-about-timetable",
                        "title": "Asking About the Timetable",
                        "description": "Clarify lecture timings, break periods, and lab schedules with class representative.",
                        "difficulty": "Elementary",
                        "cefr_level": "A2",
                        "scenario": "You contact the Class Representative to clarify sudden schedule changes and lab slots.",
                        "ai_role": "Class Representative (Nithya)",
                        "user_role": "Student checking schedule",
                        "learning_objectives": [
                            "Inquire about specific time slots and days",
                            "Confirm venue and professor availability",
                            "Use time expressions accurately"
                        ],
                        "allowed_topics": ["timetable", "lecture slots", "rescheduled classes", "breaks", "lab batches"],
                        "forbidden_topics": ["unrelated gossip"],
                        "conversation_stages": [
                            "1. Inquiring About Timetable",
                            "2. Checking Friday Lab Timings",
                            "3. Rescheduled Sessions",
                            "4. Confirmation"
                        ],
                        "opening_message": "Hi! Did you check the updated schedule on the department noticeboard for this week?",
                        "completion_conditions": ["User asked about specific class timing", "User clarified lab batch schedule"],
                        "suggested_vocabulary": ["rescheduled", "slot", "period", "recess", "batch", "practical"],
                        "estimated_duration": 4,
                        "target_turns": 5,
                        "order_index": 4
                    },
                    {
                        "slug": "talking-about-college-day",
                        "title": "Talking About Your College Day",
                        "description": "Summarize how your day went with a roommate or friend.",
                        "difficulty": "Intermediate",
                        "cefr_level": "B1",
                        "scenario": "You return to your hostel room / common room after a busy day of lectures and labs.",
                        "ai_role": "Hostel Roommate (Selvan)",
                        "user_role": "Hostel student",
                        "learning_objectives": [
                            "Use past tense naturally to describe events",
                            "Express feelings of tiredness or excitement",
                            "Ask about the other person's day"
                        ],
                        "allowed_topics": ["daily lectures", "canteen food", "lab experiments", "homework", "evening plans"],
                        "forbidden_topics": ["politics", "exam leakage conspiracies"],
                        "conversation_stages": [
                            "1. Evening Greeting",
                            "2. Describing Highlights of the Day",
                            "3. Discussing Challenges / Labs",
                            "4. Evening / Dinner Plans"
                        ],
                        "opening_message": "Phew! What a long day. How did your afternoon lab session go?",
                        "completion_conditions": ["User narrated at least 2 events from their day", "User asked about roommate's day"],
                        "suggested_vocabulary": ["hectic", "exhausting", "presentation", "experiment", "submission", "refreshing"],
                        "estimated_duration": 5,
                        "target_turns": 6,
                        "order_index": 5
                    }
                ]
            },
            {
                "slug": "classroom-conversations",
                "title": "Classroom Conversations",
                "description": "Interact respectfully and clearly with faculty, project teammates, and study groups.",
                "order_index": 2,
                "sessions": [
                    {
                        "slug": "asking-teacher-a-question",
                        "title": "Asking a Teacher a Question",
                        "description": "Politely ask your professor to clarify a concept after a lecture.",
                        "difficulty": "Intermediate",
                        "cefr_level": "B1",
                        "scenario": "After a lecture on Thermodynamics / Data Structures, you approach your professor's desk to ask for clarification.",
                        "ai_role": "College Professor (Dr. Aravind)",
                        "user_role": "Inquisitive student",
                        "learning_objectives": [
                            "Use formal and polite academic greetings",
                            "State the specific point of confusion concisely",
                            "Acknowledge the explanation politely"
                        ],
                        "allowed_topics": ["lecture topic", "slide formulas", "reference chapters", "office hours"],
                        "forbidden_topics": ["personal favors", "bribes", "unrelated chatter"],
                        "conversation_stages": [
                            "1. Formal Greeting & Permission to Ask",
                            "2. Stating the Specific Doubt",
                            "3. Engaging with Professor's Explanation",
                            "4. Thanking Professor and Next Steps"
                        ],
                        "opening_message": "Yes, come in. Do you have a question regarding today's lecture on algorithm efficiency?",
                        "completion_conditions": ["User stated their question politely", "User responded to teacher's clarification"],
                        "suggested_vocabulary": ["clarify", "concept", "slide", "approach", "formula", "office hours"],
                        "estimated_duration": 5,
                        "target_turns": 5,
                        "order_index": 1
                    },
                    {
                        "slug": "discussing-group-project",
                        "title": "Discussing a Group Project",
                        "description": "Coordinate division of work and deadlines with your project team leader.",
                        "difficulty": "Intermediate",
                        "cefr_level": "B1",
                        "scenario": "Your team needs to submit a mini-project report in two weeks. You are dividing research and slide creation roles.",
                        "ai_role": "Project Team Lead (Divya)",
                        "user_role": "Project team member",
                        "learning_objectives": [
                            "Propose specific task assignments",
                            "Negotiate timeline and milestone dates",
                            "Give constructive feedback"
                        ],
                        "allowed_topics": ["project tasks", "milestones", "presentation slides", "data collection", "deadlines"],
                        "forbidden_topics": ["unrelated personal life"],
                        "conversation_stages": [
                            "1. Project Sync Initiation",
                            "2. Task Division & Preference",
                            "3. Agreeing on Deadlines",
                            "4. Final Action Plan"
                        ],
                        "opening_message": "Thanks for meeting up. We have two weeks until the submission. Which part of the project would you like to take ownership of?",
                        "completion_conditions": ["User selected a task", "User agreed on a milestone deadline"],
                        "suggested_vocabulary": ["deliverable", "milestone", "collaborate", "outline", "deadline", "slides"],
                        "estimated_duration": 5,
                        "target_turns": 6,
                        "order_index": 2
                    }
                ]
            },
            {
                "slug": "career-preparation",
                "title": "Career Preparation",
                "description": "Campus placements, resume reviews, technical project explanations, and HR mock interviews.",
                "order_index": 3,
                "sessions": [
                    {
                        "slug": "introducing-yourself-interview",
                        "title": "Introducing Yourself in an Interview",
                        "description": "Deliver a crisp, impactful answer to 'Tell me about yourself' for campus placements.",
                        "difficulty": "Upper Intermediate",
                        "cefr_level": "B2",
                        "scenario": "You are sitting across from a company hiring manager for a campus placement interview.",
                        "ai_role": "Campus Placement Interviewer (Mr. Madhavan)",
                        "user_role": "Job candidate / final-year student",
                        "learning_objectives": [
                            "Structure 'Tell me about yourself' (Education, Skills, Projects, Passion)",
                            "Highlight key technical and soft skills",
                            "Speak with professional confidence and clear articulation"
                        ],
                        "allowed_topics": ["education", "academic background", "technical skills", "internships", "projects", "career ambitions"],
                        "forbidden_topics": ["childhood stories", "unrelated hobbies", "salary demands in introduction"],
                        "conversation_stages": [
                            "1. Welcome & Formal Opening",
                            "2. 'Tell me about yourself' Pitch",
                            "3. Follow-up on Key Project / Skill",
                            "4. Candidate Motivation for the Role",
                            "5. Interview Next Steps"
                        ],
                        "opening_message": "Welcome to the interview! To get started, could you please walk me through your background and what you are passionate about?",
                        "completion_conditions": ["User gave a structured intro", "User responded to interviewer's follow-up question"],
                        "suggested_vocabulary": ["strengths", "passionate", "internship", "hands-on experience", "problem-solving", "aspiring"],
                        "estimated_duration": 6,
                        "target_turns": 6,
                        "order_index": 1
                    }
                ]
            }
        ]
    },

    # ---------------------------------------------------------
    # GENRE 2: DAILY LIFE
    # ---------------------------------------------------------
    {
        "slug": "daily-life",
        "title": "Daily Life",
        "description": "Daily routines, family conversations, weekend leisure, and sharing personal experiences.",
        "icon": "Sun",
        "order_index": 2,
        "units": [
            {
                "slug": "daily-routine",
                "title": "Daily Routine",
                "description": "Talk about morning habits, commuting, work-life balance, and evening relaxation.",
                "order_index": 1,
                "sessions": [
                    {
                        "slug": "morning-routine",
                        "title": "Morning Routine",
                        "description": "Describe your morning schedule, exercise, breakfast, and preparing for the day.",
                        "difficulty": "Beginner",
                        "cefr_level": "A1",
                        "scenario": "You and your colleague are sharing morning habits over a cup of tea.",
                        "ai_role": "Colleague / Friend (Janani)",
                        "user_role": "Friend sharing daily schedule",
                        "learning_objectives": [
                            "Use simple present tense for habitual actions (I wake up, I usually have)",
                            "Use adverbs of frequency (always, often, usually, rarely)",
                            "Discuss morning time management"
                        ],
                        "allowed_topics": ["waking up", "alarm clocks", "breakfast", "exercise", "tea/coffee", "commute"],
                        "forbidden_topics": ["politics", "complex financial advice"],
                        "conversation_stages": [
                            "1. Casual Morning Conversation Starter",
                            "2. Sharing Wake-up Time & Habits",
                            "3. Breakfast & Morning Exercise",
                            "4. Preparing for the Day",
                            "5. Wrap-up"
                        ],
                        "opening_message": "Good morning! You look energetic today. Are you an early riser, or do you prefer sleeping in?",
                        "completion_conditions": ["User described wake up time", "User mentioned breakfast or morning habit"],
                        "suggested_vocabulary": ["routine", "alarm", "meditation", "wholesome", "commute", "productive"],
                        "estimated_duration": 4,
                        "target_turns": 5,
                        "order_index": 1
                    },
                    {
                        "slug": "weekend-routine",
                        "title": "Weekend Routine",
                        "description": "Discuss how you spend your Saturdays and Sundays relaxing or pursuing hobbies.",
                        "difficulty": "Elementary",
                        "cefr_level": "A2",
                        "scenario": "It is Friday evening, and your friend asks about your usual weekend activities.",
                        "ai_role": "Close Friend (Tharun)",
                        "user_role": "Friend making weekend plans",
                        "learning_objectives": [
                            "Contrast weekday work with weekend leisure",
                            "Express likes and dislikes with reasons",
                            "Talk about outdoor and indoor activities"
                        ],
                        "allowed_topics": ["weekends", "movies", "cleaning", "outings", "sports", "sleeping"],
                        "forbidden_topics": ["work spreadsheets", "unrelated politics"],
                        "conversation_stages": [
                            "1. Friday Anticipation",
                            "2. Saturday Leisure vs Chores",
                            "3. Sunday Family Time",
                            "4. Recharging for the Week"
                        ],
                        "opening_message": "Thank goodness it's Friday! How do you usually spend your weekends? Do you prefer staying home or going out?",
                        "completion_conditions": ["User described typical weekend activities", "User gave reasons for preferences"],
                        "suggested_vocabulary": ["unwind", "chores", "errands", "binge-watch", "outdoors", "recharge"],
                        "estimated_duration": 4,
                        "target_turns": 5,
                        "order_index": 2
                    }
                ]
            },
            {
                "slug": "home-and-family",
                "title": "Home & Family",
                "description": "Talk warmly about your hometown, family members, responsibilities, and neighborhood.",
                "order_index": 2,
                "sessions": [
                    {
                        "slug": "introducing-your-family",
                        "title": "Introducing Your Family",
                        "description": "Describe your family members, their occupations, and what you enjoy doing together.",
                        "difficulty": "Elementary",
                        "cefr_level": "A2",
                        "scenario": "During a friendly dinner, your conversational partner asks you about your family background.",
                        "ai_role": "Friendly acquaintance (Ananya)",
                        "user_role": "Speaker sharing family details",
                        "learning_objectives": [
                            "Use descriptive family vocabulary (siblings, elder, younger, occupation)",
                            "Describe personalities and occupations",
                            "Share a fond family tradition or meal"
                        ],
                        "allowed_topics": ["parents", "siblings", "hometown", "professions", "family dinners", "pets"],
                        "forbidden_topics": ["family disputes", "confidential legal details"],
                        "conversation_stages": [
                            "1. Inquiring About Family Size",
                            "2. Talking About Siblings and Parents",
                            "3. Occupations and Interests",
                            "4. Memorable Family Gathering"
                        ],
                        "opening_message": "Tell me a bit about your family! Do you have a large family, and do you have any brothers or sisters?",
                        "completion_conditions": ["User mentioned at least 2 family members", "User described an occupation or personality trait"],
                        "suggested_vocabulary": ["siblings", "joint family", "nuclear family", "supportive", "hometown", "tradition"],
                        "estimated_duration": 5,
                        "target_turns": 5,
                        "order_index": 1
                    }
                ]
            }
        ]
    },

    # ---------------------------------------------------------
    # GENRE 3: SHOPPING
    # ---------------------------------------------------------
    {
        "slug": "shopping",
        "title": "Shopping",
        "description": "Retail interactions, comparing prices, buying clothing and electronics, returns and customer care.",
        "icon": "ShoppingBag",
        "order_index": 3,
        "units": [
            {
                "slug": "clothing",
                "title": "Clothing & Apparel",
                "description": "Try on clothes, ask for sizes and colors, check fitting, and inquire about discounts.",
                "order_index": 1,
                "sessions": [
                    {
                        "slug": "buying-a-shirt",
                        "title": "Buying a Shirt",
                        "description": "Choose a casual or formal shirt, ask for your size, and negotiate price.",
                        "difficulty": "Elementary",
                        "cefr_level": "A2",
                        "scenario": "You are at a clothing store looking for a formal cotton shirt for an upcoming event.",
                        "ai_role": "Store Sales Associate (Vignesh)",
                        "user_role": "Shopper looking for formal wear",
                        "learning_objectives": [
                            "Express preferences for fabric, size, and fit (slim fit, regular, medium)",
                            "Ask about trial rooms and price discounts",
                            "Make a polite decision to purchase"
                        ],
                        "allowed_topics": ["shirt types", "sizes", "colors", "fabrics", "trial rooms", "price & discounts"],
                        "forbidden_topics": ["unrelated politics", "store company balance sheets"],
                        "conversation_stages": [
                            "1. Store Greeting & Inquiry",
                            "2. Recommending Colors & Sizes",
                            "3. Trying On & Checking Fit",
                            "4. Billing & Discount Inquiries"
                        ],
                        "opening_message": "Welcome to our store! Are you looking for formal shirts or something casual today?",
                        "completion_conditions": ["User specified size/color", "User asked about trial or price", "User confirmed selection"],
                        "suggested_vocabulary": ["formal", "cotton", "trial room", "fitting", "discount", "receipt"],
                        "estimated_duration": 4,
                        "target_turns": 5,
                        "order_index": 1
                    },
                    {
                        "slug": "returning-clothing",
                        "title": "Returning or Exchanging an Item",
                        "description": "Politely explain why an item did not fit and request an exchange or refund.",
                        "difficulty": "Intermediate",
                        "cefr_level": "B1",
                        "scenario": "You bought a jacket yesterday, but upon trying it at home you found a stitch defect and the wrong size.",
                        "ai_role": "Customer Service Executive (Saravanan)",
                        "user_role": "Customer requesting exchange",
                        "learning_objectives": [
                            "State the issue clearly and politely",
                            "Present proof of purchase (receipt/tag)",
                            "Negotiate exchange options"
                        ],
                        "allowed_topics": ["receipt", "exchange policy", "defect", "size mismatch", "replacement"],
                        "forbidden_topics": ["verbal abuse", "unrelated topics"],
                        "conversation_stages": [
                            "1. Customer Service Greeting",
                            "2. Explaining Reason for Return",
                            "3. Presenting Receipt & Condition Check",
                            "4. Processing Exchange / Refund",
                            "5. Confirmation & Closing"
                        ],
                        "opening_message": "Hello, how can I assist you at customer service today?",
                        "completion_conditions": ["User explained the problem with the item", "User requested size exchange or refund"],
                        "suggested_vocabulary": ["receipt", "defect", "exchange", "refund", "store credit", "warranty"],
                        "estimated_duration": 5,
                        "target_turns": 5,
                        "order_index": 2
                    }
                ]
            },
            {
                "slug": "electronics",
                "title": "Electronics",
                "description": "Compare smartphones, laptops, headphones, ask about warranty and technical specs.",
                "order_index": 2,
                "sessions": [
                    {
                        "slug": "buying-headphones",
                        "title": "Buying Wireless Headphones",
                        "description": "Compare noise-cancellation, battery life, and sound quality with a tech specialist.",
                        "difficulty": "Intermediate",
                        "cefr_level": "B1",
                        "scenario": "You visit a tech showroom looking for noise-canceling headphones for online meetings and travel.",
                        "ai_role": "Showroom Tech Advisor (Selvan)",
                        "user_role": "Customer looking for audio gear",
                        "learning_objectives": [
                            "Ask comparative questions (Which has better battery life?)",
                            "Express budget constraints and key priorities",
                            "Inquire about manufacturer warranty and return policies"
                        ],
                        "allowed_topics": ["audio specs", "battery life", "noise cancellation", "budget", "warranty", "bluetooth version"],
                        "forbidden_topics": ["unrelated politics", "piracy"],
                        "conversation_stages": [
                            "1. Tech Needs Assessment",
                            "2. Comparing 2 Brand Models",
                            "3. Inquiring About Battery & Noise Cancellation",
                            "4. Pricing & Warranty Clarification",
                            "5. Purchase Decision"
                        ],
                        "opening_message": "Hello! Looking for headphones today? What is your primary use — music, gaming, or office calls?",
                        "completion_conditions": ["User stated their use case and budget", "User asked about features or warranty"],
                        "suggested_vocabulary": ["noise-cancellation", "battery life", "wireless", "ergonomic", "warranty", "clarity"],
                        "estimated_duration": 5,
                        "target_turns": 6,
                        "order_index": 1
                    }
                ]
            }
        ]
    },

    # ---------------------------------------------------------
    # GENRE 4: TRAVEL
    # ---------------------------------------------------------
    {
        "slug": "travel",
        "title": "Travel",
        "description": "Airport check-in, hotel reservations, local transport, taxi booking, and sightseeing recommendations.",
        "icon": "Plane",
        "order_index": 4,
        "units": [
            {
                "slug": "hotel",
                "title": "Hotel",
                "description": "Hotel check-in, room preferences, amenity requests, room service, and check-out.",
                "order_index": 1,
                "sessions": [
                    {
                        "slug": "checking-into-a-hotel",
                        "title": "Checking Into a Hotel",
                        "description": "The quintessential hotel check-in scenario: show booking, choose room, ask about breakfast.",
                        "difficulty": "Intermediate",
                        "cefr_level": "B1",
                        "scenario": "The user has arrived at a hotel lobby and wants to complete their check-in process.",
                        "ai_role": "Hotel Receptionist (Swathi)",
                        "user_role": "Hotel Guest",
                        "learning_objectives": [
                            "Provide reservation information and personal identification",
                            "Ask about room amenities, floor, and breakfast timings",
                            "Make one polite special request (quiet room, high floor, extra card key)",
                            "Complete check-in smoothly"
                        ],
                        "allowed_topics": ["reservation", "guest name", "identification", "room type", "check-in", "breakfast", "hotel facilities", "basic requests"],
                        "forbidden_topics": ["politics", "unrelated trivia", "programming", "general knowledge", "unrelated travel planning"],
                        "conversation_stages": [
                            "1. Greeting & Reservation Inquiry",
                            "2. Identification & Booking Verification",
                            "3. Room Allocation & Key Card Handover",
                            "4. Facility Overview (Breakfast, Wi-Fi, Gym)",
                            "5. Special Request & Confirmation",
                            "6. Polite Closing"
                        ],
                        "opening_message": "Good evening! Welcome to the Grand Heritage Hotel. Do you have a reservation with us?",
                        "completion_conditions": [
                            "User provided booking name or details",
                            "User confirmed room preference or made a polite request",
                            "User acknowledged key card and breakfast information",
                            "At least 5 conversational turns completed"
                        ],
                        "suggested_vocabulary": ["reservation", "booking confirmation", "complimentary breakfast", "key card", "amenities", "high floor"],
                        "estimated_duration": 5,
                        "target_turns": 6,
                        "order_index": 1
                    },
                    {
                        "slug": "reporting-a-room-problem",
                        "title": "Reporting a Room Problem",
                        "description": "Call the hotel front desk to report an air conditioning issue or missing towels.",
                        "difficulty": "Intermediate",
                        "cefr_level": "B1",
                        "scenario": "You have checked into room 402, but the air conditioner is blowing warm air and the hot water isn't working.",
                        "ai_role": "Front Desk Manager (Murugan)",
                        "user_role": "Hotel Guest in Room 402",
                        "learning_objectives": [
                            "Politely express dissatisfaction without losing temper",
                            "Describe physical problems accurately (not functioning, leaking, blowing warm air)",
                            "Confirm when maintenance staff will arrive"
                        ],
                        "allowed_topics": ["room number", "AC problem", "hot water", "maintenance", "room change"],
                        "forbidden_topics": ["profanity", "unrelated gossip"],
                        "conversation_stages": [
                            "1. Front Desk Answering Call",
                            "2. Explaining the Room Issue",
                            "3. Troubleshooting & Apology",
                            "4. Dispatching Maintenance",
                            "5. Follow-up Assurance"
                        ],
                        "opening_message": "Front Desk, this is Manoj speaking. How may I assist you this evening?",
                        "completion_conditions": ["User gave room number", "User explained AC or water problem", "User agreed on maintenance visit"],
                        "suggested_vocabulary": ["air conditioning", "malfunctioning", "maintenance", "promptly", "inconvenience", "technician"],
                        "estimated_duration": 4,
                        "target_turns": 5,
                        "order_index": 2
                    }
                ]
            },
            {
                "slug": "transportation",
                "title": "Transportation & Cabs",
                "description": "Hail a taxi, negotiate routes, use metro passes, and ask locals for navigation help.",
                "order_index": 2,
                "sessions": [
                    {
                        "slug": "taking-a-taxi",
                        "title": "Taking a Taxi / Cab",
                        "description": "Give your destination address, request AC, and ask about luggage and meter fare.",
                        "difficulty": "Beginner",
                        "cefr_level": "A1",
                        "scenario": "You step outside the airport terminal and need a taxi to take you to City Center.",
                        "ai_role": "Taxi Driver (Selvan)",
                        "user_role": "Passenger arriving with luggage",
                        "learning_objectives": [
                            "State destination and landmarks clearly",
                            "Ask about meter vs fixed fares",
                            "Give navigation instructions (turn left, stop here)"
                        ],
                        "allowed_topics": ["destination", "luggage", "meter fare", "toll charges", "traffic route"],
                        "forbidden_topics": ["unrelated politics", "driver personal history"],
                        "conversation_stages": [
                            "1. Inquiring Destination",
                            "2. Boot / Luggage Loading",
                            "3. Fare and Route Discussion",
                            "4. Arrival and Payment"
                        ],
                        "opening_message": "Hello sir! Where would you like to go today?",
                        "completion_conditions": ["User stated destination", "User confirmed fare / meter", "User completed ride"],
                        "suggested_vocabulary": ["destination", "luggage", "meter", "toll", "landmark", "drop-off"],
                        "estimated_duration": 4,
                        "target_turns": 5,
                        "order_index": 1
                    }
                ]
            }
        ]
    },

    # ---------------------------------------------------------
    # GENRE 5: COOKING & FOOD
    # ---------------------------------------------------------
    {
        "slug": "cooking-food",
        "title": "Cooking & Food",
        "description": "Ordering in restaurants, explaining recipes, dietary preferences, and discussing world cuisines.",
        "icon": "Utensils",
        "order_index": 5,
        "units": [
            {
                "slug": "restaurants",
                "title": "Restaurants & Dining",
                "description": "Reserve a table, order starters and main course, ask about spice levels, and pay the bill.",
                "order_index": 1,
                "sessions": [
                    {
                        "slug": "ordering-food",
                        "title": "Ordering Food at a Restaurant",
                        "description": "Order dishes, specify dietary restrictions (vegetarian, low spice), and ask for recommendations.",
                        "difficulty": "Elementary",
                        "cefr_level": "A2",
                        "scenario": "You are having dinner at a popular restaurant with a friend and are ordering from the server.",
                        "ai_role": "Restaurant Server (Vimal)",
                        "user_role": "Diner placing an order",
                        "learning_objectives": [
                            "Use polite ordering phrases ('Could we please have...', 'I would like...')",
                            "Specify spice level and dietary needs",
                            "Ask about chef specials or beverage options"
                        ],
                        "allowed_topics": ["menu items", "starters", "main course", "drinks", "spice level", "desserts", "bill"],
                        "forbidden_topics": ["unrelated politics", "kitchen recipes in detail"],
                        "conversation_stages": [
                            "1. Server Greeting & Beverage Order",
                            "2. Chef Recommendations",
                            "3. Main Course & Spice Customization",
                            "4. Side Orders & Breads",
                            "5. Order Confirmation"
                        ],
                        "opening_message": "Good evening! Welcome to Saffron Bistro. Can I start you off with some fresh lime soda or appetizers while you review the menu?",
                        "completion_conditions": ["User ordered appetizers/drinks", "User ordered main course with spice preference"],
                        "suggested_vocabulary": ["appetizers", "specialty", "mild spice", "vegetarian", "platter", "beverage"],
                        "estimated_duration": 5,
                        "target_turns": 5,
                        "order_index": 1
                    },
                    {
                        "slug": "paying-the-bill",
                        "title": "Paying the Bill & Splitting",
                        "description": "Ask for the check, verify itemized items, split with friends, and choose payment method.",
                        "difficulty": "Beginner",
                        "cefr_level": "A1",
                        "scenario": "You have finished your meal and want to settle the bill using card or UPI.",
                        "ai_role": "Restaurant Cashier / Server",
                        "user_role": "Customer settling the bill",
                        "learning_objectives": [
                            "Ask for the bill politely",
                            "Inquire about payment methods (Card, Cash, UPI)",
                            "Leave a tip or clarify service charge"
                        ],
                        "allowed_topics": ["bill", "payment method", "service charge", "receipt", "tip"],
                        "forbidden_topics": ["unrelated topics"],
                        "conversation_stages": [
                            "1. Requesting the Check",
                            "2. Confirming Payment Method",
                            "3. Processing Payment & Receipt",
                            "4. Polite Goodbye"
                        ],
                        "opening_message": "I hope you enjoyed your meal! Would you like to see our dessert menu, or shall I bring the check?",
                        "completion_conditions": ["User asked for bill", "User specified payment mode"],
                        "suggested_vocabulary": ["check", "bill", "itemized", "contactless", "receipt", "service tax"],
                        "estimated_duration": 3,
                        "target_turns": 4,
                        "order_index": 2
                    }
                ]
            },
            {
                "slug": "cooking",
                "title": "Cooking & Recipes",
                "description": "Explain how to prepare your favorite dish, describe ingredients, spices, and cooking steps.",
                "order_index": 2,
                "sessions": [
                    {
                        "slug": "explaining-a-recipe",
                        "title": "Explaining a Recipe",
                        "description": "Walk a curious friend through making Biryani, Dosa, or your signature homemade dish.",
                        "difficulty": "Intermediate",
                        "cefr_level": "B1",
                        "scenario": "Your friend tasted a delicious dish you brought from home and eagerly asks how to make it.",
                        "ai_role": "Curious Foodie Friend (Madhavan)",
                        "user_role": "Home Cook explaining recipe",
                        "learning_objectives": [
                            "Use sequential linking words (First, Then, After that, Finally)",
                            "Describe cooking actions (sauté, simmer, marinate, stir, boil)",
                            "Detail spice proportions and cooking time"
                        ],
                        "allowed_topics": ["ingredients", "spices", "cooking steps", "marination", "flame heat", "garnishing"],
                        "forbidden_topics": ["unrelated politics", "restaurant business financials"],
                        "conversation_stages": [
                            "1. Friend Complimenting the Food",
                            "2. Listing Key Ingredients & Spices",
                            "3. Explaining Preparation & Cooking Steps",
                            "4. Tips for Best Flavor & Garnishing"
                        ],
                        "opening_message": "That meal was incredible! You have to teach me how you made it. What are the key ingredients I need to buy first?",
                        "completion_conditions": ["User listed key ingredients", "User gave step-by-step instructions"],
                        "suggested_vocabulary": ["sauté", "simmer", "marinate", "aromatic", "garnish", "proportions"],
                        "estimated_duration": 5,
                        "target_turns": 6,
                        "order_index": 1
                    }
                ]
            }
        ]
    },

    # ---------------------------------------------------------
    # GENRE 6: CASUAL TALKS
    # ---------------------------------------------------------
    {
        "slug": "casual-talks",
        "title": "Casual Talks",
        "description": "Effortless small talk, catching up with friends, debating movies, social media, and sharing stories.",
        "icon": "MessageCircle",
        "order_index": 6,
        "units": [
            {
                "slug": "small-talk",
                "title": "Small Talk",
                "description": "Start spontaneous conversations at bus stops, coffee shops, conferences, and parties.",
                "order_index": 1,
                "sessions": [
                    {
                        "slug": "meeting-someone-new",
                        "title": "Meeting Someone New at a Coffee Shop",
                        "description": "Start a casual, warm chat with a neighbor at a cozy cafe counter.",
                        "difficulty": "Elementary",
                        "cefr_level": "A2",
                        "scenario": "You are waiting for your beverage order at a cafe and start chatting with the person beside you.",
                        "ai_role": "Friendly Cafe Visitor (Divya)",
                        "user_role": "Cafe customer",
                        "learning_objectives": [
                            "Open a conversation with a pleasant situational remark",
                            "Ask open-ended questions about coffee, weather, or neighborhood",
                            "Keep conversation balanced and warm"
                        ],
                        "allowed_topics": ["coffee/tea", "cafe atmosphere", "work from cafe", "weather", "music playing"],
                        "forbidden_topics": ["invasive personal questions", "politics"],
                        "conversation_stages": [
                            "1. Casual Icebreaker",
                            "2. Sharing Drink Preferences",
                            "3. Talking About What Brought You to the Cafe",
                            "4. Pleasant Farewell"
                        ],
                        "opening_message": "The aroma of freshly brewed coffee here is amazing, isn't it? Have you tried their hazelnut cappuccino before?",
                        "completion_conditions": ["User shared beverage taste", "User exchanged friendly remarks"],
                        "suggested_vocabulary": ["aroma", "atmosphere", "cozy", "regular", "cappuccino", "unwind"],
                        "estimated_duration": 4,
                        "target_turns": 5,
                        "order_index": 1
                    }
                ]
            },
            {
                "slug": "opinions-and-stories",
                "title": "Opinions & Stories",
                "description": "Express your thoughts on technology, cinema, social media trends, and storytelling.",
                "order_index": 2,
                "sessions": [
                    {
                        "slug": "discussing-movies",
                        "title": "Discussing a Movie You Watched",
                        "description": "Share your review of a recent blockbuster, plot twists, acting, and music score.",
                        "difficulty": "Intermediate",
                        "cefr_level": "B1",
                        "scenario": "You and a friend just watched an exciting new sci-fi / drama thriller film.",
                        "ai_role": "Movie Enthusiast Friend (Karthik)",
                        "user_role": "Friend sharing movie review",
                        "learning_objectives": [
                            "Use evaluative adjectives (gripping, predictable, phenomenal, lackluster)",
                            "Explain plot highlights without giving away major spoilers",
                            "Defend your rating with specific scenes"
                        ],
                        "allowed_topics": ["plot", "cinematography", "acting", "director", "soundtrack", "climax"],
                        "forbidden_topics": ["unrelated politics", "piracy download sites"],
                        "conversation_stages": [
                            "1. Initial Reaction & Rating",
                            "2. Discussing Best & Weakest Scenes",
                            "3. Acting and Background Score",
                            "4. Recommendation to Others"
                        ],
                        "opening_message": "Wow, what an ending! I really didn't see that twist coming. What did you think of the film overall?",
                        "completion_conditions": ["User expressed rating/reaction", "User highlighted specific scene or character"],
                        "suggested_vocabulary": ["gripping", "plot twist", "cinematography", "soundtrack", "performance", "underrated"],
                        "estimated_duration": 5,
                        "target_turns": 6,
                        "order_index": 1
                    }
                ]
            }
        ]
    },

    # ---------------------------------------------------------
    # GENRE 7: PROFESSIONAL TALKS
    # ---------------------------------------------------------
    {
        "slug": "professional-talks",
        "title": "Professional Talks",
        "description": "Workplace standups, status updates, client communication, negotiating deadlines, and manager 1-on-1s.",
        "icon": "Briefcase",
        "order_index": 7,
        "units": [
            {
                "slug": "workplace-basics",
                "title": "Workplace Basics",
                "description": "Introduce yourself on your first day at work, talk to desk neighbors, and ask for assistance.",
                "order_index": 1,
                "sessions": [
                    {
                        "slug": "introducing-yourself-at-work",
                        "title": "Introducing Yourself on Your First Day at Work",
                        "description": "Introduce yourself to your team lead and colleagues on day one at the office.",
                        "difficulty": "Intermediate",
                        "cefr_level": "B1",
                        "scenario": "It is your first morning at a new tech / business firm. Your team manager introduces you to the squad.",
                        "ai_role": "Engineering Manager / Team Lead (Soundarya)",
                        "user_role": "New joiner / Software Analyst",
                        "learning_objectives": [
                            "Introduce previous background and current designated role",
                            "Express enthusiasm to collaborate with the team",
                            "Ask a proactive question regarding onboarding setup"
                        ],
                        "allowed_topics": ["designation", "previous domain", "team role", "tools & technologies", "onboarding wiki"],
                        "forbidden_topics": ["previous company confidential IP", "unrelated chatter"],
                        "conversation_stages": [
                            "1. Manager Welcome & Team Introduction",
                            "2. Your Background & Role Overview",
                            "3. Tech Stack & Collaboration Tools",
                            "4. Onboarding Checklist & Initial Goals"
                        ],
                        "opening_message": "Welcome to the team! Everyone, this is our new colleague joining us today. Would you like to introduce yourself and share a bit about what you'll be working on?",
                        "completion_conditions": ["User shared their role and background", "User expressed excitement to collaborate"],
                        "suggested_vocabulary": ["onboarding", "collaborate", "deliverables", "tech stack", "initiative", "alignment"],
                        "estimated_duration": 5,
                        "target_turns": 5,
                        "order_index": 1
                    }
                ]
            },
            {
                "slug": "meetings",
                "title": "Meetings & Updates",
                "description": "Daily standups, progress reporting, asking clarification questions, agreeing, and disagreeing diplomatically.",
                "order_index": 2,
                "sessions": [
                    {
                        "slug": "giving-a-status-update",
                        "title": "Giving a Standup Status Update",
                        "description": "Deliver a concise 3-part standup update: what you did yesterday, what you are doing today, any blockers.",
                        "difficulty": "Upper Intermediate",
                        "cefr_level": "B2",
                        "scenario": "You are in the morning 15-minute Agile standup meeting. The Scrum Master passes the mic to you.",
                        "ai_role": "Scrum Master (Karthik)",
                        "user_role": "Software Developer / Project Contributor",
                        "learning_objectives": [
                            "Structure update clearly (Yesterday, Today, Blockers)",
                            "Use precise professional verbs (implemented, refactored, resolved, investigated)",
                            "Highlight dependencies and timeline impact"
                        ],
                        "allowed_topics": ["tasks completed", "current sprint tickets", "blockers", "code reviews", "deployment"],
                        "forbidden_topics": ["lengthy technical debugging in standup", "unrelated topics"],
                        "conversation_stages": [
                            "1. Scrum Master Passing Turn",
                            "2. Delivering Yesterday & Today Progress",
                            "3. Highlighting Blockers or Dependencies",
                            "4. Scrum Master Follow-up & Next Action"
                        ],
                        "opening_message": "Thanks everyone. Next up on the sprint board is you — could you give us a quick update on the authentication module and if you have any blockers?",
                        "completion_conditions": ["User gave structured update", "User addressed blockers/timeline"],
                        "suggested_vocabulary": ["standup", "sprint ticket", "blocker", "implemented", "code review", "dependency"],
                        "estimated_duration": 5,
                        "target_turns": 5,
                        "order_index": 1
                    },
                    {
                        "slug": "politely-disagreeing",
                        "title": "Politely Disagreeing in a Meeting",
                        "description": "Offer an alternative perspective tactfully using diplomatic language ('I see your point, but perhaps...')",
                        "difficulty": "Advanced",
                        "cefr_level": "C1",
                        "scenario": "During a product strategy meeting, a colleague proposes rushing a release without automated tests.",
                        "ai_role": "Product Manager (Aravind)",
                        "user_role": "Senior Quality & Tech Lead",
                        "learning_objectives": [
                            "Use hedging and softening phrases ('With respect', 'While I understand the deadline, another factor is...')",
                            "State technical risks clearly with evidence",
                            "Propose a balanced win-win compromise"
                        ],
                        "allowed_topics": ["release deadlines", "test coverage", "technical debt", "user experience", "compromise solution"],
                        "forbidden_topics": ["personal insults", "unprofessional hostility"],
                        "conversation_stages": [
                            "1. PM Proposing Immediate Launch",
                            "2. Diplomatic Expression of Concern",
                            "3. Providing Technical Justification",
                            "4. Proposing Phased Rollout Solution",
                            "5. Consensus Agreement"
                        ],
                        "opening_message": "I really think we should push the release to production tonight and skip writing unit tests for now to meet the client deadline. What do you think?",
                        "completion_conditions": ["User voiced polite disagreement", "User offered structured alternative"],
                        "suggested_vocabulary": ["diplomatically", "technical debt", "mitigate risk", "phased rollout", "contingency", "compromise"],
                        "estimated_duration": 6,
                        "target_turns": 6,
                        "order_index": 2
                    }
                ]
            },
            {
                "slug": "workplace-problems",
                "title": "Workplace Problems",
                "description": "Discuss deadline extensions, report unexpected roadblocks, explain mistakes, and find solutions.",
                "order_index": 3,
                "sessions": [
                    {
                        "slug": "asking-for-more-time",
                        "title": "Asking for a Deadline Extension",
                        "description": "Speak to your project manager professionally to explain unforeseen delays and request 3 extra days.",
                        "difficulty": "Upper Intermediate",
                        "cefr_level": "B2",
                        "scenario": "A third-party API outage delayed your deliverable. You meet your manager to request a realistic timeline adjustment.",
                        "ai_role": "Project Manager (Harish)",
                        "user_role": "Team Lead / Analyst",
                        "learning_objectives": [
                            "Acknowledge the commitment professionally",
                            "Explain root cause objectively without sounding defensive",
                            "Offer revised timeline and mitigation plan"
                        ],
                        "allowed_topics": ["deadline extension", "root cause", "third-party delay", "revised milestone", "quality assurance"],
                        "forbidden_topics": ["complaining about colleagues", "unrelated excuses"],
                        "conversation_stages": [
                            "1. Meeting Initiation",
                            "2. Explaining the Unforeseen Roadblock",
                            "3. Proposing Adjusted Milestone Date",
                            "4. Manager Agreement & Risk Mitigation"
                        ],
                        "opening_message": "Hi, you wanted to discuss the Friday deliverable schedule? How is the implementation tracking?",
                        "completion_conditions": ["User explained the roadblock", "User requested realistic extension with new target date"],
                        "suggested_vocabulary": ["unforeseen", "timeline adjustment", "mitigate", "deliverable", "root cause", "milestone"],
                        "estimated_duration": 5,
                        "target_turns": 5,
                        "order_index": 1
                    }
                ]
            }
        ]
    }
]


def seed_curriculum(db: DBSession) -> None:
    """
    Idempotent seeding function.
    Iterates through all genres, units, and sessions.
    If a record exists by slug, it updates it. Otherwise, it creates it.
    Guarantees no duplicate records.
    """
    print("[Seed] Seeding complete 7-Genre Angiyam Curriculum...")
    
    total_genres = 0
    total_units = 0
    total_sessions = 0

    for g_data in CURRICULUM_DATA:
        genre = db.query(Genre).filter(Genre.slug == g_data["slug"]).first()
        if not genre:
            genre = Genre(
                slug=g_data["slug"],
                title=g_data["title"],
                description=g_data["description"],
                icon=g_data.get("icon"),
                order_index=g_data["order_index"]
            )
            db.add(genre)
            db.flush()
        else:
            genre.title = g_data["title"]
            genre.description = g_data["description"]
            genre.icon = g_data.get("icon")
            genre.order_index = g_data["order_index"]
            db.flush()
        total_genres += 1

        for u_data in g_data.get("units", []):
            unit = db.query(Unit).filter(Unit.genre_id == genre.id, Unit.slug == u_data["slug"]).first()
            if not unit:
                unit = Unit(
                    genre_id=genre.id,
                    slug=u_data["slug"],
                    title=u_data["title"],
                    description=u_data["description"],
                    order_index=u_data["order_index"]
                )
                db.add(unit)
                db.flush()
            else:
                unit.title = u_data["title"]
                unit.description = u_data["description"]
                unit.order_index = u_data["order_index"]
                db.flush()
            total_units += 1

            for s_data in u_data.get("sessions", []):
                session = db.query(Session).filter(Session.unit_id == unit.id, Session.slug == s_data["slug"]).first()
                if not session:
                    session = Session(
                        unit_id=unit.id,
                        genre_id=genre.id,
                        slug=s_data["slug"],
                        title=s_data["title"],
                        description=s_data["description"],
                        difficulty=s_data.get("difficulty", "Intermediate"),
                        cefr_level=s_data.get("cefr_level", "B1"),
                        scenario=s_data["scenario"],
                        ai_role=s_data["ai_role"],
                        user_role=s_data["user_role"],
                        learning_objectives=s_data.get("learning_objectives", []),
                        allowed_topics=s_data.get("allowed_topics", []),
                        forbidden_topics=s_data.get("forbidden_topics", []),
                        conversation_stages=s_data.get("conversation_stages", []),
                        opening_message=s_data["opening_message"],
                        completion_conditions=s_data.get("completion_conditions", []),
                        suggested_vocabulary=s_data.get("suggested_vocabulary", []),
                        estimated_duration=s_data.get("estimated_duration", 5),
                        target_turns=s_data.get("target_turns", 6),
                        order_index=s_data.get("order_index", 0)
                    )
                    db.add(session)
                    db.flush()
                else:
                    session.title = s_data["title"]
                    session.description = s_data["description"]
                    session.difficulty = s_data.get("difficulty", "Intermediate")
                    session.cefr_level = s_data.get("cefr_level", "B1")
                    session.scenario = s_data["scenario"]
                    session.ai_role = s_data["ai_role"]
                    session.user_role = s_data["user_role"]
                    session.learning_objectives = s_data.get("learning_objectives", [])
                    session.allowed_topics = s_data.get("allowed_topics", [])
                    session.forbidden_topics = s_data.get("forbidden_topics", [])
                    session.conversation_stages = s_data.get("conversation_stages", [])
                    session.opening_message = s_data["opening_message"]
                    session.completion_conditions = s_data.get("completion_conditions", [])
                    session.suggested_vocabulary = s_data.get("suggested_vocabulary", [])
                    session.estimated_duration = s_data.get("estimated_duration", 5)
                    session.target_turns = s_data.get("target_turns", 6)
                    session.order_index = s_data.get("order_index", 0)
                    db.flush()
                total_sessions += 1

    db.commit()
    print(f"[Seed] Successfully seeded {total_genres} Genres, {total_units} Units, and {total_sessions} Sessions!")
