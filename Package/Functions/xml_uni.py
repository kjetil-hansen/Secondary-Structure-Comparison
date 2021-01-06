#Function to fetch UniProt XML data and convert to dictionary

import xmlschema
import sys
from pprint import pprint

def unischema(file):
    schema = xmlschema.XMLSchema('https://www.uniprot.org/docs/uniprot.xsd')    #Fetch UniProt XML Schema
    if schema.is_valid(file)is False:                                           #Validate schema against uniprot file
        sys.exit('XML file not valid')
    dict = schema.to_dict(file)                                                 #Convert xml to dictionary using schema
    content = dict['entry'][0]                                                  #select entry data
    if '$' in content['protein']['recommendedName']['fullName']:
        protein_name = content['protein']['recommendedName']['fullName']['$']
    else:
        protein_name = content['protein']['recommendedName']['fullName']

    strand_count, helix_count, total_helix, total_strand=0,0,0,0

    for i in content['feature']:
        if i['@type'] == 'helix':
            helix_count += 1
            helix_end = i['location']['end']['@position']
            helix_begin = i['location']['begin']['@position']
            helix_length = helix_end - helix_begin + 1
            total_helix += helix_length
        if i['@type'] == 'strand':
            strand_count += 1
            strand_end = i['location']['end']['@position']
            strand_begin = i['location']['begin']['@position']
            strand_length = strand_end - strand_begin + 1
            total_strand += strand_length

    seq_length = content['sequence']['@length']                                       #get length of sequence
    percent_helix = (total_helix / seq_length) *100
    percent_strand = (total_strand / seq_length) *100
    percent_loop = ((seq_length - (total_helix + total_strand)) / seq_length) *100

    return(protein_name, seq_length, percent_helix, percent_strand, percent_loop)

if __name__ == "__main__":
    print(unischema('Output/_random_5.xml'))
