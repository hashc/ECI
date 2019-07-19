import numpy as np
import scipy.sparse.linalg 
import scipy
from scipy import sparse
import time
def timelogger(func):
    def inner(*args, **kwargs): #1
        start = time.perf_counter()
        res = func(*args, **kwargs) 
        print("==Time %.2f=="%(time.perf_counter()-start))
        return func(*args, **kwargs) #2
    return inner
@timelogger
def RCA(Xcp):
    """
    Xcp is a numpy.matrix type
    --|steel|oil|chip|bean|clothes
    --|--|--|--|--|--
    USA|1|1|1|1|0
    China|1|0|0|1|1
    Viet Nam|0|0|0|1|1
    """
    if type(Xcp) is not np.matrix:
        if type(Xcp) is np.array or list:
            Xcp = np.matrix(Xcp)
        else:
            raise ValueError('Xcp must be matrix')
    else:
        pass
    B = Xcp.sum(1)*Xcp.sum(0) 
    Sum = Xcp.sum()
    R= Xcp*Sum/B
    R[R>=1]=1
    R[R<1]=0
    return R.astype(float)
@timelogger
def RCA_sparse(M):
    B = M.sum(1)*M.sum(0) 
    Sum = M.sum()
    R = sparse.lil_matrix(M*Sum/B)
    R[R>=1]=1
    R[R<1]=0
    R = R.tocsc()
    return R

@timelogger
def Get_eci_pci(M):
    d = M.sum(1).T.tolist()[0]
    u = M.sum(0).tolist()[0]
    D = np.diag([1.0/i if i>0 else 0. for i in d])
    U = np.diag([1.0/i if i>0 else 0. for i in u])
    mcp1 = D * M
    mcp2 = M * U
    
    Mcc = mcp1 * mcp2.T
    Mpp = mcp2.T * mcp1
    eigvals, eigvecs = np.linalg.eig(Mpp)
    eigvecs = np.real(eigvecs)
    # Get eigenvector corresponding to second largest eigenvalue
    eig_index = eigvals.argsort()[-2]
    kp = eigvecs[:, eig_index]
    kc = mcp1 @ kp
    s1 = np.sign(np.corrcoef(M.sum(1).reshape(-1), kc.reshape(-1))[0, 1])
    eci = s1 * kc
    pci = s1 * kp  
    return {'eci':Get_z_score(eci.T.tolist()[0]),'pci':Get_z_score(pci.T.tolist()[0])}
@timelogger
def Get_eci_pci_sparse(M,third_eig=False):
    d = M.sum(1).T.tolist()[0]
    u = M.sum(0).tolist()[0]
    nd,nu = len(d),len(u)
    D1 = scipy.sparse.csc_matrix(([1.0/i if i>0 else 0. for i in d], (range(nd), range(nd))),shape=(nd,nd))
    U1 = scipy.sparse.csc_matrix(([1.0/i if i>0 else 0. for i in u], (range(nu), range(nu))),shape=(nu,nu))
    M = sparse.csc_matrix(M)
    mcp1 = D1 * M
    del D1
    del d
    del u
    mcp2 = M * U1
    del U1
    #Mcc = mcp1 @ mcp2.T
    Mpp = mcp2.T * mcp1
    Mpp = scipy.sparse.csc_matrix(Mpp)
    eigvals, eigvecs = scipy.sparse.linalg.eigs(Mpp, k=3)
    eigvecs = np.real(eigvecs)
    # Get eigenvector corresponding to second largest eigenvalue
    eig_index2 = eigvals.argsort()[-2]
    kp2 = eigvecs[:, eig_index2]
    kc2 = mcp1 * kp2
    s2 = np.sign(np.corrcoef(M.sum(1).reshape(-1), kc2.reshape(-1))[0, 1])
    eci2 = s2 * kc2
    pci2 = s2 * kp2
    Dict={"eci":Get_z_score(eci2),'pci':Get_z_score(pci2)}
    if third_eig:
        eigvals, eigvecs = scipy.sparse.linalg.eigs(Mpp, k=3)
        eig_index3 = eigvals.argsort()[-3]
        kp3 = eigvecs[:, eig_index3]
        kc3 = mcp1 * kp3
        s3 = np.sign(np.corrcoef(M.sum(1).reshape(-1), kc2.reshape(-1))[0, 1])
        eci3 = s3 * kc3
        pci3 = s3 * kp3
        Dict={"eci":Get_z_score(eci2),'pci':Get_z_score(pci2),'eci3':Get_z_score(eci3),'pci3':Get_z_score(pci3)}
    return Dict

def Get_z_score(x):
    x=np.array(x)
    std=np.std(x)
    mean=np.mean(x)
    return (x-mean)/std