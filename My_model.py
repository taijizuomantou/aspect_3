#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 14:12:37 2019
@author: xue
"""
import copy
import json
import math

import six
import torch
import torch.nn as nn
from torch.nn import CrossEntropyLoss
from torch.nn.functional import softmax
from transformers import BertTokenizer, BertModel, BertForMaskedLM
class BertForSequenceClassification(nn.Module):
    """BERT model for classification.
    This module is composed of the BERT model with a linear layer on top of
    the pooled output.
    Example usage:
    ```python
    # Already been converted into WordPiece token ids
    input_ids = torch.LongTensor([[31, 51, 99], [15, 5, 0]])
    input_mask = torch.LongTensor([[1, 1, 1], [1, 1, 0]])
    token_type_ids = torch.LongTensor([[0, 0, 1], [0, 2, 0]])
    config = BertConfig(vocab_size=32000, hidden_size=512,
        num_hidden_layers=8, num_attention_heads=6, intermediate_size=1024)
    num_labels = 2
    model = BertForSequenceClassification(config, num_labels)
    logits = model(input_ids, token_type_ids, input_mask)
    ```
    """
    def __init__(self, num_labels):
        super(BertForSequenceClassification, self).__init__()
        self.bert = BertModel.from_pretrained("./abc/")
        self.dropout = nn.Dropout(0.1)
        self.classifier_detection = nn.Linear(768, 2)
        self.classifier_sentiment = nn.Linear(768, 4)
        self.embedding = nn.Embedding(5,768)
        #self.embedding.weight.data.copy_(self.load_aspect_embedding_weight())
        self.wh_d = nn.Linear(768,768)
        self.wh_c = nn.Linear(768,768)
        self.wa_d = nn.Linear(768,768)
        self.wa_c = nn.Linear(768,768)
        self.w_d = nn.Linear(768,1)
        self.w_c = nn.Linear(768,1)
        self.softmax_d = nn.Softmax(dim=1)
        self.softmax_c = nn.Softmax(dim=1)
    def load_aspect_embedding_weight(self):
        f = open("aspect_embedding/aspect_embedding.txt","r")
        weight = []
        while True:
            line = f.readline()
            if len(line) ==0:break
            item = line.split()
            aspect = []
            for num in item:
                num = float(num)
                aspect.append(num)
            weight.append(aspect)
        myw = torch.tensor(weight,dtype = torch.float)
        return myw
    def forward(self, input_ids, token_type_ids, attention_mask, class_labels, detection_lablels,aspects):
        encode, pooled_output = self.bert(input_ids, attention_mask=attention_mask,token_type_ids= token_type_ids,)
        #print(encode.size())
        pooled_output = self.dropout(pooled_output)
        encode = self.dropout(encode)
        detection_logits = self.classifier_detection(pooled_output)
        sentiment_logits = self.classifier_sentiment(pooled_output)
        aspect_embed = self.embedding(aspects)
        aspect_embed = aspect_embed.unsqueeze(1)
        full_aspect_embed = aspect_embed.expand(-1,128,768)
        
        Md = self.wh_d(encode)+self.wa_d(full_aspect_embed)
        attention_d = self.softmax_d(self.w_d(Md))
        temp_encode = encode.permute(0,2,1)
        r_d = torch.bmm(temp_encode,attention_d).squeeze(-1)
        detection_logits = self.classifier_detection(r_d)
        
        Mc = self.wh_c(encode)+self.wa_c(full_aspect_embed)
        attention_c = self.softmax_c(self.w_c(Mc)) + attention_d
        temp_encode = encode.permute(0,2,1)
        r_c = torch.bmm(temp_encode,attention_c).squeeze(-1)
        sentiment_logits = self.classifier_sentiment(r_c)
        
      #  print(attention_d.size())
        loss_fct = CrossEntropyLoss()
        loss = loss_fct(detection_logits, detection_lablels)

        loss_fct_2 = CrossEntropyLoss(ignore_index=4)
        loss = loss + loss_fct_2(sentiment_logits,class_labels)
      #  print(attention_d.size())
        attention_d = attention_d.squeeze(-1)
#        attention_c = attention_c.squeeze(-1)
#        #print(attention_d.size())
#        #print(attention_d.permute(1,0).size())
#        
        sizee = full_aspect_embed.size(0)
#      #  print(sizee)
        attention_loss_d = 1 - torch.sum(torch.mul(attention_d,attention_d))/sizee
#        if(attention_loss_d < 0):
#            print(attention_loss_d)
#            print(attention_d)
#        attention_loss_c = 1 - torch.sum(torch.mul(attention_c,attention_c))/sizee
        #print( torch.sum(torch.mul(attention_d,attention_d)))
        loss = loss +attention_loss_d #+attention_loss_c
        return loss, detection_logits,sentiment_logits