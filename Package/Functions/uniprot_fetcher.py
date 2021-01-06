#Search uniprot through API

import requests

def uni_search(query, organism, format='xml'):
    if organism == 'human':
        organism_sele = '+AND+organism:9606'
    elif organism == 'ecoli':
        organism_sele = '+AND+organism:83333'
    elif organism == 'any':
        organism_sele = ''

    if 'random' in query:
        base_url = f'http://www.uniprot.org/uniprot/?query=reviewed:yes{organism_sele}&random=yes'
        payload = {'format':format}
    else:
        base_url = 'http://www.uniprot.org/uniprot'
        payload = {'query':query, 'format':format}
    output = requests.get(base_url, params=payload)
    if output.ok:
        return output.content

if __name__ == "__main__":
    x = uni_search('random')
    print(x)
