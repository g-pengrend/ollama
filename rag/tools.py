from nltk.tokenize import sent_tokenize, word_tokenize

def chunker(text, max_words_per_chunk=100):
  """
  Splits the input text into overlapping chunks of words up to the max per chunk
  Returns:
    list of chunks which are strings
  """

  sentences = sent_tokenize(text)
  chunks = []
  current_chunk = []

  for sentence in sentences:
    
      words = word_tokenize(sentence)

      if len(current_chunk) + len(words) <= max_words_per_chunk:
          current_chunk.extend(words)
      else:
          chunks.append(' '.join(current_chunk))
          current_chunk = words

  # Add the last chunk if it's not empty
  if current_chunk:
      chunks.append(' '.join(current_chunk))

  overlapping_chunks = []
  for i in range(len(chunks)):
      chunk_start = max(0, i - 1)
      chunk_end = i + 1
      overlapping_chunk = ' '.join(chunks[chunk_start:chunk_end])
      overlapping_chunks.append(overlapping_chunk)

  return overlapping_chunks

from typing import List

def chunk_text_by_sentences(source_text: str, sentences_per_chunk: int, overlap: int) -> List[str]:
    """
    Splits text by sentences
    """
    if sentences_per_chunk < 2:
        raise ValueError("The number of sentences per chunk must be 2 or more.")
    if overlap < 0 or overlap >= sentences_per_chunk - 1:
        raise ValueError("Overlap must be 0 or more and less than the number of sentences per chunk.")
    
    sentences = sent_tokenize(source_text)
    if not sentences:
        print("Nothing to chunk")
        return []
    
    chunks = []
    i = 0
    while i < len(sentences):
        end = min(i + sentences_per_chunk, len(sentences))
        chunk = sentences[i:end]
        
        if overlap > 0 and i > 1:
            overlap_start = max(0, i - overlap)
            chunk = sentences[overlap_start:end]
        
        chunks.append(' '.join(chunk))
        i += sentences_per_chunk - overlap
    
    return chunks

def chunk_text_by_words(source_text: str, words_per_chunk: int, overlap: int) -> List[str]:
    """
    Splits text into chunks by words with overlap.
    """
    if words_per_chunk < 2:
        raise ValueError("The number of sentences per chunk must be 2 or more.")
    if overlap < 0 or overlap >= words_per_chunk - 1:
        raise ValueError("Overlap must be 0 or more and less than the number of sentences per chunk.")
    
    words = word_tokenize(source_text)
    if not words:
        print("Nothing to chunk")
        return []
    
    chunks = []
    i = 0
    while i < len(words):
        end = min(i + words_per_chunk, len(words))
        chunk = words[i:end]
        
        if overlap > 0 and i != 0:
            overlap_start = max(0, i - overlap)
            chunk = words[overlap_start:end]
        
        chunks.append(' '.join(chunk))
        i += words_per_chunk - overlap
    
    return chunks