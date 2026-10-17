import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {evaluate,payment} from './study-model.mjs';
const base=JSON.parse(readFileSync(new URL('./scenarios.json',import.meta.url))).scenarios[0];
test('Finite tax input cannot return an infinite budget',()=>assert.throws(()=>evaluate(300000,2000,{...base,property_tax_fraction:1e308}),/numeric range/));
test('Receipt and annual debt overflow are errors',()=>{
  assert.throws(()=>evaluate(300000,1e308,base),/numeric range/);
  assert.throws(()=>evaluate(1e308,2000,{...base,annual_interest_rate:10}),/numeric range/);
});
test('Unrepresentable loan period is rejected',()=>assert.throws(()=>payment(1,.06,1e308),/Invalid loan input/));
test('Tiny positive occupancy must not become zero occupancy',()=>assert.throws(()=>evaluate(300000,2000,{...base,occupied_months:5e-324,management_fraction:.9}),/numeric range/));
test('Actual zero occupancy retains null threshold and negative surplus',()=>{
  const result=evaluate(300000,2000,{...base,occupied_months:0});
  assert.equal(result.break_even_gross_monthly_rent,null);assert.ok(result.annual_cash_surplus<0);
});
test('Large finite calculations are not arbitrarily capped',()=>{
  const result=evaluate(1e100,1e90,{...base,down_payment_fraction:1,property_tax_fraction:1e100});
  assert.ok(Number.isFinite(result.annual_cash_surplus));assert.ok(result.annual_cash_surplus< -1e199);
});
