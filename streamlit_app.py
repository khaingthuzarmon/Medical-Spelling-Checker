import streamlit as st
import pandas as pd
import re
from collections import Counter

# Set page config
st.set_page_config(
    page_title="Medical Spell Checker",
    page_icon="🏥",
    layout="wide"
)

@st.cache_data
def load_sample_dictionary():
    """Create a sample medical dictionary for demo purposes"""
    # Sample medical words with frequencies (you'll replace this with your actual data)
    sample_words = [
        ('patient', 15000), ('patients', 12000), ('treatment', 8000), 
        ('medical', 7000), ('study', 6500), ('disease', 5000),
        ('cancer', 4500), ('diabetes', 4000), ('therapy', 3500),
        ('clinical', 3000), ('diagnosis', 2800), ('symptoms', 2500),
        ('hospital', 2200), ('doctor', 2000), ('medicine', 1800),
        ('surgery', 1600), ('infection', 1400), ('health', 1200),
        ('blood', 1100), ('heart', 1000), ('brain', 900),
        ('liver', 800), ('kidney', 750), ('lung', 700)
    ]
    
    df = pd.DataFrame(sample_words, columns=['word', 'frequency'])
    return df

def levenshtein_distance(word1, word2):
    """Calculate edit distance between two words"""
    len1, len2 = len(word1), len(word2)
    matrix = [[0] * (len2 + 1) for _ in range(len1 + 1)]
    
    for i in range(len1 + 1):
        matrix[i][0] = i
    for j in range(len2 + 1):
        matrix[0][j] = j
    
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            cost = 0 if word1[i-1] == word2[j-1] else 1
            matrix[i][j] = min(
                matrix[i-1][j] + 1,      # deletion
                matrix[i][j-1] + 1,      # insertion
                matrix[i-1][j-1] + cost  # substitution
            )
    
    return matrix[len1][len2]

def generate_candidates(word, word_dict_df, max_distance=2):
    """Generate spelling correction candidates"""
    candidates = []
    dict_words = word_dict_df['word'].tolist()
    
    for dict_word in dict_words:
        distance = levenshtein_distance(word.lower(), dict_word.lower())
        if distance <= max_distance and distance > 0:
            frequency = word_dict_df[word_dict_df['word'] == dict_word]['frequency'].iloc[0]
            candidates.append({
                'word': dict_word,
                'distance': distance,
                'frequency': frequency
            })
    
    candidates.sort(key=lambda x: (x['distance'], -x['frequency']))
    return candidates[:5]

class SimpleSpellChecker:
    def __init__(self, word_dict_df):
        self.word_dict = word_dict_df
        self.vocab = set(word_dict_df['word'].str.lower().tolist())
    
    def is_word_in_dictionary(self, word):
        return word.lower() in self.vocab
    
    def check_spelling(self, text):
        """Check spelling and return errors with suggestions"""
        # Simple text cleaning
        text = re.sub(r'[^\w\s]', ' ', text)
        words = text.lower().split()
        errors = []
        
        for i, word in enumerate(words):
            if word and not self.is_word_in_dictionary(word):
                candidates = generate_candidates(word, self.word_dict)
                if candidates:  # Only add if we have suggestions
                    errors.append({
                        'position': i,
                        'word': word,
                        'suggestions': candidates
                    })
        
        return errors

def main():
    # Load dictionary
    word_dict = load_sample_dictionary()
    spell_checker = SimpleSpellChecker(word_dict)
    
    # App header
    st.title("🏥 Medical Spell Checker")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("📚 Dictionary Info")
        st.metric("Total Words", len(word_dict))
        st.metric("Most Common", word_dict.iloc[0]['word'])
        
        st.subheader("Search Dictionary")
        search_term = st.text_input("Search for a word:")
        if search_term:
            matches = word_dict[word_dict['word'].str.contains(search_term.lower(), case=False)]
            if not matches.empty:
                st.write("**Matches found:**")
                for _, row in matches.head(5).iterrows():
                    st.write(f"• {row['word']} ({row['frequency']:,})")
            else:
                st.write("No matches found")
    
    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Enter Medical Text")
        user_text = st.text_area(
            "Text to check:",
            height=150,
            placeholder="Enter your medical text here... (e.g., 'The pateint has diabetis and needs treatmnt')",
            help="Enter medical text to check for spelling errors"
        )
        
        if st.button("🔍 Check Spelling", type="primary"):
            if user_text.strip():
                with st.spinner("Checking spelling..."):
                    errors = spell_checker.check_spelling(user_text)
                
                if errors:
                    st.error(f"Found {len(errors)} spelling error(s)")
                    
                    for error in errors:
                        st.write(f"**Error:** `{error['word']}`")
                        suggestions = [s['word'] for s in error['suggestions'][:3]]
                        if suggestions:
                            st.write(f"**Suggestions:** {', '.join(suggestions)}")
                        st.write("---")
                else:
                    st.success("✅ No spelling errors found!")
            else:
                st.warning("Please enter some text to check.")
    
    with col2:
        st.subheader("Quick Examples")
        examples = [
            "The pateint has diabetis",
            "Doctr prescribed medicne", 
            "Clincal study results",
            "Hospitl treatment plan"
        ]
        
        for example in examples:
            if st.button(f"Try: {example}", key=example):
                st.session_state.example_text = example
        
        if hasattr(st.session_state, 'example_text'):
            st.text_area("Example:", value=st.session_state.example_text, key="example_display")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "**Note:** This is a demo version with a limited medical dictionary. "
        "Upload your own dictionary for better results."
    )

if __name__ == "__main__":
    main()