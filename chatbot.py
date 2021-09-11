import numpy as np
import re
import pickle
from keras.models import Model
from keras.layers import Embedding, Dense, LSTM, Input
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model


word2idx = pickle.load(open('data/wordtoidx.pkl', 'rb'))
idx2word = pickle.load(open('data/idxtoword.pkl', 'rb'))


def contractions():
    short_w = open('data/short forms.txt', encoding= 'utf-8').read().split('\n')
    contraction = {}
    cont_list = []
    for el in short_w:
        el = el.replace('"' ,'')
        el = el.replace(',' ,'')
        key, value = el.split(':')
        value = value.lower()
        contraction[key] = value
        cont_list.append(key)
    return contraction, cont_list


def clean_text(el):
    el = el.lower()
    el = re.sub("[^a-zA-Z' ]", '', el)
    y = el.split()
    
    ## calling contractions() will return dict, list
    contraction, cont_list = contractions()
    
    for le in y:
        if(le in cont_list):
            el = el.replace(le, contraction[le])
    el = el.replace('  ', ' ')
    return el


def replyGenerator(user_input, modelpath, _print = False):

    model = load_model(modelpath)

    encoder_inputs = model.input[0]
    encoder_out, h, c = model.layers[4].output
    encoder_states = [h, c]
    encoder_model = Model([encoder_inputs], encoder_states)


    init_h = Input(shape=(256,), name='dec_input_h')
    init_c = Input(shape=(256,), name='dec_input_c')
    decoder_states_initial = [init_h, init_c]

    ## decoder lstm 
    decoder_inputs = model.input[1]
    embed_out = model.layers[3].output
    decoder_states_initial = [init_h, init_c]

    decoder_lstm = model.layers[5]
    decoder_out, dec_h, dec_c = decoder_lstm(embed_out, initial_state = decoder_states_initial)
    decoder_states_final = [dec_h, dec_c]

    decoder_model = Model([decoder_inputs]+ decoder_states_initial, [decoder_out] + decoder_states_final)

    dense = model.layers[6]


    cleaned_str = clean_text(user_input)
    user_text = []
    for word in cleaned_str.split():
        try:
            user_text.append(word2idx[word])
        except:
            user_text.append(0)

    user_text = pad_sequences([user_text], maxlen = 15, padding= 'post')
    states = encoder_model.predict(user_text)  ## encoder model will output states

    ## decoder_model expects <sos> and internal states of encoder model
    input_token_sos = np.zeros(shape=(1,1))
    input_token_sos[0,0] = word2idx['<sos>']

    stop_condition = False
    decoded_message = ''

    while not stop_condition:
        o, h, c = decoder_model.predict([input_token_sos] + states)

        dense_out = dense(o)
        sampled_index = np.argmax(dense_out)
        sampled_word = idx2word[sampled_index] + ' '

        if sampled_word != '<eos> ':
            decoded_message += sampled_word

        if sampled_word == '<eos> ' or len(decoded_message.split())> 15:
            stop_condition = True

        input_token_sos = np.zeros(shape=(1,1))
        input_token_sos[0,0] = sampled_index
        states = [h, c]

    if(_print):
        print('Computer : ', decoded_message)
    return decoded_message


