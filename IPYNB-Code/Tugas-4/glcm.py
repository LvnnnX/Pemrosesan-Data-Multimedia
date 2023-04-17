from skimage import io
from skimage.feature import graycomatrix, graycoprops
import pandas as pd
import numpy as np
from pathlib import Path

PATH = Path(__file__).parent.parent.parent #Membuat Base Directory, Karena berada pada PDM/IPYNB-Code/Tugas-3, harus keluar directory sebanyak 3x
DDIR = PATH / 'datasets' #Directory untuk datasets

def get_glcm(image, derajat=0, jarak=1): #Fungsi untuk menghitung glcm
    derajat_acc = [0, 45, 90, 135] #Daftar derajat yang dikenali
    if(derajat not in derajat_acc): #Jika derajat tidak dikenali
        print('Derajat tidak dikenali')
        return
    image_max = np.max(image) #Mencari nilai maksimum pada gambar
    print(image_max)
    glcm_matrix = np.zeros((image_max+1, image_max+1), dtype=int) #Membuat matrix dengan ukuran (image_max+1, image_max+1) dengan tipe data integer
    if(derajat == 0):
        for i in range(image.shape[0]-jarak):
            for j in range(image.shape[1]-jarak):
                glcm_matrix[image[i,j], image[i+jarak,j+jarak]] += 1 #Menghitung glcm
    elif(derajat == 45):
        for i in range(image.shape[0]-jarak):
            for j in range(jarak, image.shape[1]):
                glcm_matrix[image[i,j], image[i+jarak,j-jarak]] += 1 #Menghitung glcm
    elif(derajat == 90):
        for i in range(image.shape[0]-jarak):
            for j in range(image.shape[1]):
                glcm_matrix[image[i,j], image[i+jarak,j]] += 1 #Menghitung glcm
    else:
        for i in range(image.shape[0]-jarak):
            for j in range(image.shape[1]-jarak):
                glcm_matrix[image[i,j], image[i+jarak,j+jarak]] += 1 #Menghitung glcm
 
    glcm_transposed = glcm_matrix.T #Membuat transpose dari matrix glcm
    glcm_matrix = glcm_matrix + glcm_transposed #Menghitung glcm dengan transpose
    glcm_all_value = np.sum(glcm_matrix) #Menghitung jumlah semua nilai pada matrix glcm
    glcm_matrix = glcm_matrix / glcm_all_value #Menghitung glcm dengan jumlah semua nilai pada matrix glcm
    return glcm_matrix #Mengembalikan nilai glcm

def calc_glcm_all_agls(img, label, props, dists=[5], agls=[0, np.pi/4, np.pi/2, 3*np.pi/4], lvl=256, sym=True, norm=True): #Fungsi untuk menghitung glcm dengan semua derajat
        glcm = graycomatrix(img,  # image
                        distances=dists, 
                        angles=agls, 
                        levels=lvl,
                        symmetric=sym, 
                        normed=norm)
        # idms = [idm(p) for p in glcm]
        feature = [] #Membuat list kosong untuk menampung nilai feature
        glcm_props = [propery for name in props for propery in graycoprops(glcm, name)[0]] #Menghitung nilai feature
        for item in glcm_props: #Mengambil nilai feature
                feature.append(item)
        feature.append(label) 

        return glcm,feature #Mengembalikan nilai glcm dan feature

def inverse_difference_moment(matrix): #Fungsi untuk menghitung inverse difference moment
    rows, cols, a, all_b = matrix.shape #Mengambil ukuran matrix
    idms=[] 
    for b in range(all_b): 
        idm = 0.0
        for i in range(rows):
            for j in range(cols):
                idm += matrix[i][j][a-1][b] / (1 + (i - j)**2) #Menghitung inverse difference moment
        idms.append(idm)
    return idms #Mengembalikan nilai inverse difference moment

def entropy(matrix): #Fungsi untuk menghitung entropy
    all_entropy = []
    new_matrix = np.squeeze(matrix) #Menghilangkan dimensi yang tidak diperlukan
    for i in range(len(new_matrix)): 
        a,b,c = new_matrix[i].shape #Mengambil ukuran matrix
        list_entropy = []
        for i in range(c):
            entropy = -np.sum(new_matrix[:][:][i]*np.log2(new_matrix[:][:][i] + (new_matrix[:][:][i]==0))) #Menghitung entropy
            list_entropy.append(entropy)
        all_entropy.append(list_entropy)
    return all_entropy #Mengembalikan nilai entropy

def run_glcm(type:str, num_allowed:list) -> pd.DataFrame: #Fungsi untuk menjalankan glcm
    image_name = []
    all_image = []
    for num,value in enumerate(num_allowed):
        image_name.append(f'{type}-{value:04d}') #Membuat nama gambar
        all_image.append(io.imread(f'{DDIR}/{type}/{type}-{value:04d}.jpg')) #Membaca gambar

    properties = ['dissimilarity', 'correlation', 'homogeneity', 'contrast', 'ASM', 'energy'] #Daftar properti yang dikenali

    all_matrix = []
    glcm_all_agls = []
    for img, label in zip(all_image, image_name): 
        matrix, feature = calc_glcm_all_agls(img,label,props=properties) #Menghitung glcm dengan semua derajat
        glcm_all_agls.append(feature) #Menambahkan nilai feature ke list
        all_matrix.append(matrix) #Menambahkan nilai matrix ke list
        
    columns = []
    angles = ['0', '45', '90','135']
    for name in properties :
        for ang in angles:
            columns.append(name + "_" + ang) #Membuat nama kolom
            
    columns.append("label") #Menambahkan nama kolom label

    glcm_df = pd.DataFrame(glcm_all_agls, columns=columns) #Membuat dataframe

    #TODO IDM
    get_idms = [inverse_difference_moment(x) for x in all_matrix] #Menghitung inverse difference moment
    glcm_df['idm_0'] = [x[0] for x in get_idms]
    glcm_df['idm_45'] = [x[1] for x in get_idms]
    glcm_df['idm_90'] = [x[2] for x in get_idms]
    glcm_df['idm_135'] = [x[3] for x in get_idms]

    #TODO Entropy
    get_entropy = entropy(all_matrix) #Menghitung entropy
    glcm_df['entropy_0'] = [x[0] for x in get_entropy]
    glcm_df['entropy_45'] = [x[1] for x in get_entropy]
    glcm_df['entropy_90'] = [x[2] for x in get_entropy]
    glcm_df['entropy_135'] = [x[3] for x in get_entropy]

    #TODO ASM lowercase
    glcm_df.rename(columns={'ASM_0':'asm_0', 'ASM_45':'asm_45', 'ASM_90':'asm_90', 'ASM_135':'asm_135'}, inplace=True) #Mengubah nama kolom

    #TODO label as index
    glcm_df.index=glcm_df['label']
    glcm_df.drop(columns=['label'], inplace=True)   
    glcm_df = glcm_df.T #Membuat transpose dari dataframe
    return glcm_df #Mengembalikan dataframe