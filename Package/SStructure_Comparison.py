## Python script to fetch and compare prevalence of secondary structure between two organisms

# Last edited 06/01/2020 by KJ

import argparse, sys, os, requests
import pandas as pd, numpy as np, matplotlib.pyplot as plt
from matplotlib import rc
from Functions.uniprot_fetcher import uni_search
from Functions.xml_uni import unischema

##Input flag options
parser = argparse.ArgumentParser()
parser.add_argument('-r', help = 'Number of random proteins from each organism')
args = parser.parse_args()

#make path to save output
path_out = os.getcwd() +'/../2_Output/'
os.makedirs(path_out, exist_ok=True)
os.chdir(path_out)

#Organisms to compare
organism1 = 'human'
organism2 = 'ecoli'

#format (must be xml)
format = 'xml'

#Define dict for switch loop
organisms = {
    1: organism1,
    2: organism2
}

columns = ['Organism', 'Protein Name', 'Sequence Length',
            'Helix', 'Beta-Strand',
            'Unstructured']

#Initialise DataFrame
df = pd.DataFrame(columns=columns)

#fetch and save xml files
for key in organisms:
    organism = organisms[key]
    for i in range(int(args.r)):
        accession_organism = organism + '_random_'+ str(i+1)
        data = uni_search(accession_organism, organism, format)
        unicode_data = data.decode('utf-8')
        result = list(unischema(unicode_data))
        result.insert(0,organism)
        df = df.append(pd.Series(result, index=columns), ignore_index=True)
#
print(df)

#Save file
df.to_csv('SSOutput.csv', index=False)


#Remove 100% unstructured proteins
df = df[df.Unstructured != 100]

print(df)

#Mean by organism
df = df.groupby(['Organism']).mean()

print(df)

#Plot colours
a,b,c = [plt.cm.Blues, plt.cm.Reds, plt.cm.Greens]

#Assign plot variables, exit if all organism proteins are unstructured
if (df.index == 'human').any() == True:
    hh = float(df.loc['human',['Helix']])
    hb = float(df.loc['human',['Beta-Strand']])
    hu = float(df.loc['human',['Unstructured']])
else:
    sys.exit('No structured human proteins fetched')

if (df.index == 'ecoli').any() == True:
    eh = float(df.loc['ecoli',['Helix']])
    eb = float(df.loc['ecoli',['Beta-Strand']])
    eu = float(df.loc['ecoli',['Unstructured']])
else:
    sys.exit('No structured ecoli proteins fetched')

r = [0,1]
greenBars = [hh, eh]
orangeBars = [hb, eb]
blueBars = [hu, eu]

##Bar Plot
barWidth = 0.85
names = ('Human', 'E.coli')
plt.bar(r, greenBars, color = '#6fac5e', edgecolor = 'white', width = barWidth, label = 'Helix')
plt.bar(r, orangeBars, bottom = greenBars, color = '#e38e43', edgecolor = 'white', width = barWidth, label = 'Beta-Strand')
plt.bar(r, blueBars, bottom = [i+j for i,j in zip(greenBars, orangeBars)], color = '#6aa0f7', edgecolor = 'white', width = barWidth, label = 'Unstructured')

plt.xticks(r, names)
plt.xlabel('Organism')
plt.ylabel('Percentage')

plt.legend(loc = 'upper right', bbox_to_anchor=(1,1), ncol=1)

plt.savefig('OutputBar.png')

plt.show()
