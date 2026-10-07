$(document).ready(function() {
    $('#tablaResenas').DataTable({
        responsive: true,
        dom: "<'row mb-3 align-items-center'<'col-sm-12 col-md-6 d-flex gap-2'B><'col-sm-12 col-md-6 d-flex justify-content-md-end mt-2 mt-md-0'f>>" +
             "<'row'<'col-sm-12'tr>>" +
             "<'row mt-3 align-items-center'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7 d-flex justify-content-md-end mt-2 mt-md-0'p>>",
        buttons: [
            {
                extend: 'excelHtml5',
                text: '<i class="bi bi-file-earmark-excel me-1"></i> Excel',
                className: 'btn btn-success btn-sm shadow-sm',
                exportOptions: { columns: ':not(:last-child)' }
            },
            {
                extend: 'pdfHtml5',
                text: '<i class="bi bi-file-earmark-pdf me-1"></i> PDF',
                className: 'btn btn-danger btn-sm shadow-sm',
                exportOptions: { columns: ':not(:last-child)' }
            }
        ],
        columnDefs: [
            { orderable: false, targets: -1 }
        ],
        pageLength: 10,
        language: {
            processing: "Procesando...",
            lengthMenu: "Mostrar _MENU_ registros",
            zeroRecords: "No se encontraron resultados",
            emptyTable: "No hay reseñas registradas",
            info: "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ reseñas",
            infoEmpty: "Mostrando 0 de 0 reseñas",
            infoFiltered: "(filtrado de un total de _MAX_ reseñas)",
            search: "Buscar:",
            paginate: {
                first: "Primero",
                last: "Último",
                next: "Siguiente",
                previous: "Anterior"
            }
        }
    });
});
