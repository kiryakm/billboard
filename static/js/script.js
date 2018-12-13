
		var multX = 0;		// Множитель по X
		var multY = 0;		// по Y
		var screenDiv = 4;	// Делитель экранов для отображения (чем больше картинка тем меньше экраны)
		var mode = 0;		// Для растяжения финальной картинки 0 - норм, 1 - растяжение по X, 2 - по Y, 3 - максимальное растяжение
		var rotation = 0;	// 0-0 1-90 2-180 3-270

		var origCanvas = document.getElementByName('origCanvas');
		var click = false;
		origCanvas.addEventListener('mousedown', canvasDown, false);
		origCanvas.addEventListener('mouseup', canvasUp, false);
		origCanvas.addEventListener('mousemove', mouseMove, false);

		function canvasDown(ev)
		{
            click = true;
            alert("asd")
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

		function redraw(x, y)
		{
			pic = new Image();
			pic.onload = function()
			{
				var rect = origCanvas.getBoundingClientRect();
				var sm = 320/pic.height;

				if (rotation == 0 || rotation == 2)
					multX = (1-x/(pic.width*sm));
				else
					multX = (1-y/(pic.width*sm));
					
				multY = multX;
				drawOriginal(multX, multY);
				makeTable(multX, multY)
			}
			pic.src = URL.createObjectURL(document.getElementById('pic').files[0]); 
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

		function drawOriginal(multX, multY)
		{
			pic = new Image();
			pic.onload = function()
			{
				var origCan = document.getElementById("origImg");
				var ctx = origCan.getContext("2d");
				var sm = 320/pic.height;	// screen multiplier нужен что бы оригинальная картинка отображалась одного размера, размер зависит от соотношения сторон 
				if (rotation == 0 || rotation == 2)
				{
					origCan.height = pic.height*sm;
					origCan.width = pic.width*sm;
				}
				else
				{
					origCan.width = pic.height*sm;
					origCan.heigth = pic.width*sm;
				}
				
				ctx = rotateCtx(origCan, ctx)

				//0
				if (rotation == 0)
					ctx.drawImage(pic, 0, 0, origCan.width - multX * origCan.width, origCan.height - multY * origCan.height);				
				//90
				if (rotation == 1)
					ctx.drawImage(pic, 0,  0, origCan.height - multY * origCan.height, origCan.width - multX * origCan.width);
				//180
				if (rotation == 2)
					ctx.drawImage(pic, 0, 0, origCan.width - multX * origCan.width, origCan.height - multY * origCan.height);			
				//270
				if (rotation == 3)
					ctx.drawImage(pic, 0,  0, origCan.height - multY * origCan.height, origCan.width - multX * origCan.width);
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
			if (inum <= 3 && jnum <= 3)
					screenDiv = 4;
			if ((inum > 3 && inum <=6) || (jnum > 3 && jnum <=6))
					screenDiv = 6;
			if ((inum > 6) || (jnum > 6))
					screenDiv = 8;
		}

		function getInf(height, width, inum, jnum)	// Получить информацию
		{
			pic = new Image();
			pic.src = URL.createObjectURL(document.getElementById('pic').files[0]);
			document.getElementById("picRes").innerHTML = "Uploaded image resalution: " + pic.width + "x" + pic.height;
			document.getElementById("endRes").innerHTML = "Resalution of screens: " + width*jnum + "x" + height*inum;
			document.getElementById("quantOfScreens").innerHTML = "Quantity of screens: " + inum*jnum;
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
			pic.src = URL.createObjectURL(document.getElementById('pic').files[0]);
			if (rotation == 0 || rotation == 2)
			{
				inum = Math.ceil((pic.height - multY * (pic.height))/height);	// Число строк
				jnum = Math.ceil((pic.width - multX * (pic.width))/width);		// Число столбцов
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
				var idRow= "tr"+i;
				if (document.getElementById(idRow))
					document.getElementById(idRow).remove();
			}

	        for (var i = 0; i < inum; i++)		// Формируем таблицу для вывода
			{
				var idRow= "tr"+i;
				var newRow = document.createElement('tr');
				newRow.id = idRow;
				table.appendChild(newRow);
				for (var j = 0; j < jnum; j++)
				{
					var idCol = "td"+i+"_"+j;
					var newCol = document.createElement('td');
					newCol.id = idCol;
					var str = '<canvas id="canvas'+ i + '_' + j + '" height="' + height/screenDiv + '" width="'+ width/screenDiv + '" style="border:1px solid #000000;"></canvas>'
					newCol.innerHTML += str;
					newRow.appendChild(newCol);
				}
			}

			mode = 0;
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
				var origCan = document.getElementById("origImg");
				var ctx = origCan.getContext("2d");
				
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
						var canId;
						if (rotation == 0)
							canId = 'canvas'+ i + '_' + j;
						if (rotation == 1)
							canId = 'canvas'+ i + '_' + (jnum-1-j);
						if (rotation == 2)
							canId = 'canvas'+ (inum-1-i) + '_' + (jnum-1-j);
						if (rotation == 3)
							canId = 'canvas'+ (inum-1-i) + '_' + j;

						var canvas = document.getElementById(canId);
						var ctx = canvas.getContext("2d");
						ctx.fillStyle = "#FFFFFF";	
						ctx.fillRect(0,0, canvas.width, canvas.height);	// Заполнить canvas белым
						// Отрисовать поверх
						draw2(canvas, ctx, pic, sumW, sumH, inum, jnum, multX, multY, screenDiv, height, width, mode, true);
						
						if (rotation == 0 || rotation == 2)
							sumW += canvas.width;	//0 180
						else 
							sumH += canvas.width;	//90 270
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

		function draw2(origCan, ctx, pic, sumW, sumH, inum, jnum, multX, multY, screenDiv, height, width, mode, rotate)
		{
			if (mode == 0)
			{
				ctx = rotateCtx(origCan, ctx);
				ctx.drawImage(pic, -(sumW), -(sumH), (pic.width/screenDiv) - multX * (pic.width/screenDiv), (pic.height/screenDiv) - multY * (pic.height/screenDiv));
				return;
			}
			if (mode == 1)
			{
				if (rotation == 0 || rotation == 2)
					ctx.drawImage(pic, -(sumW), -(sumH), (jnum*width/screenDiv), (pic.height/screenDiv) - multY * (pic.height/screenDiv));
				if (rotation == 1 || rotation == 3)
					ctx.drawImage(pic, -(sumW), -(sumH), (inum*height/screenDiv), (pic.height/screenDiv) - multY * (pic.height/screenDiv));
			}
			if (mode == 2)
			{
				if (rotation == 0 || rotation == 2)
					ctx.drawImage(pic, -(sumW), -(sumH), (pic.width/screenDiv) - multX * (pic.width/screenDiv), (inum*height/screenDiv));
				if (rotation == 1 || rotation == 3)
					ctx.drawImage(pic, -(sumW), -(sumH), (pic.width/screenDiv) - multX * (pic.width/screenDiv), (jnum*width/screenDiv));	
			}
			if (mode == 3)
			{
				if (rotation == 0 || rotation == 2)
					ctx.drawImage(pic, -(sumW), -(sumH), (jnum*width/screenDiv), (inum*height/screenDiv));
				if (rotation == 1 || rotation == 3)
					ctx.drawImage(pic, -(sumW), -(sumH), (inum*height/screenDiv), (jnum*width/screenDiv));
			}
		}

		function rotateCtx(canvas, ctx)
		{
			if (rotation == 1)
			{
				ctx.translate(canvas.width, 0);
				ctx.rotate(90*Math.PI / 180);
			}
			//180
			if (rotation == 2)
			{
				ctx.translate(canvas.width, canvas.height);		
				ctx.rotate(180*Math.PI / 180);
			}				
			//270
			if (rotation == 3)
			{
				ctx.translate(0, canvas.height);	
				ctx.rotate(270*Math.PI / 180);
			}
			
			return ctx;
		}

        function send()   //посылаю на сервер json с картинкой закодированной в base64
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
						var canId;
						if (rotation == 0)
							canId = 'canvas'+ i + '_' + j;
						if (rotation == 1)
							canId = 'canvas'+ i + '_' + (jnum-1-j);
						if (rotation == 2)
							canId = 'canvas'+ (inum-1-i) + '_' + (jnum-1-j);
						if (rotation == 3)
							canId = 'canvas'+ (inum-1-i) + '_' + j;

						var canvas = document.getElementById(canId);
						var ctx = canvas.getContext("2d");

						// Увеличиваю canvas-ы до оригинального размера(1280x960)
						canvas.height = canvas.height*screenDiv;		
						canvas.width = canvas.width*screenDiv;
						ctx.fillStyle = "#FFFFFF";
						ctx.fillRect(0,0, canvas.width, canvas.height);
						// Отрисовываю в них картинку оригинального размера
						ctx = rotateCtx(canvas, ctx)
						
						draw2(canvas, ctx, pic, sumW*screenDiv, sumH*screenDiv, inum, jnum, multX, multY, 1, height, width, mode, false);

	                	url = document.getElementById(canId).toDataURL();   //беру url картинки из canvas
						// формирую название картинки
						if  (document.getElementById('vert').checked == true)
							name = "Vert"+pic.width+"x"+pic.height+" "+i+"_"+j;
						if  (document.getElementById('hor').checked == true)
							name = "Hor"+pic.width+"x"+pic.height+" "+i+"_"+j;

	                	upload(url, name); // url - url картинки из canvas, name - название картинки
						
						
						canvas.height = canvas.height/screenDiv;
						canvas.width = canvas.width/screenDiv;
						ctx.fillStyle = "#FFFFFF";
						ctx.fillRect(0,0, canvas.width, canvas.height);

						ctx = rotateCtx(canvas, ctx)
						draw2(canvas, ctx, pic, sumW, sumH, inum, jnum, multX, multY, screenDiv, height, width, mode, false);

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
