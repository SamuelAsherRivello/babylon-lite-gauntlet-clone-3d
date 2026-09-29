import {chromium} from '@playwright/test';
import assert from 'node:assert/strict';
const browser=await chromium.launch({channel:'chrome',headless:true});
try{
const context=await browser.newContext({viewport:{width:390,height:844},hasTouch:true,isMobile:true});const page=await context.newPage();await page.goto(process.env.GAME_URL||'http://127.0.0.1:5186/babylon-lite-gauntlet-clone-3d/');await page.waitForFunction(()=>window.gameDiagnostics?.state.status==='connected');
await page.locator('[data-class="elf"]').click();
const stick=await page.locator('#stick').boundingBox(),attack=await page.locator('#attack').boundingBox(),cdp=await context.newCDPSession(page);
await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{id:1,x:stick.x+stick.width/2+25,y:stick.y+stick.height/2},{id:2,x:attack.x+attack.width/2,y:attack.y+attack.height/2}]});
await page.waitForTimeout(300);let input=await page.evaluate(()=>window.gameDiagnostics.input);assert(input.x>.5&&input.attack);
await cdp.send('Input.dispatchTouchEvent',{type:'touchCancel',touchPoints:[]});await page.waitForTimeout(100);input=await page.evaluate(()=>window.gameDiagnostics.input);assert.equal(input.x,0);assert.equal(input.attack,false);
console.log('PASS simultaneous touch and cancellation; waiting for natural defeat');
await page.waitForFunction(()=>window.gameDiagnostics.state.gameState.phase==='defeat',null,{timeout:150000});assert.match(await page.locator('#overlay-title').textContent(),/fallen/);await page.locator('#overlay-action').click();await page.waitForFunction(()=>window.gameDiagnostics.state.gameState.phase==='playing');console.log('PASS natural defeat and restart');
await context.setOffline(true);await page.waitForFunction(()=>window.gameDiagnostics.state.status!=='connected',null,{timeout:20000});await context.setOffline(false);await page.locator('#overlay-action').click();await page.waitForFunction(()=>window.gameDiagnostics.state.status==='connected',null,{timeout:30000});console.log('PASS disconnect and retry');await context.close();
const unsupported=await browser.newContext();await unsupported.addInitScript(()=>Object.defineProperty(navigator,'gpu',{value:undefined}));const p=await unsupported.newPage();await p.goto(process.env.GAME_URL||'http://127.0.0.1:5186/babylon-lite-gauntlet-clone-3d/');await p.waitForFunction(()=>document.getElementById('overlay-title')?.textContent==='WebGPU unavailable');console.log('PASS unsupported WebGPU message');await unsupported.close();
}finally{await browser.close();}
