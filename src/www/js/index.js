(function ($) {
 "use strict";
		
		/////////////////////////////////////////////////
		
		$.get("state/sysstate", function(ret){
			$("#db").attr('data-rel', ret['data']['db']);
			$("#cpu").attr('data-rel', ret['data']['cpu']);
			$("#gpu").attr('data-rel', ret['data']['gpu']);
			$("#disk").attr('data-rel', ret['data']['disk']);
			$("#network").attr('data-rel', ret['data']['network']);
			$("#temp").attr('data-rel', ret['data']['temp']);
			
			//knob
			if(typeof($.fn.knob) != 'undefined') {
				$('.knob').each(function () {
				  var $this = $(this),
					  knobVal = $this.attr('data-rel');
			
				  $this.knob({
					'draw' : function () { 
					  $(this.i).val(this.cv + '%')
					}
				  });
				  
				  $this.appear(function() {
					$({
					  value: 0
					}).animate({
					  value: knobVal
					}, {
					  duration : 2000,
					  easing   : 'swing',
					  step     : function () {
						$this.val(Math.ceil(this.value)).trigger('change');
					  }
					});
				  }, {accX: 0, accY: -150});
				});
			}	
			
			
		});  
		
		/////////////////////////////////////////////////
		
		$.get("state/jobcounter", function(ret){
			$("#job_total").text(ret['data']['job_total']);
			$("#task_total").text(ret['data']['task_total']);
			$("#job_pending").text(ret['data']['job_pending']);
			$("#work_pending").text(ret['data']['work_pending']);
			
			$('.jobcounter').counterUp({
				delay: 10,
				time: 1000
			});	
			
		});  
		
		/////////////////////////////////////////////////
		
		$.get("state/latestwork", function(ret){
			
			var latest_job_htmlstr = ''
			var job_latest = ret['data']['job_latest']
			var len = job_latest.length
			for(var i = 0; i < len; i++){
				var item = job_latest[i]
				var time = new Date()
				time.setTime(parseInt(item[0])*1000)
				var ts = time.toLocaleString()
				var str = '<tr>\
								<td class="f-500 c-cyan">'+item[2]+'</td>\
								<td >'+item[3]+'&nbsp;&nbsp;&nbsp;<span style="color:gray;font-size:12px">'+ts+'<span></td>\
								<td class="f-500 c-cyan">'+item[1]+'</td>\
							</tr>'
				latest_job_htmlstr = str + latest_job_htmlstr
			}
			
			$('#latest_job').html(latest_job_htmlstr);
			
			var latest_task_htmlstr = ''
			var task_latest = ret['data']['task_latest']
			var len = task_latest.length
			for(var i = 0; i < len; i++){
				var item = task_latest[i]
				
				var str = '<div class="recent-post-signle">\
                                    <div class="recent-post-flex rct-pt-mg">\
                                        <div class="recent-post-img">\
                                            <img src="img/'+item['port']+'.png" alt="" />\
                                        </div>\
                                        <div class="recent-post-it-ctn">\
                                            <a href="#"><h5>'+item['description']+'</h5></a>\
                                            <a href="#"><p title="'+item['data']+'" >'+item['data']+'/p></a>\
                                        </div>\
                                    </div>\
                            </div>'
				latest_task_htmlstr = str + latest_task_htmlstr
			}
			if (latest_task_htmlstr == ''){
				latest_task_htmlstr = '<div>没有文件正在处理中<div>'
			}
			
			
			
			$('#latest_task').html(latest_task_htmlstr);
			
		});  
		
		/////////////////////////////////////////////////
		
		$.get("state/nodecounter", function(ret){
			$("#vendor_count").text(ret['data']['vendor_count']);
			$("#worker_count").text(ret['data']['worker_count']);
			
			$('.nodecounter').counterUp({
				delay: 10,
				time: 1000
			})
			
			//map count
			var workerslen_jiangsu = 0
			var workerslen_zhejiang = 0
			
			//city
			var worker_city = []
			var vendor_city = []
			
			////
			var workers_htmlstr = ''
			var workers = ret['data']['workers']
			
			var len = workers.length
			for(var i = 0; i < len; i++){
				var item = workers[i]
				
				var isonline = ''
				if (item['state']=='online'){
					isonline = 'checked'
				}
				
				var time = new Date()
				time.setTime(parseInt(item['ping_time'])*1000)
				var ts = time.toLocaleString()
				var str = '<li class="list-group-item">\
								<div class="checkbox checkbox-primary">\
									<input class="todo-done" type="checkbox" '+isonline+' readonly />\
									<label>'+item['location']+':'+item['name']+'<br/><span style="color:gray;font-size:12px">'+item['ip']+'&nbsp;&nbsp;'+ts+'</span></label>\
								</div>\
							</li>'
				workers_htmlstr = str + workers_htmlstr
				
				if (item['location'] == '南京'){
					workerslen_jiangsu = workerslen_jiangsu + 1
				}
				
				if (item['location'] == '杭州'){
					workerslen_zhejiang = workerslen_zhejiang + 1
				}
				
				//worker_city
				if (worker_city.includes(item['location']) == false){
					worker_city.push(item['location'])
				}
			}
			if (workers_htmlstr == ''){
				workers_htmlstr = '<div class="recent-post-signle">没有工作节点</div>'
			}
			
			//city tag
			var worker_city_str = ''
			for(var i = 0; i < worker_city.length; i++){

				var str = '<div class="realtime-bw">\
								<span>'+worker_city[i]+'</span>\
							</div>'
				worker_city_str = str + worker_city_str
				
			}

			$('#worker_city').html(worker_city_str);
			
			
			/////
			var vendors_htmlstr = ''
			var vendors = ret['data']['vendors']
			
			var len = vendors.length
			for(var i = 0; i < len; i++){
				var item = vendors[i]
				
				var isonline = ''
				if (item['state']=='online'){
					isonline = 'checked'
				}
				
				var time = new Date()
				time.setTime(parseInt(item['ping_time'])*1000)
				var ts = time.toLocaleString()
				var str = '<li class="list-group-item">\
								<div class="checkbox checkbox-primary">\
									<input class="todo-done" type="checkbox" '+isonline+' readonly />\
									<label>'+item['location']+':'+item['name']+'<br/><span style="color:gray;font-size:12px">'+item['ip']+'&nbsp;&nbsp;'+ts+'</span></label>\
								</div>\
							</li>'
				vendors_htmlstr = str + vendors_htmlstr
				
				//vendor_city
				if (vendor_city.includes(item['location']) == false){
					vendor_city.push(item['location'])
				}
			}
			if (vendors_htmlstr == ''){
				vendors_htmlstr = '<div class="recent-post-signle">没有业务节点</div>'
			}
			
			$('#node-list').html(vendors_htmlstr+workers_htmlstr);
			
			//city tag
			var vendor_city_str = ''
			for(var i = 0; i < vendor_city.length; i++){

				var str = '<div class="realtime-bw">\
								<span>'+vendor_city[i]+'</span>\
							</div>'
				vendor_city_str = str + vendor_city_str
				
			}

			$('#vendor_city').html(vendor_city_str);
			
			
			//map
			var cityName = [
					{id: "CN-32", name: "江苏",},
					{id: "CN-52", name: "贵州",},
					{id: "CN-53", name: "云南",},
					{id: "CN-50", name: "重庆",},
					{id: "CN-51", name: "四川",},
					{id: "CN-31", name: "上海",},
					{id: "CN-54", name: "西安",},
					{id: "CN-33", name: "浙江",},
					{id: "CN-15", name: "内蒙古"},
					{id: "CN-14", name: "山西",},
					{id: "CN-",   name: "福建",},
					{id: "CN-12", name: "天津",},
					{id: "CN-13", name: "河北",},
					{id: "CN-11", name: "北京",},
					{id: "CN-34", name: "安徽",},
					{id: "CN-36", name: "江西",},
					{id: "CN-37", name: "山东",},
					{id: "CN-41", name: "河南",},
					{id: "CN-43", name: "湖南",},
					{id: "CN-42", name: "河北",},
					{id: "CN-45", name: "广西",},
					{id: "CN-44", name: "广东",},
					{id: "CN-46", name: "海南",},
					{id: "CN-65", name: "新疆",},
					{id: "CN-64", name: "宁夏",},
					{id: "CN-63", name: "青海",},
					{id: "CN-62", name: "甘肃",},
					{id: "CN-61", name: "陕西",},
					{id: "CN-23", name: "黑龙江",},
					{id: "CN-22", name: "吉林",},
					{id: "CN-21", name: "辽宁",},
				];
				
				
				var mapData = {
					"CN-32": workerslen_jiangsu,
					"CN-52": 0,
					"CN-53": 0,
					"CN-50": 0,
					"CN-51": 0,
					"CN-31": 0,
					"CN-54": 0,
					"CN-33": workerslen_zhejiang,
					"CN-15": 0,
					"CN-14": 0,
					"CN-"  : 0,
					"CN-12": 0,
					"CN-13": 0,
					"CN-11": 0,
					"CN-34": 0,
					"CN-36": 0,
					"CN-37": 0,
					"CN-41": 0,
					"CN-43": 0,
					"CN-42": 0,
					"CN-45": 0,
					"CN-44": 0,
					"CN-46": 0,
					"CN-65": 0,
					"CN-64": 0,
					"CN-63": 0,
					"CN-62": 0,
					"CN-61": 0,
					"CN-23": 0,
					"CN-22": 0,
					"CN-21": 0,
				};

				$('#world-map').vectorMap({
					map: 'cn_mill',
					
					backgroundColor: "transparent",
					regionStyle: {
						initial: {
							fill: '#00c292',
							"fill-opacity": 0.6,
							stroke: 'none',
							"stroke-width": 0,
							"stroke-opacity": 0
						}
					},

					series: {
						regions: [{
							values: mapData,
							scale: ["#cccccc", "#00c292"],
							normalizeFunction: 'polynomial'
						}]
					},
					
					focusOn: {
					  x: 0.5,
					  y: 0.5,
					  scale: 1,
					  animate: true
					},

			　　　　onRegionTipShow: function (event, label, code) {
			　　　　　　$.each(cityName, function (i, items) {
			　　　　　　　　if (code == items.id) {
			　　　　　　　　　　label.html(items.name + " " + mapData[code]);
			　　　　　　　　}
			　　　　　　});
			　　　　},
					
				});
				//end map
				
		});  

		
		
		
  


})(jQuery); 