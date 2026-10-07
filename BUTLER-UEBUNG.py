"""Offline exercise; no network, Telegram, model, actuator or real house configuration."""
from pathlib import Path
from datetime import datetime
import argparse,json,sqlite3,html,math
def dt(x):
 value=datetime.fromisoformat(x)
 if value.tzinfo is None:raise ValueError('Timezone required')
 return value
def evaluate(d):
 if d.get('synthetic') is not True:raise ValueError('Only explicitly synthetic data accepted')
 now=dt(d['now']);limit=d['max_age_seconds']
 if type(limit) is not int or not 1<=limit<=3600:raise ValueError('Bad freshness limit')
 readings={};rows=[]
 for s in d['sensors']:
  if s['id'] in readings:raise ValueError('Duplicate sensor id')
  value=s['value']
  if type(value) not in (int,float) or not math.isfinite(value):raise ValueError('Finite numerical reading required')
  age=(now-dt(s['at'])).total_seconds();fresh=0<=age<=limit
  rows.append({**s,'age_seconds':age,'fresh':fresh});readings[s['id']]=rows[-1]
 inside=readings.get('inside');outside=readings.get('outside')
 dp_unit='degC dew point'
 if inside and outside and inside['fresh'] and outside['fresh'] and inside['unit']==outside['unit']==dp_unit:
  moisture='outside_lower_dew_point' if outside['value']<inside['value'] else 'outside_not_lower_dew_point'
 else:moisture='unknown_due_to_missing_stale_or_wrong_units'
 request=d['switch_request'];ack=d.get('switch_ack');observed=d.get('switch_observation')
 if request['requested'] not in ('on','off'):raise ValueError('Unknown target state')
 if not 0<=(now-dt(request['at'])).total_seconds()<=limit:raise ValueError('Stale or future request')
 confirmed=False
 if isinstance(ack,dict) and isinstance(observed,dict):
  ordered=dt(request['at'])<=dt(ack['at'])<=dt(observed['at'])<=now
  fresh_ack=0<=(now-dt(ack['at'])).total_seconds()<=limit
  fresh_observation=0<=(now-dt(observed['at'])).total_seconds()<=limit
  confirmed=(ack.get('request_id')==request['id'] and ack.get('applied') is True and observed.get('state')==request['requested'] and ordered and fresh_ack and fresh_observation)
 return {'synthetic':True,'at':d['now'],'readings':rows,'moisture_comparison':moisture,
  'ventilation_automation':False,'ventilation_note':'Dew-point comparison only; weather, outdoor pollutants, temperature and building conditions not assessed.',
  'switch_requested':request['requested'],'switch_confirmed':confirmed,
  'switch_status':'synthetic_confirmation_matches' if confirmed else 'not_confirmed',
  'calendar':d['calendar'],'actual_device_command':False,'actual_message_sent':False,'model_inference':False}
def record_briefing(path,event):
 # Persistent UNIQUE key proves suppression of a repeated PREPARATION, not delivery.
 if dt(event['day']+'T00:00:00+00:00').date().isoformat()!=event['day']:raise ValueError('Invalid day')
 if event['event_id']!='morning-'+event['day']:raise ValueError('Unexpected synthetic event id')
 con=sqlite3.connect(str(path),timeout=5)
 try:
  con.execute('CREATE TABLE IF NOT EXISTS briefing (event_id TEXT PRIMARY KEY, day TEXT NOT NULL, status TEXT NOT NULL)')
  cur=con.execute('INSERT OR IGNORE INTO briefing VALUES (?, ?, ?)',(event['event_id'],event['day'],'prepared_simulation_not_sent'))
  inserted=cur.rowcount==1;con.commit()
  count=con.execute('SELECT COUNT(*) FROM briefing').fetchone()[0]
 finally:con.close()
 return {'event_id':event['event_id'],'new_preparation':inserted,'stored_event_count':count,'delivery_confirmed':False}
def run():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--data',required=True);ap.add_argument('--state',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
 source=Path(a.data).resolve();state=Path(a.state).resolve();out=Path(a.output).resolve()
 if out.exists():raise SystemExit('Existing output preserved; choose a new output directory')
 if state==source or state.is_dir() or not state.parent.exists():raise SystemExit('State must be a separate file in an existing parent')
 d=json.loads(source.read_text(encoding='utf-8-sig'));report=evaluate(d)
 if d['briefing']['day']!=dt(d['now']).date().isoformat():raise ValueError('Briefing day differs from synthetic clock')
 report['briefing']=record_briefing(state,d['briefing']);out.mkdir()
 (out/'BERICHT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 esc=html.escape
 rows=''.join('<tr><td>'+esc(str(s[k]))+'</td><td>'+esc(str(s['value']))+'</td><td>'+esc(s['unit'])+'</td><td>'+esc(s['at'])+'</td><td>'+str(s['fresh'])+'</td></tr>' for s in report['readings'] for k in ['label'])
 page='<!doctype html><meta charset="utf-8"><title>Synthetic house exercise</title><style>body{font:20px system-ui;margin:40px;background:#10202b;color:#edf7f8}td,th{padding:12px;border-bottom:1px solid #5e7e89}table{border-collapse:collapse}pre{white-space:pre-wrap}b{color:#72e7bd}</style><h1>SYNTHETIC HOUSE EXERCISE</h1><p>No house connected. No commands or messages sent.</p><p>Fixed synthetic clock: '+esc(report['at'])+'</p><table><tr><th>Source</th><th>Value</th><th>Unit</th><th>Time</th><th>Fresh</th></tr>'+rows+'</table><h2>Requested ≠ confirmed</h2><p><b>'+esc(report['switch_status'])+'</b></p><h2>Persistent briefing preparation</h2><pre>'+esc(json.dumps(report['briefing'],indent=2))+'</pre><h2>Moisture comparison</h2><p>'+esc(report['moisture_comparison'])+'</p><p>'+esc(report['ventilation_note'])+'</p>'
 (out/'DASHBOARD.html').write_text(page,encoding='utf-8')
 print('Offline report created. No device/Telegram/model request. New briefing preparation: '+str(report['briefing']['new_preparation']))
if __name__=='__main__':run()
