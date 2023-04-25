from app.perceptron import *

def load_data():
    labels = []
    images = []
    try:
        for image in os.listdir(os.path.join(os.getcwd(), 'app/static/images')):

            labels.append(encode(int(image[0]))) #appends label to list of labels
            
            #opens image reshape it to (784, 1)
            images.append(np.max(np.asarray(Image.open(os.path.join(os.getcwd(), f'app/static/images/{image}'))), -1).reshape(-1, 1).astype(float)/256)
        
    except:
        #retries if there is error
        labels, images = load_data()
    #labels = encode(labels).T
    return labels, images

    


def run():
    import time
    print("training started")

    i = 0

    #try to open the file with pretrained network
    try:
        net = np.fromfile(os.path.join(os.getcwd(), f'app/static/net/net.npy'))
        net = (net[0], net[1])
    except:
        net = init_network([784,28,10])

    while True:
        #load data
        labels, images = load_data()
        
        #for every image in images, labels
        for img, lbl in zip(images, labels):
            
            
           
            net, err = Update(*net, model_input=img, labels=lbl, learning_rate=0.3)
            

        if i%50 ==0:
            
            with open(os.path.join(os.getcwd(), f'app/static/net/net.npy'), 'wb') as f:
                np.save(f, np.array(net, dtype = "object"))
                
            
            i = 0
        i+=1