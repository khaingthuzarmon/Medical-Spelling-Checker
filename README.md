# Medical Spell Checker

A Streamlit web application for checking spelling in medical texts using edit distance algorithms.

## Features

- ✅ Real-time spell checking for medical terminology
- ✅ Edit distance-based correction suggestions
- ✅ Medical dictionary search functionality
- ✅ Clean, user-friendly interface

## Demo

🚀 **Live Demo:** [Your App URL will be here]

## Local Development

1. Clone this repository:
```bash
git clone https://github.com/yourusername/medical-spell-checker.git
cd medical-spell-checker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run streamlit_app.py
```

## Deployment

This app is deployed on Streamlit Cloud. Any pushes to the main branch will automatically update the live demo.

## Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Algorithm**: Levenshtein Distance
- **Data**: Pandas DataFrames

## How It Works

1. **Text Processing**: Cleans input text and tokenizes words
2. **Dictionary Lookup**: Checks words against medical vocabulary
3. **Error Detection**: Identifies misspelled words
4. **Candidate Generation**: Uses edit distance to find similar words
5. **Ranking**: Suggests corrections based on frequency and similarity

## Sample Usage

Try these examples:
- "The pateint has diabetis" → "The patient has diabetes"
- "Doctr prescribed medicne" → "Doctor prescribed medicine"
- "Clincal study results" → "Clinical study results"

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License
