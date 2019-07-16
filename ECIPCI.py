import numpy as np
import scipy as sp
import scipy.sparse as sparse

example_link = [[0,0], [0,1], [0,2], [0,3], [1,1], [2,2], [2,3], [3,3]]
example_size = (4, 4)

def matAB(links, size):
    country_size, product_size = size
    out_degree_country = [0] * country_size
    out_degree_product = [0] * product_size
    
    for i,j in links:
        out_degree_country[i] += 1
        out_degree_product[j] += 1
    #print('degree counted')
    matA = sparse.dok_matrix((country_size,product_size))
    matB = sparse.dok_matrix((country_size, product_size))
    #print('initial matrix')
    for i,j in links:
        matA[i, j] = 1. / out_degree_country[i]
        matB[i, j] = 1. / out_degree_product[j]
    #print('mat made')
    return matA, matB.T, out_degree_country, out_degree_product

def IterProcess(matA, matB, initC, initP, n=1):
    eci = np.array(initC)
    pci = np.array(initP)
    dt = int(n / 10)
    
    for i in range(n):
        eci = matA * pci
        pci = matB * eci
        
        eci = matA * pci
        pci = matB * eci
        
        eci = eci - np.mean(eci)
        eci = eci / np.std(eci)
        pci = pci - np.mean(pci)
        pci = pci / np.std(pci)
        if (i + 1) % dt == 0:
            print(100 * (i + 1) / n, '%')
    pci = matB * eci
    pci = pci - np.mean(pci)
    pci = pci / np.std(pci)
    
    return eci, pci

def ECI_PCI(links, size, iter_n=1):
    print('making matrix...')
    ma, mb, initc, initp = matAB(links, size)
    print('computing eci & pci...')
    return IterProcess(ma, mb, initc, initp, n=iter_n)
