from fileWork import distance,KMeans
from matplotlib.pyplot import plot,show

def inertia_(lable,last_centroids, data_norm):
    value =0
    i=0
    for elem in lable:
        dist = distance(data_norm[i],last_centroids[elem])
        value+=dist
        i+=1

    return value

def elbow_method(max_k, data_norm, centroids_history, lables_history, mas):
    inertia=[]
    for i in range(1,max_k):
        last_lable=KMeans(i, data_norm, centroids_history, lables_history, mas)
        value=inertia_(last_lable,centroids_history[len(centroids_history)-1], data_norm)
        inertia.append(value)
        centroids_history.clear()
        lables_history.clear()

    plot(range(1,max_k),inertia,marker='s')
    show()

