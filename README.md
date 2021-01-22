# Pairwise Preference Dataset for Poems
## Structure

#### source_corpora
Files containing poems for each model/dataset taken into account while forming pairs. They may differ in their structure and should be integrated seperately.
#### created_datasets
Output directory for created pairwise datasets.

#### batch_results
The annotations directly from AMT without modifications and merging.

#### annotated_datasets
Merged batch results without additional columns and information from AMT. With only one row containing all categories and annotations for one pair.

## Setup
Code is meant to run on Python3. Earlier version are not supported.<br>
Simply install all dependencies in requirements.txt with pip:
```
pip install -r requirements.txt
```
Download the real poem corpus with the following command and unzip it in *source_corpora*:
```shell
wget https://github.com/anonymous-poetrybot-386/eacl-metrical-tagging-in-the-wild/raw/master/English/LargeCorpus/eng_gutenberg_measures_all.json.zip
```
## Pairwise dataset creation
The non-annotated dataset can be created by executing the following script.
```
python create_pairwise_dataset.py
```
The probability for a real poem to be chosen defaults to 0.5 but can be controlled by the argument *--prob-real* followed by a number between 0. and 1. Outputs are created in the directory *created_datasets*  with an optional custom name for the file by providing a value to the argument *--output-filename*
```
python create_pairwise_dataset.py --prob-real 0.3 --output-filename custom_output_name.csv
```

The created datasets can then be used for annotation in AMT.

## Dataset Extension
Dataset can be further enrichen with more comparison with the existing pairs by following the code in *extend.ipynb*

## Annotation results review
To review annotation results from AMT follow the code in *metrics.ipynb*

## Consolidation of single annotations
As the questions for annotations have been split up a consolidated dataset can be created by using the code in *consolidate.ipynb*
