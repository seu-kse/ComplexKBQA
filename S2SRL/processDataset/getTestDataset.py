# coding:utf-8
'''Get all questions, annotated actions, entities, relations, types together in JSON format.
'''
from itertools import islice
import sys
import json
import os
#Python codes to read the binary files.
import numpy as np
LINE_SIZE = 100000
from random import shuffle

special_counting_characters = {'-','|','&'}
special_characters = {'(',')','-','|','&'}

# Get full-set test dataset.
def getTestDataset():
    # fwTrainQ = open('../../data/auto_QA_data/mask_test/FINAL_train.question', 'w', encoding="UTF-8")
    # fwTrainA = open('../../data/auto_QA_data/mask_test/FINAL_train.action', 'w', encoding="UTF-8")
    fwTestQ = open('../../data/auto_QA_data/mask_test/FINAL_test.question', 'w', encoding="UTF-8")
    fwTestA = open('../../data/auto_QA_data/mask_test/FINAL_test.action', 'w', encoding="UTF-8")
    with open("../../data/auto_QA_data/CSQA_ANNOTATIONS_test.json", 'r', encoding="UTF-8") as load_f:
        count = 1
        train_action_string_list, test_action_string_list, train_question_string_list, test_question_string_list = list(), list(), list(), list()
        dict_list = list()
        load_dict = json.load(load_f)
        for key, value in load_dict.items():
                question_string = '<E> '
                entities = value['entity_mask']
                if len(entities) > 0:
                    for entity_key, entity_value in entities.items():
                        if str(entity_value) != '':
                            question_string += str(entity_value) + ' '
                question_string += '</E> <R> '
                relations = value['relation_mask']
                if len(relations) > 0:
                    for relation_key, relation_value in relations.items():
                        if str(relation_value) !='':
                            question_string += str(relation_value) + ' '
                question_string += '</R> <T> '
                types = value['type_mask']
                if len(types) > 0:
                    for type_key, type_value in types.items():
                        if str(type_value) !='':
                            question_string += str(type_value) + ' '
                question_string += '</T> '
                question_token = str(value['question']).lower().replace('?', '')
                question_token = question_token.replace(',', ' ')
                question_token = question_token.replace(':', ' ')
                question_token = question_token.replace('(', ' ')
                question_token = question_token.replace(')', ' ')
                question_token = question_token.replace('"', ' ')
                question_token = question_token.strip()
                question_string += question_token
                question_string = question_string.strip() + '\n'
                action_string = '' + '\n'

                dict_temp = {}
                dict_temp.setdefault('q', str(key) + ' ' + question_string)
                dict_temp.setdefault('a', str(key) + ' ' + action_string)
                dict_list.append(dict_temp)

    # train_size = int(len(dict_list) * 0.95)
    train_size = int(len(dict_list))
    for i, item in enumerate(dict_list):
        if i < train_size:
            test_action_string_list.append(item.get('a'))
            test_question_string_list.append(item.get('q'))
        elif train_size <= i:
            train_action_string_list.append(item.get('a'))
            train_question_string_list.append(item.get('q'))
    # fwTrainQ.writelines(train_question_string_list)
    # fwTrainA.writelines(train_action_string_list)
    fwTestQ.writelines(test_question_string_list)
    fwTestA.writelines(test_action_string_list)
    # fwTrainQ.close()
    # fwTrainA.close()
    fwTestQ.close()
    fwTestA.close()
    print ("Getting test processDataset is done!")

# Get one-tenth samples from test dataset as sample test-dataset.
# LogicalReasoning: 20787; SimpleQuestion: 81994; QuantitativeReasoning: 27950; ComparativeReasoning: 15616; Verification: 10150;
# Total samples in test dataset is: 156497.
def getSampleTestDataset():
    fwTestQ = open('../../data/auto_QA_data/mask_test/SAMPLE_FINAL_test.question', 'w', encoding="UTF-8")
    fwTestA = open('../../data/auto_QA_data/mask_test/SAMPLE_FINAL_test.action', 'w', encoding="UTF-8")
    with open("../../data/auto_QA_data/CSQA_ANNOTATIONS_test.json", 'r', encoding="UTF-8") as load_f:
        count = 1
        train_action_string_list, test_action_string_list, train_question_string_list, test_question_string_list = list(), list(), list(), list()
        dict_list = list()
        load_dict = json.load(load_f)
        for key, value in load_dict.items():
                question_string = '<E> '
                entities = value['entity_mask']
                if len(entities) > 0:
                    for entity_key, entity_value in entities.items():
                        if str(entity_value) != '':
                            question_string += str(entity_value) + ' '
                question_string += '</E> <R> '
                relations = value['relation_mask']
                if len(relations) > 0:
                    for relation_key, relation_value in relations.items():
                        if str(relation_value) !='':
                            question_string += str(relation_value) + ' '
                question_string += '</R> <T> '
                types = value['type_mask']
                if len(types) > 0:
                    for type_key, type_value in types.items():
                        if str(type_value) !='':
                            question_string += str(type_value) + ' '
                question_string += '</T> '
                question_token = str(value['question']).lower().replace('?', '')
                question_token = question_token.replace(',', ' ')
                question_token = question_token.replace(':', ' ')
                question_token = question_token.replace('(', ' ')
                question_token = question_token.replace(')', ' ')
                question_token = question_token.replace('"', ' ')
                question_token = question_token.strip()
                question_string += question_token
                question_string = question_string.strip() + '\n'
                action_string = '' + '\n'

                dict_temp = {}
                dict_temp.setdefault('q', str(key) + ' ' + question_string)
                dict_temp.setdefault('a', str(key) + ' ' + action_string)
                count += 1
                if count%20==0:
                    dict_list.append(dict_temp)

    # train_size = int(len(dict_list) * 0.95)
    train_size = int(len(dict_list))
    for i, item in enumerate(dict_list):
        if i < train_size:
            test_action_string_list.append(item.get('a'))
            test_question_string_list.append(item.get('q'))
        elif train_size <= i:
            train_action_string_list.append(item.get('a'))
            train_question_string_list.append(item.get('q'))
    # fwTrainQ.writelines(train_question_string_list)
    # fwTrainA.writelines(train_action_string_list)
    fwTestQ.writelines(test_question_string_list)
    fwTestA.writelines(test_action_string_list)
    # fwTrainQ.close()
    # fwTrainA.close()
    fwTestQ.close()
    fwTestA.close()
    print ("Getting test processDataset is done!")

def getSampleTestDatasetForMAML():
    # Create target directory & all intermediate directories if don't exists
    dirName = '../../data/auto_QA_data/mask_test'
    if not os.path.exists(dirName):
        os.makedirs(dirName)
        print("Directory ", dirName, " Created ")
    else:
        print("Directory ", dirName, " already exists")
    path = dirName + '/SAMPLE_FINAL_MAML_test.question'
    fwTestQ = open(path, 'w', encoding="UTF-8")
    with open("../../data/auto_QA_data/CSQA_ANNOTATIONS_test.json", 'r', encoding="UTF-8") as load_f:
        count = 1
        dict_list = {}
        load_dict = json.load(load_f)
        list_of_load_dict = list(load_dict.items())
        # random.seed(SEED+4)
        # random.shuffle(list_of_load_dict)
        load_dict = dict(list_of_load_dict)
        for key, value in load_dict.items():
            orig_response, question = "", ""
            try:
                orig_response = value['orig_response']
                question = value['question']
            except SyntaxError:
                pass
            if len(orig_response) > 0 and len(question) >0:
                count += 1
                if count % 20 == 0:
                    dict_temp = value
                    question_string = '<E> '
                    entities = value['entity_mask']
                    if len(entities) > 0:
                        for entity_key, entity_value in entities.items():
                            if str(entity_value) != '':
                                question_string += str(entity_value) + ' '
                    question_string += '</E> <R> '
                    relations = value['relation_mask']
                    if len(relations) > 0:
                        for relation_key, relation_value in relations.items():
                            if str(relation_value) != '':
                                question_string += str(relation_value) + ' '
                    question_string += '</R> <T> '
                    types = value['type_mask']
                    if len(types) > 0:
                        for type_key, type_value in types.items():
                            if str(type_value) != '':
                                question_string += str(type_value) + ' '
                    question_string += '</T> '
                    question_token = str(value['question']).lower().replace('?', '')
                    question_token = question_token.replace(',', ' ')
                    question_token = question_token.replace(':', ' ')
                    question_token = question_token.replace('(', ' ')
                    question_token = question_token.replace(')', ' ')
                    question_token = question_token.replace('"', ' ')
                    question_token = question_token.strip()
                    question_string += question_token
                    question_string = question_string.strip()
                    dict_temp['input'] = question_string
                    dict_list[key] = dict_temp
    if len(dict_list) > 0:
        fwTestQ.writelines(json.dumps(dict_list, indent=1, ensure_ascii=False))
    fwTestQ.close()
    print ("Getting MAML processDataset is done!")

# Run getTestDataset to get the final test processDataset.
if __name__ == "__main__":
    # getTestDataset()
    # getSampleTestDataset()
    getSampleTestDatasetForMAML()




