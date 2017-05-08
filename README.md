# HabitualBe
Project to identify habitual be in black English. 

## Scripts
### findmatches.py
Identify candidates for habitual be from a directory of texts

### get_gutenberg.py
Download gutenberg texts to use for testing from metadata and store in directory gutenberg/

## Data
### pg-metadata-rdf.hdf
Gutenberg metadata for downloading all Gutenberg files. Metadata in HDF file  from [Jonathan Reeve](https://github.com/JonathanReeve/gitenberg-experiments).
### slavenarratives/ 
Text of slave narratives. Can run findmatches.py on it
### slavenarratives.csv
Example output from findmatches.py on slavenarratives/
### gutenberg.csv
Example output from findmatches.py on gutenberg/