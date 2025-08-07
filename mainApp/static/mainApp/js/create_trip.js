document.addEventListener('DOMContentLoaded', function () {
  const totalForms = document.getElementById('id_form-TOTAL_FORMS');
  const addFormBtn = document.getElementById('add-form');
  const formContainer = document.getElementById('form-container');
  const formTemplate = document.getElementById('form-template').innerHTML;

  let formIndex = parseInt(totalForms.value);
  let lastSelectedStationName = '';

  addFormBtn.addEventListener('click', function () {
    const forms = formContainer.querySelectorAll('.form-fields-add-trip');
    const lastForm = forms[forms.length - 1];


    const lastToCitySelect = lastForm.querySelector('select.to-city');
    const cityOptionsHTML = lastToCitySelect ? lastToCitySelect.innerHTML : '';

    const selectedCityText = lastToCitySelect?.selectedOptions[0]?.text || '';


    let newFormHTML = formTemplate
      .replace(/__prefix__/g, formIndex)
      .replace(/__ORDER__/g, formIndex + 1)
      .replace(/__CITY_OPTIONS__/g, cityOptionsHTML)
      .replace(/__FROM_CITY_TEXT__/g, selectedCityText)
      .replace(/__FROM_PLACE_TEXT__/g, lastSelectedStationName || '');


    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = newFormHTML;
    formContainer.appendChild(tempDiv.firstElementChild);


    totalForms.value = formIndex + 1;


    attachCityListeners(formIndex);

    formIndex++;
  });

  function loadStations(cityId, placeSelect) {
    if (!cityId) return;
    fetch(`/api/get-stations/?city_id=${cityId}`)
      .then(response => response.json())
      .then(data => {
        placeSelect.innerHTML = '<option value="">-- оберіть зупинку --</option>';
        data.stations.forEach(station => {
          const option = document.createElement('option');
          option.value = station.id;
          option.textContent = station.name;
          placeSelect.appendChild(option);
        });

        placeSelect.addEventListener('change', () => {
          const selectedOption = placeSelect.options[placeSelect.selectedIndex];
          if (selectedOption) {
            lastSelectedStationName = selectedOption.textContent;
          }
        });
      });
  }

  function attachCityListeners(index) {
    const fromCity = document.querySelector(`.from-city-${index}`);
    const toCity = document.querySelector(`.to-city-${index}`);

    if (fromCity) {
      fromCity.addEventListener('change', function () {
        const pair = `from-city-${index}`;
        const placeSelect = document.querySelector(`.from-place-select[data-pair="${pair}"]`);
        loadStations(this.value, placeSelect);
      });
    }

    if (toCity) {
      toCity.addEventListener('change', function () {
        const pair = `to-city-${index}`;
        const placeSelect = document.querySelector(`.to-place-select[data-pair="${pair}"]`);
        loadStations(this.value, placeSelect);
      });
    }
  }


  for (let i = 0; i < formIndex; i++) {
    attachCityListeners(i);
  }
});
