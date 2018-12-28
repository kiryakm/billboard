var multX = 0;		// Множитель по X
var multY = 0;		// по Y
var screenDiv = 4;	// Делитель экранов для отображения (чем больше картинка тем меньше экраны)
var mode = 0;		// Для растяжения финальной картинки 0 - норм, 1 - растяжение по X, 2 - по Y, 3 - максимальное растяжение
var rotation = 0;	// 0-0 1-90 2-180 3-270


function canvasDown(ev)
{
	click = true;
}
function canvasUp(ev)
{
	click = false;
}

function mouseMove(ev)	
{
	if (click == true)
	{
		var rect = origCanvas.getBoundingClientRect();
		var x = ev.clientX - rect.left;
		var y = ev.clientY - rect.top;
		mode = 0;
		redraw(x, y);
	}
}

function temp(multX, multY)
{
	drawOriginal(multX, multY);
	makeTable(multX, multY);
}

function redraw(x, y)		// Отрисовка при двежение мыши
{
	pic = new Image();
	pic.onload = function()
	{
		if (pic.height < pic.width)
			var sm = 300 / pic.height;	// screen multiplier нужен что бы оригинальная картинка отображалась одного размера, размер зависит от соотношения сторон 
		else
			var sm = 300 / pic.width;

		if (rotation == 0 || rotation == 2)
			multX = (1 - x / (pic.width * sm));
		else
			multX = (1 - y / (pic.width * sm));
			
		multY = multX;
	}
	pic.src = URL.createObjectURL(document.getElementById('pic').files[0]); 
	drawOriginal(multX, multY);
	makeTable(multX, multY);
}

function rotate()
{	
	multX = 0;
	multY = 0;
	var origCan = document.getElementById("origImg");
	rotation += 1;
	if (rotation == 4)
		rotation = 0;
	var s = origCan.height;
	origCan.height = origCan.width;
	origCan.width = s;			
	drawOriginal(multX, multY);
	makeTable(multX, multY);
}

function getId(i, j, inum, jnum)	// Получить Id canvas-а
{			
	if (rotation == 0)
		return 'canvas'+ i + '_' + j;
	if (rotation == 1)
		return 'canvas'+ i + '_' + (jnum-1-j);
	if (rotation == 2)
		return 'canvas'+ (inum-1-i) + '_' + (jnum-1-j);
	if (rotation == 3)
		return 'canvas'+ (inum-1-i) + '_' + j;
}
function getName(pic, i, j, inum, jnum)	// Получить название картинки
{			
	if (rotation == 0)
		name = pic.width + "x" + pic.height + " " + i + "_" + j;
	if (rotation == 1)
		name = pic.width + "x" + pic.height + " " + i + "_" + (jnum-1-j);
	if (rotation == 2)
		name =  pic.width + "x" + pic.height + " " + (inum-1-i) + '_' + (jnum-1-j);
	if (rotation == 3)
		name = pic.width + "x" + pic.height + " " + (inum-1-i) + '_' + j;		
	if  (document.getElementById('vert').checked == true)
		return "Vert" + name;
	if  (document.getElementById('hor').checked == true)
		return "Hor" + name;		
}

function rotateCtx(canvas)
{				
	var ctx = canvas.getContext("2d");
	if (rotation == 1)
	{
		ctx.translate(canvas.width, 0);
		ctx.rotate(90 * Math.PI / 180);
	}
	if (rotation == 2)
	{
		ctx.translate(canvas.width, canvas.height);		
		ctx.rotate(180 * Math.PI / 180);
	}		
	if (rotation == 3)
	{
		ctx.translate(0, canvas.height);	
		ctx.rotate(270 * Math.PI / 180);
	}			
	return ctx;
}

function drawOriginal(multX, multY)
{
	pic = new Image();
	pic.onload = function()
	{
		var origCan = document.getElementById("origImg");
		var ctx = origCan.getContext("2d");
		//alert("pic height " + pic.height)
		if (pic.height < pic.width)
			var sm = 300 / pic.height;	// screen multiplier нужен что бы оригинальная картинка отображалась одного размера, размер зависит от соотношения сторон 
		else
			var sm = 300 / pic.width;
		if (rotation == 0 || rotation == 2)
		{
			origCan.height = pic.height * sm;
			origCan.width = pic.width * sm;
		}
		else
		{
			origCan.width = pic.height * sm;
			origCan.heigth = pic.width * sm;
		}
		ctx = rotateCtx(origCan);

		if (rotation == 0)
			ctx.drawImage(pic, 0, 0, origCan.width - multX * origCan.width, origCan.height - multY * origCan.height);			
		if (rotation == 1)
			ctx.drawImage(pic, 0, 0, origCan.height - multY * origCan.height, origCan.width - multX * origCan.width);
		if (rotation == 2)
			ctx.drawImage(pic, 0, 0, origCan.width - multX * origCan.width, origCan.height - multY * origCan.height);		
		if (rotation == 3)
			ctx.drawImage(pic, 0, 0, origCan.height - multY * origCan.height, origCan.width - multX * origCan.width);
	}
	pic.src = URL.createObjectURL(document.getElementById('pic').files[0]);
}

// Растянуть оригинальную картинку
function stretchOrigX ()
{
	multX = 0;
	mode = 0;
	drawOriginal(multX,multY);
	if (rotation == 0 || rotation == 2)
		makeTable(multX, multY);
	else
		makeTable(multY, multX);
}

function stretchOrigY ()
{
	multY = 0;
	mode = 0;
	drawOriginal(multX,multY);
	if (rotation == 0 || rotation == 2)
		makeTable(multX, multY);
	else
		makeTable(multY, multX);
}
function stretchOrigXY ()
{
	multX = 0
	multY = 0
	makeTable(multX, multY)
	drawOriginal(multX,multY)
}
// Растянуть картинку на экранах
function stretchPrevX ()
{
	mode = 1;
	draw(multX, multY);
}

function stretchPrevY ()
{
	mode = 2;
	draw(multX, multY);
}

function stretchPrevXY ()
{				
	mode = 3;
	
	draw(multX, multY);
}

function setScreenDiv(inum, jnum)	// Получить делитель экранов для отображения
{
	if (inum <= 2 && jnum <= 3)
			screenDiv = 4;
	if ((inum > 2 && inum <=6) || (jnum > 3 && jnum <=6))
			screenDiv = 6;
	if ((inum > 6) || (jnum > 6))
			screenDiv = 8;
}

function getInf(height, width, inum, jnum)	// Получить информацию
{
	pic = new Image();
	pic.onload = function() 
	{
		document.getElementById("picRes").innerHTML = "Uploaded image resalution: " + pic.width + "x" + pic.height;
		document.getElementById("endRes").innerHTML = "Resalution of screens: " + width*jnum + "x" + height*inum;
		document.getElementById("quantOfScreens").innerHTML = "Quantity of screens: " + inum*jnum;
	}
	pic.src = URL.createObjectURL(document.getElementById('pic').files[0]);
}

function getHW()	// Получить высоту и ширину 
{
	var HW = []
	if  (document.getElementById("hor").checked==true)
	{
		HW[0] = 960;	// height		
		HW[1] = 1280	// width
	}
	if  (document.getElementById("vert").checked==true)
	{
		HW[0] = 1280;	// height
		HW[1] = 960		// width
	}
	return HW
}

function makeTable(multX, multY)
{
	var height = getHW()[0];
	var width = getHW()[1];
	var inum, jnum;
	
	pic = new Image();
	pic.onload = function() 
	{		
		if (rotation == 0 || rotation == 2)
		{
			inum = Math.ceil((this.height - multY * (this.height)) / height);	// Число строк
			jnum = Math.ceil((this.width - multX * (this.width))/width);		// Число столбцов
		}
		else
		{
			jnum = Math.ceil((pic.height - multY * (pic.height))/width);	// Число строк
			inum = Math.ceil((pic.width - multX * (pic.width))/height);		// Число столбцов
		}
		setScreenDiv(inum, jnum);
		getInf(height, width, inum, jnum);

		var table = document.getElementById('drawTable');
		for (var i = 0; i < inum+jnum; i++)		// Удаляем старую таблицу
		{
			var idRow= "tr" + i;
			if (document.getElementById(idRow))
				document.getElementById(idRow).remove();
		}

		for (var i = 0; i < inum; i++)		// Формируем таблицу для вывода
		{
			var idRow= "tr" + i;
			var newRow = document.createElement('tr');
			newRow.id = idRow;
			table.appendChild(newRow);
			for (var j = 0; j < jnum; j++)
			{
				var idCol = "td" + i + "_" + j;
				var newCol = document.createElement('td');
				newCol.id = idCol;
				var str = '<canvas id="canvas'+ i + '_' + j + '" height="' + height/screenDiv + '" width="'+ width/screenDiv + '" style="border:1px solid #000000;"></canvas>'
				newCol.innerHTML += str;
				newRow.appendChild(newCol);
			}
		}

		mode = 0;
	}
	pic.src = URL.createObjectURL(document.getElementById('pic').files[0]);
	
	draw(multX, multY);
		
}

function draw(multX, multY)
{
	var inum = document.getElementById('drawTable').rows.length;
	var jnum = document.getElementById('drawTable').rows[0].cells.length;
	
	var height = getHW()[0];
	var width = getHW()[1];

	pic = new Image();
	pic.onload = function()   
	{
		
		var sumH = 0;//0
		var sumW = 0;//90
		for (var i = 0; i < inum; i++)
		{
			if (rotation == 0 || rotation == 2)
				sumW = 0;//0;
			else 
				sumH = 0;//90

			for (var j = 0; j < jnum; j++)
			{
				var canId = getId(i, j, inum, jnum);

				var canvas = document.getElementById(canId);
				if (canvas != null)
				{
					var ctx = canvas.getContext("2d");
					ctx.fillStyle = "#FFFFFF";	
					ctx.fillRect(0,0, canvas.width, canvas.height);	// Заполнить canvas белым
					// Отрисовать поверх
					drawing(canvas, pic, sumW, sumH, inum, jnum, multX, multY, screenDiv, height, width, mode);
					
					if (rotation == 0 || rotation == 2)
						sumW += canvas.width;	//0 180
					else 
						sumH += canvas.width;	//90 270
				}
			}
			var canvas = document.getElementById("canvas0_0");
			if (rotation == 0 || rotation == 2)
				sumH += canvas.height;	//0 180
			else 
				sumW += canvas.height;	//90 270
				
		}
	}
	pic.src = URL.createObjectURL(document.getElementById('pic').files[0]); 
}

function drawing(canvas, pic, sumW, sumH, inum, jnum, multX, multY, screenDiv, height, width, mode)
{
	var ctx = canvas.getContext("2d");
	if (rotation == 0)
	{					
		offsetX = 0;
		offsetY = 0;
	}
	if (rotation == 1)
	{
		offsetX = 0;					
		offsetY = jnum * width / screenDiv - (-multY+1) * pic.height/screenDiv;
	}
	if (rotation == 2)
	{
		offsetX = jnum * width / screenDiv - (-multX+1) * pic.width/screenDiv;
		offsetY = inum * height / screenDiv - (-multY+1) * pic.height/screenDiv;
	}
	if (rotation == 3)
	{
		offsetX = inum * height / screenDiv - (-multX+1) * pic.width/screenDiv;					
		offsetY = 0;
	}
	if (mode == 0)
	{
		ctx = rotateCtx(canvas);			
		ctx.drawImage(pic, -(sumW)+offsetX, -(sumH)+offsetY, (pic.width/screenDiv) - multX * (pic.width/screenDiv), (pic.height/screenDiv) - multY * (pic.height/screenDiv));
		//ctx.drawImage(pic, -(sumW), -(sumH), (pic.width/screenDiv) - multX * (pic.width/screenDiv), (pic.height/screenDiv) - multY * (pic.height/screenDiv));
	}
	if (mode == 1)
	{
		if (rotation == 0 || rotation == 2)
			ctx.drawImage(pic, -(sumW), -(sumH)+offsetY, (jnum*width/screenDiv), (pic.height/screenDiv) - multY * (pic.height/screenDiv));
		if (rotation == 1 || rotation == 3)
			ctx.drawImage(pic, -(sumW)+offsetX, -(sumH)+offsetY, (inum*height/screenDiv), (pic.height/screenDiv) - multY * (pic.height/screenDiv));
	}
	if (mode == 2)
	{
		if (rotation == 0 || rotation == 2)
			ctx.drawImage(pic, -(sumW)+offsetX, -(sumH), (pic.width/screenDiv) - multX * (pic.width/screenDiv), (inum*height/screenDiv));
		if (rotation == 1 || rotation == 3)
			ctx.drawImage(pic, -(sumW)+offsetX, -(sumH), (pic.width/screenDiv) - multX * (pic.width/screenDiv), (jnum*width/screenDiv));	
	}
	if (mode == 3)
	{
		if (rotation == 0 || rotation == 2)
			ctx.drawImage(pic, -(sumW), -(sumH), (jnum*width/screenDiv), (inum*height/screenDiv));
		if (rotation == 1 || rotation == 3)
			ctx.drawImage(pic, -(sumW), -(sumH), (inum*height/screenDiv), (jnum*width/screenDiv));
	}
}


function send()   //посылаю на сервер json с картинкой закодированной в base64
/* увеличиваю canvas-ы до их оригинального размера и отрисовываю в них картинку оригинального размера
содержимое canvas-ов отправляю на сервер, уменьшаю canvas-ы и отрисовываю уменьшенную картинку
*/
{
	var inum = document.getElementById('drawTable').rows.length;
	var jnum = document.getElementById('drawTable').rows[0].cells.length;
	var height, width;
	
	var height = getHW()[0];
	var width = getHW()[1];

	pic = new Image();
	pic.onload = function()   
	{
		if (rotation == 0 || rotation == 2)
			var sumH = 0;//0;
		else 
			var sumW = 0;//90

		for (var i = 0; i < inum; i++)
		{
			if (rotation == 0 || rotation == 2)
				var sumW = 0;//0;
			else 
				var sumH = 0;//90

			var url;
			for (var j = 0; j < jnum; j++)
			{
				
				var canId = getId(i, j, inum, jnum);

				var canvas = document.getElementById(canId);
				var ctx = canvas.getContext("2d");

				// Увеличиваю canvas-ы до оригинального размера(1280x960)
				canvas.height = canvas.height*screenDiv;		
				canvas.width = canvas.width*screenDiv;
				ctx.fillStyle = "#FFFFFF";
				ctx.fillRect(0,0, canvas.width, canvas.height);
				// Отрисовываю в них картинку оригинального размера
				drawing(canvas,  pic, sumW*screenDiv, sumH*screenDiv, inum, jnum, multX, multY, 1, height, width, mode);

				url = document.getElementById(canId).toDataURL();   //беру url картинки из canvas
				// формирую название картинки
				upload(url, getName(pic, i, j, inum, jnum)); // url - url картинки из canvas, name - название картинки
				
				
				// Обратно уменьшаю
				canvas.height = canvas.height/screenDiv;
				canvas.width = canvas.width/screenDiv;
				ctx.fillStyle = "#FFFFFF";
				ctx.fillRect(0,0, canvas.width, canvas.height);

				drawing(canvas,  pic, sumW, sumH, inum, jnum, multX, multY, screenDiv, height, width, mode);

				if (rotation == 0 || rotation == 2)
					sumW += canvas.width;
				else 
					sumH += canvas.width;	//90
			}
			var canvas = document.getElementById("canvas0_0");
			if (rotation == 0 || rotation == 2)
				sumH += canvas.height;
			else 
				sumW += canvas.height;	//90
		}
	}
	pic.src = URL.createObjectURL(document.getElementById('pic').files[0]); 
	
		$.ajax({
		url: "/send",
		type: 'GET'
		});
	

}

function upload(dataURL, name) //функция с ajax запросом
{
	// формирую json
	var data = {
		data: "'" + dataURL + "'",
		name: "" + name + ""
		};
	//отправляю json на сервер
	$.ajax({
		url: "/upload",
		dataType: "json",
		contentType: "application/json",
		data: JSON.stringify(data),
		type: 'POST'
		});
}
