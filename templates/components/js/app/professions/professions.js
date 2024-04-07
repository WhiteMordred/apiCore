
//---------------------------------------------------------------//
// START DataTable 
//---------------------------------------------------------------//

var table = $('#datatableDefault').DataTable({
  "processing": true,
  "serverSide": false,
  "ajax": {
    "url": "/professions_api/professions",
    "type": "GET",
    "dataSrc": ""
  },
  "columnDefs": [
    {
      "targets": 0,
      "checkboxes": {
        "selectRow": true
      },
      "orderable": false
    }
  ],
  "select": {
    "style": 'multi',
    "selector": 'td:first-child'
  },
  "columns": [
    {
      "data": null,
      "className": 'select-checkbox',
      "orderable": false,
      "defaultContent": '',
      "width": "30px",
    },
    { "data": "profession_id", "visible": false },
    { "data": "name" },
    {
      "data": null,
      "render": function (data, type, row) {
        return "<button class='btn btn-outline-info me-1'  data-id='" + data.profession_id + "' onclick='OpenModalInfo(this)'><i class='fa-solid fa-eye'></i></button>" +
          "<button class='btn btn-outline-warning me-1' data-id='" + data.profession_id + "' onclick='OpenModalEdit(this)' ><i class='fa-solid fa-pen'></i></button>" +
          "<button class='btn btn-outline-danger' data-id='" + data.profession_id + "' data-name='" + data.name + "' onclick='OpenModalDel(this)'><i class='fa-solid fa-trash'></i></button>";
      }
    }
  ],
  "dom": "<'row mb-3'<'col-sm-4'l><'col-sm-8 text-end'<'d-flex justify-content-end'fB>>>t<'d-flex align-items-center'<'me-auto'i><'mb-0'p>>",
  "lengthMenu": [10, 20, 30, 40, 50],
  "responsive": true,
  "buttons": [
    {
      extend: 'print',
      className: 'btn btn-outline-default btn-sm ms-1 me-1 mb-1',
      text: '<i class="fa fa-print"></i> Imprimer'
    },
    {
      extend: 'csv',
      className: 'btn btn-outline-default btn-sm me-1 mb-1',
      text: '<i class="fa fa-file-csv"></i> Exporter'
    },
    {
      text: '<i class="fa fa-upload"></i> Impoter',
      className: 'btn btn-outline-default btn-sm me-1 mb-1',
      action: function (e, dt, node, config) {
        $('#modalCoverImport').modal('show');
      }
    },
    {
      text: '<i class="fa fa-plus"></i> Ajouter',
      className: 'btn btn-outline-theme btn-sm bg-none me-1 mb-1',
      action: function (e, dt, node, config) {
        $('#modalCoverAdd').find('input').val('');
        $('#modalCoverAdd').modal('show');
      }
    },
    {
      text: '<i class="fa fa-trash"></i> Supprimer',
      className: 'btn btn-outline-danger btn-sm bg-none mb-1',
      action: function (e, dt, node, config) {
        var selectedRows = table.rows({ selected: true }).data();
        if (selectedRows.length > 0) {
          updateSelectedProfessionsList(selectedRows); 
          $('#modalCoverDeleteAll').data('selectedRows', selectedRows);
          $('#modalCoverDeleteAll').modal('show');
        } else {
          alert('Veuillez sélectionner au moins une ligne.');
        }
      }
    }
  ],
  "language": {
    "search": "Recherche :",
    "lengthMenu": "Afficher _MENU_ éléments",
    "zeroRecords": "Aucun enregistrement trouvé",
    "info": "Affichage de _START_ à _END_ sur _TOTAL_ éléments",
    "infoEmpty": "Aucun élément disponible",
    "infoFiltered": "(filtré de _MAX_ éléments au total)",
    "paginate": {
      "first": "Premier",
      "last": "Dernier",
      "next": "Suivant",
      "previous": "Précédent"
    }
  }

});

function updateSelectedProfessionsList() {
  var selectedRows = table.rows({ selected: true }).data();
  var listContainer = $('#selectedProfessionsList');
  listContainer.empty(); 
  selectedRows.each(function(rowData) {
      var professionName = rowData.name; 
      listContainer.append('<li>' + professionName + '</li>'); 
  });
}
function confirmDeletion() {
  var selectedRows = $('#modalCoverDeleteAll').data('selectedRows');
  $('#modalCoverDeleteAll').modal('hide'); 
  $('#modalSpinnerDelete').modal('show'); 
  deleteSelectedRows(selectedRows);   
}
function deleteSelectedRows() {
  var selectedRows = table.rows({ selected: true }).data();
  var numberOfRows = selectedRows.length;

  if (numberOfRows === 0) {
      alert('Veuillez sélectionner au moins une ligne.');
      return;
  }

  var processedCount = 0;
  $('#modalCoverDeleteAll').modal('hide');
  for (var i = 0; i < numberOfRows; i++) {
      (function(index) {
          setTimeout(function() {
              var rowData = selectedRows[index];
              console.log('Row Data:', rowData);
              var id = rowData.profession_id;

              if (id) {
                  fetch('/professions_api/professions/' + id, {
                      method: 'DELETE',
                      headers: {
                          'Content-Type': 'application/json'
                      }
                  })
                  .then(response => {
                      if (response.ok) {
                          console.log('Métier supprimé avec succès:', id);
                      } else {
                          console.error('Erreur lors de la suppression du métier:', id);
                      }
                  })
                  .catch(error => {
                      console.error('Erreur lors de l\'envoi de la requête:', error);
                  })
                  .finally(() => {
                      processedCount++;
                      if (processedCount === numberOfRows) {
                        $('#modalSpinnerDelete').modal('hide');
                          table.ajax.reload();
                      }
                  });
              } else {
                  console.error('ID métier non trouvé:', rowData);
                  processedCount++;
              }
          }, 500 * index);
      })(i);
  }
}

//---------------------------------------------------------------//
// STOP DataTable 
//---------------------------------------------------------------//

//---------------------------------------------------------------//
// START Add Modal 
//---------------------------------------------------------------//
document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('modal_add');
  const submitButton = document.getElementById('modal_submit_add');

  form.addEventListener('submit', function (event) {
    event.preventDefault();
    const name = document.getElementById('name').value;
    const professionData = {
      name: name,
    };
    fetch('/professions_api/professions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(professionData)
    })
      .then(response => {
        if (response.ok) {
          console.log('Métier ajouté avec succès');
          $('#modalCoverAdd').modal('hide');
          table.ajax.reload();

        } else {
          console.error('Erreur lors de l\'ajout du métier');
          $('#modalCoverAdd').modal('hide');
          table.ajax.reload();
        }
      })
      .catch(error => {
        console.error('Erreur lors de l\'envoi de la requête:', error);
      });
  });
});

//---------------------------------------------------------------//
// STOP Add Modal 
//---------------------------------------------------------------//

//---------------------------------------------------------------//
// START Info Modal 
//---------------------------------------------------------------//
function OpenModalInfo(data) {
  var profession_id = data.getAttribute('data-id')
  fetch('/professions_api/professions/' + profession_id, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    }
  })
    .then(response => {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error('Erreur lors de la récupération des données métier');
      }
    })
    .then(professionData => {
      $('#modalCoverInfo').find('#infoId').val(professionData.profession_id);
      $('#modalCoverInfo').find('#infoName').val(professionData.name);
      $('#modalCoverInfo').modal('show');
    })
    .catch(error => {
      console.error('Erreur:', error);
    });

}

//---------------------------------------------------------------//
// STOP Info Modal 
//---------------------------------------------------------------//

//---------------------------------------------------------------//
// START Edit Modal 
//---------------------------------------------------------------//
function OpenModalEdit(data) {
  var profession_id = data.getAttribute('data-id')
  fetch('/professions_api/professions/' + profession_id, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    }
  })
    .then(response => {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error('Erreur lors de la récupération des données métier');
      }
    })
    .then(professionData => {
      $('#modalCoverEdit').find('#editId').val(professionData.profession_id);
      $('#modalCoverEdit').find('#editName').val(professionData.name);
      $('#modalCoverEdit').modal('show');
    })
    .catch(error => {
      console.error('Erreur:', error);
    });

}

document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('modal_edit');
  const submitButton = document.getElementById('modal_submit_edit');

  form.addEventListener('submit', function (event) {
    event.preventDefault();
    const id = document.getElementById('editId').value;
    const name = document.getElementById('editName').value;

    const professionData = {
      profession_id: id,
      name: name
    };
    fetch('/professions_api/professions/' + id, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(professionData)
    })
      .then(response => {
        if (response.ok) {
          console.log('Métier modifié avec succès');
          $('#modalCoverEdit').modal('hide');
          table.ajax.reload();

        } else {
          console.error('Erreur lors de la modification du métier');
          $('#modalCoverEdit').modal('hide');
          table.ajax.reload();
        }
      })
      .catch(error => {
        console.error('Erreur lors de l\'envoi de la requête:', error);
      });
  });
});

//---------------------------------------------------------------//
// STOP Edit Modal 
//---------------------------------------------------------------//

//---------------------------------------------------------------//
// START Del Modal 
//---------------------------------------------------------------//
function OpenModalDel(data) {
  var profession_id = data.getAttribute('data-id')
  var name = data.getAttribute('data-name')
  document.getElementById('modal_submit_del_profession').value = profession_id;
  document.getElementById('modalDelName').innerText = name;
  var modalElement = document.getElementById('modalCoverDelete');
  var modal = new bootstrap.Modal(modalElement);
  modal.show();
}

function ValidateDel(data) {
  var id = data.value
  fetch('/professions_api/professions/' + id, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json'
    }
  })
    .then(response => {
      if (response.ok) {
        console.log('Métier supprimer avec succès');
        $('#modalCoverDelete').modal('hide');
        table.ajax.reload();

      } else {
        console.error('Erreur lors de la suppresion  du métier');
        $('#modalCoverDelete').modal('hide');
        table.ajax.reload();
      }
    })
}

//---------------------------------------------------------------//
// STOP Del Modal 
//---------------------------------------------------------------//

//---------------------------------------------------------------//
// START Import Modal 
//---------------------------------------------------------------//
document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('modal_import');
  const fileInput = document.getElementById('importFile');

  form.addEventListener('submit', function (event) {
    event.preventDefault();
    const file = fileInput.files[0];

    if (file) {
      $('#modalCoverImport').modal('hide');
      $('#modalSpinner').modal('show');

      const reader = new FileReader();
      reader.onload = function (e) {
        const text = e.target.result;
        const lines = text.split('\n').filter((line, index) => line.trim() && index > 0);
        let processedCount = 0;

        lines.forEach((line, index) => {
          setTimeout(() => {
            const name = line.trim();
            if (name) {
              const professionData = {
                name: name
              };

              fetch('/professions_api/professions', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json'
                },
                body: JSON.stringify(professionData)
              })
              .finally(() => {
                processedCount++;
                if (processedCount === lines.length) {
                  $('#modalSpinner').modal('hide');
                  table.ajax.reload();
                }
              });
            } else {
              console.error('Format de ligne incorrect:', line);
              processedCount++;
            }
          }, 1000 * index);
        });
      };

      reader.readAsText(file);
    }
  });
});
//---------------------------------------------------------------//
// STOP Import Modal 
//---------------------------------------------------------------//



