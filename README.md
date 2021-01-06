## Secondary structure comparison script

*last updated by KJ Hansen on 06/01/2020*

This python-based script compares the secondary structure prevalence between two organisms (*E. coli* and human by default). The script accesses the Swissprot database through the Uniprot API to fetch *n* number of random *E. coli* and human proteins. The Uniprot XML schema is used to read in the secondary structure features for each protein. This information is tabulated and statistics for alpha helices, beta strands and unstructured regions calculated. The results are displayed as a stacked bar chart.

---

### Usage

Requirements:

- Python 3.0+

#### Flag Usage:

-r  number of random proteins for each organism to compare

#### Terminal usage example:

```
python<version> SStructure_Comparison -r 10
```

---

### Output

A file containing all proteins and associated secondary structure percentages is saved as a .csv file. The bar chart is saved as a .png.

An example of the output is shown below:

<img src="https://github.com/kjetil-hansen/Secondary-Structure-Comparison/blob/master/Output/SSOutput.png" width="600" height="341">

![Example of stacked bar chart](https://github.com/kjetil-hansen/Secondary-Structure-Comparison/blob/master/Output/OutputBar.png)
