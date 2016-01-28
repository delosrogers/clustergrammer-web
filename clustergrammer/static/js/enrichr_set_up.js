function enrichr_set_up(cgm, network_data){

  var query_string = QueryStringToJSON();
  var enr_score_type = 'combined_score';

  // fitler based on N_row_sum
  var sub_views = _.filter(network_data.views, function(d){return _.has(d,'N_row_sum');});

  // filter based on enr_score_type
  sub_views = _.filter(sub_views, 
    function(d){
      return d.enr_score_type == enr_score_type;
    });

  inst_N = query_string.N_row_sum;

  // initialize the slider 
  ini_enr_slider(cgm, sub_views, inst_N, enr_score_type);

}


function ini_enr_slider(cgm, sub_views, inst_N, enr_score_type){
  var filter_type = 'N_row_sum_enr';

  var inst_max = sub_views.length - 1;

  $( '#slider_'+filter_type ).slider({
    value:0,
    min: 0,
    max: inst_max,
    step: 1,
    stop: function( event, ui ) {

      // change value 
      $( "#amount" ).val( "$" + ui.value );

      // get value 
      var inst_index = $( '#slider_'+filter_type ).slider( "value" ); 

      var inst_top = N_dict[inst_index];

      change_view = {
        'N_row_sum':inst_top,
        'enr_score_type':enr_score_type
      };
      filter_name = 'N_row_sum';

      d3.select('#main_svg').style('opacity',0.70);

      d3.select('#'+filter_type).text('Top rows: '+inst_top+' rows'); 

      $('.slider_filter').slider('disable');
      d3.selectAll('.btn').attr('disabled',true);

      cgm.update_network(change_view);

      // ini_sliders();

      function enable_slider(){
        $('.slider_filter').slider('enable');  
        d3.selectAll('.btn').attr('disabled',null);
      }
      setTimeout(enable_slider, 2500);

    }
  });
  $( "#amount" ).val( "$" + $( '#slider_'+filter_type ).slider( "value" ) );


  // make N_dictionary 
  var N_dict = {};

  // filters
  var all_filt = _.pluck( sub_views,'N_row_sum');

  _.each(all_filt, function(d){
    tmp_index = _.indexOf(all_filt, d);
    N_dict[tmp_index] = d;
  });

  // get the index of the current requested value so that the slider can be
  // initialized 
  _.each(N_dict,function(d,i){
    if (String(d) === String(inst_N)){
      inst_index = i;
    }
  });

  // set up slider
  $('#slider_N_row_sum_enr').slider( "value", inst_index);

  // set up slider title
  d3.select('#N_row_sum_enr').text('Top rows:  '+inst_N+' rows');

}


function QueryStringToJSON() { 
  var pairs = location.search.slice(1).split('&');
  
  var result = {};
  pairs.forEach(function(pair) {
      pair = pair.split('=');
      result[pair[0]] = decodeURIComponent(pair[1] || '');
  });

  return JSON.parse(JSON.stringify(result));
}