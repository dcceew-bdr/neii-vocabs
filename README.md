# NEII Vocabs


## Improvement process

1. Remove all RDF/DCTERMS cruft
2. Convert all vocabs to LongTurtle format
3. Handle Agents in VocPub
4. Improve Agents info 


x. Rplace all "N/A" IRIs with N-A



### 1. Remove all RDF/DCTERMS cruft

Done - Nick, 2024-04-10 


### 2. Convert all vocabs to LongTurtle format

Done - Nick, 2024-04-10 


### 3. Handle Agents in VocPub

Allow `dcterms:Agent` in VocPub got Agent and make a new release (4.8). This will allow VocPub 4.8 validation for these vocabs to work with PoolParty


### 4. Improve Agents info 

Ensure all Agents are valid according to VocPub.

All Org agents need additional typing to `schema:Organization` and an `sdo:url` value. May be blank.

All Persons need additional typing to `schema:Person` and an `sdo:email` value. May be blank.

All Agents need either AGLDWG PID IRIs or vocab local IRIs.



x. Rplace all "N/A" IRIs with N-A

E.g. <http://www.neii.gov.au/def/voc/GW/australian-groundwater-insight/N/A> in bom_australian-groundwater-insight.ttl