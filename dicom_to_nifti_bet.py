import fastr
import os, sys
import pathlib

worteldir1 = ('/home/ghitharie/dcm-bestanden')
worteldir2 = ('/home/ghitharie/dcm-bestanden 
worteldir3 = 
worteldir4 =
dicom_images_t1 = []
dicom_images_t2 = []
dicom_images_flair = []
dicom_images_t1gd = []
T1_mensen = []
T2_mensen = []
Flair_mensen = []
T1GD_mensen = []
dcm_totaal = []
dcm_t1 = []
dcm_t2 = []
dcm_flair = []
dcm_t1gd = []


def create_network():
    network = fastr.create_network(id='offical_fastr_test_giovanni_v2', version='1.0')
    source1 = network.create_source('DicomImageFile_t1' ,id='mri_t1')
    source2 = network.create_source('DicomImageFile_t2',id='mri_t2')
    source3 = network.create_source('DicomimageFile_flair',id='mri_flair')
    source4 = network.create_source('DicomimageFile_t1gd',id='mri_t1gd')
    node1 = network.create_node('dcm2nii/DicomToNifti:0.1', id='DicomToNifti', tool_version='0.1')
    node2 = network.create_node('fsl/Bet:5.0.9', id='fslbet', tool_version='0.2')
    node3 = network.create_node('dcm2nii/DicomToNifti:0.1', id='DicomToNifti', tool_version='0.1')
    node4 = network.create_node('fsl/Bet:5.0.9', id='fslbet', tool_version='0.2')
    node5 = network.create_node('dcm2nii/DicomToNifti:0.1', id='DicomToNifti', tool_version='0.1')
    node6 = network.create_node('fsl/Bet:5.0.9', id='fslbet', tool_version='0.2')
    node7 = network.create_node('dcm2nii/DicomToNifti:0.1', id='DicomToNifti', tool_version='0.1')
    node8 = network.create_node('fsl/Bet:5.0.9', id='fslbet', tool_version='0.2')
    sink1 = network.create_sink('NiftiImageFile', id='brain_t1')
    sink2 = network.create_sink('NiftiImageFile', id='nonbrain_t1')
    sink3 = network.create_sink('NiftiImageFile', id='brain_t2')
    sink4 = network.create_sink('NiftiImageFile', id='nonbrain_t2')
    sink5 = network.create_sink('NiftiImageFile', id='brain_flair')
    sink6 = network.create_sink('NiftiImageFile', id='nonbrain_flair')
    sink7 = network.create_sink('NiftiImagefile', id='brain_t1gd')
    sink8 = network.create_sink('NiftiImageFile', id='nonbrain_t1gd')
    
    link1 = source1.output >> node1.inputs['dicom_image_t1']
    link2 = source2.output >> node3.inputs['dicom_image_t2']
    link3 = source3.output >> node5.inputs['dicom_image_flair']
    link4 = source4.output >> node7.inputs['dicom_image_t1gd']
    link5 = node1.outputs['image_t1'] >> node2.inputs['image_t1']
    link6 = node3.outputs['image_t2'] >> node4.inputs['image_t2']
    link7 = node5.outputs['image_flair'] >> node6.inputs['image_flair']
    link8 = node7.outputs['image_t1gd'] >> node8.inputs['image_t1gd']
    link9 = node1.outputs['image_t1'] >> sink1.input
    link10 = node3.outputs['image_t2'] >> sink3.input
    link11 = node5.outputs['image_flair'] >> sink5.input
    link12 = node7.outputs['image_t1gd'] >> sink7.input
    link13 = node2.outputs['mask_image_t1'] >> sink2.input
    link14 = node4.outputs['mask_image_t2'] >> sink4.input
    link15 = node6.outputs['mask_image_flair'] >> sink6.input
    link16 = node8.outputs['mask_image_t1gd'] >> sink8.input
    return network

def path_source1():
    for subdir, dirs, files in os.walk(worteldir1):
        for file in files:
            filepath = subdir + os.sep + file
            if filepath.endswith(".dcm"):
                dicom_images.append(filepath)
        if os.path.basename(subdir) == 'DICOM':
            dcm.append(subdir)
    dirs = os.listdir(worteldir)
        for file in dirs:
            T1_mensen.append(file)
path_source()

def path_source2():
    for subdir, dirs, files in os.walk(worteldir2):
        for file in files:
            filepath = subdir + os.sep + file
            if filepath.endswith(".dcm"):
                dicom_images.append(filepath)
        if os.path.basename(subdir) == 'DICOM':
            dcm.append(subdir)
    dirs = os.listdir(worteldir)
        for file in dirs:
            mensen.append(file)
path_source()

def path_source3():
    for subdir, dirs, files in os.walk(worteldir3):
        for file in files:
            filepath = subdir + os.sep + file
            if filepath.endswith(".dcm"):
                dicom_images.append(filepath)
        if os.path.basename(subdir) == 'DICOM':
            dcm.append(subdir)
    dirs = os.listdir(worteldir)
        for file in dirs:
            mensen.append(file)
path_source()

def path_source4():
    for subdir, dirs, files in os.walk(worteldir4):
        for file in files:
            filepath = subdir + os.sep + file
            if filepath.endswith(".dcm"):
                dicom_images.append(filepath)
        if os.path.basename(subdir) == 'DICOM':
            dcm.append(subdir)
    dirs = os.listdir(worteldir)
        for file in dirs:
            mensen.append(file)
path_source()

def source_data():
    res = [sub.replace('/home/ghitharie', 'vfs://home') for sub in dcm]
    return {'mri':res}
  
def sink_data():
    
    return {'brain': 'vfs://home/DICOM-IMAGES/stripped{sample_id}.nii.gz',
            'nonbrain': 'vfs://home/DICOM-IMAGES/image{sample_id}.nii.gz'}
     
def main():
    network = create_network()
    network.draw()
    network.execute(source_data(), sink_data())

if __name__ == '__main__':
    main()
    
print("Aantal T1 afbeeldingen omgezet naar nifti:", dicom_images_t1)
print("Aantal T2 afbeeldingen omgezet naar nifti:", dicom_images_t2)
print("Aantal Flair beelden omgezet naar nifti:", dicom_images_flair)
print("Aantal T1GD beelden omgezet naar nifti:", dicom_images_gd)
print("Aantal mensen T1:", T1_mensen)
print("Aantal mensen T2:", T2_mensen)
print("Aantal mensen Flair:", Flair_mensen)
print("Aantal mensen T1GD:", T1GD_mensen)
