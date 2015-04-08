'''
Created on 8.4.2015

@author: Ondrej
'''

import numpy as np
import warnings

def calcWeightVector(matrix):
    eigenvalues, eigenvector=np.linalg.eig(matrix)
    warnings.simplefilter("ignore", np.ComplexWarning)
    maxindex=np.argmax(eigenvalues)
    eigenvalues=np.float32(eigenvalues)
    eigenvector=np.float32(eigenvector)
    weight=eigenvector[:, maxindex] #extract vector from eigenvector with max vaue in eigenvalues
    weight.tolist() #convert array(numpy)  to vector
    weight=[ w/sum(weight) for w in weight ]
    return weight

def calcWeightMatrix(leftArray, topArray, votes, parentCrit = None):
    weightMatrix = np.eye(len(leftArray), len(topArray))
    for i, left in enumerate(leftArray):
        for j, right in enumerate(topArray):
            if weightMatrix[i,j] == 0:
                qs = votes.filter(critVarLeft=left, critVarRight=right, parentCrit=parentCrit)
                valueArray = []
                for vote in qs:
                    for w in range(0, vote.user.weight):
                        valueArray.append(vote.value)
                if len(qs) > 0:
                    value = np.median(valueArray)
                    weightMatrix[i,j] = value;
                    weightMatrix[j,i] = 1/value;                
    print weightMatrix
    return weightMatrix

def calcCriteriaWeight(criterias, votes):
    return calcWeightVector(calcWeightMatrix(criterias, criterias, votes))