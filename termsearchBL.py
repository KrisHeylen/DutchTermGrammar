import pandas as pd
import urllib.parse
import urllib.request
import requests
import json

def wordFreqTableBlackLab(CorpusURL,searchpattern,sortingCrit=None,metafilter=False):
    CorpusURL = CorpusURL+'hits?'
    if metafilter:
        CorpusURL = CorpusURL+'filter='+'+AND+'.join(list(map(urllib.parse.quote_plus,metafilter)))
   
    #make sure we group by word
    CorpusURL = CorpusURL+'&first=0&group=hit:word:i'
    if searchpattern:
        CorpusURL = CorpusURL+'&patt='+urllib.parse.quote_plus(searchpattern)
    else:
        raise ValueError("No CQL pattern")
    if sortingCrit:
        # default seems to be "size(descending)", so only change if you need to sort by ascending size or alphabetically
        CorpusURL = CorpusURL+'&sort='+sortingCrit
    CorpusURL = CorpusURL+'&outputformat=json'   
#    print(CorpusURL)
    try:
        f = urllib.request.urlopen(url)
        response = json.loads(f.read().decode('utf-8'))
    except:
        response= {'hitGroups':[]}
    if len(response['hitGroups'])>0:
        df = pd.json_normalize(response['hitGroups'])
        df = df[['identityDisplay','size','numberOfDocs']]
        df = df.rename(columns={"identityDisplay": "string", "size": "freq","numberOfDocs":"docs"})
        df['subcorpusSizeTokens'] = response['summary']['subcorpusSize']['tokens']
        df['subcorpusSizeDocuments'] = response['summary']['subcorpusSize']['documents']
    else:
        df = pd.DataFrame()
    return df