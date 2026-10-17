// Compare the exported Python CSV values with the shipped JS model, not the DOM.
import {readFileSync} from 'node:fs';
import {evaluate, summarize} from './study-model.mjs';
const input=JSON.parse(readFileSync(0,'utf8'));
const tolerance=0.000001;
let comparisons=0,maxError=0;
function same(actual, expected, label) {
  if (!Number.isFinite(actual) || !Number.isFinite(expected)) throw Error(`Nonfinite: ${label}`);
  const error=Math.abs(actual-expected);
  if (error>tolerance) throw Error(`Model mismatch: ${label}: ${actual} vs ${expected}`);
  comparisons++; maxError=Math.max(maxError,error);
}
function number(value) {
  if (typeof value!=='string' || !value.trim() || !Number.isFinite(Number(value))) throw Error('Missing or invalid Python number');
  return Number(value);
}
function unique(rows,key) {
  const map=new Map();
  for (const row of rows) {const id=key(row);if(map.has(id)) throw Error(`Duplicate: ${id}`);map.set(id,row);}
  return map;
}
const scenarioMap=unique(input.data.scenarios,s=>s.id);
const metros=unique(input.data.metros,m=>m.cbsa);
if (!scenarioMap.size || !metros.size) throw Error('Empty comparison inputs');
const summary=unique(input.summary,r=>JSON.stringify([r.scenario,r.cbsa]));
const detail=unique(input.detail,r=>JSON.stringify([r.scenario,r.cbsa,r.hud_area_code]));
let summaryRows=0,detailRows=0;
for (const s of scenarioMap.values()) for (const m of metros.values()) {
  const row=summary.get(JSON.stringify([s.id,m.cbsa]));
  if (!row) throw Error('Missing Python summary row');
  if (!m.areas.length) throw Error('Empty HUD areas');
  unique(m.areas,a=>a.code);
  const result=summarize(m,s);
  for (const [js,csv] of Object.entries({min:'cash_surplus_min_usd',max:'cash_surplus_max_usd',priceMin:'price_endpoint_surplus_min_usd',priceMax:'price_endpoint_surplus_max_usd',threshold:'break_even_gross_monthly_usd'})) same(result[js],number(row[csv]),`${s.id}/${m.cbsa}/${js}`);
  summaryRows++;
  for (const a of m.areas) {
    const expected=detail.get(JSON.stringify([s.id,m.cbsa,a.code]));
    if (!expected) throw Error('Missing Python HUD-area row');
    const actual=evaluate(m.price,a.rent,s);
    for (const [key,value] of Object.entries(actual)) {
      if (key==='input_status') {if(value!==expected[key])throw Error('Input status mismatch');}
      else {if(expected[key]===undefined || expected[key]==='')throw Error('Missing numeric field');same(value,number(expected[key]),`${s.id}/${m.cbsa}/${a.code}/${key}`);}
    }
    detailRows++;
  }
}
if (summaryRows!==summary.size || detailRows!==detail.size) throw Error('Unexpected Python output rows');
console.log(JSON.stringify({status:'PASS',summary_rows:summaryRows,detail_rows:detailRows,numeric_comparisons:comparisons,tolerance_usd:tolerance,max_rounding_error_usd:maxError,scope:'Shipped JS module against rebuilt Python CSV; no DOM, market or geographic certification'},null,2));
