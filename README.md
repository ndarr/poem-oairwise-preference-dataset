# TODOs
- aggregate_poems.py
- dataset_extension.ipynb
- metrics.ipynb
- requirements.txt
- README.md

# Structure
#### source_corpora
Files containing poems for each model/dataset taken into account while forming pairs. They may differ in their structure and should be integrated seperately.
#### created_datasets
Output directory for created pairwise datasets.

#### batch_results
The annotations directly from AMT without modifications and merging.
#### annotated_datasets
Merged batch results without additional columns and information from AMT. With only one row containing all categories and annotations for one pair.

# Setup
Code is meant to run on Python3. Earlier version are not supported.<br>
Simply install all dependencies in requirements.txt with pip:
```
pip install -r requirements.txt
```

# Pairwise dataset creation
The non-annotated dataset can be created by executing the following script.
```
python create_pairwise_dataset.py
```
The probability for a real poem to be chosen defaults to 0.5 but can be controlled by the argument *--prob-real* followed by a number between 0. and 1. Outputs are created in the directory *created_datasets*  with an optional custom name for the file by providing a value to the argument *--output-filename*
```
python create_pairwise_dataset.py --prob-real 0.3 --output-filename custom_output_name.csv
```