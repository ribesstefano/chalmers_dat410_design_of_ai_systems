# Mini-Project

* Data cleaning and requirements description: 4 hours, many examples are already available online and the datasets themselves aren't particularly large to manage.
* Models Design: 8 hours, at least two models shall be designed (CNN+RNN-based and Transformer architectures).
* Models Development: 20 hours, this phase shall include the training and hyper parameters tuning of the designed models.
* Evaluation: 2 hours, different tests shall be carried out and properly reported.

## Tasks

* Stefano
	* Data Cleaning:
		* ~~Dataset generation~~
		* ~~Dataset retrival~~
	* Evaluation:
		* time evaluation
		* scalability
		* accuracy

* Daniele
	* Collect Python models: GRU, CNN+RNN? Transformer? check [this project](https://github.com/gyunggyung/Sequence-Models-coursera/tree/master/Week%203/Trigger%20word%20detection).
	* Implement and train them on fake datasets:
		* ~~Get the shape of the data required~~ Get the shape from the dataset (see Getting started guide)
		* Get the parameters

## Getting Started

To generate the dataset:

0. Install the required Python modules (see requirements file)
1. Get the background files from [this repository](https://github.com/gyunggyung/Sequence-Models-coursera/tree/master/Week%203/Trigger%20word%20detection/raw_data/backgrounds) and place it under `module8/data/backgrounds/`. Rename them `background_1.wav` and `background_2.wav` respectively
2. Get the [dataset zipfile](http://www-mmsp.ece.mcgill.ca/Documents/Data/TSP-Speech-Database/16k-LP7.zip) and place it in `data/`
3. Unzip the zipfile into a folder named `16k/`
3. Go to `src/` and run `python data_cleaner.py`, a file name `16k.npy` should get generated under `data/`
4. Use the function `load_dataset()` in `data_cleaner.py` to retrive the cleaned training/test datasets