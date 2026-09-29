export class GameInput {
 keys=new Set();touches={x:0,z:0,attack:false,magic:false};paused=false;
 read(){if(this.paused)return {x:0,z:0,attack:false,magic:false};const k=this.keys;return {x:Math.max(-1,Math.min(1,Number(k.has('KeyD')||k.has('ArrowRight'))-Number(k.has('KeyA')||k.has('ArrowLeft'))+this.touches.x)),z:Math.max(-1,Math.min(1,Number(k.has('KeyS')||k.has('ArrowDown'))-Number(k.has('KeyW')||k.has('ArrowUp'))+this.touches.z)),attack:k.has('Space')||this.touches.attack,magic:k.has('KeyE')||this.touches.magic};}
 clear(){this.keys.clear();this.touches={x:0,z:0,attack:false,magic:false};}
}
