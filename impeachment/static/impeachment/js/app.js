
// Document Ready Action
$(document).ready(function(){
  enable_buttons();
  $('#register_id').mask("0000 0000 0000", {selectOnFocus: true});
});

// Action Btn
function enable_buttons(argument) 
{
  $("#contra").click(function(){
   if_valid_save_vote('0');
      
  }); 
 
  $("#a-favor").click(function(){
    if_valid_save_vote('1');
  }); 

  $("#indeciso").click(function(){
    if_valid_save_vote('2');
  });
}

// Validation
var is_valid = false;
function if_valid_save_vote(vote) {
  // Set default
  var register_id = get_register_id() ;
  
  // Call API VALIDATOR
  $.get( '/votopopular/isvalid/' + register_id ).done(function( data ) {
    if(data['isvalid'] == '1'){
      $('#input').removeClass('has-error').addClass('has-success');
      save(vote);
    }else{
      $('#input').removeClass('has-success').addClass('has-error');
      report_error();
    }
  });
}

function set_isvalid_false(){
  is_valid = false;
}

function set_isvalid_true(){
  is_valid = true;
}

function report_error() {
  alert('Informe seu título de eleitor corretamente');
}

// helpers
function save(vote){
  var url = get_url(vote)
  $.get( url ).done(function( data ) {
    alert('Voto computado');
  });
}

function get_url(vote){
  var id = get_register_id();
  var url = "/votopopular/vote/" + id + "/" + vote;

  return url;
}

function get_register_id(){
  var str = $('#register_id').val() ;
  return str.replace(/\s/g, "");
}


// Chart.js
$.get( 'votopopular/api/impeachment/counted_votes' ).done(function( votes ) {
  create_chart(votes['against'], votes['in_favor'], votes['undecided']);
});
function create_chart(x, y, z){
  var config = {
      type: 'pie',
      data: {
          labels: ["contra", "a favor", "indeciso"],
          datasets: [
          {
              data: [x, y, z],
              backgroundColor: [
                  "#d9534f",
                  "#5cb85c",
                  "#f0ad4e"
              ],
              hoverBackgroundColor: [
                  "#FF6384",
                  "#8fd18f",
                  "#FFCE56"
              ]
          }]
      }
  };
  var ctx = document.getElementById("myChart");
  var myPieChart = new Chart(ctx, config);
}