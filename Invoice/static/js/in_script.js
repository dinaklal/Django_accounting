$(document).ready(function() {



  function calc_gnd_total()
  {
    total= $('#sub_total').val()- $('#discount').val()
    $('#total_amount').val(total.toFixed(2));
  
  }
  function calc_total()
  {
    total=0;
    $('.total').each(function() {
          total += parseInt($(this).val());
      });
    $('#sub_total').val(total.toFixed(2));
    calc_gnd_total()
  }

  

  function calc_total_units()
  {
    total=0;
    $('.units').each(function() {
          total += parseInt($(this).val());
      });
    $('#tot_units').val(total.toFixed(2));
  
  }

  $myFunction = function(id1) {


    var id = $(id1).attr('id');

    var selid = "selid" + id;
    //var sel = $('<select id='+selid+'  class="form-control" >')\
    var sel = $('<select class="form-control sel_auto sel_"  name=' + selid + ' id=' + selid + '>');
    $(sites).each(function() {
      sel.append($("<option>").attr('value', this.id).text(this.name));
    });



    var row = $("<tr/>");
    sel = $("<td/>").append(sel)
    var sel1id = "sel1id" + id;
    var sel1 = $('<select class="form-control sel1_"  name=' + sel1id + ' id=' + sel1id + '>');
    sel1.append($("<option>").attr('value', "3200").text("3200"));
    sel1.append($("<option>").attr('value', "3100").text("3100"));
    sel1.append($("<option>").attr('value', "1").text("Specify in Loads"));
    sel1 = $("<td/>").append(sel1)


    var inpid = "inpid" + id
    var inp = $("<td/>").append("<input type='text' placeholder='Unit price' value='" + sites[0].Unit_price + "'   name=" + inpid + " class='form-control' id=" + inpid + " readonly>");


    var lodid = "lodid" + id
    var lod = $("<td/>").append("<input type='text' placeholder='No of Loads'  name=" + lodid + "  class='form-control textinput' id=" + lodid + " required>");

    var untid = "untid" + id
    var unt = $("<td/>").append("<input type='text' placeholder='Total Units'  name=" + untid + "  class='form-control units' id=" + untid + " readonly>");



    var totid = "totid" + id
    var tot = $("<td/>").append("<input type='text'  placeholder='Total price'  name=" + totid + " class='form-control total' id=" + totid + " readonly>");


    var rm_button = $("<td/>").append("<button   class='btn btn-danger remove_b' > <i class='more-less glyphicon glyphicon-minus'></i></button>");
    row.append(sel);
    row.append(sel1);
    row.append(lod);
    row.append(unt);
    row.append(inp);
    row.append(tot);
    row.append(rm_button);



    $("#ttb").append(row);

    id = parseInt(id) + 1
    $(id1).attr('id', id);
    change_sel();
    change_sel1();

    $(document).on('click', '.remove_b', function() {
      $(this).closest('tr').remove();
      calc_total();
      calc_total_units()
    });

    $('input.discount_').on('input', function(e) {
      calc_total()
    });

    $('input.textinput').on('input', function(e) {
      var i = $(this).attr('id');
      tot_id = i.replace('lod', 'tot');
      unt_id = i.replace('lod', 'unt');
      unit_price_id = i.replace('lod', 'inp');
      up = $('input[id=' + unit_price_id + ']').val();
      sel1_id = i.replace('lod', 'sel1');
      sel1 = $('select[id=' + sel1_id + ']').children("option:selected").val();
      var utc = new Date().toJSON().slice(0,10).replace(/-/g,'/');
      $('input[id=date]').val(utc);
      console.log(sel1)
      $('input[id=' + tot_id + ']').val(up * $(this).val() * sel1)
      $('input[id=' + unt_id + ']').val($(this).val() * sel1)
      calc_total();
      calc_total_units()
    });

   

  }




  function change_sel() {
    $('.sel_').on('change', function() {
      var i = $(this).attr('id');
      i = i.replace('sel', 'inp');
      console.log(i);
      var sel_id = $(this).children("option:selected").val();
      console.log(sel_id);
      var price = 1
      $(sites).each(function() {
        if (this.id == sel_id) {
          price = this.Unit_price
        }
      });
      console.log(price);
      $('input[id=' + i + ']').val(price)

      tot_id = i.replace('inp', 'tot');
      sel1_id = i.replace('inp', 'sel1');
      sel1 = $('select[id=' + sel1_id + ']').children("option:selected").val();
      up = $('input[id=' + i + ']').val();

      lod_id = i.replace('inp', 'lod');
      lods = $('input[id=' + lod_id + ']').val();


      $('input[id=' + tot_id + ']').val(up * lods * sel1);
      calc_total();
      calc_total_units()
    });
  }

  function change_sel1() {
    $('.sel1_').on('change', function() {
      var i = $(this).attr('id');
      unit_price_id = i.replace('sel1', 'inp');
      unt_id = i.replace('sel1', 'unt');
      console.log(i);
      var sel1 = $(this).children("option:selected").val();
      tot_id = i.replace('sel1', 'tot');
      up = $('input[id=' + unit_price_id + ']').val();
      console.log(sel1)
      lod_id = i.replace('sel1', 'lod');
      lods = $('input[id=' + lod_id + ']').val();


      $('input[id=' + tot_id + ']').val(up * lods * sel1)
      $('input[id=' + unt_id + ']').val(lods * sel1)
      calc_total();
      calc_total_units()
    });
  }

 
  $myFunction(document.getElementById(0));
  // this.attr("id","2");










});
