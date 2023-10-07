
var formattedDateTime;
var click_count = 0;
function clickEventHandler(e){
  var id = e.target.id
  var count = id.slice(-1)
  console.log(click_count)
  if(e.target.matches("#req")){
      if(e.target.checked == true){
          $("#reqo")
              .text("YES")
              .attr('style','font-weight: bold; color: green; margin-left:40%;')
          document.getElementById("submitBtn").setAttribute("disabled","disabled")
          addInputs()
          
      }else{
          $("#dyna_row").remove()
          $("#reqo")
          .text('NO')
          .attr('style','font-weight: bold; color: red;')
          click_count = 0
          $("#db").find('li').remove()
          document.getElementById("submitBtn").removeAttribute("disabled")
          document.getElementById("submitBtn").addEventListener("click",clickEventHandler)
          M.toast({html: 'You have selected "No Changes Found". If you are sure, you can Submit the form', classes: 'red darken-4 text-white rounded'});
      }
  }
  if(e.target.matches("#adbtn")){
    var parentElement = document.getElementById("dyna_row");
    console.log("add btn clicked")            
    var childElements = parentElement.querySelectorAll("*");
    var valid = "True"     
    var input_value = []
    childElements.forEach(function(childElement) {
        var reqfield = childElement.getAttribute("required")
        var reqid = childElement.getAttribute("id")
        // console.log(reqid)
        if(reqfield != null){
            // console.log(document.getElementById(reqid).value)
            if(document.getElementById(reqid).value == ""){
                // console.log('#span_'+reqid)
                $('#span_'+reqid)
                    .text('Invalid Input. Please check')
                    .attr('style','color:red; font-size:600')
                valid = "False"
            }
            else{
                $('#span_'+reqid)
                    .text('')
                    .attr('style','')
            }                    
        }
    });
    if(valid != "False"){
        childElements.forEach(function(childElement){
            var childId = childElement.getAttribute("for");
            var elem = document.getElementById(childId)
            if (childId !== null) {
                if(elem.type == "select-multiple"){
                    sel_value = ""
                    for(i=0;i<elem.selectedOptions.length;i++){
                        sel_value = sel_value + elem.selectedOptions[i].value + ","
                    }
                    input_value.push(sel_value)
                    elem.selectedIndex = -1
                    elem.parentElement.firstChild.value = ""
                }else if(elem.type == "select-one"){
                    input_value.push(elem.value)
                    elem.selectedIndex = -1
                    elem.parentElement.firstChild.value = ""
                }else{
                    input_value.push(elem.value)
                    elem.value = ""
                }
            }
        })
        addCollapsible(input_value)
       
        $(document).ready(function(){
            $('.collapsible').collapsible();
        });
    }
    // click_count++
  }
  if(e.target.matches("#rmbtn_"+count)){
      $("#li_"+count).remove()
  }
  if(e.target.matches("#submitBtn")){
    data = []
    var parentElement = document.getElementById("main_div");
    var childElements = parentElement.querySelectorAll("*");
    for(i = 0; i< click_count; i++){
      var rowData = {}
      childElements.forEach(function(childElement) {
        var reqfield = childElement.getAttribute("required")
        var reqid = childElement.getAttribute("id")
        if(reqfield !== null && !reqid.startsWith("ts_")){
          if(document.getElementById(reqid).value != null){
            rowData[document.getElementById(reqid).getAttribute("name")] = document.getElementById(reqid).value
          }else if(reqfield == null || reqid.startsWith("date_"+i)){
            rowData[document.getElementById(reqid).getAttribute("name")] = document.getElementById(reqid).textContent
          }          
        }else if(reqfield !== null && reqid.startsWith("ts_"+(i+1))){
          if(document.getElementById(reqid).value != null){
            rowData[document.getElementById(reqid).getAttribute("name")] = document.getElementById(reqid).value
          }else{
            rowData[document.getElementById(reqid).getAttribute("name")] = document.getElementById(reqid).textContent
          } 
        }
        rowData['clickCount'] = click_count
      })
      data.push(rowData)
    }
      
    console.log(data)
    fetch('/submit_data_to_python', {
      method: 'POST',
      body: JSON.stringify(data),
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => response.json())
    .then(data => {
      $("#dyna_row").remove()
      $("#reqo")
        .text('NO')
        .attr('style','font-weight: bold; color: red;')
      document.getElementById("req").checked = false
      click_count = 0
      $("#db").find('li').remove()
      document.getElementById("submitBtn").removeAttribute("disabled")
      document.getElementById("submitBtn").addEventListener("click",clickEventHandler)
      M.toast({html: 'Your Task is completed. You can now close this window.', classes: 'green darken-4 text-white rounded'});

    })
    .catch(error => {
      M.toast({html: 'There was an error submitting your response. Please try again. Error: '+error, classes: 'red darken-4 text-white rounded'});
    });
  }
}
function changeEventHandler(e){
  var id = e.target.id
  var count = id.slice(-1)
  console.log(click_count)
  if(e.target.matches("#module_"+click_count)){
      console.log(e.target.value)
      var mod = e.target.value
      var pro_elem = document.getElementById("processes_"+click_count)
      var pinstance = M.FormSelect.getInstance(pro_elem);
      var pdata = process.filter(function(r){ return r[1] == mod})
      pinstance.destroy();
      pro_elem.innerHTML = ""
      M.FormSelect.init(pro_elem);
      uniqueDropdown(pro_elem,pdata,3)
      var task_elem = document.getElementById("tasks_"+click_count)
      var tinstance = M.FormSelect.getInstance(task_elem);
      var tdata = task.filter(function(r){ return r[1] == mod})
      tinstance.destroy();
      task_elem.innerHTML = ""
      M.FormSelect.init(task_elem);
      uniqueDropdown(task_elem,tdata,4)

  }
}
function uniqueDropdown(el,data,index){
  $(document).ready(function(){
    $('select').formSelect();
  });
  var currentlyAdded = [];
  data.forEach(function(r){
    if(currentlyAdded.indexOf(r[index]) === -1){
      var option = document.createElement("option");
      option.textContent = r[index];
      el.appendChild(option);
      currentlyAdded.push(r[index]);
    }
  });
}
function addInputs(){
  $.ajax({
      url: '/input_partial?clickCount='+click_count, // Replace with the correct path
      type: 'GET',
      dataType: 'html',
      success: function (partialHTML) {
          // Append the partial content to the #dyna container
          $("#dyna").append(partialHTML);
          $('select').formSelect();
          document.getElementById("adbtn").addEventListener("click",clickEventHandler)
      },
      error: function (error) {
          console.error("Error loading partial template:", error);
      }
  });
}
function addCollapsible(in_data){
  var dynamicVariables = {};
  var dt = new Date()
  const day = String(dt.getDate()).padStart(2, '0');
  const month = dt.toLocaleString('default', { month: 'short' });
  const year = dt.getFullYear();
  const hours = String(dt.getHours()).padStart(2, '0');
  const minutes = String(dt.getMinutes()).padStart(2, '0');
  const seconds = String(dt.getSeconds()).padStart(2, '0');
  formattedDateTime = `${day}-${month}-${year} ${hours}:${minutes}:${seconds}`;
  
  $("#db")
    .append($('<li>')
      .attr('id','li_'+click_count)
      .attr('style','margin-top:-1.5%;')
      .append($('<div>')
        .attr('class','collapsible-header row')
        .attr('id','coldiv_'+click_count)
        .append($('<i>')
          .attr('class','material-icons')
          .text('storage')
        )
      )
      .append($('<div>')
          .attr('class','collapsible-body row')
          .attr('id','data_'+click_count)
        )
    )
  for (var i = 1; i < (in_data.length/2); i++) {
    var variableName = "ini" + i;
    dynamicVariables[i] = in_data[i]
    $('#coldiv_'+click_count)
      .append($('<div>')
        .attr('class','col s2 m2')
        .text('Input '+i)
      )      
  }
  $('#coldiv_'+click_count)
    .append($('<div>')
      .attr('class','col s2 m2')
      .attr('id','date_'+click_count)
      .attr('name','date_'+click_count)
      .attr('required','required')
      .text(formattedDateTime)
    )
    .append($('<div>')
      .attr('class','col s1 m1')
      .append($('<a>')
        .attr('class','btn-floating btn-small waves-effect waves-light red')
        // .attr('style','margin-top:5%')
        .append($('<i>')
          .attr('id','rmbtn_'+click_count)
          .attr('name','rmbtn_'+click_count)
          .attr('class','material-icons')
          .text('exposure_neg_1')
        )
      )
    )
  $("#data_"+click_count)
      .append($('<div>')
        .attr('class','row')
        .attr('id','row_'+click_count)
      )
  $("#row_"+click_count)
      .append($('<div>')
        .attr('class','row')
        .attr('id','row1_'+click_count)
      )
  for (var i = 1; i < (in_data.length/2); i++){
    $("#row1_"+click_count)
      .append($('<div>')
        .attr('class','col s2 m2')
        .attr('style','word-break: break-all;')
        .attr('id','ts_'+Number(click_count+1)+'_'+i)
        .attr('name','ts_'+Number(click_count+1)+'_'+i)
        .attr('required','required')
        .text(in_data[i-1])
      )    
  }
  $("#row_"+click_count)
      .append($('<div>')
        .attr('class','row')
        .attr('id','row2_'+click_count)
      )
  for (var i = Math.floor(in_data.length/2)+1; i <= in_data.length; i++){
    $("#row2_"+click_count)
      .append($('<div>')
        .attr('class','col s2 m2')
        .attr('style','word-break: break-all;')
        .attr('id','ts_'+Number(click_count+1)+'_'+i)
        .attr('name','ts_'+Number(click_count+1)+'_'+i)
        .attr('required','required')
        // .attr('hidden','hidden')
        .text(in_data[i-1])
      )    
  }
  $('#dyna_row').remove()
  click_count++
  addInputs(function () {
    document.getElementById("rmbtn_" + click_count).addEventListener("click", clickEventHandler);
    
  });
  document.getElementById("submitBtn").removeAttribute("disabled")
  document.getElementById("submitBtn").addEventListener("click",clickEventHandler)
}
// document.addEventListener("DOMContentLoaded",function(){
//   document.getElementById("task_form").addEventListener("submit", function (event) {
//     event.preventDefault();
      
      
//   });
// })

