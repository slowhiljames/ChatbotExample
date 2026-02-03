=================================================
APS NATURALS CHATBOT - README
=================================================

DESCRIPTION:
-----------
This is an AI-powered chatbot that answers questions about APS Naturals 
products using a trained neural network model. It uses TF-IDF vectorization 
and a deep learning model to understand user queries and provide relevant 
answers from the dataset.

FILES:
------
- chatbot.py         : Main chatbot interface (run this to chat)
- train.py           : Script to train the model
- model.py           : Neural network architecture
- preprocessing.py   : Text cleaning and preprocessing
- vectorizer.py      : Dataset loading and vectorization
- utils.py           : Utility functions (currently empty)
- requirements.txt   : Required Python packages
- dataset/           : Folder containing Q&A dataset

SETUP INSTRUCTIONS:
-------------------
1. Install Python (3.8 or higher recommended)

2. Install required packages:
   pip install -r requirements.txt

3. Train the model (first time only):
   python train.py
   
   This will create three files:
   - qa_model.h5      : Trained neural network model
   - vectorizer.pkl   : TF-IDF vectorizer
   - answers.pkl      : Answer mappings

4. Run the chatbot:
   python chatbot.py

USAGE:
------
Once the chatbot starts, simply type your questions about APS Naturals:

Example:
  You: What is APS Naturals?
  Bot: APS Naturals is a brand that provides natural and organic 
       products focused on health, wellness, and sustainability.

Type 'exit', 'quit', or 'bye' to stop the chatbot.

FEATURES:
---------
✓ Natural language processing with text cleaning
✓ TF-IDF vectorization for question matching
✓ Deep neural network for answer prediction
✓ Error handling and input validation
✓ Confidence-based responses
✓ User-friendly interface

TROUBLESHOOTING:
----------------
Q: Error "Model file not found"
A: Run 'python train.py' first to train the model

Q: NLTK stopwords error
A: The code will automatically download stopwords on first run

Q: Low-quality responses
A: You can increase training epochs in train.py or add more data 
   to the dataset

CUSTOMIZATION:
--------------
To add more Q&A pairs:
1. Edit dataset/apsnaturals_qa_dataset.txt
2. Add questions and answers in this format:
   Question: Your question here?
   Answer: Your answer here.
   
   (Leave a blank line between Q&A pairs)
3. Re-run: python train.py
4. Start chatbot: python chatbot.py

To modify model architecture:
- Edit model.py to change layers, neurons, or activation functions
- Re-train the model after changes

=================================================
Created: January 2026
=================================================
