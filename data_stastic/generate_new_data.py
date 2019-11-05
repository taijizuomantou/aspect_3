import csv
import en_core_web_sm

def read_csv(input_file):
    with open(input_file, "r") as f:
            reader = csv.reader(f, delimiter="\t")
            lines = []
            for line in reader:
                lines.append(line)
            return lines
input_file = "../data/semeval2014/bert-pair/test_NLI_M.csv"
output_file = "multi_test_NLI_M2.csv"
f = open(output_file,"w")
f2 = open("temp2.txt","w")
#f3 = open("temp3.txt","w")
#f4 = open("temp4.txt","w")
#nlp = en_core_web_sm.load()
##f.write("id\tsentence1\tsentence2\tlabel\n")
lines =  read_csv(input_file)
#ans = 0
#for i in range(int(len(lines) / 5)):
#  #  i = 12
#    text = lines[i*5][3]
#    f4.write(text)
#    f4.write("\n")
#    docs = nlp(text.lower())
#    count = 0
#    temp = []
#    for item in docs.noun_chunks:
#        count += 1
#       # print(item.text)
#        temp.append(item)
#    
#    if count >= 0:ans += 1
#    
#    for idd in temp:
#        #print(idd)
#        text = nlp(str(idd))
#        flag = False
#        
#        for item in text:
#            if item.tag_ != 'PRP':
#                flag = True
#                break
#        if str(idd) == "us" or str(idd) == "that":flag = False
#       # flag = True
#        if flag == True:
#            f3.write(str(idd))
#            f3.write("     " )
#    #f3.write(text)
#    f3.write("\n")
#   # break
#print(ans)
ans = 0
whole = 0
length = len(lines) / 5
for i in range(int(length)):
    count = 0
    for j in range(5):
        if lines[i*5+j][1] != "none":count += 1
    if count <= 1:
        for j in range(5):
            for item in lines[i * 5 + j]:
                f.write(str(item))
                f.write("\t")
            f.write("\n")
        f2.write(str(lines[i*5][3]))
        f2.write("\n")
    if count > 1:ans += 1
    whole += 1
print(ans)
print(whole)