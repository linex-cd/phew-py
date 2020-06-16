(function ($) {
 "use strict";
		
		$.get("state/jobcounter", function(ret){
			$("#job_total").text(ret['data']['job_total']);
			$("#task_total").text(ret['data']['task_total']);
			$("#job_pending").text(ret['data']['job_pending']);
			$("#task_pending").text(ret['data']['task_pending']);
			
			$('.jobcounter').counterUp({
				delay: 10,
				time: 1000
			});	
			
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
								<td >'+item[3]+'&nbsp;&nbsp;&nbsp;<span style="color:gray;font-size:10px">'+ts+'<span></td>\
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
				latest_task_htmlstr = '没有文件正在处理中'
			}
			
			
			
			$('#latest_task').html(latest_task_htmlstr);
			
		});  
		
		$.get("state/nodecounter", function(ret){
			$("#vendor_count").text(ret['data']['vendor_count']);
			$("#worker_count").text(ret['data']['worker_count']);
			
			$('.nodecounter').counterUp({
				delay: 10,
				time: 1000
			})
			
			var workers_htmlstr = ''
			var workers = ret['data']['workers']
			
			var len = workers.length
			for(var i = 0; i < len; i++){
				var item = workers[i]
				var time = new Date()
				time.setTime(parseInt(item['ping_time'])*1000)
				var ts = time.toLocaleString()
				var str = '<li class="list-group-item">\
								<div class="checkbox checkbox-primary">\
									<input class="todo-done" type="checkbox" checked="" readonly />\
									<label>'+item['location']+':'+item['name']+'<br/>'+item['ip']+'&nbsp;&nbsp;'+ts+'</label>\
								</div>\
							</li>'
				workers_htmlstr = str + workers_htmlstr
			}
			if (workers_htmlstr == ''){
				workers_htmlstr = '<div class="recent-post-signle">没有工作节点</div>'
			}
			
			var vendors_htmlstr = ''
			var vendors = ret['data']['vendors']
			
			var len = vendors.length
			for(var i = 0; i < len; i++){
				var item = vendors[i]
				var time = new Date()
				time.setTime(parseInt(item['ping_time'])*1000)
				var ts = time.toLocaleString()
				var str = '<li class="list-group-item">\
								<div class="checkbox checkbox-primary">\
									<input class="todo-done" type="checkbox" checked="" readonly />\
									<label>'+item['location']+':'+item['name']+'<br/>'+item['ip']+'&nbsp;&nbsp;'+ts+'</label>\
								</div>\
							</li>'
				vendors_htmlstr = str + vendors_htmlstr
			}
			if (vendors_htmlstr == ''){
				vendors_htmlstr = '<div class="recent-post-signle">没有业务节点</div>'
			}
			
			$('#node-list').html(vendors_htmlstr+workers_htmlstr);
		});  

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

})(jQuery); 