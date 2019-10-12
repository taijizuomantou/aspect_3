#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 14:07:08 2019

@author: xue
"""
from My_model import BertForSequenceClassification
import torch
label_id = [0,1,2,3,4,4,4,1]
label_exist_id = []
    #label_classify_id = []
for label in label_id:
   if label == 4:
        label_exist_id.append(0)
   else:
        label_exist_id.append(1)
label_exist_id = torch.tensor(label_exist_id,dtype = torch.long)
print(label_exist_id)
print(label_exist_id.unsqueeze(1))
aspect_map = {}
aspect_list = ['price','anecdotes','food','ambience','service']
for (i, label) in enumerate(aspect_list):
    aspect_map[label] = i
print(aspect_map)
import torch.nn as nn
embedding = nn.Embedding(5,3)
for i in range(0,5):
    print(embedding(torch.tensor(i,dtype=torch.long)))
import numpy as np
abc = np.random.randn(4,300)
torch_abc = torch.from_numpy(abc)
torch_abc = torch_abc.unsqueeze(1)
print(torch_abc.size())
expand = torch_abc.expand(-1,512,300)
print(expand.size())
aa = np.random.randn(4,512,768)
aa = torch.from_numpy(aa)
answer = torch.cat((aa,expand),dim = -1)
print(answer.size())
aa = np.random.randn(4,512,1)
aa = torch.from_numpy(aa)
aa = aa.squeeze(-1)
print(aa.size())
a1 = [[2],[4]]

a2 = [[2,3,4],[4,5,6]]
a1 = torch.tensor(a1,dtype = torch.long)
a1 = a1.expand(2,3)
a2 = torch.tensor(a2,dtype = torch.long)
print(a1.size())
print(a2.size())
print(a1)
ans = torch.mul(a1,a2)
print(ans)
abc = np.random.randn(4,300,1)
torch_abc = torch.from_numpy(abc)
torch_abc = torch_abc.squeeze(-1)
print(torch_abc.size())
def load_aspect_embedding_weight():
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
#weight = load_aspect_embedding_weight()
#model = BertForSequenceClassification( 5)
#no_decay = ['bias', 'gamma', 'beta']
#print(model.named_parameters() )
#for n, p in model.named_parameters() :
#  #  print(n)
#  #pass
#    if any(nd in n for nd in no_decay):
#        print(n)
#optimizer_parameters = [
#     #{'params': [p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)], 'weight_decay_rate': 0.01},
#     {'params': [p for n, p in model.named_parameters() if any(nd in n for nd in no_decay)], 'weight_decay_rate': 0.0}
#     ]
#i = 0
#f = open("abc2.txt","w")
#f.write(str(optimizer_parameters))
       # import torch
x = torch.tensor([[0.3,0.7],[0.2,0.8]])
t = torch.tensor([[0.3,0.7],[0.9,0.1]])
print(torch.mul(x,x))
y = torch.sum(torch.mul(x,x)/2 ) #x.mm(x)
print(y)