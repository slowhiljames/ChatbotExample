"""
Knowledge Base Module for APS Naturals Chatbot
This module handles loading, searching, and retrieving relevant information
from the knowledge base to answer user questions dynamically.
"""

import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from preprocessing import clean_text

class KnowledgeBase:
    def __init__(self, knowledge_file="dataset/apsnaturals_qa_dataset.txt"):
        self.knowledge_file = knowledge_file
        self.sections = {}
        self.all_sentences = []
        self.section_map = []  # Maps sentence index to section name
        self.vectorizer = None
        self.sentence_vectors = None
        self.load_knowledge()
        
    def load_knowledge(self):
        """Load and parse the knowledge base file"""
        with open(self.knowledge_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse sections
        current_section = None
        for line in content.split('\n'):
            line = line.strip()
            
            # Skip comments and empty lines
            if line.startswith('#') or not line:
                continue
            
            # Check for section headers
            if line.startswith('[') and line.endswith(']'):
                current_section = line[1:-1]
                self.sections[current_section] = []
            elif current_section:
                # Add sentence to current section
                self.sections[current_section].append(line)
                self.all_sentences.append(line)
                self.section_map.append(current_section)
        
        # Create TF-IDF vectors for all sentences
        if self.all_sentences:
            self.vectorizer = TfidfVectorizer(max_features=500)
            self.sentence_vectors = self.vectorizer.fit_transform(self.all_sentences)
    
    def search(self, query, top_k=5):
        """
        Search for relevant information based on the query
        Returns top_k most relevant sentences with their sections
        """
        if not self.all_sentences:
            return []
        
        # Vectorize the query
        query_vector = self.vectorizer.transform([query])
        
        # Calculate cosine similarity
        similarities = cosine_similarity(query_vector, self.sentence_vectors)[0]
        
        # Get top_k indices
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        # Prepare results
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.1:  # Minimum similarity threshold
                results.append({
                    'text': self.all_sentences[idx],
                    'section': self.section_map[idx],
                    'score': float(similarities[idx])
                })
        
        return results
    
    def get_section(self, section_name):
        """Get all information from a specific section"""
        return self.sections.get(section_name, [])
    
    def get_relevant_context(self, query, max_sentences=5):
        """
        Get relevant context for answering a query
        Returns a formatted string with relevant information
        """
        results = self.search(query, top_k=max_sentences)
        
        if not results:
            return None
        
        # Group results by section for better context
        sections_used = {}
        for result in results:
            section = result['section']
            if section not in sections_used:
                sections_used[section] = []
            sections_used[section].append(result['text'])
        
        # Format context
        context_parts = []
        for section, sentences in sections_used.items():
            context_parts.extend(sentences)
        
        return " ".join(context_parts)
    
    def generate_answer(self, query):
        """
        Generate an answer to the query based on relevant knowledge
        """
        # Get relevant context
        results = self.search(query, top_k=5)
        
        if not results or results[0]['score'] < 0.12:
            return None, 0.0
        
        # Analyze query to determine what type of answer is needed
        query_lower = query.lower()
        
        # Check if it's a yes/no question
        is_yes_no = any(query_lower.startswith(word) for word in ['is', 'are', 'does', 'do', 'can', 'will', 'has', 'have'])
        
        # Check for specific question types
        is_what = query_lower.startswith('what') or 'what' in query_lower
        is_why = query_lower.startswith('why')
        is_how = query_lower.startswith('how')
        is_who = query_lower.startswith('who')
        is_where = query_lower.startswith('where')
        is_tell = 'tell' in query_lower or 'about' in query_lower
        
        # Get the most relevant information
        top_info = results[0]['text']
        confidence = results[0]['score']
        
        # For yes/no questions, provide affirming answer
        if is_yes_no:
            # Check if the information supports a positive answer
            if any(word in query_lower for word in ['organic', 'natural', 'safe', 'eco', 'cruelty-free', 'sustainable', 'quality']):
                answer = f"Yes, {top_info}"
            else:
                answer = top_info
        
        # For 'what' questions or 'tell me about' questions
        elif is_what or is_tell:
            # Combine multiple relevant points for richer answers
            if len(results) > 1 and confidence > 0.2:
                context_sentences = [r['text'] for r in results[:3] if r['score'] > 0.15]
                answer = " ".join(context_sentences)
            else:
                answer = top_info
        
        # For 'why' questions
        elif is_why:
            # Combine multiple relevant points
            context_sentences = [r['text'] for r in results[:3] if r['score'] > 0.15]
            answer = " ".join(context_sentences)
        
        # For 'how' questions
        elif is_how:
            context_sentences = [r['text'] for r in results[:3] if r['score'] > 0.15]
            answer = " ".join(context_sentences)
        
        # For 'who' questions
        elif is_who:
            answer = top_info
        
        # For 'where' questions
        elif is_where:
            answer = top_info
        
        # General questions - combine top results
        else:
            if len(results) > 1 and confidence > 0.2:
                context_sentences = [r['text'] for r in results[:3] if r['score'] > 0.15]
                answer = " ".join(context_sentences)
            else:
                answer = top_info
        
        return answer, confidence


# Global instance
kb = None

def get_knowledge_base():
    """Get or create the global knowledge base instance"""
    global kb
    if kb is None:
        kb = KnowledgeBase()
    return kb
