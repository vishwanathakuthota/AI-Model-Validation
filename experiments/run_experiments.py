"""Reproducible experiments on included synthetic datasets. Python 3.10+, standard library."""
from pathlib import Path
import csv,math,statistics,random
D=Path(__file__).resolve().parents[1]/'datasets'
def load(n):
 with (D/n).open() as f:return list(csv.DictReader(f))
def report(name, value):print(f'{name}: {value}')
a=load('classification_predictions.csv'); y=[int(r['label']) for r in a];p=[float(r['score'])>=.5 for r in a]
tp=sum(t and z for t,z in zip(y,p));tn=sum(not t and not z for t,z in zip(y,p));fp=sum(not t and z for t,z in zip(y,p));fn=sum(t and not z for t,z in zip(y,p))
report('Classification accuracy',round((tp+tn)/len(a),4));report('Precision',round(tp/max(1,tp+fp),4));report('Recall',round(tp/max(1,tp+fn),4))
r=load('regression_predictions.csv');errors=[float(x['prediction'])-float(x['actual']) for x in r];report('MAE',round(statistics.mean(map(abs,errors)),4));report('RMSE',round(math.sqrt(statistics.mean(e*e for e in errors)),4))
c=load('llm_claim_verification.csv');report('Claim factual precision',round(sum(x['reference_state']=='supported' for x in c)/len(c),4));report('Contradiction rate',round(sum(x['reference_state']=='contradicted' for x in c)/len(c),4))
j=load('judge_pairwise.csv');report('Judge-human pairwise agreement',round(sum(x['judge_choice']==x['human_choice'] for x in j)/len(j),4))
cl=load('assurance_claims.csv');report('Mandatory assurance pass',all(float(x['observed'])>=float(x['threshold']) for x in cl if x['mandatory']=='1'))
