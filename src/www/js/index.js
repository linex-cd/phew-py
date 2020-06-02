(function ($) {
 "use strict";
		
		$.get("state/totalcounter", function(ret){
			$("#tasks").text(ret['data']['tasks']);
			$("#files").text(ret['data']['files']);
			$("#inqueuetasks").text(ret['data']['inqueuetasks']);
			$("#inqueuefiles").text(ret['data']['inqueuefiles']);
			
			$('.totalcounter').counterUp({
				delay: 10,
				time: 1000
			});	
		});  
		
		$.get("state/vendorcounter", function(ret){
			$("#vendors").text(ret['data']['vendors']);
			$("#cities").text(ret['data']['cities']);
			
			$('.vendorcounter').counterUp({
				delay: 10,
				time: 1000
			})
		});  
		
		$.get("state/successcounter", function(ret){
			$("#successtasks").text(ret['data']['successtasks']);
			$("#failedtasks").text(ret['data']['failedtasks']);
			$("#successfiles").text(ret['data']['successfiles']);
			$("#failedfiles").text(ret['data']['failedfiles']);
			
			$('.successcounter').counterUp({
				delay: 10,
				time: 1000
			})
		});  
		
		$.get("state/sysstate", function(ret){
			$("#load").attr('data-rel', ret['data']['load']);
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