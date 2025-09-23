google.charts.load('current', {packages:['orgchart']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
  
  fetch(apiUrl)
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      // Prepara el DataTable
      var dataTable = new google.visualization.DataTable();
      dataTable.addColumn('string', 'Name');
      dataTable.addColumn('string', 'Manager');
      dataTable.addColumn('string', 'ToolTip');

      // Crea un array para almacenar todas las filas aplanadas
      let allRows = [];
      
      // Llama a la función recursiva para procesar el nodo raíz
      processNode(data, allRows, ''); 

      // Agrega todas las filas al DataTable de una vez
      dataTable.addRows(allRows);

      // Dibuja el gráfico
      var chart = new google.visualization.OrgChart(document.getElementById('chart_div'));
      chart.draw(dataTable, { 'allowHtml': true });
    })
    .catch(error => console.error('Error fetching data:', error));
}

// Función recursiva para aplanar la estructura del JSON
function processNode(node, allRows, parentId) {
  // Crea el nodo para la persona actual
  const nodeData = {
    'v': node.id.toString(), 
    'f': `<b>${node.nombre} ${node.apellido_paterno}</b><br><span>${node.apellido_materno}</span>`
  };
  
  // Agrega la fila actual al array
  allRows.push([
    nodeData,
    parentId, // Usa el ID del padre pasado como argumento
    `Alcance: ${node.descendant_count}`
  ]);
  
  // Si tiene hijos, llama a la función recursivamente para cada uno
  if (node.children && node.children.length > 0) {
    node.children.forEach(child => {
      // El ID de este nodo se convierte en el padre para sus hijos
      processNode(child, allRows, node.id.toString());
    });
  }
}