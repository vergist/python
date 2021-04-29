#!/usr/bin/env python
# coding: utf-8

# In[12]:


def find_max(numbers):
#numbers=[10,3,6,2]
    max=numbers[0]
    for i in numbers:
        if i>max:
            max=numbers[i]
    return max


# In[ ]:




