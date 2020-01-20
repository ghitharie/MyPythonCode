import fastr
import json
import xnat
import os
import pathlib
import SimpleITK

def create_network():
    #With this piece of code you can make an empty network and give it a name
    network = fastr.create_network(id="dcm_nii_resample_v2", version='1.0')
    
    #With the lines of code I am creating all my sources. 
    #These sources are directories to an xnat server where a large amount of dicom images are stored. 
    #The links are stored in a .json file.
    
    source1 = network.create_source('Directory', id='mri_t1') 
    source2 = network.create_source('Directory', id='mri_t2')
    source3 = network.create_source('Directory', id='mri_t1gd')
    source4 = network.create_source('Directory', id='mri_flair')
    
    #With these lines of code I create my own nodes.
    
    node1 = network.create_node('dcm2niix/DicomToNifti:0.1', id='DicomToNifti_t1', tool_version='0.1')
    node2 = network.create_node('fsl/Bet:5.0.9', id='fslbet_t1', tool_version='0.2')
    node3 = network.create_node('dcm2niix/DicomToNifti:0.1', id='DicomToNifti_t2', tool_version='0.1')
    node4 = network.create_node('fsl/Bet:5.0.9', id='fslbet_t2', tool_version='0.2')
    node5 = network.create_node('dcm2niix/DicomToNifti:0.1', id='DicomToNifti_t1gd', tool_version='0.1')
    node6 = network.create_node('fsl/Bet:5.0.9', id='fslbet_t1gd', tool_version='0.2')
    node7 = network.create_node('dcm2niix/DicomToNifti:0.1', id='DicomToNifti_flair', tool_version='0.1')
    node8 = network.create_node('fsl/Bet:5.0.9', id='fslbet_flair', tool_version='0.2')
    
    node9 = network.create_node('custom/resample:0.1', id='resample_t1', tool_version='0.1')
    node10 = network.create_node('custom/resample:0.1', id='resample_t2', tool_version='0.1')
    node11 = network.create_node('custom/resample:0.1', id='resample_t1gd', tool_version='0.1')
    node12 = network.create_node('custom/resample:0.1', id='resample_flair', tool_version='0.1')
    
    sink1 = network.create_sink('NiftiImageFileCompressed', id='resampled_image_t1')
    sink2 = network.create_sink('NiftiImageFileCompressed', id='resampled_image_t2')
    sink3 = network.create_sink('NiftiImageFileCompressed', id='resampled_image_t1gd')
    sink4 = network.create_sink('NiftiImageFileCompressed', id='resampled_image_flair')
    sink5 = network.create_sink('NiftiImageFileCompressed', id='resampled_mask_t1')
    sink6 = network.create_sink('NiftiImageFileCompressed', id='resampled_mask_t2')
    sink7 = network.create_sink('NiftiImageFileCompressed', id='resampled_mask_t1gd')
    sink8 = network.create_sink('NiftiImageFileCompressed', id='resampled_mask_flair')
    
    link1 = source1.output >> node1.inputs['dicom_image']
    link2 = source2.output >> node3.inputs['dicom_image']
    link3 = source3.output >> node5.inputs['dicom_image']
    link4 = source4.output >> node7.inputs['dicom_image']
    
    link5 = node1.outputs['image'] >> node2.inputs['image']
    link6 = node3.outputs['image'] >> node4.inputs['image']
    link7 = node5.outputs['image'] >> node6.inputs['image']
    link8 = node7.outputs['image'] >> node8.inputs['image']
    
    link9 = node1.outputs['image'] >> node9.inputs['image']
    link10 = node3.outputs['image'] >> node10.inputs['image']
    link11 = node5.outputs['image'] >> node11.inputs['image']
    link12 = node7.outputs['image'] >> node12.inputs['image']
    link13 = node2.outputs['mask_image'] >> node9.inputs['mask']
    link14 = node4.outputs['mask_image'] >> node10.inputs['mask']
    link15 = node6.outputs['mask_image'] >> node11.inputs['mask']
    link16 = node8.outputs['mask_image'] >> node12.inputs['mask']
    
    link17 = node9.outputs['image_resampled'] >> sink1.input
    link18 = node10.outputs['image_resampled'] >> sink2.input
    link19 = node11.outputs['image_resampled'] >> sink3.input
    link20 = node12.outputs['image_resampled'] >> sink4.input
    
    link21 = node9.outputs['mask_resampled'] >> sink5.input
    link22 = node10.outputs['mask_resampled'] >> sink6.input
    link23 = node11.outputs['mask_resampled'] >> sink7.input
    link24 = node12.outputs['mask_resampled'] >> sink8.input
    return network
    
json_file = open("/home/ghitharie/MyPythonCodes/fastr_source_all.json", "r", encoding="utf-8")
dataset = json.load(json_file)

def source_data():
    return {'mri_t1':dataset["T1"],
            'mri_t2':dataset["T2"],
            'mri_t1gd':dataset["T1GD"],
            'mri_flair':dataset["FLAIR"]}


def sink_data():
    return {'resampled_image_t1':'vfs://scratch/TCGA_FSLBET_resampled/{sample_id}/t1.nii.gz',
            'resampled_image_t2':'vfs://scratch/TCGA_FSLBET_resampled/{sample_id}/t2.nii.gz',
            'resampled_image_t1gd':'vfs://scratch/TCGA_FSLBET_resampled/{sample_id}/t1gd.nii.gz',
            'resampled_image_flair':'vfs://scratch/TCGA_FSLBET_resampled/{sample_id}/flair.nii.gz',
            'resampled_mask_t1':'vfs://scratch/TCGA_FSLBET_resampled/{sample_id}/t1_mask.nii.gz',
            'resampled_mask_t2':'vfs://scratch/TCGA_FSLBET_resampled/{sample_id}/t2_mask.nii.gz',
            'resampled_mask_t1gd':'vfs://scratch/TCGA_FSLBET_resampled/{sample_id}/t1gd_mask.nii.gz',
            'resampled_mask_flair':'vfs://scratch/TCGA_FSLBET_resampled/{sample_id}/flair_mask.nii.gz'}
    
def main():
    network = create_network()
    network.draw()
    network.execute(source_data(),sink_data())
    
if __name__ == '__main__':
    main()
    
      
