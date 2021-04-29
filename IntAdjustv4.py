#!/usr/bin/env python
# coding: utf-8

# # Interest Adjustment Program 
# ## Baselined 19-July-2019 (Still in Dev)
# Code Clean up 01 Sep 2020
# 
# # Read Excel with Source Data

# In[40]:


# Please copy blank exclusion files if the country does not have any data for a type of exclusion namely settlement, refinance, insurance, exclusion
# for TZ please rename the Interestcappedcheck to VarianceToInterest_Capped in the source file
# vergist@bayportfinance.com
import pandas as pd
# import sys as sys
import os.path
from IntAdjustFunc import logline

paramfileloc = input("Enter file name of the param file: ")
# print(paramfileloc)
# paramfileloc=r"C:\Users\vergist\Downloads\Int Adjust\201904\May 2019\MZ\201904 param.xlsx"
# params=pd.read_excel (io=paramfileloc,sheet_name="Sheet1")
paramfileloc = "".join(paramfileloc)
# print(paramfileloc)


# In[41]:


params = pd.read_excel(io=paramfileloc, sheet_name="Sheet1")

# In[42]:


# params

logFile = os.path.dirname(paramfileloc)
logFile = logFile + "\\IntAdjust.log"
logline(logFile, "parameter file is " + paramfileloc)

# In[4]:


tomfolder = params['tomfolder'].astype(str)
# tomfolder=tomfolder.astype(str)
pd.set_option('max_colwidth', 8000)
# print (tomfolder)
logline(logFile, "Folder is " + str(tomfolder))

# In[7]:


period = params['Period'].astype(str)
# tomfile=tomfolder.astype(str)
# print("Period is",period)
logline(logFile, "Period is " + str(period))

# In[9]:


tomfile = params['tomfile'].astype(str)
# tomfile=tomfolder.astype(str)
# print(tomfile)
logline(logFile, "Filename is " + str(tomfile))

# In[10]:


sheetname = params['sheetname'].astype(str)

sheetname = "".join(sheetname)
# print('sheetname  ' +sheetname)


# In[11]:


fileloc = params['fileloc']

# In[43]:


settlefile = params['settlefile']

# In[44]:


insfile = params['insfile']

# In[45]:


Replacementfile = params['Replacementfile']

# In[46]:


Exclusionfile = params['Exclusionfile']

# In[47]:


settheader = params['settheader']

# In[48]:


insheader = params['insheader']

# In[49]:


replacementheader = params['replacementheader']

# In[50]:


exclusionheader = params['exclusionheader']

# In[20]:


# fileloc="C:\\Users\\vergist\\Downloads\\Int Adjust\\201904\\May 2019\\BFS\\"
# tomfolder="C:\\Users\\vergist\\Downloads\\Int Adjust\\201904\\"
# tomfile="BFS.xlsx"
# sheetname=["GH_BFS"]
readtomfile = "".join(tomfolder)
readtomfile = readtomfile + "\\" + readtomfile.join(tomfile)
# readtomfile=tomfolder+tomfile
# print (readtomfile)
# print (readtomfile,sheetname)

logline(logFile, "Finance file is " + readtomfile)

# In[21]:


import datetime

# print ('Reading Finance file now....')
logline(logFile, "Reading Finance file now....")
d1 = datetime.datetime.now()
# print (d1)
df_tomfile = pd.read_excel(io=readtomfile, sheet_name=sheetname)
d2 = datetime.datetime.now()
# print ('Finished Reading Finance file ')
logline(logFile, "Finished Reading Finance file")

# In[22]:


# print ('Time taken to read file' ,d2-d1)
logline(logFile, "Time taken is" + str(d2 - d1))

# In[23]:


df_tomfile1 = df_tomfile[["LoanID", "DebtorCode", "VarianceToInterest_Capped"]]

# In[29]:


# print ("Number of records read",df_tomfile1.count())
logline(logFile, "Number of records read " + str(df_tomfile1.count()))

# ## Drop zero value records

# In[30]:


df_tomfile2 = df_tomfile1[df_tomfile1["VarianceToInterest_Capped"] != 0.00]

# In[31]:


df_tomfilezero = df_tomfile1[df_tomfile1["VarianceToInterest_Capped"] == 0.00]

# In[33]:


filename = "".join(fileloc)
filename = filename + "".join('\\') + "".join('AfterDroppingzeroint.csv')
# filename


# In[35]:


#print("Number of records after dropping zeroes", df_tomfile2.count())
# below works
# df_tomfile2.to_csv(r'C:\Users\vergist\Downloads\Int Adjust\201904\May 2019\BFS\AfterDroppingzeroint.csv',columns=['LoanID','VarianceToInterest_Capped'],header=False,index=False)
# After dropping zeroes
# df_tomfile2.to_csv(filename,columns=['LoanID','VarianceToInterest_Capped'],header=False,index=False)


# In[36]:


filename = "".join(fileloc)
filename = filename + "".join('\\') + "".join('zeroamounts.csv')
# filename


# In[37]:


# df_tomfilezero.to_csv(r'C:\Users\vergist\Downloads\Int Adjust\201904\May 2019\BFS\zeroamounts.csv',columns=['LoanID','VarianceToInterest_Capped'],header=False,index=False)
# zero value lines file
# df_tomfilezero.to_csv(filename,columns=['LoanID','VarianceToInterest_Capped'],header=False,index=False)


# In[54]:


# fileloc+settlefile
filename = "".join(fileloc)
filename = filename + "".join('\\') + "".join(settlefile)
# filename


# # Read settled loans

# In[63]:


# print(filename)
# print(settheader[0])
# settheader.dtype
# type(settheader)


# In[61]:


settledloan = pd.read_csv(filename, usecols=["ClientID"], skiprows=settheader[0])

# In[67]:


# settledloan.shape


# In[68]:


# print(filename)


# In[71]:


# print ('Number of Settled records read=',settledloan.shape[0])


# In[72]:


settledloan1 = settledloan.ClientID.str.replace("\'", "")

# In[73]:


# settledloan1=[settledloan1.rename(columns={'ClientID': 'DebtorCode'})]
settledloan1 = pd.DataFrame(settledloan1)

# In[75]:


settledloan1.columns = ['DebtorCode']
# print("Settled records ", settledloan1.count())


# In[79]:


# df_tomfile3 = pd.merge(df_tomfile2, settledloan3, on='DebtorCode',how='outer')

# print("Loan records\n",df_tomfile2.count())


# In[80]:


settledloan1 = settledloan1.dropna()

# In[82]:


settledloan1['DebtorCode'] = settledloan1['DebtorCode'].astype('int64')
# print("Settled records",settledloan1.count())


# ## Remove Settled Loans

# In[83]:


df_tomfile3 = df_tomfile2[~df_tomfile2['DebtorCode'].isin(settledloan1['DebtorCode'])]

# In[84]:


filename = ""
filename = "".join(fileloc)
filename = filename + "".join('\\') + "".join('AfterDroppingSettledLoan.csv')
#filename

# In[85]:


df_tomfile3.count()
# df_tomfile3.to_csv(filename,columns=['LoanID','VarianceToInterest_Capped'],header=False,index=False)


# In[86]:


df_tomfilesettled = df_tomfile2[df_tomfile2['DebtorCode'].isin(settledloan1['DebtorCode'])]

# In[87]:


filename = "".join(fileloc)
filename = filename + "".join('\\') + "".join('settledrecords.csv')
#filename

# In[88]:


# df_tomfilesettled.to_csv(filename,columns=['LoanID','VarianceToInterest_Capped'],header=False,index=False)


# ## Remove Insurance Claims

# In[89]:


filename = "".join(fileloc)
filename = filename + "".join('\\') + "".join(insfile)
#filename

# In[91]:


# BFS,CFC,MZ has 11 skiprows before CSV
InsClaimloan = pd.read_csv(filename, usecols=["LoanID"], skiprows=insheader[0])

# In[93]:


# print("Insurance records read",InsClaimloan.shape)


# In[94]:


# InsClaimloan


# In[95]:


InsClaimloan1 = InsClaimloan.LoanID.str.replace("\'", "")

# In[96]:


InsClaimloan1 = pd.DataFrame(InsClaimloan1)

# In[97]:


# print('Insurance count',InsClaimloan.shape)


# In[98]:


InsClaimloan1 = InsClaimloan1.dropna()

# In[99]:


# print('After Drop null values from Insurance',InsClaimloan1.shape)


# In[100]:


df_tomfile3.count()

# In[101]:


df_tomfile4 = df_tomfile3[~df_tomfile3['LoanID'].isin(InsClaimloan1['LoanID'])]

# In[102]:


df_tomfile4.count()

# In[103]:


filename = "".join(fileloc)
filename = filename + "".join('\\') + "".join('AfterDroppingInsclaim.csv')
#filename

# In[104]:


#df_tomfile4.count()
# df_tomfile4.to_csv(filename,columns=['LoanID','VarianceToInterest_Capped'],header=False,index=False)


# In[105]:


df_tomfileinsclaim = df_tomfile3[df_tomfile3['LoanID'].isin(InsClaimloan1['LoanID'])]

# In[106]:


filename = "".join(fileloc)
filename = filename + "".join('\\') + "".join('insclaim.csv')
filename

# In[107]:


# df_tomfileinsclaim.to_csv(filename,columns=['LoanID','VarianceToInterest_Capped'],header=False,index=False)


# ## Remove Replacement Loans
filename = "".join(fileloc)
filename = filename + "".join('\\') + "".join(Replacementfile)
filename
# In[117]:


Replaceloan = pd.read_csv(filename, usecols=["SettledLoanIDs"], skiprows=replacementheader[0])

# In[118]:


Replaceloan = Replaceloan.SettledLoanIDs.str.replace("\'", "")

# In[119]:


Replaceloan = Replaceloan.str.replace("-", "")

# In[120]:


Replaceloan = Replaceloan.str.replace(" ", "")

# In[121]:


Replaceloan = Replaceloan.dropna()

# In[122]:


Replaceloan = Replaceloan.str.strip()

# In[123]:


Replaceloan1 = Replaceloan[Replaceloan.apply(len) <= 14]

# In[124]:


df_tomfile5 = df_tomfile4[~df_tomfile4['LoanID'].isin(Replaceloan1)]

# In[125]:


filename = "".join(fileloc)
filename = filename + "".join('\\') + "".join('AfterDroppingReplacements.csv')
#filename

# In[128]:


# print("After dropping replacement loans ",df_tomfile5.count())
# df_tomfile5.to_csv(filename,columns=['LoanID','VarianceToInterest_Capped'],header=False,index=False)
# df_tomfile4.info()


# In[129]:


replacedloans = df_tomfile4[df_tomfile4['LoanID'].isin(Replaceloan1)]

# In[130]:


filename = "".join(fileloc)
filename = filename + "".join('\\') + "".join('replacedloans.csv')
#filename

# In[131]:


# replacedloans.to_csv(filename,columns=['LoanID','VarianceToInterest_Capped'],header=False,index=False)


# ## Remove Excluded loans

# In[133]:


filename = "".join(fileloc)
filename = filename + "".join('\\') + "".join(Exclusionfile)
#filename

# In[134]:


# BFS has 14 in header
Excludedloan = pd.read_csv(filename, usecols=["ClientID"], skiprows=exclusionheader[0])

# In[135]:


Excludedloan.info()

# In[136]:


Excludedloan = Excludedloan.ClientID.str.replace("\'", "")

# In[137]:


Excludedloan1 = pd.DataFrame(Excludedloan)

# In[140]:


Excludedloan1.count()

# In[141]:


Excludedloan1 = Excludedloan1.dropna()

# In[142]:


#Excludedloan1.count()

# In[145]:


df_tomfile6 = df_tomfile5[~df_tomfile5['DebtorCode'].isin(Excludedloan1['ClientID'])]

# In[146]:


filename = "".join(fileloc)
filename = filename + "".join('\\') + "".join('AfterDroppingExclusions.csv')
#filename

# In[148]:


#print("Loan records now", df_tomfile6.info())
#df_tomfile6.to_csv(filename, columns=['LoanID', 'VarianceToInterest_Capped'], header=False, index=False)

# In[149]:


excluded = df_tomfile5[df_tomfile5['DebtorCode'].isin(Excludedloan1['ClientID'])]

# In[150]:


filename = "".join(fileloc)
filename = filename + "".join('\\') + "".join('excluded.csv')
#filename

# In[151]:


# excluded.to_csv(filename,columns=['LoanID','VarianceToInterest_Capped'],header=False,index=False)


# # Generate FULL file

# In[155]:


filename = "".join(fileloc)
filename = filename + "".join('\\') + "".join(period + "_" + sheetname + '_Adjustment File Full.csv')
#filename
# 201904_MZ_Adjustment File Full.csv


# In[156]:


df_tomfile6.to_csv(filename,columns=['LoanID','VarianceToInterest_Capped'],header=False,index=False)


# In[157]:


sumvalue = sum(df_tomfile6['VarianceToInterest_Capped'])

# ## Generate 500 sample file

# In[158]:


filename = "".join(fileloc)
filename = filename + "".join('\\') + "".join(period + "_" + sheetname + '_Adjustment File UAT 500 Loan Sample.csv')
#filename

# In[159]:


df_tomfile6.head(500).to_csv(filename, columns=['LoanID', 'VarianceToInterest_Capped'], header=False, index=False)

# In[160]:


# print ("Final records after all exclusions",df_tomfile6.count())


# In[161]:


# Summary

DictOutput = {"Initial records": len(df_tomfile1), "After Dropping zeroes": len(df_tomfile2),
              "After Dropping settled loans": len(df_tomfile3), "After Dropping Insurance claim": len(df_tomfile4),
              "After Dropping Replacements": len(df_tomfile5), "After Dropping Exclusions": len(df_tomfile6),
              "Total sum value": sumvalue}

# In[162]:


DictOutputAuditDrops = {"zero value records": len(df_tomfilezero), "Settled": len(df_tomfilesettled),
                        "Insurance": len(df_tomfileinsclaim), "Replaced": len(replacedloans),
                        "Exclusions": len(excluded),
                        "Total Excluded": len(df_tomfilezero) + len(df_tomfilesettled) + len(df_tomfileinsclaim) + len(
                            replacedloans) + len(excluded)}

# In[163]:


filename = "".join(fileloc)
filename = filename + "".join('\\') + "".join('Output.log')
filename

# In[164]:


import csv

with open(filename, 'a+') as f:
    for key in DictOutput.keys():
        f.write("%s,%s\n" % (key, DictOutput[key]))
    for key in DictOutputAuditDrops.keys():
        f.write("%s,%s\n" % (key, DictOutputAuditDrops[key]))

# In[165]:

##
# filename="".join(fileloc)
# filename=filename+"".join('\\')+"".join('OutputDrops.log')
# filename
##

# In[166]:


# with open(filename, 'w') as f:
# for key in DictOutputAuditDrops.keys():
# f.write("%s,%s\n"%(key,DictOutputAuditDrops[key]))


# In[ ]:


# End of Program
