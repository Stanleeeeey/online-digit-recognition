
import numpy as np
import os
from PIL import Image

def encode(lbls):
    nb = 1
    aL = np.zeros([10, nb], dtype = float)
    aL[lbls, np.arange(nb)] = 1
    return aL

def decode(aL):
    return np.argmax(aL, axis= 0)


def sigma(x):
    if x<0.:
        return np.exp(x)/(1+np.exp(x))
    else:
        return 1/(1+np.exp(-x))

sgm = np.vectorize(sigma)

def sgm_prime(x):
    return np.exp(-np.abs(x))/(1+np.exp(-np.abs(x)))

def forward(biases, weights, model_input):
    layer = model_input


    for bias, weight in zip(biases, weights):
        
        
        layer = sgm(weight@layer + bias)


    return layer 

def init_network(sizes):
    biases  = [np.zeros([y,1]) for y in sizes[1:]]
    weights = [np.random.randn(y,x) for x,y in zip(sizes[:-1], sizes[1:])]

    return [biases, weights]

def Update(biases, weights, model_input, labels, learning_rate):
    # batch size
    batch_size = float(model_input.shape[-1])
    #print(batch_size)
    
    # forward
    ai = model_input
    z = []
    a = []
    a.append(ai)
    for bias, weight in zip(biases, weights):
          
        zi = weight@ai + bias
        z.append(zi)
        ai = sgm(zi)
        a.append(ai)

    # norm
    # 
    error = np.linalg.norm(a[-1] - labels)/batch_size #(labels*np.log(a[-1]) + np.log(1-labels)*np.log(1-a[-1])).sum()/batch_size #
    print(error)
    # backward
    dlt = (a[-1]-labels)*sgm_prime(z[-1]) /batch_size #a[-1] - labels #
    
    # update 
    new_biases = biases
    new_weights = weights   

    for layer_index in range(len(weights)-1, 0, -1):

        dlt = weights[layer_index].T@dlt * sgm_prime(z[layer_index-1]) # weights[layer_index].T@ dlt * sgm_prime(z[layer_index-1]) #
    


        new_biases[layer_index-1][:,0] = new_biases[layer_index-1][:,0] - learning_rate*dlt.sum(axis=1)
        new_weights[layer_index-1] = new_weights[layer_index-1] - learning_rate* (dlt@a[layer_index-1].T)

    return [new_biases, new_weights], error 


def load_data():
    labels = []
    images = []

    for image in os.listdir(os.path.join(os.getcwd(), 'app/static/images')):

        labels.append(int(image[0]))
        
        images.append(np.max(np.asarray(Image.open(os.path.join(os.getcwd(), f'app/static/images/{image}'))), -1).reshape(-1, 1))
    

    #labels = encode(labels).T
    return labels, images

    


def run():
    import time
    print("training started")
    net = init_network([784,28,10])
    i = 0
    while True:
        
        labels, images = load_data()
        
        for img, lbl in zip(images, labels):
            print(img.shape, lbl, encode(lbl))
            time.sleep(1)
            #break
            net, err = Update(*net, model_input=img, labels=encode(lbl), learning_rate=0.3)
            #print(err)
        if i%50 ==0:
            list_of_lists = [[i.tolist() for i in arr] for arr in net]
            #print(list_of_lists)
            
            with open(os.path.join(os.getcwd(), f'app/static/net/net.npy'), 'wb') as f:
                np.save(f, np.array(net, dtype = "object"))
                
            
            i = 0
        i+=1
        #break
            