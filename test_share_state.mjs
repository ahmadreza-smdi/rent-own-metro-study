// Execute the actual UI module in a small DOM fixture. Model arithmetic is outside this test.
import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';

const file=process.argv[2] || new URL('./study-ui.mjs', import.meta.url);
const source=fs.readFileSync(file,'utf8').replace(/^import \{summarize\} from [^\n]+\n/,'');
function fixture(hash=''){
 class Element{
  constructor(tag='div'){this.tagName=tag;this.value='';this.hidden=false;this.textContent='';this.children=[];this.events={};this.attrs={};}
  get value(){return this._value;}
  set value(v){this._value=String(v);}
  append(...items){for(const item of items){this.children.push(item);if(item.id)nodes.set(item.id,item);}}
  replaceChildren(...items){this.children=[];this.append(...items);}
  setAttribute(k,v){this.attrs[k]=v;}
  addEventListener(k,fn){this.events[k]=fn;}
  trigger(k){this.events[k]?.();}
  select(){} scrollIntoView(){}
 }
 const ids=['detail','study-data','assumptions','selected-name','selected-proxy','area-body','threshold','budget','error','download-current','result-body','print-assumptions','count','search','sort','page','previous','next','axis','preset','print','share','share-url','share-status'];
 const nodes=new Map(ids.map(id=>[id,new Element()]));
 nodes.get('share-url').hidden=true;
 const fields=[{key:'occupied_months',label:'Paid months',percent:false},{key:'management_fraction',label:'Management',percent:true}];
 const scenario={id:'fixture',label:'Fixture',occupied_months:10,management_fraction:.1};
 const metros=['A','B'].map((name,i)=>({name,cbsa:String(i),price:100000,moe:1000,areas:[{name:'Area',code:String(i),rent:1000}]}));
 nodes.get('study-data').textContent=JSON.stringify({fields,scenarios:[scenario],metros});
 const summarize=(m,s)=>({min:1,max:2,priceMin:0,priceMax:3,threshold:1,details:[{name:'Area',code:m.cbsa,rent:1000,result:{annual_cash_surplus:1,annual_receipts:2,annual_management:0,annual_fixed_budget:1,annual_principal_interest:0}}]});
 const context={document:{getElementById:id=>nodes.get(id),createElement:tag=>new Element(tag),createElementNS:(_,tag)=>new Element(tag)},summarize,location:{hash,href:'https://example.invalid/study/'+hash},window:{print(){}},console,setTimeout,URL,Blob};
 vm.runInNewContext(source,context,{filename:String(file)});
 return {nodes,click:id=>nodes.get(id).trigger('click'),change:(id,value,event='input')=>{nodes.get(id).value=value;nodes.get(id).trigger(event);}};
}
let passed=0;
const test=(name,run)=>{run();passed++;console.log('PASS '+name);};
const cleared=f=>{assert.equal(f.nodes.get('share-url').value,'');assert.equal(f.nodes.get('share-url').hidden,true);assert.equal(f.nodes.get('share-status').textContent,'');};
test('changed assumptions invalidate old link and rebuilding captures current values',()=>{
 const f=fixture();f.click('share');assert.ok(f.nodes.get('share-url').value.includes('#scenario='));
 f.change('occupied_months','8');cleared(f);f.click('share');
 const payload=JSON.parse(decodeURIComponent(f.nodes.get('share-url').value.split('#scenario=')[1]));assert.equal(payload.inputs.occupied_months,8);
});
test('blank input clears results and old link',()=>{const f=fixture();f.click('share');f.change('occupied_months','');cleared(f);assert.equal(f.nodes.get('download-current').disabled,true);assert.equal(f.nodes.get('result-body').children.length,0);});
test('correcting an input clears a stale share failure message',()=>{const f=fixture();f.change('occupied_months','');f.click('share');assert.match(f.nodes.get('share-status').textContent,/Complete/);f.change('occupied_months','8');cleared(f);});
test('search invalidates previous link',()=>{const f=fixture();f.click('share');f.change('search','B');cleared(f);});
test('preset invalidates previous link',()=>{const f=fixture();f.click('share');f.change('preset','fixture','change');cleared(f);});
test('selecting another metro invalidates link and rebuild captures new metro',()=>{
 const f=fixture();f.click('share');f.nodes.get('result-body').children[1].children[0].children[0].trigger('click');cleared(f);f.click('share');
 assert.equal(JSON.parse(decodeURIComponent(f.nodes.get('share-url').value.split('#scenario=')[1])).cbsa,'1');
});
test('malformed inbound link notice survives initial render',()=>{const f=fixture('#scenario=invalid');assert.match(f.nodes.get('share-status').textContent,/could not be restored/);});
test('valid inbound scenario restores without an old output link',()=>{const hash='#scenario='+encodeURIComponent(JSON.stringify({version:1,inputs:{occupied_months:7,management_fraction:.2},cbsa:'1',search:''}));const f=fixture(hash);assert.equal(f.nodes.get('occupied_months').value,'7');cleared(f);f.click('share');assert.equal(JSON.parse(decodeURIComponent(f.nodes.get('share-url').value.split('#scenario=')[1])).cbsa,'1');});
for(const cbsa of ['missing',null,1,undefined,'']){
 test('unknown or invalid metro is rejected: '+String(cbsa),()=>{
  const hash='#scenario='+encodeURIComponent(JSON.stringify({version:1,inputs:{occupied_months:7,management_fraction:.2},cbsa,search:'B'}));
  const f=fixture(hash);
  assert.match(f.nodes.get('share-status').textContent,/could not be restored/);
  assert.equal(f.nodes.get('occupied_months').value,'10');
  assert.equal(f.nodes.get('management_fraction').value,'10');
  assert.equal(f.nodes.get('search').value,'');assert.equal(f.nodes.get('selected-name').textContent,'A');
 });
}
console.log(`${passed} scoped UI-state tests passed; fictional DOM/model fixture, not browser or financial-model certification.`);
