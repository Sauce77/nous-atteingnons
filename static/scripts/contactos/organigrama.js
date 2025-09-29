google.charts.load('current', {packages:['orgchart']});
google.charts.setOnLoadCallback(drawChart);

// Función principal para dibujar el gráfico
function drawChart() {
  
  fetch(apiUrl)
    .then(response => response.json())
    .then(data => {
      let dataTable = new google.visualization.DataTable();
      dataTable.addColumn('string', 'Name');
      dataTable.addColumn('string', 'Manager');
      dataTable.addColumn('string', 'ToolTip');
      dataTable.addColumn({type: 'string', role: 'style'}); 
      
      let allRows = [];
      processNode(data, allRows, ''); 

      dataTable.addRows(allRows);

      var chart = new google.visualization.OrgChart(document.getElementById('chart_div'));

      // Agrega el "listener" aquí
      google.visualization.events.addListener(chart, 'select', function() {
        handleNodeClick(chart, dataTable);
      });
      
      var options = { 'allowHtml': true };
      chart.draw(dataTable, options);
    })
    .catch(error => console.error('Error fetching data:', error));
}

// Función para manejar el clic en el nodo
function handleNodeClick(chart, dataTable) {

  var selection = chart.getSelection();
  if (selection.length > 0) {
    
    var rowIndex = selection[0].row;
    var nodeId = dataTable.getValue(rowIndex, 0);

    var newUrl = urlNodo.replace("0", nodeId)

    console.log(newUrl);
    
    // Redirige a la URL deseada
    window.location.href = newUrl;
  }
}

// Función recursiva (la que ya tenías)
function processNode(node, allRows, parentId) {

  const nodeData = {
    'v': node.id.toString(), 
    'f': `<b>${node.nombre} ${node.apellido_paterno}</b><br><span>${node.apellido_materno}</span>`,
  };

  let styleString = '';
  if (node.estatus === 'A') {
      styleString = 'background-color: #4CAF50; background-image: none; color: white;'; // Verde
  } else if (node.estatus === 'D') {
      styleString = 'background-color: #ff0707ff; background-image: none;'; // Amarillo
  } else {
      styleString = 'background-color: #2196F3; background-image: none;'; // Azul por defecto
  }

  allRows.push([
    nodeData,
    parentId,
    `Contactos: ${node.descendant_count}`,
    styleString,
  ]);
  
  if (node.children && node.children.length > 0) {
    node.children.forEach(child => {
      processNode(child, allRows, node.id.toString());
    });
  }
}