import json
import xnat
import numpy as np
import argparse

#TYPES = ['FLAIR', 'T1', 'T1GD', 'T2']
TYPES = ['T1']

def select_scans(xnat_host, xnat_project, result_filename='selected.json'):
    data_to_download = {}
    not_suitable = []
    with xnat.connect(xnat_host) as connection:
        xnat_project = connection.projects[xnat_project]
        for subj in xnat_project.subjects:
            xnat_subject = xnat_project.subjects[subj]

            for exp in xnat_subject.experiments:
                xnat_experiment = xnat_subject.experiments[exp]

                selected = select_from_exp(xnat_experiment)
                label = xnat_experiment.label
                if selected == -1:
                    not_suitable.append(label)
                else:
                    data_to_download[label] = selected

    with open(result_filename, 'w+') as f:
        json.dump(data_to_download, f)
    return data_to_download

def select_from_exp(xnat_experiment):
    potential = {t:[] for t in TYPES}
    selected = {t:[] for t in TYPES}
    for sc in xnat_experiment.scans:
        xnat_scan = xnat_experiment.scans[sc]
        if 'DICOM' in xnat_scan.resources:
            #print(xnat_scan.type)
            for t in TYPES:
                if t + '_' in xnat_scan.type:
                    potential[t].append(xnat_scan.id)

    for t in TYPES:
        if len(potential[t]) == 0:
            ## apparently this sequence is not available
            return -1
        selected_id = select_from_type(potential[t], xnat_experiment)
        selected[t] = xnat_experiment.scans[selected_id].external_uri()
    return selected

def select_from_type(list_of_ids, xnat_experiment):
    if len(list_of_ids) == 1:
        return list_of_ids[0]
    # SELECT ON ORIENTATION
    else:
        selected = [d for d in list_of_ids if '3D' in xnat_experiment.scans[d].type]
    if len(selected) == 0:
        selected = [d for d in list_of_ids if 'Ax' in xnat_experiment.scans[d].type]
    if len(selected) == 0:
        selected = list_of_ids
    num_files = [len(xnat_experiment.scans[sc].resources['DICOM'].files) for sc in selected]
    return selected[np.argmax(num_files)]

def convert_to_fastr_source(dict_of_experiments, result_filename = 'fastr_source.json'):
    result = {t:{} for t in TYPES}
    for exp in dict_of_experiments:
        for t in TYPES:
            result[t][exp] = dict_of_experiments[exp][t].replace('https://', 'xnat://') + '/resources/DICOM/files'

    with open(result_filename, 'w+') as f:
        json.dump(result, f)
    print(result)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Select scans for segmentation from a sorted XNAT repository.')
    parser.add_argument('xnathost', help='url of xnat.')
    parser.add_argument('project', help='project id')

    args = parser.parse_args()
    dict_of_experiments = select_scans(args.xnathost, args.project)
    fastr_source = convert_to_fastr_source(dict_of_experiments)
