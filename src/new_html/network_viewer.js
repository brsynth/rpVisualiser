$(function() {

  var cy = cytoscape({
    container: $('#cy')});


  function network(){   //CREATE THE INITIAL NETWORK
      cy.add(obj);


      var layout=cy.layout({
            name: 'dagre',
          });
      layout.run();

      cy.style(
        cytoscape.stylesheet()

          .selector( "node")
          .css({
              "label": "data(name)",
              "font-size": "14px"
            })

          .selector( "node[category='reaction']")
          .css({
            'background-color':"data(colour)",
            'shape': 'roundrectangle',
            'width': 100,
            'height': 100,
          })
         .selector("node[category='reactant']")
         .css( {
           'background-color': '#FFFFFF',
           'border-color': '#52be80',
           'border-width': 5,
           'background-image':'data(image)',
           'background-fit':'contain',
           'width': 200,
           'height': 200,
         })

         .selector("node[category='product']")
         .css( {
           'background-color': '#FFFFFF',
           'border-color': '#80D0D0',
           'border-width': 5,
           'background-image':'data(image)',
           'background-fit':'contain',
           'width': 200,
           'height': 200,
         })

        .selector( 'edge')
          .css( {
            'curve-style': 'bezier',
            'width': '3px',
            'target-arrow-shape': 'triangle',
            'line-color':"data(colour)",
          })


          .selector("node[root='target']")
          .css( {
            'border-color': '#C60800',
            'background-color': '#FFFFFF',
            'border-width': 10,

        })


        .selector('.mySecondClass')
        .css( {
        'background-color': 'blue',
          })

        )};

function displaynet(filt){
    network();
    cy.remove("node[root='target_reaction']") //delete the reaction target node

    Node_list=[];
    Edge_list=[];
    for (e in filt){ //For each pathway selected

      Filtered_nodes=cy.filter(function(element,i){
        return element.isNode() && (filt[e] in element.data("pathway"));
      });
      Filtered_edges=cy.filter('edge[pathway="'+filt[e]+'"]')

      Node_list.push(Filtered_nodes);
      Edge_list.push(Filtered_edges);
    };

    if (jQuery.inArray("all",filt)===(-1)){ //if "all" not selected
    cy.nodes().remove();
    for (j in Node_list){
      cy.add(Node_list[j])
    };
    for (k in Edge_list){
      cy.add(Edge_list[k])
    };
  };
  var layout=cy.layout({
        name: 'dagre',
      });
  layout.run();
  };

/*cy.on('mouseover','node',function(e){
var node_select=e.target;
molecule=node_select.data("image");
if(molecule){
$("#molecule").append(molecule)};
});

cy.on('mouseout','node',function(e){
$("#molecule").empty();
});*/

cy.on('tap','node',function(e){
var node_select=e.target;
console.log(node_select.data("name"));
link=node_select.data("link");
if(link){
  window.open(link)
};
if(node_select.data("category")==='reaction'){
  rsmiles=node_select.data("Rsmiles")
  console.log("C'est une rÃ©action");
  $("#react_img").empty();
  $(".inf1 > p").remove();
  $(".inf2 > p").remove();
  $("#reversibility>p").remove();
  $("#reversibility").append("<p>Reversible ? "+node_select.data("reversibility")+"</p>");
  $("#sub_rule_id").append("<p>"+node_select.data("rule_id")+"</p>");
  $("#sub_rule_score").append("<p>"+node_select.data("rule_score")+"</p>");
  $("#sub_o").append("<p>"+node_select.data("dfG_prime_o")+"</p>");
  $("#sub_m").append("<p>"+node_select.data("dfG_prime_m")+"</p>");
  $("#sub_uncert").append("<p>"+node_select.data("dfG_uncert")+"</p>");
  $("#sub_fba").append("<p>"+node_select.data("flux_value")+"</p>");
  $("#sub_fba_obj").append("<p>"+node_select.data("fba_obj_name")+"</p>");

  $("#selenzyme-link").empty();
  $("#selenzyme_table").empty();
  $("#information").show("slide", {direction: "right" }, 1000);
  ri=node_select.data("image2");
  ribig=node_select.data("image2big");
  $("#react_img").append(ri);
  $("#react_img").click(function(){
     $('#big_image').empty();
     $('#big_image').append(ribig);
     $('#zoom').show("slide", {direction: "right" }, 1000);
     });
 link="http://selenzyme.synbiochem.co.uk/results?smarts=" + encodeURIComponent( rsmiles )
 $("#selenzyme-link").append('<a target="_blank" href='+link+ '> Crosslink to Selenzyme' + '</a>');
 CreateTable(node_select.data("data_tab"));
};
});

//CREATE CHECKBOXES TO SELECT PATHWAYS INDIVIDUALLY
$('#table_path').find('tr').each(function(index){ //for each row in the pathway table
path_id=$(this).find('td').eq(0).text().trim() //name of the path for each row (result of previous sorts)
$(this).find('td').eq(1).html('<input type="checkbox" value='+path_id+'>'); //update select column with checkbox
});


function CreateTable(data) {

// EXTRACT VALUE FOR HTML HEADER.

var col = [];
for (var key in data){
  col.push(key)
};

// CREATE DYNAMIC TABLE.
var table = document.createElement("table");
table.id='sel'
// CREATE HTML TABLE HEADER ROW USING THE EXTRACTED HEADERS ABOVE.

var tr = table.insertRow(-1);                   // TABLE ROW.

for (var i = 0; i < col.length; i++) {
    var th = document.createElement("th");      // TABLE HEADER.
    th.innerHTML = col[i];
    tr.appendChild(th);
};

//CREATE ROWS
for (var i = 0; i < Object.keys(data).length; i++) {
    tr = table.insertRow(-1);
    for (var j = 0; j < col.length; j++) {
        var tabCell = tr.insertCell(-1);
        tabCell.innerHTML = "";
    }
};

// FINALLY ADD THE NEWLY CREATED TABLE WITH JSON DATA TO A CONTAINER.
var divContainer = document.getElementById("selenzyme_table");
divContainer.innerHTML = "";
divContainer.appendChild(table);

for (var c=0; c < col.length;c++){
  L=Object.values(data[col[c]])

$("table[id='sel'] tr td:nth-child("+(c+1)+")").each(function(i){
    $(this).text(L[i])
  });

  // COLUMN WITH THE UNIPROT LINK
  if (c===1){
    $("table[id='sel'] tr td:nth-child("+(c+1)+")").each(function(i){
        url="https://www.uniprot.org/uniprot/"+L[i]
        $(this).html('<a target="_blank "href='+url+'>'+L[i]+'</a>' )
      });
  };
};
};


  $( "#interaction" ).draggable();
  $( "#information" ).draggable();
  $("#zoom").draggable();

  $(":checkbox").change(function(){
    var select_path=[]
    $(':checkbox:checked').each(function(){
      value=$(this).val();
      select_path.push(value)});
      console.log(select_path);
    displaynet(select_path);
    change_color();
  });

  $("#all_button").click(function(){
    $(':checkbox').each(function() {
      this.checked = true;  });
    displaynet(["all"]);
  });

  $("#none_button").click(function(){
    $(':checkbox').each(function() {
      this.checked = false;  });
    displaynet([""]);
  });

  $("#close_button").click(function(){
    $("#information").hide("slide", {direction: "right" }, 1000);
  });

  $("#close_button_img").click(function(){
    $("#zoom").hide("slide", {direction: "right" }, 1000);
  });

  $("#new_window").click(function(){
    if(!window.opener) {
      window.open(window.location.href, '_blank')};
  });

  $("#hide_inter").click(function(){
      $("#interaction").toggle();
    });

  $("#selectbox").change(function(){ //UPLOAD SCORE COLUMN
      $("#table_path th:last-child, #table_path td:last-child").remove(); //remove the last column
      value=$("#selectbox :selected").val(); //Score chosen
      text=$("#selectbox :selected").text(); //score chosen
      $('#table_path').find('tr').each(function(index){ //for each row
        path_id=$(this).find('td').eq(0).text().trim() //name of the path for each row (result of previous sorts) Trim() to delete escapes
        $(this).find('th').eq(-1).after('<th class="pointer">'+text+'</th>'); //update score column name
        $(this).find('td').eq(-1).after('<td>'+scores[value][path_id]+'</td>'); //update score
      });
      sortTabledesc()
      change_color();
  });

  var sort="desc"

  $("#table_path").on('click','th:eq(-1)',function(){
    if (sort==="asc"){
      sortTabledesc();
      sort="desc";
      return false;};
    if (sort==="desc"){
      sortTableacs();
      sort="asc"};
    });

  function sortTableacs(){
  var rows = $('#table_path tbody  tr').get();
  text='\u2193'+$("#selectbox :selected").text(); //to add the edge for the sort
  $("#table_path th:eq(-1)").html(text);

  rows.sort(function(a, b) {

      var A = parseFloat($(a).children('td').eq(-1).text().toUpperCase()); //really important to compare float and not str !
      var B = parseFloat($(b).children('td').eq(-1).text().toUpperCase());

      if(A <= B) {
      return -1;
      }

      if(A > B) {
      return 1;
      }
      return 0;

      });

  $.each(rows, function(index, row) {
  $('#table_path tbody').append(row);
  });
};

  function sortTabledesc(){
  var rows = $('#table_path tbody  tr').get();
  text='\u2191'+$("#selectbox :selected").text(); //to add the edge for the sort
  $("#table_path th:eq(-1)").html(text);

  rows.sort(function(a, b) {

      var A = parseFloat($(a).children('td').eq(-1).text().toUpperCase()); //really important to compare float and not str !
      var B = parseFloat($(b).children('td').eq(-1).text().toUpperCase());

      if(A <= B) {
      return 1;
      }

      if(A > B) {
      return -1;
      }
      return 0;

      });

  $.each(rows, function(index, row) {
  $('#table_path tbody').append(row);
  });
};

$("#rule_button").click(function(){
  $("#rule").toggle()
});

$("#thermo_button").click(function(){
  $("#thermo").toggle()
});

$("#flux_button").click(function(){
  $("#flux").toggle()
});


$("#reset_color_button").click(function(){
  reset_col();
});

$("#gradient_color_button").click(function(){
  change_color();
});

function reset_col(){  //To restore original colours
    cy.$('node[category="reaction"]').forEach(function(ele)  {
      ele.style("background-color",ele.data("colour"))
    });
    cy.edges().forEach(function(ele){
      ele.style("line-color",ele.data("colour"))
    });
};

function change_color(){
  value=$("#selectbox :selected").val();
  col_dic='col_'+value;
  if (value !="Choose_a_score"){
  cy.$('node[category="reaction"]').forEach(function(ele){
      path=Object.keys(ele.data("pathway"))[0]; //to get the pathway of the node
      ele.style("background-color",scores_col[col_dic][path]);
    });
  cy.edges().forEach(function(ele){
      path=ele.data("pathway");
      console.log(path)
      ele.style("line-color",scores_col[col_dic][path]);
  });
    };
  };


});
