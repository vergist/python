#!/usr/bin/env python
# coding: utf-8

# # Read Excel with Source Data

# In[ ]:


#Please copy blank exclusion files if the country does not have any data
#for TZ please rename the Interestcappedcheck to VariancetoInterestcapped
import pandas as pd
import sys as sys
#print (len(sys.argv))
#print (sys.argv[0])
#print (sys.argv[1])
#print (sys.argv[2])
paramfileloc = input("Enter file name of the param file: ") 
print(paramfileloc) 
#paramfileloc=r"C:\Users\vergist\Downloads\Int Adjust\201904\May 2019\MZ\201904 param.xlsx"
#params=pd.read_excel (io=paramfileloc,sheet_name="Sheet1")
paramfileloc="".join(paramfileloc)
print(paramfileloc) 


# In[2]:


params=pd.read_excel (io=paramfileloc,sheet_name="Sheet1")


# In[46]:


params


# In[47]:


tomfolder=params['tomfolder'].astype(str)
#tomfolder=tomfolder.astype(str)
pd.set_option('max_colwidth', 8000)
print (tomfolder)


# In[48]:


period=params['Period'].astype(str)
#tomfile=tomfolder.astype(str)
period


# In[49]:


tomfile=params['tomfile'].astype(str)
#tomfile=tomfolder.astype(str)
tomfile


# In[50]:


sheetname=params['sheetname'].astype(str)

sheetname="".join(sheetname)
print('sheetname  ' +sheetname)


# In[51]:


fileloc=params['fileloc']


# In[52]:


settlefile=params['settlefile']


# In[53]:


insfile=params['insfile']


# In[54]:


Replacementfile=params['Replacementfile']


# In[55]:


Exclusionfile=params['Exclusionfile']


# In[56]:


#fileloc="C:\\Users\\vergist\\Downloads\\Int Adjust\\201904\\May 2019\\BFS\\"
#tomfolder="C:\\Users\\vergist\\Downloads\\Int Adjust\\201904\\"
#tomfile="BFS.xlsx"
#sheetname=["GH_BFS"]
readtomfile="".join(tomfolder)
readtomfile=readtomfile+"\\"+readtomfile.join(tomfile)
#readtomfile=tomfolder+tomfile
#print (readtomfile)
#print (readtomfile,sheetname)
readtomfile


# In[58]:


import datetime
print ('Reading Finance file now....')
d1=datetime.datetime.now()
df_tomfile=pd.read_excel (io=readtomfile,sheet_name=sheetname)
d2=datetime.datetime.now()
print ('Finished Reading Finance file ')


# In[59]:


print ('Time taken to read file' ,d2-d1)


# In[62]:


#This needs to be changed for TZ to use InterestCappedCheck
df_tomfile1=df_tomfile[["LoanID","DebtorCode","VarianceToInterest_Capped"]]


# In[63]:


df_tomfile1.info()


# ## Drop zero value records

# In[64]:


df_tomfile2=df_tomfile1[df_tomfile1["VarianceToInterest_Capped"]!=0.00]


# In[65]:


df_tomfilezero=df_tomfile1[df_tomfile1["VarianceToInterest_Capped"]==0.00]


# In[66]:


filename="".join(fileloc)
filename=filename+"".join('\\')+"".join('AfterDroppingzeroint.csv')
filename


# In[67]:


df_tomfile2.info()
#below works
#df_tomfile2.to_csv(r'C:\Users\vergist\Downloads\Int Adjust\201904\May 2019\BFS\AfterDroppingzeroint.csv',columns=['LoanID','VarianceToInterest_Capped'],header=False,index=False)
#After dropping zeroes
df_tomfile2.to_csv(filename,columns=['LoanID','VarianceToInterest_Capped'],header=False,index=False)


# In[68]:


filename="".join(fileloc)
filename=filename+"".join('\\')+"".join('zeroamounts.csv')
filename


# In[69]:



#df_tomfilezero.to_csv(r'C:\Users\vergist\Downloads\Int Adjust\201904\May 2019\BFS\zeroamounts.csv',columns=['LoanID','VarianceToInterest_Capped'],header=False,index=False)
#zero value lines file
df_tomfilezero.to_csv(filename,columns=['LoanID','VarianceToInterest_Capped'],header=False,index=False)


# In[70]:


#fileloc+settlefile
filename="".join(fileloc)
filename=filename+"".join('\\')+"".join(settlefile)
filename


# In[71]:


settledloan=pd.read_csv(filename,usecols=["ClientID"])


# In[72]:


print ('Number of Settled records read',settledloan.count())


# In[73]:


settledloan1=settledloan.ClientID.str.replace("\'","")


# In[74]:


#settledloan1=[settledloan1.rename(columns={'ClientID': 'DebtorCode'})]
settledloan1=pd.DataFrame(settledloan1)


# In[75]:


settledloan1.columns=['DebtorCode']
settledloan1.info()


# In[76]:


#df_tomfile3 = pd.merge(df_tomfile2, settledloan3, on='DebtorCode',how='outer')
df_tomfile2.info()


# In[77]:


settledloan1['DebtorCode']=settledloan1['DebtorCode'].astype('int64')
settledloan1.info()


# ## Remove Settled Loans

# In[78]:


df_tomfile3=df_tomfile2[~df_tomfile2['DebtorCode'].isin(settledloan1['DebtorCode'])]


# In[79]:


filename=""
filename="".join(fileloc)
filename=filename+"".join('\\')+"".join('AfterDroppingSettledLoan.csv')
filename


# In[80]:


df_tomfile3.count()
df_tomfile3.to_csv(filename,columns=['LoanID','VarianceToInterest_Capped'],header=False,index=False)


# In[81]:


df_tomfilesettled=df_tomfile2[df_tomfile2['DebtorCode'].isin(settledloan1['DebtorCode'])]


# In[82]:


filename="".join(fileloc)
filename=filename+"".join('\\')+"".join('settledrecords.csv')
filename


# In[83]:


df_tomfilesettled.to_csv(filename,columns=['LoanID','VarianceToInterest_Capped'],header=False,index=False)


# ## Remove Insurance Claims

# In[84]:


filename="".join(fileloc)
filename=filename+"".join('\\')+"".join(insfile)
filename


# In[85]:



InsClaimloan=pd.read_csv(filename,usecols=["LoanID"])


# In[86]:


InsClaimloan1=InsClaimloan.LoanID.str.replace("\'","")


# In[87]:


InsClaimloan1=pd.DataFrame(InsClaimloan1)


# In[88]:


df_tomfile4=df_tomfile3[~df_tomfile3['LoanID'].isin(InsClaimloan1['LoanID'])]


# In[89]:


filename="".join(fileloc)
filename=filename+"".join('\\')+"".join('AfterDroppingInsclaim.csv')
filename


# In[90]:


df_tomfile4.count()
df_tomfile4.to_csv(filename,columns=['LoanID','VarianceToInterest_Capped'],header=False,index=False)


# In[91]:


df_tomfileinsclaim=df_tomfile3[df_tomfile3['LoanID'].isin(InsClaimloan1['LoanID'])]


# In[92]:


filename="".join(fileloc)
filename=filename+"".join('\\')+"".join('insclaim.csv')
filename


# In[93]:


df_tomfileinsclaim.to_csv(filename,columns=['LoanID','VarianceToInterest_Capped'],header=False,index=False)


# In[ ]:





# ## Remove Replacement Loans

# In[94]:


filename="".join(fileloc)
filename=filename+"".join('\\')+"".join(Replacementfile)
filename


# In[95]:


Replaceloan=pd.read_csv(filename,usecols=["SettledLoanIDs"])


# In[96]:


Replaceloan=Replaceloan.SettledLoanIDs.str.replace("\'","")


# In[97]:


Replaceloan=Replaceloan.str.replace("-","")


# In[98]:


Replaceloan=Replaceloan.str.replace(" ","")


# In[99]:


Replaceloan=Replaceloan.str.strip()


# In[100]:


Replaceloan1=Replaceloan[Replaceloan.apply(len)<=14]


# In[101]:


df_tomfile5=df_tomfile4[~df_tomfile4['LoanID'].isin(Replaceloan1)]


# In[102]:


filename="".join(fileloc)
filename=filename+"".join('\\')+"".join('AfterDroppingReplacements.csv')
filename


# In[103]:


df_tomfile5.info()
df_tomfile5.to_csv(filename,columns=['LoanID','VarianceToInterest_Capped'],header=False,index=False)
#df_tomfile4.info()


# In[104]:


replacedloans=df_tomfile4[df_tomfile4['LoanID'].isin(Replaceloan1)]


# In[105]:


filename="".join(fileloc)
filename=filename+"".join('\\')+"".join('replacedloans.csv')
filename


# In[106]:


replacedloans.to_csv(filename,columns=['LoanID','VarianceToInterest_Capped'],header=False,index=False)


# ## Remove Excluded loans

# In[107]:


filename="".join(fileloc)
filename=filename+"".join('\\')+"".join(Exclusionfile)
filename


# In[108]:


Excludedloan=pd.read_csv(filename,usecols=["ClientID"])


# In[109]:


Excludedloan.info()


# In[110]:


Excludedloan=Excludedloan.ClientID.str.replace("\'","")


# In[111]:


Excludedloan1=pd.DataFrame(Excludedloan)


# In[112]:


df_tomfile6=df_tomfile5[~df_tomfile5['DebtorCode'].isin(Excludedloan1['ClientID'])]


# In[113]:


filename="".join(fileloc)
filename=filename+"".join('\\')+"".join('AfterDroppingExclusions.csv')
filename


# In[114]:


df_tomfile6.info()
df_tomfile6.to_csv(filename,columns=['LoanID','VarianceToInterest_Capped'],header=False,index=False)


# In[115]:


excluded=df_tomfile5[df_tomfile5['DebtorCode'].isin(Excludedloan1['ClientID'])]


# In[116]:


filename="".join(fileloc)
filename=filename+"".join('\\')+"".join('excluded.csv')
filename


# In[117]:


excluded.to_csv(filename,columns=['LoanID','VarianceToInterest_Capped'],header=False,index=False)


# # Generate FULL file

# In[118]:


filename="".join(fileloc)
filename=filename+"".join('\\')+"".join(period+"_"+sheetname+'_Adjustment File Full.csv')
filename
#201904_MZ_Adjustment File Full.csv


# In[119]:


df_tomfile6.to_csv(filename,columns=['LoanID','VarianceToInterest_Capped'],header=False,index=False)


# In[120]:


sumvalue=sum(df_tomfile6['VarianceToInterest_Capped'])


# ## Generate 500 sample file

# In[121]:


filename="".join(fileloc)
filename=filename+"".join('\\')+"".join(period+"_"+sheetname+'_Adjustment File UAT 500 Loan Sample.csv')
filename


# In[122]:


df_tomfile6.head(500).to_csv(filename,columns=['LoanID','VarianceToInterest_Capped'],header=False,index=False)


# In[123]:


df_tomfile6.info()


# In[124]:


#Summary

DictOutput={"Initial records":len(df_tomfile1),"After Dropping zeroes":len(df_tomfile2),"After Dropping settled loans":len(df_tomfile3),"After Dropping Insurance claim":len(df_tomfile4),"After Dropping Replacements":len(df_tomfile5),"After Dropping Exclusions":len(df_tomfile6),"Total sum value":sumvalue}


# In[125]:


DictOutputAuditDrops={"zero value records":len(df_tomfilezero),"Settled":len(df_tomfilesettled),"Insurance":len(df_tomfileinsclaim),"Replaced":len(replacedloans),"Exclusions":len(excluded),"Total Excluded":len(df_tomfilezero)+len(df_tomfilesettled)+len(df_tomfileinsclaim)+len(replacedloans)+len(excluded)}


# In[126]:


filename="".join(fileloc)
filename=filename+"".join('\\')+"".join('Output.csv')
filename


# In[127]:


import csv


with open(filename, 'w') as f:
    for key in DictOutput.keys():
        f.write("%s,%s\n"%(key,DictOutput[key]))


# In[128]:


filename="".join(fileloc)
filename=filename+"".join('\\')+"".join('OutputDrops.csv')
filename


# In[129]:


with open(filename, 'w') as f:
    for key in DictOutputAuditDrops.keys():
        f.write("%s,%s\n"%(key,DictOutputAuditDrops[key]))


# In[ ]:





# In[ ]:




