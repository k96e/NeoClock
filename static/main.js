function sendAPI(key,value){
	var xhr = new XMLHttpRequest();
	xhr.open('get', '/api?k='+key+'&v='+value);
	xhr.onreadystatechange = function () {
		if (xhr.readyState === 4) {
			if (xhr.responseText.length<20){
				iziToast.show({
					title: 'Success',
					position:"topCenter",
					transitionIn:"bounceInDown",
					timeout:2000,
					progressBar:false,
					iconUrl:"/static/success.svg",
					message: xhr.responseText
				});
			}else{
				alert(xhr.responseText);
			}
		}
	}
	xhr.send();
}
function sendCTR(key,value){
	var xhr = new XMLHttpRequest();
	xhr.open('get', '/Mapi?k='+key+'&v='+value);
	xhr.onreadystatechange = function () {
		if (xhr.readyState === 4) {
			if (key==="getWindows"){
				var ws = xhr.responseText.split('\n');
				var modalEl = document.createElement('div');
				modalEl.style.margin = '5% 20%';
				modalEl.style.padding = '10px';
				modalEl.style.backgroundColor = '#fff';
				for(var i=0;i<ws.length;i++){
					if(ws[i]==='')
						continue;
					var child = document.createElement('h3');
					child.innerText=ws[i];
					child.onclick=function(e){
						document.getElementById("inWindow").value=e['path'][0].innerText;
						mui.overlay('off');
					};
					modalEl.appendChild(child);
				}
				mui.overlay('on', modalEl);
			}
			else if (key==="readCopy"){
				if (xhr.responseText.length<=20){
					document.getElementById("copyboard").value=xhr.responseText;
				}else{
					alert(xhr.responseText);
				}
			}
			else if (xhr.responseText.length<20){
				iziToast.show({
					title: 'Success',
					position:"topCenter",
					animateInside:false,
					transitionIn:"bounceInDown",
					timeout:2000,
					displayMode:2,
					progressBar:false,
					iconUrl:"/static/success.svg",
					message: xhr.responseText
				});
			}else{
				alert(xhr.responseText);
			}
		}
	}
	xhr.send();
}

function sendK(key){
	sendCTR('setKey',key);
}

var imgEle = document.getElementById("screenImg");
document.getElementById("loadImg").onclick=function(){
	imgEle.src="/getNewScreenshot";
};
document.getElementById("sendPos").onclick=function(){
	sendAPI('setPos',document.getElementById("inPos").value);
};
document.getElementById("sendURL").onclick=function(){
	sendCTR('sendURL',document.getElementById("inURL").value);
};
document.getElementById("getWindows").onclick=function(){
	sendCTR('getWindows','none');
};
document.getElementById("sendWindowAct").onclick=function(){
	sendCTR('ctrWindow_act',document.getElementById("inWindow").value);
};
document.getElementById("sendWindowMax").onclick=function(){
	sendCTR('ctrWindow_max',document.getElementById("inWindow").value);
};
document.getElementById("sendWindowMin").onclick=function(){
	sendCTR('ctrWindow_min',document.getElementById("inWindow").value);
};
document.getElementById("sendWindowRst").onclick=function(){
	sendCTR('ctrWindow_rst',document.getElementById("inWindow").value);
};
document.getElementById("sendWindowExt").onclick=function(){
	sendCTR('ctrWindow_ext',document.getElementById("inWindow").value);
};
document.getElementById("sendMKey").onclick=function(){
	sendK(document.getElementById("inKey").value);
};

document.getElementById("readCopy").onclick=function(){
	sendCTR("readCopy",'none');
};
document.getElementById("writeCopy").onclick=function(){
	sendCTR("writeCopy",document.getElementById("copyboard").value);
};
document.getElementById("capImg").onclick=function(){
	sendCTR("capImg","none");
	setTimeout("window.open('takenImg')",5000);
};