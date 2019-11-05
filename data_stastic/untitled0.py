#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 17:46:41 2019

@author: xue
"""

import spacy
import en_core_web_sm

nlp = en_core_web_sm.load()
doc = nlp("The bread is top notch as well. I love you")
#print(doc)
print(doc.noun_chunks.__sizeof__())
for ent in doc.noun_chunks:
    print("A")
    print(ent)
doc = nlp("and")
print([(token.text, token.tag_) for token in doc])