import os

data_dir='../OTE_data/semeval2014/RES/'

my_ote = open("tempp.txt","w")
dir_path = data_dir+'bert/'
if not os.path.exists(dir_path):
    os.makedirs(dir_path)
count = 0
with open(dir_path+"test_NLI_M.csv","w",encoding="utf-8") as g:
    with open(data_dir+"Restaurants_Test_Gold.xml","r",encoding="utf-8") as f:
        s=f.readline().strip()
        while s:
            category=[]
            polarity=[]
           # g.write(s)
           # g.write("\n")
            #
            if "<sentence id" in s:
                

                left=s.find("id")
                right=s.find(">")
                id=s[left+4:right-1]
                while not "</sentence>" in s:
                    if "<text>" in s:
                        my_ote.write('\n')
                        count += 1
                        left=s.find("<text>")
                        right=s.find("</text>")
                        text=s[left+6:right]
                    if"aspectTerms"not in s and "aspectTerm" in s:
                        left=s.find("term=")
                        right=s.find("polarity=")
                        category.append(s[left+6:right-2])
                        my_ote.write(s[left+6:right-2])
                        my_ote.write("     ")
                        left=s.find("polarity=")
                        right=s.find("from")
                        polarity.append(s[left+10:right-3])
                    
                    s=f.readline().strip()
            
                for i,item in enumerate(category):
                    g.write(id+"\t"+polarity[i]+"\t"+str(item)+"\t"+text+"\n")
            
            else:
                s = f.readline().strip()
           

print(count)
