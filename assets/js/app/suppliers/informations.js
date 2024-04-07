//---------------------------------------------------------------//
// START Info Modal 
//---------------------------------------------------------------//
function OpenModalInfo(data) {
    var supplier_id = data.getAttribute('data-id')
    fetch('/suppliers_api/suppliers/' + supplier_id, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(response => {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error('Erreur lors de la récupération des données fournisseur');
        }
      })
      .then(supplierData => {
        //Informations Supplier
        $('#modalCoverInfo').find('#supplier_id').html(supplierData.supplier_id);
        $('#modalCoverInfo').find('#supplier_logo').attr("src",supplierData.logo_file);
        $('#modalCoverInfo').find('#supplier_name').html(supplierData.supplier_name);
        $('#modalCoverInfo').find('#short_code').html(supplierData.short_code);
        $('#modalCoverInfo').find('#description').html(supplierData.description);
        $('#modalCoverInfo').find('#address').html(supplierData.address);
        $('#modalCoverInfo').find('#city').html(supplierData.city);
        $('#modalCoverInfo').find('#zip').html(supplierData.zip);
        $('#modalCoverInfo').find('#country').html(supplierData.country);
        $('#modalCoverInfo').find('#phone').html(supplierData.phone);
        $('#modalCoverInfo').find('#website').attr("href",supplierData.website);
        $('#modalCoverInfo').on('show.bs.modal', function () {
            populateTagsMetiers(supplierData);
        });
        $('#modalCoverInfo').on('show.bs.modal', function () {
            populateTagsMarques(supplierData);
        });
        $('#modalCoverInfo').on('show.bs.modal', function () {
            populateTagsProduits(supplierData);
        });

        $('#modalCoverInfo').on('show.bs.modal', function () {
            populateContacts(supplierData);
        });

        $('#modalCoverInfo').on('show.bs.modal', function () {
            pdf_viewer(supplierData);
        });
        $('#modalCoverInfo').on('show.bs.modal', function () {
            website_viewer(supplierData);
        });

        $('#modalCoverInfo').find('#infoId').val(supplierData.supplier_id);
        $('#modalCoverInfo').find('#infoName').val(supplierData.name);
        $('#modalCoverInfo').modal('show');
      })
      .catch(error => {
        console.error('Erreur:', error);
      });
  
  }
  
  //---------------------------------------------------------------//
  // STOP Info Modal 
  //---------------------------------------------------------------//


        // Tags 
        function populateTagsMetiers(supplierData) {
            const container = $('#modalCoverInfo').find('#tags-container-professions');
            container.empty();
            supplierData.professions.forEach(tag => {
                const tagElement = $('<button>');
                tagElement.text(tag); 
                tagElement.addClass('btn btn-outline-theme btn-sm me-1 mb-1');
                container.append(tagElement);
            });
        }
        function populateTagsMarques(supplierData) {
            const container = $('#modalCoverInfo').find('#tags-container-marks');
            container.empty();
            supplierData.marks.forEach(tag => {
                const tagElement = $('<button>');
                tagElement.text(tag); 
                tagElement.addClass('btn btn-outline-theme btn-sm me-1 mb-1');
                container.append(tagElement);
            });
        }
        function populateTagsProduits(supplierData) {
            const container = $('#modalCoverInfo').find('#tags-container-products');
            container.empty();
            supplierData.products.forEach(tag => {
                const tagElement = $('<button>');
                tagElement.text(tag); 
                tagElement.addClass('btn btn-outline-theme btn-sm me-1 mb-1');
                container.append(tagElement);
            });
        }

        //Contact 

        function populateContacts(supplierData) {
            // Sélectionner la div où les informations de contact doivent être ajoutées
            const container = $('#modalCoverInfo').find('#contact_follow');
        
            // S'assurer que le conteneur est vide avant d'ajouter de nouveaux contacts
            container.empty();
        
            // Boucle sur les contacts de supplierData et créer une nouvelle liste pour chaque contact
            supplierData.contact.forEach(contact => {
                const contactElement = $('<div>').addClass('list-group-item d-flex align-items-center');
                
                // Ajouter le contenu du contact
                contactElement.append(`
                    <div class="flex-fill px-3">
                      <div><a href="#" class="text-inverse fw-bold text-decoration-none"><i class="fa-solid fa-user"></i> @${contact.name}</a></div>
                      <div class="text-inverse text-opacity-50 fs-13px"><i class="fa-solid fa-bell-concierge"></i> ${contact.service}</div>
                      <div class="text-inverse text-opacity-50 fs-13px"><i class="fa-solid fa-envelope"></i> ${contact.email}</div>
                      <div class="text-inverse text-opacity-50 fs-13px"><i class="fa-solid fa-phone"></i> ${contact.phone}</div>
                    </div>
                    <a href="mailto:${contact.email}" class="btn btn-outline-theme me-1">Email</a>
                    <a href="tel:${contact.phone}" class="btn btn-outline-theme">Téléphone</a>
                `);
        
                // Ajouter le contact à la div
                container.append(contactElement);
            });
        }
        function pdf_viewer(supplierData) {
            if (supplierData.catalog_file) {
                showPDF(supplierData.catalog_file);
            } else if (supplierData.catalog_link) {
                showPDF(supplierData.catalog_link);
            } else {
                displayNoCatalogMessage();
            }
        }
        
        function showPDF(url) {
            var pdfjsLib = window['pdfjs-dist/build/pdf'];
            pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://mozilla.github.io/pdf.js/build/pdf.worker.js';
        
            var pdfDoc = null,
                pageNum = 1,
                canvas = document.getElementById('pdf-canvas'),
                ctx = canvas.getContext('2d');
        
            function renderPage(num) {
                pdfDoc.getPage(num).then(function(page) {
                    var viewport = page.getViewport({scale: 1.5});
                    canvas.height = viewport.height;
                    canvas.width = viewport.width;
        
                    var renderContext = {
                        canvasContext: ctx,
                        viewport: viewport
                    };
                    page.render(renderContext);
                });
            }
        
            function queueRenderPage(num) {
                if (pdfDoc !== null) {
                    renderPage(num);
                }
            }
        
            pdfjsLib.getDocument(url).promise.then(function(pdfDoc_) {
                pdfDoc = pdfDoc_;
                renderPage(pageNum);
                document.getElementById('page_count').textContent = pdfDoc.numPages;
            });
        
            // Boutons de navigation
            document.getElementById('prev').addEventListener('click', function() {
                if (pageNum <= 1) {
                    return;
                }
                pageNum--;
                queueRenderPage(pageNum);
                document.getElementById('page_num').textContent = pageNum;
            });
        
            document.getElementById('next').addEventListener('click', function() {
                if (pageNum >= pdfDoc.numPages) {
                    return;
                }
                pageNum++;
                queueRenderPage(pageNum);
                document.getElementById('page_num').textContent = pageNum;
            });
        }
        
        function displayNoCatalogMessage() {
            var container = document.getElementById('pdf-viewer-container');
            if (container) {
                container.innerHTML = '<p>Pas de catalogue disponible.</p>';
            }
        }
        

        function website_viewer(supplierData) {
            var iframeContainer = document.getElementById('website_iframe');
            var websitelink = document.getElementById('website-link-viewer')
            websitelink.setAttribute('href', supplierData.website)
            iframeContainer.innerHTML = '';
            var iframe = document.createElement('iframe');
            iframe.setAttribute('src', supplierData.website);
            iframe.style.width = '100%';
            iframe.style.height = '600px';
            iframeContainer.appendChild(iframe);
        }
        
        
        