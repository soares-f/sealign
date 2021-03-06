from embedding_related import *
import numpy as np




#----------------------------- user inputs ----------------------------------------------------------------------
print('insert src fastText model path\n')
src_path = input( )
print('insert tgt fastText model path')
tgt_path = input()

print('insert src text path')
src_txt = input( )
print('insert tgt text path')
tgt_txt = input()


en_in = open(src_txt, encoding='utf8').readlines()
es_in = open(tgt_txt, encoding='utf8').readlines()


#---------------loading word2vec models -----------------------------------------------------------------------

print('\nloading models ...')
src_model = gensim.models.KeyedVectors.load_word2vec_format(src_path)
print('\nsrc model loaded')
tgt_model = gensim.models.KeyedVectors.load_word2vec_format(tgt_path)
print('\ndone')
#---------------------------------------------------------------------------------------------------------------

#raw input will be used later
english_text = load_care(en_in,src_model,'english',stop_w == False)
spanish_text = load_care(es_in,tgt_model,'spanish',stop_w == False)

#sentences distance matrix
matrix = generate_matrix(src_model, tgt_model, english_text, spanish_text,txt = 'yes')

#list with the min value index of each column
spanish_index = np.argmin(matrix,axis = 0)

"""generate bilingual aligned sentences in a txt file
   format:  sentence1   tab   sentence 2    tab   result  lf
"""
out = open('./results/aligned_out.txt',"w+",encoding = 'utf-8')
for ind in range(0,len(english_text)):
    out.write(en_in[ind].replace('\n','\t'))
    out.write(es_in[spanish_index[ind]].replace('\n','\t'))
    out.write(str(np.min(matrix[spanish_index[ind]],axis = 0)) + '\n')

#distance matrix result output

result = matrix_evaluation(matrix)
out_result = open('./results/matrix_result.txt',"w+",encoding = 'utf-8')
out_result.write('matrix evaluation: ' + str(result))
out_result.write('\nnumber of sentences:\nsrc: '+ str(len(en_in)) +'\ntgt: ' + str(len(es_in)))