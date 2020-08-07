#!/usr/bin/env python
# coding: utf-8

# In[99]:


import boto3
import numpy as np
import sklearn.cluster
import distance
from boto3 import client
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score


# # List File names from s3 bucket 

# In[100]:


file_list=[]
conn = client('s3')  # again assumes boto.cfg setup, assume AWS S3
for key in conn.list_objects(Bucket='sagemaker-studio-qfizos0irmr')['Contents']:
    file_list.append(key['Key'])
file_list


# # Extract File name remove surfix

# In[101]:


file_names=[]
for i in file_list:
    new_i = '.'+i[len(i)-1]+i[len(i)-2]+i[len(i)-3]
    i = i.replace(new_i,'')
    file_names.append(i)
file_names    


# # Test Words

# In[87]:


random_words=['Christene Shanahan','Deanna Chrysler','Camille Selby','Viki Dennard','Thaddeus Burma','Idella Bartley','Kyung Evett']


# In[97]:


random="adb-africa adb-asia aibd aid anrpc asean atpc bis cipec comecon ec imf inro irsg isa itc iwc-whale mfa oapec oecd opec un unctad who worldbank"
random_list=[]
for i in random.split():
    random_list.append(i) 
random_list


# # Cluster File name using Levenshtein Distance

# In[105]:


words = np.asarray(random_list) #So that indexing with a list will work
lev_similarity = -1*np.array([[distance.levenshtein(w1,w2) for w1 in words] for w2 in words])
affprop = sklearn.cluster.AffinityPropagation(affinity="precomputed", damping=0.5)
affprop.fit(lev_similarity)
for cluster_id in np.unique(affprop.labels_):
    exemplar = words[affprop.cluster_centers_indices_[cluster_id]]
    cluster = np.unique(words[np.nonzero(affprop.labels_==cluster_id)])
    cluster_str = ", ".join(cluster)
    print(" - %s: %s" % (exemplar, cluster_str))


# # Cluster File Using K-Means
Learn from sklearn.cluster.KMeans https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
# In[1]:


vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(file_names)

true_k = 2
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
model.fit(X)

order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(true_k):
    print("Cluster %d:" % i),
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind]),
    print


# In[ ]:




