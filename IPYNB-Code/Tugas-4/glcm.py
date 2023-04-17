from skimage import io
from skimage.feature import graycomatrix, graycoprops
import pandas as pd
import numpy as np
from pathlib import Path

PATH = Path(__file__).parent.parent.parent
DDIR = PATH / 'datasets'

def get_glcm(image, derajat=0, jarak=1):
    derajat_acc = [0, 45, 90, 135]
    if(derajat not in derajat_acc):
        print('Derajat tidak dikenali')
        return
    image_max = np.max(image)
    print(image_max)
    glcm_matrix = np.zeros((image_max+1, image_max+1), dtype=int)
    if(derajat == 0):
        for i in range(image.shape[0]-jarak):
            for j in range(image.shape[1]-jarak):
                glcm_matrix[image[i,j], image[i+jarak,j+jarak]] += 1
    elif(derajat == 45):
        for i in range(image.shape[0]-jarak):
            for j in range(jarak, image.shape[1]):
                glcm_matrix[image[i,j], image[i+jarak,j-jarak]] += 1
    elif(derajat == 90):
        for i in range(image.shape[0]-jarak):
            for j in range(image.shape[1]):
                glcm_matrix[image[i,j], image[i+jarak,j]] += 1
    else:
        for i in range(image.shape[0]-jarak):
            for j in range(image.shape[1]-jarak):
                glcm_matrix[image[i,j], image[i+jarak,j+jarak]] += 1

    glcm_transposed = glcm_matrix.T
    glcm_matrix = glcm_matrix + glcm_transposed
    glcm_all_value = np.sum(glcm_matrix)
    glcm_matrix = glcm_matrix / glcm_all_value
    return glcm_matrix

def calc_glcm_all_agls(img, label, props, dists=[5], agls=[0, np.pi/4, np.pi/2, 3*np.pi/4], lvl=256, sym=True, norm=True):
        glcm = graycomatrix(img, 
                        distances=dists, 
                        angles=agls, 
                        levels=lvl,
                        symmetric=sym, 
                        normed=norm)
        # idms = [idm(p) for p in glcm]
        feature = []
        glcm_props = [propery for name in props for propery in graycoprops(glcm, name)[0]]
        for item in glcm_props:
                feature.append(item)
        feature.append(label) 

        return glcm,feature

def inverse_difference_moment(matrix):
    rows, cols, a, all_b = matrix.shape
    idms=[]
    for b in range(all_b):
        idm = 0.0
        for i in range(rows):
            for j in range(cols):
                idm += matrix[i][j][a-1][b] / (1 + (i - j)**2)
        idms.append(idm)
    return idms

def entropy(matrix):
    all_entropy = []
    new_matrix = np.squeeze(matrix)
    for i in range(len(new_matrix)):
        a,b,c = new_matrix[i].shape
        list_entropy = []
        for i in range(c):
            entropy = -np.sum(new_matrix[:][:][i]*np.log2(new_matrix[:][:][i] + (new_matrix[:][:][i]==0)))
            list_entropy.append(entropy)
        all_entropy.append(list_entropy)
    return all_entropy

def run_glcm(type:str, num_allowed:list) -> pd.DataFrame:
    image_name = []
    all_image = []
    for num,value in enumerate(num_allowed):
        image_name.append(f'{type}-{value:04d}')
        all_image.append(io.imread(f'{DDIR}/{type}/{type}-{value:04d}.jpg'))

    properties = ['dissimilarity', 'correlation', 'homogeneity', 'contrast', 'ASM', 'energy']

    all_matrix = []
    glcm_all_agls = []
    for img, label in zip(all_image, image_name): 
        matrix, feature = calc_glcm_all_agls(img,label,props=properties)
        glcm_all_agls.append(feature)
        all_matrix.append(matrix)
        
    columns = []
    angles = ['0', '45', '90','135']
    for name in properties :
        for ang in angles:
            columns.append(name + "_" + ang)
            
    columns.append("label")

    glcm_df = pd.DataFrame(glcm_all_agls, columns=columns)

    #TODO IDM
    get_idms = [inverse_difference_moment(x) for x in all_matrix]
    glcm_df['idm_0'] = [x[0] for x in get_idms]
    glcm_df['idm_45'] = [x[1] for x in get_idms]
    glcm_df['idm_90'] = [x[2] for x in get_idms]
    glcm_df['idm_135'] = [x[3] for x in get_idms]

    #TODO Entropy
    get_entropy = entropy(all_matrix)
    glcm_df['entropy_0'] = [x[0] for x in get_entropy]
    glcm_df['entropy_45'] = [x[1] for x in get_entropy]
    glcm_df['entropy_90'] = [x[2] for x in get_entropy]
    glcm_df['entropy_135'] = [x[3] for x in get_entropy]

    #TODO ASM lowercase
    glcm_df.rename(columns={'ASM_0':'asm_0', 'ASM_45':'asm_45', 'ASM_90':'asm_90', 'ASM_135':'asm_135'}, inplace=True)

    #TODO label as index
    glcm_df.index=glcm_df['label']
    glcm_df.drop(columns=['label'], inplace=True)   
    glcm_df = glcm_df.T
    return glcm_df