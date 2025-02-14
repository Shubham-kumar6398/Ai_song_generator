# book_summary = "This fantasy novel follows Kvothe, a gifted young man with a tragic past, as he rises from a child performer to a legendary figure. The story is told in two timelines: Kvothe, now a quiet innkeeper, recounts his life to a chronicler.As a boy, Kvothe’s family, who were traveling performers, are slaughtered by the mysterious Chandrian, a group of mythical beings feared across the world. Left orphaned, he survives on the streets before making his way to the prestigious University, where he studies magic, music, and alchemy. Kvothe's genius helps him rise quickly, but his fiery temper and recklessness lead him into constant conflict with powerful figures.Throughout his journey, Kvothe searches for the truth behind the Chandrian while dealing with enemies, romance, and financial struggles. His talent for music and magic makes him famous, but he also attracts danger.The book is a beautifully written mix of adventure, mystery, and myth, making it a beloved classic of modern fantasy."
import streamlit as st
import cohere

# Initialize Cohere API
COHERE_API_KEY = "r9uX1zwVave9HWB9FoY4AITKVd12BefKQ3hVWfw5"
co = cohere.Client(COHERE_API_KEY)


def generate_lyrics(book_summary, genre):
    prompt = (
        f"Write a complete song based on this book summary: {book_summary}. "
        f"The song should follow the {genre} style. Ensure that all verses, chorus, "
        f"and bridge are complete and do not end mid-line. Use the following format:\n\n"
        "Verse 1:\n[Complete lyrics here]\n\n"
        "Chorus:\n[Complete lyrics here]\n\n"
        "Verse 2:\n[Complete lyrics here]\n\n"
        "Bridge:\n[Complete lyrics here]\n\n"
        "Chorus:\n[Repeat with variations]\n\n"
        "Outro:\n[Closing lyrics that provide a satisfying ending]"
    )
    
    response = co.generate(
        model="command-xlarge-nightly",
        prompt=prompt,
        max_tokens=1000,  # Increased to avoid cutoff
        temperature=0.8,   # Makes lyrics more creative
        # stop_sequences=["Outro:"]  # Ensures proper stopping point
    )
    
    return response.generations[0].text.strip()

# Streamlit UI
st.title("AI Song Lyrics Generator 🎶")
book_summary = st.text_area("Enter a book summary:")
genre = st.selectbox("Select Genre", ["Pop", "Rock", "Jazz", "Hip-Hop", "Classical"])

if st.button("Generate Lyrics"):
    if book_summary:
        lyrics = generate_lyrics(book_summary, genre)
        st.text_area("Generated Lyrics", lyrics, height=300)
    else:
        st.warning("Please enter a book summary.")

# Verse 1:
# In the realm of fantasy, a tale unfolds,
# A young Kvothe, gifted but scarred, his story's told,
# From the ashes of tragedy, he rose like a phoenix,
# A performer's child, now a legend, his journey's complex.

# Chorus:
# The Chandrian's curse, a mystery unsolved,
# From the streets to the University, his path evolved,
# Magic and music, his weapons, his shield,
# Kvothe's legacy, a story worth revealing.

# Verse 2:
# A family's loss, the Chandrian's deadly game,
# Left young Kvothe alone, a name he had to claim,
# The University's halls, his knowledge grew,
# But his temper, a fire, kept him in constant view.
# He fought the powers, his recklessness a charm,
# His talent for magic and melody, a rising storm.

# Bridge:
# In search of the truth, he wandered far and wide,
# A legend in the making, with enemies to hide,
# Love and loss, he faced them all,
# His journey's a ballad, a story to enthrall.

# Chorus:
# (The Chronicler's pen) writes his tale, a captivating scroll,
# Kvothe's life, a symphony, with secrets to unfold,
# The Chandrian's shadow, a haunting melody,
# His rise and struggle, a hip-hop fantasy.

# Outro:
# From the ashes, a hero emerges, a star,
# Kvothe's legacy, a timeless, magical scar,
# His story, a rhythm, a captivating beat,
# A fantasy classic, a masterpiece complete.