'''
    Parameters: 
        Flags:
        1. To cluster data.
            --input: Name of the input jsonl file.
            --k: Number of clusters
        2. To create mapping file and recreate the refined dataset in json format.
            --path: Path of the output folder created after 1st command.
        
    Commands: 
        1. python3 sentence_clustering.py --input input_file(.jsonl) --k no_of_cluster
        2. python3 sentence_clustering.py --path path_to_output_folder_crated_in_command_one(input_file_Cluster_Output)

    Example command: 
        1. python3 sentence_clustering.py --input lab_hosp_20_jun.jsonl --k 10
        2. python3 sentence_clustering.py --path /home/chitranshbose/Downloads/python_prac/lab_hosp_20_jun_Cluster_Output
    
    Output Folder: input_file_Cluster_Output
    Example: lab_hosp_20_jun_Cluster_Output
'''
import numpy as np
import re
import spacy
import json
import os
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import wordnet
from sklearn.cluster import kmeans_plusplus, KMeans
import argparse

stop_words = nltk.corpus.stopwords.words('english')
lemma = WordNetLemmatizer()
nlp_lg = spacy.load('en_core_web_lg')
def preprocess(sent):
    sent = sent.lower()
    patt1 = r"\d{2}-\w{3}-\d{4}"
    patt2 = r"\d{2}\w{3}\d{4}"
    patt3 = r"\d{2} \w{3} \d{4}"
    patt4 = r"\d{2}\w{3}\d{2}"
    patt5 = r"[0-9]"
    sent = re.sub(patt1, "", sent)
    sent = re.sub(patt2, "", sent)
    sent = re.sub(patt3, "", sent)
    sent = re.sub(patt4, "", sent)
    sent = re.sub(patt5, "", sent)
    token_obj = RegexpTokenizer(r'\w+')
    words = token_obj.tokenize(sent)
    pos_tag = nltk.pos_tag(words)
    lemmatized_words = []
    for x in pos_tag:
        if x[1].startswith('J'):
            lemmatized_words.append(lemma.lemmatize(x[0], wordnet.ADJ))
        elif x[1].startswith('V'):  
            lemmatized_words.append(lemma.lemmatize(x[0], wordnet.VERB))
        elif x[1].startswith('N'):
            lemmatized_words.append(lemma.lemmatize(x[0], wordnet.NOUN))
        elif x[1].startswith('R'):
            lemmatized_words.append(lemma.lemmatize(x[0], wordnet.ADV))
        else:
            lemmatized_words.append(lemma.lemmatize(x[0]))
                    
    words = [wrd for wrd in lemmatized_words if wrd not in stop_words] 
            
    return ' '.join(words)
    
def cluster(vectors, no_of_clust):
    if len(vectors) < no_of_clust:
        no_of_clust = len(vectors)//5
    cen, _ = kmeans_plusplus(vectors, n_clusters = no_of_clust,random_state=42)
    km = KMeans(n_clusters = no_of_clust, init = cen, random_state = 42)
    clust = km.fit_predict(vectors)
    return clust, cen
def extract_features(features):
    vectors = []
    for sent in features:
        doc = nlp_lg(sent) 
        vectors.append(doc.vector)
    vectors = np.array(vectors)
    return vectors

def get_cluster_output(data, clust, vectors, no_of_clust, cen):
    
    clust_sent = {i:[] for i in range(no_of_clust)}
    repr_sent = {i:"" for i in range(no_of_clust)}
    repr_dist = {i:float('inf') for i in range(no_of_clust)}
        
    for sen, clus, embd in zip(data, clust, vectors):
      
        clust_sent[clus].append(sen)
        dist = np.linalg.norm(embd - cen[clus])
        if dist < repr_dist[clus]:
            repr_dist[clus] = dist
            repr_sent[clus] = sen
        
    for clus, sen in clust_sent.items():
           
            
        with open(output_file+str(clus+1)+'.txt','w') as f:
            for i, s in enumerate(sen):
                f.write(f"{s}\n")
                   
    return repr_sent, clust_sent, repr_dist


if __name__== "__main__":
    parse = argparse.ArgumentParser(description="""Sentence clusterin: Provide either --input and --k to cluster sentences or --path to generating dataset in json format and sentence: cluster mapping file.""")
    parse.add_argument("--input", help="Name of input file.")
    parse.add_argument("--k", help="Number of clusters.")
    parse.add_argument("--path", help="Path till the name of folder contaning clustered output.")
    argv = parse.parse_args()

    if argv.input and argv.k:
        no_of_clust = int(argv.k)
        input_file = argv.input
        name, ext = input_file.split('.')
        path = name+'_Cluster_Output/'
        print("Output folder: "+path)
        print("Starting process")
        if not os.path.exists(path):
            os.mkdir(path)
        output_file = path+name+'_Cluster_'
        datas = []
        with open(input_file, 'r') as file:
            for line in file:
                datas.append(json.loads(line))
            lst_data = []
            for data in datas:
                lst_data.append(data['text'])

        lst_data = list(set(lst_data))
        features_data = [preprocess(sent) for sent in lst_data]
        vector_data = extract_features(features_data)
        clust, cen = cluster(vector_data, no_of_clust)
        repr_sent_data, clust_sent_data, repr_dist_data = get_cluster_output(lst_data, clust, vector_data, no_of_clust, cen)

        print("Output generated.")

    elif argv.path:
        inp_dir = argv.path+'/'
        files = os.listdir(inp_dir)
        main_file_name = inp_dir.split('/')[-2].split("_Cluster")[0]+'.jsonl'
        datas = []
        with open(main_file_name, 'r') as file:
            for line in file:
                datas.append(json.loads(line))
            lst_data = []
            for data in datas:
                lst_data.append(data)
          
        final_sentences = []
        final_sentences_map = {}
        for file in files:
            if file.split(".")[1] == 'txt':
                cluster_no = file.split("Cluster_")[1].split(".")[0]
                with open(inp_dir+file, 'r') as f:
                    sent = [line.strip() for line in f]
                    for s in sent:
                        final_sentences.append(s)
                        final_sentences_map[s] = cluster_no
    
        final_output = [data for data in lst_data if data['text'] in final_sentences]
    
        obj = json.dumps(final_sentences_map, indent = 4)
        with open(inp_dir+"sentence_mapping.jsonl",'w') as f:
            f.write(obj)    
    
        obj = json.dumps(final_output, indent = 1)
        with open(inp_dir+"final_sentences.jsonl",'w') as f:
            f.write(obj)   
        print("Files created")
    else:
        print("Invalid arguments.")