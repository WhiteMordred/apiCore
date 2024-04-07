//---------------------------------------------------------------//
// START Add Modal 
//---------------------------------------------------------------//

let currentStep = 1;

function showStep(step) {
  for (let i = 1; i <= 5; i++) {
    document.getElementById('wizardStep' + i).style.display = i === step ? 'block' : 'none';
    const navLink = document.getElementById('navLink' + i);
    if (i < step) {
      navLink.className = 'nav-link completed';
    } else if (i === step) {
      navLink.className = 'nav-link active';
    } else {
      navLink.className = 'nav-link';
    }
  }
  currentStep = step;

  switch(step) {
    case 3:
      fetchMetiers();
      fetchMarques();
      fetchProduits();
      break;
  }
}

function fetchMetiers() {
  fetch('/professions_api/professions')
    .then(response => response.json())
    .then(data => {
      console.log(data)
      updateMetierPicker(data);
    })
    .catch(error => console.error('Erreur lors de la récupération des métiers:', error));
}

function updateMetierPicker(data) {
  const select = document.getElementById('professions-select');

  data.forEach(d => {
    const option = document.createElement('option');
    option.value = d.name;
    option.textContent = d.name; 
    select.appendChild(option);
  });
  jQuery('#professions-select').picker({
    search: true,
    texts: {
        trigger: "Choisir un ou des métier(s)", 
        noResult: "Aucun résultat", 
        search: "Rechercher"
    }
});
}


function fetchMarques() {
  fetch('/marks_api/marks')
    .then(response => response.json())
    .then(data => {
      console.log(data)
      updateMarquePicker(data);
    })
    .catch(error => console.error('Erreur lors de la récupération des marques:', error));
}

function updateMarquePicker(data) {
  const select = document.getElementById('marks-select');

  data.forEach(d => {
    const option = document.createElement('option');
    option.value = d.name;
    option.textContent = d.name; 
    select.appendChild(option);
  });
  jQuery('#marks-select').picker({
    search: true,
    texts: {
        trigger: "Choisir une ou des marque(s)", 
        noResult: "Aucun résultat", 
        search: "Rechercher"
    }
});
}

function fetchProduits() {
  fetch('/products_api/products')
    .then(response => response.json())
    .then(data => {
      console.log(data)
      updateProduitPicker(data);
    })
    .catch(error => console.error('Erreur lors de la récupération des produits:', error));
}

function updateProduitPicker(data) {
  const select = document.getElementById('products-select');

  data.forEach(d => {
    const option = document.createElement('option');
    option.value = d.name;
    option.textContent = d.name; 
    select.appendChild(option);
  });
  jQuery('#products-select').picker({
    search: true,
    texts: {
        trigger: "Choisir un ou des produit(s)", 
        noResult: "Aucun résultat", 
        search: "Rechercher"
    }
});
}

function goToNextStep(event) {
  event.preventDefault();
  if (currentStep < 5) {
    showStep(currentStep + 1);
  }
}

function goToPreviousStep(event) {
  event.preventDefault();
  if (currentStep > 1) {
    showStep(currentStep - 1);
  }
}

showStep(1);

$('.summernote').summernote({
  height: 200
});

document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('modal_add');
  const submitButton = document.getElementById('modal_submit_add');

  form.addEventListener('submit', function (event) {
    event.preventDefault();

    const contactsData = [];
    document.querySelectorAll('.contact-card').forEach(card => {
        const contactName = card.querySelector('[placeholder="Dupont Bernard"]').value;
        const contactPhone = card.querySelector('[placeholder="01 00 00 00 00"]').value;
        const contactEmail = card.querySelector('[placeholder="name@example.com"]').value;
        const contactServiceSelect = card.querySelector('.service-select'); // Utilisez une classe ou un ID approprié pour votre élément select
        const contactService = contactServiceSelect ? contactServiceSelect.value : '';

        contactsData.push({
            name: contactName,
            phone: contactPhone,
            email: contactEmail,
            service: contactService
        });
    });


    // Collecter les données de toutes les étapes
    const supplierData = {
      supplier_name: document.getElementById('supplier_name').value,
      website: document.getElementById('website').value,
      short_code: document.getElementById('short_code').value,
      contact: contactsData,
      phone: document.getElementById('phone').value,
      professions: Array.from(document.getElementById('professions-select').selectedOptions).map(option => option.value),
      marks: Array.from(document.getElementById('marks-select').selectedOptions).map(option => option.value),
      products: Array.from(document.getElementById('products-select').selectedOptions).map(option => option.value),
      catalog_link: document.getElementById('catalog_link').value,
      catalog_file: document.getElementById('catalog_file_path').value,
      logo_link: document.getElementById('logo_link').value,
      logo_file: document.getElementById('logo_file_path').value,
      min_cmd: document.getElementById('min_cmd').value,
      freq_cmd: document.getElementById('freq_cmd').value,
      description: document.getElementById('description').value,
      address:document.getElementById('address').value ,
      city:document.getElementById('city').value,
      zip:document.getElementById('zip').value,
      country:document.getElementById('country').value
    };

    fetch('/suppliers_api/suppliers', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(supplierData)
    })
      .then(response => {
        if (response.ok) {
          console.log('Fournisseur ajouté avec succès');
          $('#modalCoverAdd').modal('hide');
          location.reload() 
        } else {
          console.error('Erreur lors de l\'ajout du fournisseur');
          $('#modalCoverAdd').modal('hide');
          location.reload() 
        }
      })
      .catch(error => {
        console.error('Erreur lors de l\'envoi de la requête:', error);
      });
  });
});
document.getElementById('catalog_file').addEventListener('change', function(event) {
  const file = event.target.files[0];
  const formData = new FormData();
  formData.append('file', file);

  fetch('/suppliers_api/upload_catalog', {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    if (data.file_path) {
      // Stockez le chemin du fichier dans un champ caché ou une variable
      document.getElementById('catalog_file_path').value = data.file_path;
    }
  })
  .catch(error => console.error('Erreur lors de l\'envoi du fichier:', error));
});
document.getElementById('logo_file').addEventListener('change', function(event) {
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append('file', file);
  
    fetch('/suppliers_api/upload_logo', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      if (data.file_path) {
        // Stockez le chemin du fichier dans un champ caché ou une variable
        document.getElementById('logo_file_path').value = data.file_path;
      }
    })
    .catch(error => console.error('Erreur lors de l\'envoi du fichier:', error));
  });
  

//---------------------------------------------------------------//
// STOP Add Modal 
//---------------------------------------------------------------//


document.addEventListener('DOMContentLoaded', function () {
    const contactsContainer = document.getElementById('contacts-container');
    const addContactBtn = document.getElementById('add-contact-btn');

    // Récupérer les données des services
    fetchServices();

    addContactBtn.addEventListener('click', function() {
        addContactCard();
    });

    function fetchServices() {
        fetch('/services_api/services')
            .then(response => response.json())
            .then(services => {
                window.servicesData = services; // Stocker les données globalement
            })
            .catch(error => console.error('Erreur lors de la récupération des services:', error));
    }

    function addContactCard() {
        const card = document.createElement('div');
        card.classList.add('card', 'contact-card');
        card.innerHTML = `
            <div class="card-body">
                <div class="form-group mb-3">
                    <label>Nom du contact</label>
                    <input type="text" class="form-control" placeholder="Dupont Bernard">
                </div>
                <div class="row">
                    <div class="form-group mb-3 col-6">
                        <label>Téléphone</label>
                        <input type="text" class="form-control" placeholder="01 00 00 00 00">
                    </div>
                    <div class="form-group mb-3 col-6">
                        <label>Email</label>
                        <input type="email" class="form-control" placeholder="name@example.com">
                    </div>
                </div>
                <div class="form-group mb-3">
                    <label>Service</label>
                    <select class="form-control service-select">${populateServiceOptions()}</select>
                </div>
                <div class="row mb-3 d-flex justify-content-center">
                    <button type="button" class="remove-contact-btn btn btn-outline-danger w-50" ><i class="fa-solid fa-trash"></i></button>
                </div>
            </div>
            <div class="card-arrow">
                <div class="card-arrow-top-left"></div>
                <div class="card-arrow-top-right"></div>
                <div class="card-arrow-bottom-left"></div>
                <div class="card-arrow-bottom-right"></div>
            </div>
        `;

        const removeBtn = card.querySelector('.remove-contact-btn');
        removeBtn.addEventListener('click', function() {
            card.remove();
        });

        contactsContainer.appendChild(card);
    }

    function populateServiceOptions() {
        return window.servicesData.map(service => `<option value="${service.name}">${service.name}</option>`).join('');
    }
});
