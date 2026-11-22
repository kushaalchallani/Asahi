"""
Mission library for Asahi mental wellness application.

Contains 70 diverse missions across 12 categories, designed to be:
- Achievable and optional
- Appropriate for various energy levels
- Suitable for different mood states
- Diverse in purpose and type

Each mission has distinct purpose, no duplicates or near-duplicates.
"""
from core.database import SessionLocal
from models import Mission


# Define all missions with their attributes

# =============================================================================
# EMOTIONAL REGULATION (Missions that help manage stress/anxiety)
# =============================================================================
regulation_missions = [
    Mission(
        title="Do a 4-7-8 breathing exercise",
        description="Breathe in through your nose for 4 counts, hold for 7 counts, exhale through your mouth for 8 counts. Repeat 3-4 cycles when feeling tense.",
        category="regulation",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Name 5 things you hear right now",
        description="Look around and silently identify 5 distinct sounds. Let each sound come and go without judgment. This grounds you in the present moment.",
        category="regulation",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Take 3 slow deep breaths",
        description="Pause wherever you are. Place one hand on your chest and one on your belly. Breathe in for 4 counts, exhale for 6 counts. Feel your belly rise and fall.",
        category="regulation",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Do a body scan from feet to head",
        description="Close your eyes and slowly bring attention to each body part from your toes up to your head. Notice sensations without trying to change them. 2-3 minutes.",
        category="regulation",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Practice progressive muscle relaxation",
        description="Tense each muscle group for 3 seconds (feet, calves, thighs, abdomen, hands, arms, shoulders, face), then release. Move slowly up your body.",
        category="regulation",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Count backwards from 100 by threes",
        description="Start at 100 and count down by subtracting 3 each time (100, 97, 94...). Focus only on the numbers. Do 10-15 counts.",
        category="regulation",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Wrap yourself in a soft blanket",
        description="Find a blanket you like. Wrap it loosely around yourself. Sit or lie down and notice the feeling of security and warmth.",
        category="regulation",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Do gentle neck stretches",
        description="Sit or stand. Gently tilt your head toward each shoulder, holding 10 seconds. Rotate slowly left and right. Stop if you feel pain.",
        category="regulation",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
]

# =============================================================================
# MINDFULNESS (Present-moment awareness practices)
# =============================================================================
mindfulness_missions = [
    Mission(
        title="Mindfully drink one cup of water",
        description="Pour a glass of water. Notice its temperature, the sound of pouring, the weight of the glass. Take small sips, feeling each one.",
        category="reflection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Notice 3 colors in your surroundings",
        description="Look around the room or space you're in. Identify three distinct colors. Observe them without labeling or judging them.",
        category="reflection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Set a 2-minute timer and simply be",
        description="Close your eyes or soften your gaze. Let your attention rest naturally. When thoughts arise, notice them and gently return to stillness.",
        category="reflection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Practice mindful walking for 5 minutes",
        description="Walk slowly indoors or outdoors. With each step, notice the sensation of your foot touching the ground. Match your pace to your breath.",
        category="reflection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Listen to one song with full attention",
        description="Find a song you know well. Listen without doing anything else. Notice instruments, vocals, and how the song builds. Let yourself be moved by it.",
        category="reflection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
]

# =============================================================================
# SELF-REFLECTION (Introspection and personal insight)
# =============================================================================
self_reflection_missions = [
    Mission(
        title="Write one sentence about today",
        description="In a notebook or phone note, write exactly one sentence describing one meaningful moment, feeling, or observation from today.",
        category="reflection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="List 3 things you're looking forward to this week",
        description="Think about the next 7 days. Name 3 specific things, big or small, that you feel positively about or anticipate.",
        category="reflection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Write down what went well today",
        description="Even small things count. Think of one moment, interaction, or realization from today that went positively. Write it down in detail.",
        category="reflection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Identify one thing you did well today",
        description="Think of any action you took today - big or small. Name one thing you feel proud of or that you handled well. Write it down.",
        category="reflection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Describe a moment that made you smile",
        description="Think of any moment today or recently that brought you joy or a smile. Describe the scene, feeling, or person involved.",
        category="reflection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Write down one strength you have",
        description="Think of a quality, skill, or character trait you possess. Write why this is meaningful to you. Be specific with examples.",
        category="reflection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Note one thing you're grateful for",
        description="Think of one person, thing, or experience you're grateful for. Write why it matters to you. Focus on the feeling, not the thing.",
        category="reflection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
]

# =============================================================================
# PERSONAL GROWTH (Building habits and self-awareness)
# =============================================================================
personal_growth_missions = [
    Mission(
        title="Set a micro-intention for tomorrow",
        description="Think about one small thing you'd like to try differently tomorrow. Write it as a positive intention, not a goal (e.g., 'I will notice my breath').",
        category="reflection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Try one new way to do a routine task",
        description="Pick a daily habit (brushing teeth, making coffee) and do it differently - use your non-dominant hand, do it in silence, or very slowly.",
        category="reflection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Ask yourself: What would I tell a friend in this situation?",
        description="When facing a difficult moment, pause and consider: what kind advice would you give someone close to you? Notice the difference in perspective.",
        category="reflection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Write down one value that matters to you",
        description="Think of a value that guides your decisions - kindness, creativity, growth, etc. Write a sentence about why it's important.",
        category="reflection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
]

# =============================================================================
# PRODUCTIVITY (Organizing and efficiency)
# =============================================================================
productivity_missions = [
    Mission(
        title="Clear one small physical space",
        description="Choose one small area (desk corner, vanity top, bookshelf one shelf). Remove everything, decide what stays, put items back neatly.",
        category="reflection",
        difficulty="medium",
        social_required=False,
        energy_required="medium",
    ),
    Mission(
        title="Write a quick to-do list for tomorrow",
        description="List 3-5 things you'd like to accomplish tomorrow. Keep it realistic. Include at least one self-care item.",
        category="reflection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Organize one digital folder or photo album",
        description="Choose one folder on your phone/computer with photos, documents, or downloads. Delete duplicates, rename unclear files, delete unnecessary items.",
        category="reflection",
        difficulty="medium",
        social_required=False,
        energy_required="medium",
    ),
    Mission(
        title="Prepare one healthy snack or meal element",
        description="Wash one fruit, prep vegetables for later, or make a simple sandwich. Focus on the process - washing, chopping, arranging.",
        category="self-care",
        difficulty="medium",
        social_required=False,
        energy_required="medium",
    ),
    Mission(
        title="Review and organize one page of your journal/notes",
        description="Take a page from your journal or notes. Read what's there, tear out what's not useful, fold or file what is. Do just one page.",
        category="reflection",
        difficulty="medium",
        social_required=False,
        energy_required="medium",
    ),
]

# =============================================================================
# CREATIVITY (Expressive and exploratory activities)
# =============================================================================
creativity_missions = [
    Mission(
        title="Draw one simple shape without lifting your hand",
        description="Put pen/paper or finger/screen to paper. Create one continuous line that forms a shape. Don't think about the result - just move.",
        category="reflection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Create a 3-word playlist for today's mood",
        description="Think of three words that describe your current mood. Search or make a playlist with 3 songs that match each word.",
        category="reflection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Arrange 5 objects by their colors",
        description="Find five objects nearby (books, keys, clothes, etc.). Sort them from shortest to longest wavelength of color you see.",
        category="reflection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Write a postcard to your future self",
        description="Imagine receiving this message in 6 months. What advice, hope, or celebration would you want to share? Keep it brief and genuine.",
        category="reflection",
        difficulty="medium",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Create a 60-second mood photo",
        description="Take a photo that captures how you feel right now. It doesn't need to be pretty - just a visual representation of your present moment.",
        category="reflection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Doodle in the margins of a page",
        description="Open any book or paper. Draw whatever comes to mind in the margins. No skill required - just let your hand move.",
        category="reflection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Write a silly word association chain",
        description="Write a word, then next to it write the first strange word that comes to mind. Continue for 10 links. Don't judge the connections.",
        category="reflection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
]

# =============================================================================
# PHYSICAL ACTIVITY (Movement and body care)
# =============================================================================
physical_activity_missions = [
    Mission(
        title="Do 1 minute of shoulder rolls",
        description="Sit or stand. Slowly roll your shoulders backward in a circle 5 times, then forward 5 times. Focus on the sensation of release.",
        category="reflection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Stretch one body part for 2 minutes",
        description="Choose one area: neck, back, legs, or arms. Gentle stretching - hold 30 seconds, release, repeat 3 times. Breathe into the stretch.",
        category="reflection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Do 10 wall push-ups",
        description="Stand arm's length from a wall. Place hands on wall at shoulder height. Lean forward, touch wall, then push back to start. 10 repetitions.",
        category="reflection",
        difficulty="medium",
        social_required=False,
        energy_required="medium",
    ),
    Mission(
        title="Walk to the end of your street and back",
        description="Step outside. Walk to the end of your block or driveway and return. Notice your stride, the air on your skin, sounds around you.",
        category="environment",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Do one minute of dancing",
        description="Put on any song. Move your body however feels good - sway, bounce, spin, or gesture. No mirror needed. Just move for joy.",
        category="reflection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Roll your ankles for 30 seconds",
        description="Sit or stand. Rotate each ankle in circles - 10 clockwise, 10 counter-clockwise. Feel the joints loosen and wake up.",
        category="reflection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Touch your toes or reach for your toes",
        description="Stand or sit. Try to touch your toes or reach your toes. Hold for 3 deep breaths. Don't force - just go slowly.",
        category="reflection",
        difficulty="medium",
        social_required=False,
        energy_required="medium",
    ),
    Mission(
        title="Hold a yoga pose for 2 minutes",
        description="Choose one pose - child's pose, cat-cow, or standing forward fold. Focus on breathing and sensation. No need for perfection.",
        category="reflection",
        difficulty="medium",
        social_required=False,
        energy_required="medium",
    ),
    Mission(
        title="Stretch your whole body gently",
        description="Stand up and reach high, then bend to touch toes. Roll your shoulders, stretch your neck side to side. Move slowly through full range.",
        category="reflection",
        difficulty="medium",
        social_required=False,
        energy_required="medium",
    ),
]

# =============================================================================
# OUTDOOR ACTIVITIES (Time outside, nature connection)
# =============================================================================
outdoor_missions = [
    Mission(
        title="Step outside and feel the air on your skin",
        description="Open a door or step onto a porch. Stand still and notice air temperature, humidity, or breeze. Close your eyes if helpful.",
        category="environment",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Look up at the sky for 2 minutes",
        description="Find a spot where you can see the sky (through a window is fine). Just look up. Notice clouds, light, colors, or lack thereof.",
        category="environment",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Find one natural thing you didn't notice before",
        description="Look around your immediate environment for something natural - a leaf shape, cloud pattern, tree bark texture, or bird sound.",
        category="environment",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Smell something outside",
        description="Step outside or open a window. Find one scent to notice - grass, rain on pavement, flowers, or air. Take a slow, deep sniff.",
        category="environment",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Sit on the ground or floor for 3 minutes",
        description="Find a comfortable spot on the ground. Sit with feet flat or legs crossed. Notice how your body feels supported by the earth.",
        category="environment",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Find a shadow and trace its shape",
        description="Look for a shadow on the ground or wall. Use your finger or a stick to trace its outline in the dust or dirt.",
        category="environment",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Listen for one bird sound",
        description="Find a quiet moment. Listen carefully for any bird, insect, or animal sound. Just hearing - no need to identify the species.",
        category="environment",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
]

# =============================================================================
# SOCIAL CONNECTION (Interpersonal activities)
# =============================================================================
social_missions = [
    Mission(
        title="Send a 'just thinking of you' text",
        description="Think of someone you care about. Send a brief message: 'Hey, just wanted you to know I was thinking of you today.' No need to explain why.",
        category="connection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Compliment one person today",
        description="Notice someone - cashiers, coworkers, family, friends. Offer one genuine compliment about something they choose (clothes, work, effort).",
        category="connection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Text one person asking how they're doing",
        description="Choose someone you haven't spoken to recently. Ask specifically: 'How have you been? I've been thinking of you.' Listen without fixing.",
        category="connection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Share a photo from your camera roll",
        description="Open your photos. Find one snapshot from a recent day or trip. Share it with a friend with a simple caption about why you like it.",
        category="connection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Leave a kind note for someone",
        description="Write a brief, positive note to leave where someone will find it - fridge, car, desk, or wallet. Keep it anonymous or signed simply.",
        category="connection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Call one person for 5 minutes",
        description="Pick someone you enjoy talking to. Call just to chat - no agenda needed. Catch up on their week or share something small from yours.",
        category="connection",
        difficulty="medium",
        social_required=True,
        energy_required="medium",
    ),
    Mission(
        title="Invite someone for a walk together",
        description="Reach out to a neighbor, friend, or colleague. Suggest: 'Would you like to take a walk together this week?' Be flexible on timing.",
        category="connection",
        difficulty="medium",
        social_required=True,
        energy_required="medium",
    ),
    Mission(
        title="Do a small act of service together",
        description="Invite someone to help with something small - grocery pickup, meal prep, or errand. Focus on the shared activity, not the task.",
        category="connection",
        difficulty="medium",
        social_required=True,
        energy_required="medium",
    ),
    Mission(
        title="Have coffee or tea with someone in person",
        description="Suggest meeting at a café, or bring drinks to a park bench. Keep the conversation light - no deep topics required. 20-30 minutes.",
        category="connection",
        difficulty="medium",
        social_required=True,
        energy_required="medium",
    ),
    Mission(
        title="Send a voice note instead of text",
        description="Record a 30-60 second voice message instead of typing. Share a quick thought, greeting, or song snippet with someone.",
        category="connection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Share your screen and show something interesting",
        description="Video call a friend/family. Share your screen and show them something you find interesting - a photo, article, or app.",
        category="connection",
        difficulty="medium",
        social_required=True,
        energy_required="medium",
    ),
]

# =============================================================================
# DAILY LIFE AND SELF-CARE (Routine maintenance)
# =============================================================================
self_care_missions = [
    Mission(
        title="Brush your teeth and really notice the taste",
        description="Focus fully on the minty (or other) taste of your toothpaste. Notice temperature of water, sensation of brush against gums.",
        category="self-care",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Change into clean clothes",
        description="Pick an outfit that feels good. Notice fabric against skin, the sound of zippers, the visual change. Make it something you want to wear.",
        category="self-care",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Wash your face with intention",
        description="Remove any makeup or dirt thoroughly. Cool water on cheeks. Pat dry, apply moisturizer. Feel the difference between clean and unprepared.",
        category="self-care",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Make your bed exactly the way you like",
        description="Pull sheets tight, fluff pillows, adjust blankets. Make it inviting for yourself if you get up early, or tidy if you're winding down.",
        category="self-care",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Prepare your outfit for tomorrow",
        description="Choose clothes that fit your plans and mood. Lay them out. Maybe add that item you've been wanting to wear. Reduce morning friction.",
        category="self-care",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Organize one drawer or small cabinet",
        description="Open one drawer, cabinet, or pantry. Take everything out, toss obvious trash, group like items together, return neatly.",
        category="self-care",
        difficulty="medium",
        social_required=False,
        energy_required="medium",
    ),
    Mission(
        title="Fill a glass of water and place it somewhere visible",
        description="Fill a clean glass with water. Put it where you'll see it today - desk, nightstand, kitchen counter. A small reminder to hydrate.",
        category="self-care",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Set your phone wallpaper to something uplifting",
        description="Change your phone background to a photo, quote, or image that makes you feel positively when you see it.",
        category="self-care",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Tidy one corner of a room",
        description="Pick one corner - entryway, closet, kitchen counter. Put away items, straighten things, create a small clean space.",
        category="self-care",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Take a 2-minute hygiene break",
        description="Splash cold water on your face, trim nails if needed, floss one tooth. Small acts of self-care that take almost no time.",
        category="self-care",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Do one simple meal prep for the week",
        description="Wash and chop vegetables for salads or snacks. Or hard-boil eggs, or portion oatmeal. Focus on one thing that saves time later.",
        category="self-care",
        difficulty="medium",
        social_required=False,
        energy_required="high",
    ),
    Mission(
        title="Create a simple self-care routine template",
        description="Write down a morning and evening routine with 3-5 small actions each. Include hydration, movement, and one enjoyable moment.",
        category="self-care",
        difficulty="medium",
        social_required=False,
        energy_required="medium",
    ),
]

# =============================================================================
# LEARNING AND EXPLORATION (Curiosity and growth)
# =============================================================================
learning_missions = [
    Mission(
        title="Read one page of any book",
        description="Open any book you've been meaning to read, or pick a random page in a store. Read just that one page - no pressure to continue.",
        category="reflection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Watch one educational short video (<5 min)",
        description="Find a brief documentary clip, TED-Ed video, or explainer on YouTube. Pick something that catches your interest - no commitment to learn more.",
        category="reflection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Learn one new word using a dictionary app",
        description="Open a dictionary app or website. Search for an unfamiliar word you've seen. Read definition, pronunciation, and usage examples.",
        category="reflection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Look up one recipe that sounds interesting",
        description="Open a recipe website or app. Search for something you've never cooked. Just read the ingredients and steps - no need to cook now.",
        category="reflection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Read the credits of one movie/show you enjoyed",
        description="Think of a film or show you liked. Look up who directed it, wrote it, or acted in it. Learn the names of people behind something you enjoyed.",
        category="reflection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Listen to one podcast episode about something new",
        description="Browse podcast platforms for a topic you haven't explored. Listen to the first 10 minutes of an episode - just to taste the subject.",
        category="reflection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Visit one website you've never explored before",
        description="Think of an interest - animals, history, science, art. Visit a website dedicated to it. Browse for 5-10 minutes without pressure.",
        category="reflection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Read one Wikipedia page about something random",
        description="Open Wikipedia and click 'Random article'. Read for 3-5 minutes. Let yourself be surprised by what you learn.",
        category="reflection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Learn one fact about your birth month",
        description="Search online for 'famous people born in [your birth month]' or 'historical events [your birth year]'. Discover something new.",
        category="reflection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
]

# =============================================================================
# GRATITUDE AND POSITIVE EXPERIENCES
# =============================================================================
gratitude_missions = [
    Mission(
        title="Write down what you're grateful for right now",
        description="Think of 3 specific things happening now. They can be small - a comfortable chair, a good cup of tea, or a sunny window.",
        category="reflection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Text one person something you appreciate about them",
        description="Think of one genuine quality, action, or thing you appreciate about someone. Send them a brief message saying so.",
        category="connection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Notice and acknowledge one good thing that happened",
        description="Think of one positive event, interaction, or moment from the past 24 hours. Acknowledge it silently or out loud.",
        category="reflection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Do one small thing you're proud of today",
        description="Think of a small accomplishment - finishing a task, helping someone, or just taking care of yourself. Acknowledge your effort.",
        category="reflection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Create a 'wins' list for this week",
        description="Write 3-5 things that went well or that you did well this week. Celebrate small progress without comparing to others.",
        category="reflection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
]

# =============================================================================
# CHALLENGING (High-effort personal development)
# =============================================================================
challenging_missions = [
    Mission(
        title="Plan a 7-day self-care schedule",
        description="Create a simple schedule with one self-care activity per day. Include variety: physical, mental, creative, and social options.",
        category="self-care",
        difficulty="challenging",
        social_required=False,
        energy_required="medium",
    ),
    Mission(
        title="Write a 1-page reflection on your growth this year",
        description="Think of how you've changed in the past 12 months. Write about challenges you've overcome, skills you've built, and lessons learned.",
        category="reflection",
        difficulty="challenging",
        social_required=False,
        energy_required="medium",
    ),
    Mission(
        title="Create a 3-month mental wellness plan",
        description="Define 3 wellness goals. For each, write 1 action per month that would support it. Include how you'll track progress.",
        category="self-care",
        difficulty="challenging",
        social_required=False,
        energy_required="high",
    ),
    Mission(
        title="Plan a meaningful social gathering",
        description="Choose 2-4 people you'd like to connect with. Plan a simple activity - potluck, game night, or walk. Send invitations.",
        category="connection",
        difficulty="challenging",
        social_required=True,
        energy_required="high",
    ),
    Mission(
        title="Research and pick a new hobby to explore",
        description="Spend 30 minutes researching 3 hobbies that interest you. Pick one to try for 2 weeks. Gather what you need to start.",
        category="reflection",
        difficulty="challenging",
        social_required=False,
        energy_required="medium",
    ),
]


# Combine all missions
missions = (
    regulation_missions +
    mindfulness_missions +
    self_reflection_missions +
    personal_growth_missions +
    productivity_missions +
    creativity_missions +
    physical_activity_missions +
    outdoor_missions +
    social_missions +
    self_care_missions +
    learning_missions +
    gratitude_missions +
    challenging_missions
)


def seed_missions():
    """Seed the database with all missions, skipping duplicates."""
    db = SessionLocal()
    added_count = 0

    try:
        for mission in missions:
            existing = (
                db.query(Mission)
                .filter(Mission.title == mission.title)
                .first()
            )

            if not existing:
                db.add(mission)
                added_count += 1

        db.commit()

        print(f"Added {added_count} new missions out of {len(missions)} total.")

    finally:
        db.close()


if __name__ == "__main__":
    seed_missions()