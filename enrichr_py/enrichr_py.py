# -*- coding: utf-8 -*-

import os
import json
import requests
import numpy as np

class Enrichr:
    '''
    This is just a wrapper class for Enrichr API.
    http://amp.pharm.mssm.edu/Enrichr/help#api
    '''
    
    _Enrichr_URL = 'http://amp.pharm.mssm.edu/Enrichr'
    
    def __init__(self, geneListStr, description = None):
        '''
        The default constructor of the class. It takes a list of genes (as a string)
        and its description (optional) and registers them to Enrichr using self._addList()
        '''
        if description is None:
            description = ''
        self.description = description
        self.geneListStr = geneListStr
        self.responseAddList = self._addList()
        self.userListId = json.loads(self.responseAddList.text)['userListId']
        self.shortId = json.loads(self.responseAddList.text)['shortId']        
        self.enrichCache = dict({})
        
    def getURL(self):
        '''
        This method provides the URL to browse the results on the web
        '''
        return(os.path.join(self._Enrichr_URL, 'enrich?dataset={}'.format(self.shortId)))
               
    def _addList(self):
        '''
        This method is called from constructor and registers the list of genes to Enrichr
        '''
        response = requests.post(
            os.path.join(self._Enrichr_URL, 'addList'), 
            files = {
                'list': (None, self.geneListStr),
                'description': (None, self.description)
            }
        )
        if not response.ok:
            raise Exception('Error analyzing gene list')
        return response
    
    def view(self):
        '''
        This method calls Enrichr API to see the list of genes
        '''
        response = requests.get(
            os.path.join(self._Enrichr_URL, 'view?userListId={}'.format(self.userListId))
        )
        if not response.ok:
            raise Exception('Error getting gene list')
        return response
    
    def enrich(self, gene_set_library, outFileName = None):
        '''
        This method performs Enrichment analysis given a name of gene set library.
        It caches the results of enrichment analysis to self.enrichCache to
        avoide duplicated queries to the server.
        '''
        if gene_set_library not in self.enrichCache:
            response = requests.get(
                os.path.join(
                    self._Enrichr_URL, 
                    'enrich?userListId={}&backgroundType={}'.format(self.userListId, gene_set_library)
                )
             )
            if not response.ok:
                raise Exception('Error fetching enrichment results')
            self.enrichCache[gene_set_library] = response
            
        if outFileName is not None:            
            if os.path.isabs(outFileName):
                outFileAbs = outFileName
            else:
                outFileAbs = os.path.abspath(os.path.join('./', outFileName))
            
            if not os.path.exists(os.path.dirname(outFileAbs)):
                try:
                    os.makedirs(os.path.dirname(outFileAbs))
                except:
                    raise()
            try:
                with open(outFileAbs, 'wb') as f:
                    for chunk in self.enrichCache[gene_set_library].iter_content(chunk_size=1024): 
                        if chunk:
                            f.write(chunk)
            except:
                raise()
        return self.enrichCache[gene_set_library]
    
    def enrich_data(self, gene_set_library, field=2):
        '''
        This method returns a pair of term and their score 
        based on the results of enrichment analysis for a given gene set.
        One may specify the data field by passing an index to argument field.
        The default is set to be (uncorrected) p-value.
        
        Field:
          0: Index
          1: Name
          2: P-value
          3: Adjusted p-value
          4: Z-score
          5: Combined score (sort the terms in the decreasing order)
        '''
        if(field == 5):
            sort_sign = -1
        else:
            sort_sign = 1
        data = json.loads(
            self.enrich(gene_set_library, outFileName = None).text
        )[gene_set_library]
        n_enriched = len(data)
        names = [data[i][1] for i in range(n_enriched)]
        values = [data[i][field] for i in range(n_enriched)]
        sort_order = np.argsort(sort_sign * values)
        return [names[i] for i in sort_order], [values[i] for i in sort_order]

