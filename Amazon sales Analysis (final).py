#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns


# In[2]:


sales_data = pd.read_csv("D:\internship dataset/amazon-data.csv")


# In[3]:


sales_data.head()


# In[4]:


#checking the shape
sales_data.shape


# In[5]:


sales_data.columns


# In[6]:


sales_data.info()


# In[7]:


#checking no. of null values
sales_data.isnull().sum()


# In[8]:


sales_data1 = sales_data.copy()


# In[9]:


sales_data1['Item Class'].value_counts()


# In[10]:


#generating descriptive statistics 
sales_data1.describe()


# In[11]:


sales_data1.head()


# In[12]:


sales_data1['Invoice Date'] = pd.to_datetime(sales_data1['Invoice Date'])


# In[13]:


# creating Year, Month , Quarter, Day Columns in sales_data1

sales_data1['Invoice_Year']= sales_data1['Invoice Date'].dt.year
sales_data1['Invoice_Month']= sales_data1['Invoice Date'].dt.month
sales_data1['Invoice_Quarter']= sales_data1['Invoice Date'].dt.quarter
sales_data1['Invoice_Day']= sales_data1['Invoice Date'].dt.day


# In[14]:


sales_data1.info()


# In[15]:


#Creating DataFrame only with necessary values.
sales_data2 = sales_data1[['CustKey','Item','Invoice Date','Invoice_Year','Invoice_Quarter','Invoice_Month','Invoice_Day',
                          'Sales Quantity','Sales Amount','Sales Amount Based on List Price','Discount Amount','Sales Margin Amount',
                           'Sales Cost Amount','Sales Rep','U/M','List Price','Sales Price']]


# In[16]:


sales_data2.isnull().sum()


# In[17]:


#removed the null values from the columns
sales_data2.dropna(subset=['Discount Amount','Sales Price'],axis=0,inplace=True)


# In[18]:


sales_data2.isnull().sum()


# In[19]:


#checking the correlation
plt.figure(figsize=(12,8))
sns.heatmap(sales_data2.corr(method='pearson'),annot=True, vmin=-1, vmax=1 )


# Observations:
#     
# 1- Discount Amount is highly related to Sales Amount,Sales Cost
# Amount,Sales Amount Based on List Price & Sales Margin Amount 
# and moderately related to Sales Quantity.
# 
# 2- List Price highly related to sales price and has no relations with
# Sales amount, Sales cost amount, Sales amount based on list price & sales 
# margin amount. 
#  
# 3- Sales quantity is moderately related to Sales amount,discount
# amount, sales margin amount.
# 
# 4- Their is no relation Between Sales Rep and Sales Amount,Sales
# Margin Amount.

# In[20]:


sales_data2.head()


# In[21]:


sales_data2.tail()


# In[22]:


sales_data2.shape


# In[23]:


sales_data2.Item.value_counts()


# In[24]:


sales_data2.describe()


# # Automated EDA

# In[25]:


import sys
get_ipython().system('pip install pandas-profiling')


# In[26]:


from pandas_profiling import ProfileReport


# In[27]:


from pandas_profiling.profile_report import ProfileReport


# In[28]:


profile = ProfileReport(sales_data2,explorative = True ,dark_mode=True)


# In[29]:


profile


# In[30]:


get_ipython().system('pip install dtale')


# In[31]:


import dtale 
dtale.show(sales_data2)


# In[32]:


sales_data2[['List Price','Sales Price','Sales Amount Based on List Price','Sales Amount','Discount Amount']].head(16)


# Observation Discount Amount = (Sales Amount Based on List price Sales Amount)

# # Yearly Sales Record:

# In[33]:


Yearly_Sales = sales_data2[['CustKey','Item','Invoice Date','Invoice_Year','Invoice_Month',
                           'Sales Quantity','Sales Amount Based on List Price','Discount Amount',
                            'Sales Amount','Sales Margin Amount','Sales Cost Amount','Sales Rep',
                            'U/M','List Price','Sales Price']]


# In[34]:


Yearly_Sales01 = Yearly_Sales.groupby('Invoice_Year').sum().reset_index()
sns.catplot(y = 'Sales Amount',x = 'Invoice_Year',data = Yearly_Sales01, palette = 'Reds',kind ="bar")
plt.xlabel('Year')
plt.ylabel('Sales Amount')
plt.title('Yearly Sales')
Yearly_Sales[['Invoice_Year','Sales Amount']]


# In[35]:


plt.figure(figsize = (15,5))
sns.lineplot(y = 'Sales Amount', x = 'Invoice_Month',
            data= sales_data2.groupby(['Invoice Date','Invoice_Year','Invoice_Month']).sum(),
            hue = 'Invoice_Year',palette='bright' )


# Observtions: From this plot, it is clear that Sales decreased continuously & then it started to increase from 2018 to 2019.

# In[36]:


#plotting piechart to know Sales Sahre among 3 years
plt.figure(figsize=(17,6))
plt.pie('Sales Amount' , labels='Invoice_Year',data=Yearly_Sales01,
       autopct='%1.2f%%',shadow=True,startangle=90)
plt.axis('equal')
plt.title('Sales Contribution')
plt.legend(round(Yearly_Sales01['Sales Amount'],2), loc=7 , fontsize = 'xx-large')
plt.show()


# Observations: From 2017-19 Highest Sales Amount 2017>2019>2018.

# In[37]:


plt.figure(figsize=(20,7))
sales_data2['Sales Rep'].value_counts().plot.bar()
plt.xlabel('Sales Rep')
plt.ylabel('count')


# Sales Rep "108" were used most often while sales Rep"150" has been used the least.

# # Yearly-Monthwise Records:

# In[38]:


Yearly_Monthwise_Sales = sales_data2.groupby(['Invoice_Year','Invoice_Month']).sum().reset_index()
Yearly_Monthwise_Sales.iloc[:,6:].describe()


# In[39]:


sns.relplot(x='Invoice_Month',y= 'Sales Amount', data= Yearly_Monthwise_Sales,height=5,
          kind = 'line',aspect = 1, col = 'Invoice_Year')
plt.xlabel('Month')
plt.ylabel('Sales Amount')
print('*'*50+'Yearly-Monthwise Sales Trend'+'*'*50)


# In[40]:


sns.histplot(Yearly_Monthwise_Sales['Sales Amount'], kde = True)


# In[41]:


Monthly_sales = sales_data2.groupby(['Invoice_Year','Invoice_Month','Invoice_Day']).sum().reset_index()
Monthly_sales.iloc[:,5:].describe()


# In[42]:


sns.relplot(y ='Sales Quantity' ,x = 'Sales Amount' ,data=sales_data2,height = 3,aspect=1,
          col = 'Invoice_Month',col_wrap=5,palette='muted')


# In[43]:


plt.figure(figsize=(8,20))
sns.relplot(x='Invoice_Day',y ='Sales Amount',data= sales_data2.query('Invoice_Year == 2017'),
          kind ='line',col = 'Invoice_Month' , col_wrap =2, height = 4, aspect = 2)
plt.ylabel('Sales Amount')
print('*'*46+'Monthly Sales Trend in 2017'+'*'*40)


# In[44]:


plt.figure(figsize=(8,20))
sns.relplot(x='Invoice_Day',y ='Sales Amount',data = sales_data2.query('Invoice_Year ==2018'),
            kind = 'line',col = 'Invoice_Month' , col_wrap = 2, height = 4 ,aspect = 2)
plt.ylabel('Sales Amount')
print('*'*50+'Monthly Sales Trend in 2018'+'*'*50)


# In[45]:


plt.figure(figsize=(8,20))
sns.relplot(x='Invoice_Day',y ='Sales Amount',data = sales_data2.query('Invoice_Year ==2019'),
            kind = 'line',col = 'Invoice_Month' , col_wrap = 2, height = 4 ,aspect = 2)
plt.ylabel('Sales Amount')
print('*'*50+'Monthly Sales Trend in 2018'+'*'*50)


# # Profits Records:

# In[46]:


sns.catplot(y = 'Sales Margin Amount' , x = 'Invoice_Year',data = Yearly_Sales01,kind="bar" )
plt.xlabel('Year')
plt.ylabel('Sales Margin Amount')
plt.title('Yearly Profits')
Yearly_Sales01[['Invoice_Year','Sales Margin Amount']]


# In[47]:


plt.figure(figsize = (15,5))
sns.lineplot(y = 'Sales Margin Amount' , x = 'Invoice_Month',
            data= sales_data2.groupby(['Invoice Date','Invoice_Year','Invoice_Month']).sum(),
            hue = 'Invoice_Year' , palette='bright')
plt.title('profits Trend')
plt.show()


# In[48]:


plt.figure(figsize=(10,6))
plt.pie('Sales Margin Amount',labels='Invoice_Year',data=Yearly_Sales01[['Invoice_Year','Sales Margin Amount']],
       autopct='%1.2f%%' ,shadow=True,startangle=90)
plt.axis('equal')
plt.title('Profit Share')
plt.show()


# # Top 10 Records:

# In[49]:


Top10byCustKey17 = Yearly_Sales[Yearly_Sales['Invoice_Year']==2017].groupby(['Invoice_Year','CustKey']).sum()
Top10byCustKey17 = Top10byCustKey17.sort_values('Sales Margin Amount',ascending = False).reset_index().head(10)


# In[50]:


plt.figure(figsize=(10,5))
sns.barplot(x='CustKey',y='Sales Margin Amount',data= Top10byCustKey17, palette = 'turbo',
           order = Top10byCustKey17.CustKey)
plt.title('Top 10 Custkey by Sales Margin Amount')
Top10byCustKey17[['CustKey' , 'Sales Margin Amount']]


# In[51]:


plt.figure(figsize=(20,8))
plt.pie('Sales Margin Amount' ,labels='CustKey',data=Top10byCustKey17,
       autopct='%1.2f%%',shadow=True,startangle=90, explode =(0.15, 0,0,0,0,0,0,0,0,0.1))
plt.axis('equal')
plt.show()


# Observations:Among the 10 CustKey that generated the most Sales Margin Amount, CustKey-10021485 contributed around 30.57% of
#     the Sales Magin Amount in 2017.

# In[52]:


Top10byCustKey18 = Yearly_Sales[Yearly_Sales['Invoice_Year']==2018].groupby(['Invoice_Year','CustKey']).sum()
Top10byCustKey18 = Top10byCustKey18.sort_values('Sales Margin Amount', ascending = False).reset_index().head(10)


# In[53]:


plt.figure(figsize=(10,5))
sns.barplot(x='CustKey',y='Sales Margin Amount',data= Top10byCustKey18, palette = 'turbo',
            order = Top10byCustKey18.CustKey)
Top10byCustKey18[['CustKey','Sales Margin Amount']]


# In[54]:


plt.figure(figsize=(20,8))
plt.pie('Sales Margin Amount',labels='CustKey',data=Top10byCustKey18,autopct='%1.2f%%',
       shadow=True,startangle=90,explode =(0.15,0,0,0,0,0,0,0,0,0.1))
plt.axis('equal')
plt.title('Top 10 CustKey by Sales Margin Amount')
plt.show()


# Observations: Among the 10 CustKey that generated the most Sales Margin Amount, CustKey-10025039 contributed around 30.79% of
#     the Sales Margin Amount in 2018.

# In[55]:


Top10byCustKey19 = Yearly_Sales[Yearly_Sales['Invoice_Year']==2019].groupby(['Invoice_Year','CustKey']).sum()
Top10byCustKey19 = Top10byCustKey19.sort_values('Sales Margin Amount',ascending = False).reset_index().head(10)


# In[56]:


plt.figure(figsize=(10,5))
sns.barplot(x='CustKey',y='Sales Margin Amount',data = Top10byCustKey19, palette = 'turbo',
           order = Top10byCustKey19.CustKey)
Top10byCustKey19[['CustKey','Sales Margin Amount']]


# In[57]:


plt.figure(figsize=(20,8))
plt.pie('Sales Margin Amount' ,labels='CustKey',data=Top10byCustKey19,autopct='%1.2f%%',
       shadow=True,startangle=90, explode= (0.15,0,0,0,0,0,0,0,0,0.1))
plt.axis('equal')
plt.title('Top 10 CustKey by Sales Margin Amount')
plt.show()


# Observations: Among the 10 CustKey that generated the most Sales Margin Amount, CustKey-10009676 contributed around 30.41% of 
#     the Sales Margin Amount in 2019.
