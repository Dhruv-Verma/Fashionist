import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import OrdinalEncoder
from random import sample
import pickle
from scipy.spatial import distance
from sklearn.metrics import silhouette_score


#function to filter out images on the basis of occasion and gender
def filtering(dataset,occasion,gender):
    data=pd.DataFrame(columns=dataset.columns)
    for i in range(dataset.shape[0]):
        row=dataset.iloc[i]
        if row["occasion"]==occasion and row['gender']==gender:
            data=data.append(row,ignore_index=True)
    return data

#function to return ideal number of clusters
def silhouette(df):
    sil=[]
    cluster_val=[]
    for i in range(2,11):
        cluster_val.append(i)
        kmeans = KMeans(n_clusters=i,random_state=0).fit(df)
        labels=kmeans.labels_
        sil.append(silhouette_score(df,labels))
    ideal=cluster_val[sil.index(max(sil))]
    return ideal  

#retrieval function
def retrieval(dataset,occasion,gender,recom_num,pref_matrix=None):

    occasion=occasion.capitalize()
    dataset=dataset.fillna('nan')
    enc=OrdinalEncoder()
    new_data=dataset.drop(columns=['occasion', 'gender',"image","colour_bottom","colour_top","full_body_bbox","upper_body_bbox","lower_body_bbox"])
    enc.fit(new_data)

    
    data=filtering(dataset,occasion,gender)
    
    df=data.drop(columns=['occasion', 'gender',"image","colour_bottom","colour_top","full_body_bbox","upper_body_bbox","lower_body_bbox"])
    df=enc.transform(df)
    df=pd.DataFrame(df,columns=["full_body", "lower_body", "upper_body","outerwear",'neckline','upper_body_length','lower_body_length','closure_type','sleeve_length'])
    clusters=silhouette(df)
    
    
    kmeans = KMeans(n_clusters=clusters, random_state=0).fit(df)
    centroids=kmeans.cluster_centers_
    labels=kmeans.labels_
    weights=np.zeros(clusters)
    
    #PLOTTING CLUSTERS
    """plot_df=df
    cen=kmeans.cluster_centers_
    plot_df=np.concatenate((cen,plot_df))
    tsne = TSNE(perplexity=30, n_components=2, init='pca', n_iter=3500, random_state=32)
    plot_df=tsne.fit_transform(plot_df)
    
    cen=plot_df[:clusters,:]
    plot_df=plot_df[clusters:,:]

    LABEL_COLOR_MAP = {0 : 'chartreuse',
                   1 : 'deeppink',
                   2:"gold",
                   3:"turquoise",
                4:"midnightblue" ,
                5:"springgreen",
                      6:"black",
                      7:"silver",
                      8:"crimson",
                      9:"plum",
                      10:"brown"}

    label_color = [LABEL_COLOR_MAP[l] for l in kmeans.labels_]    
    plt.figure(figsize=(20,10))
    #ax = fig.add_subplot(111, projection='3d')
    plt.scatter(plot_df[:,0], plot_df[:,1],c=label_color, alpha=0.7,s=90,marker="o",edgecolors="#000000")
    

    plt.scatter(cen[:,0], cen[:,1],c="r", alpha=1,s=200,marker="o",edgecolors="#000000")
    plt.show()"""
    #############################
    
    
    if str(type(pref_matrix))=="<class 'numpy.ndarray'>":
        pref_matrix=pd.DataFrame(pref_matrix,columns=["full_body", "lower_body", "upper_body","outerwear",'neckline','upper_body_length','lower_body_length','closure_type','sleeve_length'])
        pref_matrix=enc.transform(pref_matrix)
    
        for i in range(pref_matrix.shape[0]):
            cluster_dist=[]
            for j in range(len(centroids)):
                centroid=centroids[j]
                dist=distance.euclidean(pref_matrix[i,:],centroid)
                cluster_dist.append(dist)
            ind=cluster_dist.index(min(cluster_dist))
            weights[ind]+=1

        
    else:
        weights=np.ones(clusters)
    
    weights=(weights/np.sum(weights))*recom_num
    
    dflist=[]
    for i in range(clusters):
        dflist.append(pd.DataFrame(columns=dataset.columns))

    y=pd.DataFrame(labels, columns=['label'])
    data=pd.concat([data,y],axis=1)
    for i in range(data.shape[0]):
        clusterval=data.iloc[i]['label']
        dflist[clusterval]=dflist[clusterval].append(data.iloc[i],ignore_index=True)
    
    retrieval=pd.DataFrame(columns=dataset.columns)
    for i in range(len(dflist)):
        ind=[i for i in sample([j for j in range(dflist[i].shape[0])], int(weights[i]))]
        for j in ind:
            retrieval=retrieval.append(dflist[i].iloc[j])
    if retrieval.shape[0]<recom_num:
        extra=recom_num-retrieval.shape[0]
        max_clusters=np.argsort(weights)[-extra:]
        for i in max_clusters:
            ind=[i for i in sample([j for j in range(dflist[i].shape[0])], 1)]
            for j in ind:
                retrieval=retrieval.append(dflist[i].iloc[j])
    
                
    retrieval=retrieval.drop(columns=['label'])
    retrieval.reset_index(drop=True, inplace=True)
    
    ids=[i for i in retrieval.image]
    if len(ids)>recom_num:
        ids=sample(ids,recom_num)
    return ids

# if __name__ == "__main__":
#     dataset=pickle.load(open("dataset.pkl","rb"))
#     pref_matrix=[["nan","shorts","t_shirt","nan","round_neck","hip_length","full_length","pullover","short"],
#             ["nan","shorts","tank_top","nan","round_neck","hip_length","full_length","pullover","short"]]
#     print(retrieval(dataset,"Travel","male",10))
#     print(retrieval(dataset,"Travel","male",10,pref_matrix))
