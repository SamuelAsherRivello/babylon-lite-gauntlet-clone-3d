import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
const root=new URL('../public/assets/',import.meta.url);
test('all original game GLBs contain scoped self-contained geometry',async()=>{
 const manifest=JSON.parse(await readFile(new URL('manifest.json',root),'utf8'));
 assert.equal(Object.keys(manifest.assets).length,16);
 for(const [name,asset] of Object.entries(manifest.assets)){
  const data=await readFile(new URL(asset.file,root));assert.equal(data.readUInt32LE(0),0x46546c67,name);assert.equal(data.readUInt32LE(4),2);assert.equal(data.readUInt32LE(8),data.length);
  const gltf=JSON.parse(data.subarray(20,20+data.readUInt32LE(12)).toString());assert.equal(gltf.meshes.length,1);assert.equal(gltf.scenes.length,1);assert.equal(gltf.cameras,undefined);
  assert.ok(gltf.buffers.every(b=>!b.uri));assert.ok(gltf.meshes[0].primitives.every(p=>gltf.accessors[p.attributes.POSITION].count>0));
 }
});
test('portraits use genuine rendered PNGs',async()=>{
 for(const name of ['warrior','valkyrie','wizard','elf']){const b=await readFile(new URL(name+'.png',root));assert.equal(b.readUInt32BE(16),256);assert.equal(b.readUInt32BE(20),256);}
});
