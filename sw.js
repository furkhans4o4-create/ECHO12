/* ECHO/12 Build 051 — entire static puzzle fits in one versioned cache. */
'use strict';
const CACHE='echo12-shell-build-051';
const PREFIX='echo12-shell-build-';
const ROOT=new URL('./',self.registration.scope);
const INDEX=new URL('index.html',self.registration.scope);
const MANIFEST=new URL('manifest.webmanifest',self.registration.scope);
const ICON=new URL('icons/echo12.svg',self.registration.scope);
const SHELL=[ROOT.href,INDEX.href,MANIFEST.href,ICON.href];
self.addEventListener('install',event=>{
 event.waitUntil((async()=>{
  const cache=await caches.open(CACHE);
  await cache.addAll(SHELL);
  await self.skipWaiting();
 })());
});
self.addEventListener('activate',event=>{
 event.waitUntil((async()=>{
  const names=await caches.keys();
  await Promise.all(names.filter(name=>name.startsWith(PREFIX)&&name!==CACHE)
   .map(name=>caches.delete(name)));
  await self.clients.claim();
 })());
});
self.addEventListener('fetch',event=>{
 const request=event.request;
 if(request.method!=='GET')return;
 const url=new URL(request.url);
 if(url.origin!==self.location.origin||!url.pathname.startsWith(ROOT.pathname))return;
 if(request.mode==='navigate'){
  event.respondWith((async()=>{
   try{
    const response=await fetch(request);
    if(response.ok){
     const cache=await caches.open(CACHE);
     await cache.put(INDEX.href,response.clone());
    }
    return response;
   }catch(error){
    const cache=await caches.open(CACHE);
    return await cache.match(INDEX.href)||await cache.match(ROOT.href)||Response.error();
   }
  })());
  return;
 }
 // Keep the versioned, installed shell assets available without connectivity.
 if([MANIFEST.href,ICON.href,INDEX.href].includes(url.href)){
  event.respondWith((async()=>{
   const cache=await caches.open(CACHE);
   const stored=await cache.match(request);
   if(stored)return stored;
   const response=await fetch(request);
   if(response.ok)await cache.put(request,response.clone());
   return response;
  })());
 }
});
